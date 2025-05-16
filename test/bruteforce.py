import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
                                                
from bruteforce import bruteforce_expected_optimal_policy, bruteforce_expected_optimal_policy_leximin, bruteforce_optimal_policy
from sample_IC import sample_k_IC_profiles
import numpy as np


n = 5
m = 20
profile = sample_k_IC_profiles(1,n, m)[0]
best_policy, max_welfare = bruteforce_optimal_policy(profile, "Borda", "egalitarian")
print("Best policy:", best_policy, max_welfare)



# With with expected utility
from sample_IC import sample_k_IC_profiles
k = 20
set_of_profiles = sample_k_IC_profiles(k,n,m)
allocation, sw, utilities = bruteforce_expected_optimal_policy(set_of_profiles, "Borda", "egalitarian")
print(allocation, sw, utilities)



# Optimizing leximing
allocation, sw, utilities = bruteforce_expected_optimal_policy_leximin(set_of_profiles, "Borda", "egalitarian")
print(allocation, sw, utilities)