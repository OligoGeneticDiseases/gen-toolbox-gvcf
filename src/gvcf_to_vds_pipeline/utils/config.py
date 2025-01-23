import json
from pathlib import Path

def load_gene_config():
    """
    Loads gene_config.json from src/config/gene_config.json
    """
    config_path = Path(__file__).parent / "../config/gene_config.json"
    with config_path.open() as f:
        return json.load(f)

def get_target_genes():
    """
    Example function that returns a list of genes from config.
    """
    data = load_gene_config()
    if "target_genes" in data:
        return data["target_genes"]
    return []
