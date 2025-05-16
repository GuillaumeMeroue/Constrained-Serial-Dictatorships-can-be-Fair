from utility import compute_score_vector, compute_utility
from allocation import allocate_objects

def construct_esw_optimal_policy(profile, score_function):
    n = len(profile)
    m = len(profile[0])
    score_vector = compute_score_vector(m, score_function)
    
    current_policy = [0] * n
    max_min_utility = -float('inf')
    best_policy = None

    for i in range(m+1):
        allocation = allocate_objects(current_policy, profile)
        utilities = [compute_utility(profile[i], allocation[i], score_vector) for i in range(n)]

        min_utility = utilities[0]
        chosen_agent = 0
        for agent_id, utility in enumerate(utilities):
            if utility < min_utility:
                chosen_agent = agent_id
                min_utility = utility

        if min_utility > max_min_utility:
            max_min_utility = min_utility
            best_policy = current_policy.copy()

        if i<m: current_policy[chosen_agent] += 1 # Don't add m + 1 objects but the last loop test if the ESW is better at the end (when j=m) 


    # Complete the policy by giving all remaining objects to the last agent
    remaining_objects = m - sum(best_policy)
    best_policy[-1] += remaining_objects

    return best_policy, max_min_utility


# Test
# from generate_profiles import generate_preference_profile
# import numpy as np
# np.random.seed(41)
# n = 5
# m = 20
# profile = generate_preference_profile(n, m)
# best_policy, max_welfare = construct_esw_optimal_policy(profile, "Borda")
# print("Best policy:", best_policy, max_welfare)


# Expected
from utility import compute_expected_utilities


def construct_expected_esw_optimal_policy(set_of_profiles, score_function):

    k = len(set_of_profiles)
    n = len(set_of_profiles[0])
    m = len(set_of_profiles[0][0])

    score_vector = compute_score_vector(m, score_function)
    
    current_policy = [0] * n
    max_min_utility = -float('inf')
    best_policy = None

    for i in range(m+1):

        utilities = compute_expected_utilities(current_policy, set_of_profiles, score_vector)

        min_utility = utilities[0]
        chosen_agent = 0
        for agent_id, utility in enumerate(utilities):
            if utility < min_utility:
                chosen_agent = agent_id
                min_utility = utility

        if min_utility > max_min_utility:
            max_min_utility = min_utility
            best_policy = current_policy.copy()


        if i<m: current_policy[chosen_agent] += 1 # Don't add m + 1 objects but the last loop test if the ESW is better at the end (when j=m) 


    # Complete the policy by giving all remaining objects to the last agent
    remaining_objects = m - sum(best_policy)
    best_policy[-1] += remaining_objects
    best_utilities = compute_expected_utilities(best_policy, set_of_profiles, score_vector)

    return best_policy, max_min_utility, best_utilities



from sample_IC import sample_k_IC_profiles
import numpy as np
n = 10
m = 150
k = 1000
set_of_profiles = sample_k_IC_profiles(k, n, m)
# best_policy, max_welfare, best_utilities = construct_expected_esw_optimal_policy(set_of_profiles, "Borda")
# print("Best policy:", best_policy, max_welfare, best_utilities)





# leximin

def construct_expected_esw_optimal_leximin_policy(set_of_profiles, score_function):

    k = len(set_of_profiles)
    n = len(set_of_profiles[0])
    m = len(set_of_profiles[0][0])

    score_vector = compute_score_vector(m, score_function)
    
    current_policy = [0] * n
    max_min_utility = -float('inf')
    best_policy = None
    remaining_objects = m
    from_agent = 0 # We give object from agent from_agent to m
    k = 0
    while remaining_objects > 0 and from_agent < n:
        print(from_agent)
        # print(utilities)
        for i in range(remaining_objects + 1):
            utilities = compute_expected_utilities(current_policy, set_of_profiles, score_vector)

            # print(n,m,from_agent)

            min_utility = utilities[from_agent]
            chosen_agent = from_agent
            for agent_id, utility in enumerate(utilities[from_agent:], start=from_agent):
                if utility < min_utility:
                    chosen_agent = agent_id
                    min_utility = utility
                    # print(from_agent, agent_id, utilities)

            if min_utility > max_min_utility:
                max_min_utility = min_utility
                best_policy = current_policy.copy()

            if i < remaining_objects:
                current_policy[chosen_agent] += 1  # Don't add remaining_objects + 1 objects but the last loop test if the ESW is better at the end (when j=m)

        # Update the remaining objects
        remaining_objects = m - sum(best_policy)
        utilities = compute_expected_utilities(best_policy, set_of_profiles, score_vector)
        current_policy = best_policy.copy()
        print(utilities)

        min_utility = utilities[from_agent]
        for agent_id, utility in enumerate(utilities[from_agent:], start=from_agent):
            if utility < min_utility:
                from_agent = agent_id
                min_utility = utility

        if from_agent == n-1:
            best_policy[n-1] += remaining_objects # We give all remainings objects to the last agent
            remaining_objects = 0
        else:
            from_agent += 1 # We start to give object to agents after the index of the current min.
        
    best_utilities = compute_expected_utilities(best_policy, set_of_profiles, score_vector)

    return best_policy, max_min_utility, best_utilities


# n = 7
# m = 11
# k = 100
# set_of_profiles = sample_k_profiles(k, n, m)
# best_policy, max_welfare, best_utilities = construct_expected_esw_optimal_leximin_policy(set_of_profiles, "Borda")
# print("Best policy:", best_policy, max_welfare, best_utilities)