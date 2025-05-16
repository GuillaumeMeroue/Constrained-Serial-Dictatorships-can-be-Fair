from utility import compute_score_vector, compute_expected_social_welfare, compute_social_welfare, compute_expected_utilities, social_welfare
from generate_policies import generate_policy
from allocation import allocate_objects


def bruteforce_optimal_policy(profile, score_function, aggregation_function):
    """
    This function compute the optimal policy knowing the profile of preferences of agents
    """
    n = len(profile)
    m = len(profile[0])
    score_vector = compute_score_vector(m, score_function)
    max_welfare = -float('inf')
    best_policy = None

    for policy in generate_policy(n, m):
        allocation = allocate_objects(policy, profile)
        social_welfare = compute_social_welfare(allocation, profile, score_vector, aggregation_function)
        if social_welfare > max_welfare:
            max_welfare = social_welfare
            best_policy = policy

    return best_policy, max_welfare



# With expected utility
def bruteforce_expected_optimal_policy(set_of_profiles, score_function, aggregation_function):
    k = len(set_of_profiles)
    n = len(set_of_profiles[0])
    m = len(set_of_profiles[0][0])
    score_vector = compute_score_vector(m, score_function)
    # print(score_vector)
    max_welfare = -float('inf')
    best_policy = None

    for policy in generate_policy(n, m):
        expected_social_welfare, expected_utilities = compute_expected_social_welfare(policy, set_of_profiles, score_vector, aggregation_function)
        # print(expected_social_welfare)
        # print(policy, expected_social_welfare)
        if expected_social_welfare > max_welfare:
            max_welfare = expected_social_welfare
            best_policy = policy
            best_utilities = expected_utilities


    return best_policy, max_welfare, best_utilities



# Leximin one
def bruteforce_expected_optimal_policy_leximin(set_of_profiles, score_function, aggregation_function):
    k = len(set_of_profiles)
    n = len(set_of_profiles[0])
    m = len(set_of_profiles[0][0])
    score_vector = compute_score_vector(m, score_function)
    best_utilities = [0] * n
    sorted_best_utilities =  [0] * n
    best_policy = None

    for policy in generate_policy(n, m):
        expected_utilities = compute_expected_utilities(policy, set_of_profiles, score_vector)
        # print(expected_social_welfare)
        # Optimize leximin
        sorted_expected_utilities = sorted(expected_utilities)
        if  sorted_expected_utilities > sorted_best_utilities:
            best_utilities = expected_utilities
            best_policy = policy
            sorted_best_utilities = sorted_expected_utilities
        
        max_welfare = social_welfare(best_utilities, aggregation_function) 


    return best_policy, max_welfare, best_utilities