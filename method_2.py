import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV, LeaveOneOut
from sklearn.neighbors import KernelDensity
import matplotlib.pyplot as plt

# Load your data
df = pd.read_csv("merged_census_1990_2019_23_california.csv")

# Use median home values; you might want to reshape for annual values if needed
# Here we assume 1990 values and 2019-23 aggregate value
# We'll create a 'year' array for smoothing
df_long = df.melt(
    id_vars=['GISJOIN', 'STATE', 'TRACTA'],
    value_vars=['median_home_value_1990', '2019-23_value'],
    var_name='Year', value_name='Median_Home_Value'
)

# Map year names to numeric values
year_map = {'median_home_value_1990': 1990, '2019-23_value': 2021}  # midpoint for 2019-23
df_long['Year'] = df_long['Year'].map(year_map)

# Nadaraya-Watson smoothing function
def nadaraya_watson(x_eval, x, y, bandwidth):
    # Ensure x_eval is scalar
    x_eval = np.atleast_1d(x_eval)
    weights = np.exp(-0.5 * ((x_eval[:, None] - x[None, :])/bandwidth)**2)
    weights /= weights.sum(axis=1)[:, None]
    # Weighted average
    y_pred = weights @ y
    # If x_eval was scalar, return scalar
    return y_pred[0] if y_pred.size == 1 else y_pred

# Bandwidth selection using leave-one-out cross-validation
X = df_long['Year'].values
y = df_long['Median_Home_Value'].values

bandwidths = np.linspace(1, 15, 15)
loo = LeaveOneOut()
best_bandwidth = None
best_mse = np.inf

for bw in bandwidths:
    errors = []
    for train_index, test_index in loo.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        y_pred = nadaraya_watson(X_test, X_train, y_train, bw)
        errors.append((y_test - y_pred)**2)
    mse = np.mean(errors)
    if mse < best_mse:
        best_mse = mse
        best_bandwidth = bw

print(f"Selected bandwidth: {best_bandwidth}")

# Apply Nadaraya-Watson smoothing
years_unique = np.sort(df_long['Year'].unique())
smoothed_values = np.array([nadaraya_watson(years_unique[i], X, y, best_bandwidth)
                            for i in range(len(years_unique))])

# Bootstrap for confidence intervals
n_boot = 1000
boot_estimates = np.zeros((n_boot, len(years_unique)))

np.random.seed(42)
for i in range(n_boot):
    sample_idx = np.random.choice(len(df_long), len(df_long), replace=True)
    X_sample = X[sample_idx]
    y_sample = y[sample_idx]
    boot_estimates[i, :] = [nadaraya_watson(years_unique[j], X_sample, y_sample, best_bandwidth)
                            for j in range(len(years_unique))]

ci_lower = np.percentile(boot_estimates, 2.5, axis=0)
ci_upper = np.percentile(boot_estimates, 97.5, axis=0)

# Plot results
plt.figure(figsize=(8,5))
plt.plot(years_unique, smoothed_values, label="Smoothed Median Home Value", color='blue')
plt.fill_between(years_unique, ci_lower, ci_upper, color='blue', alpha=0.3, label="95% CI")
plt.scatter(X, y, color='gray', alpha=0.5, s=10, label="Observed Data")
plt.xlabel("Year")
plt.ylabel("Median Home Value")
plt.title("Smoothed Median Home Values with Bootstrap 95% CI")
plt.legend()
plt.show()