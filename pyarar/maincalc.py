#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : maincalc.py
# @Author : Yang Wu
# @Date   : 2021/12/25
# @Email  : wuy@cug.edu.cn

from pyarar import calcFuncs as ProFunctions
from pyarar import sample
from math import exp

def corrBlank(sp: sample.Sample):
    """
    Blank correction
    """
    if sp.CorrBlank:
        sp.Ar36TempList, sp.Ar36TempErrorList \
            = ProFunctions.corr_blank(sp.Ar36MList, sp.Ar36MErrorList, sp.Ar36BList, sp.Ar36BErrorList)
        sp.Ar37TempList, sp.Ar37TempErrorList \
            = ProFunctions.corr_blank(sp.Ar37MList, sp.Ar37MErrorList, sp.Ar37BList, sp.Ar37BErrorList)
        sp.Ar38TempList, sp.Ar38TempErrorList \
            = ProFunctions.corr_blank(sp.Ar38MList, sp.Ar38MErrorList, sp.Ar38BList, sp.Ar38BErrorList)
        sp.Ar39TempList, sp.Ar39TempErrorList \
            = ProFunctions.corr_blank(sp.Ar39MList, sp.Ar39MErrorList, sp.Ar39BList, sp.Ar39BErrorList)
        sp.Ar40TempList, sp.Ar40TempErrorList \
            = ProFunctions.corr_blank(sp.Ar40MList, sp.Ar40MErrorList, sp.Ar40BList, sp.Ar40BErrorList)

def corrDiscr(sp: sample.Sample):
    """
    Discrimination correction
    """
    def _func(a0, e0, f):
        k1 = [ProFunctions.error_mul((a0[i], e0[i]), (f[0], f[1])) for i in range(len(a0))]
        k0 = [a0[i] * f[0] for i in range(len(a0))]
        return k0, k1
    if sp.CorrDiscr:
        # Mass Discrimination based on the mass of Ar40, Ar36 | Ar37 | Ar38 | Ar39
        MDF, sMDF = sp.MDF, sp.MDFError
        M36, M37, M38, M39, M40 = sp.Ar36Mass, sp.Ar37Mass, sp.Ar38Mass, sp.Ar39Mass, sp.Ar40Mass
        c = ProFunctions.corr_discr(MDF, MDF * sMDF / 100, M36, M40)  # 36Ar
        sp.Ar36TempList, sp.Ar36TempErrorList = _func(sp.Ar36TempList, sp.Ar36TempErrorList, c)
        c = ProFunctions.corr_discr(MDF, MDF * sMDF / 100, M37, M40)  # 37Ar
        sp.Ar37TempList, sp.Ar37TempErrorList = _func(sp.Ar37TempList, sp.Ar37TempErrorList, c)
        c = ProFunctions.corr_discr(MDF, MDF * sMDF / 100, M38, M40)  # 38Ar
        sp.Ar38TempList, sp.Ar38TempErrorList = _func(sp.Ar38TempList, sp.Ar38TempErrorList, c)
        c = ProFunctions.corr_discr(MDF, MDF * sMDF / 100, M39, M40)  # 39Ar
        sp.Ar39TempList, sp.Ar39TempErrorList = _func(sp.Ar39TempList, sp.Ar39TempErrorList, c)

def corrDecay(sp: sample.Sample):
    """
    Decay correction
    """
    def _func(a0, e0, f):
        k1 = ProFunctions.error_mul((a0, e0), (f[0], f[1]))
        k0 = a0 * f[0]
        return k0, k1
    # Decay Correction
    t2 = sp.IrradiationEndTimeList  # irradiation end time in second
    t3 = sp.IrradiationDurationList  # irradiation duration time in hour
    if sp.Corr37ArDecay:
        for row in range(len(sp.Ar37TempList)):
            c = ProFunctions.corr_decay(sp.MDateTimeList[row], t2, t3, sp.Ar37Const, sp.Ar37ConstError)  # 37Ar
            sp.Ar37TempList[row], sp.Ar37TempErrorList[row] \
                = _func(sp.Ar37TempList[row], sp.Ar37TempErrorList[row], c)
    if sp.Corr39ArDecay:
        for row in range(len(sp.Ar39TempList)):
            c = ProFunctions.corr_decay(sp.MDateTimeList[row], t2, t3, sp.Ar39Const, sp.Ar39ConstError)  # 39Ar
            sp.Ar39TempList[row], sp.Ar39TempErrorList[row] \
                = _func(sp.Ar39TempList[row], sp.Ar39TempErrorList[row], c)

def degasPattern(sp: sample.Sample):
    """
    Degas Pattern
    """
    def _mul(a0, e0, f, rsf, state: bool):
        k1 = [ProFunctions.error_mul((a0[i], e0[i]), (f, rsf * f / 100)) if state else 0 for i in range(len(a0))]
        k0 = [a0[i] * f if state else 0 for i in range(len(a0))]
        return k0, k1

    def _sub(a0, e0, a1, e1, state: bool):
        k1 = [ProFunctions.error_add(e0[i], e1[i]) if state else 0 for i in range(len(a0))]
        k0 = [a0[i] - a1[i] if state else 0 for i in range(len(a0))]
        return k0, k1

    def _second(datetime: list, endtime: list):
        t_day, t_month, t_year, t_hour, t_min = datetime
        return [(ProFunctions.get_datetime(t_year, t_month, t_day, t_hour, t_min) - i) / (3600 * 24 * 365.242) for i in
                endtime]
    # Corr Ca
    sp.Ar37DegasCa, sp.Ar37DegasCaError = _mul(sp.Ar37TempList, sp.Ar37TempErrorList, 1, 0, sp.CorrCa)
    # Force negative values to zero
    sp.Ar37DegasCa = [0 if i < 0 and sp.ForceNegative else i for i in sp.Ar37DegasCa]
    sp.Ar36DegasCa, sp.Ar36DegasCaError \
        = _mul(sp.Ar37DegasCa, sp.Ar37DegasCaError, sp.Ar36vsAr37Ca, sp.Ar36vsAr37CaError, sp.CorrCa)
    sp.Ar38DegasCa, sp.Ar38DegasCaError \
        = _mul(sp.Ar37DegasCa, sp.Ar37DegasCaError, sp.Ar38vsAr37Ca, sp.Ar38vsAr37CaError, sp.CorrCa)
    sp.Ar39DegasCa, sp.Ar39DegasCaError \
        = _mul(sp.Ar37DegasCa, sp.Ar37DegasCaError, sp.Ar39vsAr37Ca, sp.Ar39vsAr37CaError, sp.CorrCa)
    sp.Ar40DegasCa, sp.Ar40DegasCaError = _mul(sp.Ar37DegasCa, sp.Ar37DegasCaError, 0, 0, False)
    # Corr K
    sp.Ar39DegasK, sp.Ar39DegasKError\
        = _sub(sp.Ar39TempList, sp.Ar39TempErrorList, sp.Ar39DegasCa, sp.Ar39DegasCaError, sp.CorrK)
    # Force negative values to zero
    sp.Ar39DegasK = [0 if i < 0 and sp.ForceNegative else i for i in sp.Ar39DegasK]
    sp.Ar40DegasK, sp.Ar40DegasKError\
        = _mul(sp.Ar39DegasK, sp.Ar39DegasKError, sp.Ar40vsAr39K, sp.Ar40vsAr39KError, sp.CorrK)
    sp.Ar38DegasK, sp.Ar38DegasKError\
        = _mul(sp.Ar39DegasK, sp.Ar39DegasKError, sp.Ar38vsAr39K, sp.Ar38vsAr39KError, sp.CorrK)
    sp.Ar36DegasK, sp.Ar36DegasKError = _mul(sp.Ar39DegasK, sp.Ar39DegasKError, 0, 0, False)
    sp.Ar37DegasK, sp.Ar37DegasKError = _mul(sp.Ar39DegasK, sp.Ar39DegasKError, 0, 0, False)
    # Corr Cl
    try:
        if not sp.CorrCl:
            raise ValueError('Do not Correct Cl')
        stand_time_year = [_second(datetime, sp.IrradiationEndTimeList)[-1] for datetime in sp.MDateTimeList]
        # 36Ar deduct Ca, that is sum of 36Ara and 36ArCl
        v36acl = [sp.Ar36TempList[i] - sp.Ar36DegasCa[i] for i in range(len(sp.Ar36TempList))]
        sv36acl = [ProFunctions.error_add(sp.Ar36TempErrorList[i], sp.Ar36DegasCaError[i]) for i in
                   range(len(sp.Ar36TempErrorList))]
        # 38Ar deduct K and Ca, that is sum of 38Ara and 38ArCl
        v38acl = [sp.Ar38TempList[i] - sp.Ar38DegasK[i] - sp.Ar38DegasCa[i] for i in range(len(sp.Ar38TempList))]
        sv38acl = [ProFunctions.error_add(sp.Ar38TempErrorList[i], sp.Ar38DegasKError[i], sp.Ar38DegasCaError[i])
                   for i in range(len(v38acl))]
        v3 = [sp.Cl36vs38Productivity * (1 - exp(-1 * sp.Cl36Const * stand_time_year[i])) for i in
              range(len(stand_time_year))]
        s3 = [pow((sp.Cl36vs38Productivity * sp.Cl36vs38ProductivityError / 100 *
                   (1 - exp(-1 * sp.Cl36Const * stand_time_year[i]))) ** 2 +
                  (sp.Cl36vs38Productivity * stand_time_year[i] * (exp(-1 * sp.Cl36Const * stand_time_year[i])) *
                   sp.Cl36Const * sp.Cl36ConstError / 100) ** 2, 0.5) for i in range(len(stand_time_year))]
        s3 = [ProFunctions.error_div((1, 0), (v3[i], s3[i])) for i in range(len(s3))]
        v3 = [1 / v3[i] for i in range(len(v3))]
        # 36ArCl
        sp.Ar36DegasCl = [(v36acl[i] * sp.Ar38vsAr36Trapped - v38acl[i]) / (sp.Ar38vsAr36Trapped - v3[i]) for i in range(len(v36acl))]
        s1 = [(sv36acl[i] * sp.Ar38vsAr36Trapped / (sp.Ar38vsAr36Trapped - v3[i])) ** 2 for i in range(len(sp.Ar36DegasCl))]
        s2 = [(sv38acl[i] / (sp.Ar38vsAr36Trapped - v3[i])) ** 2 for i in range(len(sp.Ar36DegasCl))]
        s3 = [(s3[i] * (v36acl[i] * sp.Ar38vsAr36Trapped - v38acl[i]) / (sp.Ar38vsAr36Trapped - v3[i]) ** 2) ** 2 for i in range(len(sp.Ar36DegasCl))]
        s4 = [(v36acl[i] / (sp.Ar38vsAr36Trapped - v3[i]) - (v36acl[i] * sp.Ar38vsAr36Trapped - v38acl[i]) / (sp.Ar38vsAr36Trapped - v3[i]) ** 2) ** 2 * (
                sp.Ar38vsAr36TrappedError * sp.Ar38vsAr36Trapped / 100) ** 2 for i in range(len(sp.Ar36DegasCl))]
        sp.Ar36DegasClError = [pow(s1[i] + s2[i] + s3[i] + s4[i], 0.5) for i in range(len(sp.Ar36DegasCl))]
        # Force negative values to zero
        sp.Ar36DegasCl = [0 if i < 0 and sp.ForceNegative else i for i in sp.Ar36DegasCl]
        '''
        # force 36ArCl to zero if 36Ar - 36ArCa - 36Cl < 0
        sp.Ar36DegasClError = [sp.Ar36DegasClError[i] if v36acl[i] - sp.Ar36DegasCl[i] >= 0 else 0 for i in range(len(sp.Ar36DegasClError))]
        sp.Ar36DegasCl = [sp.Ar36DegasCl[i] if v36acl[i] - sp.Ar36DegasCl[i] >= 0 else 0 for i in range(len(sp.Ar36DegasCl))]
        '''
        # 38ArCl
        sp.Ar38DegasClError = [ProFunctions.error_mul((sp.Ar36DegasCl[i], sp.Ar36DegasClError[i]), (v3[i], s3[i]))
                               for i in range(len(sp.Ar36DegasCl))]
        sp.Ar38DegasCl = [sp.Ar36DegasCl[i] * v3[i] for i in range(len(sp.Ar36DegasCl))]
        sp.Ar37DegasCl, sp.Ar37DegasClError = [0] * len(sp.Ar36DegasCl), [0] * len(sp.Ar36DegasCl)
        sp.Ar39DegasCl, sp.Ar39DegasClError = [0] * len(sp.Ar36DegasCl), [0] * len(sp.Ar36DegasCl)
        sp.Ar40DegasCl, sp.Ar40DegasClError = [0] * len(sp.Ar36DegasCl), [0] * len(sp.Ar36DegasCl)
    except Exception as e:
        print('Error in corr Cl: %s' % str(e))

    # Corr Atm
    try:
        if not sp.CorrAtm:
            raise ValueError('Do not Correct Cl')

        # 36ArAir
        sp.Ar36DegasAir = [sp.Ar36TempList[i] - sp.Ar36DegasCa[i] - sp.Ar36DegasCl[i] - sp.Ar36DegasK[i] for i in
                           range(len(sp.Ar36TempList))]
        sp.Ar36DegasAirError = [
            ProFunctions.error_add(sp.Ar36TempErrorList[i], sp.Ar36DegasCaError[i], sp.Ar36DegasClError[i],
                                   sp.Ar36DegasKError[i])for i in range(len(sp.Ar36DegasCl))]
        # Force negative values to zero
        sp.Ar36DegasAir = [0 if i < 0 and sp.ForceNegative else i for i in sp.Ar36DegasAir]

        # 38ArAir
        sp.Ar38DegasAir = [sp.Ar36DegasAir[i] * sp.Ar38vsAr36Trapped for i in range(len(sp.Ar36DegasAir))]
        sp.Ar38DegasAirError = [
            ProFunctions.error_mul((sp.Ar36DegasAir[i], sp.Ar36DegasAirError[i]),
                                   (sp.Ar38vsAr36Trapped, sp.Ar38vsAr36TrappedError)) for i in
            range(len(sp.Ar36DegasAir))]

        # 40ArAir
        sp.Ar40DegasAir = [sp.Ar36DegasAir[i] * sp.Ar40vsAr36Trapped for i in range(len(sp.Ar36DegasAir))]
        sp.Ar40DegasAirError = [
            ProFunctions.error_mul((sp.Ar36DegasAir[i], sp.Ar36DegasAirError[i]),
                                   (sp.Ar40vsAr36Trapped, sp.Ar40vsAr36TrappedError)) for i in
            range(len(sp.Ar36DegasAir))]

        sp.Ar37DegasAir, sp.Ar37DegasAirError = [0] * len(sp.Ar36DegasAir), [0] * len(sp.Ar36DegasAir)
        sp.Ar39DegasAir, sp.Ar39DegasAirError = [0] * len(sp.Ar36DegasAir), [0] * len(sp.Ar36DegasAir)
    except Exception as e:
        print('Error in corr Air: %s' % str(e))

    # 40Arr
    sp.Ar40DegasR = [sp.Ar40TempList[i] - sp.Ar40DegasCa[i] - sp.Ar40DegasCl[i] - sp.Ar40DegasK[i] - sp.Ar40DegasAir[i]
                     for i in range(len(sp.Ar40TempList))]
    sp.Ar40DegasRError = [
        ProFunctions.error_add(sp.Ar40TempErrorList[i], sp.Ar40DegasCaError[i], sp.Ar40DegasClError[i],
                               sp.Ar40DegasKError[i], sp.Ar40DegasAirError[i]) for i in range(len(sp.Ar40TempList))]
    # Force negative values to zero
    sp.Ar40DegasR = [0 if i < 0 and sp.ForceNegative else i for i in sp.Ar40DegasR]

def calcRatios(sp: sample.Sample):
    """
    Get ratios using to plot isochron diagrams.
    """
    def _getIsochron(x, sx, y, sy, z, sz):
        _n = min([len(x), len(sx), len(y), len(sy), len(z), len(sz)])
        # x / z
        k0 = [x[i] / z[i] if z[i] != 0 else 0 for i in range(_n)]
        k1 = [ProFunctions.error_div((x[i], sx[i]), (z[i], sz[i])) if z[i] != 0 else 0 for i in range(_n)]
        # y / z
        k2 = [y[i] / z[i] if z[i] != 0 else 0 for i in range(_n)]
        k3 = [ProFunctions.error_div((y[i], sy[i]), (z[i], sz[i])) if z[i] != 0 else 0 for i in range(_n)]
        k4 = [ProFunctions.error_cor(sx[i] / x[i], sy[i] / y[i], sz[i] / z[i]) if x[i] * y[i] * z[i] != 0 else 0
              for i in range(_n)]
        return [k0, k1, k2, k3, k4]
    # Cl isochron 1: 40Ar* / 38ArCl vs. 39ArK / 38ArCl, 40Ar* = 40ArCl+r
    sp.ClNormalIsochron = _getIsochron(sp.Ar40DegasR, sp.Ar40DegasRError,
                                       sp.Ar39DegasK, sp.Ar39DegasKError,
                                       sp.Ar38DegasCl, sp.Ar38DegasClError)
    # Cl isochron 2: 38ArCl / 40Ar* vs. 39ArK / 40Ar*
    sp.ClInverseIsochron = _getIsochron(sp.Ar38DegasCl, sp.Ar38DegasClError,
                                        sp.Ar39DegasK, sp.Ar39DegasKError,
                                        sp.Ar40DegasR, sp.Ar40DegasRError)
    # Cl isochron 3: 40Ar*/39ArK vs. 38ArCl/39ArK
    sp.ClKIsochron = _getIsochron(sp.Ar40DegasR, sp.Ar40DegasRError,
                                  sp.Ar38DegasCl, sp.Ar38DegasClError,
                                  sp.Ar39DegasK, sp.Ar39DegasKError)
    # normal isochron: 39ArK / 36Ara vs. 40Ar* / 36Ara, 40Ar* = 40Ara+r, however it is actually 40Ara+r+Cl
    c = [sp.Ar40TempList[i] - sp.Ar40DegasK[i] - sp.Ar40DegasCa[i] - sp.Ar40DegasCl[i]
         for i in range(len(sp.Ar40TempList))]
    sc = [ProFunctions.error_add(sp.Ar40TempErrorList[i], sp.Ar40DegasKError[i], sp.Ar40DegasCaError[i],
                                 sp.Ar40DegasClError[i]) for i in range(len(sp.Ar40TempList))]
    c = [0 if i < 0 else i for i in c]
    sp.AtmNormalIsochron = _getIsochron(sp.Ar39DegasK, sp.Ar39DegasKError,
                                        c, sc,
                                        sp.Ar36DegasAir, sp.Ar36DegasAirError)
    # inverse isochron: 39ArK / 40Ar* vs. 36Ara / 40Ar*
    sp.AtmInverseIsochron = _getIsochron(sp.Ar39DegasK, sp.Ar39DegasKError,
                                         sp.Ar36DegasAir, sp.Ar36DegasAirError,
                                         c, sc)
    # 3D isochron: 39ArK / 40Ar* vs. 36Ara / 40Ar* vs. 38ArCl / 40Ar*, 40Ar* = 40Ara+r+Cl
    c1 = _getIsochron(sp.Ar38DegasCl, sp.Ar38DegasClError, sp.Ar39DegasK, sp.Ar39DegasKError, c, sc)
    sp.ThreeDimIsochron = [sp.AtmInverseIsochron[0], sp.AtmInverseIsochron[1],
                           sp.AtmInverseIsochron[2], sp.AtmInverseIsochron[3],
                           c1[0], c1[1]]
