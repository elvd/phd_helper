# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 17:01:45 2014

@author: elvd
"""

import numpy as np


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
        new_data[1, :] *= factor
    elif np.size(new_data, 0) >= np.size(new_data, 1):
        new_data[:, 1] *= factor

    return new_data


def extract_region(data, region='pdr'):
    if np.ndim(data) != 2:
        raise IndexError('Incorrect data format')

    new_data = data.copy()

    if np.size(new_data, 0) < np.size(new_data, 1):
        new_data = new_data.T

    if region == 'pdr':

