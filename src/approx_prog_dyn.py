import numpy as np
import copy

from utility import compute_expected_social_welfare, compute_expected_utilities, compute_expected_utilities_list, compute_score_vector
from sample_luce import sample_k_luce_profiles

# Scoring vector

def Borda(n):
    return [0] + [ n - i + 1 for i in range(1,n+1)] # The first element is not used

def Lexicographic(m):
    return [0] + [ 2 ** ( m - i ) for i in range(m)]

eps = 5.e-2

def QI(m):
    return [0] + [ 1 + eps * (m - i) for i in range(m) ]

# Social welfare

def egalitarian(x,y):
    return min(x,y)

def utilitarian(x,y):
    return x + y

def nash(x,y):
    return x * y


def Utility_sampling(k,t, set_of_profiles, score_vector, U):
    """
        Compute the expected utility of an agent picking t objects knowing that k already have been picked
    """
    if U[k, t] != -1:
        return U[k, t]

    n = len(set_of_profiles[0])
    policy = [k, t] + [0 for _ in range(n-2)]

    expected_utilities = compute_expected_utilities(policy, set_of_profiles, score_vector)
    U[k, t] = expected_utilities[1]
    return expected_utilities[1]

 

def Alloc_aux(set_of_profiles,i,k,l,m,V,U,M,F, score_vector):
    """
    Compute the optimal (partial) social welfare (and the policy) for :
    - set_of_profile
    - i the i-th agent ( to fill M)
    - k objets already selected
    - l users left
    - m objects in total
    - V the vector of score
    - U array used for the memoisation of Utility(k,t)
    - M array used for the memoisation of G(i,l)
    """

    if M[k,l,0,0] == -1: # if not already computed
        M[k,l,0,0] = m   # set as computed
        if l == 1 :      # if there is just one agent
            M[k,1,i,0] = m - k  # then he takes all remaining objetcs
            M[k,1,i,1] = Utility_sampling(k, m - k, set_of_profiles, score_vector, U)
            M[k,1,0,1] = M[k,1,i,1] #there is one agent so the partial social welfare is her utility
        else:
            SW_max = 0   #  we want to keep the utility which optimize the social welfare
            for t in range(m-k+1): # we will give t=0...(m-k) objets to agent i
                U_k = Utility_sampling(k, t, set_of_profiles, score_vector, U) # we compute his expected utility
                partiel = Alloc_aux(set_of_profiles,i+1,k+t,l-1,m,V,U,M,F, score_vector) # compute the sub-problem solution
                SW = F(partiel[0][1],U_k) # compute the expected social welfare
                if SW > SW_max: #if the policy maximize the social welfare
                    M[k,l] = copy.deepcopy(partiel)  # save policy of the sub-problem
                    M[k,l,0,1] = SW # change the social welfare
                    M[k,l,i,0] = t # add the number of objects given to agent i
                    M[k,l,i,1] = U_k #add the expected utility of agent i 
                    SW_max = SW
                                
    return M[k,l]

def Allocation_luce(n,m,V,F,values,k, scoring_function="Borda"):
    """
    Compute the optimal policy for :
    - a the coefficient of correlation
    - n the number of agents
    - m the number of objetcs
    - V the scoring vector
    - F the social welfare
    """
    U = np.full((m + 1, m + 1), -1.0)
    M = np.full((m+1,n+1,n+1,2),-1.0)
    # values = list(range(1,m+1))

    set_of_profile = sample_k_luce_profiles(k, values, 2, m)

    score_vector = compute_score_vector(m, scoring_function)

    res = Alloc_aux(set_of_profile,1,0,n,m,V,U,M,F, score_vector)
    alloc = res[1:,0]
    utilities = res[1:,1]

    # utilities = compute_expected_utilities_list(alloc, set_of_profile, "Borda")
    return res, alloc, utilities

# n = 5
# k = 100
# m = 30
# V = Borda(m)
# F = egalitarian
# values = [100**-i for i in range(m)]
# # values = [1 for i in range(m)]

# print(Allocation_luce(n,m,V,F,values,k))



n = 3
k = 100
m = 15
V = Borda(m)
F = utilitarian
values = [1 for i in range(m)]
# values = [1 for i in range(m)]

# print(Allocation_luce(n,m,V,F,values,k))