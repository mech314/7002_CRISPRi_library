# CRISPRi Library Analysis Pipeline for *Synechococcus* sp. PCC 7002

A comprehensive bioinformatics pipeline for analyzing CRISPR interference (CRISPRi) knockdown library data from the cyanobacterium *Synechococcus* sp. PCC 7002.

## Overview

CRISPR/Cas9-mediated transcriptional interference (CRISPRi) enables programmable gene knockdown, producing loss-of-function phenotypes for virtually any gene. This pipeline processes high-throughput sequencing data to identify differentially expressed genes under various environmental conditions.

### Key Features

- High-identity (95%) global sequence alignment
- Automated read count extraction
- Differential expression analysis using DESeq2
- Comprehensive log-fold change (LFC) data integration
- Support for multiple experimental conditions

## Installation

### Prerequisites

- Python 3.8 or higher
- R (for DESeq2 analysis)
- VSEARCH (for sequence alignment)

### Python Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Or install the package directly:

```bash
pip install -e .
```

### R Dependencies

Install DESeq2 in R:

```R
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install("DESeq2")
```

## Project Structure

```
7002_CRISPRi_library/
├── src/
│   ├── alignment/        # Read alignment and count extraction
│   ├── preprocessing/    # Count data combination
│   └── analysis/         # Differential expression and LFC analysis
├── scripts/              # Shell scripts for alignment workflows
├── data/                 # Input data directory
├── output/               # Processed count files
└── results/              # Analysis results
```

## Usage

### 1. Merge Paired-End Reads

Combine reads from Illumina sequencing files:

```bash
chmod +x scripts/merge_pairs.sh
./scripts/merge_pairs.sh
```

### 2. Global Alignment

Perform global alignment (adjust cores and identity threshold as needed):

```bash
chmod +x scripts/global_alignment.sh
./scripts/global_alignment.sh
```

### 3. Extract Read Counts

Extract read counts from aligned sequences:

```bash
python src/alignment/ExtCounts.py
```

### 4. Combine Count Data

Combine counts from multiple conditions:

```bash
python src/preprocessing/count_combiner.py condition1.csv condition2.csv condition3.csv
```

This generates:
- `All_conditions.csv` - Combined count matrix
- `metadata.csv` - Sample metadata for DESeq2

### 5. Differential Expression Analysis

Run DESeq2 analysis:

```bash
Rscript src/analysis/run_DESeq2.R
```

### 6. Combine LFC Results

Consolidate all log-fold change results:

```bash
python src/analysis/LFC_combiner.py
```

## Output

The pipeline generates a comprehensive dataframe with log-fold change values across all conditions:

| Gene_ID | Condition_A_LFC | Condition_B_LFC | Condition_C_LFC | locus |
|---------|-----------------|-----------------|-----------------|-------|
| Gene_1  | -1.23           | 0.45            | 2.34            | A0001 |
| Gene_2  | 0.56            | -0.78           | 1.12            | A0002 |
| Gene_3  | 1.34            | -1.45           | 0.89            | A0003 |

## Research Background

This pipeline was developed to analyze a CRISPRi knockdown library for *Synechococcus* sp. PCC 7002 under varying environmental conditions:

- **Temperature**: 37°C vs. 22°C
- **Light wavelengths**: White, red, and blue light

The analysis identified differentially expressed genes and highlighted key metabolic pathways responsive to environmental changes.

## Configuration

Customize alignment parameters in the scripts:
- Identity threshold (default: 95%)
- Number of cores for parallel processing
- Organism-specific locus names and lengths

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for improvements or new features.

## License

This project is available under the [GNU General Public License v3.0](LICENSE).

## Citation

If you use this pipeline in your research, please cite the original study and this repository.

## Contact

For questions or support, please open an issue on GitHub.