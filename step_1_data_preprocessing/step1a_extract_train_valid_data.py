import csv
from datetime import datetime

def parse_date(date_str):
    """Parse different datetime formats from the input string"""
    formats = [
        "%m/%d/%Y %I:%M:%S %p",  # Format with AM/PM and seconds
        "%m/%d/%Y %I:%M %p",     # Format with AM/PM without seconds
        "%m/%d/%Y %H:%M:%S",     # 24-hour format with seconds
        "%m/%d/%Y %H:%M"         # 24-hour format without seconds
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    raise ValueError(f"Unparsable date format: {date_str}")

# Define time period boundaries
period1_start = datetime(2011, 1, 1)
period1_end = datetime(2020, 12, 31, 23, 59, 59) # Define data from 2011_01_01 to 2020_12_31 as train dataset
period2_start = datetime(2021, 1, 1)
period2_end = datetime(2023, 12, 31, 23, 59, 59) # Define data from 2021_01_01 to 2023_12_31 as validation dataset

# Input and output csv files
input_filename = "code\data\crime_data\original_data_Crimes_-_2001_to_Present.csv"
output_2011_2020 = "code\data\crime_data\step1a_crime_2011-2020_data.csv" # Output the train dataset
output_2021_2023 = "code\data\crime_data\step1a_crime_2021-2023_data.csv" # Output the validation dataset

# Extract the train dataset and the validation dataset
with open(input_filename, mode="r", newline="", encoding="utf-8") as infile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    
    with open(output_2011_2020, mode="w", newline="", encoding="utf-8") as outfile1, \
         open(output_2021_2023, mode="w", newline="", encoding="utf-8") as outfile2:
        
        writer1 = csv.DictWriter(outfile1, fieldnames=fieldnames)
        writer2 = csv.DictWriter(outfile2, fieldnames=fieldnames)
        writer1.writeheader()
        writer2.writeheader()
        
        for row in reader:
            try:
                dt = parse_date(row["Date"])
            except ValueError as e:
                print(f"Skipping row due to error: {e}")
                continue
            
            if period1_start <= dt <= period1_end:
                writer1.writerow(row)
            elif period2_start <= dt <= period2_end:
                writer2.writerow(row)

print("Data splitting completed successfully.")