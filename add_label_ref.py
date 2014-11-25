# -*- coding: utf-8 -*-
"""
Created on Wed Nov 19 15:59:49 2014

@author: elvd
"""


def add_label(record):
    global record_id
    for item in record:
        if '%F' in item:
            break
    else:
        label = ''.join(['Mixer', str(record_id), '\n'])
        record_id = record_id + 1
        record.append(['%F', label])


def write_record(output_file, record):
    for item in record:
        line_new = ' '.join(item)
        output_file.write(line_new)

    output_file.write('\n\n\n')


fname_in = r'All_References.txt'
fname_out = r'All_References_Processed.txt'

counter = 0
record_id = 1

record_parameters = list()

with open(fname_in, 'rt') as file_in, open(fname_out, 'wt') as file_out:
    for line in file_in:

        if counter >= 3:
            counter = 0

            add_label(record_parameters)
            write_record(file_out, record_parameters)

            record_parameters = list()

        if line.startswith('\n'):
            counter = counter + 1
            continue

        record_parameters.append(line.split(' ', 1))

    else:
        if record_parameters:
            add_label(record_parameters)
            write_record(file_out, record_parameters)
