import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from libpysal.weights import DistanceBand
from esda.moran import Moran
import matplotlib.pyplot as plt

# Calculate Moran's I
def calculate_morans_i(file_path, distance_threshold=0.01):
    df = pd.read_csv(file_path)
    df = df.dropna(subset=['Latitude', 'Longitude'])  # Delete missing values
    
    # Construct GeoDataFrame
    geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry)
    
    # Calculate crime count at each point
    gdf['crime_count'] = gdf.groupby(['Latitude', 'Longitude'])['Latitude'].transform('count')
    crime_counts = gdf['crime_count'].values
    
    # Constructing distance-based weight matrix
    w = DistanceBand.from_dataframe(gdf, threshold=distance_threshold, binary=True)
    w.transform = 'r'
    
    # Calculate Moran's I
    moran = Moran(crime_counts, w)
    crime_counts_std = (crime_counts - np.mean(crime_counts)) / np.std(crime_counts)
    spatial_lag = w.sparse @ crime_counts_std

    # Plot Moran's I scatterplot
    plt.figure(figsize=(6, 6))
    plt.scatter(crime_counts_std, spatial_lag, edgecolor='k', alpha=0.6)
    plt.axhline(0, color='r', linestyle='--')
    plt.axvline(0, color='r', linestyle='--')
    plt.xlabel("Standardized Crime Count")
    plt.ylabel("Spatial Lag")
    plt.title("Moran's I Scatterplot")
    plt.show()
    
    return moran.I, moran.p_sim



file_path = r"code\data\crime_data\step1c_crime_2020-12_data.csv"
morans_i, p_value = calculate_morans_i(file_path)
print(f"Moran's I: {morans_i}, p-value: {p_value}")

