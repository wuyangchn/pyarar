#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : maincalc.py
# @Author : Yang Wu
# @Date   : 2021/12/25
# @Email  : wuy@cug.edu.cn

from pyarar import calcFuncs as ProFunctions
from pyarar import sample
from math import exp

def corrBlank(sp: sample.UnkSample):
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

def corrDiscr(sp: sample.UnkSample):
    """
    Discrimination correction
    """
    def _func(a0, e0, f):
        k1 = [ProFunctions.error_mul((a0[i], e0[i]), (f[0], f[1])) for i in range(len(a0))]
        k0 = [a0[i] * f[0] for i in range(len(a0))]
        return k0, k1
    if sp.CorrDiscr:
        '''Mass Discrimination based on the mass of Ar40, Ar36 | Ar37 | Ar38 | Ar39'''
        MDF, sMDF = sp.MDF, sp.MDFError  # absolute error
        M36, M37, M38, M39, M40 = sp.Ar36Mass, sp.Ar37Mass, sp.Ar38Mass, sp.Ar39Mass, sp.Ar40Mass
        c = ProFunctions.corr_discr(MDF, sMDF, M36, M40)  # 36Ar
        sp.Ar36TempList, sp.Ar36TempErrorList = _func(sp.Ar36TempList, sp.Ar36TempErrorList, c)
        c = ProFunctions.corr_discr(MDF, sMDF, M37, M40)  # 37Ar
        sp.Ar37TempList, sp.Ar37TempErrorList = _func(sp.Ar37TempList, sp.Ar37TempErrorList, c)
        c = ProFunctions.corr_discr(MDF, sMDF, M38, M40)  # 38Ar
        sp.Ar38TempList, sp.Ar38TempErrorList = _func(sp.Ar38TempList, sp.Ar38TempErrorList, c)
        c = ProFunctions.corr_discr(MDF, sMDF, M39, M40)  # 39Ar
        sp.Ar39TempList, sp.Ar39TempErrorList = _func(sp.Ar39TempList, sp.Ar39TempErrorList, c)

def corrDecay(sp: sample.UnkSample):
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

def degasPattern(sp: sample.UnkSample):
    """
    Degas Pattern
    """
    def _mul(a0, e0, f, sf, state: bool):
        k1 = [ProFunctions.error_mul((a0[i], e0[i]), (f, sf)) if state else 0 for i in range(len(a0))]
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
        s3 = [pow((sp.Cl36vs38ProductivityError * (1 - exp(-1 * sp.Cl36Const * stand_time_year[i]))) ** 2 +
                  (sp.Cl36vs38Productivity * stand_time_year[i] * (exp(-1 * sp.Cl36Const * stand_time_year[i])) *
                   sp.Cl36ConstError) ** 2, 0.5) for i in range(len(stand_time_year))]
        s3 = [ProFunctions.error_div((1, 0), (v3[i], s3[i])) for i in range(len(s3))]
        v3 = [1 / v3[i] for i in range(len(v3))]
        # 36ArCl
        sp.Ar36DegasCl = [(v36acl[i] * sp.Ar38vsAr36Trapped - v38acl[i]) / (sp.Ar38vsAr36Trapped - v3[i]) for i in range(len(v36acl))]
        s1 = [(sv36acl[i] * sp.Ar38vsAr36Trapped / (sp.Ar38vsAr36Trapped - v3[i])) ** 2
              for i in range(len(sp.Ar36DegasCl))]
        s2 = [(sv38acl[i] / (sp.Ar38vsAr36Trapped - v3[i])) ** 2 for i in range(len(sp.Ar36DegasCl))]
        s3 = [(s3[i] * (v36acl[i] * sp.Ar38vsAr36Trapped - v38acl[i]) / (sp.Ar38vsAr36Trapped - v3[i]) ** 2) ** 2
              for i in range(len(sp.Ar36DegasCl))]
        s4 = [(v36acl[i] / (sp.Ar38vsAr36Trapped - v3[i]) -
               (v36acl[i] * sp.Ar38vsAr36Trapped - v38acl[i]) / (sp.Ar38vsAr36Trapped - v3[i]) ** 2) ** 2 * (
                sp.Ar38vsAr36TrappedError) ** 2 for i in range(len(sp.Ar36DegasCl))]
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

def calcApparentAge(sp: sample.UnkSample):
    sp.FValues = [sp.Ar40DegasR[i] / sp.Ar39DegasK[i] if sp.Ar39DegasK[i] != 0 else 0
                  for i in range(len(sp.Ar40DegasR))]
    sp.FValuesError = [
        ProFunctions.error_div((sp.Ar40DegasR[i], sp.Ar40DegasRError[i]), (sp.Ar39DegasK[i], sp.Ar39DegasKError[i]))
        if sp.Ar39DegasK[i] != 0 else 0 for i in range(len(sp.Ar40DegasR))]
    age, s1, s2, s3 = [], [], [], []
    for i in range(len(sp.FValues)):
        k0 = calcAge(sp.FValues[i], sp.FValuesError[i], sp)
        age.append(k0[0])
        s1.append(k0[1])
        s2.append(k0[2])
        s3.append(k0[3])
    sp.ApparentAge, sp.ApparentAgeAnalysisError, sp. ApparentAgeInternalError, sp.ApparentAgeFullExternalError = \
        age, s1, s2, s3

def calcKCaClRatios(sp: sample.UnkSample):
    def _func(a0: list, e0: list, a1: list, e1: list, f: float, sf: float):
        n = min(len(a0), len(e0), len(a1), len(e1))
        k0 = [f * a0[i] / a1[i] if a1[i] != 0 else 0 for i in range(n)]
        k1 = [ProFunctions.error_mul((f, sf), (a0[i] / a1[i], ProFunctions.error_div((a0[i], e0[i]), (a1[i], e1[i]))))
              if a1[i] != 0 else 0 for i in range(n)]
        return k0, k1

    isKCa = False
    if isKCa:
        """K/Ca"""
        sp.KCaRatios, sp.KCaRatiosError = \
            _func(sp.Ar39DegasK, sp.Ar39DegasKError, sp.Ar37DegasCa, sp.Ar37DegasCaError,
                  sp.KvsCaFactor, sp.KvsCaFactorError)
    else:
        """Ca/K"""
        sp.KCaRatios, sp.KCaRatiosError = \
            _func(sp.Ar37DegasCa, sp.Ar37DegasCaError, sp.Ar39DegasK, sp.Ar39DegasKError,
                  1 / sp.KvsCaFactor, ProFunctions.error_div((1, 0), (sp.KvsCaFactor, sp.KvsCaFactorError)))
    isKCl = True
    if isKCl:
        """K/Cl"""
        sp.KClRatios, sp.KClRatiosError = \
            _func(sp.Ar39DegasK, sp.Ar39DegasKError, sp.Ar38DegasCl, sp.Ar38DegasClError,
                  sp.KvsClFactor, sp.KvsClFactorError)
    else:
        """Cl/K"""
        sp.KClRatios, sp.KClRatiosError = \
            _func(sp.Ar38DegasCl, sp.Ar38DegasClError, sp.Ar39DegasK, sp.Ar39DegasKError,
                  1 / sp.KvsClFactor, ProFunctions.error_div((1, 0), (sp.KvsClFactor, sp.KvsClFactorError)))
    isCaCl = True
    if isCaCl:
        """Ca/Cl"""
        sp.CaClRatios, sp.CaClRatiosError = \
            _func(sp.Ar37DegasCa, sp.Ar37DegasCaError, sp.Ar38DegasCl, sp.Ar38DegasClError,
                  sp.CavsClFactor, sp.CavsClFactorError)
    else:
        """Cl/Ca"""
        sp.CaClRatios, sp.CaClRatiosError = \
            _func(sp.Ar38DegasCl, sp.Ar38DegasClError, sp.Ar37DegasCa, sp.Ar37DegasCaError,
                  1 / sp.KvsClFactor, ProFunctions.error_div((1, 0), (sp.CavsClFactor, sp.CavsClFactorError)))

def calcRatios(sp: sample.UnkSample):
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
        return [k0, k1, k2, k3, k4, []]
    # Cl isochron 1: 39ArK / 38ArCl vs. 40Ar* / 38ArCl, 40Ar* = 40ArCl+r
    sp.ClNormalIsochron = _getIsochron(sp.Ar39DegasK, sp.Ar39DegasKError,
                                       sp.Ar40DegasR, sp.Ar40DegasRError,
                                       sp.Ar38DegasCl, sp.Ar38DegasClError)
    # Cl isochron 2: 39ArK / 40Ar* vs. 38ArCl / 40Ar*
    sp.ClInverseIsochron = _getIsochron(sp.Ar39DegasK, sp.Ar39DegasKError,
                                        sp.Ar38DegasCl, sp.Ar38DegasClError,
                                        sp.Ar40DegasR, sp.Ar40DegasRError)
    # Cl isochron 3: 40Ar* / 39ArK vs. 38ArCl / 39ArK
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

def isochronAge(sp: sample.UnkSample):
    def _getIsochronAge(iso, isNormal=False, isInverse=False, isKIsochron=False):
        x, sx, y, sy, pho = [[i[j] for j in sp.IsochronSelectedPoints] for i in iso]
        k0 = ProFunctions.isochron_regress(x, sx, y, sy, pho,
                                           isNormal=isNormal, isInverse=isInverse, isKIsochron=isKIsochron,
                                           statistics=True, convergence=sp.York2FitConvergence,
                                           iteration=sp.York2FitIteration)
        if not k0:
            return ['Null'] * 16
        k1 = calcAge(k0[2], k0[3], sp)
        k2 = (x, sx, y, sy, pho, sp.IsochronSelectedPoints)
        '''list in order: '''
        '''0-3: Age, analytical error, internal error, full external error'''
        '''4-15: ratio, error, 40r/39k, error, MSWD, b, seb, m, sem, convergence, iterations, error magnification'''
        '''16-21: x, sx, y, sy, pho, sp.IsochronSelectedPoints'''
        return [i for i in k1 + k0 + k2]
    sp.ClNormalIsochron[5] = _getIsochronAge(sp.ClNormalIsochron[:5], isNormal=True)
    sp.ClInverseIsochron[5] = _getIsochronAge(sp.ClInverseIsochron[:5], isInverse=True)
    sp.ClKIsochron[5] = _getIsochronAge(sp.ClKIsochron[:5], isKIsochron=True)
    sp.AtmNormalIsochron[5] = _getIsochronAge(sp.AtmNormalIsochron[:5], isNormal=True)
    sp.AtmInverseIsochron[5] = _getIsochronAge(sp.AtmInverseIsochron[:5], isInverse=True)

def calcAge(F, sF, sp: sample.UnkSample):
    k0 = ProFunctions.calc_age(F, sF, sp.JValue, sp.JValueError, sp.K40Const, sp.K40ConstError,
                               uf=1, useMin2000=sp.UseMinCalculation,
                               activity_of_K=sp.K40Activity, activity_of_K_error=sp.K40ActivityError,
                               activity_of_K_to_Ar=sp.K40ECActivity,
                               activity_of_K_to_Ar_error=sp.K40ECActivityError,
                               activity_of_K_to_Ca=sp.K40BetaNActivity,
                               activity_of_K_to_Ca_error=sp.K40BetaNActivityError,
                               atomic_weight_of_K=sp.K40Mass, atomic_weight_of_K_error=sp.K40MassError,
                               seconds_in_a_year=sp.yearConst, seconds_in_a_year_error=sp.yearConstError,
                               fraction_of_40K=sp.K40vsKFractions, fraction_of_40K_error=sp.K40vsKFractionsError,
                               avogadro_number=sp.NoConst, avogadro_number_error=sp.NoConstError,
                               decay_constant_of_40K=sp.K40Const, decay_constant_of_40K_error=sp.K40ConstError,
                               decay_constant_of_40K_EC=sp.K40ECConst,
                               decay_constant_of_40K_EC_error=sp.K40ECConstError,
                               standard_age=sp.StandardAge, standard_age_error=sp.StandardAgeError,
                               standard_Ar_conc=sp.Ar40Concentration,
                               standard_Ar_conc_error=sp.Ar40ConcentrationError,
                               standard_K_conc=sp.KConcentration, standard_K_conc_error=sp.KConcentrationError,
                               standard_40K_K=sp.StandardAr40vsK, standard_40K_K_error=sp.StandardAr40vsKError)
    return k0

def calcPlateauAge(sp: sample.UnkSample):
    def _plateau(points: list):
        F, sF = [[i[j] for j in points] for i in [sp.FValues, sp.FValuesError]]
        k4, k5, k6, k7 = ProFunctions.err_wtd_mean(F, sF)  # weighted F, error, dp, MSWD
        k0, k1, k2, k3 = calcAge(k4, k5, sp)  # age, analysis error, internal error, full external error
        k8 = sum([sp.Ar39DegasK[i] for i in points]) / sum(sp.Ar39DegasK)  # accumulative 39ArK
        k9 = points  # selected steps
        return [k0, k1, k2, k3, k4, k5, k6, k7, k8, k9]
    sp.PlateauAges = []
    x, y1, y2 = ProFunctions.get_spectra(sp.ApparentAge, sp.ApparentAgeInternalError, sp.Ar39DegasK)
    sp.SpectraLines = [x, y1, y2]
    sp.PlateauAges = _plateau(sp.IsochronSelectedPoints)

def calcTFAge(sp: sample.UnkSample):
    a0, e0 = sum(sp.Ar40DegasR), pow(sum([i ** 2 for i in sp.Ar40DegasRError]), 0.5)
    a1, e1 = sum(sp.Ar39DegasK), pow(sum([i ** 2 for i in sp.Ar39DegasKError]), 0.5)
    F, sF = a0 / a1, ProFunctions.error_div((a0, e0), (a1, e1))
    k0, k1, k2, k3 = calcAge(F, sF, sp)
    sp.TotalFusionAge = [k0, k1, k2, k3, F, sF, len(sp.Ar40DegasR)]  # TF age, e1, e2, e3, 40Arr/39Ark, error, dp
