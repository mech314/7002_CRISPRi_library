#!/bin/bash

#Bash command script to merge all reads into corresponding merged reads in the folder.
#Output is forwarded into _statistics.txt file


# Directory containing the files
input_dir="./"
output_dir="./merged_sequences"

if [ ! -d "$output_dir" ]; then
    mkdir -p "$output_dir"
    echo "Directory $output_dir created."
else
    echo "Directory $output_dir already exists."
fi

# Get the list of all fastq files
files=("${input_dir}"*_R1*.fastq)
total_files=${#files[@]}
processed=0

# Show the progress
show_progress() {
    local process=$1
    local total=$2
    local bar_length=50
    local filled=$((process * bar_length / total))
    local empty=$((bar_length - filled))
    printf "\rProgress: [%s%s] %d/%d files" \
        "$(printf '#%.0s' $(seq 1 $filled))" \
        "$(printf ' %.0s' $(seq 1 $empty))" \
        "$process" "$total"
}

# Show initial progress (before any files are processed)
show_progress "$processed" "$total_files"

# Loop through all *_R1* files
for f_read in "${files[@]}"; do
    # get the base name
    base=$(basename "$f_read" | sed 's/_R1.*//')

    # Construct the reverse file name
    r_read="${input_dir}${base}_R2_001.fastq"

    # Check if the reverse file exists
    if [[ -f "$r_read" ]]; then

        # output file name
        merged="${output_dir}/${base}_merged.fastq"

        # redirect output into file
        stat_output="${output_dir}/${base}_stat_output.txt"

        # Run vsearch to merge the pairs
        vsearch --fastq_mergepairs "$f_read" \
                --reverse "$r_read" \
                --fastqout "$merged" \
                > "$stat_output" 2>&1

        # Upgrade progress
        ((processed++))
        show_progress "$processed" "$total_files"
    else
        echo -e  "\nReverse file not found for $f_read. Skipping..."
    fi
done

# Final message
echo -e "\nAll files processed!"
