#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : mainProcess.py
# @Author : Yang Wu
# @Date   : 2022/1/14
# @Email  : wuy@cug.edu.cn

import pyarar

def process_unksmp(unksmp: pyarar.sample.UnkSample):
    print(unksmp.IsochronSelectedPoints)
    pyarar.sampleFuncs.initializeData(unksmp)
    pyarar.sampleFuncs.readDataFromAgeFile(unksmp)
    pyarar.sampleFuncs.corrBlank(unksmp)
    pyarar.sampleFuncs.corrDiscr(unksmp)
    pyarar.sampleFuncs.corrDecay(unksmp)
    pyarar.sampleFuncs.degasPattern(unksmp)
    pyarar.sampleFuncs.calcApparentAge(unksmp)
    pyarar.sampleFuncs.calcRatios(unksmp)
    pyarar.sampleFuncs.calcIsochronAge(unksmp)
    pyarar.sampleFuncs.calcKCaClRatios(unksmp)
    pyarar.sampleFuncs.calcPlateauAge(unksmp)
    pyarar.sampleFuncs.calcTFAge(unksmp)
    pyarar.sampleFuncs.calc3DIsochronAge(unksmp)
    pyarar.sampleFuncs.plotAgeSpectra(unksmp)
    pyarar.sampleFuncs.plot3DIsochron(unksmp)
    pyarar.sampleFuncs.plotIsochron(unksmp)

def process_monitor(monitor: pyarar.sample.MonitorSample):
    pyarar.sampleFuncs.initializeData(monitor)
    pyarar.sampleFuncs.readDataFromAgeFile(monitor)
    pyarar.sampleFuncs.corrBlank(monitor)
    pyarar.sampleFuncs.corrDiscr(monitor)
    pyarar.sampleFuncs.corrDecay(monitor)
    pyarar.sampleFuncs.degasPattern(monitor)
    pyarar.sampleFuncs.calcJValue(monitor)

def process_airsmp(air: pyarar.sample.AirSample):
    pyarar.sampleFuncs.readDataFromAgeFile(air)
    pyarar.sampleFuncs.corrBlank(air)
    pyarar.sampleFuncs.calcMDF(air)
