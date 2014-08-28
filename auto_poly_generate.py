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
import iv_manipulate


def genpoly(startdir, degree):
    warnings.simplefilter('ignore', np.RankWarning)

    for dirname, subdirlist, filelist in os.walk(startdir):
        os.chdir(dirname)
        gen = (fname for fname in filelist if
               os.path.splitext(fname)[1] == '.ivm')

        polynoms = {}

        for fname in gen:
            data = np.loadtxt(fname, skiprows=1)
            data[:, 1] /= 1e-3  # convert to mA
            data = iv_manipulate.make_symmetric(data, quadrant='neg')
#            data = iv_manipulate.extract_region(data, 'pdr')
#            data = iv_manipulate.scale_iv(data, factor=0.1)

            fit, polynom = elvd_tools.fitpoly(data, degree)
            bundle = np.array([data, fit])

            name, ext = os.path.splitext(fname)
            name = name.split('_')
            device_id = ' '.join(name[1:3])
            plot_title = ' '.join([device_id, 'Comparison'])

            try:
                elvd_tools.custom_plot(data=bundle,
                                       xlabel='Voltage, [V]',
                                       ylabel='Current, [mA]',
                                       mode='linear',
                                       title=plot_title,
                                       legend=['Measurement', 'Fit'])
                name = '_'.join(name[1:4])
                name = '_'.join([name, 'sym_neg'])
                name = '.'.join([name, 'jpg'])
                plt.savefig(name, dpi=600)
                plt.close()
            except IndexError as e:
                print e.message

            polynoms[device_id] = polynom

        if polynoms:
            with open(dirname+'_autopoly_sym_neg.txt', 'w') as fout:
                for device, iv in polynoms.items():
                    fout.write(device)
                    fout.write(': \n')
                    fout.write(iv[:-1])
                    fout.write('\n')

if __name__ == '__main__':
    startdir = r'D:\RTD_modified_iv\N1014'
    degree = 60

    genpoly(startdir, degree)

    plt.close('all')
