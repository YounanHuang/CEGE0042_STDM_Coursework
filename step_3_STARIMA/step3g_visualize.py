import pandas as pd
import matplotlib.pyplot as plt

# Read file
pred_df = pd.read_excel("code\data\crime_data\step3e_STARIMA_crime_predict.xlsx") 
true_df = pd.read_csv("code\data\crime_data\step3c_crime_2021-2023_counts_by_grid_transferred.csv")


# Preprocess Date format
def preprocess_dates(df):
    df['Date'] = pd.to_datetime(df['Date'])
    return df.set_index('Date')

pred_df = preprocess_dates(pred_df)
true_df = preprocess_dates(true_df)

# Calculate mean value of each time
pred_mean = pred_df.mean(axis=1).rename('Predicted')
true_mean = true_df.mean(axis=1).rename('Actual')

# Combine results
combined = pd.concat([pred_mean, true_mean], axis=1)

# Visualization settings
plt.figure(figsize=(12, 6))
ax = plt.gca()

# Plot polyline
combined['Predicted'].plot(ax=ax, color='orange', linestyle='--', label='Predicted')
combined['Actual'].plot(ax=ax, color='blue', linewidth=2, label='Actual')

plt.ylabel('Average Crime Count')
plt.title('Time Series Comparison: Predicted vs Actual Averages')
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()

plt.show()