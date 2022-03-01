#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : FuncsFile.py
# @Author : Yang Wu
# @Date   : 2021/12/20
# @Email  : wuy@cug.edu.cn

"""
Functions involved in read and write files.
"""
import pickle
import pyarar
import pyarar.FuncsCalc as FuncsCalc


def openSmpFile(path: str):
    with open(path, 'rb') as f:
        smp = pickle.load(f)
    return smp

def openAgeFile(path: str):
    sampleName = path.split("/")[-1].split(".")[0]
    smp = pyarar.sample.UnkSample(SampleName=sampleName)
    smp.AgeFilePath = path
    pyarar.FuncsSample.initializeData(smp)
    pyarar.FuncsSample.readDataFromAgeFile(smp)
    pyarar.mainProcess.process_unksmp(smp)
    smp.save()
    return smp

def openAirFile(path: str):
    sampleName = path.split("/")[-1].split(".")[0]
    smp = pyarar.sample.AirSample(SampleName=sampleName)
    smp.AgeFilePath = path
    pyarar.FuncsSample.initializeData(smp)
    pyarar.FuncsSample.readDataFromAgeFile(smp)
    pyarar.mainProcess.process_airsmp(smp)
    smp.save()
    return smp

def openRawFile(path: str):
    return False

def openFilteredFile(path: str):
    """
    :param path: directory of file
    :return: list = [dict, dict]
    """
    k = []
    for i in path.split("\\"):
        k = k + i.split("/")
    sampleName = k[-1].split(".")[0]
    smp = pyarar.sample.UnkSample(SampleName=sampleName)
    smp.FilteredFilePath = path
    pyarar.FuncsSample.initializeData(smp)
    pyarar.FuncsSample.readDataFromFilteredFile(smp)
    return smp


def openOriginalFile(path: str):
    """
    :param path: directory of file
    :return: step_list -> [[[header of step one], [cycle one in the step], [cycle two in the step]],[[],[]]]
    """
    res = FuncsCalc.open_original_xls(path)
    return res
