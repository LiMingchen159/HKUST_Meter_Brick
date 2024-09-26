# -*- coding: utf-8 -*-
"""
@Project ：HKUST_Brick
@File    ：Dorm_Room_Analysis.py
@Time: 09/26/2024 14:53
@Author: Mingchen Li
"""

import pandas as pd
from rdflib import Graph


def get_data_from_excel_file_with_str(meter_name):
    """
    Function to load and interpolate the meter data from an Excel file.

    Args:
        meter_name (str): The name of the meter to extract data from.

    Returns:
        pd.DataFrame: The loaded and interpolated data from the Excel file.
    """
    # Extract the meter ID from the provided meter name and append the '.xlsx' extension.
    meter_name = meter_name.split("_")[-1] + ".xlsx"

    # Load the data from the Excel file corresponding to the meter.
    data = pd.read_excel("../Resampled Data/" + meter_name)

    # Interpolate any missing values in the data using linear interpolation.
    data = data.interpolate(method='linear')

    return data


# Open and parse the TTL (Turtle) file
with open("../HKUST_Meter_Metadata.ttl", "r", encoding="utf-8") as file:
    ttl_data = file.read()
    g = Graph()

    # Parse the Turtle data into an RDF graph
    g.parse(data=ttl_data, format='ttl')

# SPARQL query to select all meters associated with the bedroom and toilet components on the 1F floor
query_all = f"""
    SELECT  ?meter
    WHERE {{
        bldg:Student_Hall_10_GGT_1F_Bedroom_and_Toilets  brick:isLocationOf  ?Equip  .
        ?Equip  brick:isMeteredBy  ?meter  .
    }}
"""
# Execute the SPARQL query on the RDF graph
results_all = g.query(query_all)

# Extract unique meters from the query results
GGT_With_Meter = list(set(row['meter'] for row in results_all))
print(GGT_With_Meter)

# List to store data from all meters
dfs = []

# Loop through each meter and retrieve the data
for i in range(0, len(GGT_With_Meter)):
    Single_Meter = GGT_With_Meter[i].split("#")[-1]  # Extract the meter ID
    print(Single_Meter)
    try:
        # Attempt to load data for the meter
        data = get_data_from_excel_file_with_str(Single_Meter)
    except FileNotFoundError:
        # Handle cases where the Excel file is not found
        print(f"File not found for {Single_Meter}")
        continue  # Skip to the next iteration if the file is missing
    except Exception as e:
        # Handle any other exceptions that might occur
        print(f"An error occurred for {Single_Meter}: {e}")
        continue  # Skip to the next iteration if an error occurs
    # Store the retrieved data in a DataFrame and add it to the list
    df = pd.DataFrame(data)
    dfs.append(df)

# Step 1: Resample each DataFrame to hourly intervals
resampled_dfs = []
for df in dfs:
    # Convert the 'time' column to a DateTime type and set it as the DataFrame index
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)

    # Resample the data to hourly intervals and calculate the mean for each hour
    resampled_df = df.resample('H').mean()

    # Add the resampled DataFrame to the list
    resampled_dfs.append(resampled_df)

# Step 2: Align all DataFrames by time and concatenate them into one DataFrame
aligned_df = pd.concat(resampled_dfs, axis=1)

# Step 3: Sum the data from all meters to create a new column 'All_kWh' representing total energy consumption
aligned_df['All_kWh'] = aligned_df.sum(axis=1)

# Keep only the 'All_kWh' column in the final DataFrame
final_df = aligned_df[['All_kWh']]
# Reset the index to make 'time' a regular column again
final_df.reset_index(inplace=True)

# Calculate the difference between consecutive hours to obtain power consumption in kW
final_df['kW'] = final_df['All_kWh'].diff().fillna(0)

# Step 4: Remove outliers using the Interquartile Range (IQR) method
Q1 = final_df['kW'].quantile(0.25)  # First quartile (25th percentile)
Q3 = final_df['kW'].quantile(0.75)  # Third quartile (75th percentile)
IQR = Q3 - Q1  # Interquartile range
# Filter the data to keep only values within 1.5 times the IQR from Q1 and Q3
filter = (final_df['kW'] >= Q1 - 1.5 * IQR) & (final_df['kW'] <= Q3 + 1.5 * IQR)
final_df_cleaned = final_df[filter]

# Print the cleaned final results
print(final_df_cleaned)

# Save the cleaned DataFrame to a CSV file
final_df_cleaned.to_csv(f'final_data_1F_Bedroom_and_Toilets.csv', index=False)
