import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import numpy as np
from sample_luce import sample_k_luce_profiles
from scipy.stats import spearmanr, pearsonr, kendalltau



n = 5
m = 4
values = [10, 20, 30, 40]
k = 100

# First example
set_of_preference_profiles = sample_k_luce_profiles(k, values, n, m)
print(set_of_preference_profiles)



from sample_luce import sample_k_luce_profiles
from bruteforce import bruteforce_expected_optimal_policy


def test_bruteforce_luce(n,m,k):
    """
    Test if bruteforce and esw have differents expected social welfares given a set of profiles.
    """
    # for n in range(1,10):
    #     for m in range(n,15):
    # values = reversed(list(range(m)))
    values = list(range(m,0,-1))
    # print(values)
    set_of_profiles = sample_k_luce_profiles(k, values, n, m)
    brute_force_sw = bruteforce_expected_optimal_policy(set_of_profiles, "Borda", "utilitarian")
    return brute_force_sw


n = 3
m = 7
k = 1000

print(test_bruteforce_luce(n,m,k))

from greedy_esw import construct_expected_esw_optimal_policy


def test_esw_luce(n,m,k):
    """
    Test if bruteforce and esw have differents expected social welfares given a set of profiles.
    """
    # for n in range(1,10):
    #     for m in range(n,15):
    # values = reversed(list(range(m)))
    values = list(range(m,0,-1))
    print(values)
    set_of_profiles = sample_k_luce_profiles(k, values, n, m)
    esw = construct_expected_esw_optimal_policy(set_of_profiles, "Borda")
    return esw


print(test_esw_luce(20,50,1000))



from prog_dyn import Allocation, Borda, utilitarian, egalitarian, nash


def luce_is_FI(n,m,k):
    """
    Test if bruteforce and esw have differents expected social welfares given a set of profiles.
    """
    # for n in range(1,10):
    #     for m in range(n,15):
    values = [1] * m
    # print(values)
    set_of_profiles = sample_k_luce_profiles(k, values, n, m)
    # print(set_of_profiles[:10])

    brute_force_sw = bruteforce_expected_optimal_policy(set_of_profiles, "Borda", "egalitarian")
    prog_dyn = Allocation(1,n,m,Borda(m), egalitarian) # a = 1 => FI
    return brute_force_sw, prog_dyn

print(luce_is_FI(n,m,k))

# (((2, 2, 2, 2, 2), 10.959, array([19.   , 18.322, 17.287, 15.4  , 10.959])), 
# array([[10.        , 11.        ],
#        [ 2.        , 19.        ],
#        [ 2.        , 18.33333333],
#        [ 2.        , 17.28571429],
#        [ 2.        , 15.4       ],
#        [ 2.        , 11.        ]]))


def luce_is_FC(n,m,k):
    """
    Test if bruteforce and esw have differents expected social welfares given a set of profiles.
    """
    for n in range(2,5):
        for m in range(n,10):
            values = [1000 ** i for i in range(m-1,-1,-1)]
            print(values)
            set_of_profiles = sample_k_luce_profiles(k, values, n, m)
            print(set_of_profiles[:10])
            brute_force_sw = bruteforce_expected_optimal_policy(set_of_profiles, "Borda", "egalitarian")
            prog_dyn = Allocation(0,n,m,Borda(m), egalitarian) # a = 0 => FC
            return brute_force_sw, prog_dyn


# print(luce_is_FC(n,m,k))





# Correlation
# What are the correlation of profile fct of x 

def calculate_correlation(set_of_profiles, reference_profile):
    correlations = []
    for profile in set_of_profiles:
        for pref in profile:
            corr, _ = kendalltau(pref, reference_profile)
            correlations.append(corr)
    return np.mean(correlations)

def correlation_fct_of_x(x_values, reference_profile, k, n, m):
    correlations = []
    for x in x_values:
        values = [x ** i for i in range(1,m+1)]
        set_of_preference_profiles = sample_k_luce_profiles(k, values, n, m)
        corr = calculate_correlation(set_of_preference_profiles, reference_profile)
        correlations.append(corr)
        print(corr)
    return correlations

# Paramètres
n = 5
m = 70
k = 100
reference_profile = [i for i in range(m,0,-1)]
# x_values = np.arange(1, 5, 0.1)
x_values = np.arange(1, 3, 0.01)
# # x_values = np.geomspace(1, 10, 50)

# correlations = correlation_vs_x(x_values, reference_profile, k, n, m)

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 8))
for m in range(10, 71, 10):
    reference_profile = [i for i in range(m, 0, -1)]
    correlations = correlation_fct_of_x(x_values, reference_profile, k, n, m)
    plt.plot(list(x_values), correlations, label=f'm = {m}')



plt.axhline(y=0.95, color='red', linestyle='--', label='99% Correlation')

plt.xlabel('x: The coefficient factor between o_{i+1} and o_i')
plt.ylabel('Correlation with reference profile')
plt.title('Kendall-Tau correlation between generated profiles and reference profile as a function of x for some values of m')
plt.legend(title='Number of items')
plt.grid(True)
plt.show()