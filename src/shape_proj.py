from functools import partial

import pyproj
from shapely import geometry
from shapely.geometry import Point
from shapely.ops import transform

import pandas as pd
import geopandas as gpd

import pygmt

import argparse

# Define the lon, lat, and radius
parser = argparse.ArgumentParser(description="Create a shape projection")
parser.add_argument("--lon", type=float, default=-82.204141, help="Longitude of the center of the circle")
parser.add_argument("--lat", type=float, default=29.471344, help="Latitude of the center of the circle")
parser.add_argument("--radius64", type=float, default=120, help="Radius of 64 circle in km")
parser.add_argument("--radius_max", type=float, default=60, help="Radius of max circle in km")
args = parser.parse_args()

lon, lat = args.lon, args.lat 
radius64, radius_max = (args.radius64 * 1000), (args.radius_max * 1000)

print(f"Longitude: {lon}, Latitude: {lat}, Radius64: {radius64/1000}km, Radius Max: {radius_max/1000}km")

local_azimuthal_projection = "+proj=aeqd +R=6371000 +units=m +lat_0={} +lon_0={}".format(
    lat, lon
)
wgs84_to_aeqd = partial(
    pyproj.transform,
    pyproj.Proj("+proj=longlat +datum=WGS84 +no_defs"),
    pyproj.Proj(local_azimuthal_projection),
)
aeqd_to_wgs84 = partial(
    pyproj.transform,
    pyproj.Proj(local_azimuthal_projection),
    pyproj.Proj("+proj=longlat +datum=WGS84 +no_defs"),
)

center = Point(float(lon), float(lat))
point_transformed = transform(wgs84_to_aeqd, center)
buffer = point_transformed.buffer(radius64)
buffer_small = point_transformed.buffer(radius_max)
# Get the polygon with lat lon coordinates
circle_poly = transform(aeqd_to_wgs84, buffer)
circle_poly_small = transform(aeqd_to_wgs84, buffer_small)


# Read the csv files
county_bounds = pd.read_csv("../data/cleaned_data/county_bounds.csv")

# Convert the geometry column to a GeoSeries
county_bounds['geometry'] = gpd.GeoSeries.from_wkt(county_bounds['geometry'])

# Find the counties that overlap with the radius 64
county_bounds["intersects_big"] = county_bounds["geometry"].apply(
    lambda x: circle_poly.intersects(x) if type(x) != geometry.multipolygon.MultiPolygon else any(
        circle_poly.intersects(poly) for poly in x.geoms
    )
)

# Find the counties that overlap with the radius max
county_bounds["intersects_small"] = county_bounds["geometry"].apply(
    lambda x: circle_poly_small.intersects(x) if type(x) != geometry.multipolygon.MultiPolygon else any(
        circle_poly_small.intersects(poly) for poly in x.geoms
    )
)

# Filter the counties that overlap with the circle
intersections_64 = county_bounds[county_bounds["intersects_big"] == True]
intersections_max = county_bounds[county_bounds["intersects_small"] == True]

# Remove the intersections from 64 that are also in max
only_intersections_64 = intersections_64[~intersections_64["intersects_small"]]

# Create a GMT figure
fig = pygmt.Figure()
region = [-87.9, -79, 24, 31.2]
fig.basemap(region=region, projection="M4i", frame=True)
fig.coast( 
    water='skyblue', 
    shorelines=True)

# If the county is a multipolygon, draw the polygons individually
def draw_multipolygon(fig, multipolygon, draw=True, fill="orange"):
    for polygon in list(multipolygon.geoms):
        if type(polygon) == geometry.multipolygon.MultiPolygon:
            draw_multipolygon(fig, polygon)
            return
        if draw:
            x, y = polygon.exterior.xy
            fig.plot(x=x, y=y, pen="black")
        else:
            x, y = polygon.exterior.xy
            fig.plot(x=x, y=y, fill=fill, intensity=0.40)

# Highlight the counties that intersect with the 64 circle
for county in only_intersections_64['geometry']:
    if type(county) == geometry.multipolygon.MultiPolygon:
        draw_multipolygon(fig, county, draw=False, fill="orange")
        continue
    x, y = county.exterior.xy
    fig.plot(x=x, y=y, fill="orange", intensity=0.30)

# Highlight the counties that intersect with the max circle
for county in intersections_max['geometry']:
    if type(county) == geometry.multipolygon.MultiPolygon:
        draw_multipolygon(fig, county, draw=False, fill="red")
        continue
    x, y = county.exterior.xy
    fig.plot(x=x, y=y, fill="red", intensity=0.30)

# Draw the county boundaries
for county in county_bounds['geometry']:
    if type(county) == geometry.multipolygon.MultiPolygon:
        draw_multipolygon(fig, county)
        continue
    x, y = county.exterior.xy
    fig.plot(x=x, y=y, pen="black")

# Draw the Radius 64
circle_poly_simple = circle_poly.simplify(0.01)
fig.plot(x=circle_poly_simple.exterior.xy[0], y=circle_poly_simple.exterior.xy[1], pen="2p,orange", fill="orange", intensity=0.10, transparency=40)

# Draw the Radius Max
circle_poly_simple = circle_poly_small.simplify(0.01)
fig.plot(x=circle_poly_simple.exterior.xy[0], y=circle_poly_simple.exterior.xy[1], pen="2p,red", fill="red", intensity=0.20, transparency=50)

# Draw the center of the circle
fig.plot(x=[lon], y=[lat], style='c0.1c', pen='black', fill='black', intensity=0.20)

# Save the figure

fig.savefig(f"../data/hurricane@({lat},{lon})&{radius_max/1000}.png")

# Calculate the total valuation
total_valuation = intersections_64["County_Valuation"].sum()

# Filter the coastal counties from max
coastal_intersections = intersections_max[intersections_max["COASTAL"] == "Y"]

# Remove coastal counties from max
intersections_max = intersections_max[intersections_max["COASTAL"] == "N"]

print(coastal_intersections)
print(intersections_max)
print(only_intersections_64)

# Calculate the total damage based on radius of 64 and max
damage_coast_max = coastal_intersections["County_Valuation"].sum() * 0.020  # 2.0%
damage_max = intersections_max["County_Valuation"].sum() * 0.015 # 1.5%
damage_64 = only_intersections_64["County_Valuation"].sum() * 0.010 # 1.0%
print("damage_coast_max", '${:,.2f}'.format(damage_coast_max))
print("damage_max", '${:,.2f}'.format(damage_max))
print("damage_64", '${:,.2f}'.format(damage_64))
total_damage = damage_coast_max + damage_max + damage_64
print(f"Total County Valuation: {'${:,.2f}'.format(total_valuation)}")
print(f"Total Damage: {'${:,.2f}'.format(total_damage)}")