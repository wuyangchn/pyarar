#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : params.py
# @Author : Yang Wu
# @Date   : 2022/1/26
# @Email  : wuy@cug.edu.cn

class CalcParams:
    def __init__(self, **kwargs):
        self.K40Const: float = 0  # decay constant of K40, unit in /a
        self.K40ECConst: float = 0  # 40K --> 40Ar
        self.K40BetaNConst: float = 0  # alpha -, 40K --> 40Ca
        self.K40BetaPConst: float = 0  # alpha +
        self.Ar39Const: float = 0
        self.Ar37Const: float = 0
        self.Cl36Const: float = 0
        self.K40Activity: float = 0
        self.K40ActivityError: float = 0
        self.K40ECActivity: float = 0
        self.K40BetaNActivity: float = 0
        self.K40BetaPActivity: float = 0
        self.Cl36vs38Productivity: float = 0
        self.K40Mass: float = 0
        self.NoConst: float = 0  # avogadro number
        self.YearConst: float = 0  # seconds in a year
        self.K40vsKFractions: float = 0
        self.Cl35vsCl37Fractions: float = 0
        self.HClvsClFractions: float = 0
        self.Ar40vsAr36AirConst: float = 0

        self.K40ConstError: float = 0  # absolute error
        self.K40ECConstError: float = 0
        self.K40BetaNConstError: float = 0  # absolute error
        self.K40BetaPConstError: float = 0
        self.Ar39ConstError: float = 0
        self.Ar37ConstError: float = 0
        self.Cl36ConstError: float = 0
        self.K40ECActivityError: float = 0
        self.K40BetaNActivityError: float = 0
        self.K40BetaPActivityError: float = 0
        self.Cl36vs38ProductivityError: float = 0
        self.K40MassError: float = 0
        self.NoConstError: float = 0  # absolute error
        self.YearConstError: float = 0
        self.K40vsKFractionsError: float = 0
        self.Cl35vsCl37FractionsError: float = 0
        self.HClvsClFractionsError: float = 0
        self.Ar40vsAr36AirConstError: float = 0
        self.JValue: float = 0  # 0.015150673
        self.JValueError: float = 0  # 0.5
        self.MDF: float = 0
        self.MDFError: float = 0

        self.Ar36Mass: float = 35.96754628
        self.Ar36MassError: float = 0
        self.Ar37Mass: float = 36.9667759
        self.Ar37MassError: float = 0
        self.Ar38Mass: float = 37.9627322
        self.Ar38MassError: float = 0
        self.Ar39Mass: float = 38.964313
        self.Ar39MassError: float = 0
        self.Ar40Mass: float = 39.962383123
        self.Ar40MassError: float = 0

        self.York2FitConvergence: float = 0
        self.York2FitIteration: float = 0

        self.Ar40vsAr36Const: float = 0
        self.Ar40vsAr36ConstError: float = 0

        self.Fitting: str = "York-2"

        self.ForceNegative: bool = True  # Force negative value to zero
        self.CorrBlank: bool = True  # Correct blank
        self.CorrDiscr: bool = True  # Correct mass discrimination
        self.Corr37ArDecay: bool = True
        self.Corr39ArDecay: bool = True
        self.Corr36ClDecay: bool = True
        self.CorrK: bool = True
        self.CorrCa: bool = True
        self.CorrAtm: bool = True
        self.CorrCl: bool = True
        self.DisplayRelative: bool = True  # Display relative error
        self.UseDecayConst: bool = False
        self.UseInterceptCorrAtm: bool = False
        self.LinMassDiscrLaw: bool = True  # Mass Discrimination method: Lin
        self.ExpMassDiscrLaw: bool = False  # Mass Discrimination method: Exp
        self.PowMassDiscrLaw: bool = False  # Mass Discrimination method: Pow
        self.RecalibrationToPrimary: bool = False  # Recalibration to primary standard
        self.RecalibrationUseAge: bool = False  # Recalibration to primary standard using age
        self.RecalibrationUseRatio: bool = False  # Recalibration to primary standard using ratio

        self.StandardName: str = kwargs.pop("StandardName", "")
        self.StandardAge: float = kwargs.pop("StandardAge", 0)
        self.StandardAgeError: float = kwargs.pop("StandardAgeError", 0)

        self.PrimaryStdName: str = kwargs.pop("PrimaryStdName", "")
        self.PrimaryStdAge: float = kwargs.pop("PrimaryStdAge", 0)
        self.PrimaryStdAgeError: float = kwargs.pop("PrimaryStdAgeError", 0)
        self.PrimaryStdAr40Conc: float = kwargs.pop("PrimaryStd40ArConc", 0)
        self.PrimaryStdAr40ConcError: float = kwargs.pop("PrimaryStd40ArConcError", 0)
        self.PrimaryStdKConc: float = kwargs.pop("PrimaryStdKConc", 0)
        self.PrimaryStdKConcError: float = kwargs.pop("PrimaryStdKConcError", 0)
        self.PrimaryStdAr40vsK: float = kwargs.pop("PrimaryStdAr40vsK", 0)
        self.PrimaryStdAr40vsKError: float = kwargs.pop("PrimaryStdAr40vsKError", 0)


class IrraParams:
    def __init__(self, **kwargs):
        self.Ar40vsAr36Trapped: float = kwargs.pop("Ar40vsAr36Trapped", 0)
        self.Ar40vsAr36Cosmo: float = kwargs.pop("Ar40vsAr36Cosmo", 0)
        self.Ar38vsAr36Trapped: float = kwargs.pop("Ar38vsAr36Trapped", 0)
        self.Ar38vsAr36Cosmo: float = kwargs.pop("Ar38vsAr36Cosmo", 0)
        self.Ar39vsAr37Ca: float = kwargs.pop("Ar39vsAr37Ca", 0)
        self.Ar38vsAr37Ca: float = kwargs.pop("Ar38vsAr37Ca", 0)
        self.Ar36vsAr37Ca: float = kwargs.pop("Ar36vsAr37Ca", 0)
        self.Ar40vsAr39K: float = kwargs.pop("Ar40vsAr39K", 0)
        self.Ar38vsAr39K: float = kwargs.pop("Ar38vsAr39K", 0)
        self.Ar36vsAr38Cl: float = kwargs.pop("Ar36vsAr38Cl", 0)
        self.KvsCaFactor: float = kwargs.pop("KvsCaFactor", 0)
        self.KvsClFactor: float = kwargs.pop("KvsClFactor", 0)
        self.CavsClFactor: float = kwargs.pop("CavsClFactor", 0)
        self.CavsClFactorError: float = kwargs.pop("CavsClFactorError", 0)
        self.KvsClFactorError: float = kwargs.pop("KvsClFactorError", 0)
        self.KvsCaFactorError: float = kwargs.pop("KvsCaFactorError", 0)
        self.Ar36vsAr38ClError: float = kwargs.pop("Ar36vsAr38ClError", 0)
        self.Ar38vsAr39KError: float = kwargs.pop("Ar38vsAr39KError", 0)
        self.Ar40vsAr39KError: float = kwargs.pop("Ar40vsAr39KError", 0)
        self.Ar36vsAr37CaError: float = kwargs.pop("Ar36vsAr37CaError", 0)
        self.Ar38vsAr37CaError: float = kwargs.pop("Ar38vsAr37CaError", 0)
        self.Ar39vsAr37CaError: float = kwargs.pop("Ar39vsAr37CaError", 0)
        self.Ar38vsAr36CosmoError: float = kwargs.pop("Ar38vsAr36CosmoError", 0)
        self.Ar38vsAr36TrappedError: float = kwargs.pop("Ar38vsAr36TrappedError", 0)
        self.Ar40vsAr36CosmoError: float = kwargs.pop("Ar40vsAr36CosmoError", 0)
        self.Ar40vsAr36TrappedError: float = kwargs.pop("Ar40vsAr36TrappedError", 0)

        self.IrradiationEndTimeList: list = kwargs.pop("IrradiationEndTimeList", [0])
        self.IrradiationDurationList: list = kwargs.pop("IrradiationDurationList", [0])

        self.IrradiationName: list = kwargs.pop("IrradiationName", "")


class ParamsInfo(CalcParams, IrraParams):
    def __init__(self):
        CalcParams.__init__(self)
        IrraParams.__init__(self)
        
        self.K40Const: str = "decay constant of K40, unit in /a"
        self.K40ECConst: str = "40K --> 40Ar"
        self.K40BetaNConst: str = "alpha -, 40K --> 40Ca"
        self.K40BetaPConst: str = "alpha +"
        self.Ar39Const: str = ""
        self.Ar37Const: str = ""
        self.Cl36Const: str = ""
        self.K40Activity: str = ""
        self.K40ActivityError: str = ""
        self.K40ECActivity: str = ""
        self.K40BetaNActivity: str = ""
        self.K40BetaPActivity: str = ""
        self.Cl36vs38Productivity: str = ""
        self.K40Mass: str = ""
        self.NoConst: str = "avogadro number"
        self.YearConst: str = "seconds in a year"
        self.K40vsKFractions: str = ""
        self.Cl35vsCl37Fractions: str = ""
        self.HClvsClFractions: str = ""
        self.Ar40vsAr36AirConst: str = ""

        self.K40ConstError: str = "absolute error"
        self.K40ECConstError: str = ""
        self.K40BetaNConstError: str = "absolute error"
        self.K40BetaPConstError: str = ""
        self.Ar39ConstError: str = ""
        self.Ar37ConstError: str = ""
        self.Cl36ConstError: str = ""
        self.K40ECActivityError: str = ""
        self.K40BetaNActivityError: str = ""
        self.K40BetaPActivityError: str = ""
        self.Cl36vs38ProductivityError: str = ""
        self.K40MassError: str = ""
        self.NoConstError: str = "absolute error"
        self.YearConstError: str = ""
        self.K40vsKFractionsError: str = ""
        self.Cl35vsCl37FractionsError: str = ""
        self.HClvsClFractionsError: str = ""
        self.Ar40vsAr36AirConstError: str = ""
        self.JValue: str = ""
        self.JValueError: str = ""
        self.MDF: str = ""
        self.MDFError: str = ""
        self.Ar36Mass: str = ""
        self.Ar36MassError: str = ""
        self.Ar37Mass: str = ""
        self.Ar37MassError: str = ""
        self.Ar38Mass: str = ""
        self.Ar38MassError: str = ""
        self.Ar39Mass: str = ""
        self.Ar39MassError: str = ""
        self.Ar40Mass: str = ""
        self.Ar40MassError: str = ""
        self.York2FitConvergence: str = ""
        self.York2FitIteration: str = ""

        self.Ar40vsAr36Const: str = ""
        self.Ar40vsAr36ConstError: str = ""

        self.Fitting: str = "York-2"

        self.ForceNegative: str = "Force negative value to zero"
        self.CorrBlank: str = "Correct blank"
        self.CorrDiscr: str = "Correct mass discrimination"
        self.Corr37ArDecay: str = ""
        self.Corr39ArDecay: str = ""
        self.Corr36ClDecay: str = ""
        self.CorrK: str = ""
        self.CorrCa: str = ""
        self.CorrAtm: str = ""
        self.CorrCl: str = ""
        self.RelativeError: str = "Display relative error"
        self.UseDecayConst: str = ""
        self.UseInterceptCorrAtm: str = ""
        self.LinMassDiscrLaw: str = "Mass Discrimination method: Lin"
        self.ExpMassDiscrLaw: str = "Mass Discrimination method: Exp"
        self.PowMassDiscrLaw: str = "Mass Discrimination method: Pow"
        self.RecalibrationToPrimary: str = "Recalibration to primary standard"
        self.RecalibrationUseAge: str = "Recalibration to primary standard using age"
        self.RecalibrationUseRatio: str = "Recalibration to primary standard using ratio"
        
        self.Ar40vsAr36Trapped: str = ""
        self.Ar40vsAr36Cosmo: str = ""
        self.Ar38vsAr36Trapped: str = ""
        self.Ar38vsAr36Cosmo: str = ""
        self.Ar39vsAr37Ca: str = ""
        self.Ar38vsAr37Ca: str = ""
        self.Ar36vsAr37Ca: str = ""
        self.Ar40vsAr39K: str = ""
        self.Ar38vsAr39K: str = ""
        self.Ar36vsAr38Cl: str = ""
        self.KvsCaFactor: str = ""
        self.KvsClFactor: str = ""
        self.CavsClFactor: str = ""
        self.CavsClFactorError: str = ""
        self.KvsClFactorError: str = ""
        self.KvsCaFactorError: str = ""
        self.Ar36vsAr38ClError: str = ""
        self.Ar38vsAr39KError: str = ""
        self.Ar40vsAr39KError: str = ""
        self.Ar36vsAr37CaError: str = ""
        self.Ar38vsAr37CaError: str = ""
        self.Ar39vsAr37CaError: str = ""
        self.Ar38vsAr36CosmoError: str = ""
        self.Ar38vsAr36TrappedError: str = ""
        self.Ar40vsAr36CosmoError: str = ""
        self.Ar40vsAr36TrappedError: str = ""

        self.IrradiationEndTimeList: str = ""
        self.IrradiationDurationList: str = ""

        self.StandardName: str = ""

        self.StandardAge: str = ""
        self.StandardAgeError: str = ""

        self.PrimaryStdName: str = ""
        self.PrimaryStdAge: str = ""
        self.PrimaryStdAgeError: str = ""
        self.PrimaryStdAr40Conc: str = ""
        self.PrimaryStdAr40ConcError: str = ""
        self.PrimaryStdKConc: str = ""
        self.PrimaryStdKConcError: str = ""
        self.PrimaryStdAr40vsK: str = ""
        self.PrimaryStdAr40vsKError: str = ""

    def get_data(self):
        k = {}
        for key, value in self.__dict__.items():
            if key in list(CalcParams().__dict__.keys()) + list(IrraParams().__dict__.keys()):
                k[key] = value
        return k


class ParamsName(CalcParams, IrraParams):
    def __init__(self):
        CalcParams.__init__(self)
        IrraParams.__init__(self)

        self.K40Const: str = "40K"
        self.K40ECConst: str = "40K(EC)"
        self.K40BetaNConst: str = "40K(β-)"
        self.K40BetaPConst: str = "40K(β+)"
        self.Ar39Const: str = "39Ar"
        self.Ar37Const: str = "37Ar"
        self.Cl36Const: str = "36Cl"
        self.K40Activity: str = "40K"
        self.K40ActivityError: str = ""
        self.K40ECActivity: str = "40K(EC)"
        self.K40BetaNActivity: str = "40K(β-)"
        self.K40BetaPActivity: str = "40K(β+)"
        self.Cl36vs38Productivity: str = "36/38Cl(p)"
        self.K40Mass: str = "40K Mass"
        self.NoConst: str = "Avogadro Number"
        self.YearConst: str = "Seconds in a Year"
        self.K40vsKFractions: str = "40K/K"
        self.Cl35vsCl37Fractions: str = "35Cl/37Cl"
        self.HClvsClFractions: str = "HCl/Cl"
        self.Ar40vsAr36AirConst: str = "40/36Atm"

        self.K40ConstError: str = ""
        self.K40ECConstError: str = ""
        self.K40BetaNConstError: str = ""
        self.K40BetaPConstError: str = ""
        self.Ar39ConstError: str = ""
        self.Ar37ConstError: str = ""
        self.Cl36ConstError: str = ""
        self.K40ECActivityError: str = ""
        self.K40BetaNActivityError: str = ""
        self.K40BetaPActivityError: str = ""
        self.Cl36vs38ProductivityError: str = ""
        self.K40MassError: str = ""
        self.NoConstError: str = ""
        self.YearConstError: str = ""
        self.K40vsKFractionsError: str = ""
        self.Cl35vsCl37FractionsError: str = ""
        self.HClvsClFractionsError: str = ""
        self.Ar40vsAr36AirConstError: str = ""
        self.JValue: str = "J value"
        self.JValueError: str = ""
        self.MDF: str = "MDF"
        self.MDFError: str = ""
        self.Ar36Mass: str = "36Ar Mass"
        self.Ar36MassError: str = ""
        self.Ar37Mass: str = "37Ar Mass"
        self.Ar37MassError: str = ""
        self.Ar38Mass: str = "38Ar Mass"
        self.Ar38MassError: str = ""
        self.Ar39Mass: str = "39Ar Mass"
        self.Ar39MassError: str = ""
        self.Ar40Mass: str = "40Ar Mass"
        self.Ar40MassError: str = ""
        self.York2FitConvergence: str = "Convergence"
        self.York2FitIteration: str = "Iteration"

        self.Ar40vsAr36Const: str = ""
        self.Ar40vsAr36ConstError: str = ""

        self.Fitting: str = "Fitting Method"

        self.ForceNegative: str = ""
        self.CorrBlank: str = ""
        self.CorrDiscr: str = ""
        self.Corr37ArDecay: str = ""
        self.Corr39ArDecay: str = ""
        self.Corr36ClDecay: str = ""
        self.CorrK: str = ""
        self.CorrCa: str = ""
        self.CorrAtm: str = ""
        self.CorrCl: str = ""
        self.RelativeError: str = "Display relative error"
        self.UseDecayConst: str = ""
        self.UseInterceptCorrAtm: str = ""
        self.LinMassDiscrLaw: str = "Mass Discrimination method"
        self.ExpMassDiscrLaw: str = "Mass Discrimination method"
        self.PowMassDiscrLaw: str = "Mass Discrimination method"
        self.RecalibrationToPrimary: str = ""
        self.RecalibrationUseAge: str = "Recalibration to primary standard using age"
        self.RecalibrationUseRatio: str = "Recalibration to primary standard using ratio"

        self.Ar40vsAr36Trapped: str = ""
        self.Ar40vsAr36Cosmo: str = ""
        self.Ar38vsAr36Trapped: str = ""
        self.Ar38vsAr36Cosmo: str = ""
        self.Ar39vsAr37Ca: str = ""
        self.Ar38vsAr37Ca: str = ""
        self.Ar36vsAr37Ca: str = ""
        self.Ar40vsAr39K: str = ""
        self.Ar38vsAr39K: str = ""
        self.Ar36vsAr38Cl: str = ""
        self.KvsCaFactor: str = ""
        self.KvsClFactor: str = ""
        self.CavsClFactor: str = ""
        self.CavsClFactorError: str = ""
        self.KvsClFactorError: str = ""
        self.KvsCaFactorError: str = ""
        self.Ar36vsAr38ClError: str = ""
        self.Ar38vsAr39KError: str = ""
        self.Ar40vsAr39KError: str = ""
        self.Ar36vsAr37CaError: str = ""
        self.Ar38vsAr37CaError: str = ""
        self.Ar39vsAr37CaError: str = ""
        self.Ar38vsAr36CosmoError: str = ""
        self.Ar38vsAr36TrappedError: str = ""
        self.Ar40vsAr36CosmoError: str = ""
        self.Ar40vsAr36TrappedError: str = ""

        self.IrradiationEndTimeList: str = ""
        self.IrradiationDurationList: str = ""

        self.StandardName: str = ""

        self.StandardAge: str = ""
        self.StandardAgeError: str = ""
        self.Ar40Concentration: str = ""
        self.Ar40ConcentrationError: str = ""
        self.KConcentration: str = ""
        self.KConcentrationError: str = ""
        self.StandardAr40vsK: str = ""
        self.StandardAr40vsKError: str = ""

    def get_data(self):
        k = {}
        for key, value in self.__dict__.items():
            if key in list(CalcParams().__dict__.keys()) + list(IrraParams().__dict__.keys()):
                k[key] = value
        return k

class DefaultParams:
    def __init__(self, **kwargs):
        self.K40Const: float = 0.0000000005530  # decay constant of K40, unit in /a
        self.K40ECConst: float = 0.000000000058  # 40K --> 40Ar
        self.K40BetaNConst: float = 0.000000000495  # alpha -, 40K --> 40Ca
        self.K40BetaPConst: float = 0  # alpha +
        self.Ar39Const: float = 0.0000002940
        self.Ar37Const: float = 0.0008230
        self.Cl36Const: float = 0.000002257
        self.K40Activity: float = 31.58
        self.K40ActivityError: float = 0.064
        self.K40ECActivity: float = 3.310
        self.K40BetaNActivity: float = 28.270
        self.K40BetaPActivity: float = 0
        self.Cl36vs38Productivity: float = 0
        self.K40Mass: float = 39.0983
        self.NoConst: float = 6.0221367e+23  # avogadro number
        self.YearConst: float = 31556930  # seconds in a year
        self.K40vsKFractions: float = 0.000117
        self.Cl35vsCl37Fractions: float = 3.08663
        self.HClvsClFractions: float = 0.2
        self.Ar40vsAr36AirConst: float = 298.56

        self.K40ConstError: float = 0.0000000000048  # absolute error
        self.K40ECConstError: float = 0.0000000000048
        self.K40BetaNConstError: float = 0.00000000000430  # absolute error
        self.K40BetaPConstError: float = 0
        self.Ar39ConstError: float = 0.0000000016
        self.Ar37ConstError: float = 0.0000012
        self.Cl36ConstError: float = 0.000000015
        self.K40ECActivityError: float = 0.040
        self.K40BetaNActivityError: float = 0.050
        self.K40BetaPActivityError: float = 0
        self.Cl36vs38ProductivityError: float = 0
        self.K40MassError: float = 0
        self.NoConstError: float = 3.553060653e+17  # absolute error
        self.YearConstError: float = 0
        self.K40vsKFractionsError: float = 0.000100
        self.Cl35vsCl37FractionsError: float = 2
        self.HClvsClFractionsError: float = 20
        self.Ar40vsAr36AirConstError: float = 0
        self.JValue: float = 0.015150673
        self.JValueError: float = 0.5
        self.MDF: float = 0.995573
        self.MDFError: float = 0.1
        self.Ar36Mass: float = 35.96754628
        self.Ar36MassError: float = 0
        self.Ar37Mass: float = 36.9667759
        self.Ar37MassError: float = 0
        self.Ar38Mass: float = 37.9627322
        self.Ar38MassError: float = 0
        self.Ar39Mass: float = 38.964313
        self.Ar39MassError: float = 0
        self.Ar40Mass: float = 39.962383123
        self.Ar40MassError: float = 0
        self.York2FitConvergence: float = 0.01
        self.York2FitIteration: float = 100

        self.Ar40vsAr36Const: float = 298.56
        self.Ar40vsAr36ConstError: float = 0

        self.Fitting: str = "York-2"

        self.ForceNegative: bool = True  # Force negative value to zero
        self.CorrBlank: bool = True  # Correct blank
        self.CorrDiscr: bool = True  # Correct mass discrimination
        self.Corr37ArDecay: bool = True
        self.Corr39ArDecay: bool = True
        self.Corr36ClDecay: bool = True
        self.CorrK: bool = True
        self.CorrCa: bool = True
        self.CorrAtm: bool = True
        self.CorrCl: bool = True
        self.DisplayRelative: bool = True  # Display relative error
        self.UseDecayConst: bool = False
        self.UseInterceptCorrAtm: bool = False
        self.LinMassDiscrLaw: bool = True  # Mass Discrimination method: Lin
        self.ExpMassDiscrLaw: bool = False  # Mass Discrimination method: Exp
        self.PowMassDiscrLaw: bool = False  # Mass Discrimination method: Pow
        self.RecalibrationToPrimary: bool = False
        self.RecalibrationUseAge: bool = False
        self.RecalibrationUseRatio: bool = False

        self.Ar40vsAr36Trapped: float = kwargs.pop("Ar40vsAr36Trapped", 298.56)
        self.Ar40vsAr36Cosmo: float = kwargs.pop("Ar40vsAr36Cosmo", 0.018)
        self.Ar38vsAr36Trapped: float = kwargs.pop("Ar38vsAr36Trapped", 0.1869)
        self.Ar38vsAr36Cosmo: float = kwargs.pop("Ar38vsAr36Cosmo", 1.493)
        self.Ar39vsAr37Ca: float = kwargs.pop("Ar39vsAr37Ca", 0.000699)
        self.Ar38vsAr37Ca: float = kwargs.pop("Ar38vsAr37Ca", 0)
        self.Ar36vsAr37Ca: float = kwargs.pop("Ar36vsAr37Ca", 0.00027)
        self.Ar40vsAr39K: float = kwargs.pop("Ar40vsAr39K", 0.01024)
        self.Ar38vsAr39K: float = kwargs.pop("Ar38vsAr39K", 0)
        self.Ar36vsAr38Cl: float = kwargs.pop("Ar36vsAr38Cl", 262.8)
        self.KvsCaFactor: float = kwargs.pop("KvsCaFactor", 0.57)
        self.KvsClFactor: float = kwargs.pop("KvsClFactor", 0)
        self.CavsClFactor: float = kwargs.pop("CavsClFactor", 0)
        self.CavsClFactorError: float = kwargs.pop("CavsClFactorError", 0)
        self.KvsClFactorError: float = kwargs.pop("KvsClFactorError", 0)
        self.KvsCaFactorError: float = kwargs.pop("KvsCaFactorError", 0.570 * 2 / 100)
        self.Ar36vsAr38ClError: float = kwargs.pop("Ar36vsAr38ClError", 0)
        self.Ar38vsAr39KError: float = kwargs.pop("Ar38vsAr39KError", 0.1)
        self.Ar40vsAr39KError: float = kwargs.pop("Ar40vsAr39KError", 24.9)
        self.Ar36vsAr37CaError: float = kwargs.pop("Ar36vsAr37CaError", 0.37)
        self.Ar38vsAr37CaError: float = kwargs.pop("Ar38vsAr37CaError", 21.9)
        self.Ar39vsAr37CaError: float = kwargs.pop("Ar39vsAr37CaError", 1.83)
        self.Ar38vsAr36CosmoError: float = kwargs.pop("Ar38vsAr36CosmoError", 3)
        self.Ar38vsAr36TrappedError: float = kwargs.pop("Ar38vsAr36TrappedError", 0)
        self.Ar40vsAr36CosmoError: float = kwargs.pop("Ar40vsAr36CosmoError", 35)
        self.Ar40vsAr36TrappedError: float = kwargs.pop("Ar40vsAr36TrappedError", 0)

        self.IrradiationEndTimeList: list = kwargs.pop("IrradiationEndTimeList", [1522797300, 1522798400])
        self.IrradiationDurationList: list = kwargs.pop("IrradiationDurationList", [38.0, 40.0])

        self.StandardName: str = kwargs.pop("StandardName", "")
        self.StandardAge: float = kwargs.pop("StandardAge", 132.7)
        self.StandardAgeError: float = kwargs.pop("StandardAgeError", 132.7 * 0.91 / 100)

        self.PrimaryStdName: str = kwargs.pop("PrimaryStdName", "")
        self.PrimaryStdAge: float = kwargs.pop("PrimaryStdAge", 0)
        self.PrimaryStdAgeError: float = kwargs.pop("PrimaryStdAgeError", 0)
        self.PrimaryStdAr40Conc: float = kwargs.pop("PrimaryStdAr40Conc", 0)
        self.PrimaryStdAr40ConcError: float = kwargs.pop("PrimaryStdAr40ConcError", 0)
        self.PrimaryStdKConc: float = kwargs.pop("PrimaryStdKConc", 0)
        self.PrimaryStdKConcError: float = kwargs.pop("PrimaryStdKConcError", 0)
        self.PrimaryStdAr40vsK: float = kwargs.pop("PrimaryStdAr40vsK", 0)
        self.PrimaryStdAr40vsKError: float = kwargs.pop("PrimaryStdAr40vsKError", 0)
