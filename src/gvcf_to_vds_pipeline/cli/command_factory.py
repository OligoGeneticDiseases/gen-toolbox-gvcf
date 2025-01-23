import argparse

class CommandFactory:
    def __init__(self, parser):
        self.parser = parser
        self.subparsers = parser.add_subparsers(title="commands", dest="command")

    def create_read_gvcfs_command(self):
        """
        Command for building or combining a VDS from GVCF(s).
        """
        read_cmd = self.subparsers.add_parser(
            "readgvcfs",
            help="Combine GVCF file(s) (and optional existing VDS) into a new or updated VDS."
        )
        read_cmd.add_argument(
            "-f", "--file", nargs="+", required=True,
            help="Path(s) to GVCF file(s) or directories containing .g.vcf/.g.vcf.gz"
        )
        read_cmd.add_argument(
            "--vds_in", type=str, default=None,
            help="(Optional) Path to an existing VDS to combine with new GVCFs."
        )
        read_cmd.add_argument(
            "-d", "--dest", type=str, required=True,
            help="Destination path for the resulting VDS."
        )
        read_cmd.add_argument(
            "--temp", type=str, required=True,
            help="Temporary directory/bucket for intermediate data."
        )
        read_cmd.add_argument(
            "--save_plan", type=str, default=None,
            help="Path to store the combiner plan JSON for restart if needed."
        )
        read_cmd.add_argument(
            "--use_genome_intervals", action="store_true", default=False,
            help="Use Hail's default intervals for whole-genome partitioning."
        )
        read_cmd.add_argument(
            "--use_exome_intervals", action="store_true", default=False,
            help="Use Hail's default intervals for exome partitioning."
        )
        read_cmd.add_argument(
            "--intervals", nargs="+", default=None,
            help="List of intervals (e.g. chr1:1-100000) for GVCF partitioning."
        )
        read_cmd.add_argument(
            "--import_interval_size", type=int, default=None,
            help="Interval size in base pairs for GVCF partitioning."
        )

    def create_filter_samples_command(self):
        filter_cmd = self.subparsers.add_parser(
            "filter_samples",
            help="Filter samples in a VariantDataset."
        )
        filter_cmd.add_argument(
            "-v", "--vds", type=str, required=True,
            help="Path to the input VDS"
        )
        filter_cmd.add_argument(
            "-s", "--samples", type=str, required=True,
            help="File with one sample ID per line to keep or remove."
        )
        filter_cmd.add_argument(
            "-k", "--keep", action="store_true", default=False,
            help="Keep these samples (default is remove)."
        )
        filter_cmd.add_argument(
            "-o", "--out", type=str, required=False,
            help="Path to the output VDS. If omitted, overwrites original."
        )

    def create_filter_intervals_command(self):
        filter_cmd = self.subparsers.add_parser(
            "filter_intervals",
            help="Filter intervals in a VDS. Removes all data outside intervals."
        )
        filter_cmd.add_argument(
            "-v", "--vds", type=str, required=True,
            help="Path to input VDS."
        )
        filter_cmd.add_argument(
            "-i", "--intervals", nargs="+", required=True,
            help="List of intervals (e.g. chr1:1-100000) to keep or remove."
        )
        filter_cmd.add_argument(
            "--keep", action="store_true", default=True,
            help="Keep only these intervals (default). If false, remove intervals."
        )
        filter_cmd.add_argument(
            "-o", "--out", type=str, required=False,
            help="Path to output VDS. If omitted, overwrites original."
        )

    def create_sample_qc_command(self):
        qc_cmd = self.subparsers.add_parser(
            "sample_qc",
            help="Compute sample QC metrics on a VDS."
        )
        qc_cmd.add_argument(
            "-v", "--vds", type=str, required=True,
            help="Path to input VDS."
        )
        qc_cmd.add_argument(
            "-o", "--out", type=str, required=False,
            help="Path to output with QC results (e.g. a text file)."
        )

    def create_split_multi_command(self):
        sm_cmd = self.subparsers.add_parser(
            "split_multi",
            help="Split multi-allelic variants in a VDS's variant_data."
        )
        sm_cmd.add_argument(
            "-v", "--vds", type=str, required=True,
            help="Path to input VDS."
        )
        sm_cmd.add_argument(
            "-o", "--out", type=str, required=True,
            help="Path to the output (split) VDS."
        )
        sm_cmd.add_argument(
            "--filter_changed_loci", action="store_true", default=False,
            help="If true, filter out variants whose locus changes after splitting."
        )

    def create_to_dense_mt_command(self):
        td_cmd = self.subparsers.add_parser(
            "to_dense_mt",
            help="Convert a VariantDataset to a dense MatrixTable."
        )
        td_cmd.add_argument(
            "-v", "--vds", type=str, required=True,
            help="Path to input VDS."
        )
        td_cmd.add_argument(
            "-o", "--out", type=str, required=True,
            help="Path to the resulting dense MT."
        )

    def setup_parser():
        """
        Sets up the command-line argument parser.
        """
        parser = argparse.ArgumentParser(description="GVCF to VDS Pipeline")
        factory = CommandFactory(parser)

        factory.create_read_gvcfs_command()
        factory.create_filter_samples_command()
        factory.create_filter_intervals_command()
        factory.create_sample_qc_command()
        factory.create_split_multi_command()
        factory.create_to_dense_mt_command()

        return parser