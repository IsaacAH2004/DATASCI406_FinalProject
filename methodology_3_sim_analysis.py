## Imports
# Please note that, to run this code, you will need to be using an environment
# where these libraries are installed.
# The Conda package manager comes pre-loaded with most of these. 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

# for consistent results
np.random.seed(42)

# The following functions will be used throughout the simulation. 
# They include generating power law samples, fitting power law parameters,
# computing KS statistics, and performing the Monte Carlo KS test.

# FORMULA SOURCE: https://stats.stackexchange.com/questions/563921/maximum-likelihood-estimator-for-power-law-with-negative-exponent#:~:text=Solution,languages%2C%20see%20e.g.%20here.)
def power_law_mle_alpha(data_vals, x_minimum=None):
    if x_minimum is None:
        x_minimum = np.min(data_vals)
    
    filtered_data = data_vals[data_vals >= x_minimum]
    num_obs = len(filtered_data)
    alpha_estimate = 1 + num_obs / np.sum(np.log(filtered_data / x_minimum))
    
    return alpha_estimate, x_minimum

# CDF SOURCE: https://en.wikipedia.org/wiki/Power_law#Continuous_power_law_distribution
def power_law_cdf(x, alpha, x_minimum):
    return 1 - (x / x_minimum) ** (1 - alpha)

def generate_power_law_samples(num_samples, alpha, x_minimum, x_maximum):
    uniform_vals = np.random.uniform(0, 1, num_samples)
    
    samples = x_minimum * (1 - uniform_vals * (1 - (x_minimum / x_maximum) ** (alpha - 1))) ** (-1 / (alpha - 1))
    
    return samples

# Compute the Kolmogorov-Smirnov statistic
# SOURCE: https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test
def compute_ks_statistic(data_vals, alpha, x_minimum):
    sorted_data = np.sort(data_vals[data_vals >= x_minimum])
    num_obs = len(sorted_data)
    
    empirical_cdf = np.arange(1, num_obs + 1) / num_obs
    theoretical_cdf = power_law_cdf(sorted_data, alpha, x_minimum)
    ks_stat = np.max(np.abs(empirical_cdf - theoretical_cdf))
    
    return ks_stat

# The following functions are purpose-built for the simulation and analysis.
# They take advantage of the funcitons created above -- please refer to them
# to understand this section. 
def monte_carlo_ks_test(data_vals, alpha, x_minimum):
    num_obs = len(data_vals)
    x_maximum = np.max(data_vals) * 1.5
    
    observed_ks = compute_ks_statistic(data_vals, alpha, x_minimum)
    simulated_ks = np.zeros(10000)
    
    for i in range(10000):
        
        synthetic_data = generate_power_law_samples(num_obs, alpha, x_minimum, x_maximum)
        simulated_ks[i] = compute_ks_statistic(synthetic_data, alpha, x_minimum)
    
    p_val = np.mean(simulated_ks >= observed_ks)
    
    return observed_ks, simulated_ks, p_val

# Corresponds to simulation for methodology 3, paragraph 1. 
# This, and simulation part 2, takes VERY long to run with all 4000 observations.
def simulation_part1(num_obs=4000, true_alpha=2.5):
    print("\nSIMULATION 1: Testing when assumptions HOLD")
    
    x_minimum = 2.0
    x_maximum = 15.0
    pvalues_list = []
    type_i_error_accumulator = 0
    
    # using 1000 simulations -- change 1000 to some other number for more/less runs. 
    for i in range(1000):
        # Uncomment for updates
        # if (i + 1) % 200 == 0:
        #   print("Run", i + 1, "/", 1000)
        
        synthdata = generate_power_law_samples(num_obs, true_alpha, x_minimum, x_maximum)
        alpha, _ = power_law_mle_alpha(synthdata, x_minimum=x_minimum)
        not_needed, not_needed2, p_value = monte_carlo_ks_test(synthdata, alpha, x_minimum)
        pvalues_list.append(p_value)
        
        if p_value < 0.05:
            type_i_error_accumulator += 1
    
    type_i_rate = type_i_error_accumulator / 1000
    
    print("Mean p-value:", np.mean(pvalues_list))
    print("Type I error rate:", type_i_rate)

# Methodology 3, paragraph 2 simulation.
def simulation_part2(num_obs=4000):
    print("\nSIMULATION 2: Testing when assumptions VIOLATED")
    
    mu = 1.5
    sigma = 0.5
    x_minimum = 2.0
    
    pvalues_list = []
    numreject = 0
    
    for i in range(1000):
        # Uncomment for updates
        # if (i + 1) % 200 == 0:
        #   print("Run", i + 1, "/", 1000)
        
        # Same process as above, except the data for comparison is drawn from a lognormal distribution. 
        lognorm_data = np.random.lognormal(mu, sigma, num_obs)
        lognorm_data = lognorm_data[lognorm_data >= x_minimum]
        
        alpha, _ = power_law_mle_alpha(lognorm_data, x_minimum=x_minimum)
        not_needed, not_needed2, p_value = monte_carlo_ks_test(lognorm_data, alpha, x_minimum)
        
        pvalues_list.append(p_value)
        
        if p_value < 0.05:
            numreject += 1
    
    power_stat = numreject / 1000
    
    # Here, we're looking for a high rejection rate, indicating that the test correctly identifies distributions.
    print("Mean p-value:", np.mean(pvalues_list))
    print("Power (correct rejection rate):", power_stat)

# Methodology 3, paragraph 3 simulation.
def simulation_part3():
    print("\nSIMULATION 3: Computational Efficiency Analysis")
    
    # Test all these values for computational performance (runtime is O(n log(n))).
    # Feel free to adjust these to understand the performance further. 
    sample_sizes_fortest = [500, 1000, 2000, 4000]
    montecarlo_nums = [1000, 2000, 5000, 10000]
    
    for n in sample_sizes_fortest:
        print("Testing sample size n =", n)
        test_data = generate_power_law_samples(n, 2.5, 2.0, 15.0)
        alpha, x_min = power_law_mle_alpha(test_data)
        
        for mc_iter in montecarlo_nums:
            start_t = time.time()
            not_needed, not_needed2, not_needed3 = monte_carlo_ks_test(test_data, alpha, x_min) 
            
            elapsed_t = time.time() - start_t
            
            print("MC =", mc_iter, ":", elapsed_t, "seconds")

# Please refer to Analysis, methodology 3 section for results and interpretation.
def analyze_cal_housing_data():
    print("\nAnalyzing REAL data for California Home Value Appreciation Ratios (2019-2023 vs 1990)")
    
    # Read in the actual dataset -- refer to data section to understand
    df = pd.read_csv('data/merged_census_1990_2019_23_california.csv')
    housing_ratios = df['home_value_ratio_2019_23_to_1990'].values
    housing_ratios = housing_ratios[housing_ratios > 0]
    
    # get statistics of the california housing dataset
    print("How many census tracts are common to 1990 AND 2019-2023? ", len(housing_ratios),
          "\nWhat's the mean ratio of housing prices between 1990 and 2019-2023? ", np.mean(housing_ratios),
          "\nWhat's the median ratio of housing prices between 1990 and 2019-2023? ", np.median(housing_ratios),
          "\nMinimum ratio? ", min(housing_ratios),
          "\nMaximum ratio? ", max(housing_ratios))
    
    print("Fit power law to housing ratio data and get MLE + parameters")
    alpha, x_min = power_law_mle_alpha(housing_ratios)
    print("Estimated alpha:", alpha)
    print("xmin:", x_min)
    
    observed_ks_stat = compute_ks_statistic(housing_ratios, alpha, x_min)
    print("KS statistic:", observed_ks_stat)
    
    print()
    print("Running Monte Carlo Hypothesis Test")
    observed_ks_stat, sim_ks_stats, p_val = monte_carlo_ks_test(
        housing_ratios, alpha, x_min
    )
    
    effect_sz = (observed_ks_stat - np.mean(sim_ks_stats)) / np.std(sim_ks_stats)
    
    print()
    # Final results -- does our null hypothesis (ratio data follows power law) hold? 
    print("\nHYPOTHESIS TEST RESULTS",
          "\nNull Hypothesis: Data follows a power law distribution"
          "\nObserved KS statistic:", observed_ks_stat,
          "\nMean simulated KS:", np.mean(sim_ks_stats), 
          "\nStd Dev of simulated KS:", np.std(sim_ks_stats),
          "\np-value:", p_val, 
          "\nEffect size:", effect_sz)
    
    print('Reject Null Hypothesis') if p_val < 0.05 else print('Fail to Reject')

if __name__ == "__main__":
    # On my machine (Apple M2), the entire program takes a very long time to run (~1 hour).
    # Feel free to adjust some of the parameters in the functions above for faster performance. 
    print("METHODOLOGY 3: COMPLETE SIMULATION AND ANALYSIS")
    
    analyze_cal_housing_data()
    simulation_part1()
    simulation_part2()
    simulation_part3()
    
    print("\nANALYSIS COMPLETE")


