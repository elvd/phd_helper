# -*- coding: utf-8 -*-
"""
Functions to manipulate and modify measurement data for RTD current-voltage
characteristics. Contains three functions:
- make_symmetric
    Purpose: makes an I-V and makes it anti-symmetric, i.e. odd with respect to
    the origin, by taking one half of the I-V and rotating it around the
    origin.
    Inputs:
        - data: measurement data, consisting of x-y datapoints.
        - quadrant: 'pos' or 'neg' accepted, selects which half to use.
    Outputs:
        - new_data: a NumPy array.
- scale_iv
    Purpose: scales an I-V by multiplying they measured y data by a factor.
    Performs a type conversion before scaling.
    Inputs:
        - data: measurement data, consisting of x-y datapoints.
        - factor: factor by which to scale, no restrictions on number.
    Outputs:
        - new_data: a NumPy array.
- extract_region:
    Purpose: extracts a part of the measured I-V that is of interest. Possible
    regions are either the initial Positive Differential Resistance one, or the
    Negative Differential Resistance regions plus the second PDR regions.
    Inputs:
        - data: measurement data, consisting of x-y datapoints.
        - region: 'pdr' or 'ndr' accepted, selects which region to be returned.
    Outputs:
        - new_data: a NumPy array

Created on Tue Aug 19 17:01:45 2014
@author: elvd
"""

import numpy as np
import scipy.signal as spsig


def make_symmetric(data, quadrant='pos'):
    if np.ndim(data) != 2:
        raise IndexError('Incorrect data format')

    new_data = data.copy()

    if np.size(new_data, 0) < np.size(new_data, 1):
        new_data = new_data.T

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

    if quadrant == 'pos':
        new_data = np.concatenate((mirror_data, new_data))
    else:
        new_data = np.concatenate((new_data, mirror_data))

    return new_data


def scale_iv(data, factor):
    if np.ndim(data) != 2:
        raise IndexError('Incorrect data format')

    new_data = data.copy().astype(type(factor))

    if np.size(new_data, 0) < np.size(new_data, 1):
        new_data = new_data.T

    new_data[:, 1] *= factor

    return new_data


def extract_region(data, region='pdr'):
    if np.ndim(data) != 2:
        raise IndexError('Incorrect data format')

    new_data = data.copy()

    if np.size(new_data, 0) < np.size(new_data, 1):
        new_data = new_data.T

    local_min_indices = spsig.argrelmin(new_data, order=100)
    local_max_indices = spsig.argrelmax(new_data, order=100)

    local_min_indices = local_min_indices[0]
    local_max_indices = local_max_indices[0]

    local_min_values = new_data[local_min_indices]
    local_max_values = new_data[local_max_indices]

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
