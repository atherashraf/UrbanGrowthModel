import numpy as np
from typing import Union

import rasterio
from rasterio import DatasetReader, MemoryFile


# from rasterio.session import AWSSession


class RioRaster:
    # src: str
    dataset: DatasetReader = None
    data: np.ndarray = None

    def __init__(self, src: Union[str, DatasetReader], no_data_value=None):
        self.set_dataset(src)
        if no_data_value:
            self.set_no_data(no_data_value)

    def set_dataset(self, src: Union[str, DatasetReader]):
        if isinstance(src, DatasetReader):
            self.dataset = src
        elif isinstance(src, str):
            # if "s3://" in src:
            #     self.dataset = S3Utils().get_rio_dataset(src)
            # # elif "/vsimem/" in src:
            # #     with MemoryFile(src) as memfile:
            # #         self.dataset = memfile.open()
            # else:
            self.dataset = rasterio.open(src)

    def get_dataset(self) -> DatasetReader:
        return self.dataset

    def set_no_data(self, no_data_value):
        self.data = self.get_data_array().astype('float')
        self.data[self.data == no_data_value] = np.nan

    def save_to_file(self, img_des: str):
        def create_new_raster():
            arr = self.get_data_array()
            with rasterio.open(img_des, 'w',
                               driver='GTiff',
                               height=arr.shape[0],
                               width=arr.shape[1],
                               count=1,
                               dtype=str(arr.dtype),
                               crs=self.dataset.crs,
                               transform=self.dataset.transform) as dataset:
                dataset.write(arr, 1)
                # dataset.close()

        if "s3://" in img_des:
            session = None  # rasterio.Env(AWSSession(S3Utils().get_session()))
            with session:
                create_new_raster()

        else:
            create_new_raster()

    def get_data_array(self) -> np.ndarray:
        if self.data is None:
            self.data = self.dataset.read(1)
        return self.data

    def get_raster_extent(self):
        bounds = self.dataset.bounds
        return [bounds.left, bounds.bottom, bounds.right, bounds.top]

    def get_spatial_resolution(self):
        return self.dataset.res

    def get_image_resolution(self):
        return self.dataset.height, self.dataset.width

    def make_conincident(self, raster2):
        pass

    def raster_from_array(self, arr: np.ndarray) -> 'RioRaster':
        memfile = MemoryFile()
        count = 1 if len(arr.shape) == 2 else arr.shape[2]
        with memfile.open(driver='GTiff',
                          height=arr.shape[0],
                          width=arr.shape[1],
                          count=count,
                          dtype=str(arr.dtype),
                          crs=self.dataset.crs,
                          transform=self.dataset.transform
                          ) as dataset:
            dataset.write(arr, indexes=count)

        dataset = memfile.open()  # Reopen as DatasetReader
        return RioRaster(dataset)
