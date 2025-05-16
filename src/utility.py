import numpy as np
from allocation import allocate_objects


def compute_utility(pref, allocation, score_vector):
    """
    Compute the utility of an agent given her allocation, preference and scoring vector
    """
    utility = 0
    rank_dict = {obj: rank for rank, obj in enumerate(pref)}
    for obj in allocation:
        rank = rank_dict[obj] + 1
        utility += score_vector[rank - 1]
    return utility

def compute_utility_list(pref, allocation, score_vector):
    """
    Compute the utility of an agent given her allocation, preference and scoring vector, it return utilities object by object
    """
    utility = []
    rank_dict = {obj: rank for rank, obj in enumerate(pref)}
    for obj in allocation:
        rank = rank_dict[obj] + 1
        utility.append(score_vector[rank - 1])
    return utility


def compute_social_welfare(allocation, profile, score_vector, aggregation_function):
    utilities = [compute_utility(profile[i], allocation[i], score_vector) for i in range(len(profile))]
    return social_welfare(utilities,aggregation_function)

def social_welfare(utilities, aggregation_function):
    if aggregation_function == 'utilitarian':
        return sum(utilities)
    elif aggregation_function == 'egalitarian':
        return min(utilities)
    elif aggregation_function == 'nash':
        return np.prod(utilities)


def compute_score_vector(m, score_function):
    if score_function == "Borda":
        return  [m - k + 1 for k in range(1, m + 1)]
    elif score_function == "Lexicographic":
        return [2 ** (m - k) for k in range(1, m + 1)]
    elif score_function == "QI":
        return [1 + 0.05 * (m - k) for k in range(1, m + 1)]


def compute_expected_utilities(policy, set_of_profiles, score_vector):
    
    n = len(policy)
    m = len(score_vector)
    total_utilities = np.zeros(n)
    k = len(set_of_profiles)

    for profiles in set_of_profiles:
        allocations = allocate_objects(policy, profiles)
        for i in range(n):
            total_utilities[i] += compute_utility(profiles[i], allocations[i], score_vector)

    return total_utilities / k

def compute_expected_utilities_list(policy, set_of_profiles, score_function):

    n = len(policy)
    m = len(set_of_profiles[0][0])
   
    score_vector = compute_score_vector(m, score_function)

    
 
    total_utilities = [ None for i in range(n)]
    k = len(set_of_profiles)

    for profiles in set_of_profiles:
        allocations = allocate_objects(policy, profiles)
        for i in range(n):
            if total_utilities[i] is None:
                total_utilities[i] = np.array(compute_utility_list(profiles[i], allocations[i], score_vector))
            else:
                total_utilities[i] += np.array(compute_utility_list(profiles[i], allocations[i], score_vector))

    return [ list(agent_utilities / k) for agent_utilities in total_utilities]



def compute_expected_social_welfare(policy, set_of_profiles, score_vector, aggregation_function):

    expected_utilities = compute_expected_utilities(policy, set_of_profiles, score_vector)

    return social_welfare(expected_utilities, aggregation_function), expected_utilities



# Test
# from generate_policies import generate_policy
# from generate_IC_profiles import sample_k_IC_profiles
# from allocation import allocate_objects

# n = 10
# m = 20
# all_policies = generate_policy(n,m)
# for _ in range(200000): next(all_policies) # To have an interesting policy
# policy = next(all_policies)
# print(policy)
# profile = sample_k_IC_profiles(1,n,m)[0]
# print(profile)
# allocation = allocate_objects(policy, profile)
# print(allocation)
# score_vector = compute_score_vector(m,"Borda")
# print(score_vector)
# social_welfare = compute_social_welfare(allocation, profile, score_vector, 'utilitarian')
# print(social_welfare)




# Expected Social Welfare
# n = 5
# m = 30
# k = 1000
# score_vector = compute_score_vector(m, "Lexicographic")


# policy = [3,2,2,3,20]
# set_of_profiles = sample_k_IC_profiles(k, n, m)
# expected_social_welfare, expected_utilities = compute_expected_social_welfare(policy, set_of_profiles, score_vector, "egalitarian")

# print(expected_utilities)