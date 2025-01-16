import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gvcf-vds-combiner",
    version="0.1.0",
    author="Markus Marandi",
    author_email="markus.marandi@ut.ee",
    description="Combine GVCFs into a Hail VariantDataset (VDS).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OligoGeneticDiseases/gvcf-to-vds-pipeline.git",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "hail>=0.2.133"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License",
    ],
)