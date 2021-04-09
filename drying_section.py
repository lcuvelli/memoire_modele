import heat_transfer_coefficient as libh

from scipy.optimize import fsolve
from numpy import isclose, polyfit
import matplotlib.pyplot as plt
import tikzplotlib
import numpy as np
import matplotlib as mpl
import pylab as pl



from math import exp, pi, sin
import timeit


"""Constants"""
Ca = 1009 # Heat capacity air, J/kg/K

"""Climatic data - Cambodia"""
Sm = 463  # W/m2
Tamb = 30 + 273  # °K (mean diurnal temperature)
t_rise = 7  # h - Time sunrise
t_set = 19  # h - Time sunset
t0 = 9.5    # h - Start of drying
td = 6.5    # h - Drying time
tf = td + t0  #h - End of drying
RHamb = 70  # %
Iatm = 377  # W/m2



"""Specifications - Drying 10kg of mangoes in Cambodia"""
R = 1.4   # m - Aspect ratio
Q = 0.03  # kg of humid air/s - Air flow rate
Wd = 1.4  # m - Width of the dryer
k = 0.85  # Reduction factor
M0 = 10   # kg - Mass of product
ep = 0.001 # m - Plastic thickness
lp = 0.2  # W/m*K - Plastic thermal conductivity
e = 6 / 1000  # m - Thickness of the slices of product

X0 = 7    # kg water/kg dry product - Initial moisture of the products
Xf = 0.1  # kg water/kg dry product - Final moisture of the products
M0 = 10   # kg of product to dry
Lw = 2358 * 1000 # J/kg - Mass latent heat of vaporization



DELTA_T = 0.5




def evaporation_coefficient():
    """Coefficient in the function of the energy flux consumed by the evaporation"""

    alpha = - 4 * (X0 - Xf) / (td * 3600 * (exp(-4) - 1))

    return alpha

def J(t, alpha):
    """Kg of water per kg dry product per second as a function of time

    Args:
        t: time of the day, in range [t0, t0 + td] in seconds
        alpha: coefficient of the exponentiel """

    return alpha * exp(-4 * (t - t0)/td)

def J2(t, T, alpha):
    """Kg of water per kg dry product per second as a function of time

        Args:
            t: time of the day, in range [t0, t0 + td] in seconds
            alpha: coefficient of the exponentiel """
    Ea = 30 * 1000 # J/mol
    Rg = 8.314     # J/mol*K
    Td = 70 + 273  # K

    return alpha * exp(-4 * (t - t0) / td) * exp(-Ea/Rg * (1/T - 1/Td))


def mass_per_surface_unit(M0, LD, Wd):
    Ms = M0/(LD * Wd)
    return Ms

def darboux_sum(y: list, dt)->float:
    """Gives the Darboux sum, computed as the mean value between the lower and upper Darboux.

    Args:
        y: List of the value of the function on the interval [0, len(y)]
        dt: length of the subinterval of the partition """

    lower_sum = 0
    upper_sum = 0

    for i in range(len(y) - 1):
        inf = min(y[i], y[i+1])
        sup = max(y[i], y[i+1])

        lower_sum += inf * dt
        upper_sum += sup * dt
    print("Lower Darboux sum:", lower_sum)
    print("Upper Darboux sum:", upper_sum)

    return (lower_sum + upper_sum)/2

def main():

    intervals_t = np.arange(t0, t0 + td + DELTA_T, DELTA_T).tolist()
    alpha = evaporation_coefficient()
    print(alpha)


    P = [53.755463930536635, 61.07720999613991, 67.01758728494032, 71.7111138804958, 75.26067224112127, 77.74304067972115, 79.21153410558242, 79.69757147809871, 79.21153410558242, 77.74304067972115, 75.2606722411213, 71.71111388049594, 67.01758728494003, 61.07720999613991]
    T = [57.05070711384582, 61.89683694590565, 66.07278090156086, 69.53688856317234, 72.25906951723152, 74.21781731805669,
     75.39864113287763, 75.79316322713913, 75.39864113287763, 74.21781731805669, 72.25906951723152, 69.53688856317234,
     66.07278090156092, 61.89683694590565]
    y = []
    for i in range(len(T)):
        y.append(J2(intervals_t[i],T[i]+273, alpha))
        #y.append(J(intervals_t[i], alpha))


    t = t0
    M = []
    i = 0
    while t <= tf:
        M.append(M0 / (1+X0) * Lw * y[i]/P[i])
        M[i] = M[i]/Wd
        t+= DELTA_T
        i+=1
    print(len(M), len(y))
    print(M0 /(1+X0))
    moyenne = darboux_sum(M,DELTA_T)/td
    print(moyenne)
    print(moyenne/Wd)




    plt.figure(1)
    plt.title("Surface au sol de la zone de séchage (m2)")
    plt.plot(intervals_t, M, 'yo')
    plt.xlabel('Time of the day (h)')
    plt.ylabel("Omega (m2)")
    plt.text(13,20,"Mean: 8.4 m2")


    """Drawing"""
    plt.figure(2)
    plt.title("Energy flux transferred to the air inside the dryer, W/m2 (LH = 5m)")
    plt.plot(intervals_t,P)
    plt.xlabel('Time of the day (h)')
    plt.ylabel("P (W/m2)")

    plt.figure(3)
    plt.title("J(t) with alpha = 0.0012 ")
    plt.plot(intervals_t, y, 'og')
    plt.xlabel('Time of the day (h)')
    plt.ylabel("J (kg of water/kg dry product per second)")

    #for i, txt in enumerate(T):
        #txt = str(round(txt,1))+"°C"
        #plt.annotate(txt, (intervals_t[i]+0.1, y[i]), fontsize=9)

    plt.show()

    # line, = plt.plot(intervals_t, y, label='for evaporation')
    # plt.legend()
    #
    # plt.ylabel('Energy flux (W/m2)')
    # #line.set_label('Label via method')
    # #tikzplotlib.save("mytikz.tex")
    # plt.show()


if __name__ == '__main__':
    main()

