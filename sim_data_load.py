# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 22:49:46 2015

@author: elvd
"""

import os
import csv
import numpy as np


start_dir = '/var/host/media/removable/UNTITLED/projects/phd_helper/sim_data/'

# use same key to refer to data and data labels
sim_results = dict()
sim_results_labels = dict()

# holds keys
dict_key_list = list()

for dirname, subdirlist, filelist in os.walk(start_dir):
    if not subdirlist:
        for filename in filelist:
            # key defined by filename plus path to it
            key_base = os.path.relpath(dirname, start_dir)
            key_base = key_base.replace(os.path.sep, '_')

            dict_key = '_'.join([key_base, os.path.splitext(filename)[0]])
            fname = os.path.join(dirname, filename)

            # individual datasets stored as elements in a list
            sim_results[dict_key] = list()
            sim_results_labels[dict_key] = list()
            dict_key_list.append(dict_key)

            with open(fname, 'rt') as file_in:
                inp = csv.reader(file_in, delimiter='\t')
                dataset = list()
                for line in inp:
                    if not line:  # skip empty lines
                        continue
                    try:  # test for rows containing data labels
                        line[0] = float(line[0])
                        if line[1] == '<invalid>':
                            line[1] = 0.0  # need better way to handle
                        else:
                            line[1] = float(line[1])
                        dataset.append(line)  # one datapoint
                    except:  # add data label, both x and y
                        sim_results_labels[dict_key].append(line)
                        if dataset:  # reached the start of new dataset
                            sim_results[dict_key].append(np.array(dataset))
                        dataset = list()
                if dataset:  # handle last dataset in a file
                    sim_results[dict_key].append(np.array(dataset))
