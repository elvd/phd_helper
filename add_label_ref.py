# -*- coding: utf-8 -*-
"""
A quick script to update a list of references in RIS format with a label field,
in order to ensure compatibility with BiBTeX bibliography management.

Functions contained in module.
------------------------------
- add_label(record, record_id)
- write_record(output_file, record)
- process_file(inp_fname, out_fname)

Individual documentation can be accessed by using the following commands:
>>> import add_label_ref
>>> print add_label_ref.<function_name>.__doc__  # or
>>> help(add_label_ref.<function_name>)

Created on Wed Nov 19 15:59:49 2014
@author: elvd

"""


def add_label(record, label_seed, record_id):
    """
    Appends a label field to a RIS record. Label field corresponds to a `%F`
    line in the RIS record.

    Parameters:
    -----------
    record : list of lists
        A list of lists, containing the different fields for a single reference
        record.
    label_seed : str
        Forms the base of the label. the `record_id` is concatenated with it
        to come up with a truly unique identifier.
    record_id : str
        A unique identifier, to be added to the Label field value.

    Notes:
    ------
    Modifies the list in-place.

    """
    for item in record:
        if '%F' in item:
            break
    else:
        label = ''.join([label_seed, str(record_id), '\n'])
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

    output_file.write('\n\n\n')  # record delimeter


def process_file(inp_fname, out_fname):
    """
    Processes all RIS records in a given input file, appends Label fields, and
    writes them out to a given output file.

    Parameters:
    -----------
    inp_fname : str
        Input filename.
    out_fname : str
        Output filename.

    Notes:
    ------
    Filenames must include absolute path, if they are in a different location
    than the script.

    Example:
    --------
    >>> import add_label_ref
    >>> fname_in = r'references.txt'
    >>> fname_out = r'references_labels.txt'
    >>> add_label_ref.process_file(fname_in, fname_out)

    """
    counter = 0
    label_seed = 'Mixer'
    record_id = 1
    record_parameters = list()

    with open(inp_fname, 'rt') as file_in, open(out_fname, 'wt') as file_out:
        for line in file_in:
            if counter >= 3:
                counter = 0

                add_label(record_parameters, label_seed, record_id)
                record_id = record_id + 1
                write_record(file_out, record_parameters)

                record_parameters = list()

            if line.startswith('\n'):
                counter = counter + 1
                continue

            record_parameters.append(line.split(' ', 1))

        else:
            if record_parameters:
                add_label(record_parameters, label_seed, record_id)
                write_record(file_out, record_parameters)

if __name__ == '__main__':
    print __doc__
