from osgeo import gdal
import numpy as np


def raster_value_average(filepath, bbox):
    ds_ori = gdal.Open(filepath)
    gdal.Translate(f'cut_{filepath}', ds_ori, projWin=bbox)
    ds = gdal.Open(f'cut_{filepath}')
    band = ds.GetRasterBand(1).ReadAsArray()
    size_of_band = np.array(band).size
    avg_val = np.sum(band) / size_of_band
    return avg_val


def main():
    # bbox = [upper_left_x,upper_left_y,lower_right_x,lower_right_y]
    bbox = [121.297765, 25.059719, 121.299732, 25.058262]
    ew_mean_velocity = raster_value_average(filepath='Velo_EW.tif', bbox=bbox)
    ud_mean_velocity = raster_value_average(filepath='Velo_UD.tif', bbox=bbox)
    print('EW_mean_velocity :'  f"{ew_mean_velocity}")
    print('UD_mean_velocity :'  f"{ud_mean_velocity}")


if __name__ == '__main__':
    main()
