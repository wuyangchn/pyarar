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
        Create a sample parent instance.

        parameters
        ----------
        SampleID: int, default: None
            unique number of every instance, it is defined based on the datetime the instance was created.

        SampleName: str, default: None
            sample name.

        SampleType: str, default: None
            sample type.
            -Unknown sample
            -Air
            -Flux monitor / Standard sample

        SampleDescription: str, default: None
            the description of sample

        ExperimentName: str, default: None
            experiment name

        ExperimentAnalyst: str, default: None
            experiment analyst

        LaboratoryName: str, default: None
            laboratory name

        LaboratoryInfo: str, default: None
            laboratory information
        """
        self.SampleID: int = int((datetime.datetime.now() - datetime.datetime(2000, 1, 1)).total_seconds() * 100)
        self.SampleName: str = kwargs.pop("SampleName", "")
        self.SampleType: str = kwargs.pop("SampleType", "")
        self.SampleDescription: str = kwargs.pop("SampleDescription", "")
        self.ExperimentName: str = kwargs.pop("ExperimentName", "")
        self.ExperimentAnalyst: str = kwargs.pop("ExperimentAnalyst", "")
        self.LaboratoryName: str = kwargs.pop("LaboratoryName", "")
        self.LaboratoryInfo: str = kwargs.pop("LaboratoryInfo", "")

        """isotopes value"""
        """sequences, steps and experimental date times"""
        self.MSequenceList: list = kwargs.pop("MSequenceList", [])
        self.BSequenceList: list = kwargs.pop("BSequenceList", [])
        self.MStepsList: list = kwargs.pop("MStepsList", [])
        self.BStepsList: list = kwargs.pop("BStepsList", [])
        self.MDateTimeList: list = kwargs.pop("MDateTimeList", [])  # [day, mouth, year, hour, min]
        """sample value"""
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
        """blank value"""
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
        """temporary list used to save correction values"""
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

    def save(self):
        """
        Save the instance.

        Notes
        -----
        ab: adding to the last of the file if the filename has existed.
        wb: replacing of the present file.
        SampleID is unique for every instance.
        """
        if not os.path.exists(os.getcwd() + '\\save'):
            os.mkdir(os.getcwd() + '\\save')
        _path = 'save\\{}.sp'.format(str(self.SampleName))
        _n = 0
        while os.path.exists(_path):
            '''rename if current sample name have already existed'''
            '''whereas if the file actually have same ID with present instance, rename is prohibited'''
            with open(_path, 'rb') as f:
                res = pickle.load(f)
            if res.SampleID == self.SampleID:
                break
            else:
                _n = _n + 1
                _path = 'save\\{}.{}.sp'.format(str(self.SampleName), _n)
                # print('auto rename')
        with open(_path, 'wb') as f:
            f.write(pickle.dumps(self))

class UnkSample(Sample):
    def __init__(self, **kwargs):
        """
        Create a sample instance.

        parameters
        ----------
        Calculation Params: float or bool, default: constants
            user define or inherit from the default.

        Attached files: str
            the file path user input.
        """
        super().__init__(SampleType=kwargs.pop("SampleType", "UnkSample"),
                         **kwargs)

        self.SampleOwner: str = kwargs.pop("SampleOwner", "")
        self.SampleMineral: str = kwargs.pop("SampleMineral", "")
        self.SampleEstimatedAge: str = kwargs.pop("SampleEstimatedAge", "")
        self.SampleLocation: str = kwargs.pop("SampleLocation", "")

        """isotopes degas value"""
        self.Ar36DegasCa: list = kwargs.pop("Ar36DegasCa", [])
        self.Ar36DegasK: list = kwargs.pop("Ar36DegasK", [])
        self.Ar36DegasCl: list = kwargs.pop("Ar36DegasCl", [])
        self.Ar36DegasAir: list = kwargs.pop("Ar36DegasAir", [])
        self.Ar37DegasCa: list = kwargs.pop("Ar37DegasCa", [])
        self.Ar37DegasK: list = kwargs.pop("Ar37DegasK", [])
        self.Ar37DegasCl: list = kwargs.pop("Ar37DegasCl", [])
        self.Ar37DegasAir: list = kwargs.pop("Ar37DegasAir", [])
        self.Ar38DegasCa: list = kwargs.pop("Ar38DegasCa", [])
        self.Ar38DegasK: list = kwargs.pop("Ar38DegasK", [])
        self.Ar38DegasCl: list = kwargs.pop("Ar38DegasCl", [])
        self.Ar38DegasAir: list = kwargs.pop("Ar38DegasAir", [])
        self.Ar39DegasCa: list = kwargs.pop("Ar39DegasCa", [])
        self.Ar39DegasK: list = kwargs.pop("Ar39DegasK", [])
        self.Ar39DegasCl: list = kwargs.pop("Ar39DegasCl", [])
        self.Ar39DegasAir: list = kwargs.pop("Ar39DegasAir", [])
        self.Ar40DegasCa: list = kwargs.pop("Ar40DegasCa", [])
        self.Ar40DegasK: list = kwargs.pop("Ar40DegasK", [])
        self.Ar40DegasCl: list = kwargs.pop("Ar40DegasCl", [])
        self.Ar40DegasAir: list = kwargs.pop("Ar40DegasAir", [])
        self.Ar40DegasR: list = kwargs.pop("Ar40DegasR", [])

        self.FValues: list = kwargs.pop("FValues", [])
        self.FValuesError: list = kwargs.pop("FValuesError", [])
        self.ApparentAge: list = kwargs.pop("ApparentAge", [])
        self.ApparentAgeAnalysisError: list = kwargs.pop("ApparentAgeAnalysisError", [])
        self.ApparentAgeInternalError: list = kwargs.pop("ApparentAgeInternalError", [])
        self.ApparentAgeFullExternalError: list = kwargs.pop("ApparentAgeFullExternalError", [])
        self.KCaRatios: list = kwargs.pop("KCaRatios", [])
        self.KCaRatiosError: list = kwargs.pop("KCaRatiosError", [])
        self.KClRatios: list = kwargs.pop("KClRatios", [])
        self.KClRatiosError: list = kwargs.pop("KClRatiosError", [])
        self.CaClRatios: list = kwargs.pop("CaClRatios", [])
        self.CaClRatiosError: list = kwargs.pop("CaClRatiosError", [])

        self.ClNormalIsochron: list = kwargs.pop("ClNormalIsochron", [])
        self.ClInverseIsochron: list = kwargs.pop("ClInverseIsochron", [])
        self.ClKIsochron: list = kwargs.pop("ClKIsochron", [])
        self.AtmNormalIsochron: list = kwargs.pop("AtmNormalIsochron", [])
        self.AtmInverseIsochron: list = kwargs.pop("AtmInverseIsochron", [])
        self.ThreeDimIsochron: list = kwargs.pop("ThreeDimIsochron", [])
        self.IsochronSelectedPoints: list = kwargs.pop("IsochronSelectedPoints", [])
        self.PlateauAges: list = kwargs.pop("PlateauAges", [])
        self.TotalFusionAge: list = kwargs.pop("TotalFusionAge", [])
        self.SpectraLines: list = kwargs.pop("SpectraLines", [])

        self.Ar36DegasCaError: list = kwargs.pop("Ar36DegasCaError", [])
        self.Ar36DegasKError: list = kwargs.pop("Ar36DegasKError", [])
        self.Ar36DegasClError: list = kwargs.pop("Ar36DegasClError", [])
        self.Ar36DegasAirError: list = kwargs.pop("Ar36DegasAirError", [])
        self.Ar37DegasCaError: list = kwargs.pop("Ar37DegasCaError", [])
        self.Ar37DegasKError: list = kwargs.pop("Ar37DegasKError", [])
        self.Ar37DegasClError: list = kwargs.pop("Ar37DegasClError", [])
        self.Ar37DegasAirError: list = kwargs.pop("Ar37DegasAirError", [])
        self.Ar38DegasCaError: list = kwargs.pop("Ar38DegasCaError", [])
        self.Ar38DegasKError: list = kwargs.pop("Ar38DegasKError", [])
        self.Ar38DegasClError: list = kwargs.pop("Ar38DegasClError", [])
        self.Ar38DegasAirError: list = kwargs.pop("Ar38DegasAirError", [])
        self.Ar39DegasCaError: list = kwargs.pop("Ar39DegasCaError", [])
        self.Ar39DegasKError: list = kwargs.pop("Ar39DegasKError", [])
        self.Ar39DegasClError: list = kwargs.pop("Ar39DegasClError", [])
        self.Ar39DegasAirError: list = kwargs.pop("Ar39DegasAirError", [])
        self.Ar40DegasCaError: list = kwargs.pop("Ar40DegasCaError", [])
        self.Ar40DegasKError: list = kwargs.pop("Ar40DegasKError", [])
        self.Ar40DegasClError: list = kwargs.pop("Ar40DegasClError", [])
        self.Ar40DegasAirError: list = kwargs.pop("Ar40DegasAirError", [])
        self.Ar40DegasRError: list = kwargs.pop("Ar40DegasRError", [])

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

        self.K40Const: float = kwargs.pop("K40Const", K40Const)  # unit: /a
        self.K40ConstError: float = kwargs.pop("K40ConstError", K40ConstError)
        self.K40ECConstError: float = kwargs.pop("K40ECConstError", K40ECConstError)
        self.K40ECConst: float = kwargs.pop("K40ECConst", K40ECConst)
        self.K40BetaNConst: float = kwargs.pop("K40BetaNConst", K40BetaNConst)
        self.K40BetaNConstError: float = kwargs.pop("K40BetaNConstError", K40BetaNConstError)
        self.K40BetaPConst: float = kwargs.pop("K40BetaPConst", K40BetaPConst)
        self.K40BetaPConstError: float = kwargs.pop("K40BetaPConstError", K40BetaPConstError)
        self.Ar39Const: float = kwargs.pop("Ar39Const", Ar39Const)  # unit: /h
        self.Ar39ConstError: float = kwargs.pop("Ar39ConstError", Ar39ConstError)
        self.Ar37Const: float = kwargs.pop("Ar37Const", Ar37Const)  # unit: /h
        self.Ar37ConstError: float = kwargs.pop("Ar37ConstError", Ar37ConstError)
        self.Cl36Const: float = kwargs.pop("Cl36Const", Cl36Const)  # unit: /a
        self.Cl36ConstError: float = kwargs.pop("Cl36ConstError", Cl36ConstError)
        self.K40ECActivity: float = kwargs.pop("K40ECActivity", K40ECActivity)
        self.K40ECActivityError: float = kwargs.pop("K40ECActivityError", K40ECActivityError)
        self.K40BetaNActivity: float = kwargs.pop("K40BetaNActivity", K40BetaNActivity)
        self.K40BetaNActivityError: float = kwargs.pop("K40BetaNActivityError", K40BetaNActivityError)
        self.K40BetaPActivity: float = kwargs.pop("K40BetaPActivity", K40BetaPActivity)
        self.K40BetaPActivityError: float = kwargs.pop("K40BetaPActivityError", K40BetaPActivityError)
        self.K40Activity: float = kwargs.pop("K40Activity", K40Activity)
        self.K40ActivityError: float = kwargs.pop("K40ActivityError", K40ActivityError)
        self.Cl36vs38Productivity: float = kwargs.pop("Cl36vs38Productivity", Cl36vs38Productivity)
        self.Cl36vs38ProductivityError: float = kwargs.pop("Cl36vs38ProductivityError", Cl36vs38ProductivityError)
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
        self.CorrCl: bool = kwargs.pop("CorrCl", CorrCl)
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

        self.StandardAge: float = kwargs.pop("StandardAge", StandardAge)
        self.StandardAgeError: float = kwargs.pop("StandardAgeError", StandardAgeError)
        self.Ar40Concentration: float = kwargs.pop("Ar40Concentration", Ar40Concentration)
        self.Ar40ConcentrationError: float = kwargs.pop("Ar40ConcentrationError", Ar40ConcentrationError)
        self.KConcentration: float = kwargs.pop("KConcentration", KConcentration)
        self.KConcentrationError: float = kwargs.pop("KConcentrationError", KConcentrationError)
        self.StandardAr40vsK: float = kwargs.pop("StandardAr40vsK", StandardAr40vsK)
        self.StandardAr40vsKError: float = kwargs.pop("StandardAr40vsKError", StandardAr40vsKError)

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
            self.StandardAge = float(data_tables_value[49][5])
            self.StandardAgeError = float(data_tables_value[50][5]) / 100 * float(data_tables_value[49][5])
            self.JValue = float(data_tables_value[51][5])
            self.JValueError = float(data_tables_value[52][5]) / 100 * float(data_tables_value[51][5])
            self.MDF = float(data_tables_value[53][5])
            self.MDFError = float(data_tables_value[54][5]) / 100 * float(data_tables_value[53][5])
            self.Ar40vsAr36Trapped = float(data_tables_value[71][5])
            self.Ar40vsAr36TrappedError = float(data_tables_value[72][5]) / 100 * float(data_tables_value[71][5])
            self.Ar40vsAr36Cosmo = float(data_tables_value[73][5])
            self.Ar40vsAr36CosmoError = float(data_tables_value[74][5]) / 100 * float(data_tables_value[73][5])
            self.Ar38vsAr36Trapped = float(data_tables_value[75][5])
            self.Ar38vsAr36TrappedError = float(data_tables_value[76][5]) / 100 * float(data_tables_value[75][5])
            self.Ar38vsAr36Cosmo = float(data_tables_value[77][5])
            self.Ar38vsAr36CosmoError = float(data_tables_value[78][5]) / 100 * float(data_tables_value[77][5])
            self.Ar39vsAr37Ca = float(data_tables_value[79][5])
            self.Ar39vsAr37CaError = float(data_tables_value[80][5]) / 100 * float(data_tables_value[79][5])
            self.Ar38vsAr37Ca = float(data_tables_value[81][5])
            self.Ar38vsAr37CaError = float(data_tables_value[82][5]) / 100 * float(data_tables_value[81][5])
            self.Ar36vsAr37Ca = float(data_tables_value[83][5])
            self.Ar36vsAr37CaError = float(data_tables_value[84][5]) / 100 * float(data_tables_value[83][5])
            self.Ar40vsAr39K = float(data_tables_value[85][5])
            self.Ar40vsAr39KError = float(data_tables_value[86][5]) / 100 * float(data_tables_value[85][5])
            self.Ar38vsAr39K = float(data_tables_value[87][5])
            self.Ar38vsAr39KError = float(data_tables_value[88][5]) / 100 * float(data_tables_value[87][5])
            self.Ar36vsAr38Cl = float(data_tables_value[89][5])
            self.Ar36vsAr38ClError = float(data_tables_value[90][5]) / 100 * float(data_tables_value[89][5])
            self.KvsCaFactor = float(data_tables_value[91][5])
            self.KvsCaFactorError = float(data_tables_value[92][5]) / 100 * float(data_tables_value[91][5])
            self.KvsClFactor = float(data_tables_value[93][5])
            self.KvsClFactorError = float(data_tables_value[94][5]) / 100 * float(data_tables_value[93][5])
            self.CavsClFactor = float(data_tables_value[95][5])
            self.CavsClFactorError = float(data_tables_value[96][5]) / 100 * float(data_tables_value[95][5])

            # read and rewrite calculation params
            self.York2FitConvergence = float(logs01_params[1][0]) / 100
            self.York2FitIteration = int(logs01_params[1][1])
            self.Corr37ArDecay = int(logs01_params[1][6])
            self.Corr39ArDecay = int(logs01_params[1][7])
            self.Corr36ClDecay = int(logs01_params[1][8])
            self.Fitting = 'York-2'
            self.K40Mass = float(logs01_params[1][11])
            self.Ar40MassError = float(logs01_params[1][12]) / 100 * float(logs01_params[1][11])
            self.K40vsKFractions = float(logs01_params[1][14])
            self.K40vsKFractionsError = float(logs01_params[1][15]) / 100 * float(logs01_params[1][14])
            self.Cl35vsCl37Fractions = float(logs01_params[1][16])
            self.Cl35vsCl37FractionsError = float(logs01_params[1][17]) / 100 * float(logs01_params[1][16])
            self.Cl36vs38Productivity = float(logs01_params[1][18])
            self.Cl36vs38ProductivityError = float(logs01_params[1][19]) / 100 * float(logs01_params[1][18])
            self.HClvsClFractions = float(logs01_params[1][24])
            self.HClvsClFractionsError = float(logs01_params[1][25]) / 100 * float(logs01_params[1][24])
            self.K40ECActivity = float(logs01_params[1][26])
            self.K40ECActivityError = float(logs01_params[1][27]) / 100 * float(logs01_params[1][26])
            self.K40BetaNActivity = float(logs01_params[1][28])
            self.K40BetaNActivityError = float(logs01_params[1][29]) / 100 * float(logs01_params[1][28])
            self.K40ECConst = float(logs01_params[1][30])
            self.K40ECConstError = float(logs01_params[1][31]) / 100 * float(logs01_params[1][30])
            self.K40BetaNConst = float(logs01_params[1][32])
            self.K40BetaNConstError = float(logs01_params[1][33]) / 100 * float(logs01_params[1][32])
            self.Cl36Const = float(logs01_params[1][34])
            self.Cl36ConstError = float(logs01_params[1][35]) / 100 * float(logs01_params[1][34])
            self.K40Const = float(logs01_params[1][36])
            self.K40ConstError = float(logs01_params[1][37]) / 100 * float(logs01_params[1][36])
            self.Ar39Const = float(logs01_params[1][38])
            self.Ar39ConstError = float(logs01_params[1][39]) / 100 * float(logs01_params[1][38])
            self.Ar37Const = float(logs01_params[1][40])
            self.Ar37ConstError = float(logs01_params[1][41]) / 100 * float(logs01_params[1][40])
            self.Ar40vsAr36AirConst = float(logs01_params[1][70])
            self.Ar40vsAr36AirConstError = float(logs01_params[1][71]) / 100 * float(logs01_params[1][70])

            self.LinMassDiscrLaw = 1 if logs01_params[1][67] == 'LIN' else 0
            self.ExpMassDiscrLaw = 1 if logs01_params[1][67] == 'EXP' else 0
            self.PowMassDiscrLaw = 1 if logs01_params[1][67] == 'POW' else 0
            self.UseMinCalculation = 1 if logs01_params[1][5] == 'MIN' else 0
            self.CorrBlank = 1

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
                     self.Ar36DegasCa, self.Ar36DegasK, self.Ar36DegasCl, self.Ar36DegasAir,
                     self.Ar37DegasCa, self.Ar37DegasK, self.Ar37DegasCl, self.Ar37DegasAir,
                     self.Ar38DegasCa, self.Ar38DegasK, self.Ar38DegasCl, self.Ar38DegasAir,
                     self.Ar39DegasCa, self.Ar39DegasK, self.Ar39DegasCl, self.Ar39DegasAir,
                     self.Ar40DegasCa, self.Ar40DegasK, self.Ar40DegasCl, self.Ar40DegasAir,
                     self.Ar40DegasR,
                     self.Ar36DegasCaError, self.Ar36DegasKError, self.Ar36DegasClError, self.Ar36DegasAirError,
                     self.Ar37DegasCaError, self.Ar37DegasKError, self.Ar37DegasClError, self.Ar37DegasAirError,
                     self.Ar38DegasCaError, self.Ar38DegasKError, self.Ar38DegasClError, self.Ar38DegasAirError,
                     self.Ar39DegasCaError, self.Ar39DegasKError, self.Ar39DegasClError, self.Ar39DegasAirError,
                     self.Ar40DegasCaError, self.Ar40DegasKError, self.Ar40DegasClError, self.Ar40DegasAirError,
                     self.Ar40DegasRError]
        for each_list in _dataList:
            each_list.clear()
