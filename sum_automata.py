import numpy as np
from part1 import AUTOMATON_LEN
import part2

NUM_CELLS = 40  # number of cells from both sides of the middle to take for the entropy check


# sum automaton class
class sum_automata:

    def __init__(self, rule):
        self.rule = rule.copy()
        self.mat = np.array([[1]])  # a matrix for saving all generations. Start with single 1 in the middle cell at generation 0.

    def calc_next_gen(self):

        new_mat = np.pad(self.mat.copy(), (1, 1), 'constant', constant_values=0)[1:-1]  # add 0 padding on both sides to all previous generations
        _, ncols = new_mat.shape  # get number of rows and cols
        curr_gen_temp = np.pad(new_mat[-1, :].copy(), (1, 1), 'constant', constant_values=0)  # add 0 padding for ease of computation
        freq_table = [0] * AUTOMATON_LEN  # save number of times each sum value was found
        middle_cell_index = int(ncols/2)
        left_cells = middle_cell_index - NUM_CELLS  # indices to take from the left
        right_cells = middle_cell_index + NUM_CELLS  # indices to take from the right

        # compute the sum of all triplets in the vector and get the matching cell value from the rule's vector
        for idx in range(1, ncols+1):
            summed_vals = curr_gen_temp[idx - 1] + curr_gen_temp[idx] + curr_gen_temp[idx + 1]
            cell_val = np.array(self.rule[AUTOMATON_LEN - summed_vals - 1]).reshape(1, 1)  # get cell value based on the summation of the above 3 cells
            next_gen = cell_val if idx == 1 else np.concatenate((next_gen, cell_val), 1)
            if middle_cell_index >= part2.ENTROPY_CHECK and left_cells <= idx - 1 <= right_cells:
                freq_table[summed_vals] += 1

        # add the new generation to the generation matrix
        new_mat = np.concatenate((new_mat, next_gen), 0)
        self.mat = new_mat
        return freq_table, next_gen
