# -*- coding: utf-8 -*-
"""
@Project ：HKUST_Meter_Brick
@File    ：Data Resampling.py
@Time: 05/06/2024 7:34 PM
@Author: Mingchen Li
"""
import os
import pandas as pd
from tqdm import tqdm
import gc
import math

# Get the current working directory
row_data_path = os.getcwd() + r"\Raw_data"
current_directory = os.getcwd()
empty_data = []
duplicated_time = []
# Get the list of all files and directories in this directory
file_names = os.listdir(row_data_path)

# Initialize a list to store file names and sampling times
sampling_info = []

print("List of files and directories in the directory:", file_names)

# Loop through all the file names in the file_names list
for i in tqdm(range(0, len(file_names)), desc="Processing files"):
    # Construct the path to the file
    temp_path = row_data_path + "\\" + file_names[i]
    # Read the data from the Excel file
    data = pd.read_excel(temp_path, sheet_name='Sheet1')

    # Check if the data has less than 20 rows
    if len(data) < 100:
        print(f"File skipped due to insufficient data: {file_names[i]}")
        empty_data.append(file_names[i])
        continue  # Skip to the next iteration

    # Convert the 'time' column to datetime
    data['time'] = pd.to_datetime(data['time'])
    # Set the 'time' column as the index
    data.set_index('time', inplace=True)

    # Remove duplicate timestamps
    if data.index.duplicated().any():
        # print(f"File: {file_names[i]} contains duplicate timestamps. These records will be excluded.")
        duplicated_time.append(file_names[i])
        data = data.loc[~data.index.duplicated(keep='first')]

    last_times = data.index[-100:]
    # Calculate time differences
    time_deltas = last_times.to_series().diff().dt.total_seconds().dropna()

    # Find the most common time interval (in seconds)
    most_common_interval = time_deltas.mode()[0]

    # Convert seconds to minutes
    interval_in_minutes = most_common_interval / 60

    # Check if interval is approximately 15, 30, or 60 minutes using a tolerance
    if math.isclose(interval_in_minutes, 15, abs_tol=0.9):
        sampling_time = '15T'
    elif math.isclose(interval_in_minutes, 30, abs_tol=0.9):
        sampling_time = '30T'
    elif math.isclose(interval_in_minutes, 60, abs_tol=0.9):
        sampling_time = '60T'
    elif math.isclose(interval_in_minutes, 1440, abs_tol=0.9):
        sampling_time = '1440T'
    else:
        sampling_time = '60T'  # Default value
    # Add file name and sampling time to the list
    sampling_info.append([file_names[i], sampling_time])


    # Resample the data to 15-minute averages
    resampled_data = data.resample(sampling_time).mean()
    # Construct the path for the output file
    save_file_path = current_directory + "\\Resampled Data" + "\\" + file_names[i].split('.')[1] + '.xlsx'
    # save_file_path = current_directory + "\\Data\\Resampled Data" + "\\" + file_names[i].split('.')[1] + '.xlsx'
    # Save the resampled data to an Excel file
    resampled_data.to_excel(save_file_path)

    gc.collect()
# Final statement to indicate completion

# Convert the list to a DataFrame
df_sampling_info = pd.DataFrame(sampling_info, columns=['File Name', 'Sampling Time'])

# Save the DataFrame to an Excel file
output_path = current_directory + "\\Sampling_Info.xlsx"
df_sampling_info.to_excel(output_path, index=False)

print("All files processed and saved.")
print("Files with insufficient data:", empty_data)
# print("Files with duplicate timestamps:", duplicated_time)
