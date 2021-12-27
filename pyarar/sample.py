#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : sample.py
# @Author : Yang Wu
# @Date   : 2021/12/19
# @Email  : wuy@cug.edu.cn

"""
Create a sample instance.
"""

import pickle
import datetime
from pyarar.constants import *
from pyarar.calcFuncs import *

class Sample:
    def __init__(self, **kwargs):
        """
        Create a sample instance.

        parameters
        ----------
        SampleID: int, default: None
            unique number of every instance, it is defined based on the datetime the instance was created.

        Other sample information: str, default: None
            user input.

        Calculation Params: float or bool, default: constants
            user define or inherit from the default.

        Attached files: str
            the file path user input.
        """
        self.SampleID: int = int((datetime.datetime.now() - datetime.datetime(2000, 1, 1)).total_seconds() * 100)
        self.SampleName: str = kwargs.pop("SampleName", "")
        self.SampleOwner: str = kwargs.pop("SampleOwner", "")
        self.SampleType: str = kwargs.pop("SampleType", "")
        self.SampleMineral: str = kwargs.pop("SampleMineral", "")
        self.SampleEstimatedAge: str = kwargs.pop("SampleEstimatedAge", "")
        self.SampleDescription: str = kwargs.pop("SampleDescription", "")
        self.SampleLocation: str = kwargs.pop("SampleLocation", "")
        self.ExperimentName: str = kwargs.pop("ExperimentName", "")
        self.ExperimentAnalyst: str = kwargs.pop("ExperimentAnalyst", "")
        self.LaboratoryName: str = kwargs.pop("LaboratoryName", "")
        self.LaboratoryInfo: str = kwargs.pop("LaboratoryInfo", "")

        self.MSequenceList: list = kwargs.pop("MSequenceList", [])
        self.BSequenceList: list = kwargs.pop("BSequenceList", [])
        self.MStepsList: list = kwargs.pop("MStepsList", [])
        self.BStepsList: list = kwargs.pop("BStepsList", [])
        self.MDateTimeList: list = kwargs.pop("MDateTimeList", [])  # [day, mouth, year, hour, min]

        self.Ar36MList: list = kwargs.pop("Ar36MList", [])
        self.Ar37MList: list = kwargs.pop("Ar37MList", [])
        self.Ar38MList: list = kwargs.pop("Ar38MList", [])
        self.Ar39MList: list = kwargs.pop("Ar39MList", [])
        self.Ar40MList: list = kwargs.pop("Ar40MList", [])

        self.Ar36MErrorList: list = kwargs.pop("Ar36MErrorList", [])
        self.Ar37MErrorList: list = kwargs.pop("Ar37MErrorList", [])
        self.Ar38MErrorList: list = kwargs.pop("Ar38MErrorList", [])
        self.Ar39MErrorList: list = kwargs.pop("Ar39MErrorList", [])
        self.Ar40MErrorList: list = kwargs.pop("Ar40MErrorList", [])

        self.Ar36BList: list = kwargs.pop("Ar36BList", [])
        self.Ar37BList: list = kwargs.pop("Ar37BList", [])
        self.Ar38BList: list = kwargs.pop("Ar38BList", [])
        self.Ar39BList: list = kwargs.pop("Ar39BList", [])
        self.Ar40BList: list = kwargs.pop("Ar40BList", [])

        self.Ar36BErrorList: list = kwargs.pop("Ar36BErrorList", [])
        self.Ar37BErrorList: list = kwargs.pop("Ar37BErrorList", [])
        self.Ar38BErrorList: list = kwargs.pop("Ar38BErrorList", [])
        self.Ar39BErrorList: list = kwargs.pop("Ar39BErrorList", [])
        self.Ar40BErrorList: list = kwargs.pop("Ar40BErrorList", [])

        self.Ar36TempList: list = kwargs.pop("Ar36TempList", [])
        self.Ar37TempList: list = kwargs.pop("Ar37TempList", [])
        self.Ar38TempList: list = kwargs.pop("Ar38TempList", [])
        self.Ar39TempList: list = kwargs.pop("Ar39TempList", [])
        self.Ar40TempList: list = kwargs.pop("Ar40TempList", [])

        self.Ar36TempErrorList: list = kwargs.pop("Ar36TempErrorList", [])
        self.Ar37TempErrorList: list = kwargs.pop("Ar37TempErrorList", [])
        self.Ar38TempErrorList: list = kwargs.pop("Ar38TempErrorList", [])
        self.Ar39TempErrorList: list = kwargs.pop("Ar39TempErrorList", [])
        self.Ar40TempErrorList: list = kwargs.pop("Ar40TempErrorList", [])

        self.Ar36DegassCa: list = kwargs.pop("Ar36DegassCa", [])
        self.Ar36DegassK: list = kwargs.pop("Ar36DegassK", [])
        self.Ar36DegassCl: list = kwargs.pop("Ar36DegassCl", [])
        self.Ar36DegassAir: list = kwargs.pop("Ar36DegassAir", [])
        self.Ar37DegassCa: list = kwargs.pop("Ar37DegassCa", [])
        self.Ar37DegassK: list = kwargs.pop("Ar37DegassK", [])
        self.Ar37DegassCl: list = kwargs.pop("Ar37DegassCl", [])
        self.Ar37DegassAir: list = kwargs.pop("Ar37DegassAir", [])
        self.Ar38DegassCa: list = kwargs.pop("Ar38DegassCa", [])
        self.Ar38DegassK: list = kwargs.pop("Ar38DegassK", [])
        self.Ar38DegassCl: list = kwargs.pop("Ar38DegassCl", [])
        self.Ar38DegassAir: list = kwargs.pop("Ar38DegassAir", [])
        self.Ar39DegassCa: list = kwargs.pop("Ar39DegassCa", [])
        self.Ar39DegassK: list = kwargs.pop("Ar39DegassK", [])
        self.Ar39DegassCl: list = kwargs.pop("Ar39DegassCl", [])
        self.Ar39DegassAir: list = kwargs.pop("Ar39DegassAir", [])
        self.Ar40DegassCa: list = kwargs.pop("Ar40DegassCa", [])
        self.Ar40DegassK: list = kwargs.pop("Ar40DegassK", [])
        self.Ar40DegassCl: list = kwargs.pop("Ar40DegassCl", [])
        self.Ar40DegassAir: list = kwargs.pop("Ar40DegassAir", [])
        self.Ar40DegassR: list = kwargs.pop("Ar40DegassR", [])

        self.Ar36DegassCaError: list = kwargs.pop("Ar36DegassCaError", [])
        self.Ar36DegassKError: list = kwargs.pop("Ar36DegassKError", [])
        self.Ar36DegassClError: list = kwargs.pop("Ar36DegassClError", [])
        self.Ar36DegassAirError: list = kwargs.pop("Ar36DegassAirError", [])
        self.Ar37DegassCaError: list = kwargs.pop("Ar37DegassCaError", [])
        self.Ar37DegassKError: list = kwargs.pop("Ar37DegassKError", [])
        self.Ar37DegassClError: list = kwargs.pop("Ar37DegassClError", [])
        self.Ar37DegassAirError: list = kwargs.pop("Ar37DegassAirError", [])
        self.Ar38DegassCaError: list = kwargs.pop("Ar38DegassCaError", [])
        self.Ar38DegassKError: list = kwargs.pop("Ar38DegassKError", [])
        self.Ar38DegassClError: list = kwargs.pop("Ar38DegassClError", [])
        self.Ar38DegassAirError: list = kwargs.pop("Ar38DegassAirError", [])
        self.Ar39DegassCaError: list = kwargs.pop("Ar39DegassCaError", [])
        self.Ar39DegassKError: list = kwargs.pop("Ar39DegassKError", [])
        self.Ar39DegassClError: list = kwargs.pop("Ar39DegassClError", [])
        self.Ar39DegassAirError: list = kwargs.pop("Ar39DegassAirError", [])
        self.Ar40DegassCaError: list = kwargs.pop("Ar40DegassCaError", [])
        self.Ar40DegassKError: list = kwargs.pop("Ar40DegassKError", [])
        self.Ar40DegassClError: list = kwargs.pop("Ar40DegassClError", [])
        self.Ar40DegassAirError: list = kwargs.pop("Ar40DegassAirError", [])
        self.Ar40DegassRError: list = kwargs.pop("Ar40DegassRError", [])

        self.RawFilePath: str = kwargs.pop("RawFilePath", "")
        self.FilteredFilePath: str = kwargs.pop("FilteredFilePath", "")
        self.AgeFilePath: str = kwargs.pop("FilteredFilePath", "")

        self.K40vsKFractions: float = kwargs.pop("K40vsKFractions", K40vsKFractions)
        self.K40vsKFractionsError: float = kwargs.pop("K40vsKFractionsError", K40vsKFractionsError)
        self.Cl35vsCl37Fractions: float = kwargs.pop("Cl35vsClFractions", Cl35vsClFractions)
        self.Cl35vsCl37FractionsError: float = kwargs.pop("Cl35vsClFractionsError", Cl35vsClFractionsError)
        self.HClvsClFractions: float = kwargs.pop("HClvsClFractions", HClvsClFractions)
        self.HClvsClFractionsError: float = kwargs.pop("HClvsClFractionsError", HClvsClFractionsError)
        self.Ar40vsAr36AirConst: float = kwargs.pop("Ar40vsAr36AirConst", Ar40vsAr36AirConst)
        self.Ar40vsAr36AirConstError: float = kwargs.pop("Ar40vsAr36AirConstError", Ar40vsAr36AirConstError)
        self.K40Mass: float = kwargs.pop("K40Mass", K40Mass)
        self.K40MassError: float = kwargs.pop("K40MassError", K40MassError)
        self.Ar36Mass: float = kwargs.pop("Ar36Mass", Ar36Mass)
        self.Ar36MassError: float = kwargs.pop("Ar36MassError", Ar36MassError)
        self.Ar37Mass: float = kwargs.pop("Ar37Mass", Ar37Mass)
        self.Ar37MassError: float = kwargs.pop("Ar37MassError", Ar37MassError)
        self.Ar38Mass: float = kwargs.pop("Ar38Mass", Ar38Mass)
        self.Ar38MassError: float = kwargs.pop("Ar38MassError", Ar38MassError)
        self.Ar39Mass: float = kwargs.pop("Ar39Mass", Ar39Mass)
        self.Ar39MassError: float = kwargs.pop("Ar39MassError", Ar39MassError)
        self.Ar40Mass: float = kwargs.pop("Ar40Mass", Ar40Mass)
        self.Ar40MassError: float = kwargs.pop("Ar40MassError", Ar40MassError)

        self.K40Const: float = kwargs.pop("K40Const", K40Const)
        self.K40ConstError: float = kwargs.pop("K40ConstError", K40ConstError)
        self.K40ECConstError: float = kwargs.pop("K40ECConstError", K40ECConstError)
        self.K40ECConst: float = kwargs.pop("K40ECConst", K40ECConst)
        self.K40BetaNConst: float = kwargs.pop("K40BetaNConst", K40BetaNConst)
        self.K40BetaNConstError: float = kwargs.pop("K40BetaNConstError", K40BetaNConstError)
        self.K40BetaPConst: float = kwargs.pop("K40BetaPConst", K40BetaPConst)
        self.K40BetaPConstError: float = kwargs.pop("K40BetaPConstError", K40BetaPConstError)
        self.Ar39Const: float = kwargs.pop("Ar39Const", Ar39Const)
        self.Ar39ConstError: float = kwargs.pop("Ar39ConstError", Ar39ConstError)
        self.Ar37Const: float = kwargs.pop("Ar37Const", Ar37Const)
        self.Ar37ConstError: float = kwargs.pop("Ar37ConstError", Ar37ConstError)
        self.Cl36Const: float = kwargs.pop("Cl36Const", Cl36Const)
        self.Cl36ConstError: float = kwargs.pop("Cl36ConstError", Cl36ConstError)
        self.K40ECActivity: float = kwargs.pop("K40ECActivity", K40ECActivity)
        self.K40ECActivityError: float = kwargs.pop("K40ECActivityError", K40ECActivityError)
        self.K40BetaNActivity: float = kwargs.pop("K40BetaNActivity", K40BetaNActivity)
        self.K40BetaNActivityError: float = kwargs.pop("K40BetaNActivityError", K40BetaNActivityError)
        self.K40BetaPActivity: float = kwargs.pop("K40BetaPActivity", K40BetaPActivity)
        self.K40BetaPActivityError: float = kwargs.pop("K40BetaPActivityError", K40BetaPActivityError)
        self.Cl36vs38Activity: float = kwargs.pop("Cl36vs38Activity", Cl36vs38Activity)
        self.Cl36vs38ActivityError: float = kwargs.pop("Cl36vs38ActivityError", Cl36vs38ActivityError)
        self.NoConst: float = kwargs.pop("NoConst", NoConst)
        self.NoConstError: float = kwargs.pop("NoConstError", NoConstError)
        self.yearConst: float = kwargs.pop("yearConst", yearConst)
        self.yearConstError: float = kwargs.pop("yearConstError", yearConstError)

        self.JValue: float = kwargs.pop("JValue", JValue)
        self.JValueError: float = kwargs.pop("JValueError", JValueError)
        self.MDF: float = kwargs.pop("MDF", MDF)
        self.MDFError: float = kwargs.pop("MDFError", MDFError)
        self.Ar40vsAr36Const: float = kwargs.pop("Ar40vsAr36Const", Ar40vsAr36Const)
        self.Ar40vsAr36ConstError: float = kwargs.pop("Ar40vsAr36ConstError", Ar40vsAr36ConstError)
        self.York2FitConvergence: float = kwargs.pop("York2FitConvergence", York2FitConvergence)
        self.York2FitIteration: float = kwargs.pop("York2FitIteration", York2FitIteration)
        self.Fitting: str = kwargs.pop("Fitting", Fitting)
        self.LinMassDiscrLaw: bool = kwargs.pop("LinMassDiscrLaw", LinMassDiscrLaw)
        self.ExpMassDiscrLaw: bool = kwargs.pop("ExpMassDiscrLaw", ExpMassDiscrLaw)
        self.PowMassDiscrLaw: bool = kwargs.pop("PowMassDiscrLaw", PowMassDiscrLaw)
        self.ForceNegative: bool = kwargs.pop("ForceNegative", ForceNegative)
        self.Corr37ArDecay: bool = kwargs.pop("Corr37ArDecay", Corr37ArDecay)
        self.Corr39ArDecay: bool = kwargs.pop("Corr39ArDecay", Corr39ArDecay)
        self.Corr36ClDecay: bool = kwargs.pop("Corr36ClDecay", Corr36ClDecay)
        self.CorrBlank: bool = kwargs.pop("CorrBlank", CorrBlank)
        self.CorrDiscr: bool = kwargs.pop("CorrDiscr", CorrDiscr)
        self.CorrK: bool = kwargs.pop("CorrK", CorrK)
        self.CorrCa: bool = kwargs.pop("CorrCa", CorrCa)
        self.CorrAtm: bool = kwargs.pop("CorrAtm", CorrAtm)
        self.RelativeError: bool = kwargs.pop("RelativeError", RelativeError)
        self.UseDecayConst: bool = kwargs.pop("UseDecayConst", UseDecayConst)
        self.UseInterceptCorrAtm: bool = kwargs.pop("UseInterceptCorrAtm", UseInterceptCorrAtm)
        self.UseMinCalculation: bool = kwargs.pop("UseMinCalculation", UseMinCalculation)

        self.Ar40vsAr36Trapped: float = kwargs.pop("Ar40vsAr36Trapped", Ar40vsAr36Trapped)
        self.Ar40vsAr36Cosmo: float = kwargs.pop("Ar40vsAr36Cosmo", Ar40vsAr36Cosmo)
        self.Ar38vsAr36Trapped: float = kwargs.pop("Ar38vsAr36Trapped", Ar38vsAr36Trapped)
        self.Ar38vsAr36Cosmo: float = kwargs.pop("Ar38vsAr36Cosmo", Ar38vsAr36Cosmo)
        self.Ar39vsAr37Ca: float = kwargs.pop("Ar39vsAr37Ca", Ar39vsAr37Ca)
        self.Ar38vsAr37Ca: float = kwargs.pop("Ar38vsAr37Ca", Ar38vsAr37Ca)
        self.Ar36vsAr37Ca: float = kwargs.pop("Ar36vsAr37Ca", Ar36vsAr37Ca)
        self.Ar40vsAr39K: float = kwargs.pop("Ar40vsAr39K", Ar40vsAr39K)
        self.Ar38vsAr39K: float = kwargs.pop("Ar38vsAr39K", Ar38vsAr39K)
        self.Ar36vsAr38Cl: float = kwargs.pop("Ar36vsAr38Cl", Ar36vsAr38Cl)
        self.KvsCaFactor: float = kwargs.pop("KvsCaFactor", KvsCaFactor)
        self.KvsClFactor: float = kwargs.pop("KvsClFactor", KvsClFactor)
        self.CavsClFactor: float = kwargs.pop("CavsClFactor", CavsClFactor)
        self.CavsClFactorError: float = kwargs.pop("CavsClFactorError", CavsClFactorError)
        self.KvsClFactorError: float = kwargs.pop("KvsClFactorError", KvsClFactorError)
        self.KvsCaFactorError: float = kwargs.pop("KvsCaFactorError", KvsCaFactorError)
        self.Ar36vsAr38ClError: float = kwargs.pop("Ar36vsAr38ClError", Ar36vsAr38ClError)
        self.Ar38vsAr39KError: float = kwargs.pop("Ar38vsAr39KError", Ar38vsAr39KError)
        self.Ar40vsAr39KError: float = kwargs.pop("Ar40vsAr39KError", Ar40vsAr39KError)
        self.Ar36vsAr37CaError: float = kwargs.pop("Ar36vsAr37CaError", Ar36vsAr37CaError)
        self.Ar38vsAr37CaError: float = kwargs.pop("Ar38vsAr37CaError", Ar38vsAr37CaError)
        self.Ar39vsAr37CaError: float = kwargs.pop("Ar39vsAr37CaError", Ar39vsAr37CaError)
        self.Ar38vsAr36CosmoError: float = kwargs.pop("Ar38vsAr36CosmoError", Ar38vsAr36CosmoError)
        self.Ar38vsAr36TrappedError: float = kwargs.pop("Ar38vsAr36TrappedError", Ar38vsAr36TrappedError)
        self.Ar40vsAr36CosmoError: float = kwargs.pop("Ar40vsAr36CosmoError", Ar40vsAr36CosmoError)
        self.Ar40vsAr36TrappedError: float = kwargs.pop("Ar40vsAr36TrappedError", Ar40vsAr36TrappedError)
        self.IrradiationEndTimeList: list = kwargs.pop("IrradiationEndTimeList", IrradiationEndTimeList)
        self.IrradiationDurationList: list = kwargs.pop("IrradiationDurationList", IrradiationDurationList)

    def readDataFromRawFile(self, path=None):
        """
        Read data from raw file.

        parameters
        ----------
        path: str
            raw file path.
        """
        self.initializeData()
        if path:
            self.RawFilePath = path
        res = open_original_xls(self.RawFilePath)
        if res:
            pass
            # self.Ar36MList = res[2]

    def readDataFromFilteredFile(self, path=None):
        """
        Read data from filtered file.

        parameters
        ----------
        path: str
            filtered file path.
        """
        self.initializeData()
        if path:
            self.FilteredFilePath = path
        res = open_filtered_xls(self.FilteredFilePath)
        if res:
            self._readFilteredFile(res)

    def _readFilteredFile(self, res):
        for key, value in res[0].items():
            self.MSequenceList.append(value[0])
            self.MStepsList.append(value[1])
            self.Ar36MList.append(value[2])
            self.Ar37MList.append(value[5])
            self.Ar38MList.append(value[8])
            self.Ar39MList.append(value[11])
            self.Ar40MList.append(value[14])
            self.Ar36MErrorList.append(value[3])
            self.Ar37MErrorList.append(value[6])
            self.Ar38MErrorList.append(value[9])
            self.Ar39MErrorList.append(value[12])
            self.Ar40MErrorList.append(value[15])
            self.MDateTimeList.append([int(_i) for _i in value[17:22]])
        for key, value in res[1].items():
            self.BStepsList.append(value[1])
            self.BSequenceList.append(value[2])
            self.Ar36BList.append(value[3])
            self.Ar37BList.append(value[5])
            self.Ar38BList.append(value[7])
            self.Ar39BList.append(value[9])
            self.Ar40BList.append(value[11])
            self.Ar36BErrorList.append(value[4])
            self.Ar37BErrorList.append(value[6])
            self.Ar38BErrorList.append(value[8])
            self.Ar39BErrorList.append(value[10])
            self.Ar40BErrorList.append(value[12])

    def readDataFromAgeFile(self, path=None):
        """
        Read data from filtered file.

        parameters
        ----------
        path: str
            age file path.
        """
        self.initializeData()
        if path:
            self.AgeFilePath = path
        res = open_age_xls(self.AgeFilePath)
        if res:
            self._readFilteredFile(res)
            self.IrradiationDurationList = res[3]
            self.IrradiationEndTimeList = res[4]
            book_contents = res[2]
            # read data
            data_tables_value = book_contents['Data Tables']
            # read and rewrite calculation params
            logs01_params = book_contents['Logs01']
            # read and rewrite irradiation params
            self.JValue = float(data_tables_value[51][5])
            self.JValueError = float(data_tables_value[52][5])
            self.MDF = float(data_tables_value[53][5])
            self.MDFError = float(data_tables_value[54][5])
            self.Ar40vsAr36Trapped = float(data_tables_value[71][5])
            self.Ar40vsAr36TrappedError = float(data_tables_value[72][5])
            self.Ar40vsAr36Cosmo = float(data_tables_value[73][5])
            self.Ar40vsAr36CosmoError = float(data_tables_value[74][5])
            self.Ar38vsAr36Trapped = float(data_tables_value[75][5])
            self.Ar38vsAr36TrappedError = float(data_tables_value[76][5])
            self.Ar38vsAr36Cosmo = float(data_tables_value[77][5])
            self.Ar38vsAr36CosmoError = float(data_tables_value[78][5])
            self.Ar39vsAr37Ca = float(data_tables_value[79][5])
            self.Ar39vsAr37CaError = float(data_tables_value[80][5])
            self.Ar38vsAr37Ca = float(data_tables_value[81][5])
            self.Ar38vsAr37CaError = float(data_tables_value[82][5])
            self.Ar36vsAr37Ca = float(data_tables_value[83][5])
            self.Ar36vsAr37CaError = float(data_tables_value[84][5])
            self.Ar40vsAr39K = float(data_tables_value[85][5])
            self.Ar40vsAr39KError = float(data_tables_value[86][5])
            self.Ar38vsAr39K = float(data_tables_value[87][5])
            self.Ar38vsAr39KError = float(data_tables_value[88][5])
            self.Ar36vsAr38Cl = float(data_tables_value[89][5])
            self.Ar36vsAr38ClError = float(data_tables_value[90][5])
            self.KvsCaFactor = float(data_tables_value[91][5])
            self.KvsCaFactorError = float(data_tables_value[92][5])
            self.KvsClFactor = float(data_tables_value[93][5])
            self.KvsClFactorError = float(data_tables_value[95][5])
            self.CavsClFactor = float(data_tables_value[95][5])
            self.CavsClFactorError = float(data_tables_value[96][5])

            # read and rewrite calculation params
            self.York2FitConvergence = float(logs01_params[1][0])
            self.York2FitIteration = int(logs01_params[1][1])
            self.Corr37ArDecay = int(logs01_params[1][6])
            self.Corr39ArDecay = int(logs01_params[1][7])
            self.Corr36ClDecay = int(logs01_params[1][8])
            self.Fitting = 'York-2'
            self.K40Mass = float(logs01_params[1][11])
            self.Ar40MassError = float(logs01_params[1][12])
            self.K40vsKFractions = float(logs01_params[1][14])
            self.K40vsKFractionsError = float(logs01_params[1][15])
            self.Cl35vsCl37Fractions = float(logs01_params[1][16])
            self.Cl35vsCl37FractionsError = float(logs01_params[1][17])
            self.Cl36vs38Activity = float(logs01_params[1][18])
            self.Cl36vs38ActivityError = float(logs01_params[1][19])
            self.HClvsClFractions = float(logs01_params[1][24])
            self.HClvsClFractionsError = float(logs01_params[1][25])
            self.K40ECActivity = float(logs01_params[1][26])
            self.K40ECActivityError = float(logs01_params[1][27])
            self.K40BetaNActivity = float(logs01_params[1][28])
            self.K40BetaNActivityError = float(logs01_params[1][29])
            self.K40ECConst = float(logs01_params[1][30])
            self.K40ECConstError = float(logs01_params[1][31])
            self.K40BetaNConst = float(logs01_params[1][32])
            self.K40BetaNConstError = float(logs01_params[1][33])
            self.Cl36Const = float(logs01_params[1][34])
            self.Cl36ConstError = float(logs01_params[1][35])
            self.K40Const = float(logs01_params[1][36])
            self.K40ConstError = float(logs01_params[1][37])
            self.Ar39Const = float(logs01_params[1][38])
            self.Ar39ConstError = float(logs01_params[1][39])
            self.Ar37Const = float(logs01_params[1][40])
            self.Ar37ConstError = float(logs01_params[1][41])
            self.Ar40vsAr36AirConst = float(logs01_params[1][70])
            self.Ar40vsAr36AirConstError = float(logs01_params[1][71])

            self.LinMassDiscrLaw = 1 if logs01_params[1][67] == 'LIN' else 0
            self.ExpMassDiscrLaw = 1 if logs01_params[1][67] == 'EXP' else 0
            self.PowMassDiscrLaw = 1 if logs01_params[1][67] == 'POW' else 0
            self.UseMinCalculation = 1 if logs01_params[1][5] == 'Min' else 0
            self.CorrBlank = 1

    def save(self):
        """
        Save the instance.

        Notes
        -----
        ab: adding to the last of the file if the filename has existed.
        wb: replacing of the present file.
        SampleID is unique for every instance.
        """
        _path = 'save\\{}.sp'.format(str(self.SampleName))
        with open(_path, 'ab') as f:
            f.write(pickle.dumps(self))

    def initializeData(self):
        """
        Initialize the data list
        """
        _dataList = [self.MSequenceList, self.BSequenceList, self.MStepsList, self.BStepsList,
                     self.Ar36MList, self.Ar37MList, self.Ar38MList, self.Ar39MList, self.Ar40MList,
                     self.Ar36MErrorList, self.Ar37MErrorList, self.Ar38MErrorList, self.Ar39MErrorList,
                     self.Ar40MErrorList,
                     self.Ar36BList, self.Ar37BList, self.Ar38BList, self.Ar39BList, self.Ar40BList,
                     self.Ar36BErrorList, self.Ar37BErrorList, self.Ar38BErrorList, self.Ar39BErrorList,
                     self.Ar40BErrorList,
                     self.Ar36DegassCa, self.Ar36DegassK, self.Ar36DegassCl, self.Ar36DegassAir,
                     self.Ar37DegassCa, self.Ar37DegassK, self.Ar37DegassCl, self.Ar37DegassAir,
                     self.Ar38DegassCa, self.Ar38DegassK, self.Ar38DegassCl, self.Ar38DegassAir,
                     self.Ar39DegassCa, self.Ar39DegassK, self.Ar39DegassCl, self.Ar39DegassAir,
                     self.Ar40DegassCa, self.Ar40DegassK, self.Ar40DegassCl, self.Ar40DegassAir,
                     self.Ar40DegassR,
                     self.Ar36DegassCaError, self.Ar36DegassKError, self.Ar36DegassClError, self.Ar36DegassAirError,
                     self.Ar37DegassCaError, self.Ar37DegassKError, self.Ar37DegassClError, self.Ar37DegassAirError,
                     self.Ar38DegassCaError, self.Ar38DegassKError, self.Ar38DegassClError, self.Ar38DegassAirError,
                     self.Ar39DegassCaError, self.Ar39DegassKError, self.Ar39DegassClError, self.Ar39DegassAirError,
                     self.Ar40DegassCaError, self.Ar40DegassKError, self.Ar40DegassClError, self.Ar40DegassAirError,
                     self.Ar40DegassRError]
        for each_list in _dataList:
            each_list.clear()
