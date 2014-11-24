import numpy as np


# define s-parameters
s11 = 1
s12 = 1
s21 = 2
s22 = 2

# stability testing
delta = s11 * s22 - s12 * s21
delta_mag = np.abs(delta)

k = (1 - np.abs(s11)**2 - np.abs(s22)**2 + delta_mag**2) / \
    (2 * np.abs(s12 * s21))

if k > 1 and delta_mag < 1:
    print 'Transistor is stable.'
else:
    print 'Transistor is not stable.'

    radius_load = np.abs((s12 * s21) / (np.abs(s22)**2 - delta_mag**2))
    centre_load = np.conj(s22 - delta*np.conj(s11)) \
        / (np.abs(s22)**2 - delta_mag**2)
    centre_load_mag = np.abs(centre_load)
    centre_load_angle = np.angle(centre_load, deg=True)

    radius_source = np.abs((s12 * s21) / (np.abs(s11)**2 - delta_mag**2))
    centre_source = np.conj(s11 - delta*np.conj(s22)) \
        / (np.abs(s11)**2 - delta_mag**2)
    centre_source_mag = np.abs(centre_source)
    centre_source_angle = np.angle(centre_source, deg=True)

    print 'Some stuff here...'
