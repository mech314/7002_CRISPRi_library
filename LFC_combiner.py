import re
import polars as pl
from pathlib import Path

class LFC_combiner:
	def __init__(self, folder_path="./"):
		self.pattern = r"\d{2}[A-Z]" 	# Regex pattern to experimental condition
		self.folder_path = Path(folder_path) 	# Path to the folder
		self.dataframes = []	# Store dataframes to combine


	def extract_condition(self, file_name):
		"""Extract experimental condition from file name using regex."""
		match = re.search(self.pattern, file_name)
		return match.group() if match else None


	def df_process(self, file):
		"""Process a single file and return a Polars DataFrame."""
		try:
			# Extract condition from file name
			condition = self.extract_condition(file.stem)
			if not condition:
				print(f"Condition not found in file name: {file.name}")
				return None

			# Read CSV file into Polars DataFrame
			df = pl.read_csv(file, has_header=True)

			# Rename columns dynamically
			df.columns = ["ID", "baseMean", condition, "lfcSE", "stat", "pvalue", "padj"]

			# Keep only 'ID' and the condition column
			return df.select(["ID", condition])

		except Exception as e:
			print(f"Error processing file {file.name}: {e}")
			return None


	def process_files(self):
		"""Process all files in the folder matching the pattern."""
		for file in self.folder_path.glob("DESeq2_results*"):
			if file.is_file():
				df = self.df_process(file)
				if df is not None:
					self.dataframes.append(df)


	def combine_dataframes(self):
		"""Combine all processed dataframes into a one dataframe."""
		if not self.dataframes:
			print("No DataFrames to combine")
			return None

		combined_LFC_data = self.dataframes[0]  # Start with the first DataFrame
		for df in self.dataframes[1:]:
			combined_LFC_data = combined_LFC_data.join(df, on="ID", how="full", coalesce=True)

		# Add 'locus' column
		combined_LFC_data = combined_LFC_data.with_columns(
			combined_LFC_data["ID"].str.slice(0, 5).alias("locus")
		)

		return combined_LFC_data

	def save_combined_data(self, combined_data, output_file="combined_LFC_data.csv"):
		"""Save combined DataFrame to a CSV file."""
		if combined_data is not None and not combined_data.is_empty():
			combined_data.write_csv(output_file)
			print(f"Combined LFC data saved to '{output_file}'")

	def run(self):
		"""Run pipeline"""
		self.process_files()
		combined_data = self.combine_dataframes()
		self.save_combined_data(combined_data)


# run
if __name__ == "__main__":
	combiner = LFC_combiner(folder_path="./")
	combiner.run()