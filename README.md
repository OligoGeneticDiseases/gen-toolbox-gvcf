# GVCF to VDS Pipeline

This repository provides tools to process GVCF files and produce VariantDataset (VDS) files using Hail. It is a modified and focused version of the [Oligogenicity Toolbox](https://github.com/OligoGeneticDiseases/gen-toolbox.git), designed to handle large-scale genomic data processing without annotation steps. The repository enables efficient collation and batching of multiple GVCF files into a single, unified VDS file.

Documentation can be found here: https://oligogeneticdiseases.github.io/gvcf-to-vds-docs/
---

## **Concept**

The primary goal of this repository is to streamline the process of transforming GVCF files into Hail's VariantDataset (VDS) format. Key functionalities include:
- **Batch processing** of multiple GVCF files into a single VDS.
- Use of Hail's `read_vds()` and `split_multi()` methods for processing genomic data.
- Scalability for processing large genomic datasets in high-performance environments.

This repository is specifically tailored for scenarios where annotation is not required, focusing instead on the efficient generation and combination of VDS files.

---

## Developer Notes
- All VCF ingestion code has been removed; we only handle GVCFs in this repository. 
- For advanced usage or restarts, pass `--save_plan /some/path.json`, then if you want to restart the combiner after a failure, specify the same JSON plan.



## **Key Features**

1. **GVCF File Reading:**
   - Utilizes Hail's `read_vds()` to load existing VDS files for processing.
   - Supports reading and parsing GVCF files.

2. **Multi-Allelic Variant Splitting:**
   - Uses Hail's `split_multi()` to handle multi-allelic variants in the dataset.

3. **Batch VDS Creation:**
   - Combines multiple GVCF files into a single VDS file.

4. **Scalability:**
   - Designed to work on high-performance computing systems with distributed processing.

---

## **Setup**

### **1. Clone the Repository**
```bash
git clone <repository-url>
cd <repository-folder>
```

2. Set Up a Python Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Run the Application
```bash
python main.py --help
```

## Usage

Available Commands

The main.py file serves as the command-line interface (CLI) for the application. Below are the supported commands:
	1.	Process GVCF to VDS
	•	Reads GVCF files and converts them to VDS format.
	•	Example:

```bash
python main.py readgvcfs 
-f /path/to/gvcfs_or_dir 
-d /path/to/output.vds 
–temp /tmp/combine-temp 
–use_genome_intervals
- `-f` / `--file`: Input file(s) or directory(ies) containing `.g.vcf`/`.g.vcf.gz`.
- `-d` / `--dest`: Destination path for the final VDS.
- `--temp`: Temporary directory for intermediate data.
- `--use_genome_intervals`: If set, uses hail’s default genome partitioning.  
- `--use_exome_intervals`: If set, uses hail’s exome partitioning.
```
### Hail Methods Used

1. hail.vds.read_vds()

Reads a VariantDataset (VDS) from a specified path.

vds = hl.vds.read_vds(path_to_vds)

2. hail.vds.split_multi()

Splits multi-allelic variants in a VDS.

split_vds = hl.vds.split_multi(vds)

## Research Context

### Project

• Title: Oligogenic Inheritance in Genetic Diseases

• Objective: Collate large numbers of VCF files, annotate variants, and create variant frequency tables in a pipeline fashion.

• Funding: Estonian Research Council, Grant PSG774.

• Directed By: Tartu University Hospital Centre of Medical Genetics and Tartu University Institute of Clinical Medicine.


### Ethics and Privacy

• Ethics Protocol: Approved under protocol 362/T-6 by the University of Tartu Research Ethics Committee.

• Data Privacy: All analyses are performed in accordance with the data protection plan. Data is not publicly available.


### Principal Investigator

• Dr. Sander Pajusalu
University of Tartu, Faculty of Medicine, Institute of Clinical Medicine.
