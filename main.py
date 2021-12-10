# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os

from app.local_settings import MEDIA_PATH
from app.utils.cellular_automata import CellularAutomata
from app.utils.markov_chain import MarkovChain
from app.utils.rio_raster import RioRaster


def calculate_markov_chain():
    year1 = 2011
    year2 = 2016
    v_year = 2019
    r_path1 = os.path.join(MEDIA_PATH, 'data/2011/Reclass_c2011.tif')
    r_path2 = os.path.join(MEDIA_PATH, 'data/2016/Reclass_c2016.tif')
    r_path3 = os.path.join(MEDIA_PATH, 'data/2019/Reclass_c2019.tif')
    raster1 = RioRaster(r_path1, no_data_value=127)
    raster2 = RioRaster(r_path2, no_data_value=127)
    v_raster = RioRaster(r_path3, no_data_value=127)

    # raster1.make_conincident(raster2)

    # calculating transition probability matrix
    mc = MarkovChain(raster1, raster2, diff_in_years=(year2 - year1))
    mc.cross_tabulation()
    mc.calculate_trans_probability()

    # cellular automata
    ca = CellularAutomata(raster2, v_raster, mc)
    ca.create_neibourhood()
    ca.fit_model()


if __name__ == '__main__':
    calculate_markov_chain()
