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

        self.MSequenceList: list = kwargs.pop("MSequenceList", [])
        self.BSequenceList: list = kwargs.pop("BSequenceList", [])
        self.MStepsList: list = kwargs.pop("MStepsList", [])
        self.BStepsList: list = kwargs.pop("BStepsList", [])

        self.Ar36MList: list = kwargs.pop("Ar36MList", [])
        self.Ar37MList: list = kwargs.pop("Ar37MList", [])
        self.Ar38MList: list = kwargs.pop("Ar38MList", [])
        self.Ar39MList: list = kwargs.pop("Ar39MList", [])
        self.Ar40MList: list = kwargs.pop("Ar40MList", [])

        self.Ar36BList: list = kwargs.pop("Ar36BList", [])
        self.Ar37BList: list = kwargs.pop("Ar37BList", [])
        self.Ar38BList: list = kwargs.pop("Ar38BList", [])
        self.Ar39BList: list = kwargs.pop("Ar39BList", [])
        self.Ar40BList: list = kwargs.pop("Ar40BList", [])

        self._dataList = [self.MSequenceList, self.BSequenceList, self.MStepsList, self.BStepsList,
                          self.Ar36MList, self.Ar37MList, self.Ar38MList, self.Ar39MList, self.Ar40MList,
                          self.Ar36BList, self.Ar37BList, self.Ar38BList, self.Ar39BList, self.Ar40BList]

        self.RawFilePath: str = kwargs.pop("RawFilePath", "")
        self.FilteredFilePath: str = kwargs.pop("FilteredFilePath", "")
        self.AgeFilePath: str = kwargs.pop("FilteredFilePath", "")

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
            self.Ar36MList = res[2]

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
            for key, value in res[0].items():
                self.MSequenceList.append(value[0])
                self.MStepsList.append(value[1])
                self.Ar36MList.append(value[2])
                self.Ar37MList.append(value[5])
                self.Ar38MList.append(value[8])
                self.Ar39MList.append(value[11])
                self.Ar40MList.append(value[14])
            for key, value in res[1].items():
                self.BStepsList.append(value[1])
                self.BSequenceList.append(value[2])
                self.Ar36BList.append(value[3])
                self.Ar37BList.append(value[5])
                self.Ar38BList.append(value[7])
                self.Ar39BList.append(value[9])
                self.Ar40BList.append(value[11])

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
            for key, value in res[0].items():
                self.MSequenceList.append(value[0])
                self.MStepsList.append(value[1])
                self.Ar36MList.append(value[2])
                self.Ar37MList.append(value[5])
                self.Ar38MList.append(value[8])
                self.Ar39MList.append(value[11])
                self.Ar40MList.append(value[14])
            for key, value in res[1].items():
                self.BStepsList.append(value[1])
                self.BSequenceList.append(value[2])
                self.Ar36BList.append(value[3])
                self.Ar37BList.append(value[5])
                self.Ar38BList.append(value[7])
                self.Ar39BList.append(value[9])
                self.Ar40BList.append(value[11])
            book_contents = res[2]
            # read data
            data_tables_value = book_contents['Data Tables']
            # read and rewrite calculation params
            logs01_params = book_contents['Logs01']
            # read and rewrite irradiation params
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

            irradiation_index = book_contents['Logs02'][1].index(data_tables_value[63][5])
            irradiation_info_list = book_contents['Logs02'][32][irradiation_index].split('\n')
            print('irradiation_date_list>>>%s' % irradiation_info_list)
            month_convert = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6, 'JUL': 7, 'AUG': 8, 'SEP': 9,
                             'OCT': 10, 'NOV': 11, 'DEC': 12, 'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5,
                             'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
            duration_hour = []
            standing_second = []
            for each_date in irradiation_info_list:
                if '/' in each_date:
                    year = each_date.split(' ')[1].split('/')[2]
                    month = each_date.split(' ')[1].split('/')[1]
                    if month in month_convert.keys():
                        month = month_convert[month]
                    day = each_date.split(' ')[1].split('/')[0]
                    hour = each_date.split(' ')[2].split('.')[0]
                    min = each_date.split(' ')[2].split('.')[1]
                    standing_second.append(get_datatime(t_year=int(year), t_month=int(month), t_day=int(day),
                                                        t_hour=int(hour), t_min=int(min)))
                    each_duration_hour = each_date.split(' ')[0].split('.')[0]
                    each_duration_min = each_date.split(' ')[0].split('.')[1]
                    duration_hour.append(int(each_duration_hour) + int(each_duration_min) / 60)
            self.IrradiationDurationList = duration_hour
            self.IrradiationTimeList = standing_second

            # read and rewrite calculation params
            self.K40Const = float(logs01_params[1][36])
            calc_param['40KConstError'] = float(logs01_params[1][37])
            calc_param['40K(EC)Const'] = float(logs01_params[1][30])
            calc_param['40K(EC)ConstError'] = float(logs01_params[1][31])
            calc_param['40K(β-)Const'] = float(logs01_params[1][32])
            calc_param['40K(β-)ConstError'] = float(logs01_params[1][33])
            calc_param['39ArConst'] = float(logs01_params[1][38])
            calc_param['39ArConstError'] = float(logs01_params[1][39])
            calc_param['37ArConst'] = float(logs01_params[1][40])
            calc_param['37ArConstError'] = float(logs01_params[1][41])
            calc_param['36ClConst'] = float(logs01_params[1][34])
            calc_param['36ClConstError'] = float(logs01_params[1][35])
            calc_param['40K(EC)Activity'] = float(logs01_params[1][26])
            calc_param['40K(EC)ActivityError'] = float(logs01_params[1][27])
            calc_param['40K(β-)Activity'] = float(logs01_params[1][28])
            calc_param['40K(β-)ActivityError'] = float(logs01_params[1][29])
            calc_param['36/38Cl(p)Activity'] = float(logs01_params[1][18])
            calc_param['36/38Cl(p)ActivityError'] = float(logs01_params[1][19])
            calc_param['KmassConst'] = float(logs01_params[1][11])
            calc_param['KmassConstError'] = float(logs01_params[1][12])
            calc_param['40K/KConst'] = float(logs01_params[1][14])
            calc_param['40K/KConstError'] = float(logs01_params[1][15])
            calc_param['35Cl/37ClConst'] = float(logs01_params[1][16])
            calc_param['35Cl/37ClConstError'] = float(logs01_params[1][17])
            calc_param['HCl/ClConst'] = float(logs01_params[1][24])
            calc_param['HCl/ClConstError'] = float(logs01_params[1][25])
            calc_param['40/36(air)Const'] = float(logs01_params[1][70])
            calc_param['40/36(air)ConstError'] = float(logs01_params[1][71])
            calc_param['Corr37ArDecay'] = int(logs01_params[1][6])
            calc_param['Corr39ArDecay'] = int(logs01_params[1][7])
            calc_param['Convergence'] = float(logs01_params[1][0])
            calc_param['Iteration'] = int(logs01_params[1][1])
            calc_param['Fitting'] = 'York-2'

            calc_param['LinMassDiscrLaw'] = 1 if logs01_params[1][67] == 'LIN' else 0
            calc_param['ExpMassDiscrLaw'] = 1 if logs01_params[1][67] == 'EXP' else 0
            calc_param['PowMassDiscrLaw'] = 1 if logs01_params[1][67] == 'POW' else 0
            calc_param['CorrBlank'] = 1

            calc_param['J_value'] = float(data_tables_value[51][5])
            calc_param['J_error'] = float(data_tables_value[52][5])
            calc_param['MDF'] = float(data_tables_value[53][5])
            calc_param['sMDF'] = float(data_tables_value[54][5])


    def save(self):
        """
        Save the instance.

        Notes
        -----
        ab: adding to the last of the file if the filename has existed.
        wb: replacing of the present file.
        SampleID is unique for every instance.
        """
        with open('save\\' + str(self.SampleName) + '.sp', 'ab') as f:
            f.write(pickle.dumps(self))

    def initializeData(self):
        """
        Initialize the data list
        """
        for _i in self._dataList:
            _i = []
