#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : sample.py
# @Author : Yang Wu
# @Date   : 2021/12/19
# @Email  : wuy@cug.edu.cn

class Sample:
    def __init__(self,
                 sample_name=None, experiment_name=None,
                 argon36=None, argon37=None, argon38=None, argon39=None, argon40=None):
        self.sample_name: str = sample_name
        self.experiment_name: str = experiment_name
        self.argon36: list = argon36
        self.argon37: list = argon37
        self.argon38: list = argon38
        self.argon39: list = argon39
        self.argon40: list = argon40

    def setSampleName(self, name: str):
        self.sample_name = name

    def setExperimentName(self, name: str):
        self.experiment_name = name

    def setArgon36(self, data: list):
        self.argon36 = data

    def setArgon37(self, data: list):
        self.argon37 = data

    def setArgon38(self, data: list):
        self.argon38 = data

    def setArgon39(self, data: list):
        self.argon39 = data

    def setArgon40(self, data: list):
        self.argon40 = data

    def sampleName(self):
        return self.sample_name

    def experimentName(self):
        return self.experiment_name

    def argon36(self):
        return self.argon36

    def argon37(self):
        return self.argon37

    def argon38(self):
        return self.argon38

    def sargon39(self):
        return self.argon39

    def argon40(self):
        return self.argon40
