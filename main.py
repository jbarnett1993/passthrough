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