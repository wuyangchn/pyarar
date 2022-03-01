#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : FuncsSample.py
# @Author : Yang Wu
# @Date   : 2021/12/25
# @Email  : wuy@cug.edu.cn

"""
Sample Functions
"""
from pyarar import FuncsCalc
from pyarar import FuncsPlot
from pyarar import sample
from math import exp
from matplotlib import pyplot
import numpy as np

"""
Initialize
"""
def initializeData(smp: sample.Sample):
    """
    Initialize the data list
    """
    for key, value in smp.get_intermediate_data().items():
        smp.__dict__[key] = type(value)()


"""
Read Files
"""
def readDataFromRawFile(smp: sample.Sample, path=None):
    """
    Read data from raw file.

    parameters
    ----------
    smp: Sample instance
    path: str
        raw file path.
    """
    initializeData(smp)
    if path:
        smp.RawFilePath = path
    res = FuncsCalc.open_original_xls(smp.RawFilePath)
    if res:
        pass

def readDataFromFilteredFile(smp: sample.Sample, path=None):
    """
    Read data from filtered file.

    parameters
    ----------
    smp: Sample instance
    path: str
        filtered file path.
    """
    initializeData(smp)
    if path:
        smp.FilteredFilePath = path
    res = FuncsCalc.open_filtered_xls(smp.FilteredFilePath)
    if res:
        _readFilteredFile(smp, res)

def readDataFromAgeFile(smp: sample.Sample, path=None):
    """
    Read data from filtered file.

    parameters
    ----------
    smp: Sample instance
    path: str
        age file path.
    """
    initializeData(smp)
    if path:
        smp.AgeFilePath = path
    res = FuncsCalc.open_age_xls(smp.AgeFilePath)
    if res:
        _readFilteredFile(smp, res)
        smp.IrradiationDurationList = res[3]
        smp.IrradiationEndTimeList = res[4]
        book_contents = res[2]
        # read data
        data_tables_value = book_contents['Data Tables']
        # read and rewrite calculation params
        logs01_params = book_contents['Logs01']
        # read and rewrite irradiation params
        smp.SampleName = str(data_tables_value[44][5])
        smp.SampleMineral = str(data_tables_value[45][5])
        smp.ReactorLocation = str(data_tables_value[46][5])
        smp.ExperimentAnalyst = str(data_tables_value[47][5])
        smp.StandardAge = float(data_tables_value[49][5])
        smp.StandardAgeError = float(data_tables_value[50][5]) / 100 * float(data_tables_value[49][5])
        smp.JValue = float(data_tables_value[51][5])
        smp.JValueError = float(data_tables_value[52][5]) / 100 * float(data_tables_value[51][5])
        smp.MDF = float(data_tables_value[53][5])
        smp.MDFError = float(data_tables_value[54][5]) / 100 * float(data_tables_value[53][5])
        smp.IrradiationName = smp.ReactorProject = str(data_tables_value[63][5])
        smp.ExperimentName = str(data_tables_value[65][5])
        smp.StandardName = str(data_tables_value[67][5])
        smp.Ar40vsAr36Trapped = float(data_tables_value[71][5])
        smp.Ar40vsAr36TrappedError = float(data_tables_value[72][5]) / 100 * float(data_tables_value[71][5])
        smp.Ar40vsAr36Cosmo = float(data_tables_value[73][5])
        smp.Ar40vsAr36CosmoError = float(data_tables_value[74][5]) / 100 * float(data_tables_value[73][5])
        smp.Ar38vsAr36Trapped = float(data_tables_value[75][5])
        smp.Ar38vsAr36TrappedError = float(data_tables_value[76][5]) / 100 * float(data_tables_value[75][5])
        smp.Ar38vsAr36Cosmo = float(data_tables_value[77][5])
        smp.Ar38vsAr36CosmoError = float(data_tables_value[78][5]) / 100 * float(data_tables_value[77][5])
        smp.Ar39vsAr37Ca = float(data_tables_value[79][5])
        smp.Ar39vsAr37CaError = float(data_tables_value[80][5]) / 100 * float(data_tables_value[79][5])
        smp.Ar38vsAr37Ca = float(data_tables_value[81][5])
        smp.Ar38vsAr37CaError = float(data_tables_value[82][5]) / 100 * float(data_tables_value[81][5])
        smp.Ar36vsAr37Ca = float(data_tables_value[83][5])
        smp.Ar36vsAr37CaError = float(data_tables_value[84][5]) / 100 * float(data_tables_value[83][5])
        smp.Ar40vsAr39K = float(data_tables_value[85][5])
        smp.Ar40vsAr39KError = float(data_tables_value[86][5]) / 100 * float(data_tables_value[85][5])
        smp.Ar38vsAr39K = float(data_tables_value[87][5])
        smp.Ar38vsAr39KError = float(data_tables_value[88][5]) / 100 * float(data_tables_value[87][5])
        smp.Ar36vsAr38Cl = float(data_tables_value[89][5])
        smp.Ar36vsAr38ClError = float(data_tables_value[90][5]) / 100 * float(data_tables_value[89][5])
        smp.KvsCaFactor = float(data_tables_value[91][5])
        smp.KvsCaFactorError = float(data_tables_value[92][5]) / 100 * float(data_tables_value[91][5])
        smp.KvsClFactor = float(data_tables_value[93][5])
        smp.KvsClFactorError = float(data_tables_value[94][5]) / 100 * float(data_tables_value[93][5])
        smp.CavsClFactor = float(data_tables_value[95][5])
        smp.CavsClFactorError = float(data_tables_value[96][5]) / 100 * float(data_tables_value[95][5])
        # read select state of each experiment steps, list from 0
        smp.IsochronSelectedPoints = [row_num - 5 for row_num in range(len(data_tables_value[187]))
                                      if data_tables_value[187][row_num] == 4]
        # read and rewrite calculation params
        smp.York2FitConvergence = float(logs01_params[1][0]) / 100
        smp.York2FitIteration = int(logs01_params[1][1])
        smp.Corr37ArDecay = int(logs01_params[1][6])
        smp.Corr39ArDecay = int(logs01_params[1][7])
        smp.Corr36ClDecay = int(logs01_params[1][8])
        smp.NoConst = float(logs01_params[1][9])
        smp.NoConstError = float(logs01_params[1][10]) / 100 * float(logs01_params[1][9])
        smp.Fitting = 'York-2'
        smp.K40Mass = float(logs01_params[1][11])
        smp.K40MassError = float(logs01_params[1][12]) / 100 * float(logs01_params[1][11])
        smp.YearConst = float(logs01_params[1][13])
        smp.YearConstError = 0
        smp.K40vsKFractions = float(logs01_params[1][14])
        smp.K40vsKFractionsError = float(logs01_params[1][15]) / 100 * float(logs01_params[1][14])
        smp.Cl35vsCl37Fractions = float(logs01_params[1][16])
        smp.Cl35vsCl37FractionsError = float(logs01_params[1][17]) / 100 * float(logs01_params[1][16])
        smp.Cl36vs38Productivity = float(logs01_params[1][18])
        smp.Cl36vs38ProductivityError = float(logs01_params[1][19]) / 100 * float(logs01_params[1][18])
        smp.HClvsClFractions = float(logs01_params[1][24])
        smp.HClvsClFractionsError = float(logs01_params[1][25]) / 100 * float(logs01_params[1][24])
        smp.K40ECActivity = float(logs01_params[1][26])
        smp.K40ECActivityError = float(logs01_params[1][27]) / 100 * float(logs01_params[1][26])
        smp.K40BetaNActivity = float(logs01_params[1][28])
        smp.K40BetaNActivityError = float(logs01_params[1][29]) / 100 * float(logs01_params[1][28])
        smp.K40ECConst = float(logs01_params[1][30])
        smp.K40ECConstError = float(logs01_params[1][31]) / 100 * float(logs01_params[1][30])
        smp.K40BetaNConst = float(logs01_params[1][32])
        smp.K40BetaNConstError = float(logs01_params[1][33]) / 100 * float(logs01_params[1][32])
        smp.Cl36Const = float(logs01_params[1][34])
        smp.Cl36ConstError = float(logs01_params[1][35]) / 100 * float(logs01_params[1][34])
        smp.K40Const = float(logs01_params[1][36])
        smp.K40ConstError = float(logs01_params[1][37]) / 100 * float(logs01_params[1][36])
        smp.Ar39Const = float(logs01_params[1][38])
        smp.Ar39ConstError = float(logs01_params[1][39]) / 100 * float(logs01_params[1][38])
        smp.Ar37Const = float(logs01_params[1][40])
        smp.Ar37ConstError = float(logs01_params[1][41]) / 100 * float(logs01_params[1][40])

        smp.LaboratoryName = str(logs01_params[1][44])

        smp.Ar40vsAr36AirConst = float(logs01_params[1][70])
        smp.Ar40vsAr36AirConstError = float(logs01_params[1][71]) / 100 * float(logs01_params[1][70])

        primaryStandardInfo = str(logs01_params[1][81]).split(":")
        smp.PrimaryStdName = str(logs01_params[1][82]).split(":")[-1]
        smp.PrimaryStdAr40Conc = float(primaryStandardInfo[0])
        smp.PrimaryStdAr40ConcError = float(primaryStandardInfo[1]) / 100 * float(primaryStandardInfo[0])
        smp.PrimaryStdKConc = float(primaryStandardInfo[2])
        smp.PrimaryStdKConcError = float(primaryStandardInfo[3]) / 100 * float(primaryStandardInfo[2])
        smp.PrimaryStdAge = float(primaryStandardInfo[4])
        smp.PrimaryStdAgeError = float(primaryStandardInfo[5]) / 100 * float(primaryStandardInfo[4])

        smp.K40Activity = smp.K40ECActivity + smp.K40BetaNActivity + smp.K40BetaPActivity
        smp.K40ActivityError = FuncsCalc.error_add(
            smp.K40ECActivityError, smp.K40BetaNActivityError, smp.K40BetaPActivityError)

        smp.LinMassDiscrLaw = 1 if logs01_params[1][67] == 'LIN' else 0
        smp.ExpMassDiscrLaw = 1 if logs01_params[1][67] == 'EXP' else 0
        smp.PowMassDiscrLaw = 1 if logs01_params[1][67] == 'POW' else 0
        smp.UseDecayConst = 1 if str(logs01_params[1][88]).capitalize() == "True" else 0
        smp.RecalibrationToPrimary = 1 if str(logs01_params[1][89]).capitalize() == "True" else 0
        smp.RecalibrationUseAge = 1 if str(logs01_params[1][90]).capitalize() == "True" else 0
        smp.RecalibrationUseRatio = 1 if str(logs01_params[1][92]).capitalize() == "True" else 0
        smp.CorrBlank = 1

def _readFilteredFile(smp, res):
    smp.MSequenceList = [value[0] for value in list(res[0].values())]
    smp.MStepsList = [value[1] for value in list(res[0].values())]
    smp.Ar36MList = [value[2] for value in list(res[0].values())]
    smp.Ar37MList = [value[5] for value in list(res[0].values())]
    smp.Ar38MList = [value[8] for value in list(res[0].values())]
    smp.Ar39MList = [value[11] for value in list(res[0].values())]
    smp.Ar40MList = [value[14] for value in list(res[0].values())]
    smp.Ar36MErrorList = [value[3] for value in list(res[0].values())]
    smp.Ar37MErrorList = [value[6] for value in list(res[0].values())]
    smp.Ar38MErrorList = [value[9] for value in list(res[0].values())]
    smp.Ar39MErrorList = [value[12] for value in list(res[0].values())]
    smp.Ar40MErrorList = [value[15] for value in list(res[0].values())]
    smp.MDateTimeList = [value[17:22] for value in list(res[0].values())]
    
    smp.BStepsList = [value[1] for value in list(res[1].values())]
    smp.BSequenceList = [value[2] for value in list(res[1].values())]
    smp.Ar36BList = [value[3] for value in list(res[1].values())]
    smp.Ar37BList = [value[5] for value in list(res[1].values())]
    smp.Ar38BList = [value[7] for value in list(res[1].values())]
    smp.Ar39BList = [value[9] for value in list(res[1].values())]
    smp.Ar40BList = [value[11] for value in list(res[1].values())]
    smp.Ar36BErrorList = [value[4] for value in list(res[1].values())]
    smp.Ar37BErrorList = [value[6] for value in list(res[1].values())]
    smp.Ar38BErrorList = [value[8] for value in list(res[1].values())]
    smp.Ar39BErrorList = [value[10] for value in list(res[1].values())]
    smp.Ar40BErrorList = [value[12] for value in list(res[1].values())]


"""
Corrections
"""
def corrBlank(smp: sample.Sample):
    """
    Blank correction
    """
    if smp.CorrBlank:
        smp.Ar36List, smp.Ar36ErrorList \
            = FuncsCalc.corr_blank(smp.Ar36MList, smp.Ar36MErrorList, smp.Ar36BList, smp.Ar36BErrorList)
        smp.Ar37List, smp.Ar37ErrorList \
            = FuncsCalc.corr_blank(smp.Ar37MList, smp.Ar37MErrorList, smp.Ar37BList, smp.Ar37BErrorList)
        smp.Ar38List, smp.Ar38ErrorList \
            = FuncsCalc.corr_blank(smp.Ar38MList, smp.Ar38MErrorList, smp.Ar38BList, smp.Ar38BErrorList)
        smp.Ar39List, smp.Ar39ErrorList \
            = FuncsCalc.corr_blank(smp.Ar39MList, smp.Ar39MErrorList, smp.Ar39BList, smp.Ar39BErrorList)
        smp.Ar40List, smp.Ar40ErrorList \
            = FuncsCalc.corr_blank(smp.Ar40MList, smp.Ar40MErrorList, smp.Ar40BList, smp.Ar40BErrorList)

def corrDiscr(smp: sample.Sample):
    """
    Discrimination correction
    """
    def _func(a0, e0, f):
        k1 = [FuncsCalc.error_mul((a0[i], e0[i]), (f[0], f[1])) for i in range(len(a0))]
        k0 = [a0[i] * f[0] for i in range(len(a0))]
        return k0, k1
    if smp.CorrDiscr:
        # Mass Discrimination based on the mass of Ar40, Ar36 | Ar37 | Ar38 | Ar39
        MDF, sMDF = smp.MDF, smp.MDFError  # absolute error
        M36, M37, M38, M39, M40 = smp.Ar36Mass, smp.Ar37Mass, smp.Ar38Mass, smp.Ar39Mass, smp.Ar40Mass
        c = FuncsCalc.corr_discr(MDF, sMDF, M36, M40)  # 36Ar
        smp.Ar36List, smp.Ar36ErrorList = _func(smp.Ar36List, smp.Ar36ErrorList, c)
        c = FuncsCalc.corr_discr(MDF, sMDF, M37, M40)  # 37Ar
        smp.Ar37List, smp.Ar37ErrorList = _func(smp.Ar37List, smp.Ar37ErrorList, c)
        c = FuncsCalc.corr_discr(MDF, sMDF, M38, M40)  # 38Ar
        smp.Ar38List, smp.Ar38ErrorList = _func(smp.Ar38List, smp.Ar38ErrorList, c)
        c = FuncsCalc.corr_discr(MDF, sMDF, M39, M40)  # 39Ar
        smp.Ar39List, smp.Ar39ErrorList = _func(smp.Ar39List, smp.Ar39ErrorList, c)

def corrDecay(smp: sample.UnkSample or sample.MonitorSample):
    """
    Decay correction
    """
    def _func(a0, e0, f):
        k1 = FuncsCalc.error_mul((a0, e0), (f[0], f[1]))
        k0 = a0 * f[0]
        return k0, k1
    # Decay Correction
    t2 = smp.IrradiationEndTimeList  # irradiation end time in second
    t3 = smp.IrradiationDurationList  # irradiation duration time in hour
    if smp.Corr37ArDecay:
        for row in range(len(smp.Ar37List)):
            c = FuncsCalc.corr_decay(smp.MDateTimeList[row], t2, t3, smp.Ar37Const, smp.Ar37ConstError)  # 37Ar
            smp.Ar37List[row], smp.Ar37ErrorList[row] \
                = _func(smp.Ar37List[row], smp.Ar37ErrorList[row], c)
    if smp.Corr39ArDecay:
        for row in range(len(smp.Ar39List)):
            c = FuncsCalc.corr_decay(smp.MDateTimeList[row], t2, t3, smp.Ar39Const, smp.Ar39ConstError)  # 39Ar
            smp.Ar39List[row], smp.Ar39ErrorList[row] \
                = _func(smp.Ar39List[row], smp.Ar39ErrorList[row], c)

def degasPattern(smp: sample.UnkSample or sample.MonitorSample):
    """
    Degas Pattern
    """
    def _mul(a0, e0, f, sf, state: bool):
        k1 = [FuncsCalc.error_mul((a0[i], e0[i]), (f, sf)) if state else 0 for i in range(len(a0))]
        k0 = [a0[i] * f if state else 0 for i in range(len(a0))]
        return k0, k1

    def _sub(a0, e0, a1, e1, state: bool):
        k1 = [FuncsCalc.error_add(e0[i], e1[i]) if state else 0 for i in range(len(a0))]
        k0 = [a0[i] - a1[i] if state else 0 for i in range(len(a0))]
        return k0, k1

    def _second(datetime: list, endtime: list):
        t_day, t_month, t_year, t_hour, t_min = datetime
        return [(FuncsCalc.get_datetime(t_year, t_month, t_day, t_hour, t_min) - i) / (3600 * 24 * 365.242) for i in
                endtime]
    # Corr Ca
    smp.Ar37DegasCa, smp.Ar37DegasCaError = _mul(smp.Ar37List, smp.Ar37ErrorList, 1, 0, smp.CorrCa)
    # Force negative values to zero
    smp.Ar37DegasCa = [0 if i < 0 and smp.ForceNegative else i for i in smp.Ar37DegasCa]
    smp.Ar36DegasCa, smp.Ar36DegasCaError \
        = _mul(smp.Ar37DegasCa, smp.Ar37DegasCaError, smp.Ar36vsAr37Ca, smp.Ar36vsAr37CaError, smp.CorrCa)
    smp.Ar38DegasCa, smp.Ar38DegasCaError \
        = _mul(smp.Ar37DegasCa, smp.Ar37DegasCaError, smp.Ar38vsAr37Ca, smp.Ar38vsAr37CaError, smp.CorrCa)
    smp.Ar39DegasCa, smp.Ar39DegasCaError \
        = _mul(smp.Ar37DegasCa, smp.Ar37DegasCaError, smp.Ar39vsAr37Ca, smp.Ar39vsAr37CaError, smp.CorrCa)
    smp.Ar40DegasCa, smp.Ar40DegasCaError = _mul(smp.Ar37DegasCa, smp.Ar37DegasCaError, 0, 0, False)
    # Corr K
    smp.Ar39DegasK, smp.Ar39DegasKError\
        = _sub(smp.Ar39List, smp.Ar39ErrorList, smp.Ar39DegasCa, smp.Ar39DegasCaError, smp.CorrK)
    # Force negative values to zero
    smp.Ar39DegasK = [0 if i < 0 and smp.ForceNegative else i for i in smp.Ar39DegasK]
    smp.Ar40DegasK, smp.Ar40DegasKError\
        = _mul(smp.Ar39DegasK, smp.Ar39DegasKError, smp.Ar40vsAr39K, smp.Ar40vsAr39KError, smp.CorrK)
    smp.Ar38DegasK, smp.Ar38DegasKError\
        = _mul(smp.Ar39DegasK, smp.Ar39DegasKError, smp.Ar38vsAr39K, smp.Ar38vsAr39KError, smp.CorrK)
    smp.Ar36DegasK, smp.Ar36DegasKError = _mul(smp.Ar39DegasK, smp.Ar39DegasKError, 0, 0, False)
    smp.Ar37DegasK, smp.Ar37DegasKError = _mul(smp.Ar39DegasK, smp.Ar39DegasKError, 0, 0, False)
    # Corr Cl
    try:
        if not smp.CorrCl:
            raise ValueError("Do not Correct Cl")
        stand_time_year = [_second(datetime, smp.IrradiationEndTimeList)[-1] for datetime in smp.MDateTimeList]
        # 36Ar deduct Ca, that is sum of 36Ara and 36ArCl
        v36acl = [smp.Ar36List[i] - smp.Ar36DegasCa[i] for i in range(len(smp.Ar36List))]
        sv36acl = [FuncsCalc.error_add(smp.Ar36ErrorList[i], smp.Ar36DegasCaError[i]) for i in
                   range(len(smp.Ar36ErrorList))]
        # 38Ar deduct K and Ca, that is sum of 38Ara and 38ArCl
        v38acl = [smp.Ar38List[i] - smp.Ar38DegasK[i] - smp.Ar38DegasCa[i] for i in range(len(smp.Ar38List))]
        sv38acl = [FuncsCalc.error_add(smp.Ar38ErrorList[i], smp.Ar38DegasKError[i], smp.Ar38DegasCaError[i])
                   for i in range(len(v38acl))]
        v3 = [smp.Cl36vs38Productivity * (1 - exp(-1 * smp.Cl36Const * stand_time_year[i])) for i in
              range(len(stand_time_year))]
        s3 = [pow((smp.Cl36vs38ProductivityError * (1 - exp(-1 * smp.Cl36Const * stand_time_year[i]))) ** 2 +
                  (smp.Cl36vs38Productivity * stand_time_year[i] * (exp(-1 * smp.Cl36Const * stand_time_year[i])) *
                   smp.Cl36ConstError) ** 2, 0.5) for i in range(len(stand_time_year))]
        s3 = [FuncsCalc.error_div((1, 0), (v3[i], s3[i])) for i in range(len(s3))]
        v3 = [1 / v3[i] for i in range(len(v3))]
        # 36ArCl
        smp.Ar36DegasCl = [(v36acl[i] * smp.Ar38vsAr36Trapped - v38acl[i]) / (smp.Ar38vsAr36Trapped - v3[i]) for i in range(len(v36acl))]
        s1 = [(sv36acl[i] * smp.Ar38vsAr36Trapped / (smp.Ar38vsAr36Trapped - v3[i])) ** 2
              for i in range(len(smp.Ar36DegasCl))]
        s2 = [(sv38acl[i] / (smp.Ar38vsAr36Trapped - v3[i])) ** 2 for i in range(len(smp.Ar36DegasCl))]
        s3 = [(s3[i] * (v36acl[i] * smp.Ar38vsAr36Trapped - v38acl[i]) / (smp.Ar38vsAr36Trapped - v3[i]) ** 2) ** 2
              for i in range(len(smp.Ar36DegasCl))]
        s4 = [(v36acl[i] / (smp.Ar38vsAr36Trapped - v3[i]) -
               (v36acl[i] * smp.Ar38vsAr36Trapped - v38acl[i]) / (smp.Ar38vsAr36Trapped - v3[i]) ** 2) ** 2 * (
                smp.Ar38vsAr36TrappedError) ** 2 for i in range(len(smp.Ar36DegasCl))]
        smp.Ar36DegasClError = [pow(s1[i] + s2[i] + s3[i] + s4[i], 0.5) for i in range(len(smp.Ar36DegasCl))]
        # Force negative values to zero
        smp.Ar36DegasCl = [0 if i < 0 and smp.ForceNegative else i for i in smp.Ar36DegasCl]
        '''
        # force 36ArCl to zero if 36Ar - 36ArCa - 36Cl < 0
        sp.Ar36DegasClError = [sp.Ar36DegasClError[i] if v36acl[i] - sp.Ar36DegasCl[i] >= 0 else 0 for i in range(len(sp.Ar36DegasClError))]
        sp.Ar36DegasCl = [sp.Ar36DegasCl[i] if v36acl[i] - sp.Ar36DegasCl[i] >= 0 else 0 for i in range(len(sp.Ar36DegasCl))]
        '''
        # 38ArCl
        smp.Ar38DegasClError = [FuncsCalc.error_mul((smp.Ar36DegasCl[i], smp.Ar36DegasClError[i]), (v3[i], s3[i]))
                                for i in range(len(smp.Ar36DegasCl))]
        smp.Ar38DegasCl = [smp.Ar36DegasCl[i] * v3[i] for i in range(len(smp.Ar36DegasCl))]
        smp.Ar37DegasCl, smp.Ar37DegasClError = [0] * len(smp.Ar36DegasCl), [0] * len(smp.Ar36DegasCl)
        smp.Ar39DegasCl, smp.Ar39DegasClError = [0] * len(smp.Ar36DegasCl), [0] * len(smp.Ar36DegasCl)
        smp.Ar40DegasCl, smp.Ar40DegasClError = [0] * len(smp.Ar36DegasCl), [0] * len(smp.Ar36DegasCl)
    except Exception as e:
        print('Error in corr Cl: {}, lines: {}'.format(e, e.__traceback__.tb_lineno))
        n = len(smp.Ar36List)
        smp.Ar36DegasCl, smp.Ar36DegasClError = [0] * n, [0] * n
        smp.Ar37DegasCl, smp.Ar37DegasClError = [0] * n, [0] * n
        smp.Ar38DegasCl, smp.Ar38DegasClError = [0] * n, [0] * n
        smp.Ar39DegasCl, smp.Ar39DegasClError = [0] * n, [0] * n
        smp.Ar40DegasCl, smp.Ar40DegasClError = [0] * n, [0] * n
    # Corr Atm
    if smp.CorrAtm:
        # 36ArAir
        smp.Ar36DegasAir = [smp.Ar36List[i] - smp.Ar36DegasCa[i] - smp.Ar36DegasCl[i] - smp.Ar36DegasK[i] for i in
                            range(len(smp.Ar36List))]
        smp.Ar36DegasAirError = [
            FuncsCalc.error_add(smp.Ar36ErrorList[i], smp.Ar36DegasCaError[i], smp.Ar36DegasClError[i],
                                smp.Ar36DegasKError[i])for i in range(len(smp.Ar36DegasCl))]
        # Force negative values to zero
        smp.Ar36DegasAir = [0 if i < 0 and smp.ForceNegative else i for i in smp.Ar36DegasAir]

        # 38ArAir
        smp.Ar38DegasAir = [smp.Ar36DegasAir[i] * smp.Ar38vsAr36Trapped for i in range(len(smp.Ar36DegasAir))]
        smp.Ar38DegasAirError = [
            FuncsCalc.error_mul((smp.Ar36DegasAir[i], smp.Ar36DegasAirError[i]),
                                (smp.Ar38vsAr36Trapped, smp.Ar38vsAr36TrappedError)) for i in
            range(len(smp.Ar36DegasAir))]

        # 40ArAir
        smp.Ar40DegasAir = [smp.Ar36DegasAir[i] * smp.Ar40vsAr36Trapped for i in range(len(smp.Ar36DegasAir))]
        smp.Ar40DegasAirError = [
            FuncsCalc.error_mul((smp.Ar36DegasAir[i], smp.Ar36DegasAirError[i]),
                                (smp.Ar40vsAr36Trapped, smp.Ar40vsAr36TrappedError)) for i in
            range(len(smp.Ar36DegasAir))]

        smp.Ar37DegasAir, smp.Ar37DegasAirError = [0] * len(smp.Ar36DegasAir), [0] * len(smp.Ar36DegasAir)
        smp.Ar39DegasAir, smp.Ar39DegasAirError = [0] * len(smp.Ar36DegasAir), [0] * len(smp.Ar36DegasAir)

    # 40Arr
    smp.Ar40DegasR = [smp.Ar40List[i] - smp.Ar40DegasCa[i] - smp.Ar40DegasCl[i] - smp.Ar40DegasK[i] - smp.Ar40DegasAir[i]
                      for i in range(len(smp.Ar40List))]
    smp.Ar40DegasRError = [
        FuncsCalc.error_add(smp.Ar40ErrorList[i], smp.Ar40DegasCaError[i], smp.Ar40DegasClError[i],
                            smp.Ar40DegasKError[i], smp.Ar40DegasAirError[i]) for i in range(len(smp.Ar40List))]
    # Force negative values to zero
    smp.Ar40DegasR = [0 if i < 0 and smp.ForceNegative else i for i in smp.Ar40DegasR]

    # 40Arr percentage
    smp.Ar40RPercentage = [
        smp.Ar40DegasR[i] / smp.Ar40List[i] * 100 if smp.Ar40List[i] != 0 else 0
        for i in range(len(smp.Ar40List))]
    smp.Ar39KPercentage = [
        smp.Ar39DegasK[i] / sum(smp.Ar39DegasK) * 100 if sum(smp.Ar39DegasK) != 0 else 0
        for i in range(len(smp.Ar39DegasK))]


"""
Calculations
"""
def calcApparentAge(smp: sample.UnkSample):
    smp.FValues = [smp.Ar40DegasR[i] / smp.Ar39DegasK[i] if smp.Ar39DegasK[i] != 0 else 0
                   for i in range(len(smp.Ar40DegasR))]
    smp.FValuesError = [
        FuncsCalc.error_div((smp.Ar40DegasR[i], smp.Ar40DegasRError[i]), (smp.Ar39DegasK[i], smp.Ar39DegasKError[i]))
        if smp.Ar39DegasK[i] != 0 else 0 for i in range(len(smp.Ar40DegasR))]
    k0 = [calcAge(smp.FValues[i], smp.FValuesError[i], smp) for i in range(len(smp.FValues))]
    age, s1, s2, s3 = [i[0] for i in k0], [i[1] for i in k0], [i[2] for i in k0], [i[3] for i in k0]
    smp.ApparentAge, smp.ApparentAgeAnalysisError, smp. ApparentAgeInternalError, smp.ApparentAgeFullExternalError = \
        age, s1, s2, s3

def calcKCaClRatios(smp: sample.UnkSample):
    def _func(a0: list, e0: list, a1: list, e1: list, f: float, sf: float):
        n = min(len(a0), len(e0), len(a1), len(e1))
        k0 = [f * a0[i] / a1[i] if a1[i] != 0 else 0 for i in range(n)]
        k1 = [FuncsCalc.error_mul((f, sf), (a0[i] / a1[i], FuncsCalc.error_div((a0[i], e0[i]), (a1[i], e1[i]))))
              if a1[i] != 0 else 0 for i in range(n)]
        return k0, k1

    isKCa = False
    if isKCa:
        # K/Ca
        smp.KCaRatios, smp.KCaRatiosError = \
            _func(smp.Ar39DegasK, smp.Ar39DegasKError, smp.Ar37DegasCa, smp.Ar37DegasCaError,
                  smp.KvsCaFactor, smp.KvsCaFactorError)
    else:
        # Ca/K
        smp.KCaRatios, smp.KCaRatiosError = \
            _func(smp.Ar37DegasCa, smp.Ar37DegasCaError, smp.Ar39DegasK, smp.Ar39DegasKError,
                  1 / smp.KvsCaFactor, FuncsCalc.error_div((1, 0), (smp.KvsCaFactor, smp.KvsCaFactorError)))
    isKCl = True
    if isKCl:
        # K/Cl
        smp.KClRatios, smp.KClRatiosError = \
            _func(smp.Ar39DegasK, smp.Ar39DegasKError, smp.Ar38DegasCl, smp.Ar38DegasClError,
                  smp.KvsClFactor, smp.KvsClFactorError)
    else:
        # Cl/K
        smp.KClRatios, smp.KClRatiosError = \
            _func(smp.Ar38DegasCl, smp.Ar38DegasClError, smp.Ar39DegasK, smp.Ar39DegasKError,
                  1 / smp.KvsClFactor, FuncsCalc.error_div((1, 0), (smp.KvsClFactor, smp.KvsClFactorError)))
    isCaCl = True
    if isCaCl:
        # Ca/Cl
        smp.CaClRatios, smp.CaClRatiosError = \
            _func(smp.Ar37DegasCa, smp.Ar37DegasCaError, smp.Ar38DegasCl, smp.Ar38DegasClError,
                  smp.CavsClFactor, smp.CavsClFactorError)
    else:
        # Cl/Ca
        smp.CaClRatios, smp.CaClRatiosError = \
            _func(smp.Ar38DegasCl, smp.Ar38DegasClError, smp.Ar37DegasCa, smp.Ar37DegasCaError,
                  1 / smp.KvsClFactor, FuncsCalc.error_div((1, 0), (smp.CavsClFactor, smp.CavsClFactorError)))

def calcRatios(smp: sample.UnkSample):
    """
    Get ratios using to plot isochron diagrams.
    """
    def _getIsochron(x, sx, y, sy, z, sz):
        _n = min([len(x), len(sx), len(y), len(sy), len(z), len(sz)])
        # x / z
        k0 = [x[i] / z[i] if z[i] != 0 else 0 for i in range(_n)]
        k1 = [FuncsCalc.error_div((x[i], sx[i]), (z[i], sz[i])) if z[i] != 0 else 0 for i in range(_n)]
        # y / z
        k2 = [y[i] / z[i] if z[i] != 0 else 0 for i in range(_n)]
        k3 = [FuncsCalc.error_div((y[i], sy[i]), (z[i], sz[i])) if z[i] != 0 else 0 for i in range(_n)]
        pho = [FuncsCalc.error_cor(sx[i] / x[i], sy[i] / y[i], sz[i] / z[i]) if x[i] * y[i] * z[i] != 0 else 0
               for i in range(_n)]
        return [k0, k1, k2, k3, pho, []]
    # Cl isochron 1: 39ArK / 38ArCl vs. 40Ar* / 38ArCl, 40Ar* = 40ArCl+r
    smp.ClNormalIsochron = _getIsochron(smp.Ar39DegasK, smp.Ar39DegasKError,
                                        smp.Ar40DegasR, smp.Ar40DegasRError,
                                        smp.Ar38DegasCl, smp.Ar38DegasClError)
    # Cl isochron 2: 39ArK / 40Ar* vs. 38ArCl / 40Ar*
    smp.ClInverseIsochron = _getIsochron(smp.Ar39DegasK, smp.Ar39DegasKError,
                                         smp.Ar38DegasCl, smp.Ar38DegasClError,
                                         smp.Ar40DegasR, smp.Ar40DegasRError)
    # Cl isochron 3: 40Ar* / 39ArK vs. 38ArCl / 39ArK
    smp.ClKIsochron = _getIsochron(smp.Ar40DegasR, smp.Ar40DegasRError,
                                   smp.Ar38DegasCl, smp.Ar38DegasClError,
                                   smp.Ar39DegasK, smp.Ar39DegasKError)
    # normal isochron: 39ArK / 36Ara vs. 40Ar* / 36Ara, 40Ar* = 40Ara+r, however it is actually 40Ara+r+Cl
    c = [smp.Ar40List[i] - smp.Ar40DegasK[i] - smp.Ar40DegasCa[i] - smp.Ar40DegasCl[i]
         for i in range(len(smp.Ar40List))]
    sc = [FuncsCalc.error_add(smp.Ar40ErrorList[i], smp.Ar40DegasKError[i], smp.Ar40DegasCaError[i],
                              smp.Ar40DegasClError[i]) for i in range(len(smp.Ar40List))]
    c = [0 if i < 0 else i for i in c]
    smp.AtmNormalIsochron = _getIsochron(smp.Ar39DegasK, smp.Ar39DegasKError,
                                         c, sc,
                                         smp.Ar36DegasAir, smp.Ar36DegasAirError)
    # inverse isochron: 39ArK / 40Ar* vs. 36Ara / 40Ar*
    smp.AtmInverseIsochron = _getIsochron(smp.Ar39DegasK, smp.Ar39DegasKError,
                                          smp.Ar36DegasAir, smp.Ar36DegasAirError,
                                          c, sc)
    # 3D isochron: 39ArK / 40Ar* vs. 36Ara / 40Ar* vs. 38ArCl / 40Ar*, 40Ar* = 40Ara+r+Cl
    c1 = _getIsochron(smp.Ar38DegasCl, smp.Ar38DegasClError, smp.Ar39DegasK, smp.Ar39DegasKError, c, sc)
    smp.ThreeDIsochron = [smp.AtmInverseIsochron[0], smp.AtmInverseIsochron[1],  # 39ArK / 40Ar*, error --> Z
                          smp.AtmInverseIsochron[2], smp.AtmInverseIsochron[3],  # 36Ara / 40Ar*, error --> X
                          c1[0], c1[1],  # 38ArCl / 40Ar*, error --> Y
                          smp.AtmInverseIsochron[4], smp.ClInverseIsochron[4], c1[4],  # pho_ZX, pho_ZY, pho_XZ
                          []]  # age

def calcAge(F, sF, smp: sample.UnkSample):
    k0 = FuncsCalc.calc_age(
        F, sF, smp.JValue, smp.JValueError, smp.K40Const, smp.K40ConstError,
        uf=1, useDecayConst=smp.UseDecayConst, recalibrationPrimary=smp.RecalibrationToPrimary,
        usePrimaryAge=smp.RecalibrationUseAge, usePrimaryRatio=smp.RecalibrationUseRatio,
        activity_of_K=smp.K40Activity, activity_of_K_error=smp.K40ActivityError,
        activity_of_K_to_Ar=smp.K40ECActivity,
        activity_of_K_to_Ar_error=smp.K40ECActivityError,
        activity_of_K_to_Ca=smp.K40BetaNActivity,
        activity_of_K_to_Ca_error=smp.K40BetaNActivityError,
        atomic_weight_of_K=smp.K40Mass, atomic_weight_of_K_error=smp.K40MassError,
        seconds_in_a_year=smp.YearConst, seconds_in_a_year_error=smp.YearConstError,
        fraction_of_40K=smp.K40vsKFractions, fraction_of_40K_error=smp.K40vsKFractionsError,
        avogadro_number=smp.NoConst, avogadro_number_error=smp.NoConstError,
        decay_constant_of_40K=smp.K40Const, decay_constant_of_40K_error=smp.K40ConstError,
        decay_constant_of_40K_EC=smp.K40ECConst,
        decay_constant_of_40K_EC_error=smp.K40ECConstError,
        standard_age=smp.StandardAge, standard_age_error=smp.StandardAgeError,
        standard_Ar_conc=smp.PrimaryStdAr40Conc,
        standard_Ar_conc_error=smp.PrimaryStdAr40ConcError,
        standard_K_conc=smp.PrimaryStdKConc, standard_K_conc_error=smp.PrimaryStdKConcError,
        standard_40K_K=smp.PrimaryStdAr40vsK, standard_40K_K_error=smp.PrimaryStdAr40vsKError
    )
    return k0

def calcIsochronAge(smp: sample.UnkSample):
    def _getIsochronAge(iso, isNormal=False, isInverse=False, isKIsochron=False):
        try:
            x, sx, y, sy, pho = [[i[j] for j in smp.IsochronSelectedPoints] for i in iso]
            k0 = FuncsCalc.isochron_regress(
                x, sx, y, sy, pho,
                isNormal=isNormal, isInverse=isInverse, isKIsochron=isKIsochron,
                statistics=True, convergence=smp.York2FitConvergence,
                iteration=smp.York2FitIteration
            )
            if not k0:
                raise ValueError("raise error")
        except Exception as e:
            return ['Null'] * 16
        k1 = calcAge(k0[2], k0[3], smp)
        k2 = (x, sx, y, sy, pho, smp.IsochronSelectedPoints)
        '''list in order: '''
        '''0-3: Age, analytical error, internal error, full external error'''
        '''4-15: ratio, error, 40r/39k, error, MSWD, b, seb, m, sem, convergence, iterations, error magnification'''
        '''16-21: x, sx, y, sy, pho, sp.IsochronSelectedPoints'''
        return [i for i in k1 + k0 + k2]
    smp.ClNormalIsochron[5] = _getIsochronAge(smp.ClNormalIsochron[:5], isNormal=True)
    smp.ClInverseIsochron[5] = _getIsochronAge(smp.ClInverseIsochron[:5], isInverse=True)
    smp.ClKIsochron[5] = _getIsochronAge(smp.ClKIsochron[:5], isKIsochron=True)
    smp.AtmNormalIsochron[5] = _getIsochronAge(smp.AtmNormalIsochron[:5], isNormal=True)
    smp.AtmInverseIsochron[5] = _getIsochronAge(smp.AtmInverseIsochron[:5], isInverse=True)

def calcPlateauAge(smp: sample.UnkSample):
    def _plateau(points: list):
        if not points:
            return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        F, sF = [smp.FValues[i] for i in points], [smp.FValuesError[i] for i in points]
        k4, k5, k6, k7 = FuncsCalc.err_wtd_mean(F, sF)  # weighted F, error, dp, MSWD
        k0, k1, k2, k3 = calcAge(k4, k5, smp)  # age, analysis error, internal error, full external error
        k8 = sum([smp.Ar39DegasK[i] for i in points]) / sum(smp.Ar39DegasK)  # accumulative 39ArK
        k9 = points  # selected steps
        return [k0, k1, k2, k3, k4, k5, k6, k7, k8, k9]
    smp.PlateauAges = []
    x, y1, y2 = FuncsCalc.get_spectra(smp.ApparentAge, smp.ApparentAgeInternalError, smp.Ar39DegasK)
    smp.SpectraLines = [x, y1, y2]
    smp.PlateauAges = _plateau(smp.IsochronSelectedPoints)

def calcTFAge(smp: sample.UnkSample):
    a0, e0 = sum(smp.Ar40DegasR), pow(sum([i ** 2 for i in smp.Ar40DegasRError]), 0.5)
    a1, e1 = sum(smp.Ar39DegasK), pow(sum([i ** 2 for i in smp.Ar39DegasKError]), 0.5)
    F, sF = a0 / a1, FuncsCalc.error_div((a0, e0), (a1, e1))
    k0, k1, k2, k3 = calcAge(F, sF, smp)
    smp.TotalFusionAge = [k0, k1, k2, k3, F, sF, len(smp.Ar40DegasR)]  # TF age, e1, e2, e3, 40Arr/39Ark, error, dp

def calc3DIsochronAge(smp: sample.UnkSample):
    def _pick(a0: list):
        return [a0[i] for i in smp.IsochronSelectedPoints]

    z, sz, x, sx, y, sy, pho_zx, pho_zy, pho_xy, [] = smp.ThreeDIsochron
    try:
        k0 = FuncsCalc.intercept_linest(_pick(z), _pick(x), _pick(y))  # z = k[0] + k[5][0] * x + k[5][1] * y
        if not k0:
            raise ValueError("raise error")
    except Exception as e:
        print("Error Information: Sample: {}, Type: {}, Info: {}".format(smp.SampleName, e.__class__.__name__, e))
        k0 = None
        k1 = [0, 0, 0, 0]
    else:
        k1 = list(calcAge(k0[0], 0, smp))
    k1.append(k0)
    smp.ThreeDIsochron[9] = k1

def calcJValue(smp: sample.MonitorSample):
    smp.MonitorJValue, smp.MonitorJValueError = \
        FuncsCalc.j_value(smp.MonitorAge, smp.MonitorAgeError, smp.TotalF, smp.TotalFError,
                          smp.K40Const, smp.K40ConstError)

def calcMDF(smp: sample.AirSample):
    smp.AirMDF, smp.AirMDF = \
        FuncsCalc.get_mdf(smp.AirRatio, smp.AirRatioError, smp.Ar36Mass, smp.Ar40Mass)


"""
Plot
"""
def plotAgeSpectra(smp: sample.UnkSample):
    canvas = FuncsPlot.get_default_canvas()
    canvas.axes.plot(smp.SpectraLines[0], smp.SpectraLines[1], smp.SpectraLines[0], smp.SpectraLines[2],
                     color='r', linestyle='-', linewidth=1, markersize=0)
    pyplot.plot(smp.SpectraLines[0], smp.SpectraLines[1], smp.SpectraLines[0], smp.SpectraLines[2],
                color='r', linestyle='-', linewidth=1, markersize=0)
    pyplot.show()

def plot3DIsochron(smp: sample.UnkSample):
    canvas = FuncsPlot.get_default_canvas()
    axes = pyplot.axes(projection='3d')
    axes.scatter3D(smp.ThreeDIsochron[2], smp.ThreeDIsochron[4], smp.ThreeDIsochron[0])
    """plot surface"""
    x = np.array([0, axes.get_xlim()[0], axes.get_xlim()[1]])
    y = np.array([0, axes.get_ylim()[0], axes.get_ylim()[1]])
    x, y = np.meshgrid(x, y)
    k = smp.ThreeDIsochron[9][4]
    if k:
        z = k[0] + k[5][0] * x + k[5][1] * y
        axes.plot_surface(x, y, z, facecolor='r', linewidth=0, antialiased=False)
    pyplot.show()

def plotIsochron(smp: sample.UnkSample):
    def _getCanvas():
        canvas = FuncsPlot.get_default_canvas()
    pyplot.scatter(smp.AtmNormalIsochron[0], smp.AtmNormalIsochron[2])
    pyplot.show()
    pyplot.scatter(smp.AtmInverseIsochron[0], smp.AtmInverseIsochron[2])
    pyplot.show()
    pyplot.scatter(smp.ClNormalIsochron[0], smp.ClInverseIsochron[2])
    pyplot.show()
    pyplot.scatter(smp.ClNormalIsochron[0], smp.ClNormalIsochron[2])
    pyplot.show()
    pyplot.scatter(smp.ClKIsochron[0], smp.ClKIsochron[2])
    pyplot.show()


'''
Setting
'''
def setIrraParams(smp: sample.Sample, *args, **kwargs):
    if not args and not kwargs:
        return False
    elif not args:
        return "new params project"
    elif not kwargs:
        return "change params project"
    else:
        pass
