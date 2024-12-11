import pandas as pd
import tabula
file = "data/county_median_price.pdf"
path = file
df_p1 = tabula.read_pdf(path, pages = '7', multiple_tables = False)
df_p2 = tabula.read_pdf(path, pages = '8', multiple_tables = False)
df_p1[0].to_csv("county_median_price_p1.csv", index = False)
df_p2[0].to_csv("county_median_price_p2.csv", index = False)