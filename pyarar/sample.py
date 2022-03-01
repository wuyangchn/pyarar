#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : sample.py
# @Author : Yang Wu
# @Date   : 2021/12/19
# @Email  : wuy@cug.edu.cn

"""
Create a sample instance.
"""
import os
import pickle
import datetime
from pyarar.params import CalcParams, IrraParams


class IntermediateData:
    def __init__(self, **kwargs):
        # intermediate list used to save correction values
        self.Ar36List: list = kwargs.pop("Ar36TempList", [])
        self.Ar37List: list = kwargs.pop("Ar37TempList", [])
        self.Ar38List: list = kwargs.pop("Ar38TempList", [])
        self.Ar39List: list = kwargs.pop("Ar39TempList", [])
        self.Ar40List: list = kwargs.pop("Ar40TempList", [])
        self.Ar36ErrorList: list = kwargs.pop("Ar36TempErrorList", [])
        self.Ar37ErrorList: list = kwargs.pop("Ar37TempErrorList", [])
        self.Ar38ErrorList: list = kwargs.pop("Ar38TempErrorList", [])
        self.Ar39ErrorList: list = kwargs.pop("Ar39TempErrorList", [])
        self.Ar40ErrorList: list = kwargs.pop("Ar40TempErrorList", [])

        """Unknown Sample"""
        # isotopes degas value
        self.Ar36DegasCa: list = kwargs.pop("Ar36DegasCa", [])
        self.Ar36DegasK: list = kwargs.pop("Ar36DegasK", [])
        self.Ar36DegasCl: list = kwargs.pop("Ar36DegasCl", [])
        self.Ar36DegasAir: list = kwargs.pop("Ar36DegasAir", [])
        self.Ar37DegasCa: list = kwargs.pop("Ar37DegasCa", [])
        self.Ar37DegasK: list = kwargs.pop("Ar37DegasK", [])
        self.Ar37DegasCl: list = kwargs.pop("Ar37DegasCl", [])
        self.Ar37DegasAir: list = kwargs.pop("Ar37DegasAir", [])
        self.Ar38DegasCa: list = kwargs.pop("Ar38DegasCa", [])
        self.Ar38DegasK: list = kwargs.pop("Ar38DegasK", [])
        self.Ar38DegasCl: list = kwargs.pop("Ar38DegasCl", [])
        self.Ar38DegasAir: list = kwargs.pop("Ar38DegasAir", [])
        self.Ar39DegasCa: list = kwargs.pop("Ar39DegasCa", [])
        self.Ar39DegasK: list = kwargs.pop("Ar39DegasK", [])
        self.Ar39DegasCl: list = kwargs.pop("Ar39DegasCl", [])
        self.Ar39DegasAir: list = kwargs.pop("Ar39DegasAir", [])
        self.Ar40DegasCa: list = kwargs.pop("Ar40DegasCa", [])
        self.Ar40DegasK: list = kwargs.pop("Ar40DegasK", [])
        self.Ar40DegasCl: list = kwargs.pop("Ar40DegasCl", [])
        self.Ar40DegasAir: list = kwargs.pop("Ar40DegasAir", [])
        self.Ar40DegasR: list = kwargs.pop("Ar40DegasR", [])

        # degas results data
        self.Ar36DegasCaError: list = kwargs.pop("Ar36DegasCaError", [])
        self.Ar36DegasKError: list = kwargs.pop("Ar36DegasKError", [])
        self.Ar36DegasClError: list = kwargs.pop("Ar36DegasClError", [])
        self.Ar36DegasAirError: list = kwargs.pop("Ar36DegasAirError", [])
        self.Ar37DegasCaError: list = kwargs.pop("Ar37DegasCaError", [])
        self.Ar37DegasKError: list = kwargs.pop("Ar37DegasKError", [])
        self.Ar37DegasClError: list = kwargs.pop("Ar37DegasClError", [])
        self.Ar37DegasAirError: list = kwargs.pop("Ar37DegasAirError", [])
        self.Ar38DegasCaError: list = kwargs.pop("Ar38DegasCaError", [])
        self.Ar38DegasKError: list = kwargs.pop("Ar38DegasKError", [])
        self.Ar38DegasClError: list = kwargs.pop("Ar38DegasClError", [])
        self.Ar38DegasAirError: list = kwargs.pop("Ar38DegasAirError", [])
        self.Ar39DegasCaError: list = kwargs.pop("Ar39DegasCaError", [])
        self.Ar39DegasKError: list = kwargs.pop("Ar39DegasKError", [])
        self.Ar39DegasClError: list = kwargs.pop("Ar39DegasClError", [])
        self.Ar39DegasAirError: list = kwargs.pop("Ar39DegasAirError", [])
        self.Ar40DegasCaError: list = kwargs.pop("Ar40DegasCaError", [])
        self.Ar40DegasKError: list = kwargs.pop("Ar40DegasKError", [])
        self.Ar40DegasClError: list = kwargs.pop("Ar40DegasClError", [])
        self.Ar40DegasAirError: list = kwargs.pop("Ar40DegasAirError", [])
        self.Ar40DegasRError: list = kwargs.pop("Ar40DegasRError", [])

        self.FValues: list = kwargs.pop("FValues", [])
        self.FValuesError: list = kwargs.pop("FValuesError", [])
        self.ApparentAge: list = kwargs.pop("ApparentAge", [])
        self.ApparentAgeAnalysisError: list = kwargs.pop("ApparentAgeAnalysisError", [])
        self.ApparentAgeInternalError: list = kwargs.pop("ApparentAgeInternalError", [])
        self.ApparentAgeFullExternalError: list = kwargs.pop("ApparentAgeFullExternalError", [])
        self.KCaRatios: list = kwargs.pop("KCaRatios", [])
        self.KCaRatiosError: list = kwargs.pop("KCaRatiosError", [])
        self.KClRatios: list = kwargs.pop("KClRatios", [])
        self.KClRatiosError: list = kwargs.pop("KClRatiosError", [])
        self.CaClRatios: list = kwargs.pop("CaClRatios", [])
        self.CaClRatiosError: list = kwargs.pop("CaClRatiosError", [])

        # isochron and spectra data
        self.ClNormalIsochron: list = kwargs.pop("ClNormalIsochron", [])
        self.ClInverseIsochron: list = kwargs.pop("ClInverseIsochron", [])
        self.ClKIsochron: list = kwargs.pop("ClKIsochron", [])
        self.AtmNormalIsochron: list = kwargs.pop("AtmNormalIsochron", [])
        self.AtmInverseIsochron: list = kwargs.pop("AtmInverseIsochron", [])
        self.ThreeDIsochron: list = kwargs.pop("ThreeDimIsochron", [])
        self.PlateauAges: list = kwargs.pop("PlateauAges", [])
        self.TotalFusionAge: list = kwargs.pop("TotalFusionAge", [])
        self.SpectraLines: list = kwargs.pop("SpectraLines", [])

        self.Ar40RPercentage: list = kwargs.pop("Ar40RPercentage", [])
        self.Ar39KPercentage: list = kwargs.pop("Ar39KPercentage", [])


class SampleInfo:
    def __init__(self, **kwargs):
        self.SampleName: str = kwargs.pop("SampleName", "")
        self.ExperimentName: str = kwargs.pop("ExperimentName", "")
        self.SampleLocation: str = kwargs.pop("SampleLocation", "")
        self.SampleRock: str = kwargs.pop("SampleRock", "")
        self.SampleMineral: str = kwargs.pop("SampleMineral", "")
        self.SampleGrainSize: str = kwargs.pop("SampleGrainSize", "")
        self.SampleGrainMesh: str = kwargs.pop("SampleGrainMesh", "")
        self.ReactorProject: str = kwargs.pop("ReactorProject", "")
        self.SampleOwner: str = kwargs.pop("SampleOwner", "")
        self.ExperimentAnalyst: str = kwargs.pop("ExperimentAnalyst", "")
        self.Instrument: str = kwargs.pop("Instrument", "")
        self.LaboratoryName: str = kwargs.pop("LaboratoryName", "")
        self.LaboratoryInfo: str = kwargs.pop("LaboratoryInfo", "")
        self.SampleDescription: str = kwargs.pop("SampleDescription", "")
        self.ReactorLocation: str = kwargs.pop("ReactorLocation", "")


class Sample(IntermediateData, CalcParams, IrraParams, SampleInfo):
    def __init__(self, **kwargs):
        """
        Create a sample parent instance.

        parameters
        ----------
        SampleID: int, default: None
            unique number of every instance, it is defined based on the datetime the instance was created.

        SampleName: str, default: None
            sample name.

        SampleType: str, default: None
            sample type.
            -Unknown sample
            -Air
            -Flux monitor / Standard sample

        SampleDescription: str, default: None
            the description of sample

        ExperimentName: str, default: None
            experiment name

        ExperimentAnalyst: str, default: None
            experiment analyst

        Instrument: str, default: None
            instrument name

        LaboratoryName: str, default: None
            laboratory name

        LaboratoryInfo: str, default: None
            laboratory information
        """
        IntermediateData.__init__(self, **kwargs)
        SampleInfo.__init__(self, **kwargs)
        CalcParams.__init__(self, **kwargs)
        IrraParams.__init__(self, **kwargs)

        self.SampleID: int = int((datetime.datetime.now() - datetime.datetime(2000, 1, 1)).total_seconds() * 100)
        self.AnalysisDate: datetime.datetime = datetime.datetime.now()
        self.ExperimentType: str = kwargs.pop("ExperimentType", "")  # laser or crush
        # Sample Type: UnkSample -> Unknown Sample, Monitor -> Monitor Sample, AirSample -> Air Sample
        self.SampleType: str = kwargs.pop("SampleType", "")

        # attach files
        self.RawFilePath: str = kwargs.pop("RawFilePath", "")
        self.FilteredFilePath: str = kwargs.pop("FilteredFilePath", "")
        self.AgeFilePath: str = kwargs.pop("FilteredFilePath", "")

        """Monitor Sample"""
        self.MonitorName: str = kwargs.pop("MonitorName", "")
        self.MonitorAge: float = kwargs.pop("MonitorAge", 0)
        self.MonitorAgeError: float = kwargs.pop("MonitorAgeError", 0)
        self.TotalF: float = kwargs.pop("TotalF", 0)
        self.TotalFError: float = kwargs.pop("TotalFError", 0)
        self.MonitorJValue: float = kwargs.pop("MonitorJValue", 0)
        self.MonitorJValueError: float = kwargs.pop("MonitorJValueError", 0)

        """Air Sample"""
        self.AirMDF: float = kwargs.pop("AirMDF", 0)  # 40Ara / 36Ara
        self.AirMDFError: float = kwargs.pop("AirMDFError", 0)
        self.AirRatio: float = kwargs.pop("AirRatio", 0)  # 40Ara / 36Ara
        self.AirRatioError: float = kwargs.pop("AirRatioError", 0)

        # isotopes value
        self.MSequenceList: list = kwargs.pop("MSequenceList", [])  # Measurement sequences name
        self.MStepsList: list = kwargs.pop("MStepsList", [])  # Steps info, e.g., crush number, temperature
        self.MDateTimeList: list = kwargs.pop("MDateTimeList", [])  # [day, mouth, year, hour, min]
        self.BSequenceList: list = kwargs.pop("BSequenceList", [])  # Blank sequences name
        self.BStepsList: list = kwargs.pop("BStepsList", [])  # Blank steps labels, e.g., B, Blank
        # measurement value lists
        self.Ar36MList: list = kwargs.pop("Ar36MList", [])
        self.Ar37MList: list = kwargs.pop("Ar37MList", [])
        self.Ar38MList: list = kwargs.pop("Ar38MList", [])
        self.Ar39MList: list = kwargs.pop("Ar39MList", [])
        self.Ar40MList: list = kwargs.pop("Ar40MList", [])
        self.Ar36MErrorList: list = kwargs.pop("Ar36MErrorList", [])
        self.Ar37MErrorList: list = kwargs.pop("Ar37MErrorList", [])
        self.Ar38MErrorList: list = kwargs.pop("Ar38MErrorList", [])
        self.Ar39MErrorList: list = kwargs.pop("Ar39MErrorList", [])
        self.Ar40MErrorList: list = kwargs.pop("Ar40MErrorList", [])
        # blank value lists
        self.Ar36BList: list = kwargs.pop("Ar36BList", [])
        self.Ar37BList: list = kwargs.pop("Ar37BList", [])
        self.Ar38BList: list = kwargs.pop("Ar38BList", [])
        self.Ar39BList: list = kwargs.pop("Ar39BList", [])
        self.Ar40BList: list = kwargs.pop("Ar40BList", [])
        self.Ar36BErrorList: list = kwargs.pop("Ar36BErrorList", [])
        self.Ar37BErrorList: list = kwargs.pop("Ar37BErrorList", [])
        self.Ar38BErrorList: list = kwargs.pop("Ar38BErrorList", [])
        self.Ar39BErrorList: list = kwargs.pop("Ar39BErrorList", [])
        self.Ar40BErrorList: list = kwargs.pop("Ar40BErrorList", [])

        self.IsochronSelectedPoints: list = kwargs.pop("IsochronSelectedPoints", [])

    def save(self, user_path: str = ""):
        """
        Save the instance.

        Notes
        -----
        ab: adding to the last of the file if the filename has existed.
        wb: replacing of the present file.
        SampleID is unique for every instance.
        """
        type_suffix = "unksmp" if self.SampleType == "Unknown Sample" \
            else "airsmp" if self.SampleType == "Air Sample" \
            else "monsmp" if self.SampleType == "Monitor Sample" \
            else "smp"
        if not user_path:
            here = os.path.dirname(__file__)
            if not os.path.exists(here + '\\save'):
                os.mkdir(here + '\\save')
            _path = here + '\\save\\{}.{}'.format(str(self.SampleName), type_suffix)
        else:
            if user_path.split(".")[-1] != type_suffix:
                return
            else:
                _path = user_path
        _n = 0
        while os.path.exists(_path):
            # rename if current sample name have already existed
            # whereas if the file actually have same ID with present instance, rename is prohibited
            with open(_path, 'rb') as f:
                res = pickle.load(f)
            if res.SampleID == self.SampleID:
                break
            else:
                _n = _n + 1
                _path = here + '\\save\\{}.{}.{}'.format(str(self.SampleName), _n, type_suffix)
                # print('auto rename')
        with open(_path, 'wb') as f:
            f.write(pickle.dumps(self))
        return _path

    def get_data(self, key: str, returnRelative=False):
        return self.__dict__[key]

    def get_params(self):
        k = {}
        for key, value in self.__dict__.items():
            if key in list(CalcParams().__dict__.keys()) + list(IrraParams().__dict__.keys()):
                k[key] = value
        return k

    def get_calc_params(self):
        k = {}
        for key, value in self.__dict__.items():
            if key in list(CalcParams().__dict__.keys()):
                k[key] = value
        return k

    def get_irra_params(self):
        k = {}
        for key, value in self.__dict__.items():
            if key in list(IrraParams().__dict__.keys()):
                k[key] = value
        return k

    def get_sampleInfo_params(self):
        k = {}
        for key, value in self.__dict__.items():
            if key in list(SampleInfo().__dict__.keys()):
                k[key] = value
        return k

    def get_intermediate_data(self):
        k = {}
        for key, value in self.__dict__.items():
            if key in list(IntermediateData().__dict__.keys()):
                k[key] = value
        return k


class UnkSample(Sample):
    def __init__(self, **kwargs):
        """
        Create a sample instance.

        parameters
        ----------
        Calculation Params: float or bool, default: constants
            user define or inherit from the default.

        Attached files: str
            the file path user input.
        """
        super(UnkSample, self).__init__(
            SampleType=kwargs.pop("SampleType", "Unknown Sample"), **kwargs)


class MonitorSample(Sample):
    def __init__(self, **kwargs):
        """
        Create a sample instance.

        parameters
        ----------
        Sample Type: Monitor Sample
        """
        super(MonitorSample, self).__init__(
            SampleType=kwargs.pop("SampleType", "Monitor Sample"), **kwargs)


class AirSample(Sample):
    def __init__(self, **kwargs):
        """
        Create a sample instance.

        parameters
        ----------
        Sample Type: AirSample
        """
        super(AirSample, self).__init__(
            SampleType=kwargs.pop("SampleType", "Air Sample"), **kwargs)
