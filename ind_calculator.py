# -*- coding: utf-8 -*-
"""
A quick script to calculate the parameters of a transmission line, used to
represent an inductive element.

Input parameters:
ind - inductance in pH
freq - centre frequency in GHz
er - effective dielectric constant of substrate material
z0l - desired impedance of the transmission line

Outputs:
l_elec - electrical length of an ideal transmission line
l_phys - physical length, in um
c_par - parasitic capacitance, in fF

Created on Wed Jun 25 16:20:35 2014
@author: elvd

"""

import numpy as np


def txline_calc(ind, freq, er, z0l):
    freq *= 1e9
    lambda_g = (3e8 / freq) / np.sqrt(er)
    ind *= 1e-12

    norm_impedance = 2 * np.pi * freq * ind / z0l
    if norm_impedance > 1:
        raise ValueError('Line impedance too low or frequency too high')

    else:
        l_phys = (lambda_g / (2 * np.pi)) * np.arcsin(norm_impedance)

        l_elec = ((2 * np.pi / lambda_g) * l_phys) * (180 / np.pi)

        c_par = (1 / (2 * np.pi * z0l * freq)) * \
            np.tan(np.pi * l_phys / lambda_g)

        l_phys *= 1e-6
        c_par *= 1e-15

    return [l_elec, l_phys, c_par]

if __name__ == '__main__':
    freq = raw_input('Enter frequency in GHz: ')
    freq = float(freq)
    ind = raw_input('Enter inductance in pH: ')
    ind = float(ind)
    er = raw_input('Enter effective dielectric constant: ')
    er = float(er)
    z0l = raw_input('Enter transmission line impedance: ')
    z0l = float(z0l)

# needs better input sanitisation

    try:
        results = txline_calc(ind=ind, freq=freq, er=er, z0l=z0l)
    except ValueError as e:
        print e.message
    else:
        print 'Electrical length is ', results[0]
        print 'Physical length is ', results[1], ' um'
        print 'Parasitic capacitance is ', results[2], ' fF'
