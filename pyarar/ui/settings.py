#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : settings.py
# @Author : Yang Wu
# @Date   : 2022/1/22
# @Email  : wuy@cug.edu.cn
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon

from pyarar.sample import Sample, UnkSample


class UiDefaultSetting:
    def __init__(self):
        self.color_white = QColor(255, 255, 255)
        self.color_lightblue = QColor(233, 245, 252)
        self.color_darkblue = QColor(10, 53, 79)
        
        self.palette = QPalette()
        self.palette.setColor(QPalette.Base, QColor(255, 255, 255))
        self.palette.setColor(QPalette.AlternateBase, QColor(233, 245, 252))
        
        self.header_font = QFont()
        self.header_font.setFamily("Microsoft YaHei UI")
        self.header_font.setBold(True)
        self.header_font.setPointSize(10)
        
        self.item_font = QFont()
        self.item_font.setFamily("Microsoft YaHei UI")
        self.item_font.setBold(False)
        self.item_font.setPointSize(10)
        
        self.label_font = QFont()
        self.label_font.setFamily("Microsoft YaHei UI")
        self.label_font.setBold(True)
        self.label_font.setPointSize(10)
        self.label_font.setStyle(QFont.Style(0))  # 0 for normal, 1 for italic, 2 for oblique
        
        self.title_font = QFont()
        self.title_font.setFamily("Microsoft YaHei UI")
        self.title_font.setBold(True)
        self.title_font.setPointSize(10)
        self.title_font.setStyle(QFont.Style(0))  # 0 for normal, 1 for italic, 2 for oblique
        
        self.ui_bold_font = QFont()
        self.ui_bold_font.setFamily("Microsoft YaHei UI")
        self.ui_bold_font.setBold(True)
        self.ui_bold_font.setPointSize(10)
        
        self.ui_light_font = QFont()
        self.ui_light_font.setFamily("Microsoft YaHei UI")
        self.ui_light_font.setBold(False)
        self.ui_light_font.setPointSize(8)
        
        self.tableIconPath = "C:\\Users\\Young\\Projects\\2021-12pyarar\\pyarar\\pyarar\\tools\\table_icon.jpg"
        self.figureIconPath = "C:\\Users\\Young\\Projects\\2021-12pyarar\\pyarar\\pyarar\\tools\\figure_icon.jpg"
        
        self.mTableTitle = "Intercept Table"
        self.bTableTitle = "Blank Table"
        self.degasTableTitle = "Degas Results Table"
        self.totalResultsTableTitle = "Total Results Table"
        self.atmNormalTableTitle = "Atm Normal Isochron Table"
        self.atmInverseTableTitle = "Atm Inverse Isochron Table"
        self.clNormalTableTitle = "Cl Normal Isochron Table"
        self.clInverseTableTitle = "Cl Inverse Isochron Table"
        self.clKTableTitle = "Cl K Isochron Table"
        
        self.paramsTableTitle = "Params Table"

        self.mTableStatusTip = "Intercept Table"
        self.bTableStatusTip = "Blank Table"
        self.degasTableStatusTip = "Degas Results Table"
        self.totalResultsTableStatusTip = "Total Results Table"
        self.atmNormalTableStatusTip = "Atm Normal Isochron Table"
        self.atmInverseTableStatusTip = "Atm Inverse Isochron Table"
        self.clNormalTableStatusTip = "Cl Normal Isochron Table"
        self.clInverseTableStatusTip = "Cl Inverse Isochron Table"
        self.clKTableStatusTip = "Cl K Isochron Table"

        self.paramsTableStatusTip = "Params Table"

        self.atmNormalFigureTitle = "Atm Normal Isochron Figure"
        self.atmNormalFigureStatusTip = "Atm Normal Isochron Figure"
        self.atmInverseFigureTitle = "Atm Inverse Isochron Figure"
        self.atmInverseFigureStatusTip = "Atm Inverse Isochron Figure"
        self.clNormalFigureTitle = "Cl Normal Isochron Figure"
        self.clNormalFigureStatusTip = "Cl Normal Isochron Figure"
        self.clInverseFigureTitle = "Cl Inverse Isochron Figure"
        self.clInverseFigureStatusTip = "Cl Inverse Isochron Figure"
        self.clKFigureTitle = "Cl-K Isochron Figure"
        self.clKFigureStatusTip = "Cl-K Isochron Figure"
        self.ageSpectraFigureTitle = "Age Spectra Figure"
        self.ageSpectraFigureStatusTip = "Age Spectra Figure"

        self.error = "error"
        self.headerLabel = "StepsLabel"
        self.mTableHeader = \
            ["", "Sequences", self.headerLabel,
             "36Ar", self.error, "37Ar", self.error, "38Ar", self.error, "39Ar", self.error, "40Ar", self.error,
             "Day", "Mouth", "Year", "Hour", "Min"]
        self.bTableHeader = \
            ["", "Sequences", self.headerLabel, "Blanks",
             "36Ar", self.error, "37Ar", self.error, "38Ar", self.error, "39Ar", self.error, "40Ar", self.error]
        self.degasTableHeader = \
            ["", "Sequences", self.headerLabel,
             "36ArCa", self.error, "36ArK", self.error, "36ArCl", self.error, "36ArAir", self.error,
             "37ArCa", self.error, "37ArK", self.error, "37ArCl", self.error, "37ArAir", self.error,
             "38ArCa", self.error, "38ArK", self.error, "38ArCl", self.error, "38ArAir", self.error,
             "39ArCa", self.error, "39ArK", self.error, "39ArCl", self.error, "39ArAir", self.error,
             "40ArCa", self.error, "40ArK", self.error, "40ArCl", self.error, "40ArAir", self.error,
             "40ArR", self.error,
             "Age", self.error, "K/Ca", self.error, "K/Cl", self.error, "Ca/Cl", self.error]
        self.totalResultsTableHeader =\
            ["", "Sequences", self.headerLabel,
             "36ArAir", self.error, "37ArCa", self.error,
             "38ArCl", self.error, "39ArK", self.error, "40ArR", self.error,
             "F Value", self.error, "Age", self.error, self.error, self.error,
             "K/Ca", self.error, "Ar40R%", "Ar39K%"]
        self.atmNormalTableHeader = \
            ["", "Sequences", self.headerLabel, "39ArK/36Ara", self.error, "40Ara+r/36Ara", self.error, "ri"]
        self.atmInverseTableHeader = \
            ["", "Sequences", self.headerLabel, "39ArK/40Ara+r", self.error, "36Ara/40Ara+r", self.error, "ri"]
        self.clNormalTableHeader = \
            ["", "Sequences", self.headerLabel, "39ArK/38ArCl", self.error, "40ArCl+r/38ArCl", self.error, "ri"]
        self.clInverseTableHeader = \
            ["", "Sequences", self.headerLabel, "39ArK/40ArCl+r", self.error, "38ArCl/40ArCl+r", self.error, "ri"]
        self.clKTableHeader = \
            ["", "Sequences", self.headerLabel, "40ArCl+r/39ArK", self.error, "38ArCl/39ArK", self.error, "ri"]

        self.paramsTableHeader = \
            ["Index", "Items", "Values", "Information"]

        self.atmNormalFigureCanvasTitle = "Atm Normal Isochron Figure"
        self.atmInverseFigureCanvasTitle = "Atm Inverse Isochron Figure"
        self.clNormalFigureCanvasTitle = "Cl Normal Isochron Figure"
        self.clInverseFigureCanvasTitle = "Cl Inverse Isochron Figure"
        self.clKFigureCanvasTitle = "Cl-K Isochron Figure"
        self.ageSpectraFigureCanvasTitle = "Age Spectra Figure"

        self.atmNormalFigureCanvasXLabel = r"$\ ^{39}$Ar$\ _{K}$ / $\ ^{36}$Ar$\ _{a}$"
        self.atmNormalFigureCanvasYLabel = r"$\ ^{40}$Ar$\ _{a+r}$ / $\ ^{36}$Ar$\ _{a}$"

        self.atmInverseFigureCanvasXLabel = r"$\ ^{39}$Ar$\ _{K}$ / $\ ^{40}$Ar$\ _{a+r}$"
        self.atmInverseFigureCanvasYLabel = r"$\ ^{36}$Ar$\ _{a}$ / $\ ^{40}$Ar$\ _{a+r}$"

        self.clNormalFigureCanvasXLabel = r"$\ ^{39}$Ar$\ _{K}$ / $\ ^{38}$Ar$\ _{Cl}$"
        self.clNormalFigureCanvasYLabel = r"$\ ^{40}$Ar$\ _{Cl+r}$ / $\ ^{38}$Ar$\ _{Cl}$"

        self.clInverseFigureCanvasXLabel = r"$\ ^{39}$Ar$\ _{K}$ / $\ ^{40}$Ar$\ _{Cl+r}$"
        self.clInverseFigureCanvasYLabel = r"$\ ^{38}$Ar$\ _{Cl}$ / $\ ^{40}$Ar$\ _{Cl+r}$"

        self.clKFigureCanvasXLabel = r"$\ ^{38}$Ar$\ _{Cl}$ / $\ ^{39}$Ar$\ _{K}$"
        self.clKFigureCanvasYLabel = r"$\ ^{40}$Ar$\ _{Cl+r}$ / $\ ^{39}$Ar$\ _{K}$"

        self.ageSpectraFigureCanvasXLabel = r"Cumulative$\ ^{39}$Ar released (%)"
        self.ageSpectraFigureCanvasYLabel = "Apparent age (Ma)"

        self.atmNormalFigureCanvasDpi = 100
        self.atmInverseFigureCanvasDpi = 100
        self.clNormalFigureCanvasDpi = 100
        self.clInverseFigureCanvasDpi = 100
        self.clKFigureCanvasDpi = 100
        self.ageSpectraFigureCanvasDpi = 100

        self.atmNormalFigureCanvasScatterSize = 20
        self.atmInverseFigureCanvasScatterSize = 20
        self.clNormalFigureCanvasScatterSize = 20
        self.clInverseFigureCanvasScatterSize = 20
        self.clKFigureCanvasScatterSize = 20
        self.ageSpectraFigureCanvasScatterSize = 20

        self.atmNormalFigureCanvasLineWidth = 2
        self.atmInverseFigureCanvasLineWidth = 2
        self.clNormalFigureCanvasLineWidth = 2
        self.clInverseFigureCanvasLineWidth = 2
        self.clKFigureCanvasLineWidth = 2
        self.ageSpectraFigureCanvasLineWidth = 1


class NewSettings(UiDefaultSetting):
    def __init__(self):
        super().__init__()
        pass
