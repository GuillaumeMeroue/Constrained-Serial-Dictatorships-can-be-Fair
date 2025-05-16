import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


from prog_dyn import Allocation, Borda, egalitarian
from greedy_esw import construct_esw_optimal_policy, construct_expected_esw_optimal_policy
import numpy as np

def compare_esw_with_FC():
    "Compare the social welfare of esw and out prefious function"
    for n in range(2,10):
        for m in range(n,20):
            prog_dyn = Allocation(0,n,m,Borda(m), egalitarian) # a = 0 => FC
            profile = [list(range(1,m+1))] * n # FC
            esw = construct_esw_optimal_policy(profile, "Borda")
            print(n,m, esw)
            print(prog_dyn)
            assert(prog_dyn[0,1] == esw[1])
            if not np.array_equal(prog_dyn[1:,0], np.array(esw[0], dtype=np.float64)):
                print("Two differents policy") # We can have different policies with the same (best) social welfare


# compare_esw_with_FC()


from sample_IC import sample_k_IC_profiles
def compare_esw_with_IC():
    "Compare the social welfare of esw and out prefious function"
    k = 10000
    for n in range(2,10):
        for m in range(n+1,20):
            prog_dyn = Allocation(1,n,m,Borda(m), egalitarian) # a = 0 => IC
            profiles =  sample_k_IC_profiles(k,n,m)
            esw = construct_expected_esw_optimal_policy(profiles, "Borda")
            print(n,m, esw)
            print(prog_dyn)
            assert(abs (prog_dyn[0,1] -  esw[1]) < 0.1)
            if not np.array_equal(prog_dyn[1:,0], np.array(esw[0], dtype=np.float64)):
                print("Two differents policy") # We can have different policies with the same (best) social welfare


compare_esw_with_IC()