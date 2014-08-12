### PhD Helper Scripts

This repository holds various short scripts, mainly written in Python. These were all written as part of my PhD project at the University of Leeds, and are meant to help with various little tasks.

The scripts are:
- ```auto_poly_generator.py``` - Reads in data from measurement files, containing DC current-voltage characteristics of different RTD devices. Once the data has been read, fits a polynomial to it, using NumPy's ```polyfit()``` function. Finally, it saves all the fitted polynomials, along with graphs comparing the fit to the measurement.
- ```dbrttx.py``` - Calculates the transmission probability as a function of electron energy for a given RTD semiconductor layer structure.
- ```ind_calculator.py``` - A tool to calculate the properties of a piece of a transmission line, required to present a specified inductance value at a specified frequency.

The scripts are functional as they are, but require polishing and better comments.
