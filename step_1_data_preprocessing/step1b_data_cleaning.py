import pandas as pd
from shapely.geometry import Point, MultiPolygon
from shapely import wkt
from tqdm import tqdm

tqdm.pandas(desc="Processing coordinates")

def load_chicago_boundary(boundary_file):
    """
    Load Chicago boundary from CSV with multipolygon format
    Returns a Shapely MultiPolygon object
    """
    # Read boundary file
    boundary_df = pd.read_csv(boundary_file)
    
    # Combine all multipolygons from the CSV
    polygons = []
    for wkt_str in boundary_df['the_geom']: 
        geom = wkt.loads(wkt_str)
        if geom.geom_type == 'MultiPolygon':
            polygons.extend(geom.geoms)
        elif geom.geom_type == 'Polygon':
            polygons.append(geom)
    
    return MultiPolygon(polygons)

def process_data(input_file, output_file, chicago_poly):
    """
    Process CSV file with three cleaning steps
    """
    # Read input data
    df = pd.read_csv(input_file)
    print("csv reading done")
    
    # ① Remove rows with missing values in critical columns
    df = df.dropna(subset=['Date', 'Longitude', 'Latitude'])
    print("① processing done")
    
    # ② Remove duplicate rows
    df = df.drop_duplicates()
    print("② processing done")
    
    # ③ Filter points within Chicago boundary
    # Convert coordinates to numeric type
    print("\n🌍 Starting spatial filtering...")
    
    df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
    df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
    
    # remove invalid coordinates
    valid_df = df.dropna(subset=['Longitude', 'Latitude'])
    invalid_coords = len(df) - len(valid_df)
    print(f"⚠️  {invalid_coords} invalid coordinates found")
    
    # Progress bar
    def spatial_filter(row):
        lon = row['Longitude']
        lat = row['Latitude']
        
        # Refresh the coordinate display every 100 rows
        if (row.name + 1) % 100 == 0:
            tqdm.write(f"📍 coordinate processed now:{lon:.5f}, {lat:.5f}")
        
        return chicago_poly.contains(Point(lon, lat))
    
    print("⏳ Executing spatial filtering...")
    valid_df['within_chicago'] = valid_df.progress_apply(spatial_filter, axis=1)
    
    # Integrate the results
    final_df = valid_df[valid_df['within_chicago']].drop(columns=['within_chicago'])
    print(f"\n✅ Spatial filter done | {len(valid_df)-len(final_df)} rows deleted | {len(final_df)} rows remained")
    
    # Save the results
    final_df.to_csv(output_file, index=False)
    print(f"💾 Results saved to:{output_file}")

if __name__ == "__main__":
    # Load Chicago boundary
    chicago_poly = load_chicago_boundary("code\data\Chicago_geom\City_Boundary.csv")
    
    # Process both time period files
    process_data("code\data\crime_data\step1a_crime_2011-2020_data.csv", "code\data\crime_data\step1b_crime_2011-2020_data.csv", chicago_poly)
    process_data("code\data\crime_data\step1a_crime_2021-2023_data.csv", "code\data\crime_data\step1b_crime_2021-2023_data.csv", chicago_poly)