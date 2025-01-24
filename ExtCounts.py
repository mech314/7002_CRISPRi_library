import polars as pl  # Polars for faster processing
from pathlib import Path  # Path is more fun to use
from tqdm import tqdm  # We need a progress bar


class ExtCounts:
    def __init__(self, data_dir="./data/", output_dir="./output/"):
        self.counts = None
        self.base_name = None
        self.path = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.files = list(self.path.glob("*.tsv"))

        # Create the output directory if it doesn't exist
        if not Path(self.output_dir).is_dir():
            Path(self.output_dir).mkdir(parents=True, exist_ok=True)

    def check_files(self):
        """Check if files are available in the directory."""
        if not self.files:
            print("No files found in the directory.")
            return False
        return True

    def save_counts(self):
        """Save the counts DataFrame to a CSV file."""
        output_file = self.output_dir / f"{self.base_name}_counts.csv"
        self.counts.write_csv(output_file, include_header=False)

    def extract_counts(self):
        """Extract counts from .tsv files and save results."""
        # Check if there are any files; terminate if none are found
        if not self.check_files():
            return

        for file in tqdm(self.files, desc="Processing files", unit="file", dynamic_ncols=True, ascii=False):
            try:
                # Get basename for output file
                self.base_name = file.stem.split("_")[0]

                # Load .tsv into dataframe
                df = pl.read_csv(file, separator="\t", has_header=True)

                # Columns per VSEARCH output
                df.columns = [
                    "Query ID", "Target ID", "% Identity", "Alignment Length", "Mismatches",
                    "Gap Openings", "Query Start", "Query End", "Target Start", "Target End", "E-value",
                    "Bit Score",
                ]

                # Filter by the % Identity (may need to increase the value)
                high_identity = df.filter(df["% Identity"] > 95)

                # Calculate counts
                self.counts = high_identity["Target ID"].value_counts().sort("count", descending=True)

                # Save counts to a CSV file
                self.save_counts()

            except Exception as e:
                print(f"Error processing file {file}: {e}")


if __name__ == "__main__":
    print("Extracting counts", flush=True)  # Ensure immediate print
    counts = ExtCounts(data_dir="./data/", output_dir="./output/")
    counts.extract_counts()
    print("Done", flush=True)  # Ensure immediate print
