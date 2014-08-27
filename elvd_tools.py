# -*- coding: utf-8 -*-
"""
A module to hold all auxiliary, all-purpose, functions. Currently implemented:
- custom_plot
    Purpose: plots input data, with labels, title, and legend. Used to make
    sure all graphs have the same style.
    Inputs:
        - data: data to be plotted. X and y data must be in separate columns,
          with individual datapoints in every row. If a 3D object, first index
          denotes how many sets of data there are. All are plotted on the same
          graph.
        - xlabel: X axis label.
        - ylabel: Y axis label.
        - title: Plot title, just one for the individual graph.
        - legend: A list of strings, for graph legend.
        - mode: 'linear' or 'log', specifies Y axis scaling.
    Outputs:
        - a matplotlib.pyplot.figure() object.

-fitpoly
    Purpose: fits an array of [x, y] data to a polynomial of a specified
    degree. Used to on measured I-V data in order to use it for simulations in
    Agilent ADS.
    Inputs:
        - data: a 2D NumPy array, with x and y data in separate columns.
        - degree: the desired degree of the fitted polynomial
    Outputs:
        - fit: the result of applying the fitted polynomial over the x data.
        - polynom: a string representation of the fitted polynomial, in format
        suitable for use in Agilent ADS Symbolically-Defined Device.

Created on Wed Aug 13 16:10:18 2014
@author: elvd
"""

import numpy as np
import matplotlib.pyplot as plt


def fitpoly(data, degree):
    coeffs = np.polyfit(data[:, 0], data[:, 1], degree)
    fit = np.polyval(coeffs, data[:, 0])
    fit = np.array([data[:, 0], fit])
    fit = fit.T

    coeffs = coeffs[::-1]
    polynom = ['(%e)*((_v1+_v2)^%d)+' % (j, i) for (i, j) in enumerate(coeffs)]
    polynom = ''.join(polynom)  # convert to Agilent ADS SDD format

    return fit, polynom


def custom_plot(data, xlabel='X axis', ylabel='Y axis', title='Plot title',
                legend=None, mode='linear'):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_color_cycle(['r', 'k', 'b', 'g', 'c'])

    if np.ndim(data) == 2:
        if np.size(data, 0) >= np.size(data, 1) and np.size(data, 1) > 1:
            ax1.plot(data[:, 0], data[:, 1], lw=1.0)

#            xlim_max = np.max(data[:, 0])
#            xlim_min = np.min(data[:, 0])
#
#            ylim_max = np.max(data[:, 1])
#            ylim_min = np.min(data[:, 1])
        else:
            raise IndexError('Incorrect format. Datapoints must be in columns')
    elif np.ndim(data) == 3:
        if np.size(data, 1) >= np.size(data, 2) and np.size(data, 2) > 1:
            for datum in data:
                ax1.plot(datum[:, 0], datum[:, 1], lw=1.0)

#            xlim_max = np.max(data[:, :, 0])
#            xlim_min = np.min(data[:, :, 0])
#
#            ylim_max = np.max(data[:, :, 1])
#            ylim_min = np.min(data[:, :, 1])
        else:
            raise IndexError('Incorrect format. Datapoints must be in columns')
    else:
        raise IndexError('Missing data')

    ax1.set_yscale(mode)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    ax1.set_title(title)

    if legend is not None:
        ax1.legend(legend, loc='upper left')

    ax1.set_axisbelow(True)
    ax1.grid(which='both', axis='both', color='0.1', ls=':', lw=0.2)
    ax1.tick_params(direction='out', top='off', right='off', width=0.5)

    for spine in ['left', 'top', 'right', 'bottom']:
        ax1.spines[spine].set_linewidth(0.5)

    plt.axhline(y=0, color='0', lw=0.5)
    plt.axvline(x=0, color='0', lw=0.5)

    plt.rc('font', family='serif')
    plt.rc('font', serif='Times New Roman')
    plt.rc('legend', fontsize=8)
    plt.rc('axes', titlesize=10)
    plt.rc('axes', labelsize=8)
    plt.rc('xtick', labelsize=8)
    plt.rc('ytick', labelsize=8)

#    xlim_max = np.int(np.ceil(xlim_max))
#    xlim_min = np.int(np.floor(xlim_min))
#    plt.xlim(xmax=xlim_max)
#    plt.xlim(xmin=xlim_min)
#
#    if ylim_max <= 5:
#        ymax_clip = 5
#    else:
#        ymax_clip = 10
#    ylim_max = np.round(float(ylim_max) / ymax_clip) * ymax_clip
#
#    if ylim_min >= -5:
#        ymin_clip = -5
#    else:
#        ymin_clip = -10
#    ylim_min = np.round(float(ylim_min) / ymin_clip) * ymin_clip
#
#    plt.ylim(ymax=ylim_max)
#    plt.ylim(ymin=ylim_min)

    return fig

if __name__ == '__main__':
    data1 = [[0, 0], [1, 1], [2, 2]]
    data2 = [[0, 0], [1, 1], [2, 4]]
    data3 = [[0, 0], [1, 1], [2, 8]]

    data_comb = np.array([data1, data2, data3])

    label1 = 'Test X label'
    label2 = 'Test Y label'
    title = 'Test Title'
    legend = ['Test item 1', 'Test item 2', 'Test item 3']

    try:
        test_fig = custom_plot(data_comb, label1, label2, title, legend)
        plt.show()
    except IndexError as e:
        print e.message
