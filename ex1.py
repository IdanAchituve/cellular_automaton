import numpy as np
import matplotlib


# automaton class
class cellular_automaton:

    def __init__(self, rule):
        self.rule = rule.copy()
        self.mat = np.array([[0, 1, 0]])  # an matrix of all generations so far

    def calc_next_gen(self):

        nrows, ncols = self.mat.shape  # get number of rows and cols
        curr_gen = self.mat[nrows-1, :].copy()  # get current generation
        curr_gen = np.pad(curr_gen, (1, 1), 'constant', constant_values=0)  # add 0 on both sides of the array

        # compute the sum of all triplets in the vector and get the matching cell value from the rule's vector
        for idx in range(ncols):
            summed_vals = curr_gen[nrows - 1, idx - 1] + curr_gen[nrows - 1, idx] + curr_gen[nrows - 1, idx + 1]
            cell_val = np.array(self.rule[summed_vals])
            next_gen = cell_val if idx == 0 else np.append([next_gen, cell_val])

        new_mat = np.pad(self.mat.copy(), (1, 1), 'constant', constant_values=0)[1:-1]  # add 0 padding to each row of the previous matrix
        new_mat = np.concatenate([new_mat, next_gen],0)  # add the new generation to the generation matrix
        self.mat = new_mat




if __name__ == '__main__':

    a = [[1, 2], [3, 4]]
    curr_gen = np.pad(a, (1, 1), 'constant', constant_values=0)[1:-1]
    print(curr_gen)

# rule - length 7 vector. first position correspond to sum 0, last position correspond to sum 6