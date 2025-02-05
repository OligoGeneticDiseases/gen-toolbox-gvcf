import json
import hail as hl
from pathlib import Path

def annotate_vds(dense_mt_path, output_vds, vep_config_path=None):
    """
    Annotate a dense MatrixTable with VEP and write the final annotated VDS.

    Args:
        dense_mt_path (str): Path to the dense MatrixTable file.
        output_vds (str): Path to write the final annotated VDS.
        vep_config_path (str, optional): Path to the VEP configuration JSON file.
            Defaults to the one in ../config/vep_settings.json.
    """
    if vep_config_path is None:
        vep_config_path = str(Path(__file__).parent / "../config/vep_settings.json")

    with open(vep_config_path) as f:
        vep_config = json.load(f)

    # Read the dense MatrixTable.
    mt = hl.read_matrix_table(dense_mt_path)

    # Prepare the VEP command string.
    # (Replace the placeholder __OUTPUT_FORMAT_FLAG__ with an empty string.)
    command_list = [arg if arg != "__OUTPUT_FORMAT_FLAG__" else "" for arg in vep_config["command"]]
    command_list = [arg for arg in command_list if arg]
    vep_command = " ".join(command_list)

    # Run VEP on the dense MT.
    annotated_mt = hl.vep(mt,
                          vep_command=vep_command,
                          env=vep_config.get("env", {}),
                          vep_json_schema=vep_config["vep_json_schema"])

    # Convert the annotated dense MT to a VDS.
    annotated_vds = dense_to_vds(annotated_mt)
    annotated_vds.write(output_vds, overwrite=True)

def dense_to_vds(mt):
    """
    Placeholder function to convert a dense MatrixTable to a VDS.
    In a real implementation, you would perform the conversion here.
    For this example, we simply return the MatrixTable.
    """
    return mt