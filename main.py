from scipy.stats import norm

# ... [previous code remains unchanged] ...

# Calculate D1
T = NumberOfDaysBetween/365  # Time to maturity in years
d1 = (np.log(Spot / Strike) + (UsdRate - EurRate + Sigma**2 / 2) * T) / (Sigma * np.sqrt(T))
# Calculate ND1
nd1 = norm.cdf(d1)

# Calculate D2
d2 = d1 - Sigma * np.sqrt(T)
# Calculate ND2
nd2 = norm.cdf(d2)

# Print the results
print("D1 is:", d1)
print("ND1 is:", nd1)
print("D2 is:", d2)
print("ND2 is:", nd2)

# ... [rest of your code] ...