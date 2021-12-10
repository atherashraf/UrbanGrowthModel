from app.utils.markov_chain import MarkovChain


class CellularAutomata:
    mc: MarkovChain

    def __init__(self, mc: MarkovChain):
        self.mc = mc


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
