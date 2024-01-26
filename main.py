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


'''
Positions   AUDUSD Curncy  USDCAD Curncy  USDCHF Curncy  EURUSD Curncy  GBPUSD Curncy  USDJPY Curncy  USDNOK Curncy  NZDUSD Curncy  USDSEK Curncy
date
2023-01-26            NaN            NaN            NaN            NaN            NaN            NaN            NaN            NaN            NaN    
2023-01-27       0.006076       0.001694      -0.003878       0.002066      -0.003120      -0.000565       0.005632      -0.003022       0.000619    
2023-01-30       0.002903       0.001268      -0.003219      -0.001519      -0.000828       0.000808      -0.004220      -0.001940       0.002318    
2023-01-31       0.006341      -0.004786       0.003305       0.003586       0.000184      -0.001776       0.004854       0.008069      -0.000617    
2023-02-01       0.006426      -0.002970      -0.002770      -0.006497       0.000645      -0.002993      -0.001687       0.004449      -0.004012    






'''