# HKUST Data Analysis

## Project Overview

This repository contains scripts for analyzing and processing electricity consumption data from the Hong Kong University of Science and Technology (HKUST). The project is organized into several modules, each serving a distinct purpose in the data analysis workflow.

## Directory Structure

```
├── Data_Preprocessing
│ └── Data_Resampling.py
├── Dorm_Room_Analysis
│ ├── Dorm_Room_Analysis.py
│ └── Seasonal_Plot.py
├── Evaluation
│ ├── Data_Calculation.py
│ └── Relative Error.py
├── Lighting_Analysis
│ ├── Lighting_Analysis.py
│ └── Lighting_Plot.py
├── Missing_Rate
│ ├── meter_category.xlsx
│ ├── Missing_Rate_Building_Hour.py
│ ├── Missing_Rate_Building_Hour_Plot.py
│ ├── Missing_Rate_Sampling_Times.py
│ └── Missing_Rate_Sampling_Times_Plot.py
├── Query_Example
│ ├── Building_Query.py
│ ├── Equipment_Query.py
│ └── Zone_Query.py
```


### Data Preprocessing

- **Data_Resampling.py**: This script is designed to process raw electricity consumption data by resampling it into consistent intervals.

### Dorm Room Analysis

- **Dorm_Room_Analysis.py**: This script loads and interpolates meter data for bedrooms and toilets on the 1F floor of GGT student hall. It queries the RDF graph for associated meters, processes the data, and calculates power consumption. The cleaned data is saved to a CSV file.
- **Seasonal_Plot.py**: This script visualizes the hourly power distribution for bedrooms and toilets over different seasons. It generates a line plot showing average kW for each hour, categorized by season, and saves the plot as a PNG file.

### Lighting Analysis

- **Lighting_Analysis.py**: This script performs analysis on lighting data. It includes functions to load data from Excel files, process it, and analyze lighting patterns in different floors of the academic buildings.
- **Lighting_Plot.py**: This script generates plots for visualizing the results of the lighting analysis. It uses Matplotlib to create visual representations of the lighting data over specified periods.

### Evaluation

- **Data_Calculation.py**: This script processes data for each zone, calculating total and sub-meter energy consumption. It handles missing meters and outputs the results to CSV files.
- **Relative Error.py**: This script calculates the Mean Absolute Error (MAE) percentage between total and sub-metered energy consumption, filtering out outliers using the IQR method.

### Missing Rate

- **meter_category.xlsx**: An Excel file categorizing different meters.

- **Missing_Rate_Building_Hour.py**: This script calculates the missing rate of electricity consumption data on an hourly basis for each building.

- **Missing_Rate_Building_Hour_Plot.py**: This script generates heatmaps to visualize the hourly missing rates for each building. It processes data files and creates a comprehensive heatmap for analysis.

- **Missing_Rate_Sampling_Times.py**: This script calculates the missing rates based on different sampling times. It processes the data to identify gaps and inconsistencies.

- **Missing_Rate_Sampling_Times_Plot.py**: This script generates plots to visualize the missing rates across different sampling intervals. It helps in understanding the data integrity over time.

### Query Example

- **Building_Query.py**: This script queries building-related data using SPARQL. It extracts relevant building information from the dataset and prints the results.

- **Equipment_Query.py**: This script queries equipment-related data. It retrieves information about various equipment types within the buildings and processes the results for analysis.

- **Zone_Query.py**: This script queries zone-related data. It identifies different zones within the academic buildings and retrieves associated meter data.

## Usage Note

### Prerequisites

Ensure you have the required Python packages installed. You can install them using the following command:

```
pip install pandas rdflib matplotlib tqdm seaborn scikit-learn
```

## Contributions 

Contributions to improve the scripts and documentation are welcome. Please fork the repository and submit pull requests.

## License 

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact 
For any inquiries or issues, please contact Professor [Zhe (Walter) Wang](https://walterzwang.github.io/) or postgraduate student [Mingchen Li](https://limingchen159.github.io/).

