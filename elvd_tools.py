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

Created on Wed Aug 13 16:10:18 2014
@author: elvd
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr


def custom_plot(data, xlabel='X axis', ylabel='Y axis', title='Plot title',
                legend=None, mode='linear'):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_color_cycle(['r', 'k', 'b', 'g', 'c'])

    if np.ndim(data) == 2:
        if np.size(data, 0) >= np.size(data, 1) and np.size(data, 1) > 1:
            ax1.plot(data[:, 0], data[:, 1], lw=2)
        else:
            raise IndexError('Incorrect format. Datapoints must be in columns')
    elif np.ndim(data) == 3:
        if np.size(data, 1) >= np.size(data, 2) and np.size(data, 2) > 1:
            for datum in data:
                ax1.plot(datum[:, 0], datum[:, 1], lw=2)
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

    if mode == 'linear':
        ax1.xaxis.set_minor_locator(tkr.AutoMinorLocator(n=2))
        ax1.yaxis.set_minor_locator(tkr.AutoMinorLocator(n=2))

    ax1.grid(which='both', axis='both', color='0.1', ls=':', lw=0.75)

    plt.axhline(y=0, color='0.1', lw=1)
    plt.axvline(x=0, color='0.1', lw=1)

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
