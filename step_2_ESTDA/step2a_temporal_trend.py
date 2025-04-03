import pandas as pd
import matplotlib.pyplot as plt

# Read csv file
file_path = "code\data\crime_data\step1b_crime_2011-2020_data.csv"
df = pd.read_csv(file_path, parse_dates=['Date'], dayfirst=False)

# Data preprocessing
df = df.dropna(subset=['Date'])  
df = df[(df['Date'].dt.year >= 2011) & (df['Date'].dt.year <= 2020)]

df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month_name()  # get month name

# ① Count crime monthly
monthly_total = (
    df.groupby('Month', observed=True)
    .size()
    .reset_index(name='Total_Crimes')
)

# Set month order
month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']
monthly_total['Month'] = pd.Categorical(
    monthly_total['Month'],
    categories=month_order,
    ordered=True
)
monthly_total = monthly_total.sort_values('Month')

# ② Count crime yearly
yearly_total = (
    df.groupby('Year', observed=True)
    .size()
    .reset_index(name='Total_Crimes')
    .sort_values('Year')
)

# Print results
print("2011-2020 monthly crime total:")
print(monthly_total.to_string(index=False))
print("\n2011-2020 yearly crime total:")
print(yearly_total.to_string(index=False))

# Save results to csv files
#monthly_total.to_csv("code\data\crime_data\step2a_2011-2020_monthly_crime.csv", index=False)
#yearly_total.to_csv("code\data\crime_data\step2a_2011-2020_yearly_crime.csv", index=False)

# Visualize
plt.figure(figsize=(12, 6))
plt.plot(monthly_total['Month'], monthly_total['Total_Crimes'], 'o-')
plt.title('Monthly Crime Trends (2011-2020)')
plt.xticks(rotation=45)
plt.ylabel('Total Crimes')
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(yearly_total['Year'], yearly_total['Total_Crimes'], 'o-')
plt.title('Yearly Crime Trends (2011-2020)')
plt.xticks(rotation=45)
plt.ylabel('Total Crimes')
plt.tight_layout()
plt.show()