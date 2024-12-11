import pandas as pd
import json
import shapely 
import fiona
import geopandas as gdp
import pygmt

county_valuator = pd.read_csv("../data/cleaned_data/county_valuator.csv")
polygon_fiona = fiona.open("../data/shape_data/us-county-boundaries.shp")
coastal_fiona = fiona.open("../data/coast_data/cntbnd_sep15.shp")


# Build the GeoDataFrame from Fiona Collection
poly_gdf = gdp.GeoDataFrame.from_features([feature for feature in polygon_fiona])
# Get the order of the fields in the Fiona Collection; add geometry to the end
columns = list(polygon_fiona.meta["schema"]["properties"]) + ["geometry"]
# Re-order columns in the correct order
poly_bounds = poly_gdf[columns]

# Build the GeoDataFrame from Fiona Collection
coast_gdf = gdp.GeoDataFrame.from_features([feature for feature in coastal_fiona])
# Get the order of the fields in the Fiona Collection; add geometry to the end
columns = list(coastal_fiona.meta["schema"]["properties"]) + ["geometry"]
# Re-order columns in the correct order
coast_bounds = coast_gdf[columns]

# Drop the columns that are not needed
poly_bounds = poly_bounds.drop(columns = ['statefp', 'countyfp', 'countyns', 'geoid', 'name',
       'stusab', 'lsad', 'classfp', 'mtfcc', 'csafp', 'cbsafp', 'metdivfp',
       'funcstat', 'aland', 'awater', 'intptlat', 'intptlon', 'state_name',
       'countyfp_no'])

# Rename the columns
poly_bounds = poly_bounds.rename(columns = {'namelsad': 'County'})

# Drop the columns that are not needed
coast_bounds = coast_bounds.drop(columns = ['OBJECTID', 'NAME', 'FGDLCODE', 'FIPS', 'DESCRIPT', 'FGDLAQDATE', 'AUTOID', 'geometry'])

# Rename the columns
coast_bounds = coast_bounds.rename(columns = {'TIGERNAME': 'County'})
coast_bounds["County"] = coast_bounds["County"] + " County"

# Merge the two dataframes
county_bounds = poly_bounds.merge(coast_bounds, on = "County")

# Merge the three dataframes
county_bounds = county_valuator.merge(county_bounds, on = "County")

# Export the dataframe to a csv file
county_bounds.to_csv("../data/cleaned_data/county_bounds.csv", index = False)