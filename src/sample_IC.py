import numpy as np

def sample_IC(n,m):
    rng = np.random.default_rng()
    objs = list(range(1,m+1))
    votes = []
    for _ in range(n):
        votes.append(list(rng.permutation(objs)))
    return votes

def sample_k_IC_profiles(k, n, m):
    set_of_profiles = []
    for _ in range(k):
        set_of_profiles.append(sample_IC(n,m))
    return set_of_profiles

# Test
# k = 10
# n = 5
# m = 10
# profiles = sample_k_profiles(k, n, m)
# print(profiles)
