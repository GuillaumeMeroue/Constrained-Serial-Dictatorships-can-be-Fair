import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from utility import compute_expected_utilities_list
from greedy_esw import construct_expected_esw_optimal_policy
from sample_mallows import sample_k_mallows_profiles
import numpy as np
import matplotlib.pyplot as plt
import json
import os

    # dispersions = np.linspace(0, 1, num=30)
    # dispersions = 1 - np.geomspace(1, 1e-1, num=30)


        

k = 1000
n = 10
m = 30
n_values = range(3, 5)



def save_mallows_for_tikz(n, m, k):
    """
    Save the data for the figure 2 for the tikz format
    """

    save_dir = "results"

    with open(f'{save_dir}/mallows_phi_allocation.txt', 'w') as alloc_file, open(f'{save_dir}/mallows_phi_utilities_norm.txt', 'w') as util_norm_file, open(f'{save_dir}/mallows_phi_utilities.txt', 'w') as util_file:

        alloc_file.write('phi ' + ' '.join([f'Nb{i}' for i in range(n)]) + '\n')
        util_file.write('phi ' + ' '.join([f'U{i}' for i in range(n)]) + '\n')
        util_norm_file.write('phi ' + ' '.join([f'U{i}' for i in range(n)]) + '\n')

        references = list(range(1, m + 1))


        dispersion_values = np.arange(0, 1.02, 0.02)
        for phi in dispersion_values:

            set_of_profiles = sample_k_mallows_profiles(k, n, m, phi, references)
            esw = construct_expected_esw_optimal_policy(set_of_profiles, "Borda")
            
            allocations, max_min_utility, utilities = esw
            print(allocations, utilities)
            
            total_utility = sum(utilities)
            normalized_utilities = [u / total_utility for u in utilities]
            
            alloc_file.write(f'{phi} ' + ' '.join(map(str, allocations)) + '\n')
            util_file.write(f'{phi} ' + ' '.join(map(str, utilities)) + '\n')
            util_norm_file.write(f'{phi} ' + ' '.join(map(str, normalized_utilities)) + '\n')

save_mallows_for_tikz(5,70,10000)


def fct_of_phi(k, n, m):
    """
    Data to visualise impact of correlation in the webapp
    """
    results_dir = 'results'
    os.makedirs(results_dir, exist_ok=True)
    
    dispersions = np.linspace(0, 1, num=21)
    all_results = []

    all_results = []

    for ni in range(3, n):
        for mi in range(ni, m,5):
            references = list(range(1, mi + 1))

            for dispersion in dispersions:
                set_of_profiles = sample_k_mallows_profiles(k, ni, mi, dispersion, references)
                esw = construct_expected_esw_optimal_policy(set_of_profiles, "Borda")
                
                best_policy, max_min_utility, best_utilities = esw

                print(esw)

                objects_utilities = compute_expected_utilities_list(best_policy, set_of_profiles, "Borda")
                
                result = {
                    'dispersion': dispersion,
                    'allocation': esw[0],
                    'objects_utilities': objects_utilities,
                    'social_welfare': esw[1],
                    'utilities': esw[2].tolist()
                }
                
                if not any(d['n'] == ni and d['m'] == mi for d in all_results):
                    all_results.append({
                        'n': ni,
                        'm': mi,
                        'k': k,
                        'results': []
                    })

                for entry in all_results:
                    if entry['n'] == ni and entry['m'] == mi:
                        entry['results'].append(result)

            json_filename = f'{results_dir}/mallows_phi.json'
            with open(json_filename, 'w') as f:
                json.dump(all_results, f)

