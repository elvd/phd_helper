# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 15:38:36 2015

@author: elvd
"""

import os
import lxml.etree as etree


def construct_legend(legend_xml):
    legend_string = list()
    for entry in legend_xml:
        legend_string.append(entry.text)
    return legend_string


filename_list = os.listdir(os.getcwd())
filename_list = [filename for filename in filename_list if
                 os.path.splitext(filename)[1] == '.xml']

for filename in filename_list:
    graph_info = etree.parse(filename)
    graph_info_root = graph_info.getroot()

    for graph in graph_info_root:
        subgraphs_separate = graph.find('.//*[@separate]').values()[0]
        graph_labels = graph.find('labels')

        if subgraphs_separate == 'yes':
            for subgraph in graph.find('subgraphs'):
                for data_key in graph.find('datasets'):
                    print data_key.text
                    print int(subgraph.text)
                print graph_labels.find('xlabel').text
                print graph_labels.find('ylabel').text
                subgraph_title = ''.join([".//*[@subgraph='",
                                         subgraph.text, "']"])
                print graph_labels.find(subgraph_title).text
                print construct_legend(graph_labels.find('legend'))
        else:
            for data_key in graph.find('datasets'):
                for subgraph in graph.find('subgraphs'):
                    print data_key.text
                    print int(subgraph.text)
                print graph_labels.find('xlabel').text
                print graph_labels.find('ylabel').text
                print graph_labels.find('title').text
                print construct_legend(graph_labels.find('legend'))

        print 'next graph'
    print 'next file'
