### This code is to aggregate crime data monthly, which will be used to analyse spatiotemporal autocorrelation

import pandas as pd

# Read csv file
df = pd.read_csv("code\data\crime_data\step1b_crime_2011-2020_data.csv")
raw_df = df[(df['Date'].dt.year == 2020)]

# Data preprocessing
raw_df['Month'] = pd.to_datetime(raw_df['Date']).dt.to_period('M')

raw_df['Latitude'] = raw_df['Latitude'].round(5)
raw_df['Longitude'] = raw_df['Longitude'].round(5)
raw_df = raw_df.dropna(subset=['Latitude', 'Longitude', 'Month'])
agg_df = raw_df.groupby(
    ['Month', 'Latitude', 'Longitude']
).size().reset_index(name='Crime_Count')

agg_df['Month'] = agg_df['Month'].dt.strftime('%Y-%m')

# Save results
agg_df.to_csv("code\data\crime_data\step1d_crime_2020_aggregated_monthly.csv", index=False)