import pandas as pd

# Read csv file
df = pd.read_csv("code\data\crime_data\step1e_crime_2021-2023_counts_by_grid.csv")

# Combine Grid_X and Grid_Y as new column
df["Grid"] = df["Grid_X"].astype(str) + "_" + df["Grid_Y"].astype(str)

# Order by Grid_X and Grid_Y
df = df.sort_values(["Grid_X", "Grid_Y"])

# Pivot data, YearMonth is the row, Grid is the column, Crime_Count is the value
pivot_df = df.pivot_table(
    index="YearMonth",
    columns="Grid",
    values="Crime_Count",
    aggfunc="sum", 
    fill_value=0 
).reset_index()

# Save as csv file
pivot_df.to_csv("code\data\crime_data\step3c_crime_2021-2023_counts_by_grid_transferred.csv", index=False)