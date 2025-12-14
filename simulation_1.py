import numpy as np
import statsmodels.api as sm

# ----------------------------
# Simulation parameters
# ----------------------------
n_samples = 100      # neighborhoods per iteration
n_iter = 1000        # number of simulations
beta0 = 1.0
beta1_alt = 0.5      # effect for power simulations
beta2 = 0.3

alpha = 0.05

# Collect results
type1_errors = 0
powers = 0

# ----------------------------
# Simulation loop
# ----------------------------
for i in range(n_iter):
    
    # Generate synthetic predictors similar to data ranges
    poverty_rate = np.random.uniform(0, 0.4, n_samples)
    housing_occupied = np.random.uniform(100, 5000, n_samples)
    
    # ----------------------------
    # Type I Error Simulation (β1 = 0)
    # ----------------------------
    y_null = beta0 + 0 * poverty_rate + beta2 * housing_occupied + np.random.normal(0, 1, n_samples)
    X_null = sm.add_constant(np.column_stack([poverty_rate, housing_occupied]))
    model_null = sm.OLS(y_null, X_null).fit()
    
    pval_null = model_null.pvalues[1]  # p-value for poverty_rate
    
    if pval_null < alpha:
        type1_errors += 1
    
    # ----------------------------
    # Power Simulation (β1 = beta1_alt ≠ 0)
    # ----------------------------
    y_alt = beta0 + beta1_alt * poverty_rate + beta2 * housing_occupied + np.random.normal(0, 1, n_samples)
    X_alt = sm.add_constant(np.column_stack([poverty_rate, housing_occupied]))
    model_alt = sm.OLS(y_alt, X_alt).fit()
    
    pval_alt = model_alt.pvalues[1]
    
    if pval_alt < alpha:
        powers += 1

# ----------------------------
# Final simulation results
# ----------------------------
type1_error_rate = type1_errors / n_iter
power_rate = powers / n_iter

print("\n=== SIMULATION RESULTS ===")
print("Type I Error Rate:", type1_error_rate)
print("Power:", power_rate)