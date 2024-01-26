def annualized_sharpe_ratio(data, breakdown=False):
    if not isinstance(data, pd.Series):
        data = data[data.columns[0]]
    values = np.asarray(data.values)
    r = values[1:] / values[:-1] - 1
    total_return = values[-1] / values[0]
    nb_years = (data.index[-1] - data.index[0]).days / 365
    std_r = np.std(r)
    annual_r = total_return ** (1 / nb_years) - 1
    annual_std = (std_r * np.sqrt(252))
    if not breakdown:
        if annual_std == 0:
            return np.nan
        return annual_r / annual_std
    if annual_std == 0:
        return np.nan, annual_r, annual_std
    return annual_r / annual_std, annual_r, annual_std
    
    def portfolio_annualized_sharpe(weights, returns):
    """
    Calculate the annualized Sharpe ratio of a portfolio based on given weights and historical returns.
    """
    portfolio_returns = np.dot(returns, weights)
    portfolio_total_return = np.prod(1 + portfolio_returns) - 1
    nb_years = (returns.index[-1] - returns.index[0]).days / 365
    portfolio_std_dev = np.std(portfolio_returns)
    annual_r = (portfolio_total_return + 1) ** (1 / nb_years) - 1
    annual_std = portfolio_std_dev * np.sqrt(252)

    if annual_std == 0:
        return np.nan
    return annual_r / annual_std

# You can use this function in your optimization process:
# Objective function (to be minimized)
def objective_function(weights):
    return -portfolio_annualized_sharpe(weights, df_returns)

# Rest of the optimization code remains the same

from scipy.optimize import minimize

# Optimization constraints and bounds
constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]  # Sum of weights must be 1
bounds = [(-0.20, 0.20) for _ in range(len(positions))]  # Long/short constraints

# Objective function (to be minimized)
def objective_function(weights):
    return -portfolio_annualized_sharpe(weights, df_returns)

# Initial guess for weights
initial_weights = np.array([1. / len(positions)] * len(positions))

# Optimization
optimal_weights = minimize(objective_function, initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)

# Display optimized weights
optimized_weights = pd.Series(optimal_weights.x, index=positions)
print(optimized_weights)
