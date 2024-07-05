# -*- coding: utf-8 -*-
"""
@Project ：HKUST_Meter_Brick
@File    ：Building Query.py
@Time: 05/27/2024 11:01 AM
@Author: Mingchen Li
"""
import pandas as pd
from rdflib import Graph
import matplotlib.pyplot as plt

def get_data_from_excel_file_with_str(Lighting_name):
    """
    Load data from an Excel file based on the lighting name.

    Args:
        Lighting_name (str): The name of the lighting device.

    Returns:
        pd.DataFrame: The data from the Excel file.
    """
    # Extract the specific part of the lighting name and append the .xlsx extension
    Lighting_name = Lighting_name.split("_")[-1] + ".xlsx"
    # Load the data from the specified Excel file
    data = pd.read_excel("../Resampled Data/" + Lighting_name)
    # Perform linear interpolation to fill in any missing data points
    data = data.interpolate(method='linear')
    return data

# Open and parse the TTL file containing metadata
with open("../HKUST_Meter_Metadata.ttl", "r", encoding="utf-8") as file:
    ttl_data = file.read()
    g = Graph()
    # Parse the TTL data to create a graph
    g.parse(data=ttl_data, format='ttl')

# SPARQL query to select all buildings
query_all = f"""
    SELECT ?building
    WHERE {{
        ?building a brick:Building .
    }}
"""

# Execute the SPARQL query
result = g.query(query_all)

# Iterate through the results and print the building names
for i in result:
    # Split the building URI and print only the building name
    print(i['building'].split("#")[-1])
