import polars as pl
import argparse
from pathlib import Path


class CountCombiner:

    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Combine multiple CRISPRi conditions into one .csv")
        self.args = None
        self.file_list = None
        self.combined_df = None
        self.meta_df = None
        self.dataframes = []


    def init_parser(self):
        # Argument to accept one or more files
        self.parser.add_argument(
            'files', 
            nargs="+",  # Accepts one or more files
            help='List of file paths to process'
        )
        # Set the arguments
        self.args = self.parser.parse_args()

        # Create file list
        self.file_list = self.args.files
        print("Files provided:")
        print(self.file_list)



    def comb_counts(self):
        # Initialize parser and populate file list
        self.init_parser()

        # Process files
        for file in self.file_list:
            try:
                # Create DataFrame
                df = pl.read_csv(file)

                # Get filename to create column name for counts
                file_name = Path(file).stem

                # Rename columns and add df to the list
                df.columns = ["Locus_ID", f"Syn7002_{file_name}"]
                self.dataframes.append(df)
            except Exception as e:
                print(f"Failed to load {file}: {e}")

        if self.dataframes:
            # Create new DataFrame with the first df in the list
            self.combined_df = self.dataframes[0]

            # Add all other count columns to the combined_df
            for df in self.dataframes[1:]:
                self.combined_df = self.combined_df.join(df, on="Locus_ID", how="full", coalesce=True)

            # Remove NaNs
            self.combined_df = self.combined_df.fill_null(0)

            # Save the combined DataFrame to a CSV file
            self.combined_df.write_csv("All_conditions.csv")
            print("Combined DataFrame saved as 'All_conditions.csv'.")

            # Call writemeta to create metadata
            self.writemeta()
        else:
            print("No valid DataFrames to combine.")


    def writemeta(self):
        # Create metadata dictionary
        try:
            data = {
                "sample": self.combined_df.columns[1:],  # Exclude "Gene" column
                "condition": [x.split("_")[1][:-1] for x in self.combined_df.columns[1:]],  # extract condition from column
                "replicate": [1 if "1" in x.split("_")[-2] else 2 for x in self.combined_df.columns[1:]]  # Determine replicate
            }

        except Exception as e:
            print(f"Error creating metadata: {e}")
            return

        # Create metafile for DESeq2
        self.meta_df = pl.DataFrame(data)

        # Save metadata
        self.meta_df.write_csv("metadata.csv")
        print("Metadata file 'metadata.csv' created successfully.")

# Run the script
if __name__ == "__main__":
    combiner = CountCombiner()
    combiner.comb_counts()
