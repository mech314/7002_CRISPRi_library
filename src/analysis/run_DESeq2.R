# Load the DESeq2 library
library(DESeq2)

# Load the count matrix and metadata
counts <- read.csv("All_conditions.csv", row.names = 1)  # This is the matrix with gene counts
metadata <- read.csv("metadata.csv", row.names = 1)  # This has the sample info

# Make sure the metadata lines up with the count matrix
if (!all(colnames(counts) == rownames(metadata))) {
  stop("Column names and metadata mistmatch!")
}

# Set up the DESeq2 dataset with the condition
dds <- DESeqDataSetFromMatrix(countData = counts,
                              colData = metadata,
                              design = ~ condition)

# Run the main DESeq2 pipeline
dds <- DESeq(dds)

# Grab all the conditions from the metadata
conditions <- levels(dds$condition)

# Pick the control group, dCasLib (can change it but from the scratch) in this case
base_condition <- "dCasLib"

# Double-check that the control is actually there
if (!(base_condition %in% conditions)) {
  stop(paste("Uh-oh! Base condition", base_condition, "is not in the conditions."))
}

# Loop through all the conditions (except the control) and save results
for (condition in conditions[conditions != base_condition]) {
  # Get the differential expression results for this condition vs the control
  res <- results(dds, contrast = c("condition", condition, base_condition))
  
  # Save the results into a CSV file
  output_file <- paste0("DESeq2_results_", condition, "_vs_", base_condition, ".csv")
  write.csv(as.data.frame(res), file = output_file)
  print(paste("Saved results for", condition, "vs", base_condition, "to", output_file))
}