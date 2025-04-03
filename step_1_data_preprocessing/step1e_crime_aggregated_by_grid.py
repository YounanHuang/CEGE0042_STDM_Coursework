import pandas as pd
import numpy as np
from datetime import datetime
from pyproj import Transformer

# Read csv file
df = pd.read_csv('code\data\crime_data\step1b_crime_2021-2023_data.csv', parse_dates=['Date'])

# Projection transfer
transformer = Transformer.from_crs("epsg:4326", "epsg:32616", always_xy=True)
def latlon_to_utm(lat, lon):
    return transformer.transform(lon, lat)
df[['UTM_E', 'UTM_N']] = df.apply(lambda row: latlon_to_utm(row['Latitude'], row['Longitude']), axis=1, result_type='expand')

# Calculate Grid ID
df['Grid_X'] = (df['UTM_E'] // 1000).astype(int)
df['Grid_Y'] = (df['UTM_N'] // 1000).astype(int)

# Extract date
df['YearMonth'] = df['Date'].dt.to_period('M')

# Count crimes in every grid monthly
crime_counts = df.groupby(['YearMonth', 'Grid_X', 'Grid_Y']).size().reset_index(name='Crime_Count')

# Save results
crime_counts.to_csv('code\data\crime_data\step1e_crime_2021-2023_counts_by_grid.csv', index=False)
print("Saved as step1e_crime_2021-2023_counts_by_grid.csv")
