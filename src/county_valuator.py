import pandas as pd
import numpy as np

# Read the csv files
county_price = pd.read_csv("../data/florida_counties_median_price.csv")
county_units = pd.read_csv("../data/florida_county_hosuing_units.csv")

# Drop the columns that are not needed
county_price = county_price.drop(columns = ["Monthly_Payment_Q1_2024", "Monthly_Payment_Q1_2023"])
county_units = county_units.drop(columns = ["Base_April_2020_Units", "2020_Units", "2021_Units", "2022_Units"])

# Merge the two dataframes
county_valuator = pd.merge(county_price, county_units, on = "County")

# Convert the columns to numeric
county_valuator["Median_Home_Price_Q1_2024"] = county_valuator["Median_Home_Price_Q1_2024"].str.replace("$", "").str.replace(",", "").astype("int64")
county_valuator["2023_Units"] = county_valuator["2023_Units"].str.replace(",", "").astype("int64")

# Prepopulate the County_Valuation column
county_valuator["County_Valuation"] = 0

# Calculate the county valuation
for idx, county in county_valuator.iterrows():
    data = np.random.normal(county["Median_Home_Price_Q1_2024"], county["Median_Home_Price_Q1_2024"] * 0.5, int(county["2023_Units"] * 0.64)) # Assume the median home price is normally distributed with a standard deviation of $100,000
    county_valuator.loc[idx, "County_Valuation"] = int(data.sum()) # 42% of units are single family homes (source: http://www.shimberg.ufl.edu/publications/tab2.pdf)

# Export the dataframe to a csv file
county_valuator.to_csv("../data/cleaned_data/county_valuator.csv", index = False)


