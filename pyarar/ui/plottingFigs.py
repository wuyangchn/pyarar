#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : jvalueCalculation.py
# @Author : Yang Wu
# @Date   : 2021/5/20
# @Email  : wuy@cug.edu.cn
import os
import sys
import re

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtCore import QCoreApplication, Qt, pyqtSignal, QRegExp
from PyQt5.QtGui import QRegExpValidator, QKeyEvent, QKeySequence, QColor, QImage
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem, QHeaderView, QFileDialog, QColorDialog
from pyarar.ui import UI_PlotWindow
from pyarar.ui import UI_ParamSetting
from pyarar.ui import UI_AxisSetting
from pyarar.ui import jvalueCalcualtion
from pyarar.ui import ProFunctions

class SubWindowPlotting(QDialog, UI_PlotWindow.Ui_Plot):
    current_params: list = [0.01537305, 0.00007687, 298.56, 0.31, 5.530e-10, 0.048e-10, 2,
                            0, 0, 0.001, 100, 0, 0, 0]
    axis_setting: list = [10, 0, 0, 10, 0, 2, 0, {'scatter_size': 10, 'scatter_b_c': 'black', 'scatter_f_c': 'blue',
                                                  'show_random_pts': 0, 'random_points_num': 1500,
                                                  'line_w': 1, 'line_s': 'solid', 'line_c': 'red',
                                                  'ellipse_b_c': 'y', 'ellipse_f_c': 'none'}]
    input_format = ['Normal Isochron', 'Inverse Isochron', 'Degassing', 'Ages']
    input_errors = ['1 se abs', '2 se abs', '1 se%', '2 se%']
    plot_type = ['Normal Isochron', 'Inverse Isochron', 'Age spectra']
    plot_errors = ['1 se abs', '2 se abs']
    current_plot_data, last_input_data = {}, {}

    def __init__(self):
        super(SubWindowPlotting, self).__init__()
        self.setupUi(self)
        '''add items to combo boxes'''
        self.comboBox.addItems(self.input_format)
        self.comboBox_2.addItems(self.input_errors)
        self.comboBox_3.addItems(self.plot_type)
        self.comboBox_4.addItems(self.plot_errors)
        '''connecting slots'''
        self.comboBox.currentIndexChanged.connect(self.ipt_index_changed)
        self.ipt_index_changed()
        self.comboBox_4.currentIndexChanged.connect(self.plot)
        '''instantiating a canvas'''
        self.canvas = FigureCanvas(plt.Figure(dpi=100, constrained_layout=True))
        self.verticalLayout.addWidget(self.canvas)
        '''set table row count, changing header according to the combo box text'''
        self.tableWidget.setRowCount(50)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.comboBox.currentIndexChanged.connect(lambda index: self.show_header(index))
        self.show_header(self.comboBox.currentIndex())
        '''connecting slots to buttons'''
        self.pushButton_open.clicked.connect(self.open_data)
        self.pushButton_save.clicked.connect(self.save_data)
        self.pushButton_export.clicked.connect(self.export_fig)
        self.pushButton_copy.clicked.connect(self.copy_fig)
        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_plot.clicked.connect(self.plot)
        self.pushButton_pltdata.clicked.connect(self.exchange_data_display)
        self.pushButton_params.clicked.connect(self.show_params_dialog)
        self.pushButton_axis.clicked.connect(self.show_axis_dialog)

        '''instantiating a axis dialog'''
        self.dialog_axis_setting = DialogAxisSetting(self.axis_setting)
        self.axis_setting = self.dialog_axis_setting.buttom_apply_clicked()
        self.dialog_axis_setting.signal_axis_setting.connect(self.new_axis_received)
        '''instantiating a param setting dialog'''
        self.dialog_param_setting = DialogParamSetting(self.current_params)
        self.dialog_param_setting.signal_params.connect(self.new_params_received)

    def ipt_index_changed(self):
        if self.comboBox.currentIndex() == 3:
            self.comboBox_3.setCurrentIndex(2)
            self.comboBox_3.setDisabled(True)
        else:
            self.comboBox_3.setDisabled(False)

    def save_data(self):
        file_path, file_type = QFileDialog.getSaveFileName(self, 'Save as', os.getcwd(), 'json(*.json)')
        data = dict(self.get_current_display_data())
        data['params'] = self.current_params
        data['ipt_index'] = self.comboBox.currentIndex()
        data['ipt_error'] = self.comboBox_2.currentIndex()
        data['plt_index'] = self.comboBox_3.currentIndex()
        data['plt_error'] = self.comboBox_4.currentIndex()
        data['plt_setting'] = self.axis_setting
        ProFunctions.save_Json(file_path, 2, data)

    def open_data(self):
        file_path, file_type = QFileDialog.getOpenFileName(self, 'Save as', os.getcwd(), 'json(*.json)')
        if not file_path:
            return
        data = ProFunctions.read_file(file_path, 2)

        self.current_params = data.pop('params', self.current_params)
        self.dialog_param_setting = DialogParamSetting(self.current_params)
        self.dialog_param_setting.signal_params.connect(self.new_params_received)
        self.axis_setting = data.pop('plt_setting', self.axis_setting)
        self.dialog_axis_setting = DialogAxisSetting(self.axis_setting)
        self.dialog_axis_setting.signal_axis_setting.connect(self.new_axis_received)

        self.comboBox.setCurrentIndex(data.pop('ipt_index', 0))
        self.comboBox_2.setCurrentIndex(data.pop('ipt_error', 0))
        self.comboBox_3.setCurrentIndex(data.pop('plt_index', 0))
        self.comboBox_4.setCurrentIndex(data.pop('plt_error', 0))
        self.current_plot_data = {}
        if self.pushButton_pltdata.text() == 'Input Data':
            self.last_input_data = data
            self.exchange_data_display()
        else:
            self.show_data(data)

    def copy_fig(self):
        """
        copy current fig
        :return: None
        """
        path = os.path.dirname(__file__) + '/temporary_file.png'
        self.canvas.figure.savefig(path, transparent=True, dpi=1000)
        clipboard = QApplication.clipboard()
        clipboard.setImage(QImage(path))
        os.remove(path)

    def export_fig(self):
        types = ['Excel Files (*.xlsx)', 'JPG Files (*.jpg)', 'PNG Files (*.png)']
        export_files_path, export_files_type = QFileDialog.getSaveFileName(self, 'Export Fig', os.getcwd(),
                                                                           ';;'.join(types))
        if not export_files_path:
            return
        index = types.index(export_files_type)
        if index == 0:
            export_files_path, export_files_type = QFileDialog.getSaveFileName(self, 'Export Fig', os.getcwd(),
                                                                               "Excel Files (*.xlsx)")
            if self.comboBox_3.currentIndex() == 2:
                ProFunctions.export_xls_spectra(export_files_path, self.current_plot_data)
                return
            elif self.comboBox_3.currentIndex() == 0:
                label = ['Normal Isochron', '39ArK/36Ara', '40Ar(a+r)/36Ara']
            else:
                label = ['Inverse Isochron', '39ArK/40Ar(a+r)', '36Ara/40Ar(a+r)']
            ProFunctions.export_xls_isochron(export_files_path, self.current_plot_data, label=label)
        elif index == 1:
            self.canvas.figure.savefig(export_files_path, dpi=300)
        elif index == 2:
            self.canvas.figure.savefig(export_files_path, transparent=True, dpi=300)
        else:
            return

    def keyPressEvent(self, event: QKeyEvent):
        if event.matches(QKeySequence.StandardKey(9)):
            selected_items = self.get_selected_items()
            selected_str = self.change_list_str(selected_items)
            clipboard = QApplication.clipboard()
            clipboard.setText(selected_str)
        if event.matches(QKeySequence.StandardKey(10)):
            paste_str = QApplication.clipboard().text()
            paste_list = self.change_list_str(paste_str)
            self.paste_items(paste_list)
        if event.matches(QKeySequence.StandardKey(7)):
            rows, cols = self.get_selected_range()
            for i in rows:
                for j in cols:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str('')))

    def show_header(self, index: int):
        headers = [['39k/36a', 's39k/36a', '40a+r/36a', 's40a+r/36a', 'ri', '39Ar%'],
                   ['39k/40a+r', 's39k/40a+r', '36a/40a+r', 's36a/40a+r', 'ri', '39Ar%'],
                   ['40Ara+r', 's40Ara+r', '39Ark', 's39Ark', '36Ara', 's36Ara', '39Ar%'],
                   ['age', 'sage', '39Ar%', '4', '5']]
        self.tableWidget.setColumnCount(len(headers[index]))
        for i in range(len(headers[index])):
            self.tableWidget.setHorizontalHeaderItem(i, QTableWidgetItem(headers[index][i]))

    def get_selected_range(self):
        if not self.tableWidget.selectedRanges():
            return False, False
        top_row = self.tableWidget.selectedRanges()[0].topRow()
        row_count = self.tableWidget.selectedRanges()[0].rowCount()
        left_col = self.tableWidget.selectedRanges()[0].leftColumn()
        col_count = self.tableWidget.selectedRanges()[0].columnCount()
        selected_rows = [i for i in range(top_row, top_row + row_count)]
        selected_cols = [i for i in range(left_col, left_col + col_count)]
        return selected_rows, selected_cols

    def get_selected_items(self):
        selected_rows, selected_cols = self.get_selected_range()
        selected_items = []
        for row in selected_rows:
            selected_items.append([])
            for col in selected_cols:
                try:
                    item = self.tableWidget.item(row, col).text()
                except Exception as e:
                    item = ''
                finally:
                    selected_items[selected_rows.index(row)].append(item)
        return selected_items

    def paste_items(self, items: list):
        selected_rows, selected_cols = self.get_selected_range()
        if len(set([len(i) for i in items])) != 1 or not selected_rows or not selected_cols:
            return
        if len(selected_rows) == len(selected_cols) == 1 or (selected_rows[-1] - selected_rows[0] + 1 >= len(items) and
                                                             selected_cols[-1] - selected_cols[0] + 1 >= len(items[0])):
            if selected_rows[0] + len(items) > self.tableWidget.rowCount():
                self.tableWidget.setRowCount(selected_rows[0] + len(items))
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
                        self.tableWidget.setItem(selected_rows[0]+i, selected_cols[0]+j, QTableWidgetItem(str(item)))
        else:
            return

    @staticmethod
    def change_list_str(a0):
        if isinstance(a0, list):
            line = ''
            for i in a0:
                for j in i:
                    try:
                        item = line + str(j)
                    except Exception as e:
                        item = line
                    finally:
                        if i.index(j) != len(i) - 1:
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

    def exchange_data_display(self):
        current_display_data = self.get_current_display_data()
        if self.pushButton_pltdata.text() == 'Plot Data':
            self.comboBox.setDisabled(True)
            self.comboBox_2.setDisabled(True)
            self.comboBox_3.setDisabled(True)
            self.pushButton_plot.setDisabled(True)
            self.last_input_data = dict(current_display_data)  # copy dict
            self.pushButton_pltdata.setText('Input Data')
            self.show_data(self.current_plot_data)
        elif self.pushButton_pltdata.text() == 'Input Data':
            self.comboBox.setDisabled(False)
            self.comboBox_2.setDisabled(False)
            self.comboBox_3.setDisabled(False)
            self.pushButton_plot.setDisabled(False)
            self.pushButton_pltdata.setText('Plot Data')
            self.show_data(self.last_input_data)

    def get_current_display_data(self):
        current_display_data = {}
        for col in range(self.tableWidget.columnCount()):
            col_items = [self.tableWidget.item(row, col).text() if self.tableWidget.item(row, col) is not None else ''
                         for row in range(self.tableWidget.rowCount())]
            current_display_data[self.tableWidget.horizontalHeaderItem(col).text()] = col_items
        return current_display_data

    def show_data(self, data_dict: dict):
        keys = list(data_dict.keys())
        values = list(data_dict.values())
        for col in range(self.tableWidget.columnCount()):
            try:
                self.tableWidget.setHorizontalHeaderItem(col, QTableWidgetItem(keys[col]))
            except Exception as e:
                self.tableWidget.setHorizontalHeaderItem(col, QTableWidgetItem(''))
            for row in range(self.tableWidget.rowCount()):
                try:
                    self.tableWidget.setItem(row, col, QTableWidgetItem(str(values[col][row])))
                except Exception as e:
                    self.tableWidget.setItem(row, col, QTableWidgetItem(''))

    def show_params_dialog(self):
        self.dialog_param_setting.exec()

    def show_axis_dialog(self):
        self.dialog_axis_setting.exec()

    def new_params_received(self, a0: list):
        self.current_params = list(a0)  # copy params list
        self.plot()  # replot

    def new_axis_received(self, a0: list):
        self.axis_setting = list(a0)
        self.plot()  # replot

    def plot(self):
        if not self.pushButton_plot.isEnabled():
            return
        convergence = self.current_params[9]
        iteration = self.current_params[10]
        isYorkFit = True if self.current_params[8] == 0 else False
        isOLSFit = True if self.current_params[8] == 1 else False
        '''plot properties'''
        properties = dict(self.axis_setting[7])
        properties['isAuto'] = True if self.axis_setting[5] == 2 else False
        properties['ignoreLine'] = True if self.axis_setting[6] == 2 else False
        properties['showLabel'] = True if self.current_params[7] == 2 else False

        ipt_index = self.comboBox.currentIndex()
        sf_index = self.comboBox_2.currentIndex()
        plt_index = self.comboBox_3.currentIndex()
        plt_factor = 1 if self.comboBox_4.currentIndex() == 0 else 2
        j, sj = self.current_params[0], self.current_params[1]  # J value
        rsj = self.current_params[1] / self.current_params[0] * 100
        f, sf = self.current_params[4], self.current_params[5]  # decay constant
        rsf = self.current_params[5] / self.current_params[4] * 100

        cols = []
        for col in range(self.tableWidget.columnCount()):
            cols.append([])
            for row in range(self.tableWidget.rowCount()):
                try:
                    text = float(self.tableWidget.item(row, col).text())
                except (ValueError, AttributeError) as e:
                    continue
                else:
                    cols[col].append(text)
        num = min([len(i) if len(i) != 0 else 9999 for i in cols])
        if num == 9999:
            return
        if ipt_index == 0:
            '''Normal Isochron Input'''
            ar39ar36 = cols[0][0:num]; sar39ar36 = cols[1][0:num]
            ar40ar36 = cols[2][0:num]; sar40ar36 = cols[3][0:num]
            rho = cols[4][0:num]; ar39pct = cols[5][0:num]
            if sf_index == 2 or sf_index == 3:
                sar39ar36 = list(map(lambda i, rsi: i * rsi / 100, ar39ar36, sar39ar36))
                sar40ar36 = list(map(lambda i, rsi: i * rsi / 100, ar40ar36, sar40ar36))
            if sf_index == 1 or sf_index == 3:
                sar39ar36 = [i / 2 for i in sar39ar36]
                sar40ar36 = [i / 2 for i in sar40ar36]
            if not ar39pct:
                ar39pct = [100 / num] * num
            if not rho:
                rho = [0.995] * num  # rho is important, affecting the York-2 regression and shapes of ellipses
            if not sar39ar36:
                sar39ar36 = [0] * num
            if not sar40ar36:
                sar40ar36 = [0] * num
            if not ar39ar36 or not ar40ar36:
                return
            sf = 1
            if plt_index == 0:
                '''Normal isochron plot'''
                try:
                    if isYorkFit:
                        k = ProFunctions.isochron_age(ar39ar36, sar39ar36, ar40ar36, sar40ar36, rho,
                                                      j, rsj, f, rsf, isNormal=True, statistics=True,
                                                      convergence=convergence, iteration=iteration)
                    elif isOLSFit:
                        k = ProFunctions.isochron_age_ols(ar39ar36, ar40ar36, j, rsj, f, rsf, isNormal=True)
                    else:
                        raise ValueError
                except Exception as e:
                    print('Error in fitting: %s' % str(e))
                    canvas = ProFunctions.get_isochron(ar39ar36, sar39ar36, ar40ar36, sar40ar36, rho,
                                                       isInverse=False, plt_sfactor=plt_factor, properties=properties)
                else:
                    canvas = ProFunctions.get_isochron(ar39ar36, sar39ar36, ar40ar36, sar40ar36, rho, k[9], k[11],
                                                       isInverse=False, plt_sfactor=plt_factor, properties=properties)
                    self.current_plot_data = {'X': ar39ar36, 'Y': ar40ar36,  # scatter x, scatter y
                                              # b, sb, 'Ar40a/Ar36a', value, error
                                              'Intercept': [k[9], k[10], 'Ar40a/Ar36a', k[0], k[1]],
                                              # slope, error, 'Ar40r/Ar39k', value, error
                                              'Slope': [k[11], k[12], 'Ar40r/Ar39k', k[2], k[3]],
                                              # MSWD, '', 'Age', value, error
                                              'Statistics': [k[8], '', 'Age', k[4], k[5], k[6], k[7]],
                                              # convergence, number of iterations
                                              '': [k[13], k[14], k[15]]}
            elif plt_index == 1:
                '''Inverse isochron plot'''
                ar39ar40 = list(map(lambda xi, yi: xi / yi, ar39ar36, ar40ar36))
                sar39ar40 = list(map(
                    lambda xi, sxi, yi, syi, ri:
                    pow((sxi / yi) ** 2 + (syi * xi / yi ** 2) ** 2 - 2 * ri * sxi * syi * xi / yi ** 3, 0.5),
                    ar39ar36, sar39ar36, ar40ar36, sar40ar36, rho))
                ar36ar40 = list(map(lambda yi: 1 / yi, ar40ar36))
                sar36ar40 = list(map(lambda yi, syi: pow((syi / yi ** 2) ** 2, 0.5), ar40ar36, sar40ar36))
                rho = [0] * num
                try:
                    if isYorkFit:
                        k = ProFunctions.isochron_age(ar39ar40, sar39ar40, ar36ar40, sar36ar40, rho,
                                                      j, rsj, f, rsf, isInverse=True, statistics=True,
                                                      convergence=convergence, iteration=iteration)
                    elif isOLSFit:
                        k = ProFunctions.isochron_age_ols(ar39ar40, ar36ar40, j, rsj, f, rsf, isNormal=True)
                    else:
                        raise ValueError
                except Exception as e:
                    canvas = ProFunctions.get_isochron(ar39ar40, sar39ar40, ar36ar40, sar36ar40, rho,
                                                       isInverse=True, plt_sfactor=plt_factor, properties=properties)
                else:
                    canvas = ProFunctions.get_isochron(ar39ar40, sar39ar40, ar36ar40, sar36ar40, rho, k[9], k[11],
                                                       isInverse=True, plt_sfactor=plt_factor, properties=properties)
                    self.current_plot_data = {'X': ar39ar40, 'Y': ar36ar40,  # scatter x, scatter y
                                              # b, sb, 'Ar40a/Ar36a', value, error
                                              'Intercept': [k[9], k[10], 'Ar40a/Ar36a', k[0], k[1]],
                                              # slope, error, 'Ar40r/Ar39k', value, error
                                              'Slope': [k[11], k[12], 'Ar40r/Ar39k', k[2], k[3]],
                                              # MSWD, '', 'Age', value, error
                                              'Statistics': [k[8], '', 'Age', k[4], k[5], k[6], k[7]],
                                              # convergence, number of iterations
                                              '': [k[13], k[14], k[15]]}
            elif plt_index == 2:
                '''Age spectra plot'''
                initial, sinitial = self.current_params[2], self.current_params[3]
                if self.current_params[11] == 2:
                    try:
                        k = ProFunctions.wtd_york2_regression(ar39ar36, sar39ar36, ar40ar36, sar40ar36, rho, sf=sf,
                                                              convergence=convergence, iteration=iteration)
                    except Exception as e:
                        print('Error in using intercept as initial ratio: %s' % str(e))
                    else:
                        initial, sinitial = k[0], k[1]
                ar40rar39k, sar40rar39k = \
                    ProFunctions.get_ar40rar39k(ar39ar36, sar39ar36, ar40ar36, sar40ar36, rho, initial, sinitial, False)
                k = list(map(lambda a0, e0: ProFunctions.calc_age(a0, e0, j, rsj, f, rsf, uf=1,
                                                                  useMin2000=True), ar40rar39k, sar40rar39k))
                age = [i[0] for i in k]
                ana_error, int_error, ext_error = [i[1] for i in k], [i[2] for i in k], [i[3] for i in k]
                sage = ana_error if self.current_params[6] == 2 \
                    else int_error if self.current_params[6] == 1 \
                    else ana_error
                sage = [i * 2 if self.comboBox_4.currentIndex() == 1 else i * 1 for i in sage]
                plateau_steps = None
                canvas, x, y1, y2 = ProFunctions.get_spectra(age, sage, ar39pct, plateau_steps=plateau_steps,
                                                             uf=1, properties=properties)
                self.current_plot_data = {'Ar39%': x, 'Line_1': y1, 'Line_2': y2, 'age': age,
                                          'sage': sage}
            else:
                return
        elif ipt_index == 1:
            '''Inverse Isochron Input'''
            ar39ar40 = cols[0][0:num]; sar39ar40 = cols[1][0:num]
            ar36ar40 = cols[2][0:num]; sar36ar40 = cols[3][0:num]
            rho = cols[4][0:num]; ar39pct = cols[5][0:num]
            if sf_index == 2 or sf_index == 3:
                sar39ar40 = list(map(lambda i, j: i * j / 100, ar39ar40, sar39ar40))
                sar36ar40 = list(map(lambda i, j: i * j / 100, ar36ar40, sar36ar40))
            if sf_index == 1 or sf_index == 3:
                sar39ar40 = [i / 2 for i in sar39ar40]
                sar36ar40 = [i / 2 for i in sar36ar40]
            if not ar39pct:
                ar39pct = [100 / num] * num
            if not rho:
                rho = [0] * num
            if not sar39ar40:
                sar39ar40 = [0] * num
            if not sar36ar40:
                sar36ar40 = [0] * num
            if not ar39ar40 or not ar36ar40:
                return
            sf = 1
            if plt_index == 1:
                '''Inverse isochron plot'''
                try:
                    if isYorkFit:
                        k = ProFunctions.isochron_age(ar39ar40, sar39ar40, ar36ar40, sar36ar40, rho,
                                                      j, rsj, f, rsf, isInverse=True, statistics=True,
                                                      convergence=convergence, iteration=iteration)
                    elif isOLSFit:
                        k = ProFunctions.isochron_age_ols(ar39ar40, ar36ar40, j, rsj, f, rsf, isNormal=True)
                    else:
                        raise ValueError
                except Exception as e:
                    print('Error in fitting: %s' % str(e))
                    canvas = ProFunctions.get_isochron(ar39ar40, sar39ar40, ar36ar40, sar36ar40, rho,
                                                       isInverse=True, plt_sfactor=plt_factor, properties=properties)
                else:
                    canvas = ProFunctions.get_isochron(ar39ar40, sar39ar40, ar36ar40, sar36ar40, rho, k[9], k[11],
                                                       isInverse=True, plt_sfactor=plt_factor, properties=properties)
                    self.current_plot_data = {'X': ar39ar40, 'Y': ar36ar40,  # scatter x, scatter y
                                              # b, sb, 'Ar40a/Ar36a', value, error
                                              'Intercept': [k[9], k[10], 'Ar40a/Ar36a', k[0], k[1]],
                                              # slope, error, 'Ar40r/Ar39k', value, error
                                              'Slope': [k[11], k[12], 'Ar40r/Ar39k', k[2], k[3]],
                                              # MSWD, '', 'Age', value, error
                                              'Statistics': [k[8], '', 'Age', k[4], k[5], k[6], k[7]],
                                              # convergence, number of iterations
                                              '': [k[13], k[14], k[15]]}
            elif plt_index == 0:
                '''Normal isochron plot'''
                ar39ar36 = list(map(lambda xi, yi: xi / yi, ar39ar40, ar36ar40))
                sar39ar36 = list(map(
                    lambda xi, sxi, yi, syi, ri:
                    pow((sxi / yi) ** 2 + (syi * xi / yi ** 2) ** 2 - 2 * ri * sxi * syi * xi / yi ** 3, 0.5),
                    ar39ar40, sar39ar40, ar36ar40, sar36ar40, rho))
                ar40ar36 = list(map(lambda yi: 1 / yi, ar36ar40))
                sar40ar36 = list(map(lambda yi, syi: pow((syi / yi ** 2) ** 2, 0.5), ar36ar40, sar36ar40))
                rho = [0.995] * num
                try:
                    if isYorkFit:
                        k = ProFunctions.isochron_age(ar39ar36, sar39ar36, ar40ar36, sar40ar36, rho,
                                                      j, rsj, f, rsf, isNormal=True, statistics=True,
                                                      convergence=convergence, iteration=iteration)
                    elif isOLSFit:
                        k = ProFunctions.isochron_age_ols(ar39ar36, ar40ar36, j, rsj, f, rsf, isNormal=True)
                    else:
                        raise ValueError
                except Exception as e:
                    canvas = ProFunctions.get_isochron(ar39ar36, sar39ar36, ar40ar36, sar40ar36, rho,
                                                       isInverse=False, plt_sfactor=plt_factor, properties=properties)
                else:
                    canvas = ProFunctions.get_isochron(ar39ar36, sar39ar36, ar40ar36, sar40ar36, rho, k[9], k[11],
                                                       isInverse=False, plt_sfactor=plt_factor, properties=properties)
                    self.current_plot_data = {'X': ar39ar36, 'Y': ar40ar36,  # scatter x, scatter y
                                              # b, sb, 'Ar40a/Ar36a', value, error
                                              'Intercept': [k[9], k[10], 'Ar40a/Ar36a', k[0], k[1]],
                                              # slope, error, 'Ar40r/Ar39k', value, error
                                              'Slope': [k[11], k[12], 'Ar40r/Ar39k', k[2], k[3]],
                                              # MSWD, '', 'Age', value, error
                                              'Statistics': [k[8], '', 'Age', k[4], k[5], k[6], k[7]],
                                              # convergence, number of iterations, error magnification
                                              '': [k[13], k[14], k[15]]}
            elif plt_index == 2:
                '''Age spectra plot'''
                initial, sinitial = self.current_params[2], self.current_params[3]
                if self.current_params[11] == 2:
                    try:
                        if isYorkFit:
                            k = ProFunctions.isochron_age(ar39ar40, sar39ar40, ar36ar40, sar36ar40, rho,
                                                          j, rsj, f, rsf, isNormal=True, statistics=True,
                                                          convergence=convergence, iteration=iteration)
                        elif isOLSFit:
                            k = ProFunctions.isochron_age_ols(ar39ar40, ar36ar40, j, rsj, f, rsf, isNormal=True)
                        else:
                            raise ValueError
                    except Exception as e:
                        print('Error in using intercept as initial ratio: %s' % str(e))
                    else:
                        initial, sinitial = k[0], k[1]
                ar40rar39k, sar40rar39k = \
                    ProFunctions.get_ar40rar39k(ar39ar40, sar39ar40, ar36ar40, sar36ar40, rho, initial, sinitial, True)
                k = list(map(lambda a0, e0: ProFunctions.calc_age(a0, e0, j, rsj, f, rsf, uf=sf,
                                                                  useMin2000=True), ar40rar39k, sar40rar39k))
                age = [i[0] for i in k]
                ana_error, int_error, ext_error = [i[1] for i in k], [i[2] for i in k], [i[3] for i in k]
                sage = ana_error if self.current_params[6] == 2 \
                    else int_error if self.current_params[6] == 1 \
                    else ana_error
                if age and sage and ar39pct:
                    sage = [i * 2 if self.comboBox_4.currentIndex() == 1 else i * 1 for i in sage]
                    plateau_steps = None
                    canvas, x, y1, y2 = ProFunctions.get_spectra(age, sage, ar39pct, plateau_steps=plateau_steps,
                                                                 uf=1, properties=properties)
                    self.current_plot_data = {'Ar39%': x, 'Line_1': y1, 'Line_2': y2, 'age': age, 'sage': sage}
                else:
                    return
            else:
                return
        elif ipt_index == 2:
            '''Degassing Input'''
            v0 = cols[0][0:num]; s0 = cols[1][0:num]  # Ar40(a+r)
            v1 = cols[2][0:num]; s1 = cols[3][0:num]  # Ar39k
            v2 = cols[4][0:num]; s2 = cols[5][0:num]  # Ar36a
            ar39pct = cols[6][0:num]
            s0 = [0] * num if not s0 else s0
            s1 = [0] * num if not s1 else s1
            s2 = [0] * num if not s2 else s2
            if not ar39pct:
                ar39pct = [100 / num] * num
            if not v0 or not v1 or not v2:
                return
            if sf_index == 2 or sf_index == 3:
                s0 = list(map(lambda i, si: i * si / 100, v0, s0))
                s1 = list(map(lambda i, si: i * si / 100, v1, s1))
                s2 = list(map(lambda i, si: i * si / 100, v2, s2))
            sf = 1 if sf_index == 0 or sf_index == 2 else 2
            s0 = [i / sf for i in s0]
            s1 = [i / sf for i in s1]
            s2 = [i / sf for i in s2]
            '''Normal Isochron data'''
            ar39ar36 = list(map(lambda i, i2: i / i2, v1, v2))  # Ar39 / Ar36 -> x
            sar39ar36 = list(map(lambda i, si, i2, si2: ProFunctions.error_div((i, si), (i2, si2)), v1, s1, v2, s2))
            ar40ar36 = list(map(lambda i, i2: i / i2, v0, v2))  # Ar40 / Ar36 -> y
            sar40ar36 = list(map(lambda i, si, i2, si2: ProFunctions.error_div((i, si), (i2, si2)), v0, s0, v2, s2))
            ri_normal = list(map(lambda si, si2, si3, i, i2, i3: ProFunctions.error_cor(si/i, si2/i2, si3/i3),
                                 s1, s0, s2, v1, v0, v2))
            try:
                if isYorkFit:
                    k_normal = ProFunctions.isochron_age(ar39ar36, sar39ar36, ar40ar36, sar40ar36, ri_normal,
                                                         j, rsj, f, rsf, isNormal=True, statistics=True,
                                                         convergence=convergence, iteration=iteration)
                elif isOLSFit:
                    k_normal = ProFunctions.isochron_age_ols(ar39ar36, ar40ar36, j, rsj, f, rsf, isNormal=True)
                else:
                    raise ValueError
            except Exception as e:
                k_normal = None
            '''Inverse Isochron data'''
            ar39ar40 = list(map(lambda i, i2: i / i2, v1, v0))  # Ar39k / Ar40(a+r)
            sar39ar40 = list(map(lambda i, si, i2, si2: ProFunctions.error_div((i, si), (i2, si2)), v1, s1, v0, s0))
            ar36ar40 = list(map(lambda i, i2: i / i2, v2, v0))  # Ar36a / Ar40(a+r)
            sar36ar40 = list(map(lambda i, si, i2, si2: ProFunctions.error_div((i, si), (i2, si2)), v2, s2, v0, s0))
            ri_inverse = list(map(lambda si, si2, si3, i, i2, i3: ProFunctions.error_cor(si/i, si2/i2, si3/i3),
                                  s1, s0, s2, v1, v0, v2))
            try:
                if isYorkFit:
                    k_inverse = ProFunctions.isochron_age(ar39ar40, sar39ar40, ar36ar40, sar36ar40, ri_inverse,
                                                          j, rsj, f, rsf, isInverse=True, statistics=True,
                                                          convergence=convergence, iteration=iteration)
                elif isOLSFit:
                    k_inverse = ProFunctions.isochron_age_ols(ar39ar40, ar36ar40, j, rsj, f, rsf, isNormal=True)
                else:
                    raise ValueError
            except Exception as e:
                k_inverse = None
            if plt_index == 2:
                '''Age spectra'''
                if not k_inverse:
                    return
                initial = self.current_params[2] if self.current_params[11] == 0 else \
                    k_inverse[0] if k_inverse is not None else 0
                sinitial = self.current_params[3] if self.current_params[11] == 0 else \
                    k_inverse[1] if k_inverse is not None else 0
                ar40rar39k, sar40rar39k = \
                    ProFunctions.get_ar40rar39k(ar39ar36, sar39ar36, ar40ar36, sar40ar36, ri_normal,
                                                initial, sinitial, False)
                k = list(map(lambda a0, e0: ProFunctions.calc_age(a0, e0, j, rsj, f, rsf, useMin2000=True),
                             ar40rar39k, sar40rar39k))
                age = [i[0] for i in k]
                sage = [i[1] * 1 if self.comboBox_4.currentIndex() == 0 else i[1] * 2 for i in k]
                plateau_steps = None
                canvas, x, y1, y2 = ProFunctions.get_spectra(age, sage, ar39pct, plateau_steps=plateau_steps,
                                                             uf=1, properties=properties)
                self.current_plot_data = {'Ar39%': x, 'Line_1': y1, 'Line_2': y2}
                
                plateau_f, plateau_sf, dp, mswd = ProFunctions.err_wtd_mean(ar40rar39k[3:], sar40rar39k[3:])
                plateau_age = ProFunctions.calc_age(plateau_f, plateau_sf, j, rsj, f, rsf, useMin2000=True)
                print('plateau_age: %s ± %s Ma' % (plateau_age[0], plateau_age[2]))
            else:
                if plt_index == 0:
                    '''Normal Isochron'''
                    x, sx = ar39ar36, sar39ar36  # Ar39 / Ar36 -> x
                    y, sy = ar40ar36, sar40ar36  # Ar40 / Ar36 -> y
                    k = k_normal
                    b = k_normal[9] if k_normal is not None else None
                    m = k_normal[11] if k_normal is not None else None
                    rho = ri_normal
                    canvas = ProFunctions.get_isochron(x, sx, y, sy, rho, b, m, isInverse=False,
                                                       plt_sfactor=plt_factor, properties=properties)
                else:
                    '''Inverse Isochron'''
                    x, sx = ar39ar40, sar39ar40  # Ar39 / Ar40 -> x
                    y, sy = ar36ar40, sar36ar40  # Ar36 / Ar40 -> y
                    k = k_inverse
                    b = k_inverse[9] if k_inverse is not None else None
                    m = k_inverse[11] if k_inverse is not None else None
                    rho = ri_inverse
                    canvas = ProFunctions.get_isochron(x, sx, y, sy, rho, b, m, isInverse=True,
                                                       plt_sfactor=plt_factor, properties=properties)
                if k is None:
                    k = ['None'] * 16
                self.current_plot_data = {'X': ar39ar36, 'Y': ar40ar36,  # scatter x, scatter y
                                          # b, sb, 'Ar40a/Ar36a', value, error
                                          'Intercept': [k[9], k[10], 'Ar40a/Ar36a', k[0], k[1]],
                                          # slope, error, 'Ar40r/Ar39k', value, error
                                          'Slope': [k[11], k[12], 'Ar40r/Ar39k', k[2], k[3]],
                                          # MSWD, '', 'Age', value, error
                                          'Statistics': [k[8], '', 'Age', k[4], k[5], k[6], k[7]],
                                          # convergence, number of iterations, error magnification
                                          '': [k[13], k[14], k[15]]}
        elif ipt_index == 3:
            '''Age spectra'''
            age = cols[0][0:num]; sage = cols[1][0:num]; ar39pct = cols[2][0:num]
            if not age or not sage:
                return
            if sf_index == 2 or sf_index == 3:
                sage = list(map(lambda i, si: i * si / 100, age, sage))
            if not ar39pct:
                ar39pct = [100 / num] * num
            sf = 1 if sf_index == 0 or sf_index == 2 else 2
            sage = [si * 1 / sf if self.comboBox_4.currentIndex() == 0 else si * 2 / sf for si in sage]
            plateau_steps = None
            canvas, x, y1, y2 = ProFunctions.get_spectra(age, sage, ar39pct, plateau_steps=plateau_steps,
                                                         uf=1, properties=properties)
            self.current_plot_data = {'Ar39%': x, 'Line_1': y1, 'Line_2': y2}
        try:
            self.verticalLayout.removeWidget(self.canvas)
            self.canvas.deleteLater()
        except AttributeError:
            pass
        finally:
            if self.axis_setting[5] == 2:
                self.axis_setting[0:4] = [canvas.axes.get_ybound()[1], canvas.axes.get_ybound()[0],
                                          canvas.axes.get_xbound()[0], canvas.axes.get_xbound()[1]]
                self.dialog_axis_setting.lineEdit_top.setText('%f' % float(self.axis_setting[0]))
                self.dialog_axis_setting.lineEdit_bottom.setText('%f' % float(self.axis_setting[1]))
                self.dialog_axis_setting.lineEdit_left.setText('%f' % float(self.axis_setting[2]))
                self.dialog_axis_setting.lineEdit_right.setText('%f' % float(self.axis_setting[3]))
            elif self.axis_setting[5] == 0:
                [top, bottom, left, right] = self.axis_setting[0:4]
                canvas.axes.set_xbound(left, right)
                canvas.axes.set_ybound(bottom, top)
            self.canvas = canvas
            self.verticalLayout.addWidget(self.canvas)
            return


class DialogParamSetting(QDialog, UI_ParamSetting.Ui_Dialog):
    signal_params = pyqtSignal(list)
    error_propagation = ['Full External Errors', 'Internal Errors', 'Analytical Error']
    fitting_model = ['York-2', 'OLS']
    extract_plateau = ['Method01', 'Method02', 'Method03']

    def __init__(self, current_params):
        super(DialogParamSetting, self).__init__()
        self.setupUi(self)

        self.comboBox.addItems(self.error_propagation)
        self.comboBox_1.addItems(self.fitting_model)
        self.comboBox_2.addItems(self.extract_plateau)

        regx = QRegExp('-?\d+\.?\d*e?-?\d+')
        validator = QRegExpValidator(regx, self)
        k = [self.lineEdit_1, self.lineEdit_2, self.lineEdit_3, self.lineEdit_4, self.lineEdit_5, self.lineEdit_6]
        for i in range(len(k)):
            k[i].setText(str(current_params[i]))
            k[i].setValidator(validator)
        self.lineEdit_7.setValidator(validator)
        self.lineEdit_8.setValidator(QRegExpValidator(QRegExp('^[1-9]\d*$'), self))
        self.comboBox.setCurrentIndex(current_params[6])
        self.checkBox.setCheckState(Qt.CheckState(current_params[7]))
        self.comboBox_1.setCurrentIndex(current_params[8])
        self.lineEdit_7.setText(str(current_params[9]))
        self.lineEdit_8.setText(str(current_params[10]))
        self.checkBox_1.setCheckState(Qt.CheckState(current_params[11]))
        self.checkBox_2.setCheckState(Qt.CheckState(current_params[12]))
        self.comboBox_2.setCurrentIndex(current_params[13])

        if self.checkBox_2.checkState() == 0:
            self.comboBox_2.setDisabled(True)
        else:
            self.comboBox_2.setDisabled(False)

        if self.comboBox_1.currentIndex() == 0:
            self.lineEdit_7.setDisabled(False)
            self.lineEdit_8.setDisabled(False)
        else:
            self.lineEdit_7.setDisabled(True)
            self.lineEdit_8.setDisabled(True)

        self.new_params = list(current_params)  # copy params list
        self.pushButton_apply.clicked.connect(self.button_apply_clicked)
        self.pushButton_cancel.clicked.connect(self.button_ok_clicked)
        self.pushButton.clicked.connect(self.get_Jvalue)

        self.lineEdit_1.textChanged.connect(lambda text: self.get_new_params(text, 0))
        self.lineEdit_2.textChanged.connect(lambda text: self.get_new_params(text, 1))
        self.lineEdit_3.textChanged.connect(lambda text: self.get_new_params(text, 2))
        self.lineEdit_4.textChanged.connect(lambda text: self.get_new_params(text, 3))
        self.lineEdit_5.textChanged.connect(lambda text: self.get_new_params(text, 4))
        self.lineEdit_6.textChanged.connect(lambda text: self.get_new_params(text, 5))
        self.comboBox.currentIndexChanged.connect(lambda index: self.get_new_params(index, 6))
        self.checkBox.stateChanged.connect(lambda index: self.checkbox_statechanged(index, 7))
        self.comboBox_1.currentIndexChanged.connect(lambda index: self.get_new_params(index, 8))
        self.lineEdit_7.textChanged.connect(lambda text: self.get_new_params(text, 9))
        self.lineEdit_8.textChanged.connect(lambda text: self.get_new_params(text, 10))
        self.checkBox_1.stateChanged.connect(lambda index: self.checkbox_statechanged(index, 11))
        self.checkBox_2.stateChanged.connect(lambda index: self.checkbox_statechanged(index, 12))
        self.comboBox_2.currentIndexChanged.connect(lambda index: self.get_new_params(index, 13))

    def get_new_params(self, a0, index: int):
        if isinstance(a0, str):
            try:
                self.new_params[index] = float(a0)
            except Exception as e:
                print('Error in updating params list: %s' % str(e))
        elif isinstance(a0, int):
            self.new_params[index] = a0
            if self.comboBox_1.currentIndex() == 0:
                self.lineEdit_7.setDisabled(False)
                self.lineEdit_8.setDisabled(False)
            else:
                self.lineEdit_7.setDisabled(True)
                self.lineEdit_8.setDisabled(True)
        elif isinstance(a0, tuple):
            self.lineEdit_1.setText(a0[0])
            self.lineEdit_2.setText(a0[1])

    def checkbox_statechanged(self, a0: int, a1: int):
        self.new_params[a1] = a0
        if self.checkBox_2.checkState() == 2:
            self.comboBox_2.setDisabled(False)
        else:
            self.comboBox_2.setDisabled(True)
        return

    def get_Jvalue(self):
        UI_Jvalue = jvalueCalcualtion.SubWindowJvalueCalculation()
        UI_Jvalue.signal_jvalue.connect(lambda k: self.get_new_params(k, 0))
        UI_Jvalue.exec()

    def button_apply_clicked(self):
        self.signal_params.emit(self.new_params)

    def button_ok_clicked(self):
        self.button_apply_clicked()
        self.close()


class DialogAxisSetting(QDialog, UI_AxisSetting.Ui_Dialog_AxisSetting):
    signal_axis_setting = pyqtSignal(list)
    axis_setting: list = []
    scatter_size: list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    scatter_style: dict = {'point': '.', 'pixel': ',', 'circle': 'o', 'triangle down': 'v', 'triangle up': '^',
                           'triangle left': '<', 'triangle right': '>', 'octagon': '8', 'square': 's', 'pentagon': 'p',
                           'plus': 'P', 'star': '*', 'x': 'x', 'diamond': 'D', 'thin diamond': 'd'}
    line_width: list = [0, 1, 2, 3, 4, 5]
    line_style: list = ['none', 'solid', 'dashed', 'dashdot', 'dotted']
    color_map: list = ['none', 'black', 'blue', 'red', 'yellow', 'green', 'y', 'others']

    def __init__(self, axis_setting):
        super(DialogAxisSetting, self).__init__()
        self.setupUi(self)

        self.pushButton_apply.clicked.connect(self.buttom_apply_clicked)
        self.pushButton_ok.clicked.connect(self.buttom_ok_clicked)

        regx = QRegExp('-?\d+\.?\d*e?-?\d+')
        validator = QRegExpValidator(regx, self)
        k = [self.lineEdit_top, self.lineEdit_bottom, self.lineEdit_left, self.lineEdit_right]
        for i in range(len(k)):
            k[i].setText('%f' % float(axis_setting[i]))
            k[i].setValidator(validator)
            if axis_setting[5] == 2:
                k[i].setDisabled(True)
        self.lineEdit_top.textChanged.connect(lambda text: self.textline_changed(text, self.lineEdit_top))
        self.lineEdit_bottom.textChanged.connect(lambda text: self.textline_changed(text, self.lineEdit_bottom))
        self.lineEdit_left.textChanged.connect(lambda text: self.textline_changed(text, self.lineEdit_left))
        self.lineEdit_right.textChanged.connect(lambda text: self.textline_changed(text, self.lineEdit_right))

        self.checkBox.stateChanged.connect(lambda a0: self.check_state_changed(a0, 0))
        self.checkBox_2.stateChanged.connect(lambda a0: self.check_state_changed(a0, 1))
        self.checkBox_3.stateChanged.connect(lambda a0: self.check_state_changed(a0, 2))

        self.checkBox.setCheckState(Qt.CheckState(axis_setting[4]))
        self.check_state_changed(axis_setting[4], 0)
        self.checkBox_3.setCheckState(Qt.CheckState(axis_setting[6]))
        self.check_state_changed(axis_setting[6], 1)
        self.checkBox_2.setCheckState(Qt.CheckState(axis_setting[5]))
        self.check_state_changed(axis_setting[5], 2)

        properties = dict(axis_setting[7])
        '''Scatter properties'''
        self.comboBox_scatter_size.addItems([str(i) for i in self.scatter_size])  # points size
        self.comboBox_scatter_size.setCurrentText(str(properties.pop('scatter_size', self.scatter_size[0])))
        self.comboBox_scatter_style.addItems(list(self.scatter_style.keys()))
        self.comboBox_scatter_style.setCurrentIndex(0)
        self.comboBox_scatter_b_c.currentTextChanged.connect(lambda a0: self.color_changed(a0, 0))
        self.comboBox_scatter_b_c.addItems(self.color_map)  # border color
        self.comboBox_scatter_b_c.setCurrentText(str(properties.pop('scatter_b_c', self.color_map[0])))
        self.comboBox_scatter_f_c.currentTextChanged.connect(lambda a0: self.color_changed(a0, 1))
        self.comboBox_scatter_f_c.addItems(self.color_map)  # fill color
        self.comboBox_scatter_f_c.setCurrentText(str(properties.pop('scatter_f_c', self.color_map[0])))
        self.checkBox_show_random_points.setCheckState(Qt.CheckState(int(properties.pop('show_random_pts', 0))))
        self.lineEdit_random_points_num.setText(str(properties.pop('random_points_num', 1500)))
        self.lineEdit_random_points_num.setValidator(QRegExpValidator(QRegExp('\d+'), self))
        '''Line properties'''
        self.comboBox_line_w.addItems([str(i) for i in self.line_width])  # line width
        self.comboBox_line_w.setCurrentText(str(properties.pop('line_w', self.line_width[0])))
        self.comboBox_line_s.addItems(self.line_style)  # line style
        self.comboBox_line_s.setCurrentText(str(properties.pop('line_s', self.line_style[0])))
        self.comboBox_line_c.currentTextChanged.connect(lambda a0: self.color_changed(a0, 2))
        self.comboBox_line_c.addItems(self.color_map)  # line color
        self.comboBox_line_c.setCurrentText(str(properties.pop('line_c', self.color_map[0])))
        '''Ellipse properties'''
        self.checkBox_ellipse.stateChanged.connect(lambda a0: self.check_state_changed(a0, 3))
        self.checkBox_ellipse.setCheckState(Qt.CheckState(int(properties.pop('drawEllipse', 2))))
        self.check_state_changed(self.checkBox_ellipse.checkState(), 3)
        self.comboBox_ellipse_b_c.addItems(self.color_map)  # ellipse border color
        self.comboBox_ellipse_b_c.currentTextChanged.connect(lambda a0: self.color_changed(a0, 3))
        self.comboBox_ellipse_b_c.setCurrentText(str(properties.pop('ellipse_b_c', self.color_map[0])))
        self.comboBox_ellipse_f_c.addItems(self.color_map)  # ellipse fill color
        self.comboBox_ellipse_f_c.currentTextChanged.connect(lambda a0: self.color_changed(a0, 4))
        self.comboBox_ellipse_f_c.setCurrentText(str(properties.pop('ellipse_f_c', self.color_map[0])))
        '''age spectra'''
        self.comboBox_spectra_w.addItems([str(i) for i in self.line_width])
        self.comboBox_spectra_w.setCurrentText(str(properties.pop('spectra_w', self.line_width[0])))
        self.comboBox_spectra_s.addItems(self.line_style)
        self.comboBox_spectra_s.setCurrentText(str(properties.pop('spectra_s', self.line_style[0])))
        self.comboBox_spectra_b_c.addItems(self.color_map)
        self.comboBox_spectra_b_c.currentTextChanged.connect(lambda a0: self.color_changed(a0, 5))
        self.comboBox_spectra_b_c.setCurrentText(str(properties.pop('spectra_b_c', self.color_map[0])))
        self.comboBox_spectra_f_c.addItems(self.color_map)
        self.comboBox_spectra_f_c.currentTextChanged.connect(lambda a0: self.color_changed(a0, 6))
        self.comboBox_spectra_f_c.setCurrentText(str(properties.pop('spectra_f_c', self.color_map[0])))
        self.comboBox_plateau_b_c.addItems(self.color_map)
        self.comboBox_plateau_b_c.currentTextChanged.connect(lambda a0: self.color_changed(a0, 7))
        self.comboBox_plateau_b_c.setCurrentText(str(properties.pop('plateau_b_c', self.color_map[0])))
        self.comboBox_plateau_f_c.addItems(self.color_map)
        self.comboBox_plateau_f_c.currentTextChanged.connect(lambda a0: self.color_changed(a0, 8))
        self.comboBox_plateau_f_c.setCurrentText(str(properties.pop('plateau_f_c', self.color_map[0])))

    def buttom_apply_clicked(self):
        for i in [self.lineEdit_top, self.lineEdit_bottom, self.lineEdit_left, self.lineEdit_right]:
            if list(i.text())[-1] == '-' or list(i.text())[-1] == '+' or list(i.text())[-1] == 'e':
                i.setText(i.text() + '1')
        self.axis_setting = [float(self.lineEdit_top.text()), float(self.lineEdit_bottom.text()),
                             float(self.lineEdit_left.text()), float(self.lineEdit_right.text()),
                             self.checkBox.checkState(), self.checkBox_2.checkState(), self.checkBox_3.checkState()]
        properties: dict = {'scatter_size': int(self.comboBox_scatter_size.currentText()),
                            'scatter_style': self.scatter_style[self.comboBox_scatter_style.currentText()],
                            'scatter_b_c': self.comboBox_scatter_b_c.currentText(),
                            'scatter_f_c': self.comboBox_scatter_f_c.currentText(),
                            'show_random_pts': self.checkBox_show_random_points.checkState(),
                            'random_points_num': int(self.lineEdit_random_points_num.text()),
                            'line_w': int(self.comboBox_line_w.currentText()),
                            'line_s': self.comboBox_line_s.currentText(),
                            'line_c': self.comboBox_line_c.currentText(),
                            'drawEllipse': self.checkBox_ellipse.checkState(),
                            'ellipse_b_c': self.comboBox_ellipse_b_c.currentText(),
                            'ellipse_f_c': self.comboBox_ellipse_f_c.currentText(),
                            'spectra_w': int(self.comboBox_spectra_w.currentText()),
                            'spectra_s': self.comboBox_spectra_s.currentText(),
                            'spectra_b_c': self.comboBox_spectra_b_c.currentText(),
                            'spectra_f_c': self.comboBox_spectra_f_c.currentText()}
        self.axis_setting.append(properties)
        self.signal_axis_setting.emit(self.axis_setting)
        return self.axis_setting

    def buttom_ok_clicked(self):
        self.buttom_apply_clicked()
        self.close()

    def textline_changed(self, text=None, a0=None):
        if self.checkBox.isChecked():
            scale = abs(float(self.lineEdit_right.text()) - float(self.lineEdit_left.text()))
            self.lineEdit_top.setText('%f' % (float(self.lineEdit_bottom.text()) + scale))

    def color_changed(self, a0, index, isUser: bool = True):
        combobox = [self.comboBox_scatter_b_c, self.comboBox_scatter_f_c, self.comboBox_line_c,
                    self.comboBox_ellipse_b_c, self.comboBox_ellipse_f_c, self.comboBox_spectra_b_c,
                    self.comboBox_spectra_f_c, self.comboBox_plateau_b_c, self.comboBox_plateau_f_c]
        label = [self.label_scatter_b_c, self.label_scatter_f_c, self.label_line_c,
                 self.label_ellipse_b_c, self.label_ellipse_f_c, self.label_spectra_b_c,
                 self.label_spectra_f_c, self.label_plateau_b_c, self.label_plateau_f_c]
        if not isUser:
            return
        if a0 == 'none':
            label[index].setText(combobox[index].currentText())
        elif a0 == 'others':
            initial = label[index].text()
            color_dialog = QColorDialog()
            color_dialog.setCurrentColor(QColor(initial))
            reply = color_dialog.exec()
            color = color_dialog.currentColor()
            if color.isValid() and reply == 1:
                combobox[index].addItem(color.name())
                combobox[index].setCurrentText(color.name())
            elif reply == 0:
                combobox[index].setCurrentText(initial)
        else:
            label[index].setText(combobox[index].currentText())

    def check_state_changed(self, a0: int, index: int):
        if index == 0:
            if a0 == 2:
                self.lineEdit_top.setDisabled(True)
                self.textline_changed()
            else:
                self.lineEdit_top.setDisabled(False)
        elif index == 1:
            if a0 == 2:
                self.checkBox.setCheckState(Qt.CheckState(0))
                self.checkBox.setDisabled(True)
                self.checkBox_3.setDisabled(False)
                self.lineEdit_top.setDisabled(True)
                self.lineEdit_bottom.setDisabled(True)
                self.lineEdit_left.setDisabled(True)
                self.lineEdit_right.setDisabled(True)
            else:
                self.checkBox.setDisabled(False)
                self.checkBox_3.setCheckState(Qt.CheckState(0))
                self.checkBox_3.setDisabled(True)
                self.lineEdit_top.setDisabled(False)
                self.lineEdit_bottom.setDisabled(False)
                self.lineEdit_left.setDisabled(False)
                self.lineEdit_right.setDisabled(False)
        elif index == 2:
            if a0 == 2:
                if not self.checkBox_2.isChecked():
                    self.checkBox_3.setCheckState(Qt.CheckState(0))
                    return
        elif index == 3:
            if a0 == 0:
                self.comboBox_ellipse_b_c.setDisabled(True)
                self.comboBox_ellipse_f_c.setDisabled(True)
            else:
                self.comboBox_ellipse_b_c.setDisabled(False)
                self.comboBox_ellipse_f_c.setDisabled(False)


if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    UI = SubWindowPlotting()
    UI.show()
    sys.exit(app.exec())
