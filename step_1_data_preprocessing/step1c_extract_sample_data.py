### This code is to choose crime data in December 2020, which will be used to calculate Moran's I

import pandas as pd

# Read csv file
file_path = "code\data\crime_data\step1b_crime_2011-2020_data.csv"
df = pd.read_csv(file_path)

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Filter data of 2020-12-01
filtered_df = df[(df['Date'].dt.year == 2020) & (df['Date'].dt.month == 12)]

# Save csv file
output_path = "code\data\crime_data\step1c_crime_2020-12_data.csv"
filtered_df.to_csv(output_path, index=False)

print(f"Saved as {output_path}")
