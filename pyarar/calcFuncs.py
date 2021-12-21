#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : calcFuncs.py
# @Author : Yang Wu
# @Date   : 2021/12/20
# @Email  : wuy@cug.edu.cn

"""
Functions involved in entire calculations of Ar-Ar dating.
Important Constants:

    Isotopic Mass:
    M41 = 40.9645008
    M40 = 39.962383123
    M39 = 38.964313
    M38 = 37.9627322
    M37 = 36.9667759
    M36 = 35.96754628
    M35 = 34.9752567

    M40 = 39.962384                                 # Nuclides and Isotopes, Chart of nuclides, 14th edition
    M38 = 37.962732                                 # Nuclides and Isotopes, Chart of nuclides, 14th edition
    M36 = 35.967546                                 # Nuclides and Isotopes, Chart of nuclides, 14th edition

    M40 = 39.962383123                              # Nuclides and Isotopes, Chart of nuclides, 16th edition, 2002
    M38 = 37.962732                                 # Nuclides and Isotopes, Chart of nuclides, 16th edition, 2002
    M36 = 35.9675463                                # Nuclides and Isotopes, Chart of nuclides, 16th edition, 2002

    Atom Percent Abundance:
    Ar40_AA = 99.6003                               # Nuclides and Isotopes, Chart of nuclides, 16th edition, 2002
    Ar38_AA = 0.0632                                # Nuclides and Isotopes, Chart of nuclides, 16th edition, 2002
    Ar36_AA = 0.3365                                # Nuclides and Isotopes, Chart of nuclides, 16th edition, 2002

    Atmospheric Isotope Proportion:
    (40Ar/36Ar)a = 295.5                            # Nier, 1950; Steiger and Jäger, 1977
    (38Ar/36Ar)a = 0.1869                           # Nier, 1950; Steiger and Jäger, 1977

    Artificially Radioactive:
    Ar35: Half_Life = 1.77 s                        # Nuclides and Isotopes, Chart of nuclides, 16th edition, 2002
          Modes_of_Decay_1 = positron
          Energy_of_Radiation_1 = 4.943 MeV
          Modes_of_Decay_2 = gamma ray
          Energy_of_Radiation_2 = 1219.2 keV
    Ar37: Half_Life = 35.0 d
    Ar39: Half_Life = 269 a
"""
import json
import xlrd
import xlsxwriter
from numpy import random
from math import exp, log, atan, tan, cos, sin
from math import pi as _pi
from typing import List, Any
from matplotlib import pyplot, patches
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

M40 = 39.962383123

'-----------------------'
'--J Value Calculation--'
'-----------------------'
def j_value(age: float, sage: float, r: float, sr: float, f: float, rsf: float):
    """
    :param age: age of the reference standard sample, in Ma
    :param sage: 1 sigma error of age
    :param r: 40/39 ratio of the reference standard standard sample
    :param sr: 1 sigma error of 40/39 ratio
    :param f: decay constant(lambda) of K
    :param rsf: relative error of decay constant
    :return: J value | error
    """
    f = f * 1000000  # exchange to unit of Ma
    rsf = f * rsf / 100  # exchange to absolute error
    k0 = (exp(f * age) - 1) / r
    """
    k2 = error_divide(((exp(f * a0) - 1), exp(f * a0) * error_multiply((f, sf), (a0, a1))), (a2, a3))
    # result might be a little different with k1 below
    """
    v1 = rsf ** 2 * (age * exp(f * age) / r) ** 2
    v2 = sage ** 2 * (f * exp(f * age) / r) ** 2
    v3 = sr ** 2 * ((1 - exp(f * age)) / r ** 2) ** 2
    k1 = pow(v1 + v2 + v3, 0.5)
    return k0, k1


'------------------------'
'--Correction Functions--'
'------------------------'
def get_mdf(rm: float, srm: float, m1: float, m2: float, isAapkop: bool = True):
    """
    :param isAapkop: Using formula in A.A.P.Koppers's program
    :param rm: ratio 40a/36a
    :param srm: error of ratio in one sigma
    :param m1: Ar36 isotopic mass
    :param m2: Ar40 isotopic mass
    :return:
    """
    sm1 = 0;
    sm2 = 0
    ra = 298.35;
    sra = 0
    delta_m = m2 - m1
    sdelta_m = error_add(sm2, sm1)
    ratio_m = m2 / m1
    sratio_m = error_div((m2, sm2), (m1, sm1))
    if isAapkop:
        '''line'''
        k1 = (rm / ra + delta_m - 1) / delta_m  # A.A.P.Koppers
        k2 = error_div(((rm / ra + delta_m - 1), error_div((rm, srm), (ra, sra))), (delta_m, sdelta_m))
        '''exp'''
        k3 = (log(rm / ra) / log(ratio_m)) * (1 / m1) + 1  # A.A.P.Koppers
        v1 = error_log(rm / ra, error_div((rm, srm), (ra, sra)))
        v2 = error_log(ratio_m, sratio_m)
        v3 = error_div((log(rm / ra), v1), (log(ratio_m), v2))
        k4 = error_div((log(rm / ra) / log(ratio_m), v3), (m1, sm1))
        '''pow'''
        k5 = pow((rm / ra), (1 / delta_m))  # A.A.P.Koppers
        k6 = error_pow((rm / ra, error_div((rm, srm), (ra, sra))),
                       (1 / delta_m, error_div((1, 0), (delta_m, sdelta_m))))
        return k1, k2, k3, k4, k5, k6
    else:
        mdf_line_2 = (rm / ra - 1) / delta_m  # Ryu et al., 2013


def corr_blank(a0: list, e0: list, a1: list, e1: list):
    """
    :param a0: a list of tested isotope value
    :param e0: 1 sigma error of a0, list type
    :param a1: a list of blank isotope value
    :param e1: 1 sigma error of a1, list type
    :return: list of corrected data | error list
    """
    '''do not force negative value to zero in the procedure of correcting blank'''
    k0 = [a0[i] - a1[i] for i in range(len(a0))]
    k1 = [error_add(e0[i], e1[i]) for i in range(len(k0))]
    return k0, k1


def corr_discrimination(mdf: float, smdf: float, m: float, m40: float = M40):
    """
    :param mdf: mass discrimination factor(MDF)
    :param smdf: absolute error of MDF
    :param m: mass of isotope being corrected
    :param m40: mass of Ar40, default value is defined above
    :return: correct factor | error of factor
    """
    delta_mass = abs(m40 - m)
    k0 = 1 / (delta_mass * mdf - delta_mass + 1)
    k1 = error_div((1, 0), (1 / k0, smdf * delta_mass))
    return k0, k1


def corr_decay(t1: list, t2: list, t3: list, f: float, rsf: float, unit: str = 'h'):
    """
    :param t1: [year, month, day, hour, min], test start time
    :param t2: irradiation end time, in second
    :param t3: irradiation duration time, list for all irradiation cycles, in hour
    :param f: decay constant of K
    :param rsf: relative error of f
    :param unit: unit of decay constant, input 'h' or 'a'
    :return: correction factor | error of factor | stand duration
    """
    v1 = []
    v2 = []
    e1 = []
    sf = f * rsf / 100  # change to absolute error
    t_year, t_month, t_day, t_hour, t_min = t1
    t_test_start = get_datatime(t_year, t_month, t_day, t_hour, t_min)  # the time when analysis was starting
    k2 = [t_test_start - i for i in t2]  # standing time in second between irradiation and analysing

    if unit == 'h':
        k2 = [i / 3600 for i in k2]  # exchange to unit in hour
    elif unit == 'a':
        k2 = [i / (3600 * 24 * 365.242) for i in k2]  # exchange to unit in year
        t3 = [i / (24 * 365) for i in t3]

    for i in range(len(t3)):
        iP = 1  # power
        v1.append(iP * (1 - exp(-f * t3[i])) / (f * exp(f * k2[i])))
        e11 = t3[i] * exp(-f * t3[i]) / (f * exp(f * k2[i]))
        e12 = (exp(-f * t3[i]) - 1) * (1 + f * k2[i]) * exp(f * k2[i]) / (f * exp(f * k2[i])) ** 2
        e1.append(iP * (e11 + e12))
        v2.append(iP * t3[i])
    k0 = sum(v2) / sum(v1)
    k1 = error_div((sum(v2), 0), (sum(v1), pow(sum(e1) ** 2 * sf ** 2, 0.5)))
    # other error calculation equation in CALC
    # It is calculated based on an assumption that only one irradiation exist with total duration of sum of t3,
    # and the end time is the last irradiation finish time
    k1 = pow(((sum(t3) * exp(f * k2[-1]) * (1 - exp(-f * sum(t3))) + f * sum(t3) * k2[-1] * exp(f * k2[-1]) * (
            1 - exp(-f * sum(t3))) - f * sum(t3) * exp(f * k2[-1]) * sum(t3) * exp(-f * sum(t3))) / (
                      1 - exp(-f * sum(t3))) ** 2) ** 2 * sf ** 2, 0.5)
    return k0, k1, k2[-1]


def get_datatime(t_year: int, t_month: int, t_day: int, t_hour: int, t_min: int, t_seconds: int = 0):
    """
    :param t_year: int
    :param t_month: int
    :param t_day: int
    :param t_hour: int
    :param t_min: int
    :param t_seconds: int, default == 0
    :return: seconds since 1970-1-1 8:00
    """
    base_year, base_mouth, base_day, base_hour, base_min = [1970, 1, 1, 8, 0]
    if t_year % 4 == 0 and t_year % 100 != 0 or t_year % 400 == 0:
        days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    else:
        days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    delta_seconds = ((((t_year - base_year) * 365 + ((t_year + 1 - base_year) - (t_year + 1 - base_year) % 4) / 4 +
                       sum(days[base_mouth - 1:t_month - 1]) + t_day - base_day) * 24 + t_hour - base_hour) * 60 +
                     t_min - base_min) * 60 + t_seconds
    return delta_seconds


'-------------------'
'--Age Calculation--'
'-------------------'
def calc_age(a0: float, e0: float, j: float, rsj: float, f: float, rsf: float, uf: int = 1, useMin2000: bool = False,
             **kwargs):
    """
    :param a0: value of ar40r/ar39k
    :param e0: error of ar40r/ar39k
    :param j: irradiation params
    :param rsj: relative error of j in 1 sigma
    :param f: decay constants of K
    :param rsf: relative error of f in 1 sigma
    :param uf: error factor for ar40r/ar39k error, default = 1
    :param useMin2000: use equation in Min et al., 2000 or conventional equation
    :return: age in Ma | analytical error | internal error | full external error
    """
    sf = f * rsf / 100  # change to absolute error
    sj = j * rsj / 100  # change to absolute error
    e0 = e0 / uf  # change to 1 sigma
    try:
        k0 = log(1 + j * a0) / f
    except ValueError:
        k0 = 0
    try:
        v1 = e0 ** 2 * (j / (f * (1 + j * a0))) ** 2
        v2 = sj ** 2 * (a0 / (f * (1 + j * a0))) ** 2
        v3 = sf ** 2 * (log(1 + j * a0) / (f ** 2)) ** 2
        k1 = pow(v1, 0.5)  # analytical error
        k2 = pow(v1 + v2, 0.5)  # internal error
        k3 = pow(v1 + v2 + v3, 0.5)  # full external error
    except ValueError:
        k1, k2, k3 = 0, 0, 0
    [k0, k1, k2, k3] = [i / 1000000 for i in [k0, k1, k2, k3]]  # change to Ma

    if useMin2000:
        # use standard age
        kwargs = kwargs.pop('calculationParams', kwargs)
        A = kwargs.pop('activity_of_K', 31.58)
        sA = kwargs.pop('activity_of_K_error', 0.064)
        W = kwargs.pop('atomic_weight_of_K', 39.0983)
        sW = kwargs.pop('atomic_weight_of_K_error', 39.09830 * 0.000154 / 100)
        Y = kwargs.pop('seconds_in_a_year', 31556930)
        sY = kwargs.pop('seconds_in_a_year_error', 0)
        p = kwargs.pop('fraction_of_40K', 0.000117)
        sp = kwargs.pop('fraction_of_40K_error', 0.00000100035)
        No = kwargs.pop('avogadro_number', 6.0221367E+23)
        sNo = kwargs.pop('avogadro_number_error', 0.00000355306065)
        f = kwargs.pop('decay_constant_of_40K', 5.53E-10)
        sf = kwargs.pop('decay_constant_of_40K_error', 0.048E-10)
        t = kwargs.pop('standard_age', 132.7)
        st = kwargs.pop('standard_age_error', 132.7 * 0.5 / 100)
        V = p * No / (A * W * Y)
        stdR = (exp(t * 1000000 * f) - 1) / j
        sstdR = pow((stdR / j) ** 2 * sj ** 2, 0.5)
        R = a0 / stdR
        sR_1 = error_div((a0, e0), (stdR, sstdR))
        sR_2 = error_div((a0, e0), (stdR, 0))
        K = exp(t * 1000000 / V) - 1
        XX = K * R + 1
        sXX_1 = error_mul((K, 0), (R, sR_1))
        sXX_2 = error_mul((K, 0), (R, sR_2))
        # k0 = V * log(XX), V = p * No / (A * W * Y), XX = K * R + 1
        e1 = (log(XX) * V / p + V / XX * R * (K + 1) * (t * -1000000 / V ** 2) * V / p) ** 2 * sp ** 2
        e2 = (log(XX) * V / No + V / XX * R * (K + 1) * (t * -1000000 / V ** 2) * V / No) ** 2 * sNo ** 2
        e3 = (log(XX) * V / A * -1 + V / XX * R * (K + 1) * (t * -1000000 / V ** 2) * V / A * -1) ** 2 * sA ** 2
        e4 = (log(XX) * V / W * -1 + V / XX * R * (K + 1) * (t * -1000000 / V ** 2) * V / W * -1) ** 2 * sW ** 2
        e5 = (log(XX) * V / Y * -1 + V / XX * R * (K + 1) * (t * -1000000 / V ** 2) * V / Y * -1) ** 2 * sY ** 2
        e6 = (V / XX * K * R / a0) ** 2 * e0 ** 2 if a0 != 0 else 0
        e7 = (V / XX * K * R / stdR * -1 * exp(t * 1000000 * f) / j * t * 1000000) ** 2 * sf ** 2
        e8 = (V / XX * K * R / stdR * -1 * stdR / j * -1) ** 2 * sj ** 2
        e9 = (V / XX * K * R / stdR * -1 * exp(t * 1000000 * f) / j * f * 1000000 +
              V / XX * R * (K + 1) * 1000000 / V) ** 2 * st ** 2
        try:
            k0 = V * log(XX)
        except ValueError:
            k0, k1, k2, k3 = 0, 0, 0, 0
        else:
            k1 = pow((V / XX) ** 2 * sXX_2 ** 2, 0.5)  # analytical error
            k2 = pow((V / XX) ** 2 * sXX_1 ** 2, 0.5)  # internal error
            '''the calculation of total external error still has a little mistakes'''
            '''there are different method to calculate age by Min 2000, '''
            '''depending on using primary standard or other settings'''
            k3 = pow(e1 + e2 + e3 + e4 + e5 + e6 + e7 + e8 + e9, 0.5)  # total external error
            # k3 = pow(log(XX) ** 2 * sV ** 2 + k2 ** 2, 0.5)  # total external error
        [k0, k1, k2, k3] = [i / 1000000 for i in [k0, k1, k2, k3]]  # change to Ma

    return k0, k1, k2, k3


def err_wtd_mean(a0: list, e0: list, sf: int = 1, adjust_error: bool = True):
    """
    :param a0: x
    :param e0: error
    :param sf: sigma number for age error, default = 1
    :param adjust_error: adjust error by multiply Sqrt(MSWD)
    :return: error-weighted mean value | error in 1 sigma | number of data points | MSWD
    """
    e0 = [i / sf for i in e0]  # change error to 1 sigma
    n = len(a0)
    wt = [1 / i ** 2 if i > 0 else 0 for i in e0]  # error weighting
    k0 = sum([a0[i] * wt[i] for i in range(n)]) / sum(wt)  # error-weighted value
    k3 = sum([(a0[i] - k0) ** 2 * wt[i] for i in range(n)]) / (n - 1)  # MSWD mentioned in Min et al., 2000
    if adjust_error:
        k1 = pow(k3 / sum(wt), 0.5)  # error of mean age using equation mentioned by Min et al. (2000)
    else:
        k1 = pow(1 / sum(wt), 0.5)  # ArArCALC实际是利用加权平均计算总40r/39k，再计算年龄
    k2 = n
    print('wtd_mean value: %s ± %s, dp = %s, MSWD = %s' % (k0, k1, k2, k3))
    return k0, k1, k2, k3


def wtd_york2_regression(x: list, sx: list, y: list, sy: list, ri: list, sf: int = 1, **kwargs):
    """
    :param x: isochron x-axis
    :param sx: standard error of x
    :param y: isochron y-axis, y = b + m * x
    :param sy: standard error of y
    :param ri: relative coefficient of errors of x and y
    :param sf: factor of error, default = 1, meaning inputted errors are in 1 sigma
    :return: Intercept | Error | slope | Error | MSWD | Convergence | Number of Iterations | error magnification | other
     b, sb, a, sa, mswd, dF, Di, k
    """
    conv_tol = kwargs.pop('convergence', 0.001)
    iter_num = kwargs.pop('iteration', 100)
    n = len(x)
    sx = [i / sf for i in sx]  # change to 1 sigma
    sy = [i / sf for i in sy]  # change to 1 sigma
    temp_lst = intercept_linest(y, x, external=True)
    b, seb, m, sem = temp_lst[0], temp_lst[1], temp_lst[5][0], temp_lst[6][0]
    delta_m = abs(m)
    Di = 0
    mswd, k = 1, 1
    X, sX, Y, sY, R = list(x), list(sx), list(y), list(sy), list(ri)

    while delta_m >= abs(m * conv_tol / 100):
        Di = Di + 1
        U = []
        V = []
        Up = []
        Lo = []
        S = []

        wX = [1 / i ** 2 if i != 0 else 1 for i in sX]
        wY = [1 / i ** 2 if i != 0 else 1 for i in sY]
        Z = list(
            map(lambda wXi, wYi, Ri: (wXi * wYi) / (m ** 2 * wYi + wXi - 2 * m * Ri * (wXi * wYi) ** 0.5), wX, wY, R))
        sumZY = sum(list(map(lambda Zi, Yi: Zi * Yi, Z, Y)))
        sumZX = sum(list(map(lambda Zi, Xi: Zi * Xi, Z, X)))
        b = sumZY / sum(Z) - m * sumZX / sum(Z)

        for i in range(n):
            Ui = X[i] - sumZX / sum(Z)
            Vi = Y[i] - sumZY / sum(Z)
            U.append(Ui)
            V.append(Vi)

            Upi = Z[i] ** 2 * Vi * (Ui / wY[i] + m * Vi / wX[i] - R[i] * Vi / (wX[i] * wY[i]) ** 0.5)
            Loi = Z[i] ** 2 * Ui * (Ui / wY[i] + m * Vi / wX[i] - m * R[i] * Ui / (wX[i] * wY[i]) ** 0.5)
            Up.append(Upi)
            Lo.append(Loi)

            Si = Z[i] * (Y[i] - m * X[i] - b) ** 2
            S.append(Si)

        sumUUZ = sum(list(map(lambda ui, zi: ui * ui * zi, U, Z)))
        sumXXZ = sum(list(map(lambda xi, zi: xi * xi * zi, X, Z)))

        new_m = sum(Up) / sum(Lo)
        delta_m = abs(m - new_m)
        m = new_m
        sem = pow(1 / sumUUZ, 0.5)
        seb = pow(sumXXZ / sum(Z), 0.5) * sem
        mswd = sum(S) / (n - 2)

        if mswd > 1:
            k = pow(mswd, 0.5)  # k为误差放大系数
        else:
            k = 1

        sem = sem * k
        seb = seb * k

        if Di >= iter_num:
            break

    print('----------------------------------------------------------------')
    print('截距>>>' + str(b) + '  ' + '误差>>>' + str(seb))
    print('斜率>>>' + str(m) + '  ' + '误差>>>' + str(sem))
    print('Absolute Convergence' + '>>>' + str(delta_m))
    print('Number of Iterations' + '>>>' + str(Di))
    print('MSWD' + '>>>' + str(mswd))
    print('Error Magnification>>>' + str(k))
    print('----------------------------------------------------------------')
    return b, seb, m, sem, mswd, delta_m, Di, k


def isochron_age(x: list, sx: list, y: list, sy: list, ri: list, j: float, rsj: float, f: float, rsf: float,
                 uf: int = 1, isNormal: bool = False, isInverse: bool = False, statistics: bool = False, **kwargs):
    """
    :param x: isochron x-axis
    :param sx: error of x
    :param y: isochron y-axis
    :param sy: error of y
    :param ri: relative coefficient of errors of x and y
    :param j: J value
    :param rsj: relative error of J value in 1 sigma
    :param f: total decay constants of K
    :param rsf: relative error of f in 1 sigma
    :param uf: error precision of sx and sy, default = 1 sigma
    :param isNormal: isNormal is True when calculating normal isochron data else False
    :param isInverse: isInverse is True when calculating inverse isochron data else False
    :param statistics: return all statistic data when True
    :return: 40Ara/36Ara | error in 1 sigma | 40Arr/39Ark | error in 1 sigma | age | analyse error | internal error |
             external error | MSWD
             additional return: b, seb, m, sem, convergence, iterations, error magnification
    """
    conv_tol = kwargs.pop('convergence', 0.001)
    iter_num = kwargs.pop('iteration', 100)
    if not (isNormal or isInverse) or (isNormal and isInverse):
        print('isochron type was not assigned')
        return None
    sx = [i / uf for i in sx]
    sy = [i / uf for i in sy]
    b, seb, m, sem, mswd, conv, Di, errmag = wtd_york2_regression(x, sx, y, sy, ri,
                                                                  convergence=conv_tol, iteration=iter_num)
    if isNormal:
        k0 = m
        k1 = sem
        k2 = b
        k3 = seb
        k4, k5, k6, k7 = calc_age(m, sem, j, rsj, f, rsf)
    else:
        k0 = 1 / b
        k1 = error_div((1, 0), (b, seb))
        new_b, new_seb, new_m, new_sem, mswd, conv, Di, errmag = wtd_york2_regression(y, sy, x, sx, ri,
                                                                                      convergence=conv_tol,
                                                                                      iteration=iter_num)
        k2 = 1 / new_b
        k3 = error_div((1, 0), (new_b, new_seb))
        k4, k5, k6, k7 = calc_age(k2, k3, j, rsj, f, rsf)
    if statistics:
        return k0, k1, k2, k3, k4, k5, k6, k7, mswd, b, seb, m, sem, conv, Di, errmag
    else:
        return k0, k1, k2, k3, k4, k5, k6, k7, mswd


def isochron_age_ols(x: list, y: list, j: float, rsj: float, f: float, rsf: float,
                     isNormal: bool = False, isInverse: bool = False):
    """
    :param x: isochron x-axis
    :param y: isochron y-axis
    :param j: J value
    :param rsj: relative error of J value in 1 sigma
    :param f: total decay constants of K
    :param rsf: relative error of f in 1 sigma
    :param isNormal: isNormal is True when calculating normal isochron data else False
    :param isInverse: isInverse is True when calculating inverse isochron data else False
    :return: 40Ara/36Ara | error in 1 sigma | 40Arr/39Ark | error in 1 sigma | age | analyse error | internal error |
             external error | MSWD
             additional return: b, seb, m, sem, convergence, iterations, error magnification
    """
    if not (isNormal or isInverse) or (isNormal and isInverse):
        print('isochron type was not assigned')
        return None
    b, seb, rseb, r2, mswd, [m], [sem] = intercept_linest(y, x, external=False)
    if isNormal:
        k0 = m
        k1 = sem
        k2 = b
        k3 = seb
        k4, k5, k6, k7 = calc_age(m, sem, j, rsj, f, rsf)
    else:
        k0 = 1 / b
        k1 = error_div((1, 0), (b, seb))
        new_b, new_seb, new_rseb, new_r2, mswd, [new_m], [new_sem] = intercept_linest(x, y, external=False)
        k2 = 1 / new_b
        k3 = error_div((1, 0), (new_b, new_seb))
        k4, k5, k6, k7 = calc_age(k2, k3, j, rsj, f, rsf)
    return k0, k1, k2, k3, k4, k5, k6, k7, mswd, b, seb, m, sem, '', '', ''


def get_ar40rar39k(x: list, sx: list, y: list, sy: list, rho: list, atm_ratio=None, satm_ratio=None,
                   isInverse: bool = True):
    """
    :param x: Ar39k / Ar40a+r or Ar39k / Ar36a
    :param sx:
    :param y: Ar36a / Ar40a+r or Ar40a+r / Ar36a
    :param sy:
    :param rho: correlations between x and y, should be introduced into error propagation
    :param atm_ratio: Ar40 / Ar36, used to deduct Ar40a from Ar40a+r
    :param satm_ratio: error of Ar40 / Ar36 ratio, but is not introduced into error propagation
    :param isInverse:
    :return: Ar40r / Ar39k, error of Ar40r / Ar39k
    """
    n = min(len(x), len(sx), len(y), len(sy))
    if atm_ratio is None and satm_ratio is None:
        atm_ratio = satm_ratio = [0] * n
    elif isinstance(atm_ratio, float) and isinstance(satm_ratio, float):
        atm_ratio = [atm_ratio] * n
        satm_ratio = [satm_ratio] * n
    elif isinstance(atm_ratio, list) and isinstance(satm_ratio, list):
        n = min(len(atm_ratio), len(satm_ratio)) if 0 < min(len(atm_ratio), len(satm_ratio)) < n else n
    x, sx, y, sy, rho, = x[:n], sx[:n], y[:n], sy[:n], rho[:n]
    atm_ratio, satm_ratio = atm_ratio[:n], satm_ratio[:n]
    '''Error of initial is ignored, and correlations between x and y should be considered'''
    if isInverse:
        f = list(map(lambda xi, yi, atmi: (1 - atmi * yi) / xi, x, y, atm_ratio))
        v0 = list(map(lambda xi, sxi, yi, atmi: ((1 - atmi * yi) / xi ** 2) ** 2 * sxi ** 2, x, sx, y, atm_ratio))
        v1 = list(map(lambda xi, syi, atmi: (atmi / xi) ** 2 * syi ** 2, x, sy, atm_ratio))
        v2 = list(map(lambda xi, sxi, yi, syi, ri, atmi: 2 * (1 - atmi * yi) * atmi * ri * sxi * syi / xi ** 3,
                      x, sx, y, sy, rho, atm_ratio))
        sf = list(map(lambda v0i, v1i, v2i: pow(v0i + v1i + v2i, 0.5), v0, v1, v2))
    else:
        f = list(map(lambda xi, yi, atmi: (yi - atmi) / xi, x, y, atm_ratio))
        v0 = list(map(lambda xi, sxi, yi, atmi: ((yi - atmi) / xi ** 2) ** 2 * sxi ** 2, x, sx, y, atm_ratio))
        v1 = list(map(lambda xi, syi: (1 / xi) ** 2 * syi ** 2, x, sy))
        v2 = list(map(lambda xi, sxi, yi, syi, ri, atmi: 2 * (atmi - yi) * sxi * syi * ri / xi ** 3,
                      x, sx, y, sy, rho, atm_ratio))
        sf = list(map(lambda v0i, v1i, v2i: pow(v0i + v1i + v2i, 0.5), v0, v1, v2))
    return f, sf


def error_cor(sX: float, sY: float, sZ: float):
    """
    :param sX: relative error of X, where X/Z vs. Y/Z
    :param sY: relative error of Y
    :param sZ: relative error of Z
    :return:
    """
    if sZ == 0:
        return None
    k = pow(1 / ((1 + sX ** 2 / sZ ** 2) * (1 + sY ** 2 / sZ ** 2)), 0.5)
    return k


'---------------------------'
'--Extrapolation Functions--'
'---------------------------'
def intercept_average(a0: list):
    """
    :param a0: known_y's
    :return: intercept | standard error | relative error | r2: str = None
    """
    df = len(a0) - 1
    k0 = sum(a0) / len(a0)
    k1 = pow(sum([(i - k0) ** 2 for i in a0]) / df, 0.5)  # standard deviation
    k2 = k1 / k0 * 100  # relative standard error
    k3 = 'None'  # determination coefficient
    return k0, k1, k2, k3


def intercept_weighted_least_squares(a0: list, a1: list):
    """
    :param a0: known_y's
    :param a1: known_x's
    :return: intercept | standard error | relative error | R2 | [m] | [sem]
    """
    """
    y = m * x + b, 
    """
    b0, seb0, rseb0, r2, mswd, [m0], [rem0] = intercept_linest(a0, a1, external=True)
    y0 = list(map(lambda i: m0 * i + b0, a1))
    resid = list(map(lambda i, j: i - j, y0, a0))
    weight = list(map(lambda i: 1 / i ** 2, resid))  # Use weighting by inverse of the squares of residual

    sum_wi = sum(weight)
    sum_wiyi = sum(list(map(lambda i, j: i * j, weight, a0)))
    sum_wixi = sum(list(map(lambda i, j: i * j, weight, a1)))
    sum_wiyixi = sum(list(map(lambda i, j, g: i * j * g, weight, a0, a1)))
    sum_wixixi = sum(list(map(lambda i, j, g: i * j * g, weight, a1, a1)))

    m = (sum_wiyixi - sum_wixi * sum_wiyi / sum_wi) / (sum_wixixi - sum_wixi * sum_wixi / sum_wi)
    b = (sum_wiyi - m * sum_wixi) / sum_wi
    a0 = list(map(lambda i, j: i * j, weight, a0))
    a1 = list(map(lambda i, j: i * j, weight, a1))
    b, seb, rseb, r2, mswd, [m], [rem] = intercept_linest(a0, a1, external=True, weight=weight)
    return b, seb, rseb, r2, [m], [rem]


def intercept_linest(a0: list, a1: list, *args, external=False, weight: list = None):
    """
    :param a0: known_y's, y = b + m * x
    :param a1: known_x's
    :param args: more known_x's
    :param external: external = True when is called by other fitting functions, default = False
    :param weight: necessary when weighted least squares fitting
    :return: intercept | standard error | relative error | R2 | MSWD | other params: list | error of other params: list
    """
    '''beta = (xTx)^-1 * xTy >>> xtx * beta = xty'''
    '''crate matrix of x and y, calculate the transpose of x'''
    m = len(a1)  # number of data
    n = len(args) + 2  # number of unknown x, constant is seen as x^0
    if len(a0) < 3 or len(a0) != len(a1):
        return
    if weight is not None:
        xlst = [weight, a1, *args]
    else:
        xlst = [[1] * m, a1, *args]
    ylst = a0
    xtx = list()
    xty = list()
    for i in range(n):
        xtx.append([])
        xty.append([])
        xty[i] = sum([xlst[i][k] * ylst[k] for k in range(m)])
        for j in range(n):
            xtx[i].append([])
            xtx[i][j] = sum([xlst[i][k] * xlst[j][k] for k in range(m)])
    '''solve the system of linear equations using LU factorization algorithm'''
    '''LU * beta = xty, U * beta = b, L * b = xty'''
    l: List[List[Any]] = list()
    u: List[List[Any]] = list()
    b: List[Any] = list()
    beta: List[Any] = list()
    for i in range(n):
        l.append([])
        u.append([])
        b.append([])
        beta.append([])
        for j in range(n):
            l[i].append([])
            u[i].append([])
            if j > i:
                l[i][j] = 0
            elif i > j:
                u[i][j] = 0
            else:
                l[i][j] = 1
    for i in range(n):
        if i >= 1:
            l[i][0] = xtx[i][0] / u[0][0]
        for j in range(n):
            if i == 0:
                u[i][j] = xtx[i][j]
            elif i == 1 and j >= 1:
                u[i][j] = xtx[i][j] - l[i][0] * u[0][j]
            elif i < n - 1:
                if j in range(1, i):
                    l[i][j] = (xtx[i][j] - sum([l[i][r] * u[r][j] for r in range(j)])) / u[j][j]
                if j in range(i, n):
                    u[i][j] = xtx[i][j] - sum([l[i][r] * u[r][j] for r in range(i)])
            elif i == n - 1:
                if j in range(1, i):
                    l[n - 1][j] = (xtx[n - 1][j] - sum([l[n - 1][r] * u[r][j] for r in range(j)])) / u[j][j]
                if j == n - 1:
                    u[i][j] = xtx[i][j] - sum([l[i][r] * u[r][j] for r in range(i)])
    '''calculate matrix b, L * b = y'''
    b[0] = xty[0]
    for i in range(1, n):
        b[i] = xty[i] - sum([l[i][j] * b[j] for j in range(i)])
    '''calculate matrix beta, b = U * beta'''
    beta[n - 1] = b[n - 1] / u[n - 1][n - 1]
    for i in [n - k for k in range(2, n + 1)]:
        beta[i] = (b[i] - sum([u[i][j] * beta[j] for j in range(i + 1, n)])) / u[i][i]

    '''calculate the inverse of matrix xTx'''
    inv_l: List[List[Any]] = list()
    inv_u: List[List[Any]] = list()
    for i in range(n):
        inv_l.append([])
        inv_u.append([])
        for j in range(n):
            inv_l[i].append([])
            inv_u[i].append([])
            if i == j:
                inv_l[i][j] = 1 / l[i][j]
                inv_u[i][j] = 1 / u[i][j]
            elif i > j:
                inv_u[i][j] = 0
            elif j > i:
                inv_l[i][j] = 0

    for j in range(1, n):
        for i in range(n - 1):
            if i + j > n - 1:
                break
            else:
                inv_u[i][i + j] = -1 * sum([u[i][k] * inv_u[k][i + j] for k in range(i + 1, i + j + 1)]) / u[i][i]
            if i + j > n - 1:
                break
            else:
                inv_l[i + j][i] = -1 * sum([l[i + j][k] * inv_l[k][i] for k in range(i, i + j)]) / l[i + j][i + j]

    '''inv_xTx = inv_u * inv_l'''
    inv_xtx: List[List[Any]] = list()
    for i in range(n):
        inv_xtx.append([])
        for j in range(n):
            inv_xtx[i].append([])
            inv_xtx[i][j] = sum([inv_u[i][k] * inv_l[k][j] for k in range(n)])
    # pow(inv_xtx[0][0], 0.5) is the errF in Excel Linest function

    '''calculate Y values base on the fitted formula'''
    estimate_y = [sum([xlst[j][i] * beta[j] for j in range(n)]) for i in range(m)]
    resid = [(estimate_y[i] - a0[i]) ** 2 for i in range(m)]
    reg = [(i - sum(estimate_y) / len(estimate_y)) ** 2 for i in estimate_y]
    ssresid = sum(resid)  # residual sum of squares / sum squared residual
    ssreg = sum(reg)  # regression sum of square
    sstotal = ssreg + ssresid  # total sum of squares
    df = m - n + 1 - 1  # df = degree of freedom
    m_ssresid = ssresid / df
    se_beta = [pow(m_ssresid * inv_xtx[i][i], 0.5) for i in range(n)]
    rseb = (se_beta[0] / beta[0]) * 100 if beta[0] != 0 else se_beta[0]  # relative error of intercept
    try:
        r2 = ssreg / sstotal  # r2 = ssreg / sstotal
    except ZeroDivisionError:
        r2 = 1
    try:
        mswd = sum(list(map(lambda resid_i, reg_i: (resid_i ** 2) / (reg_i ** 2), resid, reg))) / (m - 1)
    except ZeroDivisionError:
        mswd = 9999
    if not external:
        pass
    return beta[0], se_beta[0], rseb, r2, mswd, beta[1:], se_beta[1:]


def intercept_parabolic(a0: list, a1: list):
    """
    :param a0: known_y's, y = b + m1 * x + m2 * x ^ 2
    :param a1: known_x's
    :return: intercept | standard error | relative error | MSWD | [m1, m2] | [sem1, sem2]
    """
    """
    y = b + m1 * x + m2 * x ^ 2
    """
    b, seb, rseb, r2, mswd, [m1, m2], [sem1, sem2] = intercept_linest(a0, a1, [i ** 2 for i in a1], external=True)
    return b, seb, rseb, r2, mswd, [m1, m2], [sem1, sem2]


def intercept_logest(a0: list, a1: list):
    """
    :param a0: known_y's, y = b * m ^ x
    :param a1: known_x's
    :return: intercept | standard error | relative error | R2 | MSWD | m | sem
    """
    """
    y = b * m ^ x, Microsoft Excel LOGEST function, ln(y) = ln(b) + ln(m) * x
    """
    a0 = [log(i) for i in a0]  # ln(y)
    b, seb, rseb, r2, mswd, [lnm], [selnm] = intercept_linest(a0, a1, external=True)
    b = exp(b)
    m = exp(lnm)
    sem = exp(lnm) * selnm
    seb = b * seb  # Excel.Logest function do not consider the error propagation
    rseb = seb / b * 100
    return b, seb, rseb, r2, mswd, m, sem


def intercept_exponential(a0: list, a1: list, slope: float, curvature: float):
    """
    :param a0: known_y's, y = m * exp(c * x) + b
    :param a1: known_x's
    :param slope: m in y = b + m * x
    :param curvature: m2 in y = b + m1 * x + m2 * x ^ 2
    :return: intercept | standard error of intercept | relative error | R2 | MSWD | [m, c, b] | [sem, sec, seb]
    """
    intercept, se_intercept, rse_intercept, r2 = None, None, None, None
    m, sem, c, b, seb, rseb = None, None, None, None, None, None
    n = len(a1)  # number of data points
    ubound_regression = 10000  # max number of regression is 100000
    num_reg = 0  # record the number of regression
    '''determine initial curvature coefficient'''
    sgn = 1 if slope * curvature > 0 else -1 if slope * curvature < 0 else 0
    try:
        curv_coeff = abs(slope) / (max(a0) - min(a0)) * sgn
    except ZeroDivisionError as e:
        print(e)
        return
    stp = 1 / 100
    c = curv_coeff * (1 - stp)
    temp = 0
    r2 = 0.00005
    mswd = 9999
    while temp < r2:
        if num_reg >= ubound_regression:
            print('达到迭代上限')
            break
        else:
            pass
        temp = r2
        c = c * (1 - stp)
        '''y = m * z + b while z = exp(c * x)'''
        z = [exp(c * i) for i in a1]
        b, seb, rseb, r2, mswd, [m], [sem] = intercept_linest(a0, z, external=True)
        intercept = b + m
        '''calculate error of intercept'''
        errfz = pow(sum([i ** 2 for i in z]) / (n * sum([i ** 2 for i in z]) - sum(z) ** 2), 0.5)
        errfx = pow(sum([i ** 2 for i in a1]) / (n * sum([i ** 2 for i in a1]) - sum(a1) ** 2), 0.5)
        '''seb = errfz * sey = errfz * ssresid / df -> se_intercept = sey * errfx = seb / errfz * errfx'''
        se_intercept = seb / errfz * errfx
        rse_intercept = se_intercept / intercept * 100
        num_reg += 1
    return intercept, se_intercept, rse_intercept, r2, mswd, [m, c, b], [sem, 0, seb]


'---------------------'
'--Error Propagation--'
'---------------------'
def error_add(*args: float):
    """
    :param args: errors in 1 sigma
    :return: propagated error
    """
    k = pow(sum([i ** 2 for i in args]), 0.5)
    return k


def error_mul(*args: tuple):
    """
    :param args: tuple of the value and its error
    :return: propagated error
    """
    e = []
    for i in range(len(args)):
        temp = 1
        for j in range(len(args)):
            if i != j:
                temp = temp * args[j][0]
        e.append(temp ** 2 * args[i][1] ** 2)
    k = pow(sum(e), 0.5)
    return k


def error_div(a0: tuple, a1: tuple):
    """
    :param a0: a tuple of the first number and its error
    :param a1: a tuple of another number and its error
    :return: propagated error
    """
    k = pow((-1 * a0[0] / a1[0] ** 2) ** 2 * a1[1] ** 2 + (1 / a1[0]) ** 2 * a0[1] ** 2, 0.5)
    return k


def error_pow(a0: tuple, a1: tuple):
    """
    :param a0: y = pow(a0, a1) -> y = a0 ^ a1
    :param a1:
    :return: propagated error
    """
    p1 = a0[1] ** 2 * (a1[0] * pow(a0[0], (a1[0] - 1))) ** 2
    p2 = a1[1] ** 2 * (pow(a0[0], a1[0]) * log(a0[0])) ** 2
    k = pow(p1 + p2, 0.5)
    return k


def error_log(a0: float, e0: float):
    """
    :param a0: y = ln(a0).
    :param e0: error in 1 sigma.
    :return: propagated error.
    """
    k = pow(e0 ** 2 * (1 / a0) ** 2, 0.5)
    return k


'---------------------'
'--Close Temperature--'
'---------------------'
def get_close_temp():
    return


'----------------'
'--Reading File--'
'----------------'
def read_file(filepath: str, filetype: int):
    """
    :param filepath: directory
    :param filetype: xls == 0, txt == 1, json == 2
    :return: dict for xls, list for txt
    """
    isXls = True if filetype == 0 else False
    isTxt = True if filetype == 1 else False
    isJson = True if filetype == 2 else False
    if isXls:
        try:
            wb = xlrd.open_workbook(filepath)
            sheets = wb.sheet_names()
            book_dict = {}
            for each_sheet_name in sheets:
                each_sheet_list = []
                sheet = wb.sheet_by_name(each_sheet_name)
                for row in range(sheet.nrows):
                    each_sheet_list.append([])
                    for col in range(sheet.ncols):
                        each_sheet_list[row].append(sheet.cell(row, col).value)
                book_dict[each_sheet_name] = each_sheet_list
        except Exception as e:
            print('error in read xls: %s' % str(e))
        else:
            return book_dict
    if isTxt:
        try:
            with open(filepath, 'r') as file:
                txt_list = file.readlines()
        except Exception as e:
            print('error in read txt: %s' % str(e))
        else:
            return txt_list
    if isJson:
        try:
            with open(filepath, 'r') as file:
                json_dict = json.load(file)
        except Exception as e:
            print('error in read json: %s' % str(e))
        else:
            return json_dict
    return False


def save_Json(filepath: str, filetype: int, data):
    """
    :param filepath:
    :param filetype:
    :param data:
    :return:
    """
    isXls = True if filetype == 0 else False
    isTxt = True if filetype == 1 else False
    isJson = True if filetype == 2 else False
    if isJson:
        try:
            with open(filepath, 'w') as file:
                jsonData = json.dumps(data, indent=4, separators=(',', ': '))
                file.write(jsonData)
                return
        except Exception as e:
            print('error in read json: %s' % str(e))
            return


def open_original_xls(filepath: str):
    """
    :param filepath: directory of file
    :return: step_list -> [[[header of step one], [cycle one in the step], [cycle two in the step]],[[],[]]]
    """
    try:
        wb = xlrd.open_workbook(filepath)
        sheets = wb.sheet_names()
        sheet = wb.sheet_by_name(sheets[0])
        value, first_item_list, first_row_list, step_list = [], [], [], []
        for row in range(sheet.nrows):
            row_set = []
            for col in range(sheet.ncols):
                if sheet.cell(row, col).value == '':
                    pass
                else:
                    row_set.append(sheet.cell(row, col).value)
            if row_set != [] and len(row_set) > 1:
                value.append(row_set)
        for each_row in value:
            if isinstance(each_row[0], float):
                each_row[0] = int(each_row[0])
                first_row_list.append(each_row)
                first_item_list.append(each_row[0])
        for each_step in range(len(first_item_list)):
            step_list.append([])
            step_list[each_step].append(first_row_list[each_step][0:4])
            row_start_number = value.index(first_row_list[each_step])
            try:
                row_stop_number = value.index(first_row_list[each_step + 1])
            except IndexError:
                row_stop_number = len(value) + 1
            internal_steps = [value[i] for i in range(row_start_number + 2, row_stop_number - 7, 1)]
            for i in internal_steps:
                step_list[each_step].append(i)
        if value[0][0] != 'No':
            raise Exception('Wrong file')
    except Exception as e:
        print('Error in opening original excel file: %s' % str(e))
    else:
        return step_list


def open_filtered_xls(filepath: str):
    """
    :param filepath: directory of file
    :return: list = [dict, dict]
    """
    header = 2
    wb = xlrd.open_workbook(filepath)
    try:
        sheet_1 = wb.sheet_by_name('Intercept Value')
        sheet_2 = wb.sheet_by_name('Procedure Blanks')
        if sheet_1.nrows != sheet_2.nrows:
            raise IndexError('Row counts differ')
    except xlrd.biffh.XLRDError as e:
        print('Error in opening filtered excel file: %s' % str(e))
        return False
    except IndexError as e:
        print('Error in opening filtered excel file: %s' % str(e))
        return False
    else:
        '''reading intercept sheet'''
        intercept_value = [[sheet_1.cell(row, col).value for col in range(sheet_1.ncols)] for row in
                           range(header, sheet_1.nrows)]
        '''reading blank sheet'''
        blank_value = [[sheet_2.cell(row, col).value for col in range(sheet_2.ncols)] for row in
                       range(header, sheet_2.nrows)]
        '''remember as dicts'''
        dict_intercept, dict_blank = {}, {}
        for row in range(len(intercept_value)):
            dict_intercept[intercept_value[row][0]] = intercept_value[row]
            dict_blank[intercept_value[row][0]] = blank_value[row]
        return [dict_intercept, dict_blank]


def open_age_xls(filepath: str):
    """
    :param filepath:
    :return:
    """
    return False


def export_xls_isochron(export_files_path: str, plot_data: dict, label=None):
    """
    :param export_files_path: export file path
    :param plot_data: dict at least containing keys of 'X', 'Y', 'Intercept', 'Slope' and ' Statistics'
    :param label:
    :return:
    """
    if label is None:
        label = ['Tittle', 'X Axis', 'Y Axis']
    xls = xlsxwriter.Workbook(export_files_path)
    '''create new worksheets'''
    sht_data = xls.add_worksheet('PlotData')
    sht_plot = xls.add_chartsheet(label[0])
    '''write data'''
    sht_data.write_column('A1', plot_data['X'])
    sht_data.write_column('B1', plot_data['Y'])
    sht_data.write_column('C1', plot_data['Intercept'])
    sht_data.write_column('D1', plot_data['Slope'])
    sht_data.write_column('E1', plot_data['Statistics'])
    '''draw figure'''
    isochron = xls.add_chart({'type': 'scatter'})
    isochron.add_series({'name': 'Selected Points',
                         'categories': 'PlotData!$A$1:$A$%s' % (len(plot_data['X'])),
                         'values': 'PlotData!$B$1:$B$%s' % (len(plot_data['Y'])),
                         'line': {'none': True},
                         'marker': {'type': 'square',
                                    'size': 8,
                                    'border': {'color': 'black'},
                                    'fill': {'color': '#1E90FF'}}})
    isochron.add_series({'name': 'Normal Isochron Line',
                         'categories': '={%s,%s}' % (plot_data['Intercept'][2],
                                                     plot_data['Intercept'][3]),
                         'values': '={%s,%s}' % (plot_data['Slope'][2],
                                                 plot_data['Slope'][3]),
                         'line': {'color': '#1E90FF', 'width': 1.5},
                         'marker': {'type': 'none'}})
    isochron.set_chartarea({'border': {'none': True, 'width': 1.5}, 'fill': {'color': '#FFFFFF'}})
    isochron.set_plotarea({'border': {'color': 'black'}, 'fill': {'color': '#FFE4B5'}})
    isochron.set_legend({'none': True})
    isochron.set_title({'name': label[0], 'name_font': {'size': 16, 'color': '#000000'}})
    isochron.set_x_axis({'name': label[1], 'name_font': {'size': 12, 'bold': True, 'color': '#000000'},
                         'num_font': {'italic': True}, 'major_gridlines': {'visible': True,
                                                                           'line': {'width': 1.25,
                                                                                    'dash_type': 'dash'}},
                         'min': 0, 'max': max(plot_data['X']) * 1.2, })
    isochron.set_y_axis({'name': label[2], 'name_font': {'size': 12, 'bold': True, 'color': '#000000'},
                         'num_font': {'italic': True}, 'major_gridlines': {'visible': True,
                                                                           'line': {'width': 1.25,
                                                                                    'dash_type': 'dash'}},
                         'min': 0, 'max': max(plot_data['Y']) * 1.2, })
    sht_plot.set_chart(isochron)
    '''hide data sheet'''
    sht_plot.activate()
    sht_data.hide()
    try:
        xls.close()
    except Exception as e:
        print('Error in rewriting xls: %s' % str(e))


def export_xls_spectra(export_files_path: str, plot_data: dict):
    """
    :param export_files_path: export file path
    :param plot_data: dict containing keys of 'Ar39%', 'Line_1' and 'Line_2'
    :return:
    """
    xls = xlsxwriter.Workbook(export_files_path)
    '''create new worksheets'''
    sht_data = xls.add_worksheet('PlotData')
    sht_plot = xls.add_chartsheet('Age Spectra')
    '''write data'''
    sht_data.write_column('A1', plot_data['Ar39%'])
    sht_data.write_column('B1', plot_data['Line_1'])
    sht_data.write_column('C1', plot_data['Line_2'])
    '''draw figure'''
    spectra_diagram = xls.add_chart({'type': 'scatter'})
    spectra_diagram.add_series({'name': 'Line 1', 'categories': 'PlotData!$A$1:$A$%s' % (len(plot_data['Ar39%'])),
                                'values': 'PlotData!$B$1:$B$%s' % (len(plot_data['Line_1'])),
                                'line': {'color': '#DC143C', 'width': 1.5},
                                'marker': {'type': 'none'}, })
    spectra_diagram.add_series({'name': 'Line 2', 'categories': 'PlotData!$A$1:$A$%s' % (len(plot_data['Ar39%'])),
                                'values': 'PlotData!$C$1:$C$%s' % (len(plot_data['Line_2'])),
                                'line': {'color': '#DC143C', 'width': 1.5},
                                'marker': {'type': 'none'}, })
    spectra_diagram.set_chartarea({'border': {'none': True}, 'fill': {'color': '#FFFFFF'}})
    spectra_diagram.set_plotarea({'border': {'color': 'black', 'width': 1.5}, 'fill': {'color': '#FFE4B5'}})
    spectra_diagram.set_legend({'none': True})
    spectra_diagram.set_title({'name': 'Spectra Diagram', 'name_font': {'size': 16, 'color': '#000000'}})
    script = xls.add_format()
    script.set_font_script(font_script=1)
    sht_data.write_rich_string('F1', 'Cumulative ', script, '39', 'Ar released (%)')
    spectra_diagram.set_x_axis({'name': 'PlotData!$F$1',
                                'name_font': {'size': 12, 'bold': True, 'color': '#000000'},
                                'num_font': {'italic': True}, 'major_gridlines': {'visible': True,
                                                                                  'line': {'width': 1.25,
                                                                                           'dash_type': 'dash'}},
                                'min': 0, 'max': 100, })
    spectra_diagram.set_y_axis({'name': 'Apparent age (Ma)',
                                'name_font': {'size': 12, 'bold': True, 'color': '#000000'},
                                'num_font': {'italic': True}, 'major_gridlines': {'visible': True,
                                                                                  'line': {'width': 1.25,
                                                                                           'dash_type': 'dash'}},
                                'min': min(plot_data['Line_1']) * 0.5, 'max': max(plot_data['Line_1']) * 1.5, })
    sht_plot.set_chart(spectra_diagram)
    '''hide data sheet'''
    sht_plot.activate()
    sht_data.hide()
    try:
        xls.close()
    except Exception as e:
        print('Error in rewriting xls: %s' % str(e))


'----------------'
'--Draw Figures--'
'----------------'
def get_default_canvas(**kwargs):
    """
    :kwargs: properties including x_label, y_label, title
    :return: canvas: FigureCanvasQTAgg
    """
    '''create fig and canvas'''
    fig = pyplot.Figure(dpi=100, constrained_layout=True)
    canvas = FigureCanvas(fig)
    '''set axes'''
    canvas.axes = fig.subplots()
    canvas.axes.tick_params(labelsize=6, direction='in')
    font = {'family': 'Microsoft YaHei Ui', 'size': 12, 'style': 'normal'}
    canvas.axes.set_xlabel(kwargs.pop('x_label', ''), fontdict=font)
    canvas.axes.set_ylabel(kwargs.pop('y_label', ''), fontdict=font)
    font = {'family': 'Microsoft YaHei Ui', 'size': 16, 'weight': 'bold'}
    canvas.axes.set_title(kwargs.pop('title', ''), fontdict=font)
    return canvas


def get_spectra(age: list, sage: list, Ar39k_list: list, plateau_steps: list = None, uf: int = 1, plt_sfactor: int = 1,
                **kwargs):
    """
    :param age:
    :param sage: 1 sigma
    :param Ar39k_list:
    :param plateau_steps: plateau steps index
    :param uf:
    :param plt_sfactor:
    :return: canvas, x, y1, y2
    """
    kwargs = kwargs.pop('properties', kwargs)
    '''spectra line properties'''
    showLabel = kwargs.pop('showLabel', True)  # display step numbers
    line_width = kwargs.pop('spectra_w', 0)  # line width
    line_style = kwargs.pop('spectra_s', 'none')  # line style
    spectra_b_c = kwargs.pop('spectra_b_c', 'none')  # spectra line color
    spectra_f_c = kwargs.pop('spectra_f_c', 'none')  # spectra fill color
    plateau_b_c = kwargs.pop('plateau_b_c', 'none')  # plateau line color
    plateau_f_c = kwargs.pop('plateau_f_c', 'none')  # plateau fill color
    '''calculate points'''
    sum_39Ark = sum(Ar39k_list);
    n = len(Ar39k_list)
    '''error and unit'''
    sage = [i * plt_sfactor for i in sage]
    age = [i * uf for i in age]
    sage = [i * uf for i in sage]
    # k1、k2、k3、k4为中间过渡参数，x为年龄谱散点横坐标，y1、y2为年龄谱两条线的纵坐标
    k1 = []
    k2 = []
    k3 = []
    k4 = []
    y1 = []
    y2 = []
    x = []
    n = len(age)
    for i in range(n):
        y_uplimit = age[i] + sage[i]
        y_lowlimit = age[i] - sage[i]
        k1.append(y_uplimit)
        k2.append(y_lowlimit)
        k4.append(float(Ar39k_list[i] / sum_39Ark))
        k3.append(sum(k4))
    for i in range(n + 1):
        if i == 0:
            x.append(0)
            y1.append(k1[i])
            y2.append(k2[i])
        elif i < n:
            x.append(k3[i - 1])
            x.append(k3[i - 1])
            if i % 2 == 1:
                y1.append(k1[i - 1])
                y1.append(k2[i])
                y2.append(k2[i - 1])
                y2.append(k1[i])
            elif i % 2 == 0:
                y2.append(k1[i - 1])
                y2.append(k2[i])
                y1.append(k2[i - 1])
                y1.append(k1[i])
        elif i == n:
            x.append(1)
            if i % 2 == 1:
                y1.append(k1[i - 1])
                y2.append(k2[i - 1])
            elif i % 2 == 0:
                y2.append(k1[i - 1])
                y1.append(k2[i - 1])
        else:
            pass
    x = [x[i] * 100 for i in range(n * 2)]
    '''create canvas'''
    x_label = 'Cumulative ' + r'$\mathregular{^{39}Ar}$' + ' released (%)'
    y_label = 'Apparent Age (Ma)'
    title = 'Age spectrum'
    canvas = get_default_canvas(x_label=x_label, y_label=y_label, title=title)
    '''spectra line'''
    canvas.axes.plot(x, y1, color=spectra_b_c, linestyle=line_style, linewidth=line_width, markersize=0)
    canvas.axes.plot(x, y2, color=spectra_b_c, linestyle=line_style, linewidth=line_width, markersize=0)
    if showLabel:
        for i in range(n):
            canvas.axes.annotate(str(i + 1), xy=((x[i * 2] + x[i * 2 + 1]) / 2, max(y1[i * 2], y2[i * 2])),
                                 xytext=(-5, 5), textcoords='offset points')
    canvas.axes.set_xlim(0, 100)
    canvas.axes.set_ylim(min(min(y1), min(y2)) * 0.5, max(max(y1), max(y2)) * 1.5)
    '''filling if the fill color is selected'''
    if spectra_f_c != 'none' and spectra_f_c is not None:
        for i in range(len(age)):
            fill_x = [x[i * 2], x[i * 2], x[i * 2 + 1], x[i * 2 + 1]]
            fill_y = [y1[i * 2], y2[i * 2], y2[i * 2 + 1], y1[i * 2 + 1]]
            canvas.axes.fill(fill_x, fill_y, spectra_f_c)
    return canvas, x, y1, y2


def get_isochron(x: list, sx: list, y: list, sy: list, rho: list, b: float = None, m: float = None,
                 isInverse: bool = True, plt_sfactor: int = 1, **kwargs):
    """
    :param x: horizontal axis value
    :param sx: error in 1 sigma
    :param y: horizontal axis value
    :param sy: error in 1 sigma
    :param rho: correlation coefficient
    :param b: straight line intercept
    :param m: straight line slope
    :param isInverse: True or False
    :param plt_sfactor: plot error factor, using in draw error ellipse
    :return: canvas
    """
    kwargs = kwargs.pop('properties', kwargs)
    '''scatter properties'''
    showLabel = kwargs.pop('showLabel', True)  # display scatter label
    scatter_size = kwargs.pop('scatter_size', 0)  # scatter size
    scatter_style = kwargs.pop('scatter_style', '.')  # scatter marker
    scatter_b_c = kwargs.pop('scatter_b_c', 'none')  # scatter border color
    scatter_f_c = kwargs.pop('scatter_f_c', 'none')  # scatter fill color
    showRandomPts = kwargs.pop('show_random_pts', False)  # show random points
    random_points_num = kwargs.pop('random_points_num', 1500)  # number of random points

    '''isochron line properties'''
    line_w = kwargs.pop('line_w', 0)  # line width
    line_s = kwargs.pop('line_s', 'none')  # line style
    line_c = kwargs.pop('line_c', 'none')  # line color
    '''ellipse properties'''
    drawEllipse = kwargs.pop('drawEllipse', False)  # draw ellipses
    ellipse_b_c = kwargs.pop('ellipse_b_c', 'none')  # ellipse border color
    ellipse_f_c = kwargs.pop('ellipse_f_c', 'none')  # ellipse fill color
    ellipse_l_w = kwargs.pop('ellipse_l_w', 'none')  # ellipse line width
    ellipse_f = False if ellipse_f_c == 'none' or ellipse_f_c is None else True

    isAuto = kwargs.pop('isAuto', True)  # auto axis
    ignoreLine = kwargs.pop('ignoreLine', True)  # ignore fitted straight line

    '''create canvas'''
    x_label = r'$\mathregular{^{39}Ar / ^{40}Ar}$' if isInverse else r'$\mathregular{^{39}Ar / ^{36}Ar}$'
    y_label = r'$\mathregular{^{36}Ar / ^{40}Ar}$' if isInverse else r'$\mathregular{^{40}Ar / ^{36}Ar}$'
    title = 'Inverse Isochron' if isInverse else 'Normal Isochron'
    canvas = get_default_canvas(x_label=x_label, y_label=y_label, title=title)

    '''plot scatter'''
    for i in range(len(x)):
        canvas.axes.scatter(x[i], y[i], c=scatter_f_c, edgecolors=scatter_b_c,
                            marker=scatter_style, s=scatter_size)
        if showLabel:
            canvas.axes.annotate(str(i + 1), xy=(x[i], y[i]), xytext=(5, 5),
                                 textcoords='offset points')
    top, bottom = canvas.axes.get_ybound()[1], canvas.axes.get_ybound()[0]
    left, right = canvas.axes.get_xbound()[0], canvas.axes.get_xbound()[1]
    '''plot line'''
    if b is not None and m is not None:
        canvas.axes.plot([0, max(x) * 10], [b, max(x) * 10 * m + b],
                         c=line_c, linewidth=line_w, linestyle=line_s)
        if isAuto and ignoreLine:
            canvas.axes.set_xlim(left, right)
            canvas.axes.set_ylim(bottom, top)
        elif isAuto:
            x_max = max(max(x), -b / m) * 1.1 if m != 0 else max(x) * 1.05
            y_max = max(max(y), x_max * m + b, b) * 1.05
            canvas.axes.set_xlim(0, x_max)
            canvas.axes.set_ylim(0, y_max)
    '''ellipse'''
    all_points = []
    for i in range(len(x)):
        Qxx = (sx[i]) ** 2
        Qxy = sx[i] * sy[i] * rho[i]
        Qyy = (sy[i]) ** 2
        '''calculate the ellipse's short semi-axial and long semi-axial'''
        k = pow((Qxx - Qyy) ** 2 + 4 * Qxy ** 2, 0.5)
        Qee = (Qxx + Qyy + k) / 2
        Qff = (Qxx + Qyy - k) / 2
        e = pow(Qee, 0.5)  # long semi-axial
        f = pow(Qff, 0.5)  # short semi-axial
        phi_e = atan((Qee - Qxx) / Qxy) if Qxy != 0 else 0 if Qxx >= Qyy else _pi / 2  # radian
        ellipse_1 = patches.Ellipse((x[i], y[i]), e * plt_sfactor * 2, f * plt_sfactor * 2, angle=phi_e * 180 / _pi,
                                    edgecolor=ellipse_b_c, fill=ellipse_f, facecolor=ellipse_f_c)

        '''ellipse in isoplot, which has bigger semi-axial than error'''
        '''references:'''
        '''https://blog.csdn.net/u010182633/article/details/45924061'''
        '''https: // people.richland.edu / james / lecture / m170 / tbl - chi.html'''
        '''https://www.osgeo.cn/app/sb141'''
        if plt_sfactor == 1:
            v = 2.279  # 68% confidence limit, 1 sigma
        elif plt_sfactor == 2:
            v = 5.991  # 95% confidence limit, 2 sigma
        else:
            v = 1
        ellipse_2 = patches.Ellipse((x[i], y[i]), e * pow(v, 0.5) * 2, f * pow(v, 0.5) * 2,
                                    angle=phi_e * 180 / _pi, edgecolor='b', fill=ellipse_f,
                                    facecolor=ellipse_f_c)

        '''if drawing ellipse is not selected, breaking the loop there'''
        if drawEllipse:
            canvas.axes.add_patch(ellipse_1)
            canvas.axes.add_patch(ellipse_2)
        '''show random points'''
        if showRandomPts:
            count1 = count2 = 0
            mean = [x[i], y[i]]
            cov = [[sx[i] ** 2, sx[i] * sy[i] * rho[i]], [sy[i] * sx[i] * rho[i], sy[i] ** 2]]
            n = random_points_num
            random_points = random.multivariate_normal(mean, cov, n)
            all_points.append(random_points)  # using to plot isochron line distribute
            for each_point in list(random_points):
                canvas.axes.scatter(each_point[0], each_point[1], c='black', s=1)
                distance = (each_point[0] - x[i]) ** 2 + (each_point[1] - y[i]) ** 2
                cita = atan(tan(atan((each_point[1] - y[i]) / (each_point[0] - x[i])) - phi_e) * e / f)
                error_1 = (e * cos(cita)) ** 2 + (f * sin(cita)) ** 2
                if distance <= error_1 * v:
                    count1 += 1
                if distance <= error_1 * plt_sfactor ** 2:
                    count2 += 1
            p1 = round(count1 / random_points_num, 6)
            p2 = round(count2 / random_points_num, 6)
            print('bigger ellipse: %s' % str(p1))
            print('small ellipse: %s' % str(p2))
    '''isochron line distribute'''
    if showRandomPts:
        for i in range(random_points_num):
            x_list = [all_points[0][i][0], all_points[1][i][0], all_points[2][i][0],
                      all_points[3][i][0], all_points[4][i][0]]
            y_list = [all_points[0][i][1], all_points[1][i][1], all_points[2][i][1],
                      all_points[3][i][1], all_points[4][i][1]]
            k = intercept_linest(y_list, x_list)
            canvas.axes.plot([0, max(x) * 10], [k[0], max(x) * 10 * k[5][0] + k[0]], c=line_c)
    return canvas


def get_release_pattern():
    return


def get_diffusion_model():
    return


if __name__ == '__main__':
    M41 = 40.9645008
    M40 = 39.962383123
    M39 = 38.964313
    M38 = 37.9627322
    M37 = 36.9667759
    M36 = 35.96754628
    M35 = 34.9752567
    get_mdf(295.5, 0.2, M36, M40)
    open_filtered_xls('C:/Users/Young/Projects/2019-04Ar-Ar数据处理/filtered_file/19WHA0105.xls')

    print(calc_age(0.891794748138343, 0.0982869995702337, 0.0096546, 0.00001159 / 0.0096546 * 100, 5.531e-10,
                   0.015 / 5.531 * 100, useMin2000=True))
    _a = [24.48173757, 24.42967696, 24.3664485, 24.31345558, 24.26657191, 24.20899486, 24.15513883, 24.10524435,
          24.05106119, 24.01051296]
    _b = [12.231848, 24.586848, 36.911848, 49.220848, 61.532848, 73.840848, 86.154848, 98.454848, 110.790848,
          123.128848]
    _k = intercept_linest(_a, _b, external=True)
    print(_k)
    _a2 = list(map(lambda i: i / (1 - 0.16), _a))
    _k2 = intercept_linest(_a2, _b, external=True)
    print(_k2)
    '''这说明在外推零时刻值时，虽然有等比例缩放，但是截距值的相对误差是不变的'''
