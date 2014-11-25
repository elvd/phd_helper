# -*- coding: utf-8 -*-
"""
A quick script to update a list of references in RIS format with a label field,
in order to ensure compatibility with BiBTeX bibliography management.

Functions contained in module.
------------------------------
- add_label(record)
- write_record(output_file, record)
- process_file(input_file, output_file)  # not yet implemented

Individual documentation can be accessed by using the following commands:
>>> import add_label_ref
>>> print add_label_ref.<function_name>.__doc__  # or
>>> help(add_label_ref.<function_name>)

Created on Wed Nov 19 15:59:49 2014
@author: elvd

"""


def add_label(record):
    """
    Appends a label field to a RIS record. Label field corresponds to a `%F`
    line in the RIS record.

    Parameters:
    -----------
    record : list of lists
        A list of lists, containing the different fields for a single reference
        record.

    Notes:
    ------
    Modifies the list in-place. The `record_id` variable is a global, so as to
    provide a unique id.

    """
    global record_id
    for item in record:
        if '%F' in item:
            break
    else:
        # need to get  rid of magic value `Mixer`
        label = ''.join(['Mixer', str(record_id), '\n'])
        record_id = record_id + 1
        record.append(['%F', label])


def write_record(output_file, record):
    """
    Writes out a RIS record to a text file.

    Parameters:
    -----------
    output_file : file
        The output text file, must be open and write-able.
    record : list of lists
        A list of lists, containing the different fields for a single reference
        record.

    Notes:
    ------
    Also writes out a record separator, consisting of `\n\n\n`.

    """
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
