# -*- coding: utf-8 -*-
"""
@Project ：HKUST_Meter_Brick
@File    ：Equipment Query.py
@Time: 05/25/2024 9:34 PM
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


# Open and parse the TTL file containing meter metadata
with open("../HKUST_Meter_Metadata.ttl", "r", encoding="utf-8") as file:
    ttl_data = file.read()
    g = Graph()
    # Parse the TTL data to create a graph
    g.parse(data=ttl_data, format='ttl')

# SPARQL query to select all zones that are part of the Academic Building
query_all = f"""
    SELECT  ?zone
    WHERE {{
        ?zone a brick:Zone .
        bldg:Academic_Building brick:hasPart ?zone  .
    }}
"""

# Execute the SPARQL query
result = g.query(query_all)

# Initialize a counter for demonstration purposes
n = 0

# Iterate through the query results
for row in result:
    # For demonstration, break after the first iteration
    if n == 1:
        break
    # Extract the zone name from the URI
    Zone_name = row['zone'].split("#")[-1]

    # Query to select all meters associated with the zone
    temp_query = f"""
        SELECT  ?meter
        WHERE {{
            bldg:{Zone_name} brick:isMeteredBy ?meter .
            ?meter rdf:type/rdfs:subClassOf* brick:Meter .
        }}
    """
    result_meter = g.query(temp_query)

    # Initialize a list to store meter names
    meter_list = []

    # Iterate through the meter query results and append to the list
    for meter in result_meter:
        meter_list.append(meter['meter'].split("#")[-1])

    # Print the zone name and its associated meters
    print(Zone_name + ":   " + str(meter_list))

# SPARQL query to select all equipment in a specific zone, excluding electrical meters
query_equip = """
    SELECT  ?equip
    WHERE {
        bldg:Zone_E_Lift_27_28_Elect  brick:hasPart ?equip  .
        ?equip a ?Equipment .
        ?Equipment  rdf:type/rdfs:subClassOf*  brick:Equipment  .
        FILTER(?aa != brick:Electrical_Meter)
    }
"""

# Execute the SPARQL query for equipment
results_equip = g.query(query_equip)

# Process the query results
equipment = [str(row['equip']) for row in results_equip]
print("Equipment:", equipment)
print("Equipment number: " + str(len(equipment)))
