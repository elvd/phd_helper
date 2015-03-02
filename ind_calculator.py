# -*- coding: utf-8 -*-
import numpy as np


def tline_ind(ind, freq, er, z0l):
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
        Corresponding physical length in um.
    c_par : float
        Total parasitic capacitance in fF.

    Raises:
    -------
    ValueError
        In case requested inductance cannot be formed using a line of the
        specified impedance and/or the frequency specified is too high.

    Notes:
    ------
    Requires an installation of NumPy. Pretty display of results is up to
    calling function.

    Example:
    --------
    >>> import ind_calculator
    >>> results = ind_calculator.tline_ind(225, 50, 10.2, 100)
    >>> print results
    [44.979873297640133, 2.3472907724095448e-10, 1.3178277694076776e-29]

    Created on Wed Jun 25 16:20:35 2014
    @author: Viktor Doychinov

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
        l_phys /= 1e-6
        c_par /= 1e-15

    return [l_elec, l_phys, c_par]  # returns as a list

if __name__ == '__main__':
    print tline_ind.__doc__
