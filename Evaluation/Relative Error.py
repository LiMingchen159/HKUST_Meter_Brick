import pandas as pd
import numpy as np
import os
from sklearn.metrics import mean_absolute_error
from tqdm import tqdm


def calculate_metrics(file_path):
    """
    Function to calculate the Mean Absolute Error (MAE) percentage between total_kwh and sub_meter_kwh
    after removing outliers using the 1.5*IQR method.

    Args:
        file_path (str): Path to the CSV file containing the data.

    Returns:
        mae_percentage (float): The calculated MAE percentage.
    """
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Calculate the difference between total_kwh and sub_meter_kwh
    df['difference'] = df['total_kwh'] - df['sub_meter_kwh']

    # Remove outliers using the 1.5*IQR method
    Q1 = df['difference'].quantile(0.25)  # First quartile (25th percentile)
    Q3 = df['difference'].quantile(0.75)  # Third quartile (75th percentile)
    IQR = Q3 - Q1  # Interquartile Range
    lower_bound = Q1 - 1.5 * IQR  # Define the lower bound for outliers
    upper_bound = Q3 + 1.5 * IQR  # Define the upper bound for outliers
    df_filtered = df[(df['difference'] >= lower_bound) & (df['difference'] <= upper_bound)]  # Filter out outliers

    # Check if there are enough data points left after filtering
    if df_filtered.shape[0] < 2:
        return None  # Return None if there are insufficient data points for evaluation

    # Calculate Mean Absolute Error (MAE)
    mae = mean_absolute_error(df_filtered['total_kwh'], df_filtered['sub_meter_kwh'])

    # Calculate the mean of both total_kwh and sub_meter_kwh columns
    mean_total_kwh = np.mean(df_filtered['total_kwh'])
    mean_sub_meter_kwh = np.mean(df_filtered['sub_meter_kwh'])

    # Calculate the MAE percentage by dividing MAE by the larger of the two means
    mae_percentage = (mae / max(mean_total_kwh, mean_sub_meter_kwh)) * 100

    return mae_percentage  # Return the calculated MAE percentage


def process_all_files(directory):
    """
    Function to process all CSV files in a directory and calculate the average MAE percentage.

    Args:
        directory (str): The path to the directory containing the CSV files.

    Returns:
        average_mae_percentage (float): The average MAE percentage across all CSV files.
    """
    mae_percentages = []  # List to store MAE percentages for each file

    # Loop through each file in the directory
    for filename in tqdm(os.listdir(directory), desc="Processing CSV files"):
        # Only process files that end with '.csv'
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            # Calculate the MAE percentage for the current file
            mae_percentage = calculate_metrics(file_path)
            if mae_percentage is not None:
                # Print the result for the current file
                print(f"File: {filename}, MAE %: {mae_percentage:.2f}%")
                mae_percentages.append(mae_percentage)  # Add the result to the list
            else:
                # Print a message if there is insufficient data for evaluation
                print(f"File: {filename}, Insufficient data for evaluation")

    # If there are valid results, calculate the average MAE percentage
    if mae_percentages:
        average_mae_percentage = np.mean(mae_percentages)  # Compute the average of MAE percentages
    else:
        average_mae_percentage = float('nan')  # Return NaN if no valid data was found

    return average_mae_percentage  # Return the average MAE percentage


# Set the directory containing the CSV files
csv_directory = "Zone_Data"

# Process all files and calculate the average MAE percentage across the files
average_mae_percentage = process_all_files(csv_directory)

# Print the final average MAE percentage
print(f"Average MAE %: {average_mae_percentage:.2f}%")
