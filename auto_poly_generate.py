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


def genpoly(startdir, degree):
    for dirname, subdirlist, filelist in os.walk(startdir):
        print 'In folder: %s' % dirname
        os.chdir(dirname)
        gen = (fname for fname in filelist if 'measurement' in fname and
               '.txt' in fname)
        for fname in gen:
            print 'Processing file: %s' % fname
            data = np.loadtxt(fname, skiprows=1)
            coeffs = np.polyfit(data[:, 0], data[:, 1], degree)
            plt.figure()
            plt.plot(data[:, 0], data[:, 1])
            plt.plot(data[:, 0], np.polyval(coeffs, data[:, 0]))
            plt.legend(['Measurement', 'Fit'], loc='upper left')
            plt.savefig(fname+'.png')
            coeffs = coeffs[::-1]
            polynom = ['(%e)*((_v1+_v2)^%d)+' % (j, i) for (i, j) in
                       enumerate(coeffs)]
            polynom = ''.join(polynom)
            with open('autopoly.txt', 'a') as fout:
                fout.write(fname)
                fout.write(': \n')
                fout.write(polynom[:-1])
                fout.write('\n')

if __name__ == '__main__':
    startdir = r'D:\RTD_measurements'
    degree = 60

    genpoly(startdir, degree)
