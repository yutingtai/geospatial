#!/usr/bin/env python
# coding: utf-8

#  ### Import the libraries, read the satellite images and AOI shapefile

# In[2]:


import os
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import mapping
import rioxarray as rxr
import xarray as xr
import geopandas as gpd
from pyproj import CRS
import glob
import os
import numpy as np
from osgeo import gdal
import rasterio
from rasterio.plot import show, show_hist
import cv2

red_file = rxr.open_rasterio(
    "0703_R10m/T13UDR_20200703T175919_B04_10m.jp2", masked=True).squeeze()
nir_file = rxr.open_rasterio(
    "0703_R10m/T13UDR_20200703T175919_B08_10m.jp2", masked=True).squeeze()
a_red_file = rxr.open_rasterio(
    "0706_R10m/T13UDR_20200706T180919_B04_10m.jp2", masked=True).squeeze()
a_nir_file = rxr.open_rasterio(
    "0706_R10m/T13UDR_20200706T180919_B08_10m.jp2", masked=True).squeeze()

aoi = os.path.join("output/aoi.shp")
crop_aoi = gpd.read_file(aoi)


# ### Write the crs into the images and crop them with AOI shapefile

# In[4]:


red_file.rio.write_crs("EPSG:32613", inplace=True)
nir_file.rio.write_crs("EPSG:32613", inplace=True)
a_red_file.rio.write_crs("EPSG:32613", inplace=True)
a_nir_file.rio.write_crs("EPSG:32613", inplace=True)

red_file_clipped = red_file.rio.clip(
    crop_aoi.geometry.apply(mapping), crop_aoi.crs)
nir_file_clipped = nir_file.rio.clip(
    crop_aoi.geometry.apply(mapping), crop_aoi.crs)
a_red_file_clipped = a_red_file.rio.clip(
    crop_aoi.geometry.apply(mapping), crop_aoi.crs)
a_nir_file_clipped = a_nir_file.rio.clip(
    crop_aoi.geometry.apply(mapping), crop_aoi.crs)


# ### read the bands as array and convert to float for NDVI calculation

# In[5]:


red = red_file_clipped.astype(np.float).values
nir = nir_file_clipped.astype(np.float).values
a_red = a_red_file_clipped.astype(np.float).values
a_nir = a_nir_file_clipped.astype(np.float).values



def ndvi(red, nir):
    return ((nir - red)/(nir + red))


ndvi_03 = ndvi(red, nir)
ndvi_06 = ndvi(a_red, a_nir)


difference_ndvi = ndvi_03-ndvi_06


# In[7]:


y_pixels = ndvi_03.shape[0]  # number of pixels in y
x_pixels = ndvi_03.shape[1]  # number of pixels in x
a_y_pixels = ndvi_06.shape[0]  # number of pixels in y
a_x_pixels = ndvi_06.shape[1]  # number of pixels in x
d_y_pixels = difference_ndvi.shape[0]  # number of pixels in y
d_x_pixels = difference_ndvi.shape[1]  # number of pixels in x

# Set the output file as GeoTIFF
driver = gdal.GetDriverByName('GTiff')

# Create driver using  x and y pixels, # of bands, and datatype
ndvi_data = driver.Create('NDVI_03.tif', x_pixels,
                          y_pixels, 1, gdal.GDT_Float64)

a_ndvi_data = driver.Create('NDVI_06.tif', a_x_pixels,
                            a_y_pixels, 1, gdal.GDT_Float64)

difference_ndvi_data = driver.Create('NDVI_difference.tif', d_x_pixels,
                                     d_y_pixels, 1, gdal.GDT_Float64)

# Set NDVI array as the 1 output raster band
ndvi_data.GetRasterBand(1).WriteArray(ndvi_03)
a_ndvi_data.GetRasterBand(1).WriteArray(ndvi_06)
difference_ndvi_data.GetRasterBand(1).WriteArray(difference_ndvi)

# Setting up the coordinate reference system of the output file
red_geotransform = glob.glob(os.path.join("0703_R10m",  '*B04_10m.jp2'))
red_link = gdal.Open(red_geotransform[0])

# Grab input GeoTranform information
geotrans = red_link.GetGeoTransform()

# Grab projection information from input file
proj = red_link.GetProjection()

# now set GeoTransform parameters and projection on the output file
ndvi_data.SetGeoTransform(geotrans)
ndvi_data.SetProjection(proj)
ndvi_data.FlushCache()
ndvi_data = None
a_ndvi_data.SetGeoTransform(geotrans)
a_ndvi_data.SetProjection(proj)
a_ndvi_data.FlushCache()
a_ndvi_data = None

plt.imshow(ndvi_03, cmap="RdYlGn")
plt.colorbar(shrink=0.7)
plt.show()

plt.imshow(ndvi_06, cmap="RdYlGn")
plt.colorbar(shrink=0.7)
plt.show()

plt.imshow(difference_ndvi, cmap="Reds")
plt.colorbar(shrink=0.7)
plt.show()


# In[9]:


### define a function to calculate the pixel number
def pixel_number_above_threshold(matrix, threshold):
    all_pixel = matrix.shape[0] * matrix.shape[1]
    above_threshold_pixels = 0
    for x in np.nditer(matrix):
        if x > threshold:
            above_threshold_pixels = above_threshold_pixels + 1
    return above_threshold_pixels


### define a function that only preserves the difference part and apply morphological algorithm 
def get_demaged(matrix, threshold, morphology_enabled=False):
    def threshold_clamper(t): return 1.0 if t > threshold else 0.0
    clamp = np.vectorize(threshold_clamper)
    clamped = clamp(matrix)
    kernel = np.ones((4, 4), np.uint8)
    return cv2.dilate(
        cv2.erode(clamped, kernel, iterations=1),
        kernel,
        iterations=1
    ) if morphology_enabled else clamped


while True:
    user_threshold = input("Threshold:")
    if user_threshold == "q":
        break
    else:
        user_threshold = float(user_threshold)
        fig, ax = plt.subplots(1, 2, figsize=(12, 6))
        original = get_demaged(difference_ndvi, user_threshold, False)
        ax[1].imshow(original)
        ax[1].set_title('Original')
        eroded_and_dilated = get_demaged(difference_ndvi, user_threshold, True)
        ax[0].imshow(eroded_and_dilated)
        ax[0].set_title('Eroded and Dilated')
        plt.show()

        print("original numbers of pixels: ", pixel_number_above_threshold(
            original, user_threshold))
        print("Eroded numbers of pixels: ", pixel_number_above_threshold(
            eroded_and_dilated, user_threshold))

###############################################################################

