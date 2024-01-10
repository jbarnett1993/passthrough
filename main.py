import pandas as pd
import numpy as np
import tia.bbg.datamgr as dm
import tia.analysis.ta as ta
import tia.analysis.model as model
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Define the start and end dates for the data
start_date = (datetime.today() - relativedelta(years=2)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')

# Define the list of dependent variables and the independent variable
dependent_variables = [".BTP_BUND Index"]
independent_variable = ".EUIG_BUN Index"

# Initialize the data manager
mgr = dm.BbgDataManager()
mgr.sid_result_mode = 'frame'

# Get the historical data for the dependent and independent variables
independent_data = mgr[independent_variable].get_historical(['PX_LAST'], start_date, end_date)

independent_data = independent_data / independent_data.shift(1)

# Loop over the dependent variables
for dependent_variable in dependent_variables:
    # Get the historical data for the current dependent variable
    dependent_data = mgr[dependent_variable].get_historical(['PX_LAST'], start_date, end_date)

    dependent_data = dependent_data / dependent_data.shift(1)

    # Merge the data for the current dependent variable with the independent data
    combined_data = pd.merge(dependent_data, independent_data, left_index=True, right_index=True, suffixes=('_dependent', '_independent'))

    # Remove rows with missing data
    combined_data = combined_data.dropna()

    # Define the independent and dependent variables for the regression
    X = combined_data['PX_LAST_independent']
    y = combined_data['PX_LAST_dependent']

    # Rename the columns of the data frame
    X.name = independent_variable
    y.name = dependent_variable

    # Add a constant term to the independent variables
    X = sm.add_constant(X)

    # Fit the regression model
    model = sm.OLS(y, X).fit()

    print(model.summary())
