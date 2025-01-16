from setuptools import setup, find_packages

setup(
    name="gvcf_to_vds_pipeline",
    version="0.1.0",
    description="A Python package for converting GVCFs to Hail VariantDataset (VDS)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Markus Marandi",
    author_email="markus.marandi@ut.ee",
    url="https://github.com/OligoGeneticDiseases/gvcf-to-vds-pipeline.git",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "hail>=0.2.133"
        "pyspark",
    ],
    entry_points={
        "console_scripts": [
            "gvcf-to-vds=gvcf_to_vds_pipeline.__main__:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Creative Commons Attribution Non Commercial Share Alike License",
    ],
    python_requires=">=3.7",
)