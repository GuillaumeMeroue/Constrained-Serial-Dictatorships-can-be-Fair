# Old version
# 
# import numpy as np
# def sample_preference_profile(n_players, m_objects, values):
#     """
#     Sample the preferenceces for each of the n players according to Luce's model.
#     """
#     values = np.array(values)
    
#     preference_profiles = []
    
#     for _ in range(n_players):

#         remaining_objects_index = list(range(m_objects))

#         preference = []
        
#         for _ in range(m_objects):
#             # Calculate the probabilities for each remaining object
#             remaining_values = values[remaining_objects_index]
#             probabilities = remaining_values / remaining_values.sum()
           
#             chosen_index = np.random.choice(remaining_objects_index, p=probabilities)
#             chosen_object = chosen_index + 1
            
#             preference.append(chosen_object)
            
#             remaining_objects_index.remove(chosen_index)
        
#         preference_profiles.append(preference)
    
#     return preference_profiles


from prefsampling.ordinal import plackett_luce

def sample_preference_profile(n_players, m_objects, values):
    return [[obj + 1 for obj in pref] for pref in plackett_luce(n_players, m_objects, values)] # correct the fact that objetc are sampled between 0 and m-1 and note 1 to m



def sample_k_luce_profiles(k, values, n, m):
    set_of_profiles = []
    for _ in range(k):
        set_of_profiles.append(sample_preference_profile(n,m,values))
    return set_of_profiles



# n = 5
# m = 4
# values = [10, 20, 30, 40]
# k = 100

# # First example
# set_of_preference_profiles = sample_k_luce_profiles(k, values, n, m)
# print(set_of_preference_profiles)