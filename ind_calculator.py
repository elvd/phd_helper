# -*- coding: utf-8 -*-
import numpy as np


def txline_calc(ind, freq, er, z0l):
    """
    A quick script to calculate the parameters of a transmission line, used to
    represent an inductive element.

    Parameters:
    -----------
    ind : float
        Value of inductance in pH.
    freq : float
        Centre frequency in GHz.
    er : float
        Effective dielectric constant of substrate material.
    z0l : float
        Desired impedance of the transmission line.

    Returns:
    --------
    l_elec : float
        Electrical length of an ideal transmission line, used to represent the
        inductance `ind`.
    l_phys : float
        Corresponding hysical length in um.
    c_par : float
        Total parasitic capacitance in fF.

    Raises:
    -------
    ValueError
        In case requestd inductance cannot be formed using a line of the
        specified impedance and/or the frequency specified is too high.

    Notes:
    ------
    Created on Wed Jun 25 16:20:35 2014
    @author: elvd

    """

    # convert to basic units, i.e. Hz and H
    freq *= 1e9
    ind *= 1e-12

    # calculate guide wavelength
    lambda_g = (3e8 / freq) / np.sqrt(er)

    norm_impedance = 2 * np.pi * freq * ind / z0l
    if norm_impedance > 1:
        raise ValueError('Line impedance too low or frequency too high')

    else:
        l_phys = (lambda_g / (2 * np.pi)) * np.arcsin(norm_impedance)

        l_elec = ((2 * np.pi / lambda_g) * l_phys) * (180 / np.pi)

        c_par = (1 / (2 * np.pi * z0l * freq)) * \
            np.tan(np.pi * l_phys / lambda_g)

        # convert to output units
        l_phys *= 1e-6
        c_par *= 1e-15

    return [l_elec, l_phys, c_par]  # returns as a list

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
