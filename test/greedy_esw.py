import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from greedy_esw import construct_esw_optimal_policy
from sample_IC import sample_k_IC_profiles
import numpy as np
np.random.seed(41)
n = 5
m = 20
profile = sample_k_IC_profiles(1,n, m)[0]
best_policy, max_welfare = construct_esw_optimal_policy(profile, "Borda")
print("Best policy:", best_policy, max_welfare)




from sample_IC import sample_k_IC_profiles
import numpy as np
n = 10
m = 150
k = 1000
set_of_profiles = sample_k_IC_profiles(k, n, m)
# best_policy, max_welfare, best_utilities = construct_expected_esw_optimal_policy(set_of_profiles, "Borda")
# print("Best policy:", best_policy, max_welfare, best_utilities)




from sample_IC import sample_IC
from bruteforce import bruteforce_optimal_policy
from greedy_esw import construct_esw_optimal_policy

def test_bruteforce_equal_esw():
    """
    Test if bruteforce and esw have differents social welfares
    """
    for n in range(1,10):
        for m in range(n,15):
            profile = sample_IC(n,m) # only one is selected amoung (m!)^(n-1)
            brute_force_sw = bruteforce_optimal_policy(profile, "Borda", "egalitarian")[1]
            esw = construct_esw_optimal_policy(profile, "Borda")[1]
            assert(brute_force_sw == esw)
            print(n,m, brute_force_sw)


# test_bruteforce_equal_esw()


from sample_IC import sample_k_IC_profiles
from bruteforce import bruteforce_expected_optimal_policy
from greedy_esw import construct_expected_esw_optimal_policy

def test_expected_bruteforce_equal_esw(k=30):
    """
    Test if bruteforce and esw have differents expected social welfares given a set of profiles.
    """
    for n in range(1,10):
        for m in range(n,15):
            set_of_profiles = sample_k_IC_profiles(k, n, m)
            brute_force_sw = bruteforce_expected_optimal_policy(set_of_profiles, "Borda", "egalitarian")
            esw = construct_expected_esw_optimal_policy(set_of_profiles, "Borda")
            print(n, m, esw, brute_force_sw)
            assert(brute_force_sw[1] == esw[1])


# test_expected_bruteforce_equal_esw()