#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : test.py
# @Author : Yang Wu
# @Date   : 2021/12/19
# @Email  : wuy@cug.edu.cn

import pyarar
import pickle
b = pyarar.sample.Sample(SampleName='2021-12-25')
b.RawFilePath = "C:\\Users\\Young\\Projects\\2019-04Ar-Ar数据处理\\examples\\06excel\\19WHA0106.xls"
b.FilteredFilePath = "C:\\Users\\Young\\Projects\\2019-04Ar-Ar数据处理\\filtered_file\\19WHA0106.xls"
b.AgeFilePath = "C:\\Users\\Young\\Projects\\2019-04Ar-Ar数据处理\\examples\\06age\\19WHA0106.age"
b.readDataFromFilteredFile()
print(b.Ar40MList)
print(b.JValue)
b.readDataFromAgeFile()
print(b.Ar40MList)
print(b.JValue)
b.save()
print(b.SampleID)
pyarar.maincalc.corrBlank(b)
pyarar.maincalc.corrDiscr(b)
pyarar.maincalc.corrDecay(b)
pyarar.maincalc.degasPattern(b)
print(b.Ar40TempList)
print(b.Ar40DegasCa)
print(b.Ar40DegasK)
print(b.Ar40DegasCl)
print(b.Ar40DegasAir)
print(b.Ar40DegasR)

print([b.Ar40DegasRError[i] / b.Ar40DegasR[i] * 100 if b.Ar40DegasR[i] != 0 else b.Ar40DegasRError[i]
       for i in range(len(b.Ar40DegasR))])
print([b.Ar37DegasCaError[i] / b.Ar37DegasCa[i] * 100 if b.Ar37DegasCa[i] != 0 else b.Ar37DegasCaError[i]
       for i in range(len(b.Ar37DegasCa))])
print([b.Ar39DegasKError[i] / b.Ar39DegasK[i] * 100 if b.Ar39DegasK[i] != 0 else b.Ar39DegasKError[i]
       for i in range(len(b.Ar39DegasK))])

print(b.Ar36DegasClError)
print(b.Ar36DegasAirError)

print(b.Ar37DegasCaError)

print(b.IrradiationEndTimeList)
print(b.IrradiationDurationList)

res = []
with open('save\\' + str(b.SampleName) + '.sp', 'rb') as f:
    try:
        while True:
            res.append(pickle.load(f))
    except EOFError:
        print('Ran out of input, total instances: {}'.format(len(res)))

if res:
    for i in res:
        print(i.SampleID)

intercept = ['19WHA0108-2',
             '10',
             182.74678105256325, 0.0802784643137285, 0.998705097597825,
             0.17113117298079894, 0.032199395467275835, 0.43691564860851784,
             70.83002910293253, 0.07720134348499089, 0.9931499048049998,
             23.293486204146, 0.10014190141384188, 0.9738585285223623,
             95567.41360837073, 10.206991312599605, 0.9997178053923798,
             '17', '6', '2019', '20', '52']

blank = ['19WHA0108-2',
         'B',
         '19WHA0108-1',
         0.4581299712144843, 0.012239800128894291,
         0.3885501642692472, 0.026614525519796706,
         0.4247204887583761, 0.017352795639247146,
         1.3634743626111332, 0.05538157572278121,
         106.54710118438761, 0.10652459245529279,
         '17', '6', '2019', '20', '40']
