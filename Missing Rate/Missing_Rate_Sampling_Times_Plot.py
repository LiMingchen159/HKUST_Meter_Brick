# -*- coding: utf-8 -*-
"""
@Project ：HKUST_Meter_Brick
@File    ：Missing_Rate_Sampling_Times_Plot.py
@Time: 06/03/2024 8:04 PM
@Author: Mingchen Li
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
results_15T = pd.read_csv("average_quarterly_missing_rates_15T.csv")
results_30T = pd.read_csv("average_quarterly_missing_rates_30T.csv")
results_60T = pd.read_csv("average_quarterly_missing_rates_60T.csv")
results_1440T = pd.read_csv("average_quarterly_missing_rates_1440T.csv")

# Convert Quarter to datetime for uniformity in indexing
results_15T['Quarter'] = pd.PeriodIndex(results_15T['Quarter'], freq='Q').to_timestamp()
results_30T['Quarter'] = pd.PeriodIndex(results_30T['Quarter'], freq='Q').to_timestamp()
results_60T['Quarter'] = pd.PeriodIndex(results_60T['Quarter'], freq='Q').to_timestamp()
results_1440T['Quarter'] = pd.PeriodIndex(results_1440T['Quarter'], freq='Q').to_timestamp()

# Merge all results into a single DataFrame
merged_results = pd.merge(results_15T, results_30T, on='Quarter', suffixes=('_15T', '_30T'))
merged_results = pd.merge(merged_results, results_60T, on='Quarter')
merged_results = pd.merge(merged_results, results_1440T, on='Quarter', suffixes=('_60T', '_1440T'))

# Rename columns for clarity
merged_results.columns = ['Quarter', '15 Minutes', '30 Minutes', '1 Hour', '1 Day']

# Set the Quarter as index
merged_results.set_index('Quarter', inplace=True)

# Format the Quarter index to 'YYYYQX' format
merged_results.index = merged_results.index.to_period('Q').astype(str)

# Convert missing rates to percentages and round to three decimal places
merged_results = (merged_results * 100).round(3)

scale = 3/2
# Plot the heatmap
plt.figure(figsize=(8*scale, 5*scale))  # Change the figure size to be square
sns.heatmap(merged_results.T, annot=True, fmt=".3f", cmap="YlGnBu", cbar_kws={'label': 'Missing Rate (%)'})
plt.title('Missing Rates of Electrical Meter Data')
plt.xlabel('Quarter')
plt.ylabel('Sampling Time')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()
plt.savefig('Miss_Rate_Sampling_Times', dpi=300)
plt.show()
