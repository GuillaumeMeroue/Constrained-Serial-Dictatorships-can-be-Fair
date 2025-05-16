import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from greedy_esw import construct_expected_esw_optimal_policy
from approx_prog_dyn import Allocation_luce, egalitarian, utilitarian, nash, Borda, QI, Lexicographic
from sample_luce import sample_k_luce_profiles
import json
import matplotlib.pyplot as plt
import numpy as np
import tqdm


def save_luce_for_tikz(n, m, k, score_function):
    """
    Save the data for the figure 2 for the tikz format using construct_esw_optimal_policy.
    """

    save_dir = "results"

    with open(f'{save_dir}/luce_x_allocation.txt', 'w') as alloc_file, \
         open(f'{save_dir}/luce_x_utilities_norm.txt', 'w') as util_norm_file, \
         open(f'{save_dir}/luce_x_utilities.txt', 'w') as util_file:

        # Write headers
        alloc_file.write('x ' + ' '.join([f'Nb{i}' for i in range(n)]) + '\n')
        util_norm_file.write('x ' + ' '.join([f'U{i}' for i in range(n)]) + '\n')
        util_file.write('x ' + ' '.join([f'U{i}' for i in range(n)]) + '\n')

        # Iterate over x values
        x_values = reversed(np.arange(1, 1.51, 0.01))  # FC to FI
        for x in tqdm.tqdm(x_values):

            values = [x**i for i in range(m)]
            set_of_profiles = sample_k_luce_profiles(k,values,n,m)
        
            # Construct expected social welfare optimal policy
            best_policy, max_min_utility, utilities = construct_expected_esw_optimal_policy(set_of_profiles, score_function)

            # Normalize utilities
            total_utility = sum(utilities)
            normalized_utilities = [u / total_utility for u in utilities]

            # Write results to files
            alloc_file.write(f'{x} ' + ' '.join(map(str, best_policy)) + '\n')
            util_file.write(f'{x} ' + ' '.join(map(str, utilities)) + '\n')
            util_norm_file.write(f'{x} ' + ' '.join(map(str, normalized_utilities)) + '\n')

# Parameters
n = 5
m = 70
k = 10000
score_function = "Borda"
# Call the function
save_luce_for_tikz(n, m, k, score_function)



def fct_of_x(k, n, m):
    """
    To plot the impact of correlation with Luce in the web app
    """
    results_dir = 'results'
    os.makedirs(results_dir, exist_ok=True)
    
    x_values = list(reversed(np.linspace(1, 2, 30))) # FC to FI

    all_results = []

    for ni in range(3, n):
        for mi in range(ni, m, 5):
            V = Borda(m)

            for F in [egalitarian, utilitarian, nash]:

                for x in x_values:
                    values = [x**i for i in range(mi)]
                    res, alloc, util = Allocation_luce(ni, mi, V, F, values, k)

                    print(res)
                    
                    result = {
                        'x': x,
                        'allocation': list(alloc),
                        'social_welfare': res[0][1],
                        'utilities': list(util),
                        'social_welfare': F.__name__  # Enregistre le nom du mécanisme
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

            # Save all results to a single JSON file
            json_filename = f'{results_dir}/luce_x.json'
            with open(json_filename, 'w') as f:
                json.dump(all_results, f, indent=1)


# fct_of_x(1000,5,70)



def fct_of_m(k, n, m):
    """
    Save data to plot Luce fct of m (and everithing else in the web app
    """
    results_dir = 'results'
    os.makedirs(results_dir, exist_ok=True)
    
    # x_values = list(reversed(np.linspace(1, 2, 5)))  # FC to FI
    x_values = [2, 1.5, 1.15, 1.05, 1]
    all_results = {}

    for ni in range(3, n):
        all_results[ni] = {}

        for i, V_cls in enumerate([Borda, Lexicographic, QI]):
            scoring_vector_name = ["Borda", "Lexicographic", "QI"][i]
            all_results[ni][scoring_vector_name] = {}

            for F in [egalitarian, utilitarian, nash]:
                print(ni, scoring_vector_name,F.__name__)
                social_welfare_name = F.__name__
                all_results[ni][scoring_vector_name][social_welfare_name] = {}

                for x in x_values:
                    all_results[ni][scoring_vector_name][social_welfare_name][x] = {}

                    allocations = []
                    utilities = []
                    sw = []

                    for mi in range(ni, m, 1):
                        print(mi)
                        V = V_cls(mi)
                        values = [x**i for i in range(mi)]
                        res, alloc, util = Allocation_luce(ni, mi, V, F, values, k, scoring_vector_name)

                        allocations.append(list(alloc))
                        utilities.append(list(util))
                        sw.append(res[0][1])
                        
                        result = {
                            'allocations': allocations,
                            'utilitiess': utilities,
                            'sw': sw
                        }

                        all_results[ni][scoring_vector_name][social_welfare_name][x] = result

            json_filename = f'{results_dir}/luce_m.json'
            with open(json_filename, 'w') as f:
                json.dump(all_results, f)


# fct_of_m(500,6,41)
