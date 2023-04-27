import pandas as pd
import rasterio
from pyproj import Transformer


df = pd.read_csv('level_location.csv',usecols = ['LAT','LON','VALUE_levelling'])
array_lat = [lat for lat in df["LAT"].values]
array_lon = [lat for lat in df["LON"].values]


fp = r'2021q2_202209_geo_velocity_cm_dz.tif'
img = rasterio.open(fp)
band = img.read()[0]

# convert lon,lat to x,y
transformer = Transformer.from_crs("EPSG:4326", img.crs, always_xy=True)
value = []
for i in range(len(array_lat)):
    x, y = transformer.transform(array_lon[i], array_lat[i])
    if x and y > 0:
        value.append(list(img.sample([(x, y)])))
    else:
        value.append('nan')

df['value_InSAR'] = value

# To save it back as csv
df.to_csv("./level_location.csv",index=False)


