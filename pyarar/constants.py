#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : constants.py
# @Author : Yang Wu
# @Date   : 2021/12/20
# @Email  : wuy@cug.edu.cn

"""
Constants used.
"""

"""====================="""
"""Decay Physical Params"""
"""====================="""
K40Const = 0.0000000005530  # decay constant of K40, unit in /a
K40ConstError = 0.0000000000048  # absolute error
K40ECConst = 0.000000000058  # 40K --> 40Ar
K40ECConstError = 0.000000000058 * 1.466 / 100  # absolute error
K40BetaNConst = 0.000000000495  # alpha -, 40K --> 40Ca
K40BetaNConstError = 0.000000000495 * 0.869 / 100  # absolute error
K40BetaPConst = 0  # alpha +
K40BetaPConstError = 0
Ar39Const = 0.0000002940
Ar39ConstError = 0.0000000016
Ar37Const = 0.0008230
Ar37ConstError = 0.0000012
Cl36Const = 0.000002257
Cl36ConstError = 0.000000015
K40ECActivity = 3.310  # activity of 40K --> 40Ar, unit in /(g * sec)
K40ECActivityError = 0.040
K40BetaNActivity = 28.270  # activity of 40K --> 40Ca
K40BetaNActivityError = 0.050
K40BetaPActivity = 0
K40BetaPActivityError = 0
K40Activity = 31.58
K40ActivityError = 0.064
Cl36vs38Productivity = 0
Cl36vs38ProductivityError = 0
NoConst = 6.0221367e+23  # avogadro number
NoConstError = 3.553060653e+17  # absolute error
yearConst = 31556930  # seconds in a year
yearConstError = 0  # absolute error

"""====================="""
"""Isotopes Constants"""
"""====================="""
K40vsKFractions = 0.000117  # relative proportion of K40 in total K element
K40vsKFractionsError = 0.00000100035  # absolute error
Cl35vsClFractions = 3.08663
Cl35vsClFractionsError = Cl35vsClFractions * 2 / 100
HClvsClFractions = 0.2
HClvsClFractionsError = HClvsClFractions * 20 / 100
Ar40vsAr36AirConst = 298.56
Ar40vsAr36AirConstError = Ar40vsAr36AirConst * 0.1 / 100
K40Mass = 39.0983
K40MassError = K40Mass * 0.000154 / 100  # absolute error
Ar36Mass = 35.96754628
Ar36MassError = 0
Ar37Mass = 36.9667759
Ar37MassError = 0
Ar38Mass = 37.9627322
Ar38MassError = 0
Ar39Mass = 38.964313
Ar39MassError = 0
Ar40Mass = 39.962383123
Ar40MassError = 0

"""=============="""
"""Special Params"""
"""=============="""
JValue = 0.01
JValueError = 0.5
MDF = 0.995573
MDFError = 0.1

Ar40vsAr36Const = 298.56
Ar40vsAr36ConstError = 0
York2FitConvergence = 0.01
York2FitIteration = 100
Fitting = "York-2"
LinMassDiscrLaw = True
ExpMassDiscrLaw = False
PowMassDiscrLaw = False
ForceNegative = True
CorrBlank = True
CorrDiscr = True
Corr37ArDecay = True
Corr39ArDecay = True
CorrK = True
CorrCa = True
CorrCl = True
CorrAtm = True
Corr36ClDecay = True
RelativeError = True
UseDecayConst = False
UseInterceptCorrAtm = False
UseMinCalculation = True

Ar40vsAr36Trapped = 298.56
Ar40vsAr36Cosmo = 0.018
Ar38vsAr36Trapped = 0.1869
Ar38vsAr36Cosmo = 1.493
Ar39vsAr37Ca = 0.000699
Ar38vsAr37Ca = 0
Ar36vsAr37Ca = 0.000270
Ar40vsAr39K = 0.010240
Ar38vsAr39K = 0
Ar36vsAr38Cl = 262.80
KvsCaFactor = 0.570
KvsClFactor = 0
CavsClFactor = 0
CavsClFactorError = 0
KvsClFactorError = 0
KvsCaFactorError = 0.570 * 2 / 100
Ar36vsAr38ClError = 0
Ar38vsAr39KError = 0.1
Ar40vsAr39KError = 24.9
Ar36vsAr37CaError = 0.37
Ar38vsAr37CaError = 21.9
Ar39vsAr37CaError = 1.83
Ar38vsAr36CosmoError = 3
Ar38vsAr36TrappedError = 0
Ar40vsAr36CosmoError = 35
Ar40vsAr36TrappedError = 0
IrradiationEndTimeList = [1522797300, 1522798400]
IrradiationDurationList = [38.0, 40.0]

"""===================="""
"""Standard Information"""
"""===================="""
StandardAge = 132.7  # standard age of monitor mineral, unit in Ma
StandardAgeError = StandardAge * 0.91 / 100  # absolute error
Ar40Concentration = 1.813
Ar40ConcentrationError = Ar40Concentration * 0.001 / 100
KConcentration = 7.597
KConcentrationError = KConcentration * 0.03 / 100
StandardAr40vsK = 0
StandardAr40vsKError = 0
