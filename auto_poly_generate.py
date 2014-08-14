# -*- coding: utf-8 -*-
"""
A Python translation of a Matlab script used to generate polynomials to
describe the IV curve of RTDs from measured data at DC.

Input parameters:
startdir - starting folder
degree - degree of polynomials

Outputs:
For each folder, a file named autopoly.txt, containing the polynomial
expressions in a format ready to be used in Agilent ADS.

Created on Tue Aug 05 15:23:28 2014
@author: elvd

"""

import os
import numpy as np
import matplotlib.pyplot as plt
import warnings
import elvd_tools


def genpoly(startdir, degree):
    warnings.simplefilter('ignore', np.RankWarning)

    for dirname, subdirlist, filelist in os.walk(startdir):
        os.chdir(dirname)
        gen = (fname for fname in filelist if 'measurement' in fname and
               os.path.splitext(fname)[1] == '.txt')

        for fname in gen:
            data = np.loadtxt(fname, skiprows=1)
            data[:, 1] /= 1e-3  # convert to mA

            coeffs = np.polyfit(data[:, 0], data[:, 1], degree)
            fit = np.polyval(coeffs, data[:, 0])
            fit = np.array([data[:, 0], fit])
            fit = fit.T
            bundle = np.array([data, fit])

            try:
                elvd_tools.custom_plot(data=bundle, xlabel='Voltage, [V]',
                                       ylabel='Current, [mA]', mode='linear',
                                       title='Comparison',
                                       legend=['Measurement', 'Fit'])
                plt.savefig(fname+'.png')
            except IndexError as e:
                print e.message

            coeffs = coeffs[::-1]
            polynom = ['(%e)*((_v1+_v2)^%d)+' % (j, i) for (i, j) in
                       enumerate(coeffs)]
            polynom = ''.join(polynom)  # convert to Agilent ADS SDD format

            with open('autopoly.txt', 'a') as fout:
                fout.write(fname)
                fout.write(': \n')
                fout.write(polynom[:-1])
                fout.write('\n')

if __name__ == '__main__':
    startdir = r'D:\RTD_measurements'
    degree = 60

    genpoly(startdir, degree)

    plt.close('all')
