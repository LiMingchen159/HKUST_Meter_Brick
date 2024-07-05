# -*- coding: utf-8 -*-
"""
@Project ：HKUST_Meter_Brick
@File    ：Missing_Rate_Building_Hour_Plot.py
@Time: 06/08/2024 1:21 PM
@Author: Mingchen Li
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Get the current working directory
current_directory = os.getcwd() + "/Building_Missing_Rate"

# Initialize an empty DataFrame to store data from all buildings
all_data = pd.DataFrame()

# Loop through all files in the directory
for file_name in os.listdir(current_directory):
    # Check if the file name matches the pattern for average quarterly missing rates CSV files
    if file_name.startswith("average_quarterly_missing_rates") and file_name.endswith(".csv"):
        # Extract the building name from the file name
        building_name = file_name.split("average_quarterly_missing_rates_")[1].split(".csv")[0]
        file_path = os.path.join(current_directory, file_name)

        # Read the data from the CSV file
        df = pd.read_csv(file_path)
        # Add a column for the building name
        df['Building'] = building_name
        # Concatenate the data to the all_data DataFrame
        all_data = pd.concat([all_data, df])

# Convert the Quarter column to a PeriodIndex with quarterly frequency
all_data['Quarter'] = pd.PeriodIndex(all_data['Quarter'], freq='Q').to_timestamp()
# Pivot the data to create a format suitable for the heatmap
heatmap_data = all_data.pivot(index='Building', columns='Quarter', values='Average Missing Rate')

# Format the Quarter index to 'YYYYQX' format
heatmap_data.columns = heatmap_data.columns.to_period('Q').astype(str)

# Convert the missing rates to percentages and round to three decimal places
heatmap_data = (heatmap_data * 100).round(3)

# Plot the heatmap
plt.figure(figsize=(15, 10))
sns.heatmap(heatmap_data, annot=True, fmt=".3f", cmap="YlGnBu", cbar_kws={'label': 'Missing Rate (%)'})

# Set the title and labels
plt.title("Quarterly Average Missing Rates for Each Building")
plt.xlabel("Quarter")
plt.ylabel("Building")
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()
plt.savefig('Miss_Rate_Building_H', dpi=300)

# Display the heatmap
plt.show()
