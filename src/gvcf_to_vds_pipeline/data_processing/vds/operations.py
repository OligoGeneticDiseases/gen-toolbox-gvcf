# src/data_processing/vds/operations.py
import hail as hl

def filter_samples(vds_path, sample_file, keep=True, out_path=None):
    """
    Filter samples in a VariantDataset by a list of sample IDs.
    If keep=True, only these samples are retained. Otherwise, these are removed.
    Overwrites the VDS if out_path is not specified.
    """
    if out_path is None:
        out_path = vds_path

    vds = hl.vds.read_vds(vds_path)
    with open(sample_file) as f:
        sample_list = [line.strip() for line in f if line.strip()]

    # filter_samples() is a built-in hail.vds function:
    vds_filtered = hl.vds.filter_samples(vds, sample_list, keep=keep)
    vds_filtered.write(out_path, overwrite=True)


def filter_intervals(vds_path, intervals, keep=True, out_path=None):
    """
    Keep or remove intervals from both reference and variant data.
    Overwrites the input VDS if out_path not provided.
    """
    if out_path is None:
        out_path = vds_path

    vds = hl.vds.read_vds(vds_path)
    parsed_intervals = [hl.parse_locus_interval(i) for i in intervals]
    vds_filt = hl.vds.filter_intervals(vds, parsed_intervals, keep=keep)
    vds_filt.write(out_path, overwrite=True)


def run_sample_qc(vds_path):
    """
    Run sample_qc on the variant_data of a VDS, returning a table of metrics.
    """
    vds = hl.vds.read_vds(vds_path)
    # sample_qc returns a table:
    qc_ht = hl.vds.sample_qc(vds)
    return qc_ht


def split_multi(vds_path, out_path, filter_changed_loci=False):
    """
    Split the multi-allelic variants in a VariantDataset.
    """
    vds = hl.vds.read_vds(vds_path)
    vds_split = hl.vds.split_multi(vds, filter_changed_loci=filter_changed_loci)
    vds_split.write(out_path, overwrite=True)


def to_dense_mt(vds_path, out_path):
    """
    Convert a VariantDataset to a dense MatrixTable for certain analyses.
    """
    vds = hl.vds.read_vds(vds_path)
    dense_mt = hl.vds.to_dense_mt(vds)
    dense_mt.write(out_path, overwrite=True)