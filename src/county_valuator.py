import pandas as pd

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

# Calculate the county valuation
county_valuator["County_Valuation"] = county_valuator["Median_Home_Price_Q1_2024"] * county_valuator["2023_Units"]

# Export the dataframe to a csv file
county_valuator.to_csv("../data/cleaned_data/county_valuator.csv", index = False)


