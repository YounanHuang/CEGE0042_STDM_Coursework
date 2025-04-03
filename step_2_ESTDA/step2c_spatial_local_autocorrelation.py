import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from libpysal.weights import DistanceBand
from esda.moran import Moran_Local
import contextily as ctx 

# Read csv file
file_path = r"code\\data\\crime_data\\step1c_crime_2020-12_data.csv" 
df = pd.read_csv(file_path)

# Delete missing values
df = df.dropna(subset=['Latitude', 'Longitude'])

# Create GeoDataFrame
geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# Calculate crime count at each point
gdf['crime_count'] = gdf.groupby(['Latitude', 'Longitude'])['Latitude'].transform('count')
crime_counts = gdf['crime_count'].values

# Constructing distance-based weight matrix（0.01 ≈ 1.1km）
w = DistanceBand.from_dataframe(gdf, threshold=0.01, binary=True)
w.transform = 'r' 

# Calculate local Moran’s I
local_moran = Moran_Local(crime_counts, w)

# Save results into GeoDataFrame
gdf['Moran_I'] = local_moran.Is  # Moran’s I 
gdf['p_value'] = local_moran.p_sim  # p-value
gdf['LISA_cluster'] = 'Not Significant'

# Setting significance threshold（p < 0.05）
sig_threshold = 0.05

# Analyse LISA result
gdf.loc[(gdf['p_value'] < sig_threshold) & (local_moran.q == 1), 'LISA_cluster'] = 'High-High (Hotspot)' 
gdf.loc[(gdf['p_value'] < sig_threshold) & (local_moran.q == 2), 'LISA_cluster'] = 'Low-High'  
gdf.loc[(gdf['p_value'] < sig_threshold) & (local_moran.q == 3), 'LISA_cluster'] = 'Low-Low (Coldspot)' 
gdf.loc[(gdf['p_value'] < sig_threshold) & (local_moran.q == 4), 'LISA_cluster'] = 'High-Low'

# Set color
colors = {
    'High-High (Hotspot)': 'red',
    'Low-High': 'orange',
    'Low-Low (Coldspot)': 'blue',
    'High-Low': 'green',
    'Not Significant': 'gray'
}

# Visualize LISA result
fig, ax = plt.subplots(figsize=(10, 6))
gdf.plot(ax=ax, color=gdf['LISA_cluster'].map(colors), alpha=0.7, edgecolor='k', markersize=20)
ctx.add_basemap(ax, crs=gdf.crs, source=ctx.providers.CartoDB.Positron)
ax.set_title("Local Moran's I (LISA) - Crime Clusters", fontsize=14)
ax.axis('off')
plt.show()
