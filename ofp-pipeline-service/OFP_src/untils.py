from typing import Dict, Tuple, List

from osgeo import gdal, gdal_array

import numpy as np


def most_value_at_zero_gradient(band: np.ndarray, frame: bool = False) -> int:

    if frame:
        gradient_x: np.ndarray = np.gradient(band)
    else:
        gradient_x: np.ndarray = np.gradient(band, axis=1)

    zero_gradient_indices: np.ndarray = np.where(gradient_x == 0)
    values_at_zero_gradient: np.ndarray = band[zero_gradient_indices]

    most_common_value: int = np.argmax(np.bincount(values_at_zero_gradient))

    return most_common_value


def calculation_artificial_pixel_value(band: np.ndarray,
                                       window_size: int = 256) -> int:

    upper_left: np.ndarray = band[:window_size, :window_size]
    upper_right: np.ndarray = band[:window_size, -window_size:]
    lower_left: np.ndarray = band[-window_size:, :window_size]
    lower_right: np.ndarray = band[-window_size:, -window_size:]

    corner_values: List = [most_value_at_zero_gradient(window) for window in
                           (upper_left, upper_right, lower_left, lower_right)]

    most_common_value = np.argmax(np.bincount(corner_values))

    return most_common_value


def get_artificial_pixel_in_rgb(dataset: gdal.Dataset) -> np.ndarray:
    num_channels: int = dataset.RasterCount
    values: np.ndarray = np.zeros((num_channels), dtype=np.uint8)

    for i in range(1, num_channels + 1):
        band = dataset.GetRasterBand(i).ReadAsArray()
        pixel_value = calculation_artificial_pixel_value(band)
        values[i - 1] = pixel_value

    return values


def remove_artificial_pixels_in_OFP(input_file: str, window_size: int = 1024, 
                                    *args: Tuple, **kwargs: Dict) -> None:
    dataset: gdal.Dataset = gdal.Open(input_file, gdal.GA_Update)

    width: int = dataset.RasterXSize
    height: int = dataset.RasterYSize
    driver = gdal.GetDriverByName("GTiff")

    num_channels: int = dataset.RasterCount + 1

    new_dataset = driver.Create(input_file, width, height,
                                num_channels, gdal.GDT_Byte)

    for channel in range(1, num_channels):
        band = dataset.GetRasterBand(channel)
        new_dataset.GetRasterBand(channel).WriteArray(band.ReadAsArray())

    alpha_band: np.ndarray = np.ones((height, width), dtype=np.uint8) * 255
    artificial_pixel: np.ndarray = get_artificial_pixel_in_rgb(dataset)

    for i in range(0, height, window_size):
        for j in range(0, width, window_size):

            if i + window_size <= height and j + window_size <= width:
                window_r: np.ndarray = dataset.GetRasterBand(1).ReadAsArray(j, i, window_size, window_size)
                window_g: np.ndarray = dataset.GetRasterBand(2).ReadAsArray(j, i, window_size, window_size)
                window_b: np.ndarray = dataset.GetRasterBand(3).ReadAsArray(j, i, window_size, window_size)
            else:
                remaining_height = min(window_size, height - i)
                remaining_width = min(window_size, width - j)

                window_r = dataset.GetRasterBand(1).ReadAsArray(j, i, remaining_width, remaining_height)
                window_g = dataset.GetRasterBand(2).ReadAsArray(j, i, remaining_width, remaining_height)
                window_b = dataset.GetRasterBand(3).ReadAsArray(j, i, remaining_width, remaining_height)

            mask: Tuple = (
                    (window_r == artificial_pixel[0]) &
                    (window_g == artificial_pixel[1]) &
                    (window_b == artificial_pixel[2])
                )

            alpha_band[i:i+window_size, j:j+window_size][mask] = 0

    new_dataset.GetRasterBand(num_channels).WriteArray(alpha_band)
    new_dataset.SetProjection(dataset.GetProjection())
    new_dataset.SetGeoTransform(dataset.GetGeoTransform())

    dataset = None
    new_dataset = None