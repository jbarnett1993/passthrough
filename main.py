 def bond_price(C, F, r, n):
    """
    Calculate the bond price.
    
    Parameters:
    C: Periodic coupon payment
    F: Par value or face value of the bond
    r: Periodic yield
    n: Number of periods to maturity
    
    Returns:
    Bond price
    """
    return C * (1 - (1 + r)**-n) / r + F * (1 + r)**-n


def bond_convexity(P, C, F, r, n, delta_y=0.01):
    """
    Calculate the convexity of a bond.
    
    Parameters:
    P: Bond's current price
    C: Periodic coupon payment
    F: Par value or face value of the bond
    r: Periodic yield
    n: Number of periods to maturity
    delta_y: Change in yield (default is 0.01 or 1%)
    
    Returns:
    Convexity of the bond
    """
    # Calculate bond price for an upward change in yield
    P_plus = bond_price(C, F, r + delta_y, n)
    
    # Calculate bond price for a downward change in yield
    P_minus = bond_price(C, F, r - delta_y, n)
    
    # Calculate convexity
    convexity = (P_plus + P_minus - 2 * P) / (P * delta_y**2)
    
    return convexity


def annual_convexity(convexity, n_periods_in_year):
    """
    Annualize the convexity.
    
    Parameters:
    convexity: Convexity of the bond
    n_periods_in_year: Number of periods in a year (e.g., 2 for semi-annual)
    
    Returns:
    Annual convexity
    """
    return convexity * n_periods_in_year**2


# Example Usage
P = 950  # current bond price
C = 40  # periodic coupon payment (e.g., semi-annual coupon of $40)
F = 1000  # par value
r = 0.05  # current yield for semi-annual period, so 5% annually would be 0.05/2 = 0.025 for semi-annual
n = 10  # number of periods to maturity (e.g., 5 years for semi-annual payments)

convexity = bond_convexity(P, C, F, r, n)
print(f"Convexity: {convexity}")

annualized_convexity = annual_convexity(convexity, 2)  # assuming semi-annual periods
print(f"Annualized Convexity: {annualized_convexity}")