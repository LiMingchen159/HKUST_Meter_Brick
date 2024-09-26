# -*- coding: utf-8 -*-
"""
@Project ：HKUST_Brick 
@File    ：Data_Calculation.py
@Time: 06/11/2024 1:05 AM
@Author: Mingchen Li
"""

import pandas as pd
from rdflib import Graph
import os
from tqdm import tqdm

def get_data_from_excel_file_with_str(meter_name):
    meter_name = meter_name.split("_")[-1] + ".xlsx"
    # Load the data from the Excel file
    data = pd.read_excel("../Resampled Data/" + meter_name)
    return data

# Open and parse the TTL file
with open("../HKUST_Meter_Metadata.ttl", "r", encoding="utf-8") as file:
    ttl_data = file.read()
    g = Graph()
    g.parse(data=ttl_data, format='ttl')

# Query to select all related components
query_all = """
    SELECT  ?zone
    WHERE {
        ?zone  a  brick:Zone  .
        ?meter  a  brick:Electrical_Meter  .
        ?zone  brick:isMeteredBy  ?meter  .
    }
"""
results_all = g.query(query_all)
All_Zone_With_Meter = list(set(row['zone'] for row in results_all))

# Progress bar for zones
for i in tqdm(range(len(All_Zone_With_Meter)), desc="Processing Zones"):
    Single_Zone = All_Zone_With_Meter[i].split("#")[-1]

    zone_meter = f"""
        SELECT  ?meter
        WHERE {{
            ?meter  a  brick:Electrical_Meter  .
            bldg:{Single_Zone}  brick:isMeteredBy  ?meter  .
        }}
    """
    results_zone_meter = g.query(zone_meter)
    meters = [str(row['meter']).split("#")[-1] for row in results_zone_meter]

    zone_has_meter = f"""
        SELECT  ?meter
        WHERE {{
            ?meter  a  brick:Electrical_Meter  .
            bldg:{Single_Zone}  brick:hasPart  ?meter  .
        }}
    """
    results_zone_has_meter = g.query(zone_has_meter)
    has_meters = [str(row['meter']).split("#")[-1] for row in results_zone_has_meter]
    has_meters = [item for item in has_meters if item not in meters]

    print(f"Zone: {Single_Zone}")
    print(f"  Total Meters: {meters}")
    print(f"  Sub Meters: {has_meters}")

    date_range = pd.date_range(start='2022-01-01', end='2024-05-27', freq='D')
    total_kwh_data = pd.DataFrame(index=date_range)
    sub_meter_kwh_data = pd.DataFrame(index=date_range)

    # Initialize lists to keep track of missing meters
    missing_meters = []
    missing_has_meters = []

    # Progress bar for meters
    for meter in tqdm(meters, desc=f"Processing Meters in {Single_Zone}", leave=False):
        try:
            data = get_data_from_excel_file_with_str(meter)
        except FileNotFoundError:
            missing_meters.append(meter)
            continue  # Skip to the next iteration
        except Exception as e:
            missing_meters.append(meter)
            continue  # Skip to the next iteration
        df = pd.DataFrame(data)
        df.set_index('time', inplace=True)
        df = df.resample('D').first()
        total_kwh_data = total_kwh_data.join(df['number'].rename(meter), how='left')

    for meter in tqdm(has_meters, desc=f"Processing Sub-Meters in {Single_Zone}", leave=False):
        try:
            data = get_data_from_excel_file_with_str(meter)
        except FileNotFoundError:
            missing_has_meters.append(meter)
            continue  # Skip to the next iteration
        except Exception as e:
            missing_has_meters.append(meter)
            continue  # Skip to the next iteration
        df = pd.DataFrame(data)
        df.set_index('time', inplace=True)
        df = df.resample('D').first()
        sub_meter_kwh_data = sub_meter_kwh_data.join(df['number'].rename(meter), how='left')

    # Skip this Zone if there are any missing meters
    if missing_meters or missing_has_meters:
        print(f"Skipping Zone: {Single_Zone} due to missing meters.")
        continue

    # Drop rows with any NaN values
    total_kwh_data.dropna(inplace=True)
    sub_meter_kwh_data.dropna(inplace=True)

    # Calculate the difference after summing all meters
    total_kwh_series = total_kwh_data.sum(axis=1).diff().dropna()
    sub_meter_kwh_series = sub_meter_kwh_data.sum(axis=1).diff().dropna()

    # Ensure we only keep the dates where both dataframes have valid data
    valid_indices = total_kwh_series.index.intersection(sub_meter_kwh_series.index)

    # Save the data to a CSV file
    output_df = pd.DataFrame({
        'date': valid_indices,
        'total_kwh': total_kwh_series[valid_indices],
        'sub_meter_kwh': sub_meter_kwh_series[valid_indices]
    })
    output_file = os.path.join("Zone_Data", f"{Single_Zone}_data.csv")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    output_df.to_csv(output_file, index=False)

print("Processing completed.")
