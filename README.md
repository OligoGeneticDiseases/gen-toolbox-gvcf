# GVCF to VDS Pipeline

A Python command-line tool to combine and convert GVCF files into a [Hail VariantDataset (VDS)](https://hail.is/docs/0.2/hail.vds.html) for large-scale genomic processing. This pipeline is designed for high-performance environments where annotation is not required, and focuses on the efficient batching of GVCF data into a single or combined VDS.

Documentation can be found here: https://oligogeneticdiseases.github.io/gvcf-to-vds-docs/

---

## **Concept**

The primary goal of this repository is to streamline the process of transforming GVCF files into Hail's VariantDataset (VDS) format. Key functionalities include:
- **Batch processing** of multiple GVCF files into a single VDS.
- Use of Hail's `read_vds()` and `split_multi()` methods for processing genomic data.
- Scalability for processing large genomic datasets in high-performance environments.

This repository is specifically tailored for scenarios where annotation is not required, focusing instead on the efficient generation and combination of VDS files.

---

## **Key Features**

1. **Batch GVCF to VDS Conversion**  
   - Converts multiple GVCFs into a single VDS.  
   - Optionally incorporates an existing VDS for incremental updates.

2. **Multi-Allelic Splitting**  
   - Uses [`hail.vds.split_multi`](https://hail.is/docs/0.2/hail.vds.html#hail.vds.split_multi) to handle multi-allelic variants.

3. **Reference & Variant Data**  
   - Leverages Hail’s sparse representation (reference_data + variant_data) to handle large-scale genomic data efficiently.

4. **Flexible Interval Handling**  
   - Supports genome-wide intervals, exome intervals, or user-defined intervals.

5. **Built-in Utilities**  
   - Sample filtering, interval filtering, sample QC, and more.

---

## **Installation**

1. **Clone the Repository**  
```bash
git clone https://github.com/OligoGeneticDiseases/gvcf-to-vds-pipeline.git
cd gvcf-to-vds-pipeline
```
   
2. **Install via pip**
```bash
pip install .
```

This installs the gvcf-to-vds command-line tool.

## **Quickstart Usage**


```bash
gvcf-to-vds readgvcfs \
  -f /path/to/gvcf_folder \
  -d /path/to/output.vds \
  --temp /path/to/tmp/ \
  --use_genome_intervals
```

* -f or --file: One or more GVCFs or directories containing GVCFs.
* -d or --dest: The destination path for the VDS.
* --temp: A temporary directory for intermediate Spark/Hail files.
* --use_genome_intervals or --use_exome_intervals: Use Hail’s built-in intervals.
* --save_plan: Store the combiner plan in JSON for restarts if needed.

## **Commands Overview**

1. ```readgvcfs```
Combine new GVCFs (and/or an existing VDS) into a unified VDS.
2.	```filter_samples```
Include or exclude specific samples from a VDS.
3.	```filter_intervals```
Keep or remove certain genomic intervals.
4.	```sample_qc```
Perform sample-level QC metrics.
5.	```split_multi```
Split multi-allelic variants.
6.	```to_dense_mt```
Convert the VDS to a dense Hail MatrixTable.

Run ```gvcf-to-vds --help``` or ```gvcf-to-vds <command> --help``` for all available options.

## *Research Context*

### Project
* Title: Oligogenic Inheritance in Genetic Diseases
* Objective of this repository: Combine large GVCF sets and produce unified variant datasets (VDS).
* Funding: Estonian Research Council, Grant PSG774.
* Institutions: Tartu University Hospital Centre of Medical Genetics; University of Tartu.

### Ethics and Privacy
* Protocol: Approved under #362/T-6 by the University of Tartu Ethics Committee.
* Data is processed internally, following strict privacy regulations.

### Contact
* Author: Markus Marandi markus.marandi@ut.ee
* Principal Investigator: Dr. Sander Pajusalu (University of Tartu)
