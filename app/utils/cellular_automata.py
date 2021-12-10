import array
import math
import os
import random
import traceback
from copy import deepcopy

from app.local_settings import OUTPUT_PATH
from app.utils.markov_chain import MarkovChain
import matplotlib.pyplot as plt
import numpy as np

from app.utils.rio_raster import RioRaster


class CellularAutomata:
    raster: RioRaster
    v_raster: RioRaster
    mc: MarkovChain
    neighborhood: np.array
    predicted: np.array
    kernel_size: int
    can_predict: bool

    def __init__(self, raster: RioRaster, v_raster: RioRaster, mc: MarkovChain = None):
        self.mc = mc
        self.raster = raster
        self.v_raster = v_raster
        self.kernel_size = 3
        self.focused_index = ((self.kernel_size + 1) / 2) - 1
        self.can_predict = False
        self.class_val = {"water": 1,
                          "builtup": 2,
                          "veg": 3,
                          "barren": 4}
        if self.kernel_size % 2 == 1:
            self.can_predict = True
            self.error_message = "Kernel size must have odd value "

    def create_neibourhood(self):
        neighborhood = []
        for i in range(0, 13):
            neighborhood.append([])
            for j in range(-6, 7):
                euc = np.sqrt((i - 6) ** 2 + (j) ** 2)
                if (euc > 6):
                    neighborhood[i].append(7)
                else:
                    neighborhood[i].append(euc)
        self.neighborhood = np.array(neighborhood)
        print(self.neighborhood)
        # fig = plt.figure(figsize=(8, 6))
        # plt.gray()
        # this = plt.pcolormesh(self.neighborhood)
        # plt.xticks(np.arange(0, 14, 1.0))
        # plt.yticks(np.arange(0, 14, 1.0))
        # plt.colorbar(this)
        # fig.savefig(os.path.join(OUTPUT_PATH, 'neighborhood.png'))
        # plt.show()

    # s is the stochastic disturbance term
    def S(self, a1):
        rand = random.uniform(0, 1)
        return 1 + (-np.log(rand)) ** a1

    # weighting function

    # param is the array of parameters (a,b,c,d)
    # euc is the euclidean distance to cell
    def get_m(self, euc, param=[]):
        if param == ['different']:
            return -2 * (np.exp(-2 * 0.8 * (euc - 2.2)) - 2 * np.exp(-.8 * (euc - 2.2)))
        exp = np.exp(-(euc - param[2]) / param[1])
        return param[0] * (exp / (1 + exp)) + param[3]

    # def get_p(self, x, y, trans_type, grid=[]):
    #     msum = 0
    #     for j in range(0, 13):
    #         for i in range(0, 13):
    #             dist = get_dist(i - 6, j - 6)
    #             # since i and j are relative to the position of the cell, i and
    #             # j's actual positions are given by the following:
    #             real_i = int(x + i - 6)
    #             real_j = int(y + j - 6)
    #             # Check if neighboring cells are in range of the grid
    #             if (real_i >= 0 and real_i < size and real_j >= 0 and real_j < size):
    #                 # check if cells are in the neihborhood zone
    #                 if (dist <= 6):
    #                     # check if cells are not vacant type:
    #                     cell_type = get_type(real_i, real_j, grid)
    #                     if (cell_type < 3):
    #                         msum += self.get_m(dist, m_params[trans_type * 3 + cell_type])
    #
    #     return self.S(a) * (.25 + msum)

    def fit_model(self):
        try:
            if self.can_predict:
                m, n = self.data.shape
                margin = math.ceil(self.kernel_size / 2)
                data = np.array(self.raster.get_data_array())
                self.predicted = deepcopy(data)
                for y in range(margin, m - (margin - 1)):
                    for x in range(margin, n - (margin - 1)):
                        kernel = data[y - (margin - 1):y + margin, x - (margin - 1):x + (margin)]
                        predicted_val = self.get_predicted_value(kernel)
                        self.predicted[y, x] = predicted_val
            else:
                print("error:", self.error_msg)
        except Exception as e:
            traceback.print_exc()

    def get_predicted_value(self, kernel):
        focused_value = kernel[self.focused_index][self.focused_index]
        if focused_value == self.class_val["water"]:
            return focused_value
        elif focused_value == self.class_val["builtup"]:
            return focused_value
        else:
            builtup_count = sum(sum(kernel == self.class_val["builtup"]))
            if builtup_count >= math.ceil((self.kernel_size * self.kernel_size) / 2):
                return self.class_val["builtup"]

    def builtup_area_difference(self, landcover1, landcover2, buclass=1, cellsize=30):
        return (sum(sum(((landcover2 == buclass).astype(int) - (landcover1 == buclass).astype(int)) != 0)) * (
                cellsize ** 2) / 1000000)

    def check_accuracy(self):
        # Statistical Accuracy
        actual_builtup = self.builtup_area_difference(self.raster.get_data_array(),
                                                      self.v_raster.get_data_array())
        predicted_builtup = self.builtup_area_difference(self.raster.get_data_array(), self.predicted)
        spatial_accuracy = 100 - (sum(
            sum(((self.predicted == self.class_val["builtup"]).astype(float) - (
                    self.v_raster.get_data_array() == self.class_val["builtup"]).astype(
                float)) != 0)) / sum(
            sum(self.v_raster.get_data_array() == self.class_val["builtup"]))) * 100
        print(f"Actual growth: {actual_builtup}, Predicted growth: {predicted_builtup}")
        # Spatial Accuracy
        print(f"Spatial accuracy: {spatial_accuracy}")
        return spatial_accuracy

    def export_predicted(self, output_filename="predicted_image.tif"):
        export_data = self.mc.raster1.raster_from_array(self.predicted)
        des_path = os.path.join(OUTPUT_PATH, output_filename)
        export_data.save_to_file(des_path)

# def cellular_automaton(rule_number, size, steps,
#                        init_cond='random', impulse_pos='center'):
#     """Generate the state of an elementary cellular automaton after a pre-determined
#     number of steps starting from some random state.
#     Args:
#         rule_number (int): the number of the update rule to use
#         size (int): number of cells in the row
#         steps (int): number of steps to evolve the automaton
#         init_cond (str): either `random` or `impulse`. If `random` every cell
#         in the row is activated with prob. 0.5. If `impulse` only one cell
#         is activated.
#         impulse_pos (str): if `init_cond` is `impulse`, activate the
#         left-most, central or right-most cell.
#     Returns:
#         np.array: final state of the automaton
#     """
#     assert 0 <= rule_number <= 255
#     assert init_cond in ['random', 'impulse']
#     assert impulse_pos in ['left', 'center', 'right']
#
#     rule_binary_str = np.binary_repr(rule_number, width=8)
#     rule_binary = np.array([int(ch) for ch in rule_binary_str], dtype=np.int8)
#     x = np.zeros((steps, size), dtype=np.int8)
#
#     if init_cond == 'random':  # random init of the first step
#         x[0, :] = np.array(np.random.rand(size) < 0.5, dtype=np.int8)
#
#     if init_cond == 'impulse':  # starting with an initial impulse
#         if impulse_pos == 'left':
#             x[0, 0] = 1
#         elif impulse_pos == 'right':
#             x[0, size - 1] = 1
#         else:
#             x[0, size // 2] = 1
#
#     for i in range(steps - 1):
#         x[i + 1, :] = step(x[i, :], rule_binary)
#
#     return x
