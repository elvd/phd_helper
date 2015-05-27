# -*- coding: utf-8 -*-
"""
A Python translation of a Matlab script used to generate polynomials to
describe the I-V curve of RTDs from measured data at DC.

The script traverses a tree structure, and processes all files with a
specified extension. The format of the files themselves is preferred to be
one datapoint per line. The number of header lines to skip is a parameter that
is specified as well.

After reading in the contents of a data file, further manipulations are
possible, using the functions from the iv_manipulate module. To do so,
manually uncomment / comment the manipulations you want to make.

For each file, a graph is drawn, containing both the measured data, and the
result of a polynomial fit to it. Furthermore, a polynomial in format suitable
for use in Agilent/Keysight ADS is created.

For each folder, these polynomials are saved in a txt file, which has the word
`autopoly` in it.

Work is in progress to move to command-line specified parameters and more
general form of the function.

Created on Tue Aug 05 15:23:28 2014
@author: elvd

"""

from __future__ import print_function
import os
import numpy as np
import matplotlib.pyplot as plt
import warnings
import elvd_tools
import iv_manipulate


startdir = r'D:\projects\phd_helper\rtd\hamza'
degree = 60

warnings.simplefilter('ignore', np.RankWarning)

for dirname, subdirlist, filelist in os.walk(startdir):
    os.chdir(dirname)
    gen = (fname for fname in filelist if
           os.path.splitext(fname)[1] == '.ivm')

    polynoms = dict()

    for fname in gen:
        data = np.loadtxt(fname, skiprows=1)
        data[:, 1] /= 1e-3  # convert to mA
        data = iv_manipulate.make_symmetric(data, quadrant='neg')
        data = iv_manipulate.extract_region(data, 'pdr')
        data = iv_manipulate.scale_iv(data, factor=0.1)

        fit, coeffs = elvd_tools.fit_poly(data, degree)
        polynom = elvd_tools.poly_to_ads_string(coeffs)
        bundle = np.array([data, fit])

        name, ext = os.path.splitext(fname)
        name = name.split('_')
        device_id = ' '.join(name[1:3])
        plot_title = ' '.join([device_id, 'sample', name[3]])

        try:
            elvd_tools.custom_plot(data=data,
                                   xlabel='Voltage, [V]',
                                   ylabel='Current, [mA]',
                                   mode='linear',
                                   title=plot_title)
            name = '_'.join(name[1:4])
            name = '_'.join([name, 'sym_neg'])
            name = '.'.join([name, 'jpg'])
            plt.savefig(name, dpi=600)
            plt.close()
        except IndexError as e:
            print(e.message)

        polynoms[device_id] = polynom

    if polynoms:
        with open(dirname+'_autopoly_sym_neg2.txt', 'w') as fout:
            for device, iv in polynoms.items():
                fout.write(device)
                fout.write(': \n')
                fout.write(iv[:-1])
                fout.write('\n')

plt.close('all')
