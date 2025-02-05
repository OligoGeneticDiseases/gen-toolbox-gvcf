import hail as hl
from pathlib import Path

from gvcf_to_vds_pipeline.data_processing.gvcf.read import gather_gvcfs
from gvcf_to_vds_pipeline.data_processing.gvcf.process import build_or_combine_vds, GRCH37_CONTIG_RECODING
from gvcf_to_vds_pipeline.data_processing.vds import annotate
from gvcf_to_vds_pipeline.data_processing.vds.operations import (
    filter_samples,
    filter_intervals,
    run_sample_qc,
    split_multi,
    to_dense_mt
)

class CommandHandler:
    def __init__(self, args):
        self.args = args

    def handle_read_gvcfs_command(self):
        contig_map = {
            "chr1": "1", "chr2": "2", "chr3": "3", "chr4": "4", "chr5": "5",
            "chr6": "6", "chr7": "7", "chr8": "8", "chr9": "9", "chr10": "10",
            "chr11": "11", "chr12": "12", "chr13": "13", "chr14": "14", "chr15": "15",
            "chr16": "16", "chr17": "17", "chr18": "18", "chr19": "19", "chr20": "20",
            "chr21": "21", "chr22": "22", "chrX": "X", "chrY": "Y", "chrM": "MT"
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
            intervals=self.args.intervals,
            import_interval_size=self.args.import_interval_size,
            reference_genome="GRCh37",
            contig_recoding=contig_map
        )

        hl.utils.info(f"[DONE] Created or updated VDS at {self.args.dest}")

    def handle_filter_samples_command(self):
        vds = hl.vds.read_vds(self.args.vds)
        with open(self.args.samples) as f:
            sample_list = [line.strip() for line in f if line.strip()]
        new_vds = hl.vds.filter_samples(vds, sample_list, keep=self.args.keep)
        out = self.args.out if self.args.out else self.args.vds
        new_vds.write(out, overwrite=True)

        hl.utils.info(f"[DONE] Filtered samples -> {out}")

    def handle_filter_intervals_command(self):
        out = self.args.out if self.args.out else self.args.vds
        filter_intervals(
            vds_path=self.args.vds,
            intervals=self.args.intervals,
            keep=self.args.keep,
            out_path=out
        )
        hl.utils.info(f"[DONE] Filtered intervals -> {out}")

    def handle_sample_qc_command(self):
        result_table = run_sample_qc(self.args.vds)
        if self.args.out:
            result_table.export(self.args.out)
            hl.utils.info(f"[DONE] Sample QC results exported to {self.args.out}")
        else:
            hl.utils.info("[INFO] Sample QC results (first few rows):")
            result_table.show(5)

    def handle_split_multi_command(self):
        split_multi(
            vds_path=self.args.vds,
            out_path=self.args.out,
            filter_changed_loci=self.args.filter_changed_loci
        )
        hl.utils.info(f"[DONE] Split multi -> {self.args.out}")

    def handle_to_dense_mt_command(self):
        to_dense_mt(
            vds_path=self.args.vds,
            out_path=self.args.out
        )
        hl.utils.info(f"[DONE] Wrote dense MT to {self.args.out}")

    def handle_combine_annotate_command(self):
        # Step 1. Combine the input GVCFs (and optional VDS) into a new VDS.
        gvcf_paths = gather_gvcfs([Path(p) for p in self.args.file])
        combined_path = self.args.dest + self.args.combined_suffix
        build_or_combine_vds(
            gvcf_paths=gvcf_paths,
            existing_vds=self.args.vds_in,
            output_path=combined_path,
            temp_path=self.args.temp,
            save_path=self.args.save_plan,
            use_genome=self.args.use_genome_intervals,
            use_exome=self.args.use_exome_intervals,
            intervals=self.args.intervals,
            import_interval_size=self.args.import_interval_size,
            reference_genome="GRCh37",
            contig_recoding=GRCH37_CONTIG_RECODING
        )
        hl.utils.info(f"[DONE] Combined VDS created at {combined_path}")

        # Step 2. Convert the combined VDS to a dense MatrixTable.
        dense_mt_path = self.args.dest + self.args.dense_suffix
        to_dense_mt(
            vds_path=combined_path,
            out_path=dense_mt_path
        )
        hl.utils.info(f"[DONE] Dense MatrixTable created at {dense_mt_path}")

        # Step 3. Annotate the dense MatrixTable with VEP.
        annotated_vds_path = self.args.dest + self.args.annotated_suffix
        annotate.annotate_vds(dense_mt_path, annotated_vds_path)
        hl.utils.info(f"[DONE] Final annotated VDS created at {annotated_vds_path}")