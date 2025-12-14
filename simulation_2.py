import numpy as np
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import mean_squared_error

np.random.seed(406)

# ----------------------------
# Kernel smoothing (Nadaraya–Watson)
# ----------------------------
def gaussian_kernel(u):
    return np.exp(-0.5 * u**2) / np.sqrt(2 * np.pi)

def nadaraya_watson(x0, X, Y, h):
    weights = gaussian_kernel((X - x0) / h)
    return np.sum(weights * Y) / np.sum(weights)

# ----------------------------
# Cross-validation for bandwidth selection
# ----------------------------
def select_bandwidth(X, Y, bandwidth_grid):
    loo = LeaveOneOut()
    cv_errors = []

    for h in bandwidth_grid:
        preds = []
        true_vals = []

        for train_idx, test_idx in loo.split(X):
            X_train, X_test = X[train_idx], X[test_idx]
            Y_train, Y_test = Y[train_idx], Y[test_idx]

            pred = nadaraya_watson(X_test[0], X_train, Y_train, h)
            preds.append(pred)
            true_vals.append(Y_test[0])

        cv_errors.append(mean_squared_error(true_vals, preds))

    return bandwidth_grid[np.argmin(cv_errors)]

# ----------------------------
# Simulation parameters
# ----------------------------
n_years = 30
years = np.linspace(1990, 2020, n_years)
n_sims = 1000
noise_sd = 20000

bandwidth_grid = np.linspace(1, 6, 10)

bias_list = []
mse_list = []
coverage_list = []

# ----------------------------
# True smooth mean function (housing prices over time)
# ----------------------------
def true_mean_function(t):
    return 150000 + 3000 * (t - 1990) + 20000 * np.sin((t - 1990) / 6)

true_mean = true_mean_function(years)

# ----------------------------
# Simulation loop
# ----------------------------
for sim in range(n_sims):

    # Generate synthetic housing prices
    observed_prices = true_mean + np.random.normal(0, noise_sd, size=n_years)

    # Select bandwidth via CV
    best_h = select_bandwidth(years, observed_prices, bandwidth_grid)

    # Smoothed estimate
    smoothed = np.array([
        nadaraya_watson(t, years, observed_prices, best_h)
        for t in years
    ])

    # Bootstrap confidence intervals
    B = 300
    boot_estimates = np.zeros((B, n_years))

    for b in range(B):
        idx = np.random.choice(n_years, n_years, replace=True)
        Xb = years[idx]
        Yb = observed_prices[idx]

        boot_estimates[b, :] = [
            nadaraya_watson(t, Xb, Yb, best_h)
            for t in years
        ]

    lower = np.percentile(boot_estimates, 2.5, axis=0)
    upper = np.percentile(boot_estimates, 97.5, axis=0)

    # Operating characteristics
    bias = np.mean(smoothed - true_mean)
    mse = np.mean((smoothed - true_mean) ** 2)
    coverage = np.mean((true_mean >= lower) & (true_mean <= upper))

    bias_list.append(bias)
    mse_list.append(mse)
    coverage_list.append(coverage)

# ----------------------------
# Report results
# ----------------------------
print("=== SIMULATION RESULTS: METHOD 2 ===")
print(f"Average Bias: {np.mean(bias_list):.2f}")
print(f"Average MSE: {np.mean(mse_list):.2f}")
print(f"Coverage Probability (95% CI): {np.mean(coverage_list):.3f}")