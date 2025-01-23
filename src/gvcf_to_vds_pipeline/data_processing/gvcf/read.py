from pathlib import Path


def gather_gvcfs(paths):
    """
    Gather .g.vcf, .g.vcf.gz, .gvcf, .gvcf.gz, and .gvcf.bgz files from the specified paths (files/dirs).
    Returns a list of string paths for hail.vds.new_combiner().

    Args:
        paths (list of str or Path): List of file or directory paths to search for GVCF files.

    Returns:
        list of str: Resolved paths to valid GVCF files.
    """
    valid_extensions = [".g.vcf", ".g.vcf.gz", ".gvcf", ".gvcf.gz", ".gvcf.bgz"]
    gvcfs = []

    for path in paths:
        path = Path(path)
        if path.is_file():
            # Check file extensions
            if any(path.name.endswith(ext) for ext in valid_extensions):
                gvcfs.append(str(path.resolve()))
        elif path.is_dir():
            # Recursively find valid GVCFs in directories
            for ext in valid_extensions:
                for f in path.rglob(f"*{ext}"):
                    gvcfs.append(str(f.resolve()))

    return gvcfs