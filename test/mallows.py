import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


import matplotlib.pyplot as plt
from collections import Counter
import json

from sample_mallows import sample_k_mallows_profiles
from bruteforce import bruteforce_expected_optimal_policy


def test_bruteforce_mallows(n,m,k, dispersion, references):
    """
    Test if bruteforce and esw have differents expected social welfares given a set of profiles.
    """
    # for n in range(1,10):
    #     for m in range(n,15):
    set_of_profiles = sample_k_mallows_profiles(k, n, m, dispersion, references)
    brute_force_sw = bruteforce_expected_optimal_policy(set_of_profiles, "Borda", "egalitarian")
    return brute_force_sw


n = 5
m = 12
k = 1000
dispersion = 0.3
references = list(range(1,m+1))

# print(test_bruteforce_mallows(n,m,k, dispersion, references))

from greedy_esw import construct_expected_esw_optimal_policy


def test_esw_mallows(n,m,k, dispersion, references):
    """
    Test if bruteforce and esw have differents expected social welfares given a set of profiles.
    """
    # for n in range(1,10):
    #     for m in range(n,15):
    # values = reversed(list(range(m)))
    set_of_profiles = sample_k_mallows_profiles(k, n, m, dispersion, references)
    esw = construct_expected_esw_optimal_policy(set_of_profiles, "Borda")
    return esw



print(test_esw_mallows(n,m,k, dispersion, references))


from prog_dyn import Allocation, Borda, utilitarian, egalitarian, nash


def mallow_is_FI(n,m,k, references):
    """
    Test if bruteforce and esw have differents expected social welfares given a set of profiles.
    """
    # for n in range(1,10):
    #     for m in range(n,15):
    dispersion = 1 # dispertion = 1  => FI
    set_of_profiles = sample_k_mallows_profiles(k, n, m, dispersion, references) # Not working properly, I don't know why
    print(set_of_profiles[:10])
    # plot_permutation_histogram(set_of_profiles)
    brute_force_sw = bruteforce_expected_optimal_policy(set_of_profiles, "Borda", "egalitarian")
    prog_dyn = Allocation(1,n,m,Borda(m), egalitarian) # a = 1 => FI
    return brute_force_sw, prog_dyn

# print(mallow_is_FI(n,m,k, references))



def mallow_is_FC(n,m,k, references):
    """
    Test if bruteforce and esw have differents expected social welfares given a set of profiles.
    """
    # for n in range(1,10):
    #     for m in range(n,15):
    dispersion = 0 # dispertion = 0  => FC
    set_of_profiles = sample_k_mallows_profiles(k, n, m, dispersion, references)
    print(set_of_profiles[:10])
    brute_force_sw = bruteforce_expected_optimal_policy(set_of_profiles, "Borda", "egalitarian")
    prog_dyn = Allocation(0,n,m,Borda(m), egalitarian) # a = 0 => FC
    return brute_force_sw, prog_dyn


# print(mallow_is_FC(n,m,k, references))





