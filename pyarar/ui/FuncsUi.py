#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : FuncsUi.py
# @Author : Yang Wu
# @Date   : 2022/1/21
# @Email  : wuy@cug.edu.cn
import re
import sys
import traceback
from copy import deepcopy
from math import exp, log, atan, tan, cos, sin
from math import pi as _pi

from PyQt5.QtCore import Qt, pyqtSignal, QSize, QRect, QEvent, QPoint
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFontMetrics, QIcon, QKeyEvent, QKeySequence, QMouseEvent, \
    QCursor, QCloseEvent
from PyQt5.QtWidgets import QTreeView, QDialog, QTableWidgetItem, QFrame, QAbstractItemView, QApplication, QWidget, \
    QMessageBox, QMainWindow, QMdiSubWindow, QTableWidget, QPushButton, QLabel, QComboBox, QMenu, QAction
from matplotlib import patches

from matplotlib.backend_bases import MouseEvent, ResizeEvent

from pyarar.params import ParamsInfo
from pyarar.ui import untitledTable, untitledFigure, untiltedDialog
from pyarar.ui import UI_NewFileTools
from pyarar.sample import Sample, UnkSample, AirSample, MonitorSample
from pyarar.ui.settings import UiDefaultSetting, NewSettings

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.ticker as ticker


class Canvas(FigureCanvas):
    canvasClickedSignal: pyqtSignal = pyqtSignal(MouseEvent)

    def __init__(self, contents=None, isIsochron=False, isSpectra=False, **kwargs):
        self.dpi = kwargs.pop("canvasDpi", 600)
        fig: Figure = Figure(dpi=self.dpi, constrained_layout=True)
        fig.clear()
        super(Canvas, self).__init__(figure=fig)
        self.axes = fig.subplots()
        # self.dpi = fig.get_dpi()
        self.selected_points = {}
        self.unselected_points = {}

        self.xLimits = kwargs.pop("canvasXLimits", (0, 0))
        self.yLimits = kwargs.pop("canvasYLimits", (0, 0))

        self.showEllipse = kwargs.pop("showEllipse", True)
        self.showScatterLabel = kwargs.pop("showScatterLabel", False)
        self.scatter_size = kwargs.pop("canvasScatterSize", 20)
        self.line_width = kwargs.pop("canvasLineWidth", 2)

        self.scatter_color_1 = kwargs.pop("canvasScatterColor1", "Red")
        self.scatter_color_2 = kwargs.pop("canvasScatterColor2", "Blue")
        self.line_color = kwargs.pop("canvasLineColor", "r")
        self.line_style = kwargs.pop("canvasLineStyle", "solid")

        self.title_font = kwargs.pop("canvasTitleFont", UiDefaultSetting().title_font)
        font_dict = {
            "family": self.title_font.family(), "size": self.title_font.pointSize(),
            "weight": self.title_font.weight(),
            "style": ["normal", "italic", "oblique"][self.title_font.style()]
        }
        self.axes.set_title(kwargs.pop("canvasTitle", "No Title"), fontdict=font_dict)
        self.label_font = kwargs.pop("canvasLabelFont", UiDefaultSetting().label_font)
        font_dict = {
            "family": self.label_font.family(), "size": self.label_font.pointSize(),
            "weight": self.label_font.weight(),
            "style": ["normal", "italic", "oblique"][self.label_font.style()]
        }
        self.axes.set_xlabel(kwargs.pop("canvasXLabel", "No X label"), fontdict=font_dict)
        self.axes.set_ylabel(kwargs.pop("canvasYLabel", "No Y label"), fontdict=font_dict)

        if self.xLimits != (0, 0):
            self.axes.set_xlim(left=self.xLimits[0], right=self.xLimits[1])
        if self.yLimits != (0, 0):
            self.axes.set_ylim(bottom=self.yLimits[0], top=self.yLimits[1])

        (x_min, x_max) = self.axes.get_xlim()
        (y_min, y_max) = self.axes.get_ylim()
        x_ratio = abs(x_max - x_min) / self.get_width_height()[0]  # scale versus pixel
        y_ratio = abs(y_max - y_min) / self.get_width_height()[1]  # scale versus pixel
        scatter_radius_pixel = self.scatter_size ** 0.5 * self.dpi / 72 / 2
        self.adjust_ratio = kwargs.pop("canvasClickAdjustRatio", 0.8)
        self.x_scatter_radius = scatter_radius_pixel * x_ratio * self.adjust_ratio
        self.y_scatter_radius = scatter_radius_pixel * y_ratio * self.adjust_ratio

        # start and end at the x_lim
        self.axes.set_xmargin(0)
        self.axes.set_ymargin(0)

        self.axis_visible = kwargs.pop("canvasAxisVisible", True)
        self.axes.xaxis.set_visible(self.axis_visible)
        self.axes.yaxis.set_visible(self.axis_visible)

        self.title = kwargs.pop("subWindowTitle", "")
        self.mpl_connect('resize_event', lambda event: self.canvasResized(event))
        self.mpl_connect('button_press_event', lambda event: self.canvasClickedSignal.emit(event))

        self.contents = contents
        if contents:
            if isIsochron:
                [x, sx, y, sy, r, b, m, points] = contents
                self.plotIsochron(x, sx, y, sy, r, b, m, points)
            elif isSpectra:
                [x, y1, y2] = contents
                self.plotSpectra(x, y1, y2)
            else:
                pass

        self.ticksLabelSize = kwargs.pop("ticksLabelSize", 10)
        self.ticksDirection = kwargs.pop("ticksDirection", "in")
        self.axes.tick_params(
            axis="both", which="both", labelsize=self.ticksLabelSize, direction=self.ticksDirection)
        self.xTicksLocator = kwargs.pop("xTicksLocator", ("default", "default"))
        self.yTicksLocator = kwargs.pop("yTicksLocator", ("default", "default"))

        def _showTicks(axis, value, ticks="major"):
            try:
                value = float(value)
            except ValueError:
                return
            if value != 0:
                getattr(axis, "set_{}_locator".format(ticks))(ticker.MultipleLocator(value))
            else:
                getattr(axis, "set_{}_locator".format(ticks))(ticker.NullLocator())
        _showTicks(self.axes.xaxis, self.xTicksLocator[0], "minor")
        _showTicks(self.axes.xaxis, self.xTicksLocator[1], "major")
        _showTicks(self.axes.yaxis, self.yTicksLocator[0], "minor")
        _showTicks(self.axes.yaxis, self.yTicksLocator[1], "major")

    def canvasResized(self, event: ResizeEvent):
        (x_min, x_max) = self.axes.get_xlim()
        (y_min, y_max) = self.axes.get_ylim()
        x_ratio = abs(x_max - x_min) / event.width  # scale versus pixel
        y_ratio = abs(y_max - y_min) / event.height  # scale versus pixel
        scatter_radius_pixel = self.scatter_size ** 0.5 * self.dpi / 72 / 2
        self.x_scatter_radius = scatter_radius_pixel * x_ratio * self.adjust_ratio
        self.y_scatter_radius = scatter_radius_pixel * y_ratio * self.adjust_ratio

    def plotIsochron(self, x: list, sx: list, y: list, sy: list, rho: list,
                     b: float or int = None, m: float or int = None,
                     selectedPoints: list = None):
        for i in range(min([len(j) for j in [x, sx, y, sy, rho]])):
            """scatters"""
            if i in selectedPoints:
                self.axes.scatter(x[i], y[i], s=self.scatter_size, c=self.scatter_color_1)
                self.selected_points[i] = (x[i], y[i])
            else:
                self.axes.scatter(x[i], y[i], s=self.scatter_size, c=self.scatter_color_2)
                self.unselected_points[i] = (x[i], y[i])
            """scatter labels"""
            if self.showScatterLabel:
                self.axes.annotate(str(i + 1), xy=(x[i], y[i]), xytext=(5, 5), textcoords='offset points')
            """ellipses"""
            if self.showEllipse:
                plt_sfactor = 1
                ellipse_b_c = "r"
                ellipse_f_c = "none"
                ellipse_f = False if ellipse_f_c == 'none' or ellipse_f_c is None else True

                Qxx = (sx[i]) ** 2
                Qxy = sx[i] * sy[i] * rho[i]
                Qyy = (sy[i]) ** 2
                '''calculate the ellipse's short semi-axial and long semi-axial'''
                k = pow((Qxx - Qyy) ** 2 + 4 * Qxy ** 2, 0.5)
                Qee = (Qxx + Qyy + k) / 2
                Qff = (Qxx + Qyy - k) / 2
                e = pow(Qee, 0.5)  # long semi-axial
                f = pow(Qff, 0.5)  # short semi-axial
                phi_e = atan((Qee - Qxx) / Qxy) if Qxy != 0 else 0 if Qxx >= Qyy else _pi / 2  # radian

                if plt_sfactor == 1:
                    v = 2.279  # 68% confidence limit, 1 sigma
                elif plt_sfactor == 2:
                    v = 5.991  # 95% confidence limit, 2 sigma
                else:
                    v = 1
                ellipse_2 = patches.Ellipse((x[i], y[i]), e * pow(v, 0.5) * 2, f * pow(v, 0.5) * 2,
                                            angle=phi_e * 180 / _pi, edgecolor=ellipse_b_c, fill=ellipse_f,
                                            facecolor=ellipse_f_c)
                self.axes.add_patch(ellipse_2)
        """isochron line"""
        if b != "Null" and m != "Null":
            xlimit = self.axes.get_xlim()
            self.axes.plot([xlimit[0], xlimit[1]], [xlimit[0] * m + b, xlimit[1] * m + b],
                           color=self.line_color, linewidth=self.line_width,
                           linestyle=self.line_style)
        return self

    def plotSpectra(self, x: list, y1: list, y2: list):
        self.axes.plot(x, y1, x, y2, color=self.line_color, linewidth=self.line_width, linestyle=self.line_style)
        return self


class Table(QTableWidget):
    DialogErrorMassageSignal: pyqtSignal = pyqtSignal(str)
    TableCheckStateChangedSignal: pyqtSignal = pyqtSignal(list, str)

    def __init__(self, **kwargs):
        super(Table, self).__init__()
        self.setTextElideMode(Qt.ElideNone)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setObjectName("tableWidget")
        self.setColumnCount(0)
        self.setRowCount(0)
        self.horizontalHeader().setDefaultSectionSize(100)
        self.horizontalHeader().setMinimumSectionSize(30)

        # set column and row counts
        self.header = deepcopy(kwargs.pop("header", []))
        self.errorFactor = kwargs.pop("errorFactor", 1)
        self.isRelative = kwargs.pop("isRelative", True)
        self.stepLabel = kwargs.pop("stepLabel", None)
        self.headerFont = kwargs.pop("headerFont", UiDefaultSetting().header_font)
        self.headerBackGround = kwargs.pop("headerBackGround", UiDefaultSetting().color_darkblue)
        self.headerForeGround = kwargs.pop("headerForeGround", UiDefaultSetting().color_white)
        self.itemFont = kwargs.pop("itemFont", UiDefaultSetting().item_font)
        self.contents = kwargs.pop("contents", [])
        self.tableUid = kwargs.pop("tableUid", "")

        # set palette
        self.setPalette(kwargs.pop("tablePalette", UiDefaultSetting().palette))
        self.setAlternatingRowColors(True)

        # set frame
        self.setFrameShape(QFrame.NoFrame)
        self.setFocusPolicy(Qt.NoFocus)

        self.itemChanged.connect(
            lambda item: self.itemChangedEmitSignal(
                item, getattr(UiDefaultSetting(), f"{self.tableUid}Title", "default")))

        self.setHeader()
        self.writeTable()

    def setHeader(self, header=None):
        self.blockSignals(True)
        if header is not None:
            self.header = deepcopy(header)
        else:
            header = deepcopy(self.header)
        self.setColumnCount(len(header))
        if self.rowCount() < 1:
            self.setRowCount(1)
        for i in range(len(header)):
            if header[i] == UiDefaultSetting().headerLabel and self.stepLabel:
                header[i] = self.stepLabel
            if header[i] == UiDefaultSetting().error:
                header[i] = \
                    str(self.errorFactor) + "s" + "%" if self.isRelative else str(self.errorFactor) + "s"
        # set table horizontal header
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        for i in range(len(header)):
            item = QTableWidgetItem(header[i])
            item.setBackground(self.headerBackGround)
            item.setFont(self.headerFont)
            item.setForeground(self.headerForeGround)
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            self.setItem(0, i, item)
        self.blockSignals(False)

    def writeTable(self, contents: list = None):
        self.blockSignals(True)
        if contents is not None:
            self.contents = deepcopy(contents)
        try:
            self.clear()
            self.setHeader()
            self.setRowCount(max([len(i) for i in self.contents if i]) + 1)
            column_width = [(0, 25), (25, 50), (50, 75), (75, 100), (100, 125), (125, 150), (150, 175),
                            (175, 200), (200, 225), (225, 250), (250, 275), (275, 300), (300, 325),
                            (325, 350), (375, 400)]
            for row in range(1, self.rowCount()):
                for col in range(self.columnCount()):
                    try:
                        item = QTableWidgetItem(str(self.contents[col][row - 1]))
                        item.setFont(self.itemFont)
                        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        self.setItem(row, col, item)
                    except Exception:
                        self.DialogErrorMassageSignal.emit(traceback.format_exc())
            """adjust check state"""
            if self.tableUid in \
                    ["totalResultsTable", "atmNormalTable", "atmInverseTable",
                     "clNormalTable", "clInverseTable", "clKTable"]:
                for row in range(1, self.rowCount()):
                    checkState = Qt.Checked if row - 1 in self.contents[-1] else Qt.Unchecked
                    self.item(row, 2).setCheckState(checkState)
                k = list(set([self.item(row, 2).checkState() for row in range(1, self.rowCount())]))
                checkState = k[0] if len(k) == 1 else Qt.PartiallyChecked
                self.item(0, 2).setCheckState(checkState)
            """adjust column width"""
            for col in range(self.columnCount()):
                header_length = QFontMetrics(self.headerFont).width(str(self.item(0, col).text()))
                str_list = self.contents[col]
                length_list = [len(str(_i)) for _i in str_list]
                max_str_length = max(QFontMetrics(self.itemFont).width(
                    str(str_list[length_list.index(max(length_list))])), header_length)
                for i in column_width:
                    if i[0] <= max_str_length * 1.1 < i[1]:
                        self.setColumnWidth(col, i[1])
                        break
        except Exception:
            self.DialogErrorMassageSignal.emit(traceback.format_exc())
        self.blockSignals(False)

    def replaceTable(self):
        self.clear()
        self.setHeader()
        self.writeTable()

    def itemChangedEmitSignal(self, item: QTableWidgetItem, windowTitle: str):
        if windowTitle == "default":
            return
        self.blockSignals(True)
        if item.column() != 2:
            return
        if item.row() == 0:
            for row in range(1, self.rowCount()):
                checkState = Qt.Checked if item.checkState() == Qt.Checked else Qt.Unchecked
                self.item(row, 2).setCheckState(checkState)
        else:
            k = list(set([self.item(row, 2).checkState() for row in range(1, self.rowCount())]))
            checkState = k[0] if len(k) == 1 else Qt.PartiallyChecked
            self.item(0, 2).setCheckState(checkState)
            for i in self.selectedItems():
                if i.column() == item.column() and i.checkState() != item.checkState():
                    i.setCheckState(item.checkState())
        checkedList = [row - 1 for row in range(1, self.rowCount()) if self.item(row, 2).checkState() == Qt.Checked]
        self.blockSignals(False)
        self.TableCheckStateChangedSignal.emit(checkedList, windowTitle)

class TableDialog(QDialog, untitledTable.Ui_Dialog):
    DialogErrorMassageSignal = pyqtSignal(str)

    def __init__(self, **kwargs):
        super(TableDialog, self).__init__()
        self.setupUi(self)

        # set window information
        self.setWindowTitle(kwargs.pop("dialogTitle", "untitled"))
        self.setStatusTip(kwargs.pop("statusTip", "undefined"))
        self.dialogType = kwargs.pop("dialogType", "Table")
        self.dialogUid = kwargs.pop("dialogUid", "")
        
        self.tableWidget = Table(tableUid=self.dialogUid, **kwargs)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.tableWidget.DialogErrorMassageSignal.connect(
            lambda error: self.DialogErrorMassageSignal.emit(error))

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if not self.tableWidget.selectedRanges():
            return False
        selected_cells = [
            (i, j) for each_range in self.tableWidget.selectedRanges()
            for i in range(each_range.topRow(), each_range.topRow() + each_range.rowCount())
            for j in range(each_range.leftColumn(), each_range.leftColumn() + each_range.columnCount())]
        if event.key() == Qt.Key_Delete:
            for i in selected_cells:
                item = self.tableWidget.item(i[0], i[1])
                if item:
                    item.setText("")
        selected_cells_dict = {
            i: [j for j in selected_cells if j[0] == i] for i in list(set([k[0] for k in selected_cells]))}
        k = [[j[1] for j in i] for i in list(selected_cells_dict.values())]
        if k.count(k[0]) != len(k):
            error_text = "Irregular multiple selection regions cannot be copied"
            self.DialogErrorMassageSignal.emit(error_text)
            return False
        if event.matches(QKeySequence.StandardKey(9)):  # Copy = 9
            selected_items = []
            for row in sorted(selected_cells_dict):
                selected_items.append([])
                selected_cells_dict[row].sort(key=lambda i: i[1])
                for cell in selected_cells_dict[row]:
                    try:
                        item = self.tableWidget.item(cell[0], cell[1]).text()
                    except Exception:
                        item = ''
                    selected_items[-1].append(item)
            selected_str = change_list_str(selected_items)
            clipboard = QApplication.clipboard()
            clipboard.setText(selected_str)
        if event.matches(QKeySequence.Paste):
            text = QApplication.clipboard().text()
            paste_list = change_list_str(text)
            paste_items(self.tableWidget, paste_list,
                        min([i[0] for i in selected_cells]), min([i[1] for i in selected_cells]))


class FigureDialog(QDialog, untitledFigure.Ui_Dialog):
    DialogErrorMassageSignal = pyqtSignal(str)

    def __init__(self, **kwargs):
        super(FigureDialog, self).__init__()
        self.setupUi(self)

        self.contents = kwargs.pop("contents", None)

        # set window information
        self.setWindowTitle(kwargs.pop("dialogTitle", "untitled"))
        self.setStatusTip(kwargs.pop("statusTip", "undefined"))
        self.dialogType = kwargs.pop("dialogType", "Figure")
        self.dialogUid = kwargs.pop("dialogUid", "")

        self.canvasTitle = kwargs.pop("canvasTitle", "No title")
        self.canvasXLabel = kwargs.pop("canvasXLabel", "XLabel")
        self.canvasYLabel = kwargs.pop("canvasYLabel", "YLabel")
        self.scatterColor_1 = kwargs.pop("scatterColor_1", "Red")
        self.scatterColor_2 = kwargs.pop("scatterColor_2", "Blue")
        self.canvasLineColor = kwargs.pop("isochronColor", "Red")
        self.canvasDpi = kwargs.pop("canvasDpi", 100)
        self.canvasScatterSize = kwargs.pop("canvasScatterSize", 20)
        self.canvasLineWidth = kwargs.pop("canvasLineWidth", 2)
        self.canvasLineStyle = kwargs.pop("canvasLineStyle", "solid")
        self.isIsochron = kwargs.pop("isIsochron", False)
        self.isSpectra = kwargs.pop("isSpectra", False)
        self.showEllipse = kwargs.pop("showEllipse", True)
        self.showScatterLabel = kwargs.pop("showScatterLabel", False)
        self.canvasXLimits = kwargs.pop("canvasXLimits", (0, 0))
        self.canvasYLimits = kwargs.pop("canvasYLimits", (0, 0))
        self.canvasClickAdjustRatio = kwargs.pop("canvasClickAdjustRatio", 1)
        self.canvasAxisVisible = kwargs.pop("canvasAxisVisible", True)
        self.canvasTitleFont = UiDefaultSetting().title_font
        self.canvasLabelFont = UiDefaultSetting().label_font
        self.ticksLabelSize = kwargs.pop("ticksLabelSize", 10)
        self.ticksDirection = kwargs.pop("ticksDirection", "out")
        self.xTicksLocator = kwargs.pop("xTicksLocator", ("default", "default"))
        self.yTicksLocator = kwargs.pop("yTicksLocator", ("default", "default"))

        self.canvas = Canvas()

    def replaceCanvas(self, contents: list = None):
        if contents is not None:
            self.contents = contents
        try:
            canvas = Canvas(
                contents=self.contents, isIsochron=self.isIsochron, isSpectra=self.isSpectra,
                subWindowTitle=self.windowTitle(), canvasDpi=self.canvasDpi,
                canvasTitle=self.canvasTitle, canvasXLabel=self.canvasXLabel,
                canvasYLabel=self.canvasYLabel, showScatterLabel=self.showScatterLabel,
                canvasScatterSize=self.canvasScatterSize, canvasClickAdjustRatio=self.canvasClickAdjustRatio,
                canvasScatterColor1=self.scatterColor_1,
                canvasScatterColor2=self.scatterColor_2, showEllipse=self.showEllipse,
                canvasLineColor=self.canvasLineColor, canvasLineWidth=self.canvasLineWidth,
                canvasLineStyle=self.canvasLineStyle, canvasAxisVisible=self.canvasAxisVisible,
                canvasXLimits=self.canvasXLimits, canvasYLimits=self.canvasYLimits,
                canvasTitleFont=self.canvasTitleFont, canvasLabelFont=self.canvasLabelFont,
                ticksLabelSize=self.ticksLabelSize, ticksDirection=self.ticksDirection,
                xTicksLocator=self.xTicksLocator, yTicksLocator=self.yTicksLocator
            )
        except Exception:
            return
        else:
            try:
                self.verticalLayout.removeWidget(self.canvas)
            except Exception as e:
                pass
            else:
                self.canvas.deleteLater()
                self.canvas = canvas
                self.verticalLayout.addWidget(self.canvas)

    def keyPressEvent(self, event: QKeyEvent):
        print(event.key())
        if event.matches(QKeySequence.StandardKey(9)):  # Copy = 9
            pass


class NewFileToolsDialog(QDialog, UI_NewFileTools.Ui_Dialog):
    SignalDragMove = pyqtSignal(tuple)
    SignalButtonAddDelClicked = pyqtSignal(bool)
    SignalButtonRunClicked = pyqtSignal(bool)
    SignalButtonCloseClicked = pyqtSignal(bool)
    SignalButtonDefineClicked = pyqtSignal(str)

    def __init__(self):
        super(NewFileToolsDialog, self).__init__()
        self.setupUi(self)
        self.isDragging = False
        self.pressPos = (0, 0)
        self.setMouseTracking(True)
        self.widgetsRanges = []
        for i in self.findChildren((QComboBox, QLabel, QPushButton)):
            i.setMouseTracking(True)
            self.widgetsRanges.append(
                QRect(i.geometry().x(), i.geometry().top(),
                      i.geometry().width(), i.geometry().height()))

        self.comboBox.addItems(["Normal Isochron", "Inverse Isochron", "Total Results"])

        self.pushButton_add.clicked.connect(lambda: self.SignalButtonAddDelClicked.emit(True))
        self.pushButton_del.clicked.connect(lambda: self.SignalButtonAddDelClicked.emit(False))
        self.pushButton_run.clicked.connect(lambda: self.SignalButtonRunClicked.emit(True))
        self.pushButton_close.clicked.connect(lambda: self.SignalButtonCloseClicked.emit(True))
        self.pushButton_define.clicked.connect(
            lambda: self.SignalButtonDefineClicked.emit(self.comboBox.currentText()))

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        self.setCursor(Qt.SizeAllCursor)
        for i in self.widgetsRanges:
            if i.contains(a0.x(), a0.y()):
                self.setCursor(Qt.ArrowCursor)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        self.isDragging = True
        self.pressPos = (a0.x(), a0.y())
        for i in self.findChildren((QComboBox, QLabel, QPushButton)):
            if i.geometry().contains(a0.x(), a0.y()):
                self.isDragging = False

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        if self.isDragging:
            return self.SignalDragMove.emit(
                (int(a0.x() - self.pressPos[0]), int(a0.y() - self.pressPos[1])))


class InputTableDialog(TableDialog):
    def __init__(self):
        super(InputTableDialog, self).__init__()
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHeader([""] * self.tableWidget.columnCount())

        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(
            lambda pos: self.response(pos.x(), pos.y()))
        
        # right mouse menu
        menu_texts = MENU_CONTEXTS
        self.table_menu = QMenu(self.tableWidget)
        separatorAt = [0, 5, 10, 15, 18, 21, 24, 27, 30]
        self.actions = []
        for i in range(len(menu_texts)):
            self.createAction(menu_texts[i], i)
            if i in separatorAt:
                self.table_menu.addSeparator()

    def createAction(self, text, n):
        action = QAction(text, self.table_menu)
        action.setCheckable(True)
        self.table_menu.addAction(action)
        self.actions.append(action)
        self.actions[n].triggered.connect(lambda: self.contextMenuClicked(text))

    def response(self, x, y):
        if y > self.tableWidget.rowHeight(0):
            return
        colWidth = [self.tableWidget.columnWidth(col)
                    for col in range(self.tableWidget.columnCount())]
        eachColYScale = [(sum(colWidth[:i]), sum(colWidth[:i]) + colWidth[i])
                         for i in range(len(colWidth))]
        for i in eachColYScale:
            if i[0] < x < i[1]:
                self.rightClickedColumn = eachColYScale.index(i)
                headers = [self.tableWidget.item(0, col) for col in range(self.tableWidget.columnCount())]
                headers = [i.text() for i in headers if not isinstance(i, type(None))]
                for action in self.table_menu.actions():
                    if action.text().split(": ")[0] == "Error":
                        continue
                    if action.text().split(": ")[0] in headers:
                        action.setChecked(True)
                self.table_menu.exec(QCursor.pos())
                break

    def contextMenuClicked(self, menu_text: str):
        try:
            self.tableWidget.item(0, self.rightClickedColumn).setText(
                menu_text.split(": ")[0]
            )
        except Exception:
            return

    def readContents(self):
        keys = [self.tableWidget.item(0, col).text()
                if not isinstance(self.tableWidget.item(0, col), type(None)) else ""
                for col in range(self.tableWidget.columnCount())]
        values = [[self.tableWidget.item(row, col).text()
                   if not isinstance(self.tableWidget.item(row, col), type(None)) else ""
                   for row in range(1, self.tableWidget.rowCount())]
                  for col in range(self.tableWidget.columnCount())]
        for key in keys:
            while keys.count(key) != 1 and key != "Error":
                values.pop(keys.index(key))
                keys.remove(key)
        toDeleteIndex = []
        for i in range(len(keys)):
            n = -1
            while keys[i] == "Error":
                if i + n < 0:
                    toDeleteIndex.append(i)
                    break
                last_key = keys[i + n]
                if "Error" not in last_key and "Ri" not in last_key:
                    keys[i] = last_key + "Error"
                elif "Ri" in last_key or "Error" in last_key:
                    toDeleteIndex.append(i)
                    break
                else:
                    n = n - 1
            if keys[i] == "":
                toDeleteIndex.append(i)
        toDeleteIndex.reverse()
        for i in toDeleteIndex:
            keys.pop(i)
            values.pop(i)
        if len(keys) != len(values):
            return "len(keys) != len(values)"
        try:
            return {keys[i]: [float(j) for j in values[i]] for i in range(len(keys))}
        except ValueError:
            return "could not convert all items to float"

    def setHeader(self, comboBoxText: str):
        header = [i.split(": ")[0] for i in HEADER_DICT[comboBoxText]]
        self.tableWidget.setHeader(header)


class UserInputDialog(QDialog, untiltedDialog.Ui_Dialog):
    def __init__(self, parent):
        super(UserInputDialog, self).__init__(parent)
        self.setupUi(self)
        self.radioButton.setChecked(True)

    def closeEvent(self, a0: QCloseEvent) -> None:
        a0.ignore()


def setTreeView(treeView: QTreeView, modelName: str):
    model = QStandardItemModel(treeView)
    model.setObjectName(modelName)
    treeView.setModel(model)


def addItemToTreeView(treeView: QTreeView, itemText: str, upperOrderName: str = None):
    item_1 = QStandardItem(itemText)
    if "Table" in itemText and treeView.objectName() == "treeView_2":
        item_1.setIcon(QIcon(UiDefaultSetting().tableIconPath))
    elif "Figure" in itemText and treeView.objectName() == "treeView_2":
        item_1.setIcon(QIcon(UiDefaultSetting().figureIconPath))
    if not upperOrderName:
        treeView.model().appendRow(item_1)
    else:
        items: [QStandardItemModel] = [treeView.model().item(i, 0) for i in range(treeView.model().rowCount())]
        for item in items:
            if item.text() == upperOrderName:
                if itemText not in [item.child(i).text() for i in range(item.rowCount())]:
                    item.appendRow(item_1)
                    treeView.expand(item.index())
                    return item_1.index()
                else:
                    print("The file with the same name has been opened")
                    return False


def delItemFromTreeView(treeView: QTreeView, itemText: str, upperOrderName: str = None):
    items: [QStandardItemModel] = \
        [treeView.model().item(i, 0) for i in range(treeView.model().rowCount())]
    for item in items:
        if item.text() == upperOrderName:
            for i in range(item.rowCount()):
                if item.child(i).text() == itemText:
                    item.removeRow(i)
                    treeView.expand(item.index())
                    return item.rowCount()


def getDialog(indexName, isTable=False, isFigure=False, isRelative=False, smp=None):
    """
    :return:
    """
    try:
        title = getattr(UiDefaultSetting(), f"{indexName}Title", "default")
        statusTip = getattr(UiDefaultSetting(), f"{indexName}StatusTip", "default")
        if isTable:
            header = getattr(UiDefaultSetting(), f"{indexName}Header", [])
            label = smp.ExperimentType if smp else None
            dialog: TableDialog = TableDialog(
                dialogUid=indexName, dialogTitle=title,
                statusTip=statusTip, header=header, errorFactor=1,
                isRelative=isRelative, stepLabel=label)
        elif isFigure:
            isIsochron = True if "Isochron" in title else False
            isSpectra = True if "Spectra" in title else False
            canvasTitle = getattr(UiDefaultSetting(), f"{indexName}CanvasTitle", None)
            canvasXLabel = getattr(UiDefaultSetting(), f"{indexName}CanvasXLabel", None)
            canvasYLabel = getattr(UiDefaultSetting(), f"{indexName}CanvasYLabel", None)
            canvasDpi = getattr(UiDefaultSetting(), f"{indexName}CanvasDpi", None)
            canvasScatterSize = getattr(UiDefaultSetting(), f"{indexName}CanvasScatterSize", None)
            canvasLineWidth = getattr(UiDefaultSetting(), f"{indexName}CanvasLineWidth", None)
            dialog: FigureDialog = FigureDialog(
                isIsochron=isIsochron, isSpectra=isSpectra, dialogUid=indexName,
                dialogTitle=title, statusTip=statusTip,
                canvasTitle=canvasTitle, canvasXLabel=canvasXLabel,
                canvasYLabel=canvasYLabel, canvasDpi=canvasDpi,
                canvasScatterSize=canvasScatterSize, canvasLineWidth=canvasLineWidth)
        else:
            return False
        if isTable or isFigure:
            return dialog
    except Exception:
        return traceback.format_exc()


def addSubWindow(mainWindow: QMainWindow, dialog: TableDialog or FigureDialog,
                 isTable: bool = False, isFigure: bool = False):
    bigSize = QSize(int(mainWindow.mdiArea.geometry().width() * 0.8),
                    int(mainWindow.mdiArea.geometry().height() * 0.8))
    xInc = int(mainWindow.mdiArea.width() / 50)
    yInc = int(mainWindow.mdiArea.height() / 50)
    currentSubWindow = mainWindow.mdiArea.activeSubWindow()
    subWindow = mainWindow.mdiArea.addSubWindow(dialog)
    subWindow.show()
    # set subWindowIcon
    if isTable:
        mainWindow.mdiArea.activeSubWindow().setWindowIcon(QIcon(UiDefaultSetting().tableIconPath))
    elif isFigure:
        mainWindow.mdiArea.activeSubWindow().setWindowIcon(QIcon(UiDefaultSetting().figureIconPath))
    # resize the window, mention that cannot set the geometry of the subWindow directly
    if not currentSubWindow:  # no subWindow, the first subWindow is added
        mainWindow.mdiArea.activeSubWindow().setGeometry(0, 0, bigSize.width(), bigSize.height())
    elif isTable:  # add tables
        tables = [i for i in mainWindow.mdiArea.subWindowList() if "Table" in i.windowTitle()]
        mainWindow.mdiArea.activeSubWindow().setGeometry(
            xInc * (len(tables) - 1), yInc * (len(tables) - 1), bigSize.width(), bigSize.height())
    elif isFigure:  # add figure
        figures = [i for i in mainWindow.mdiArea.subWindowList() if "Figure" in i.windowTitle()]
        mainWindow.mdiArea.activeSubWindow().setGeometry(
            xInc * (len(figures) - 1), yInc * (len(figures) - 1) + 5 * yInc, bigSize.width(), bigSize.height())
    return subWindow


def addSubWindowInfo(table: QTableWidget, dialog: TableDialog or FigureDialog):
    def _add_item(_table: QTableWidget, _key: str, _value: str):
        _table.setRowCount(_table.rowCount() + 1)
        item1 = QTableWidgetItem(_key)
        item2 = QTableWidgetItem(_value)
        item1.setFlags(item1.flags() & Qt.ItemIsEnabled)
        item1.setFont(UiDefaultSetting().ui_light_font)
        item2.setFont(UiDefaultSetting().ui_light_font)
        _table.setItem(_table.rowCount() - 1, 0, item1)
        _table.setItem(_table.rowCount() - 1, 1, item2)
    table.clear()
    table.setRowCount(0)
    if dialog.dialogType == "Table":
        """item"""
        tableItem = QTableWidgetItem("Item")
        tableItem.setFont(UiDefaultSetting().ui_bold_font)
        table.setRowCount(table.rowCount() + 1)
        table.setItem(table.rowCount() - 1, 0, tableItem)
        table.setSpan(table.rowCount() - 1, 0, 1, 2)
        _add_item(table, "Item Size", str(dialog.tableWidget.itemFont.pointSize()))
        _add_item(table, "Item Family", str(dialog.tableWidget.itemFont.family()))
        _add_item(table, "Item Bold", str(dialog.tableWidget.itemFont.bold()))
        _add_item(table, "Item Style", str(dialog.tableWidget.itemFont.pointSize()))
        _add_item(table, "Item Capitalization", str(dialog.tableWidget.itemFont.capitalization()))
        """header"""
        tableItem = QTableWidgetItem("Header")
        tableItem.setFont(UiDefaultSetting().ui_bold_font)
        table.setRowCount(table.rowCount() + 1)
        table.setItem(table.rowCount() - 1, 0, tableItem)
        table.setSpan(table.rowCount() - 1, 0, 1, 2)
        _add_item(table, "Header Size", str(dialog.tableWidget.headerFont.pointSize()))
        _add_item(table, "Header Family", str(dialog.tableWidget.headerFont.family()))
        _add_item(table, "Header Bold", str(dialog.tableWidget.headerFont.bold()))
        _add_item(table, "Header Style", str(dialog.tableWidget.headerFont.pointSize()))
        _add_item(table, "Header Capitalization", str(dialog.tableWidget.headerFont.capitalization()))
        p1, p2, p3, alpha = dialog.tableWidget.headerBackGround.getRgb()
        _add_item(table, "Header Background", "{}, {}, {}, {}".format(p1, p2, p3, alpha))
        p1, p2, p3, alpha = dialog.tableWidget.headerForeGround.getRgb()
        _add_item(table, "Header Foreground", "{}, {}, {}, {}".format(p1, p2, p3, alpha))
    elif dialog.dialogType == "Figure":
        """figure"""
        tableItem = QTableWidgetItem("Figure")
        tableItem.setFont(UiDefaultSetting().ui_bold_font)
        table.setRowCount(table.rowCount() + 1)
        table.setItem(table.rowCount() - 1, 0, tableItem)
        table.setSpan(table.rowCount() - 1, 0, 1, 2)
        _add_item(table, "Dpi", "{:d}".format(int(dialog.canvas.dpi)))
        """scatter"""
        tableItem = QTableWidgetItem("Scatter")
        tableItem.setFont(UiDefaultSetting().ui_bold_font)
        table.setRowCount(table.rowCount() + 1)
        table.setItem(table.rowCount() - 1, 0, tableItem)
        table.setSpan(table.rowCount() - 1, 0, 1, 2)
        _add_item(table, "Scatter Size", str(dialog.canvas.scatter_size))
        _add_item(table, "Scatter Color 1", str(dialog.canvas.scatter_color_1))
        _add_item(table, "Scatter Color 2", str(dialog.canvas.scatter_color_2))
        _add_item(table, "Show Ellipse", str(dialog.canvas.showEllipse))
        _add_item(table, "Show Scatter Label", str(dialog.canvas.showScatterLabel))
        """line"""
        tableItem = QTableWidgetItem("Line")
        tableItem.setFont(UiDefaultSetting().ui_bold_font)
        table.setRowCount(table.rowCount() + 1)
        table.setItem(table.rowCount() - 1, 0, tableItem)
        table.setSpan(table.rowCount() - 1, 0, 1, 2)
        _add_item(table, "Line Width", str(dialog.canvas.line_width))
        _add_item(table, "Line Style",
                  str(["none", "solid", "dashed", "dashdot", "dotted"].index(str(dialog.canvas.line_style))))
        _add_item(table, "Line Color", str(dialog.canvas.line_color))
        """axes"""
        tableItem = QTableWidgetItem("Axes")
        tableItem.setFont(UiDefaultSetting().ui_bold_font)
        table.setRowCount(table.rowCount() + 1)
        table.setItem(table.rowCount() - 1, 0, tableItem)
        table.setSpan(table.rowCount() - 1, 0, 1, 2)
        _add_item(table, "Visible", str(dialog.canvas.axis_visible))
        _add_item(table, "X Limits", "{:.4f}, {:.4f}".format(
            dialog.canvas.axes.get_xlim()[0], dialog.canvas.axes.get_xlim()[1]))
        _add_item(table, "X Ticks Locator", "{}, {}".format(
            dialog.canvas.yTicksLocator[1],
            dialog.canvas.xTicksLocator[1]))
        _add_item(table, "Y Limits", "{:.4f}, {:.4f}".format(
            dialog.canvas.axes.get_ylim()[0], dialog.canvas.axes.get_ylim()[1]))
        _add_item(table, "Y Ticks Locator", "{}, {}".format(
            dialog.canvas.yTicksLocator[0],
            dialog.canvas.yTicksLocator[1]))
        _add_item(table, "Click Adjust Ratio", str(dialog.canvas.adjust_ratio))
        _add_item(table, "Ticks Label Size", str(dialog.canvas.ticksLabelSize))
        _add_item(table, "Ticks Direction", str(dialog.canvas.ticksDirection))
        """title"""
        tableItem = QTableWidgetItem("Title")
        tableItem.setFont(UiDefaultSetting().ui_bold_font)
        table.setRowCount(table.rowCount() + 1)
        table.setItem(table.rowCount() - 1, 0, tableItem)
        table.setSpan(table.rowCount() - 1, 0, 1, 2)
        _add_item(table, "Title Text", str(dialog.canvas.axes.get_title()))
        _add_item(table, "Title PointSize", str(dialog.canvas.title_font.pointSize()))
        _add_item(table, "Title Family", str(dialog.canvas.title_font.family()))
        _add_item(table, "Title Weight", str(dialog.canvas.title_font.weight()))
        _add_item(table, "Title Style", str(dialog.canvas.title_font.style()))
        """Label"""
        tableItem = QTableWidgetItem("Label")
        tableItem.setFont(UiDefaultSetting().ui_bold_font)
        table.setRowCount(table.rowCount() + 1)
        table.setItem(table.rowCount() - 1, 0, tableItem)
        table.setSpan(table.rowCount() - 1, 0, 1, 2)
        _add_item(table, "X Label", str(dialog.canvas.axes.get_xlabel()))
        _add_item(table, "Y Label", str(dialog.canvas.axes.get_ylabel()))
        _add_item(table, "Label PointSize", str(dialog.canvas.label_font.pointSize()))
        _add_item(table, "Label Family", str(dialog.canvas.label_font.family()))
        _add_item(table, "Label Weight", str(dialog.canvas.label_font.weight()))
        _add_item(table, "Label Style", str(dialog.canvas.label_font.style()))
    else:
        pass


def getContents(smp, subWindowTitle):
    if smp and subWindowTitle == "mTable":
        contents = [
            [i + 1 for i in range(len(smp.MSequenceList))],
            smp.MSequenceList, smp.MStepsList, smp.Ar36MList, smp.Ar36MErrorList, smp.Ar37MList, smp.Ar37MErrorList,
            smp.Ar38MList, smp.Ar38MErrorList, smp.Ar39MList, smp.Ar39MErrorList, smp.Ar40MList, smp.Ar40MErrorList,
            [i[0] for i in smp.MDateTimeList], [i[1] for i in smp.MDateTimeList], [i[2] for i in smp.MDateTimeList],
            [i[3] for i in smp.MDateTimeList], [i[4] for i in smp.MDateTimeList]
        ]
    elif smp and subWindowTitle == "bTable":
        contents = [
            [i + 1 for i in range(len(smp.MSequenceList))],
            smp.MSequenceList, smp.BStepsList, smp.BSequenceList, smp.Ar36BList, smp.Ar36BErrorList,
            smp.Ar37BList, smp.Ar37BErrorList, smp.Ar38BList, smp.Ar38BErrorList,
            smp.Ar39BList, smp.Ar39BErrorList, smp.Ar40BList, smp.Ar40BErrorList
        ]
    elif smp and subWindowTitle == "degasTable":
        contents = [
            [i + 1 for i in range(len(smp.MSequenceList))],
            smp.MSequenceList, smp.MStepsList,
            smp.Ar36DegasCa, smp.Ar36DegasCaError, smp.Ar36DegasK, smp.Ar36DegasKError,
            smp.Ar36DegasCl, smp.Ar36DegasClError, smp.Ar36DegasAir, smp.Ar36DegasAirError,
            smp.Ar37DegasCa, smp.Ar37DegasCaError, smp.Ar37DegasK, smp.Ar37DegasKError,
            smp.Ar37DegasCl, smp.Ar37DegasClError, smp.Ar37DegasAir, smp.Ar37DegasAirError,
            smp.Ar38DegasCa, smp.Ar38DegasCaError, smp.Ar38DegasK, smp.Ar38DegasKError,
            smp.Ar38DegasCl, smp.Ar38DegasClError, smp.Ar38DegasAir, smp.Ar38DegasAirError,
            smp.Ar39DegasCa, smp.Ar39DegasCaError, smp.Ar39DegasK, smp.Ar39DegasKError,
            smp.Ar39DegasCl, smp.Ar39DegasClError, smp.Ar39DegasAir, smp.Ar39DegasAirError,
            smp.Ar40DegasCa, smp.Ar40DegasCaError, smp.Ar40DegasK, smp.Ar40DegasKError,
            smp.Ar40DegasCl, smp.Ar40DegasClError, smp.Ar40DegasAir, smp.Ar40DegasAirError,
            smp.Ar40DegasR, smp.Ar40DegasRError,
            smp.ApparentAge, smp.ApparentAgeInternalError, smp.KCaRatios, smp.KCaRatiosError,
            smp.KClRatios, smp.KClRatiosError, smp.CaClRatios, smp.CaClRatiosError
        ]
    elif smp and subWindowTitle == "totalResultsTable":
        contents = [
            [i + 1 for i in range(len(smp.MSequenceList))],
            smp.MSequenceList, smp.MStepsList,
            smp.Ar36DegasAir, smp.Ar36DegasAirError, smp.Ar37DegasCa, smp.Ar37DegasCaError,
            smp.Ar38DegasCl, smp.Ar38DegasClError, smp.Ar39DegasK, smp.Ar39DegasKError,
            smp.Ar40DegasR, smp.Ar40DegasRError,
            smp.FValues, smp.FValuesError,
            smp.ApparentAge, smp.ApparentAgeInternalError, smp.ApparentAgeAnalysisError,
            smp.ApparentAgeFullExternalError,
            smp.KCaRatios, smp.KCaRatiosError,
            smp.Ar40RPercentage, smp.Ar39KPercentage,
            smp.IsochronSelectedPoints
        ]
    elif smp and subWindowTitle == "atmNormalTable":
        contents = [
            [i + 1 for i in range(len(smp.MSequenceList))],
            smp.MSequenceList, smp.MStepsList, smp.AtmNormalIsochron[0], smp.AtmNormalIsochron[1],
            smp.AtmNormalIsochron[2], smp.AtmNormalIsochron[3], smp.AtmNormalIsochron[4],
            smp.IsochronSelectedPoints
        ]
    elif smp and subWindowTitle == "atmInverseTable":
        contents = [
            [i + 1 for i in range(len(smp.MSequenceList))],
            smp.MSequenceList, smp.MStepsList, smp.AtmInverseIsochron[0], smp.AtmInverseIsochron[1],
            smp.AtmInverseIsochron[2], smp.AtmInverseIsochron[3], smp.AtmInverseIsochron[4],
            smp.IsochronSelectedPoints
        ]
    elif smp and subWindowTitle == "clNormalTable":
        contents = [
            [i + 1 for i in range(len(smp.MSequenceList))],
            smp.MSequenceList, smp.MStepsList, smp.ClNormalIsochron[0], smp.ClNormalIsochron[1],
            smp.ClNormalIsochron[2], smp.ClNormalIsochron[3], smp.ClNormalIsochron[4],
            smp.IsochronSelectedPoints
        ]
    elif smp and subWindowTitle == "clInverseTable":
        contents = [
            [i + 1 for i in range(len(smp.MSequenceList))],
            smp.MSequenceList, smp.MStepsList, smp.ClInverseIsochron[0], smp.ClInverseIsochron[1],
            smp.ClInverseIsochron[2], smp.ClInverseIsochron[3], smp.ClInverseIsochron[4],
            smp.IsochronSelectedPoints
        ]
    elif smp and subWindowTitle == "clKTable":
        contents = [
            [i + 1 for i in range(len(smp.MSequenceList))],
            smp.MSequenceList, smp.MStepsList, smp.ClKIsochron[0], smp.ClKIsochron[1],
            smp.ClKIsochron[2], smp.ClKIsochron[3], smp.ClKIsochron[4],
            smp.IsochronSelectedPoints
        ]
    elif smp and subWindowTitle == "paramsTable":
        contents = [
            [i + 1 for i in range(len(smp.get_params()))],
            list(smp.get_params().keys()), list(smp.get_params().values()),
            [ParamsInfo().get_data()[i] for i in list(smp.get_params().keys())]
        ]
    elif smp and subWindowTitle == "atmNormalFigure":
        contents = [
            smp.AtmNormalIsochron[0], smp.AtmNormalIsochron[1],
            smp.AtmNormalIsochron[2], smp.AtmNormalIsochron[3],
            smp.AtmNormalIsochron[4],
            smp.AtmNormalIsochron[5][9], smp.AtmNormalIsochron[5][11],
            smp.IsochronSelectedPoints
        ]
    elif smp and subWindowTitle == "atmInverseFigure":
        contents = [
            smp.AtmInverseIsochron[0], smp.AtmInverseIsochron[1],
            smp.AtmInverseIsochron[2], smp.AtmInverseIsochron[3],
            smp.AtmInverseIsochron[4],
            smp.AtmInverseIsochron[5][9], smp.AtmInverseIsochron[5][11],
            smp.IsochronSelectedPoints
        ]
    elif smp and subWindowTitle == "clNormalFigure":
        contents = [
            smp.ClNormalIsochron[0], smp.ClNormalIsochron[1],
            smp.ClNormalIsochron[2], smp.ClNormalIsochron[3],
            smp.ClNormalIsochron[4],
            smp.ClNormalIsochron[5][9], smp.ClNormalIsochron[5][11],
            smp.IsochronSelectedPoints
        ]
    elif smp and subWindowTitle == "clInverseFigure":
        contents = [
            smp.ClInverseIsochron[0], smp.ClInverseIsochron[1],
            smp.ClInverseIsochron[2], smp.ClInverseIsochron[3],
            smp.ClInverseIsochron[4],
            smp.ClInverseIsochron[5][9], smp.ClInverseIsochron[5][11],
            smp.IsochronSelectedPoints
        ]
    elif smp and subWindowTitle == "clKFigure":
        contents = [
            smp.ClKIsochron[0], smp.ClKIsochron[1],
            smp.ClKIsochron[2], smp.ClKIsochron[3],
            smp.ClKIsochron[4],
            smp.ClKIsochron[5][9], smp.ClKIsochron[5][11],
            smp.IsochronSelectedPoints
        ]
    elif smp and subWindowTitle == "ageSpectraFigure":
        contents = [
            smp.SpectraLines[0], smp.SpectraLines[1], smp.SpectraLines[2]
        ]
    else:
        contents = []
    return contents

def getErrorPopupDialog(mainWindow: QMainWindow, error: str, checked: bool = True):
    if checked:
        QMessageBox.warning(mainWindow, "Error", error, QMessageBox.Yes)

def getUserInputDialog(mainWindow: QMainWindow, title: str, tip: str):
    dialog = UserInputDialog(mainWindow)
    dialog.exec()
    return 0 if dialog.radioButton.isChecked() else 1 if dialog.radioButton_2.isChecked() else 2

def change_list_str(a0):
    if isinstance(a0, list):
        line = ''
        for i in range(len(a0)):
            for j in range(len(a0[i])):
                try:
                    item = line + str(a0[i][j])
                except Exception as e:
                    item = line
                finally:
                    if j != len(a0[i]) - 1:
                        line = item + '\t'
                    else:
                        line = item + '\n'
        return line
    elif isinstance(a0, str):
        k = []
        lines = a0.split('\n')
        if lines[-1] == '':
            lines.pop(-1)
        for i in range(len(lines)):
            k.append([])
            for j in lines[i].split('\t'):
                try:
                    item = float(j)
                except Exception as e:
                    item = str(j)
                finally:
                    k[i].append(item)
        return k

def paste_items(table: QTableWidget, items: list, row: int, col: int):
    if not table.selectedRanges():
        return
    if row + len(items) > table.rowCount():
        table.setRowCount(row + len(items))
    if col + max([len(i) for i in items]) > table.columnCount():
        add_cols = col + max([len(i) for i in items]) - table.columnCount()
        table.setHeader([table.item(0, col).text() for col in range(table.columnCount())] +
                        [""] * add_cols)
    for i in range(len(items)):
        for j in range(len(items[i])):
            try:
                item = float(items[i][j])
            except Exception as e:
                try:
                    item = re.findall(r'-?\d+\.?\d*e?-?\d*?', str(items[i][j]))[0]
                except Exception as e:
                    item = items[i][j]
            finally:
                table.setItem(row + i, col + j, QTableWidgetItem(str(item)))


MEASURED_36AR = "Ar36M: Measured 36Ar"
MEASURED_37AR = "Ar37M: Measured 37Ar"
MEASURED_38AR = "Ar38M: Measured 38Ar"
MEASURED_39AR = "Ar39M: Measured 39Ar"
MEASURED_40AR = "Ar40M: Measured 40Ar"

BLANK_36AR = "Ar36B: Blank 36Ar"
BLANK_37AR = "Ar37B: Blank 37Ar"
BLANK_38AR = "Ar38B: Blank 38Ar"
BLANK_39AR = "Ar39B: Blank 39Ar"
BLANK_40AR = "Ar40B: Blank 40Ar"

ATM_36AR = "Ar36Atm: Atmospheric 36Ar"
CA_37AR = "Ar37Ca: Calcium 37Ar"
Cl_38AR = "Ar38Cl: Chlorine 38Ar"
K_39AR = "Ar39K: Potassium 39Ar"
R_40AR = "Ar40R: Radiogenic 40Ar"

RATIO_K39_ATM36 = "39Ar/36Ar: Normal Isochron X"
RATIO_RA40_ATM36 = "40Ar/36Ar: Normal Isochron Y"
NORMAL_R = "Ri_1: Normal Isochron Ri"

RATIO_K39_RA40 = "39Ar/40Ar: Inverse Isochron X"
RATIO_ATM36_RA40 = "36Ar/40Ar: Inverse Isochron Y"
INVERSE_R = "Ri_2: inverse Isochron Ri"

RATIO_K39_Cl38 = "39Ar/38Ar: Chlorine Normal Isochron X"
RATIO_RCl40_Cl38 = "40Ar/38Ar: Chlorine Normal Isochron Y"
Cl_NORMAL_R = "Ri_3: Cl Normal Isochron Ri"

RATIO_K39_RCl40 = "39Ar/40Ar(cl): Chlorine Inverse Isochron X"
RATIO_Cl38_RCl40 = "38Ar/40Ar: Chlorine Inverse Isochron Y"
Cl_INVERSE_R = "Ri_4: Cl Inverse Isochron Ri"

RATIO_RCl40_K39 = "40Ar/39Ar: Chlorine Third Isochron X"
RATIO_Cl38_K39 = "38Ar/39Ar: Chlorine Third Isochron Y"
Cl_Third_R = "Ri_5: Cl Third Isochron Ri"

CUMULATIVE_39AR = "Cum_39Ar: Cumulative 39Ar Released"
APPARENT_AGE = "Age: Apparent Age"

ERROR = "Error: 1 Sigma Error of the last Column"

MENU_CONTEXTS = [
    ERROR,
    MEASURED_36AR, MEASURED_37AR, MEASURED_38AR, MEASURED_39AR, MEASURED_40AR,
    BLANK_36AR, BLANK_37AR, BLANK_38AR, BLANK_39AR, BLANK_40AR,
    ATM_36AR, CA_37AR, Cl_38AR, K_39AR, R_40AR,
    RATIO_K39_ATM36, RATIO_RA40_ATM36, NORMAL_R,
    RATIO_K39_RA40, RATIO_ATM36_RA40, INVERSE_R,
    RATIO_K39_Cl38, RATIO_RCl40_Cl38, Cl_NORMAL_R,
    RATIO_K39_RCl40, RATIO_Cl38_RCl40, Cl_INVERSE_R,
    RATIO_RCl40_K39, RATIO_Cl38_K39, Cl_Third_R,
    CUMULATIVE_39AR, APPARENT_AGE
]

HEADER_DICT = {
    "Normal Isochron": [
        RATIO_K39_ATM36, ERROR, RATIO_RA40_ATM36, ERROR, NORMAL_R
    ],
    "Inverse Isochron": [
        RATIO_K39_RA40, ERROR, RATIO_ATM36_RA40, ERROR, INVERSE_R
    ],
    "Total Results": [
        ATM_36AR, ERROR, CA_37AR, ERROR, Cl_38AR, ERROR, K_39AR, ERROR, R_40AR, ERROR
    ]
}

HEADER_TO_SMP = {
    'Ar36M': 'Ar36MList', 'Ar36MError': 'Ar36MErrorList',
    'Ar37M': 'Ar37MList', 'Ar37MError': 'Ar37MErrorList',
    'Ar38M': 'Ar38MList', 'Ar38MError': 'Ar38MErrorList',
    'Ar39M': 'Ar39MList', 'Ar39MError': 'Ar39MErrorList',
    'Ar40M': 'Ar40MList', 'Ar40MError': 'Ar40MErrorList',
    'Ar36B': 'Ar36BList', 'Ar36BError': 'Ar36BErrorList',
    'Ar37B': 'Ar37BList', 'Ar37BError': 'Ar37BErrorList',
    'Ar38B': 'Ar38BList', 'Ar38BError': 'Ar38BErrorList',
    'Ar39B': 'Ar39BList', 'Ar39BError': 'Ar39BErrorList',
    'Ar40B': 'Ar40BList', 'Ar40BError': 'Ar40BErrorList',
    'Ar36Atm': 'Ar36DegasAir', 'Ar36AtmError': 'Ar36DegasAirError',
    'Ar37Ca': 'Ar37DegasCa', 'Ar37CaError': 'Ar37DegasCaError',
    'Ar38Cl': 'Ar38DegasCl', 'Ar38ClError': 'Ar38DegasClError',
    'Ar39K': 'Ar39DegasK', 'Ar39KError': 'Ar39DegasKError',
    'Ar40R': 'Ar40DegasR', 'Ar40RError': 'Ar40DegasRError',
    '39Ar/36Ar': 'AtmNormalIsochron', '39Ar/36ArError': 'AtmNormalIsochron', 
    '40Ar/36Ar': 'AtmNormalIsochron', '40Ar/36ArError': 'AtmNormalIsochron', 'Ri_1': 'AtmNormalIsochron',
    '39Ar/40Ar': 'AtmInverseIsochron', '39Ar/40ArError': 'AtmInverseIsochron', 
    '36Ar/40Ar': 'AtmInverseIsochron', '36Ar/40ArError': 'AtmInverseIsochron', 'Ri_2': 'AtmInverseIsochron',
    '39Ar/38Ar': 'ClNormalIsochron', '39Ar/38ArError': 'ClNormalIsochron', 
    '40Ar/38Ar': 'ClNormalIsochron', '40Ar/38ArError': 'ClNormalIsochron', 'Ri_3': 'ClNormalIsochron',
    '39Ar/40Ar(cl)': 'ClInverseIsochron', '39Ar/40Ar(cl)Error': 'ClInverseIsochron', 
    '38Ar/40Ar': 'ClInverseIsochron', '38Ar/40ArError': 'ClInverseIsochron', 'Ri_4': 'ClInverseIsochron',
    '40Ar/39Ar': 'ClKIsochron', '40Ar/39ArError': 'ClKIsochron', 
    '38Ar/39Ar': 'ClKIsochron', '38Ar/39ArError': 'ClKIsochron', 'Ri_5': 'ClKIsochron',
    'Cum_39Ar': 'Ar39KPercentage',
    'Age': 'ApparentAge', 'AgeError': 'ApparentAgeAnalysisError'}
