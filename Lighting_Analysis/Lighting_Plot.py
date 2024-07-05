# -*- coding: utf-8 -*-
"""
@Project ：HKUST_Meter_Brick
@File    ：Lighting_Plot.py
@Time: 05/16/2024 6:41 PM
@Author: Mingchen Li
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set the style for the plot and the color scheme
sns.set(style="whitegrid")
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=plt.cm.tab10.colors)

# Create a 4x2 subplot layout (8 plots in total)
fig, axes = plt.subplots(4, 2, figsize=(16, 20))
axes = axes.flatten()  # Flatten the axes array for easy indexing

# Set the overall title for the entire figure
fig.suptitle('Hourly kW Distribution Over 2 years: Weekdays vs. Weekends', fontsize=16)

# Define the uniform y-axis range for the plots; this may need adjustment based on actual data
y_min, y_max = 0, 1800  # Example range, may need adjustment

# List of floor levels to be plotted
floors = ['GF', '1F', '2F', '3F', '4F', '5F', '6F', '7F']

# Loop through each floor and generate the corresponding plot
for i, floor in enumerate(floors):
    # Load the data for the current floor
    final_df_cleaned = pd.read_csv('final_data_' + floor + '.csv')

    # Convert the 'time' column to datetime format
    final_df_cleaned['time'] = pd.to_datetime(final_df_cleaned['time'])

    # Extract the hour and day of the week from the 'time' column
    final_df_cleaned['hour'] = final_df_cleaned['time'].dt.hour
    final_df_cleaned['day_of_week'] = final_df_cleaned['time'].dt.dayofweek

    # Determine if the day is a weekday or weekend
    final_df_cleaned['weekday'] = final_df_cleaned['day_of_week'].apply(lambda x: 'Weekday' if x < 5 else 'Weekend')

    # Plot the data using a boxplot
    ax = axes[i]
    sns.boxplot(x='hour', y='kW', hue='weekday', data=final_df_cleaned, ax=ax, palette='Set2', showfliers=False)
    ax.set_title(f'HKUST Academic Building {floor}', loc='left', fontweight='bold', fontsize=14)
    ax.set_xlabel('Hour of the Day')
    ax.set_ylabel('Lighting Power (kW)')
    ax.set_xticklabels([f"{h:02d}:00" for h in range(24)], rotation=90)  # Set x-axis labels to show hours in "00:00" format

    # Set the y-axis range for all floors except the ground floor (GF)
    if floor != 'GF':
        ax.set_ylim(y_min, y_max)

    # Place the legend above each plot
    ax.legend(loc='upper right', bbox_to_anchor=(1, 1.2), fancybox=True, ncol=5)

# Adjust the layout to prevent the overall title from overlapping with the subplots
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Save the figure to a file with high resolution
plt.savefig('Hourly_kW_Distribution_GF_7F.png', dpi=300, format='png')

# Display the plot
plt.show()
