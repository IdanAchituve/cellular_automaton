import numpy as np
from itertools import *
import sum_automata
import part1

ENTROPY_CHECK = 40  # initial generation for checking the entropy
END_GENERATION = 200  # number of generations to run each automaton
ENTROPY_MEDIUM_THRESHOLD = 0.25
ENTROPY_HIGH_THRESHOLD = 1.0
STD_THRESHOLD = 0.058
EPSILON = 0.000001
WINDOW_SIZE = 10  # fixed window size from each side of the middle cell
WINDOW_CHECK = 40  # initial generation for checking repetitions inside the window
REPETITION_THRESHOLD = 2.6


# calculate the entropy: -sigma_over_i(p_i*log(p_i))
def calc_entropy(dist):
    dist_cor = dist.copy() + EPSILON  # add epsilon to prevent undefined log
    n = np.sum(dist_cor)
    probs = dist_cor/n
    log_probs = np.log(probs)
    return -np.sum(np.dot(probs, log_probs))


# calculate stats based on entropy of the automaton
def build_stats():
    # generate all rules
    all_rules = list(map(list, product([0, 1, 2], repeat=part1.AUTOMATON_LEN)))
    simple_struc = complex_struc = chaotic_struc = 0

    for idx, rule in enumerate(all_rules):
        automaton = sum_automata.sum_automata(np.asarray(rule))
        entropy_table = []  # save entropy of each generation
        repetitions = {}  # save the number of repetitions of each occurrence

        for generation in range(END_GENERATION):
            freq_table, last_gen = automaton.calc_next_gen()  # calculate the next generation and get frequency of each sum value
            last_gen = last_gen.squeeze()

            # 1st metric: entropy
            if generation >= ENTROPY_CHECK:
                entropy_table.append(calc_entropy(np.asarray(freq_table)))

            # 2nd metric: window check
            if generation > WINDOW_CHECK:
                num_cells = int(len(last_gen) / 2)  # find middle cell
                window = last_gen[num_cells - WINDOW_SIZE:num_cells + WINDOW_SIZE]  # take middle window of cells
                window = tuple(window.tolist())
                repetitions[window] = repetitions[window] + 1 if window in repetitions else 1

        mean_entropy = np.mean(np.asarray(entropy_table))  # get mean entropy
        std = np.std((np.asarray(entropy_table)))  # get std of entropy
        avg_repetitions = np.mean(list(repetitions.values()))  # get the average number of repetitions

        # low entropy or low variance: simple structure
        if mean_entropy <= ENTROPY_MEDIUM_THRESHOLD or std < STD_THRESHOLD:
            simple_struc += 1
        # medium entropy: complex
        elif mean_entropy <= ENTROPY_HIGH_THRESHOLD:
            complex_struc += 1
        # high entropy: complex or chaotic
        else:
            # high number of recitations on average -> complex
            if avg_repetitions >= REPETITION_THRESHOLD:
                complex_struc += 1
            # low number of recitations on average -> chaotic
            else:
                chaotic_struc += 1

        # print progress bar
        if idx % 100 == 0:
            print(".", end="", flush=True)

    print("\n#Automatons that have simple structure: " + str(simple_struc))
    print("#Automatons that have complex structure: " + str(complex_struc))
    print("#Automatons that have chaotic structure: " + str(chaotic_struc))
