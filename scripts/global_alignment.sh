#!/bin/bash

# Reference database file
ref_database='./database.fasta'

# Number of threads to use (set to 128 for full utilization)
num_threads=128

# Get the list of all .fastq files
files=(./*.fastq)
total_files=${#files[@]}
processed=0

# Function to show progress
show_progress() {
    local progress=$1
    local total=$2
    local bar_length=50
    local filled=$((progress * bar_length / total))
    local empty=$((bar_length - filled))
    printf "\rProgress: [%s%s] %d/%d files" \
        "$(printf '#%.0s' $(seq 1 $filled))" \
        "$(printf ' %.0s' $(seq 1 $empty))" \
        "$progress" "$total"
}

# Show initial progress (before any files are processed)
show_progress "$processed" "$total_files"

# Loop through all .fastq files in the current directory
for file in "${files[@]}"; do
    base=$(basename "$file" .fastq) # Extract the base name

    # Redirect output into a file
    stat_output="./${base}_stat_output.txt"

    # Run vsearch for each file
    vsearch \
        --usearch_global "$file" \
        --db "$ref_database" \
        --blast6out "${base}_alignment.tsv" \
        --id 0.95 \
        --gapopen 5 \
        --gapext 2 \
        --strand both \
        --alnout "${base}_alignment.aln" \
        --threads "$num_threads" \
        >"$stat_output" 2>&1

    # Update progress
    ((processed++))
    show_progress "$processed" "$total_files"
done

# Final message
echo -e "\nAll files processed!"
