#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : test.py
# @Author : Yang Wu
# @Date   : 2021/12/19
# @Email  : wuy@cug.edu.cn

from pyarar.sample import Sample
import pickle
b = Sample(SampleName='19HN34')
print(b.Ar36MList)
b.readDataFromRawFile()
print(b.Ar36MList)
b.RawFilePath = "C:\\Users\\Young\\Projects\\2019-04Ar-Ar数据处理\\examples\\06excel\\19WHA0099.xls"
b.readDataFromRawFile()
print(b.Ar36MList)
b.save()
print(b.SampleID)

res = []
with open('save\\' + str(b.SampleName) + '.sp', 'rb') as f:
    try:
        while True:
            res.append(pickle.load(f))
    except EOFError:
        print('Ran out of input, total instances: {}'.format(len(res)))

for i in res:
    print(i.SampleID)
    i.SampleID = 1000001

if res:
    print(res[0].SampleID)
