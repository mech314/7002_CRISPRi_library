# Illumina Sequence Analysis Pipeline

This pipeline processes Illumina sequence data to:
- Trim sequences at 95% accuracy.
- Perform global alignment.
- Extract read counts.
- Run differential expression analysis using **DESeq2** in R.
- Combine all log-fold change (LFC) data into one comprehensive dataframe for downstream analysis.

---

## **Requirements**

The pipeline is written in Python and R, and requires the following dependencies:

### **Python Dependencies**
- `re`
- `tqdm`
- `polars`
- `pathlib`
- `argparse`

Install these Python packages via pip:
```bash
pip install tqdm polars argoparse pathlib


### **R Packages**
- `DESeq2`