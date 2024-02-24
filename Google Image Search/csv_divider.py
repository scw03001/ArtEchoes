import pandas as pd
import numpy as np
import math

# Define the path of the Excel file and the number of parts to divide into.
file_path = 'csv/all_artist.csv'  # Enter the path to your Excel file here.
n_parts = 40  # Enter the number of parts to divide into here.

# Read the cvs file.
df = pd.read_csv(file_path)

# Prepare to divide the DataFrame into n parts: calculate the size of each part
part_size = math.ceil(len(df) / n_parts)

# Divide into n parts and save each part to a new Excel file
for i in range(n_parts):
    start_index = i * part_size
    end_index = min((i + 1) * part_size, len(df))
    df_part = df.iloc[start_index:end_index]
    df_part.to_csv(f'csv/part_{i + 1}.csv', index=False)  # Save without the index
