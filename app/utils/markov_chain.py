import pandas as pd
import numpy as np
from app.utils.rio_raster import RioRaster


class MarkovChain:
    raster1: RioRaster
    raster2: RioRaster
    diff_in_years: int
    trans_area: pd.DataFrame
    trans_prob: pd.DataFrame

    def __init__(self, raster1: RioRaster, raster2: RioRaster, diff_in_years):
        self.raster1 = raster1
        self.raster2 = raster2
        self.diff_in_years = diff_in_years

    def cross_tabulation(self) -> pd.DataFrame:
        array1 = self.raster1.get_data_array().flatten()
        array2 = self.raster2.get_data_array().flatten()
        self.trans_area = pd.crosstab(array1, array2)
        print("transition area", self.trans_area)

    def calculate_trans_probability(self):
        if self.trans_area.empty:
            self.cross_tabulation()
        # axis = 1 is for row axis = 0 is for col np.sum(self.trans_area, axis=1)
        self.trans_prob = self.trans_area / np.sum(self.trans_area, axis=1)
        print(self.trans_prob)
