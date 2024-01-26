# Other imports and data preparation code remains the same

def portfolio_annualized_sharpe(weights, returns):
    # Function definition remains the same

# Objective function (to be minimized)
def objective_function(weights):
    return -portfolio_annualized_sharpe(weights, df_returns)  # Negative Sharpe Ratio

# Experiment with a different initial guess
np.random.seed(0)  # Set seed for reproducibility
initial_weights = np.random.random(len(positions))
initial_weights /= np.sum(initial_weights)  # Ensure they sum to 1

# Optimization
optimal_weights = minimize(objective_function, initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)

# Display optimized weights
optimized_weights = pd.Series(optimal_weights.x, index=positions)
print(optimized_weights)