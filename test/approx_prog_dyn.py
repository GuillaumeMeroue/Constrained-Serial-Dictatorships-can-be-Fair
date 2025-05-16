import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


from greedy_esw import construct_expected_esw_optimal_policy, construct_expected_esw_optimal_leximin_policy
from approx_prog_dyn import Allocation_luce, Borda, egalitarian
from bruteforce import bruteforce_expected_optimal_policy_leximin
import numpy as np
from sample_luce import sample_k_luce_profiles



def compare_esw_with_semi():
    "Compare the social welfare of esw and out prefious function"
    k = 1000
    for n in range(2,10):
        for m in range(n,20):
            if n != 3 or m  != 18:
                continue
            values = [100**-i for i in range(m)]
            set_of_profile = sample_k_luce_profiles(k,values,n,m)
            prog_dyn = Allocation_luce(n,m,Borda(m), egalitarian, values, k)
            esw = construct_expected_esw_optimal_policy(set_of_profile, "Borda")
            esw = construct_expected_esw_optimal_leximin_policy(set_of_profile, "Borda")
            # esw = bruteforce_expected_optimal_policy_leximin(set_of_profile, "Borda", "egalitarian")

            print(n,m, esw)
            print(prog_dyn)
            assert( abs(prog_dyn[0,1] - esw[1]) < 1e-2)
            if not np.array_equal(prog_dyn[1:,0], np.array(esw[0], dtype=np.float64)):
                print("Two differents policy")


compare_esw_with_semi()