import numpy as np
import matplotlib.pyplot as plt
from itertools import *
import time
import os

NUM_ITERS = 100
NUM_COLS = 201
MAX_COLOR = 255.0
AUTOMATON_LEN = 7
NUM_STATES = 3

# automaton class
class cellular_automaton:

    def __init__(self, rule):
        self.rule = rule.copy()
        self.mat = np.pad(np.array([1]), (int(NUM_COLS/2), int(NUM_COLS/2)), 'constant', constant_values=0)  # a matrix of all generations so far
        self.mat = self.mat.reshape(1, -1)

    def calc_next_gen(self):

        nrows, ncols = self.mat.shape  # get number of rows and cols
        curr_gen = self.mat[nrows-1, :].copy()  # get current generation
        curr_gen = np.pad(curr_gen, (1, 1), 'wrap')  # pad the beginning with the final number and the end with the first number

        # compute the sum of all triplets in the vector and get the matching cell value from the rule's vector
        for idx in range(1, ncols+1):
            summed_vals = curr_gen[idx - 1] + curr_gen[idx] + curr_gen[idx + 1]
            cell_val = np.array(self.rule[summed_vals]).reshape(1, 1)
            next_gen = cell_val if idx == 1 else np.concatenate((next_gen, cell_val), 1)

        new_mat = np.concatenate((self.mat.copy(), next_gen), 0)  # add the new generation to the generation matrix
        self.mat = new_mat


# animate images
def animate(mat_f, gap=0.5):

    plt.gray()  # print image in grayscale values
    plt.axis('off')  # don't print axis ticks

    # set location on screen
    mngr = plt.get_current_fig_manager()
    mngr.window.setGeometry(500, 200, 640, 545)

    plt.imshow(mat_f)  # convert matrix to image
    plt.show()  # show image
    plt.pause(gap)  # time delay


# build user requested automaton
def build_user_input_automaton(rule, rum_time):

    automaton = cellular_automaton(np.asarray(rule))
    start = time.time()  # number of seconds since unix epoch
    time.clock()  # start measuring time
    elapsed = 0

    plt.ion()

    while elapsed < rum_time:
        automaton.calc_next_gen()  # calculate the next generation
        elapsed = time.time() - start

        current_mat = automaton.mat.copy()  # get latest matrix
        mat_f = MAX_COLOR - current_mat * MAX_COLOR/2  # to float
        animate(mat_f)  # print all generations so far

        plt.close()


# build all 3^7 possible automaton
def build_all_automaton(save_img):

    # generate all rules
    all_rules = list(map(list, product([0, 1, 2], repeat=AUTOMATON_LEN)))
    plt.ion()
    powers = [pow(NUM_STATES, x) for x in range(AUTOMATON_LEN - 1, -1, -1)]  # get base 3 powers

    for rule in all_rules:
        automaton = cellular_automaton(np.asarray(rule))
        for generation in range(NUM_ITERS):
            automaton.calc_next_gen()  # calculate the next generation
        mat = automaton.mat.copy()  # get the final matrix
        mat_f = MAX_COLOR - mat * MAX_COLOR/2  # to float

        animate(mat_f, 0.001)

        # save image
        if save_img:
            rule_id = np.dot(np.asarray(rule), np.asarray(powers))  # calculate rule id
            if not os.path.exists("./images"):
                os.makedirs("./images")
            plt.savefig("./images/rule_" + str(rule_id) + ".png")
        plt.close()


def get_user_input():

    valid_input = False
    print("Hi,")
    print("Please make sure you are running Python 3.x and that you have matplotlib installed!\n")

    # get type of run preference
    while not valid_input:

        # get type of program
        run_selection = input("Please pick an option from the bellow. Enter:\n"
                              "0 - for creating all automatons\n"
                              "1 - for generating your custom made automaton\n"
                              "2 - for exiting\n\n")

        try:
            run_sel_val = int(run_selection)
        except ValueError:
            print("You entered an invalid value!")
            continue

        if run_sel_val in (0, 1):
            print("Perfect. You chose: ", run_selection)
            valid_input = True
        elif run_sel_val == 2:
            print("Bye Bye!")
            valid_input = True
        else:
            print("You didn't pick a valid option! Please choose a digit between 0 and 2")

    # running all automatons
    if run_sel_val == 0:
        save_img = False
        saving_selection = input("Do you want to save all automatons? Enter Y for yes and N for no:\n")
        if saving_selection == "Y":
            print("Automaton images will be saved under .\images")
            save_img = True
        build_all_automaton(save_img)

    # user defined automaton
    elif run_sel_val == 1:

        rule = []  # save user input
        for i in range(AUTOMATON_LEN):
            valid_input = False
            while not valid_input:

                state = input("Please enter a state value when the sum of the previous states is " + str(i) + ":\n")

                try:
                    state_val = int(state)
                except ValueError:
                    print("You entered an invalid state. Note that legal values are between 0 and 2")
                    continue

                if state_val not in [0, 1, 2]:
                    print("You entered an invalid state. Note that legal values are between 0 and 2")
                else:
                    valid_input = True
                    rule.append(state_val)

        valid_input = False
        while not valid_input:
            time_selection = input("Please enter a run time for the automaton in seconds:\n")
            try:
                run_time = float(time_selection)
                valid_input = True
            except ValueError:
                print("You entered an invalid value!")

        # run program
        build_user_input_automaton(rule, run_time)

    # exit program
    else:
        exit(0)


if __name__ == '__main__':

    get_user_input()