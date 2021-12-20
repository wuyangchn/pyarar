#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : test.py
# @Author : Yang Wu
# @Date   : 2021/12/19
# @Email  : wuy@cug.edu.cn

from pyarar.sample import Sample
b = Sample()
print(b.Ar36MList)
b.readDataFromRawFile()
print(b.Ar36MList)
b.RawFilePath = "C:\\Users\\Young\\Projects\\2019-04Ar-Ar数据处理\\examples\\06excel\\19WHA0099.xls"
b.readDataFromRawFile()
print(b.Ar36MList)
