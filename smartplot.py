import matplotlib.pylab as _plt
from   matplotlib import rc
import pandas as pd
import numpy as np
import statsmodels.api as sm
import warnings
from   IPython.display import display


# Options
params = {
    'text.usetex'         : True,
    'text.latex.unicode'  : True,
    'text.latex.preamble' : r"\usepackage[T2A]{fontenc}",
    'font.size'           : 20,
    'font.family'         : 'lmodern',
    'figure.figsize'      : (16, 9),
    }

_plt.rcParams.update(params)


def addplot(
        input  = "data.csv",
        units  = "",
        label  = None,
        labelx = 0.05,
        labely = 0.9,
        xerr   = None,
        yerr   = None,
        number = 1
        ):

    # Iterative wrapper
    if number:
        # Initialize attributes (static)
        addplot._row  = 0
        addplot._data = pd.read_csv(input, engine='python', header=None)
        addplot._axes = _plt.subplots()[1]

        for count in range(number):
            addplot(input=input, xerr=xerr, yerr=yerr, number=None)

        # Destroy 'em'
        del addplot._row, addplot._data, addplot._axes
        return

    # Load data & calculate ranges
    x = np.array(addplot._data[  addplot._row  ])
    y = np.array(addplot._data[addplot._row + 1])

    xmin, xmax = min(addplot._data[  addplot._row  ]), max(addplot._data[  addplot._row  ])
    ymin, ymax = min(addplot._data[addplot._row + 1]), max(addplot._data[addplot._row + 1])

    addplot._row += 2

    if xerr:
        xerr  = np.array(addplot._data[addplot._row])
        addplot._row += 1
    if yerr:
        yerr  = np.array(addplot._data[addplot._row])
        addplot._row += 1

    # Fit
    t = sm.add_constant(x, prepend=False)
    model  = sm.OLS(y, t)
    result = model.fit()
    s,     i     = result.params
    s_err, i_err = result.bse

    # Show result
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        display(result.summary().tables[1])

    # Heuristics, starting from (0, 0) when not too much empty space
    def need_0(l, r):
        return True if (r > 0 and l > 0 and l/r < 0.2) else False

    if need_0(xmin, xmax) and need_0(ymin, ymax):
        xmin, ymin = 0, 0

    # Plot
    _plt.plot(x, y, linestyle='None', marker='o', color='r', markersize = 7)
    _plt.plot(np.linspace(xmin, xmax), np.linspace(xmin, xmax)*s + i, 'k--', linewidth=0.5)
    if xerr or yerr:
        _plt.errorbar(x, y, xerr=xerr, yerr=yerr)

    # Label text
    if label:
        label = r"$K=(" + "{:.3f}".format(s) + r"\pm" + "{:.3f}".format(s_err) + ")$ " + units
        addplot._axes.text(labelx, labely, label, transform=addplot._axes.transAxes, bbox={'facecolor':'white', 'edgecolor':'black', 'pad':10})

    # Grid
    addplot._axes.grid(color='#e5e5e5', linestyle='--', linewidth=0.2)


def axes(xlabel=None, ylabel=None):
    _plt.xlabel(xlabel)
    _plt.ylabel(ylabel)


def show(output="graph.png", dpi=300, save=False):
    if save:
        _plt.savefig(
            output,
            dpi = dpi,
            bbox_inches = 'tight'  # Plot occupies maximum of available space
        )
    _plt.show()


def clear():
    _plt.cla()
    _plt.clf()
