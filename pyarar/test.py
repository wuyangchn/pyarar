#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : test.py
# @Author : Yang Wu
# @Date   : 2021/12/19
# @Email  : wuy@cug.edu.cn

import pyarar
import pickle
import os

"""
b = pyarar.sample.UnkSample(SampleName='Test100')
b.RawFilePath = "C:\\Users\\Young\\Projects\\2019-04Ar-Ar数据处理\\examples\\06excel\\19WHA0106.xls"
b.FilteredFilePath = "C:\\Users\\Young\\Projects\\2019-04Ar-Ar数据处理\\filtered_file\\19WHA0106.xls"
b.AgeFilePath = "C:\\Users\\Young\\Projects\\2019-04Ar-Ar数据处理\\examples\\06age\\19WHA0106.age"
b.readDataFromFilteredFile()
b.readDataFromAgeFile()
pyarar.maincalc.corrBlank(b)
pyarar.maincalc.corrDiscr(b)
pyarar.maincalc.corrDecay(b)
pyarar.maincalc.degasPattern(b)
pyarar.maincalc.calcApparentAge(b)
pyarar.maincalc.calcRatios(b)
b.IsochronSelectedPoints = [i for i in range(7, 28)]
pyarar.maincalc.isochronAge(b)
pyarar.maincalc.calcKCaClRatios(b)
pyarar.maincalc.calcPlateauAge(b)
b.save()
"""

"""read age"""
def calc(unksp: pyarar.sample.UnkSample):
    unksp.readDataFromAgeFile()
    unksp.IsochronSelectedPoints = [i for i in range(len(unksp.Ar36MList))]
    pyarar.maincalc.corrBlank(unksp)
    pyarar.maincalc.corrDiscr(unksp)
    pyarar.maincalc.corrDecay(unksp)
    pyarar.maincalc.degasPattern(unksp)
    pyarar.maincalc.calcApparentAge(unksp)
    pyarar.maincalc.calcRatios(unksp)
    pyarar.maincalc.isochronAge(unksp)
    pyarar.maincalc.calcKCaClRatios(unksp)
    pyarar.maincalc.calcPlateauAge(unksp)
    pyarar.maincalc.calcTFAge(unksp)


age_dir = "C:\\Users\\Young\\Projects\\B02Ar-Ar年代学\\数据集合\\Data\\06age"
files = os.listdir(age_dir)
print(files)
for i in files:
    sp = pyarar.sample.UnkSample(SampleName=i.split('.age')[0])
    sp.AgeFilePath = "{}\\{}".format(age_dir, i)
    calc(sp)
    sp.save()

"""read sp files"""
files = os.listdir('save')
res = []
for filename in files:
    with open('save\\' + filename, 'rb') as f:
        res.append(pickle.load(f))

for i in res:
    print("{}  ID: {}, TF Age: {}, {}, {}".format(i.SampleName, i.SampleID, i.TotalFusionAge[0], i.TotalFusionAge[4],
                                                  i.TotalFusionAge[6]))
