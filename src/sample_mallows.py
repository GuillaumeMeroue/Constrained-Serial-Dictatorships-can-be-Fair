import numpy as np

from prefsampling.ordinal import mallows


def sample_mallows_profile(n_players, m_objects, phi, central_vote):
    """
    Sample the preferences for each of the n_players according to Mallows' model.
    """

    norm_phi = False

    return mallows(n_players,m_objects,phi,norm_phi, central_vote)


def sample_k_mallows_profiles(k, n_players, m_objects, phi, central_vote):
    # single component mixture

    set_of_profiles = []
    for _ in range(k):
        set_of_profiles.append(sample_mallows_profile(n_players, m_objects, phi, central_vote))
    return set_of_profiles

# n = 3
# m = 5
# phi = 1 # 0 = FC, 1 = FI
# central_vote = np.arange(1,m+1)
# # central_vote = np.arange(m_objects)
# k = 2
# set_of_preference_profiles = sample_k_mallows_profiles(k, n, m, phi, central_vote)
# print(set_of_preference_profiles)
