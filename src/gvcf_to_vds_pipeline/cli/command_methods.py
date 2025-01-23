import hail as hl
from pathlib import Path

from gvcf_to_vds_pipeline.data_processing.gvcf.read import gather_gvcfs
from gvcf_to_vds_pipeline.data_processing.gvcf.process import build_or_combine_vds
from gvcf_to_vds_pipeline.data_processing.vds.operations import (
    filter_samples,
    filter_intervals,
    run_sample_qc,
    split_multi,
    to_dense_mt
)

class CommandHandler:
    """
    This class has methods that handle each CLI command,
    orchestrating I/O with hail, reading/writing the VDS, etc.
    """

    def __init__(self, args):
        self.args = args

    def handle_read_gvcfs_command(self):
        """
        Combine GVCFs (and optional existing VDS) into a new/updated VDS.
        """
        contig_map = {
            "chr1": "1", "chr2": "2", "chr3": "3", "chr4": "4", "chr5": "5", "chr6": "6", "chr7": "7", "chr8": "8",
            "chr9": "9", "chr10": "10",
            "chr11": "11", "chr12": "12", "chr13": "13", "chr14": "14", "chr15": "15", "chr16": "16", "chr17": "17",
            "chr18": "18", "chr19": "19",
            "chr20": "20", "chr21": "21", "chr22": "22", "chrX": "X", "chrY": "Y", "chrM": "MT"
        }

        gvcf_paths = gather_gvcfs([Path(p) for p in self.args.file])

        build_or_combine_vds(
            gvcf_paths=gvcf_paths,
            existing_vds=self.args.vds_in,
            output_path=self.args.dest,
            temp_path=self.args.temp,
            save_path=self.args.save_plan,
            use_genome=self.args.use_genome_intervals,
            use_exome=self.args.use_exome_intervals,
            intervals = self.args.intervals,
            import_interval_size = self.args.import_interval_size,
            reference_genome = "GRCh37",
            contig_recoding = contig_map
        )

        hl.utils.info(f"[DONE] Created or updated VDS at {self.args.dest}")

    def handle_filter_samples_command(self):
        """
        Filter samples from a VDS.
        """
        vds = hl.vds.read_vds(self.args.vds)
        with open(self.args.samples) as f:
            sample_list = [line.strip() for line in f]
        new_vds = hl.vds.filter_samples(vds, sample_list, keep=self.args.keep)
        out = self.args.out if self.args.out else self.args.vds
        new_vds.write(out, overwrite=True)

        hl.utils.info(f"[DONE] Filtered samples -> {out}")

    def handle_filter_intervals_command(self):
        """
        Keep or remove intervals from a VDS.
        """
        out = self.args.out if self.args.out else self.args.vds
        filter_intervals(
            vds_path=self.args.vds,
            intervals=self.args.intervals,
            keep=self.args.keep,
            out_path=out
        )
        hl.utils.info(f"[DONE] Filtered intervals -> {out}")

    def handle_sample_qc_command(self):
        """
        Compute sample QC metrics on a VDS.
        """
        result_table = run_sample_qc(self.args.vds)
        if self.args.out:
            result_table.export(self.args.out)
            hl.utils.info(f"[DONE] Sample QC results exported to {self.args.out}")
        else:
            hl.utils.info("[INFO] Sample QC results (first few rows):")
            result_table.show(5)

    def handle_split_multi_command(self):
        """
        Split multi-allelic variants in the variant data.
        """
        split_multi(
            vds_path=self.args.vds,
            out_path=self.args.out,
            filter_changed_loci=self.args.filter_changed_loci
        )
        hl.utils.info(f"[DONE] Split multi -> {self.args.out}")

    def handle_to_dense_mt_command(self):
        """
        Convert a VDS to a dense MatrixTable.
        """
        to_dense_mt(
            vds_path=self.args.vds,
            out_path=self.args.out
        )
        hl.utils.info(f"[DONE] Wrote dense MT to {self.args.out}")
