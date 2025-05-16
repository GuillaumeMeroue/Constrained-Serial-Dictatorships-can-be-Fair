# Can we have the greedy algorithm to optimize the leximin instead of the min ?


import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


import numpy as np
from bruteforce import bruteforce_expected_optimal_policy, bruteforce_expected_optimal_policy_leximin
from sample_IC import sample_k_IC_profiles


k = 100

def bruteforce_naive_equal_leximin():
    for n in range(1,50):
        for m in range(n,100):
            set_of_profiles = sample_k_IC_profiles(k,n,m)
            x = bruteforce_expected_optimal_policy(set_of_profiles, "Borda", "egalitarian")
            y = bruteforce_expected_optimal_policy_leximin(set_of_profiles, "Borda", "egalitarian")
            print(x,y)
            assert(np.array_equal(x[2], y[2]))





from greedy_esw import construct_expected_esw_optimal_leximin_policy, construct_expected_esw_optimal_policy
from bruteforce import bruteforce_expected_optimal_policy_leximin


def test_expected_bruteforce_equal_leximin_esw(k=30):
    """
    Test if leximin bruteforce and esw have differents expected social welfares and sequence given a set of profiles.
    """
    for n in range(1,10):
        for m in range(n,15):
            set_of_profiles = sample_k_IC_profiles(k, n, m)
            brute_force_sw = bruteforce_expected_optimal_policy_leximin(set_of_profiles, "Borda", "egalitarian")
            esw = construct_expected_esw_optimal_policy(set_of_profiles, "Borda")
            print(n, m, esw, brute_force_sw)
            assert(brute_force_sw[1] == esw[1])
            assert(brute_force_sw[0] == tuple(esw[0]))



test_expected_bruteforce_equal_leximin_esw()



def test_expected_naive_equal_leximin_esw(k=300):
    """
    Test if leximin and naive esw have differents expected social welfares and sequence given a set of profiles.
    """
    for n in range(3,100):
        for m in range(n+1,100):
            set_of_profiles = sample_k_IC_profiles(k, n, m)
            naive = construct_expected_esw_optimal_policy(set_of_profiles, "Lexicographic")
            leximin = construct_expected_esw_optimal_leximin_policy(set_of_profiles, "Lexicographic")
            print(n, m, leximin, naive)
            assert(naive[1] == leximin[1])
            assert(tuple(naive[0]) == tuple(leximin[0]))



# test_expected_naive_equal_leximin_esw()