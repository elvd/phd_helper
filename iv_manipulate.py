# -*- coding: utf-8 -*-
"""
Functions to manipulate and modify measurement data for RTD current-voltage
characteristics.

Functions contained in module.
------------------------------
- make_symmetric(data, quadrant)
- scale(data, factor)
- extract_region(data, region)

Individual documentation can be accessed by using the following commands:
>>> import iv_manipulate
>>> print iv_manipulate.<function_name>.__doc__  # or
>>> help(iv_manipulate.<function_name>)

Created on Tue Aug 19 17:01:45 2014
@author: Viktor Doychinov

"""

from __future__ import print_function
import numpy as np
import scipy.signal as spsig


def make_symmetric(data, quadrant='pos'):
    """
    Takes an I-V and makes it anti-symmetric, i.e. odd, with respect to
    the origin, by taking one half of the I-V and rotating it around the
    origin.

    Parameters:
    -----------
    data : numpy.ndarray
        I-V data of one device.
    quadrant : {'pos', 'neg'}, optional
        Signifies which quadrant is to be used for `symmetrising' the I-V.

    Returns:
    --------
    new_data : numpy.ndarray
        The newly symmetric I-V, with datapoints in different rows.

    Raises:
    -------
    IndexError
        In case the data array has more than 2 dimensions, i.e. data for more
        than one device.
    ValueError
        In case an invalid parameter is specified for the `quadrant` variable.

    Notes:
    ------
    Requires an installation of NumPy. Data is returned as an array, further
    processing is up to calling function.

    """

    if np.ndim(data) != 2:  # only process one I-V dataset at a time
        raise IndexError('Incorrect data format')

    if np.size(data, 0) < np.size(data, 1):
        data = data.T  # make sure data is in columns

    new_data = data.copy()  # do not change original data

    # create a boolean mask to extract region
    if quadrant == 'pos':
        elements_mask = np.where(new_data[:, 0] >= 0.0)
    elif quadrant == 'neg':
        elements_mask = np.where(new_data[:, 0] <= 0.0)
    else:
        raise ValueError('Invalid value for quadrant')

    elements_mask = elements_mask[0]
    new_data = new_data[elements_mask]

    mirror_data = new_data * -1
    mirror_data = np.flipud(mirror_data)

    # newly symmetric I-V
    if quadrant == 'pos':
        new_data = np.concatenate((mirror_data, new_data))
    else:
        new_data = np.concatenate((new_data, mirror_data))

    return new_data


def scale(data, factor):
    """
    Scales an I-V by multiplying they measured `y` data by a factor.
    Performs a type conversion before scaling.

    Parameters:
    -----------
    data : numpy.ndarray
        I-V data of one device.
    factor : float
        The factor by which to scale the I-V.

    Returns:
    --------
    new_data : numpy.ndarray
        The newly scaled I-V, with datapoints in different rows.

    Raises:
    -------
    IndexError
        In case the data array has more than 2 dimensions, i.e. data for more
        than one device.

    Notes:
    ------
    Requires an installation of NumPy. Data is returned as an array, further
    processing is up to calling function.
    Variable `factor` should be [0, Inf).

    """

    if np.ndim(data) != 2:  # only process one IV dataset at a time
        raise IndexError('Incorrect data format')

    if np.size(data, 0) < np.size(data, 1):
        data = data.T  # make sure data is in columns

    # match data types for float multiplication/division
    new_data = data.copy().astype(float)

    new_data[:, 1] *= factor

    return new_data


def extract_region(data, region='pdr'):
    """
    Extracts a part of the measured I-V that is of interest. Possible
    regions are either the initial Positive Differential Resistance one, or the
    Negative Differential Resistance regions plus the second PDR regions.

    Parameters:
    -----------
    data : numpy.ndarray
        I-V data of one device.
    region : {'pdr', 'ndr'}, optional
        Which region of the RTD's I-V to extract.

    Returns:
    --------
    new_data : numpy.ndarray
        The extracted region, with datapoints in different rows.

    Raises:
    -------
    IndexError
        In case the data array has more than 2 dimensions, i.e. data for more
        than one device.
    ValueError
        In case an invalid parameter is specified for the `region` variable.

    Notes:
    ------
    Requires an installation of NumPy and SciPy. Data is returned as an array,
    further processing is up to calling function.
    Region extraction works in the following way. First, local minima and
    maxima are identified and their `x` values saved, going from smallest to
    largest. Using those, the 'pdr' region is defined as the data between the
    last minimum before `x` = 0, and the first maximum after `x` = 0.
    When extracting the 'ndr' region, two parts of the I-V are actually
    concatenated together. The first part spans from the value with smallest
    `x` component to the last minimum before `x` = 0; and the second part is
    from the first maximum after `x` = 0, up to the value with largest `x`.

    """

    if np.ndim(data) != 2:  # only process one IV dataset at a time
        raise IndexError('Incorrect data format')

    if np.size(data, 0) < np.size(data, 1):
        data = data.T  # make sure data is in columns

    new_data = data.copy()  # do not change original data

    # find local minima and maxima
    local_min_indices = spsig.argrelmin(new_data, order=100)
    local_max_indices = spsig.argrelmax(new_data, order=100)

    # extract indices from returned data structure
    local_min_indices = local_min_indices[0]
    local_max_indices = local_max_indices[0]

    local_min_values = new_data[local_min_indices]
    local_max_values = new_data[local_max_indices]

    # split into extrema in I and III quadrant
    neg_mins_indices = np.where(local_min_values[:, 0] <= 0.0)
    neg_mins_indices = neg_mins_indices[0]
    neg_mins_indices = local_min_indices[neg_mins_indices]

    pos_max_indices = np.where(local_max_values[:, 0] >= 0.0)
    pos_max_indices = pos_max_indices[0]
    pos_max_indices = local_max_indices[pos_max_indices]

    if region == 'pdr':
        first_peak = neg_mins_indices[-1]
        second_peak = pos_max_indices[0]
        new_data = new_data[first_peak:second_peak, :]
    elif region == 'ndr':
        first_ndr = new_data[:neg_mins_indices[-1], :]
        second_ndr = new_data[pos_max_indices[0]:, :]
        new_data = np.concatenate((first_ndr, second_ndr))
    else:
        raise ValueError('Region should be either pdr or ndr')

    return new_data

if __name__ == '__main__':
    print(__doc__)
