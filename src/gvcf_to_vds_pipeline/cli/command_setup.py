import argparse
import json
from pathlib import Path

import hail as hl
from pyspark import SparkContext, SparkConf

from gvcf_to_vds_pipeline.cli.command_factory import CommandFactory
from gvcf_to_vds_pipeline.cli.command_methods import CommandHandler


def setup_parser():
    parser = argparse.ArgumentParser(
        description="CLI tool for combining GVCFs into a Hail VDS and performing common VDS operations."
    )

    cf = CommandFactory(parser=parser)
    cf.create_read_gvcfs_command()
    cf.create_filter_samples_command()
    cf.create_filter_intervals_command()
    cf.create_sample_qc_command()
    cf.create_split_multi_command()
    cf.create_to_dense_mt_command()

    return parser


def setup_spark_config(args):
    """
    Loads spark_conf.json and sets all SparkConf accordingly.
    The config file can have placeholders for hail_home if needed.
    """
    config_path = Path(__file__).parent / "../config/spark_config.json"
    with config_path.open() as f:
        conf_data = json.load(f)

    # Potentially do {hail_home} substitution
    hail_home = Path(hl.__file__).parent
    for k, v in conf_data.items():
        if isinstance(v, str):
            conf_data[k] = v.format(hail_home=str(hail_home))

    conf = SparkConf().setAll(conf_data.items())
    return conf


def command_handlers(args, conf):
    """
    Returns a dict mapping command -> function that runs the command logic.
    """
    return {
        "readgvcfs": lambda: init_spark_and_run(
            args, conf, CommandHandler(args).handle_read_gvcfs_command
        ),
        "filter_samples": lambda: init_spark_and_run(
            args, conf, CommandHandler(args).handle_filter_samples_command
        ),
        "filter_intervals": lambda: init_spark_and_run(
            args, conf, CommandHandler(args).handle_filter_intervals_command
        ),
        "sample_qc": lambda: init_spark_and_run(
            args, conf, CommandHandler(args).handle_sample_qc_command
        ),
        "split_multi": lambda: init_spark_and_run(
            args, conf, CommandHandler(args).handle_split_multi_command
        ),
        "to_dense_mt": lambda: init_spark_and_run(
            args, conf, CommandHandler(args).handle_to_dense_mt_command
        ),
        "combine_annotate": lambda: init_spark_and_run(
            args, conf, CommandHandler(args).handle_combine_annotate_command
        ),
    }


def init_spark_and_run(args, conf, func):
    """
    Initializes SparkContext with the config, then calls hail.init().
    Finally, runs the given function (the CLI subcommand logic).
    """
    sc = SparkContext(conf=conf)

    hl.init(
        sc=sc,
        tmp_dir=args.temp if hasattr(args, "temp") else "/tmp",
        local_tmpdir=args.temp if hasattr(args, "temp") else "/tmp",
        # You can log to a file if you wish:
        # log=hl.utils.timestamp_path(f"/tmp/hail_{args.command}", suffix=".log")
    )

    func()

    # stop or keep hail environment for inspection
    hl.stop()