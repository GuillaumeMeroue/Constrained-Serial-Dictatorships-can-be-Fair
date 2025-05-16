import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


from sample_mallows import sample_k_mallows_profiles
from sample_luce import sample_k_luce_profiles
from prog_dyn import Allocation
from approx_prog_dyn import Allocation_luce, Borda, nash, utilitarian, egalitarian
from bruteforce import bruteforce_expected_optimal_policy
from sample_IC import sample_k_IC_profiles
from utility import compute_expected_social_welfare, compute_score_vector
import numpy as np

all_n = [2,3, 4]
all_m = [4, 7, 10]
social_welfare = ["egalitarian", "nash", "utilitarian"]
all_F = [egalitarian, nash, utilitarian]

k = 1000
n = 5
m = 30

score_function = "Borda"



all_results = {}

def bruteforce_examples():
    "To buils tables of the appendix"
    x = 1.1
    phi = 0.8

    distributions = ["IC", "Luce", "Mallows", "FC"]

    for distribution in distributions:
        for n in all_n:
            if n not in all_results:
                all_results[n] = {}
            for m in all_m:
                if m not in all_results[n]:
                    all_results[n][m] = {}

                if distribution == "IC":
                    set_of_profiles = sample_k_IC_profiles(k, n, m)
                elif distribution == "Luce":
                    values = [x ** i for i in range(m)]
                    set_of_profiles = sample_k_luce_profiles(k, values, n, m)
                elif distribution == "Mallows":
                    central_vote = [i for i in range(1, m+1)]
                    set_of_profiles = sample_k_mallows_profiles(k, n, m, phi, central_vote)
                elif distribution == "FC":
                    set_of_profiles = [[ [i for i in range(1, m+1)] for agent in range(n) ]]

                for welfare_function in social_welfare:
                    best_policy, max_welfare, best_utilities = bruteforce_expected_optimal_policy(
                        set_of_profiles, score_function, welfare_function)

                    if distribution not in all_results[n][m]:
                        all_results[n][m][distribution] = {}
                    
                    all_results[n][m][distribution][welfare_function] = (best_policy, best_utilities)

    save_results_to_file()
    for distribution in distributions:
        generate_latex_table(distribution)

shorten_sw = {"egalitarian":"ESW", "nash":"NSW", "utilitarian":"USW"}   

def save_results_to_file():
    with open("results.txt", "w") as file:
        for n in all_results:
            for m in all_results[n]:
                for distribution in all_results[n][m]:
                    file.write(f"\n\nn={n}, m={m}, Distribution={distribution}\n")
                    for welfare_function in all_results[n][m][distribution]:
                        best_policy, best_utilities = all_results[n][m][distribution][welfare_function]
                        file.write(f"SW: {welfare_function}\n")
                        file.write(f"Best Policy: {best_policy}\n")
                        file.write(f"Best Utilities: {best_utilities}\n")


def generate_latex_table(distribution):
    latex_table = "\\begin{table}[H]\n"
    latex_table += f"\\caption{{Results for {distribution} Distribution}}\n"
    latex_table += "\\centering\n"
    latex_table += "\\begin{tabular}{|c|c|c|c|}\n\\hline\n"
    latex_table += "(n,m) & SW & Best Policy & Best Utilities \\\\ \\hline\n"
    
    for n in all_results:
        for m in all_results[n]:
            for welfare_function in all_results[n][m][distribution]:
                best_policy, best_utilities = all_results[n][m][distribution][welfare_function]
                latex_table += f"({n},{m}) & {shorten_sw[welfare_function]} & {best_policy} & {best_utilities} \\\\ \\hline\n"
            latex_table += "\\hline\n"
        # latex_table += "\\hline\n"



    latex_table += "\\end{tabular}\n"
    latex_table += "\\end{table}"

    print(latex_table)

    file_name = f"table_{distribution.lower()}.tex"
    with open(file_name, "w") as file:
        file.write(latex_table)


bruteforce_examples()
