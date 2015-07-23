# -*- coding: utf-8 -*-
"""
A module to hold all auxiliary, all-purpose, functions.

Functions contained in module.
------------------------------
- fit_poly(data, degree)
- poly_to_ads_string(coeffs)
- custom_plot(data, xlabel='X axis', ylabel='Y axis', title='Plot title',
              legend=None, mode='linear')

Individual documentation can be accessed by using the following commands:
>>> import elvd_tools
>>> print elvd_tools.<function_name>.__doc__  # or
>>> help(elvd_tools.<function_name>)

Created on Wed Aug 13 16:10:18 2014
@author: elvd

"""

from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt


def fit_poly(data, degree):
    """
    Fits an array of [x, y] data to a polynomial of a specified
    degree. Used with measured I-V data.

    Parameters:
    -----------
    data : numpy.ndarray
        I-V data of one device.
    degree : int
        The degree of polynomial to which the data is to be fitted.

    Returns:
    --------
    fit : numpy.ndarray
        The original x data, bundled with the fitted y data.
    coeffs : numpy.ndarray
        The coefficients of the fitted polynomial, highest order first.

    Notes:
    ------
    Requires an installation of NumPy.

    """

    coeffs = np.polyfit(data[:, 0], data[:, 1], degree)
    fit = np.polyval(coeffs, data[:, 0])
    fit = np.array([data[:, 0], fit])
    fit = fit.T

    return (fit, coeffs)


def poly_to_ads_string(coeffs):
    """
    Converts the numerical representation of a polynomial to a string one, to
    be used in Agilent/Keysight ADS as an SDD element.

    Parameters:
    -----------
    coeffs : numpy.ndarray
        Coefficients of the polynomial to be converted.

    Returns:
    --------
    polynom : string
        The string representation of the polynomial, to be used as the
        non-linear relationship between I and V in a 2-port SDD element.

    """

    coeffs = coeffs[::-1]
    polynom = ['(%e)*((_v1+_v2)^%d)+' % (j, i) for (i, j) in enumerate(coeffs)]
    polynom = ''.join(polynom)  # convert to Agilent ADS SDD format

    return polynom


def custom_plot(data, xlabel='X axis', ylabel='Y axis', title='Plot title',
                legend=None, mode='linear'):
    """
    Plots data, with labels, title, and legend. Used to make sure all graphs
    have the same style. Datapoints must be in columns.

    Parameters:
    -----------
    data : numpy.ndarray
        I-V data of one or more device; alternatively, the measured and fitted
        data of one device.
    xlabel, ylabel : string
        X and Y axis labels.
    title : string
        Plot title.
    legend : array_like, optional
        The lalbes for the different sets of data, to appear in the legend box.
    mode : {'linear', 'log'}, optional
        Scaling of the Y axis.

    Returns:
    --------
    fig : matplotlib.figure.Figure
        A matplotlib figure, containing the plots of the data passed to the
        function.

    Raises:
    -------
    IndexError
        In case there is insufficient data, or data is not organised in
        columns.

    Notes:
    ------
    Requires an installation of NumPy and Matplotlib. Figure is not displayed,
    just created and its parameters set. It is up to the calling function to
    display and/or save the figure.

    Example:
    --------
    >>> import elvd_tools
    >>> data1 = [[0, 0], [1, 1], [2, 2]]
    >>> data2 = [[0, 0], [1, 1], [2, 4]]
    >>> data3 = [[0, 0], [1, 1], [2, 8]]
    >>> data_comb = elvd_tools.np.array([data1, data2, data3])
    >>> label1 = 'Test X label'
    >>> label2 = 'Test Y label'
    >>> title = 'Test Title'
    >>> legend = ['Test item 1', 'Test item 2', 'Test item 3']
    >>> try:
    ...     test_fig = elvd_tools.custom_plot(data_comb, label1, label2,
                                              title, legend)
    ...     elvd_tools.plt.show()
    ... except IndexError as e:
    ...     print e.message

    """

    fig = plt.figure()
    ax1 = fig.add_subplot(111)  # just one plot
    # different colours for the different datasets
    ax1.set_color_cycle(['r', 'k', 'b', 'g', 'c', 'm'])

    if np.ndim(data) == 2:  # one set of data
        if np.size(data, 0) >= np.size(data, 1) and np.size(data, 1) > 1:
            ax1.plot(data[:, 0], data[:, 1], lw=1.0)
        else:
            raise IndexError('Incorrect format. Datapoints must be in columns')
    elif np.ndim(data) == 3:  # two or more sets
        if np.size(data, 1) >= np.size(data, 2) and np.size(data, 2) > 1:
            for datum in data:
                ax1.plot(datum[:, 0], datum[:, 1], lw=1.0)
        else:
            raise IndexError('Incorrect format. Datapoints must be in columns')
    else:
        raise IndexError('Missing data')

    # set labels, title
    ax1.set_yscale(mode)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    ax1.set_title(title)

    if legend is not None:
        ax1.legend(legend, loc='lower left')

    # cosmetic stuff, make it look pretty
    ax1.set_axisbelow(True)
    ax1.grid(which='both', axis='both', color='0.1', ls=':', lw=0.2)
    ax1.tick_params(direction='out', top='off', right='off', width=0.5)

    for spine in ['left', 'top', 'right', 'bottom']:
        ax1.spines[spine].set_linewidth(0.5)

    plt.axhline(y=0, color='0', lw=0.5)
    plt.axvline(x=0, color='0', lw=0.5)

    plt.rc('font', family='serif')

    plt.rc('legend', fontsize=12)
    plt.rc('axes', titlesize=14)
    plt.rc('axes', labelsize=12)
    plt.rc('xtick', labelsize=12)
    plt.rc('ytick', labelsize=12)

    return fig

if __name__ == '__main__':
    print(__doc__)
