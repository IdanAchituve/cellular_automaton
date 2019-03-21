import numpy as np
from itertools import *
import sum_automata
from part1 import AUTOMATON_LEN, NUM_STATES

START_GENERATION = 10  # initial generation for checking behaviour
END_GENERATION = 60  # number of generations to run the automaton before reaching a decision

# calculate the entropy: sigma_over_i(p_i*log(p_i))
def calc_entropy(dist):
    n = np.sum(dist)
    probs = dist/n
    log_probs = np.log(probs)
    return np.sum(np.dot(probs,log_probs))


def entropy_based_stats():
    # generate all rules
    all_rules = list(map(list, product([0, 1, 2], repeat=AUTOMATON_LEN)))
    powers = [pow(NUM_STATES, x) for x in range(AUTOMATON_LEN - 1, -1, -1)]  # get base 3 powers
    simple_struc = complex_struc = chaotic_struc = 0

    for rule in all_rules:
        automaton = sum_automata.sum_automata(np.asarray(rule))
        rule_id = np.dot(np.asarray(rule), np.asarray(powers))  # calculate rule id
        entropy_table = []

        for generation in range(END_GENERATION):
            freq_table = automaton.calc_next_gen()  # calculate the next generation and get frequency of each sum value
            if generation >= START_GENERATION:
                entropy_table.append(np.asarray(freq_table))

        mean_entropy = np.mean(np.asarray(entropy_table))
        if mean_entropy < 0.5:
            simple_struc += 1
        elif mean_entropy < 0.9:
            complex_struc += 1
        else:
            chaotic_struc += 1

        print("Simple Structure: " + str(simple_struc))
        print("Complex Structure: " + str(complex_struc))
        print("Chaotic Structure: " + str(chaotic_struc))
