import numpy as np
from itertools import *
import sum_automata
import part1

START_GENERATION = 40  # initial generation for checking behaviour
END_GENERATION = 200  # number of generations to run the automaton before reaching a decision
ENTROPY_MEDIUM_THRESHOLD = 0.25
ENTROPY_HIGH_THRESHOLD = 1.0
STD_THRESHOLD = 0.052
EPSILON = 0.000001
WINDOW_SIZE = 10
WINDOW_CHECK = 40
WINDOW_GENERATION2 = 80
REPETITION_THRESHOLD = 2.6


# calculate the entropy: sigma_over_i(p_i*log(p_i))
def calc_entropy(dist):
    dist_cor = dist.copy() + EPSILON  # add epslion to prevent undefined log
    n = np.sum(dist_cor)
    probs = dist_cor/n
    log_probs = np.log(probs)
    return -np.sum(np.dot(probs, log_probs))


# calculate stats based on entropy of the automaton
def build_stats():
    # generate all rules
    all_rules = list(map(list, product([0, 1, 2], repeat=part1.AUTOMATON_LEN)))
    powers = [pow(part1.NUM_STATES, x) for x in range(part1.AUTOMATON_LEN - 1, -1, -1)]  # get base 3 powers
    simple_struc = complex_struc = chaotic_struc = 0

    # calculate max entropy
    uniform_dist = [1/part1.AUTOMATON_LEN] * part1.AUTOMATON_LEN
    max_entropy = calc_entropy(np.asarray(uniform_dist))

    for idx, rule in enumerate(all_rules):
        automaton = sum_automata.sum_automata(np.asarray(rule))
        rule_id = np.dot(np.asarray(rule), np.asarray(powers))  # calculate rule id
        entropy_table = []
        repetition1 = repetition2 = 0
        repetitions = {}

        for generation in range(END_GENERATION):
            freq_table, last_gen = automaton.calc_next_gen()  # calculate the next generation and get frequency of each sum value
            last_gen = last_gen.squeeze()

            # 1st metric: entropy
            if generation >= START_GENERATION:
                entropy_table.append(calc_entropy(np.asarray(freq_table)))

            if generation > WINDOW_CHECK:
                num_cells = int(len(last_gen) / 2)
                window = last_gen[num_cells - WINDOW_SIZE:num_cells + WINDOW_SIZE]
                window = tuple(window.tolist())
                repetitions[window] = repetitions[window] + 1 if window in repetitions else 1

            """
            # 2nd metric: take small window
            if generation == WINDOW_GENERATION1:
                num_cells = int(len(last_gen)/2)
                window1 = last_gen[num_cells-WINDOW_SIZE:num_cells+WINDOW_SIZE]
            if generation > WINDOW_GENERATION1:
                num_cells = int(len(last_gen)/2)
                if np.array_equal(window1, last_gen[num_cells-WINDOW_SIZE:num_cells+WINDOW_SIZE]):
                    repetition1 += 1

            # 3rd metric: take an additional small window
            if generation == WINDOW_GENERATION2:
                num_cells = int(len(last_gen)/2)
                window2 = last_gen[num_cells-WINDOW_SIZE:num_cells+WINDOW_SIZE]
            if generation > WINDOW_GENERATION2:
                num_cells = int(len(last_gen)/2)
                if np.array_equal(window2, last_gen[num_cells-WINDOW_SIZE:num_cells+WINDOW_SIZE]):
                    repetition2 += 1
            """
        mean_entropy = np.mean(np.asarray(entropy_table))
        std = np.std((np.asarray(entropy_table)))
        avg_repetitions = np.mean(list(repetitions.values()))

        #print(str(mean_entropy) + " " + str(std) + " " + str(repetition1) + " " + str(repetition2))
        #print(str(mean_entropy) + " " + str(std) + " " + str(np.mean(list(repetitions.values()))))

        # low entropy or low variance: simple structure
        if mean_entropy <= ENTROPY_MEDIUM_THRESHOLD or std < STD_THRESHOLD:
            simple_struc += 1
        # medium entropy: complex
        elif mean_entropy <= ENTROPY_HIGH_THRESHOLD:
            complex_struc += 1
        # high entropy: complex or chaotic
        else:
            # if std is low or there are repetitions in the vectors-> complex
            if avg_repetitions >= REPETITION_THRESHOLD:  #or repetition2 >= REPETITION_THRESHOLD:
                complex_struc += 1
            # if std is medium -> chaotic
            else:
                chaotic_struc += 1

        if idx % 100 == 0:
            print(".", end="", flush=True)

    print("\nSimple Structure: " + str(simple_struc))
    print("Complex Structure: " + str(complex_struc))
    print("Chaotic Structure: " + str(chaotic_struc))
