import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.utils import resample

# ----------------------------
# Load and prepare data
# ----------------------------
df = pd.read_csv("merged_census_1990_2019_23_california.csv")

# Outcome variable 
y = df["home_value_ratio_2019_23_to_1990"]

# Choose predictors (example set—you can modify)
X = df[[
    "poverty_rate",
    "race_white",
    "race_asian_pacific_islander",
    "housing_occupied",
    "occupancy_rate",
    "total_housing_units",
    "median_home_value_1990"
]]

# Add intercept
X = sm.add_constant(X)

# ----------------------------
# Parametric linear regression
# ----------------------------
model = sm.OLS(y, X).fit()
print("\n=== PARAMETRIC REGRESSION RESULTS ===")
print(model.summary())

# Extract test statistic (coefficient of poverty_rate)
test_stat_obs = model.params["poverty_rate"]
print("\nObserved coefficient for poverty_rate:", test_stat_obs)

# ----------------------------
# Permutation Test
# ----------------------------
def perm_test(X, y, variable, n_perm=5000):
    """Permutation test for regression coefficient."""
    coeffs = []
    
    for _ in range(n_perm):
        y_perm = np.random.permutation(y)
        model_perm = sm.OLS(y_perm, X).fit()
        coeffs.append(model_perm.params[variable])
    
    coeffs = np.array(coeffs)
    
    p_val = np.mean(np.abs(coeffs) >= np.abs(test_stat_obs))
    
    return p_val, coeffs

p_value_perm, perm_dist = perm_test(X, y, "poverty_rate")
print("\n=== PERMUTATION TEST ===")
print("Permutation p-value:", p_value_perm)