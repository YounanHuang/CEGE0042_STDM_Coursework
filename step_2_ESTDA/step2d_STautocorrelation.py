import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.graphics.tsaplots import plot_acf

# Read csv file
crime_data = pd.read_csv('code\data\crime_data\step1c_crime_2020-12_data.csv')

crime_data['Date'] = pd.to_datetime(crime_data['Date'])

# 1. Aggregate by day
crime_data['date'] = crime_data['Date'].dt.date
crime_data['crime_count'] = 1 
crime_daily_december = crime_data.groupby('date')['crime_count'].sum()

# 2. Calculate and visualize ACF
plt.figure(figsize=(10, 6))
plot_acf(crime_daily_december, lags=30)
plt.title("Autocorrelation Function (ACF) of Chicago Crime")
plt.show()

### STACF calculation is in step 3, please look at step3d_STACF_STPACF.R

""" 
# 3. Calculate STACF

crime_data['date_idx'] = pd.factorize(crime_data['date'])[0]
coords = np.array(list(zip(crime_data['Latitude'], crime_data['Longitude'])))

dist_matrix = distance_matrix(coords, coords)
time_window = 1
space_threshold = 0.01 

# Calculate STACF
stacf_values = []
for t1 in range(len(crime_data['date_idx'])):
    for t2 in range(t1 + 1, len(crime_data['date_idx'])):
        if abs(crime_data['date_idx'][t1] - crime_data['date_idx'][t2]) <= time_window and dist_matrix[t1, t2] <= space_threshold:
            stacf_values.append((crime_data['crime_count'][t1], crime_data['crime_count'][t2]))

stacf_df = pd.DataFrame(stacf_values, columns=['crime_count_t1', 'crime_count_t2'])

stacf_corr = stacf_df.corr().iloc[0, 1]
print(f"STACF (Spatial-Temporal Correlation): {stacf_corr}")

# Visualize STACF
plt.figure(figsize=(10, 6))
plt.scatter(stacf_df['crime_count_t1'], stacf_df['crime_count_t2'], alpha=0.5)
plt.title("STACF (Spatial-Temporal Autocorrelation) for Crime Counts in December 2020")
plt.xlabel("Crime Count at Time 1")
plt.ylabel("Crime Count at Time 2")
plt.show()
 """