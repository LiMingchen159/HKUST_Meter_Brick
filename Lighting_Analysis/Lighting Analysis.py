# -*- coding: utf-8 -*-
"""
@Project ：HKUST_Meter_Brick
@File    ：Lighting Analysis.py
@Time: 05/16/2024 4:34 PM
@Author: Mingchen Li
"""
import pandas as pd
from rdflib import Graph
import matplotlib.pyplot as plt

# List of floor information
Floor_Info = ['GF', '1F', '2F', '3F', '4F', '5F', '6F', '7F']

def get_data_from_excel_file_with_str(Lighting_name):
    """
    Get data from an Excel file based on the lighting name.

    Args:
        Lighting_name (str): The name of the lighting device.

    Returns:
        pd.DataFrame: The data from the Excel file.
    """
    Lighting_name = Lighting_name.split("_")[-1] + ".xlsx"
    # Load the data from the Excel file
    data = pd.read_excel("../Resampled Data/" + Lighting_name)
    data = data.interpolate(method='linear')
    return data

# Open and parse the TTL file
with open("../HKUST_Meter_Metadata.ttl", "r", encoding="utf-8") as file:
    ttl_data = file.read()
    g = Graph()
    g.parse(data=ttl_data, format='ttl')

for Floor in Floor_Info:
    print(Floor)

    # SPARQL query to select all related components
    query_all = f"""
        SELECT  ?meter
        WHERE {{
            bldg:Academic_Building_{Floor}  brick:isLocationOf*  ?Light  .
            ?Light a brick:Lighting .
            ?Light brick:isMeteredBy ?meter .
        }}
    """
    results_all = g.query(query_all)
    AcadBldg_With_Lighting = list(set(row['meter'] for row in results_all))
    # print(AcadBldg_With_Lighting)

    dfs = []
    for i in range(0, len(AcadBldg_With_Lighting)):
        Single_Meter = AcadBldg_With_Lighting[i].split("#")[-1]
        print(Single_Meter)
        try:
            data = get_data_from_excel_file_with_str(Single_Meter)
        except FileNotFoundError:
            continue  # Skip to the next iteration if the file is not found
        except Exception as e:
            continue  # Skip to the next iteration for any other exceptions
        df = pd.DataFrame(data)
        dfs.append(df)

    # Step 1: Resample each DataFrame to hourly intervals
    resampled_dfs = []
    for df in dfs:
        # Convert the 'time' column to DateTime type and set it as the index
        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)

        # Resample to hourly intervals and take the mean value
        resampled_df = df.resample('H').mean()

        # Collect the resampled DataFrame
        resampled_dfs.append(resampled_df)

    # Step 2: Align and merge all DataFrames by time
    aligned_df = pd.concat(resampled_dfs, axis=1)

    # Step 3: Sum horizontally to get a new column and delete other columns
    aligned_df['All_kWh'] = aligned_df.sum(axis=1)
    final_df = aligned_df[['All_kWh']]
    final_df.reset_index(inplace=True)  # Reset index to make 'time' a regular column

    # Calculate hourly differences to convert to kW
    final_df['kW'] = final_df['All_kWh'].diff().fillna(0)

    # Remove outliers using the IQR method
    Q1 = final_df['kW'].quantile(0.25)
    Q3 = final_df['kW'].quantile(0.75)
    IQR = Q3 - Q1
    filter = (final_df['kW'] >= Q1 - 1.5 * IQR) & (final_df['kW'] <= Q3 + 1.5 * IQR)
    final_df_cleaned = final_df[filter]

    # Save the cleaned final result to a CSV file
    final_df_cleaned.to_csv(f'final_data_{Floor}.csv', index=False)
