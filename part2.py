import numpy as np
from itertools import *
import sum_automata
import part1

START_GENERATION = 30  # initial generation for checking behaviour
END_GENERATION = 100  # number of generations to run the automaton before reaching a decision
ENTROPY_MEDIUM_THRESHOLD = 0.64
ENTROPY_HIGH_THRESHOLD = 1.15
STD_MEDIUM_THRESHOLD = 0.07
STD_HIGH_THRESHOLD = 0.22
EPSILON = 0.000001


# calculate the entropy: sigma_over_i(p_i*log(p_i))
def calc_entropy(dist):
    dist_cor = dist.copy() + EPSILON  # add epslion to prevent undefined log
    n = np.sum(dist_cor)
    probs = dist_cor/n
    log_probs = np.log(probs)
    return -np.sum(np.dot(probs, log_probs))


# calculate stats based on entropy of the automaton
def entropy_based_stats():
    # generate all rules
    all_rules = list(map(list, product([0, 1, 2], repeat=part1.AUTOMATON_LEN)))
    powers = [pow(part1.NUM_STATES, x) for x in range(part1.AUTOMATON_LEN - 1, -1, -1)]  # get base 3 powers
    simple_struc = simple_complex_struc = complex_struc = chaotic_struc = 0

    # calculate max entropy
    uniform_dist = [1/part1.AUTOMATON_LEN] * part1.AUTOMATON_LEN
    max_entropy = calc_entropy(np.asarray(uniform_dist))

    for rule in all_rules:
        automaton = sum_automata.sum_automata(np.asarray(rule))
        rule_id = np.dot(np.asarray(rule), np.asarray(powers))  # calculate rule id
        entropy_table = []

        for generation in range(END_GENERATION):
            freq_table = automaton.calc_next_gen()  # calculate the next generation and get frequency of each sum value
            if generation >= START_GENERATION:
                entropy_table.append(calc_entropy(np.asarray(freq_table)))

        if rule_id == 357:
            xx = 1

        if rule_id == 789:
            xx = 1

        if rule_id == 1111:
            xx = 1

        if rule_id == 1292:
            xx = 1

        if rule_id == 1664:
            xx = 1

        mean_entropy = np.mean(np.asarray(entropy_table))
        std = np.std((np.asarray(entropy_table)))

        # low entropy: simple structure
        if mean_entropy < ENTROPY_MEDIUM_THRESHOLD:
            simple_struc += 1
        # medium entropy: simple or simple-complex
        elif mean_entropy < ENTROPY_HIGH_THRESHOLD:
            # if std is medium or low -> simple-complex
            if std < STD_HIGH_THRESHOLD:
                simple_complex_struc += 1
            # if std is high -> complex
            else:
                complex_struc += 1
        # high entropy: simple-complex or chaotic
        else:
            # if std is low -> simple-complex
            if std < STD_MEDIUM_THRESHOLD:
                simple_complex_struc += 1
            # if std is medium -> chaotic
            elif std < STD_HIGH_THRESHOLD:
                chaotic_struc += 1
            # if std is high -> complex
            else:
                complex_struc += 1

    print("Simple Structure: " + str(simple_struc))
    print("Simple-Complex Structure: " + str(simple_complex_struc))
    print("Complex Structure: " + str(complex_struc))
    print("Chaotic Structure: " + str(chaotic_struc))
