import hail as hl
from pathlib import Path

GRCH37_CONTIG_RECODING = {
    "chr1": "1", "chr2": "2", "chr3": "3", "chr4": "4", "chr5": "5", "chr6": "6", "chr7": "7", "chr8": "8", "chr9": "9", "chr10": "10",
    "chr11": "11", "chr12": "12", "chr13": "13", "chr14": "14", "chr15": "15", "chr16": "16", "chr17": "17", "chr18": "18", "chr19": "19",
    "chr20": "20", "chr21": "21", "chr22": "22", "chrX": "X", "chrY": "Y", "chrM": "MT"
}

def build_or_combine_vds(
        gvcf_paths,
        existing_vds=None,
        output_path=None,
        temp_path=None,
        save_path=None,
        use_genome=False,
        use_exome=False,
        intervals=None,
        import_interval_size=None,
        reference_genome="GRCh37",
        contig_recoding = None
):
    """
    Build a new VDS from GVCFs or combine GVCFs with an existing VDS.

    :param gvcf_paths: list of GVCF file paths
    :param existing_vds: path to existing VDS (str) if combining
    :param output_path: path for the resulting VDS
    :param temp_path: Hail combiner temp path
    :param save_path: path to store combiner plan JSON
    :param use_genome: use hail's default intervals for whole-genome partitioning
    :param use_exome: use hail's default intervals for exome partitioning
    """
    if not gvcf_paths and not existing_vds:
        raise ValueError("No GVCFs and no existing VDS. Nothing to combine.")

    # If both flags are true, prefer genome
    if use_genome and use_exome:
        hl.utils.warning("Both genome and exome intervals requested; using genome intervals.")
        use_exome = False

    # If combining with existing VDS, we pass it in as vds_paths
    vds_paths = []
    if existing_vds:
        vds_paths.append(existing_vds)

    parsed_intervals = None
    if intervals:
        parsed_intervals = [hl.parse_locus_interval(i) for i in intervals]

    combiner = hl.vds.new_combiner(
        output_path=output_path,
        temp_path=temp_path,
        save_path=save_path,
        gvcf_paths=gvcf_paths,
        vds_paths=vds_paths,
        intervals=parsed_intervals,  # <--- new
        import_interval_size=import_interval_size,
        use_genome_default_intervals=use_genome,
        use_exome_default_intervals=use_exome,
        reference_genome = reference_genome,
        contig_recoding = contig_recoding
    )
    combiner.run()