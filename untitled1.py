# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 18:03:53 2015

@author: Viktor
"""

import os
import pickle
import matplotlib.pyplot as plt


plt.ioff()
filenames = os.listdir(os.getcwd())
filenames = (filename for filename in filenames if 'pickle' in filename)

for filename in filenames:
    current_fig = pickle.load(file(filename))
    print filename
    plt.show()
    figname = os.path.splitext(filename)[0]
    figname = '.'.join([figname, 'jpg'])
    current_fig.savefig(figname, dpi=300)
