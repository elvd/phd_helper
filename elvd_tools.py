# -*- coding: utf-8 -*-
"""


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
        ax1.plot(data[:, 0], data[:, 1], lw=2)
    elif np.ndim(data) == 3:
        for datum in data:
            ax1.plot(datum[:, 0], datum[:, 1], lw=2)
    else:
        raise IndexError

    ax1.set_yscale(mode)

    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    ax1.set_title(title)

    if legend is not None:
        ax1.legend(legend, loc='upper left')

    ax1.xaxis.set_minor_locator(tkr.AutoMinorLocator(n=2))
    ax1.yaxis.set_minor_locator(tkr.AutoMinorLocator(n=2))
    ax1.grid(which='both', axis='both', color='0.1', ls=':', lw=0.75)

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
    except IndexError:
        print 'Insufficient data'
