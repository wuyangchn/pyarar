#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : test.py
# @Author : Yang Wu
# @Date   : 2021/12/19
# @Email  : wuy@cug.edu.cn

import pyarar
import pickle
import os

import pyarar.FuncsCalc


'''
b = pyarar.sample.UnkSample(SampleName='Test100')
b.AgeFilePath = "C:\\Users\\Young\\Projects\\B02Ar-Ar年代学\\数据集合\\Data\\06age\\16WHA0420.age"
pyarar.mainProcess.process_unksmp(b)
b.save()
print(b.AnalysisDate)
print(b.__dict__)
'''

age_dir = "C:\\Users\\Young\\Projects\\B02Ar-Ar年代学\\数据集合\\Data\\06age"
files = os.listdir(age_dir)
print(files)
for i in files:
    smp = pyarar.sample.UnkSample(SampleName=i.split('.age')[0])
    smp.AgeFilePath = "{}\\{}".format(age_dir, i)
    pyarar.FuncsSample.initializeData(smp)
    pyarar.FuncsSample.readDataFromAgeFile(smp)
    pyarar.mainProcess.process_unksmp(smp)
    smp.save()

"""read sp files"""
'''
files = os.listdir('save')
res = []
for filename in files:
    with open('save\\' + filename, 'rb') as f:
        res.append(pickle.load(f))

for i in res:
    print("{}  ID: {}, TF Age: {}, {}, {}".format(i.SampleName, i.SampleID, i.TotalFusionAge[0], i.TotalFusionAge[4],
                                                  i.TotalFusionAge[6]))
for i in res:
    print("{}, SelectedPoints: {}".format(i.SampleName, i.IsochronSelectedPoints))

'''