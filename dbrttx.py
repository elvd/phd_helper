# -*- coding: utf-8 -*-
"""
A Python translation of a Matlab script to calculate electron transmission
probability for a GaAs/AlGaAs Resonant-Tunneling Diode.

Input parameters:
fractE - Mole fraction of Aluminium in emitter barrier
fractC - Mole fraction of Aluminium in collector barrier
Lw - well length in Angstrom
Lbe - emitter barrier length in Angstrom
Lbc - collector barrier length in Angstrom

Outputs:
E, Tx - transmission probabilty as function of electron energy

Output is returned as a NumPy array, with E and Tx being two rows in it.

Created on Mon Aug 04 13:46:17 2014
@author: elvd

"""

import numpy as np
import elvd_tools


def dbtx_calc(fractE, fractC, Lw, Lbe, Lbc):
    m = 0.91e-30  # effective electron mass
    hbar = 1.06e-34  # Planck's constant
    q = 1.6e-19  # Electron charge
    NI = 25000
    Mw = 0.067
    Me = Mw
    Mc = Mw
    Mbe = (0.083*fractE + 0.067)
    Mbc = (0.083*fractC + 0.067)
    Vbe = (80*fractE) / 100
    Vbc = (80*fractC) / 100
    de = (Vbc - 0.001) / NI
    Ve = 0
    Vw = 0
    Vc = 0

    Tx = []
    E = []

    for n in range(NI):
        E.append((n+1)*de)
        mult = np.sqrt(2*m*q / (hbar**2))

        ke = mult * np.sqrt(Me * (E[n] - Ve))
        kbe = mult * np.sqrt(Mbe * (Vbe - E[n]))
        kw = mult * np.sqrt(Mw * (E[n] - Vw))
        kbc = mult * np.sqrt(Mbc * (Vbc - E[n]))
        kc = mult * np.sqrt(Mc * (E[n] - Vc))

        a = (kbe * Me) / (ke * Mbe)
        b = (kw * Mbe) / (kbe * Mw)
        c = (kbc * Mw) / (kw * Mbc)
        d = (kc * Mbc) / (kbc * Mc)

        e = complex(0, kw*Lw)
        N11 = complex(1, a)
        N12 = complex(1, -a)
        O11 = complex(1, -b) * np.exp(kbe*Lbe)
        O12 = complex(1, +b) * np.exp(kbe*Lbe)
        O21 = complex(1, +b) * np.exp(-kbe*Lbe)
        O22 = complex(1, -b) * np.exp(-kbe*Lbe)
        P11 = complex(1, +c) * np.exp(-e)
        P12 = complex(1, -c) * np.exp(-e)
        P21 = complex(1, -c) * np.exp(e)
        P22 = complex(1, +c) * np.exp(e)
        Q11 = complex(1, -d) * np.exp(kbc*Lbc)
        Q21 = complex(1, +d) * np.exp(-kbc*Lbc)

        T11 = (N11*O11 + N12*O21) * (P11*Q11 + P12*Q21) + \
            (N11*O12 + N12*O22) * (P21*Q11 + P22*Q21)

        Tx.append(16 * kc / (ke * (T11 * np.conj(T11))))

    E = np.abs(E)
    Tx = np.abs(Tx)

    return np.array([E, Tx])

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    fractE = 1.0
    fractC = 1.0
    Lw = 50e-10
    Lbe = 17e-10
    Lbc = 17e-10

    results = dbtx_calc(fractE=fractE, fractC=fractC, Lw=Lw, Lbe=Lbe, Lbc=Lbc)
    results = results.T

    try:
        graph = elvd_tools.custom_plot(data=results, xlabel='',
                                       ylabel='Electron energy, [eV]',
                                       title='Transmission probability',
                                       mode='log')
        plt.savefig('TxE.png')
        plt.show()
    except IndexError as e:
        print e.message
