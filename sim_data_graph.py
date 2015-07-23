# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 15:38:36 2015

@author: elvd
"""

import os
import lxml.etree as etree


def assemble_keys(graph):
    pass

filename_list = os.listdir(os.getcwd())
filename_list = [filename for filename in filename_list if
                 os.path.splitext(filename)[1] == '.xml']

graph_info = etree.parse('graph_suite_20ghz_mixers.xml')
graph_info_root = graph_info.getroot()

for graph in graph_info_root:
    key_full = graph.find('.//*[@key_full]').values()[0]

    if key_full == 'false':
        keys = assemble_keys(graph)
    else:
        keys = [key.text for key in graph.findall('.//key')]

    graph_labels = graph.find('labels')


