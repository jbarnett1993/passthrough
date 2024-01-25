# FUNCTION TO MAKE A SCATTER PLOT WITH EQUAL AXIS LENGTHS

def plot_equal_lengths_scatters(data, x_name, y_name):
    """
    This function makes a scatter plot. It also draws dotted lines to make the x-axis and y-axis more easy to see.
    
    data: pandas DataFrame with dates on the index, and x- and y-axes names as columns. 
    This is the data for the scatter plot.
    x_name: String; the column name of the x-axis.
    y_name: String; the column name of the y-axis.
    
    Return: The matplotlib.Figure and matplotlib.axes.Axes for the plot.
    """
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.grid(visible=True, linestyle='dashed', lw=0.35, color='lightgray')
    ax.axhline(y=0, color='black', linestyle=(0, (10, 6)), lw=0.5)
    ax.axvline(x=0, color='black', linestyle=(0, (10, 6)), lw=0.5)
    ax.scatter(x=data[x_name], y=data[y_name], s=15, marker='o', c='gainsboro', edgecolors='darkgrey')
    ax.set_xlabel(xlabel=x_name)
    ax.set_ylabel(ylabel=y_name)

    xlim_left, xlim_right = ax.get_xlim()
    ylim_bottom, ylim_top = ax.get_ylim()
    
    lim = np.max(np.abs(np.array([xlim_left, xlim_right, ylim_bottom, ylim_top])))
    
    ax.set_xlim(left=-lim, right=lim)
    ax.set_ylim(bottom=-lim, top=lim)
    
    return fig, ax


# FUNCTION TO MAKE A SCATTER PLOT

def plot_scatters(data, x_name, y_name, rounding=0.05):
    """
    This function makes a scatter plot. It also draws dotted lines to make the x-axis and y-axis more easy to see.
    
    data: pandas DataFrame with dates on the index, and x- and y-axes names as columns. 
    This is the data for the scatter plot.
    x_name: String; the column name of the x-axis.
    y_name: String; the column name of the y-axis.
    rounding: Float used to decide how to round off axes' limits.
    
    Return: The matplotlib.Figure and matplotlib.axes.Axes for the plot.
    """
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.grid(visible=True, linestyle='dashed', lw=0.35, color='lightgray')
    ax.axhline(y=0, color='black', linestyle=(0, (10, 6)), lw=0.5)
    ax.axvline(x=0, color='black', linestyle=(0, (10, 6)), lw=0.5)
    ax.scatter(x=data[x_name], y=data[y_name], s=15, marker='o', c='gainsboro', edgecolors='darkgrey')
    ax.set_xlabel(xlabel=x_name)
    ax.set_ylabel(ylabel=y_name)

    xlim_left = math.floor(data[x_name].min() / rounding) * rounding
    xlim_right = math.ceil(data[x_name].max() / rounding) * rounding
    ylim_bottom = math.floor(data[y_name].min() / rounding) * rounding
    ylim_top = math.ceil(data[y_name].max() / rounding) * rounding

    ax.set_xlim(left=xlim_left, right=xlim_right)
    ax.set_ylim(bottom=ylim_bottom, top=ylim_top)
    
    return fig, ax