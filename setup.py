from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="crispri-7002-library",
    version="1.0.0",
    author="Your Name",
    description="CRISPRi library analysis pipeline for Synechococcus sp. PCC 7002",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mech314/7002_CRISPRi_library",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "polars>=0.19.0",
        "tqdm>=4.66.0",
    ],
)