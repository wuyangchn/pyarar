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
        Create a sample instance

            SampleID:
                unique number of every instance, it is defined based on the datetime the instance was created

            Other sample information:
                user input

            Calculation Params:
                user define or inherit from the default

            Attached files:
                the file path user input

        :param kwargs:
        """
        self.SampleID: int = int((datetime.datetime.now() - datetime.datetime(2000, 1, 1)).total_seconds() * 100)
        self.SampleName: str = kwargs.pop("SampleName", None)
        self.SampleOwner: str = kwargs.pop("SampleOwner", None)
        self.SampleType: str = kwargs.pop("SampleType", None)
        self.SampleMineral: str = kwargs.pop("SampleMineral", None)
        self.SampleEstimatedAge: str = kwargs.pop("SampleEstimatedAge", None)
        self.SampleDescription: str = kwargs.pop("SampleDescription", None)
        self.SampleLocation: str = kwargs.pop("SampleLocation", None)
        self.ExperimentName: str = kwargs.pop("ExperimentName", None)
        self.ExperimentAnalyst: str = kwargs.pop("ExperimentAnalyst", None)

        self.Ar36MList: list = kwargs.pop("Ar36MList", None)
        self.Ar37MList: list = kwargs.pop("Ar37MList", None)
        self.Ar38MList: list = kwargs.pop("Ar38MList", None)
        self.Ar39MList: list = kwargs.pop("Ar39MList", None)
        self.Ar40MList: list = kwargs.pop("Ar40MList", None)

        self.Ar36BList: list = kwargs.pop("Ar36BList", None)
        self.Ar37BList: list = kwargs.pop("Ar37BList", None)
        self.Ar38BList: list = kwargs.pop("Ar38BList", None)
        self.Ar39BList: list = kwargs.pop("Ar39BList", None)
        self.Ar40BList: list = kwargs.pop("Ar40BList", None)

        self.K40vsKFractions: float = kwargs.pop("K40vsKFractions", K40vsKFractions)
        self.K40vsKFractionsError: float = kwargs.pop("K40vsKFractionsError", K40vsKFractionsError)
        self.Cl35vsClFractions: float = kwargs.pop("Cl35vsClFractions", Cl35vsClFractions)
        self.Cl35vsClFractionsError: float = kwargs.pop("Cl35vsClFractionsError", Cl35vsClFractionsError)
        self.HClvsClFractions: float = kwargs.pop("HClvsClFractions", HClvsClFractions)
        self.HClvsClFractionsError: float = kwargs.pop("HClvsClFractionsError", HClvsClFractionsError)
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
        self.CorrBlank: bool = kwargs.pop("CorrBlank", CorrBlank)
        self.CorrDiscr: bool = kwargs.pop("CorrDiscr", CorrDiscr)
        self.Corr37ArDecay: bool = kwargs.pop("Corr37ArDecay", Corr37ArDecay)
        self.Corr39ArDecay: bool = kwargs.pop("Corr39ArDecay", Corr39ArDecay)
        self.CorrK: bool = kwargs.pop("CorrK", CorrK)
        self.CorrCa: bool = kwargs.pop("CorrCa", CorrCa)
        self.CorrAtm: bool = kwargs.pop("CorrAtm", CorrAtm)
        self.Corr36ArCl: bool = kwargs.pop("Corr36ArCl", Corr36ArCl)
        self.RelativeError: bool = kwargs.pop("RelativeError", RelativeError)
        self.UseDecayConst: bool = kwargs.pop("UseDecayConst", UseDecayConst)
        self.UseInterceptCorrAtm: bool = kwargs.pop("UseInterceptCorrAtm", UseInterceptCorrAtm)

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
        self.IrradiationTimeList: list = kwargs.pop("IrradiationTimeList", IrradiationTimeList)
        self.StandTimeList: list = kwargs.pop("StandTimeList", StandTimeList)

        self.RawFilePath: str = kwargs.pop("RawFilePath", None)
        self.FilteredFilePath: str = kwargs.pop("FilteredFilePath", None)
        self.AgeFilePath: str = kwargs.pop("FilteredFilePath", None)

    def readDataFromRawFile(self, path=None):
        if path:
            self.RawFilePath = path
        res = open_original_xls(self.RawFilePath)
        if res:
            self.Ar36MList = res[2]

    def readDataFromFilteredFile(self, path=None):
        if path:
            self.FilteredFilePath = path
        res = open_filtered_xls(self.FilteredFilePath)
        if res:
            self.Ar36MList = res[2]

    def readDataFromAgeFile(self, path=None):
        if path:
            self.AgeFilePath = path
        res = open_age_xls(self.AgeFilePath)
        if res:
            self.Ar36MList = res[2]

    def save(self):
        """
        Save the instance

            ab: adding to the last of the file if the filename has existed
            wb: replacing of the present file
            SampleID is unique for every instance

        :return:
        """
        with open('save\\' + str(self.SampleName) + '.sp', 'ab') as f:
            f.write(pickle.dumps(self))

