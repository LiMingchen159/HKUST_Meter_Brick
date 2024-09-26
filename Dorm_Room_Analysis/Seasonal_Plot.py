# -*- coding: utf-8 -*-
"""
@Project ：HKUST_Brick 
@File    ：Seasonal_Plot.py
@Time: 09/26/2024 15:01
@Author: Mingchen Li
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set the style and color scheme for the plot
sns.set(style="whitegrid")
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=plt.cm.tab10.colors)

# Create a figure and axis for a single plot
fig, ax = plt.subplots(figsize=(10, 6))

# Set the overall title for the plot
fig.suptitle('Hourly kW Distribution Over Seasons for 1F', fontsize=16)

# Define y-axis range (adjust based on your actual data)
y_min, y_max = 0, 16  # Example range, you might need to adjust it based on your data

# Function to categorize months into seasons
def get_season(month):
    if 3 <= month <= 5:
        return 'Spring'
    elif 6 <= month <= 8:
        return 'Summer'
    elif 9 <= month <= 11:
        return 'Autumn'
    else:
        return 'Winter'

# Load the data for the 1F floor
final_df_cleaned = pd.read_csv('final_data_1F_Bedroom_and_Toilets.csv')

# Convert 'time' column to datetime type
final_df_cleaned['time'] = pd.to_datetime(final_df_cleaned['time'])

# Extract hour from the 'time' column
final_df_cleaned['hour'] = final_df_cleaned['time'].dt.hour

# Add a 'season' column based on the month
final_df_cleaned['season'] = final_df_cleaned['time'].dt.month.apply(get_season)

# Group the data by season and hour, and compute the mean kW for each group
seasonal_data = final_df_cleaned.groupby(['season', 'hour']).mean().reset_index()

# Define the seasons for plotting
seasons = ['Spring', 'Summer', 'Autumn', 'Winter']

# Plot the kW data for each season
for season in seasons:
    subset = seasonal_data[seasonal_data['season'] == season]
    ax.plot(subset['hour'], subset['kW'], label=season)

# Set the title, labels, and other properties for the plot
ax.set_title('Global Graduate Tower 1F', loc='left', fontweight='bold', fontsize=14)
ax.set_xlabel('Hour of the Day')
ax.set_ylabel('Bedroom & Toilet Power (kW)')
ax.set_xticks(range(24))  # Set ticks for all 24 hours
ax.set_xticklabels([f"{h:02d}:00" for h in range(24)], rotation=45)  # Label each hour in 24-hour format
ax.set_ylim(y_min, y_max)  # Set the y-axis limits
ax.legend(loc='upper right', bbox_to_anchor=(1, 1), fancybox=True, ncol=4)  # Add legend for seasons

# Adjust layout to prevent overlap
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Save the figure to a file
plt.savefig('Seasonal_Hourly_kW_Distribution_1F.png', dpi=300, format='png')  # Save at 300 dpi for high quality

# Display the plot
plt.show()
