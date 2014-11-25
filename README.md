### PhD Helper Scripts

This repository holds various short scripts, written in Python. These were all written as part of my PhD project at the University of Leeds, and are meant to help with various little tasks.

The scripts are:
- `auto_poly_generate.py` - Reads in data from measurement files, containing DC current-voltage characteristics of different RTD devices. Once the data has been read, fits a polynomial to it. Finally, it saves all the fitted polynomials, along with graphs comparing the fit to the measurement.
- `dbrttx.py` - Calculates the transmission probability as a function of electron energy for a given RTD semiconductor layer structure.
- `ind_calculator.py` - A tool to calculate the properties of a piece of a transmission line, required to present a specified inductance value at a specified frequency.
- `iv_manipulate.py` - A collection of functions that manipulate measured DC current-voltage data. The module has functions for scaling, extracting a specific region, and for making an I-V symmetric.
- `elvd_tools.py` - Miscellaneous functions, such as fitting a polynomial to the measured data; converting said polynomial to a format, suitable for use in Agilent/Keysight ADS; and finally, a function that plots measured data on a 2D graph, ensuring all graphs have the same style.
- `add_label_ref.py` - A quick script to append `Label` fields to each individual record in a RIS file, exported from EndNote. Could merge with `elvd_tools.py`.

The scripts are functional as they are, but could be improved for reusability and more general use.
