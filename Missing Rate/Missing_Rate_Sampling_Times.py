# -*- coding: utf-8 -*-
"""
@Project ：HKUST_Meter_Brick
@File    ：Missing_Rate_Sampling_Times.py
@Time: 06/02/2024 6:22 PM
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

data_check = pd.read_excel("..\Data Preprocessing\Sampling_Info.xlsx")

# Remove 'GUI_NO.' prefix from the 'File Name' column
data_check['File Name'] = data_check['File Name'].str.replace('GUI_NO.', '', regex=False)

file_names_15T = data_check[data_check["Sampling Time"] == "15T"]["File Name"].tolist()
file_names_30T = data_check[data_check["Sampling Time"] == "30T"]["File Name"].tolist()
file_names_60T = data_check[data_check["Sampling Time"] == "60T"]["File Name"].tolist()
file_names_1440T = data_check[data_check["Sampling Time"] == "1440T"]["File Name"].tolist()

# Define a function to calculate quarterly missing rates
def calculate_quarterly_missing_rates(file_names, resample_freq=None):
    quarterly_missing_rates = {}

    for file_name in tqdm(file_names):
        file_path = os.path.join(resampled_data_path, file_name)

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

# Calculate and save the results for each sampling time
results_15T = calculate_quarterly_missing_rates(file_names_15T)
results_15T.to_csv("average_quarterly_missing_rates_15T.csv", index=False)

results_30T = calculate_quarterly_missing_rates(file_names_30T + file_names_15T, resample_freq='30T')
results_30T.to_csv("average_quarterly_missing_rates_30T.csv", index=False)

results_60T = calculate_quarterly_missing_rates(file_names_60T + file_names_30T + file_names_15T, resample_freq='60T')
results_60T.to_csv("average_quarterly_missing_rates_60T.csv", index=False)

results_1440T = calculate_quarterly_missing_rates(file_names_1440T + file_names_60T + file_names_30T + file_names_15T, resample_freq='1440T')
results_1440T.to_csv("average_quarterly_missing_rates_1440T.csv", index=False)

print("Average quarterly missing rates have been calculated and saved.")
