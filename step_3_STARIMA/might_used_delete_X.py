### This code is to delete the string "X" in the first row of result xlxs file by step3e.r, because step3e.r sometimes might generate "X"

import pandas as pd

def clean_excel_columns(input_path, output_path):
    try:
        # Read file
        df = pd.read_excel(input_path)
        
        # Get original column name
        original_columns = df.columns.tolist()
        
        # Process column name
        new_columns = []
        for i, col in enumerate(original_columns):
            if i == 0:
                new_columns.append(col)
            else:
                # Delete "X"
                new_col = col.lstrip('X') if str(col).startswith('X') else col
                new_columns.append(new_col)
        
        # Apply new column name
        df.columns = new_columns
        
        # Save file
        df.to_excel(output_path, index=False)
        print(f"Saved to:{output_path}")
        
    except Exception as e:
        print(f"Error:{str(e)}")

input_file = "code\data\crime_data\step3e_STARIMA_crime_predict.xlsx" 
output_file = "code\data\crime_data\step3e.xlsx"  
clean_excel_columns(input_file, output_file)