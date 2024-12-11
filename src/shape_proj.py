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
parser.add_argument("--radius", type=int, default=120000, help="Radius of the circle in meters")
args = parser.parse_args()

lon, lat = args.lon, args.lat 
radius = args.radius

print(f"Longitude: {lon}, Latitude: {lat}, Radius: {radius}")

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
buffer = point_transformed.buffer(radius)
# Get the polygon with lat lon coordinates
circle_poly = transform(aeqd_to_wgs84, buffer)


# Read the csv files
county_bounds = pd.read_csv("../data/cleaned_data/county_bounds.csv")

# Convert the geometry column to a GeoSeries
county_bounds['geometry'] = gpd.GeoSeries.from_wkt(county_bounds['geometry'])

# Find the counties that overlap with the circle
county_bounds["intersects"] = county_bounds["geometry"].apply(
    lambda x: circle_poly.intersects(x) if type(x) != geometry.multipolygon.MultiPolygon else any(
        circle_poly.intersects(poly) for poly in x.geoms
    )
)

# Filter the counties that overlap with the circle
intersections = county_bounds[county_bounds["intersects"] == True]

# Create a GMT figure
fig = pygmt.Figure()
region = [-87.9, -79, 24, 31.2]
fig.basemap(region=region, projection="M4i", frame=True)
fig.coast( 
    water='skyblue', 
    shorelines=True)

# If the county is a multipolygon, draw the polygons individually
def draw_multipolygon(fig, multipolygon, draw=True):
    for polygon in list(multipolygon.geoms):
        if type(polygon) == geometry.multipolygon.MultiPolygon:
            draw_multipolygon(fig, polygon)
            return
        if draw:
            x, y = polygon.exterior.xy
            fig.plot(x=x, y=y, pen="black")
        else:
            x, y = polygon.exterior.xy
            fig.plot(x=x, y=y, fill="red", intensity=0.10)

# Highlight the counties that intersect with the circle
for county in intersections['geometry']:
    if type(county) == geometry.multipolygon.MultiPolygon:
        draw_multipolygon(fig, county, draw=False)
        continue
    x, y = county.exterior.xy
    fig.plot(x=x, y=y, fill="red", intensity=0.10)

# Draw the county boundaries
for county in county_bounds['geometry']:
    if type(county) == geometry.multipolygon.MultiPolygon:
        draw_multipolygon(fig, county)
        continue
    x, y = county.exterior.xy
    fig.plot(x=x, y=y, pen="black")

# Draw the circle
circle_poly_simple = circle_poly.simplify(0.01)
fig.plot(x=circle_poly_simple.exterior.xy[0], y=circle_poly_simple.exterior.xy[1], pen="2p,green", intensity=0.10)

# Draw the center of the circle
fig.plot(x=[lon], y=[lat], style='c0.1c', pen='green', fill='green', intensity=0.10)

# Save the figure

fig.savefig(f"../data/hurricane@{lat}&{lon}&{radius}.png")

# Calculate the total valuation
total_valuation = intersections["County_Valuation"].sum()
print(f"Total County Valuation: {'${:,.2f}'.format(total_valuation)}")