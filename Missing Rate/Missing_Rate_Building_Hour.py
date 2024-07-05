# -*- coding: utf-8 -*-
"""
@Project ：HKUST_Meter_Brick
@File    ：Missing_Rate_Building_Hour.py
@Time: 06/05/2024 6:22 PM
@Author: Mingchen Li
"""
import os
import pandas as pd
from tqdm import tqdm
import gc

# Get the current working directory
resampled_data_path = os.getcwd() + r"\Resampled Data"
current_directory = os.getcwd()

# Get the list of all files and directories in this directory
file_names = os.listdir(resampled_data_path)

# Initialize a list to store the results
results = []

# Load meter category data
data_check = pd.read_excel("meter_category.xlsx")

# Group files by category
categories = data_check['Category'].unique()
category_files = {category: data_check[data_check['Category'] == category]['Meter'].tolist() for category in categories}

# Define a function to calculate quarterly missing rates
def calculate_quarterly_missing_rates(file_names, resample_freq='H'):
    quarterly_missing_rates = {}

    for file_name in tqdm(file_names):
        file_name = file_name.split('_')[1]
        file_path = os.path.join(resampled_data_path, file_name + ".xlsx")

        # Check if the file exists, if not, skip it
        if not os.path.exists(file_path):
            print(f"File {file_path} does not exist. Skipping.")
            continue

        # Read file data
        df = pd.read_excel(file_path)

        # Convert 'time' column to datetime type
        df['time'] = pd.to_datetime(df['time'], errors='coerce')

        # Drop rows with invalid 'time'
        df = df.dropna(subset=['time'])

        # Filter out unreasonable years (e.g., before 2022)
        df = df[df['time'].dt.year >= 2022]

        # Check if data is already daily, if so, skip resampling
        if df['time'].dt.date.nunique() == df.shape[0]:
            resample_freq = None

        # Resample if necessary
        if resample_freq:
            df = df.set_index('time').resample(resample_freq).first().reset_index()

        # Group by quarter and calculate missing rate for each quarter
        df['quarter'] = df['time'].dt.to_period('Q')
        missing_rates = df.groupby('quarter')['number'].apply(lambda x: x.isna().mean())

        # Add results to quarterly_missing_rates dictionary
        for quarter, rate in missing_rates.items():
            if quarter not in quarterly_missing_rates:
                quarterly_missing_rates[quarter] = []
            quarterly_missing_rates[quarter].append(rate)

        # Free memory
        gc.collect()

    # Calculate the average missing rate for each quarter
    average_quarterly_missing_rates = {quarter: sum(rates) / len(rates) for quarter, rates in quarterly_missing_rates.items()}

    # Convert the dictionary to a sorted DataFrame
    results_df = pd.DataFrame(list(average_quarterly_missing_rates.items()), columns=['Quarter', 'Average Missing Rate'])
    results_df = results_df.sort_values(by='Quarter')

    return results_df

# Create new output directory if not exists
new_output_dir = "Building_Missing_Rate"
if not os.path.exists(new_output_dir):
    os.makedirs(new_output_dir)

# Calculate and save the results for each category
for category, files in category_files.items():
    results = calculate_quarterly_missing_rates(files)
    results.to_csv(f"{new_output_dir}/average_quarterly_missing_rates_{category}.csv", index=False)

print("Average quarterly missing rates have been calculated and saved for each category in the new directory.")
