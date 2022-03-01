#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : mainProcess.py
# @Author : Yang Wu
# @Date   : 2022/1/14
# @Email  : wuy@cug.edu.cn

import pyarar

def process_unksmp(unksmp: pyarar.sample.UnkSample):
    print("1")
    pyarar.FuncsSample.corrBlank(unksmp)
    pyarar.FuncsSample.corrDiscr(unksmp)
    print("2")
    pyarar.FuncsSample.corrDecay(unksmp)
    pyarar.FuncsSample.degasPattern(unksmp)
    print("3")
    pyarar.FuncsSample.calcApparentAge(unksmp)
    pyarar.FuncsSample.calcRatios(unksmp)
    print("4")
    pyarar.FuncsSample.calcIsochronAge(unksmp)
    pyarar.FuncsSample.calc3DIsochronAge(unksmp)
    print("5")
    pyarar.FuncsSample.calcKCaClRatios(unksmp)
    pyarar.FuncsSample.calcPlateauAge(unksmp)
    print("6")
    # pyarar.FuncsSample.plotAgeSpectra(unksmp)
    pyarar.FuncsSample.calcTFAge(unksmp)
    print("7")
    # pyarar.FuncsSample.plot3DIsochron(unksmp)
    # pyarar.FuncsSample.plotIsochron(unksmp)

def process_monitor(monitor: pyarar.sample.MonitorSample):
    pyarar.FuncsSample.initializeData(monitor)
    pyarar.FuncsSample.readDataFromAgeFile(monitor)
    pyarar.FuncsSample.corrBlank(monitor)
    pyarar.FuncsSample.corrDiscr(monitor)
    pyarar.FuncsSample.corrDecay(monitor)
    pyarar.FuncsSample.degasPattern(monitor)
    pyarar.FuncsSample.calcJValue(monitor)

def process_airsmp(air: pyarar.sample.AirSample):
    pyarar.FuncsSample.readDataFromAgeFile(air)
    pyarar.FuncsSample.corrBlank(air)
    pyarar.FuncsSample.calcMDF(air)
