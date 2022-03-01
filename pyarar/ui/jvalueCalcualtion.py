#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : jvalueCalculation.py
# @Author : Yang Wu
# @Date   : 2021/5/20
# @Email  : wuy@cug.edu.cn
import json
import os
import sys
from typing import List
import numpy as np
import copy
from math import exp
import pyarar.FuncsCalc as ProFunctions
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, FigureCanvasQTAgg
from PyQt5.QtCore import QCoreApplication, Qt, QObject, QEvent, QSize, pyqtSignal, QRegExp
from PyQt5.QtGui import QIcon, QMouseEvent, QPixmap, QRegExpValidator
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QSizePolicy, QLabel, QTableWidgetItem, QFrame, \
    QFileDialog, QLineEdit, QMessageBox, QHeaderView

from pyarar.ui import UI_JvalueCalcWindow
from pyarar.ui import UI_StdSettingDialog
from pyarar.ui import UI_UnkSettingDialog
from pyarar.ui import UI_FileFilter


class SubWindowJvalueCalculation(QDialog, UI_JvalueCalcWindow.Ui_Dialog_JvalueCalc):
    percentage_center: float = 0.5
    J_relative_error: float = 0.0015
    canvas: FigureCanvasQTAgg
    signal_jvalue = pyqtSignal(tuple)

    def __init__(self):
        super(SubWindowJvalueCalculation, self).__init__()
        self.setupUi(self)
        print('JvalueCalculation')
        '''Record the table content and can be used to sort and read value'''
        self.current_table_tuple_list: list = []
        '''Determine the selected pointer name'''
        self.selected_pointer_name: str = 'No Selected Pointer'
        self.selected_label_name: str = 'No Selected Pointer'
        self.selected_frame_name: str = 'No Selected Pointer'
        self.pointer_movable: bool = False  # Determines whether the pointer responds to the movement of mouse
        self.pushButton_vial_bottom.installEventFilter(self)
        self.pushButton_vial_top.installEventFilter(self)
        print(os.path.dirname(__file__) + "/../../icons/pointer_black.png")
        self.pushButton_vial_bottom.setIcon(QIcon(os.path.dirname(__file__) + "/../../icons/pointer_black.png"))
        self.pushButton_vial_top.setIcon(QIcon(os.path.dirname(__file__) + "/../../icons/pointer_black.png"))
        self.radioButton_line.setChecked(True)

        self.pushButton_add.clicked.connect(lambda: self.add_standard(isStandard=True))
        self.pushButton_add_2.clicked.connect(lambda: self.add_standard(isStandard=False))
        self.pushButton_delete.clicked.connect(lambda: self.del_table(isStandard=True))
        self.pushButton_delete_2.clicked.connect(lambda: self.del_table(isStandard=False))
        self.tableWidget.cellChanged.connect(self.table_1_item_changed)
        self.tableWidget_2.cellChanged.connect(self.table_2_item_changed)

        self.pushButton_setting.clicked.connect(self.std_setting)
        self.pushButton_setting_2.clicked.connect(self.unk_setting)
        self.pushButton_import.clicked.connect(self.import_file)
        self.pushButton_save.clicked.connect(self.save)
        self.pushButton_extract.clicked.connect(self.export)

        self.radioButton_para.toggled.connect(self.plot)
        self.radioButton_line.toggled.connect(self.plot)
        self.radioButton_exp.toggled.connect(self.plot)

        self.textEdit.setFontPointSize(10)
        self.textEdit.setFontFamily('Arial')

        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.ufactor = 0.25  # ufactor = scale / self.frame.width(), unit = mm / px
        self.pfactor = 0.5  # determine the ratio used to calculate x value in the plot figures
        self.sample_info: list = []
        self.show_scale(self.ufactor)

        self.table_dict = StdSettingDialog(self.ufactor, self.line_hor.width()).get_table()
        self.plot()

        '''Header index'''
        self.age_index = 2
        self.age_error_index = 3
        self.ratio_index = 4
        self.ratio_error_index = 5
        self.bottom_value_index = 6
        self.height_value_index = 7
        self.j_value_index = 8
        self.j_error_index = 9

        '''constants'''
        self.decay_const = 0.0000000005530
        self.f_relative_error = 0.0000000000048 / self.decay_const * 100

    def import_file(self):
        filepath, filetype = QFileDialog.getOpenFileName(self, 'Read Packaged Sample List', os.getcwd(),
                                                         'TXT文件(*.txt);;Excel文件(*.xl*)')
        if not filepath:
            return
        if 'txt' in filetype:
            file_list = ProFunctions.read_file(filepath, 1)
            for each_line in file_list:
                index = file_list.index(each_line)
                each_line = each_line.split()
                file_list[index] = each_line

        elif 'xl*' in filetype:
            filedict = ProFunctions.read_file(filepath, 0)
            if len(filedict.values()) == 1:
                file_list = list(filedict.values())[0]
        file_filter = FileFilterDialog(file_list)
        file_filter.exec()
        std_index = [i - 1 for i in file_filter.standard_index]
        unk_index = [i - 1 for i in file_filter.unknown_index]
        std_col_index = [i - 1 for i in file_filter.std_col_index]
        unk_col_index = [i - 1 for i in file_filter.unk_col_index]
        file_list = file_filter.file_list
        if not file_filter.apply_clicked:
            return
        '''clear table content'''
        for row in range(self.tableWidget.rowCount()):
            self.del_table(a0=0, isStandard=True)
        for row in range(self.tableWidget_2.rowCount()):
            self.del_table(a0=0, isStandard=False)
        unk_n = -1
        std_n = -1
        for row in range(len(file_list)):
            if row in std_index:
                self.add_standard()
                std_n += 1
                for i in range(len(std_col_index)):
                    if std_col_index[i] == -1:
                        continue
                    else:
                        try:
                            self.tableWidget.setItem(std_n, i, QTableWidgetItem(str(file_list[row][std_col_index[i]])))
                        except ValueError:
                            # print('Error in writing table: %s' % str(e))
                            pass
            elif row in unk_index:
                self.add_standard(isStandard=False)
                unk_n += 1
                for i in range(len(unk_col_index)):
                    if unk_col_index[i] == -1:
                        continue
                    else:
                        try:
                            self.tableWidget_2.setItem(unk_n, i, QTableWidgetItem(str(file_list[row][unk_col_index[i]])))
                        except Exception as e:
                            print('Error in writing unknown table: %s' % str(e))
            else:
                pass
        return

    def save(self):
        line_list = []
        for row in range(self.tableWidget_2.rowCount()):
            text = ''
            for col in range(self.tableWidget_2.columnCount()):
                try:
                    text = text + self.tableWidget_2.item(row, col).text() + '   '
                except Exception as e:
                    print('Error in reading table2: %s' % str(e))
                    text = text + '\t'
                if col == self.tableWidget_2.columnCount() - 1:
                    text = text + '\n'
            line_list.append(text)
        try:
            with open(os.path.dirname(__file__) + '/../../settings/unknownSample.txt', 'w') as file:
                file.writelines(line_list)
        except Exception as e:
            print('Error in writing txt: %s' % str(e))
        else:
            QMessageBox.information(self, "Info", "Unknown sample file has been successfully saved. Dir: %s" % (
                        os.path.dirname(__file__) + '/../../settings/unknownSample.txt'),
                                    QMessageBox.Yes | QMessageBox.No)

    def export(self):
        if self.tableWidget_2.selectedIndexes():
            row = self.tableWidget_2.selectedIndexes()[0].row()
            k0 = sorted(self.sample_info, key=lambda item: item[3].x())
            k1 = -1
            for i in k0:
                if len(i[0]) == self.tableWidget_2.columnCount():
                    k1 += 1
                    if k1 == row:
                        self.signal_jvalue.emit((i[0][3], i[0][4]))
                        return i[0][3], i[0][4]
            return False
        else:
            return False

    def get_stdJ(self, row):
        """
        :param row: row index of standard table
        :return:
        """
        f = self.decay_const
        sf = self.f_relative_error
        standard_list = []
        for i in self.sample_info:
            if 'standard' in i[1].objectName():
                standard_list.append(i)
        std_list = sorted(standard_list, key=lambda item: item[3].x())[row][0]
        a0 = float(std_list[self.age_index])
        a1 = float(std_list[self.age_error_index])
        a2 = float(std_list[self.ratio_index])
        a3 = float(std_list[self.ratio_error_index])
        j_value, error = ProFunctions.j_value(a0, a1, a2, a3, f, sf)
        return j_value, error

    def table_1_item_changed(self, row, col):
        self.table_item_changed(row, col, isStandard=True)
        return

    def table_2_item_changed(self, row, col):
        self.table_item_changed(row, col, isStandard=False)
        return
        
    def table_item_changed(self, row: int, col: int, isStandard: bool = True):
        """
        :param row: row number
        :param col: col number
        :param isStandard: determine the sample type, True for standard, and False for unknown
        :return: no return
        """
        if isStandard:
            table = self.tableWidget
            sample_type = 'standard'
            std_index = 1
            age_index, age_error_index = self.age_index, self.age_error_index
            ratio_index, ratio_error_index = self.ratio_index, self.ratio_error_index
            bottom_index, height_index = self.bottom_value_index, self.height_value_index
            j_index, j_error_index = self.j_value_index, self.j_error_index
        else:
            table = self.tableWidget_2
            sample_type = 'unknown'
            bottom_index, height_index = 1, 2
            '''unused index in unknown sample, J value changed in plot function'''
            [j_index, j_error_index, std_index, age_index, age_error_index] = [9999] * 5
            ratio_index, ratio_error_index = 9999, 9999
        text = table.item(row, col).text()
        '''update sample_info list'''
        table_list = sorted(self.sample_info, key=lambda item: item[1].x())
        num = 0
        for i in table_list:
            if sample_type in i[1].objectName():
                num += 1
                if num == row + 1:
                    index = table_list.index(i)  # obtain the index of changed item in sample info list
                    i[0][col] = text  # modifiable type， record the real and absolute value
                    [current_label, current_pointer, current_frame] = table_list[index][1:4]
                    break
        '''setting geometry of pointers'''
        if col == height_index:
            try:
                height_value = float(text)
                if int(float(text) * 10 / self.ufactor + current_frame.x()) > int(self.frame.x() + self.frame.width()):
                    height_value = int(self.frame.x() + self.frame.width() - current_frame.x()) * self.ufactor / 10
                current_frame.setGeometry(current_frame.x(), current_frame.y(), int(height_value * 10 / self.ufactor),
                                          current_frame.height())
            except Exception as e:
                return
        elif col == bottom_index:
            try:
                bottom_value = float(text) * 10
                x_frame = int(bottom_value / self.ufactor + self.line_hor.x())
                self.pointer_move(x_frame, current_pointer.y(), current_pointer.objectName(), isInternal=False)
                self.pointer_move(x_frame, current_frame.y(), current_frame.objectName(), isInternal=False)
                self.pointer_move(x_frame, current_label.y(), current_label.objectName(), isInternal=False)
                self.plot()
            except Exception as e:
                return
        elif col == j_index:
            try:
                self.plot()
            except Exception as e:
                return
        elif col == std_index:
            try:
                std_list = StdSettingDialog(self.ufactor, self.line_hor.width()).get_table()[text]
                table.setItem(row, age_index, QTableWidgetItem(std_list[1]))
                table.setItem(row, age_error_index, QTableWidgetItem(std_list[2]))
            except Exception as e:
                return
                # print('Error in responding to table changed: %s' % str(e))
        elif col in [age_index, age_error_index, ratio_index, ratio_error_index]:
            try:
                j_value, error = self.get_stdJ(row)
                table.setItem(row, j_index, QTableWidgetItem(str(j_value)))
                table.setItem(row, j_error_index, QTableWidgetItem(str(error)))
            except Exception as e:
                return
                # print('Error in responding to table changed: %s' % str(e))
        else:
            pass

    def change_table(self, row: int, col: int, a0, isStandard=True):
        """
        :param row: table row
        :param col: table col
        :param a0: item
        :param isStandard:
        :return: None
        """
        try:
            k1 = [self.j_value_index, self.j_error_index]; k2 = [3, 4]
            if (isStandard and col in k1) or (not isStandard and col in k2):
                a0 = str(float(a0))
            elif isStandard and col in [2, 3, 4, 5]:
                a0 = str(float(a0))
            else:
                a0 = '%.2f' % float(a0)
        except ValueError:
            a0 = str(a0)
        if isStandard:
            '''Disconnecting'''
            self.tableWidget.cellChanged.disconnect(self.table_1_item_changed)
            self.tableWidget.setItem(row, col, QTableWidgetItem(a0))
            '''Reconnecting'''
            self.tableWidget.cellChanged.connect(self.table_1_item_changed)
        else:
            '''Disconnecting'''
            self.tableWidget_2.cellChanged.disconnect(self.table_2_item_changed)
            self.tableWidget_2.setItem(row, col, QTableWidgetItem(a0))
            '''Reconnecting'''
            self.tableWidget_2.cellChanged.connect(self.table_2_item_changed)

    def std_setting(self):
        UI_StdSetting = StdSettingDialog(self.ufactor, self.line_hor.width())
        UI_StdSetting.Signal_StdSetting.connect(self.change_table_plot)
        UI_StdSetting.exec()
        return

    def unk_setting(self):
        UI_UnkSetting = UnkSettingDialog([self.J_relative_error, self.percentage_center])
        UI_UnkSetting.Signal_UnkSetting.connect(self.change_table_plot_2)
        UI_UnkSetting.exec()
        return

    def change_table_plot(self, a0: float, a1: dict):
        """
        :param a0: ufactor
        :param a1: std table dict
        :return:
        """
        '''calculate new x position based on old ufactor'''
        new_frame_x = [int((i[3].x() - self.line_ver_0.x()) * self.ufactor / a0 + self.line_ver_0.x()) for i in
                       self.sample_info]
        new_frame_width = [int(i[3].width() * self.ufactor / a0) for i in self.sample_info]
        '''assign new ufactor value'''
        self.ufactor = a0
        self.table_dict = a1
        '''delete old sticks'''
        for each_line in self.findChildren(QFrame):
            if 'line_ver_add_' in each_line.objectName():
                each_line.deleteLater()
        '''create new sticks'''
        self.show_scale(self.ufactor)
        '''move pointers based on new ufactor'''
        for i in self.sample_info:
            i[3].setGeometry(i[3].x(), i[3].y(), new_frame_width[self.sample_info.index(i)], i[3].height())
            self.pointer_move(new_frame_x[self.sample_info.index(i)], i[2].y(), i[2].objectName(), isInternal=False)
            self.pointer_move(new_frame_x[self.sample_info.index(i)], i[3].y(), i[3].objectName(), isInternal=False)
            self.pointer_move(new_frame_x[self.sample_info.index(i)], i[1].y(), i[1].objectName(), isInternal=False)
        self.plot()

    def change_table_plot_2(self, J_error_percentage: float, percentage_center: float):
        k1, k2 = J_error_percentage, percentage_center
        for i in range(self.tableWidget_2.rowCount()):
            try:
                j_err = float(self.tableWidget_2.item(i, 4).text())
            except ValueError:
                return
            else:
                self.tableWidget_2.setItem(i, 4, QTableWidgetItem(str(j_err / self.J_relative_error * k1)))
        self.J_relative_error = J_error_percentage
        self.percentage_center = percentage_center
        self.plot()

    def mousePressEvent(self, event: QMouseEvent):
        """
        :param event: mouse press event
        :return: no return
        """
        xpos, ypos = event.x(), event.y()
        print('鼠标点击坐标(%s,%s)' % (xpos, ypos))
        self.pointer_movable = False
        other_frames = ['frame_2', 'frame', 'graphicsView']
        for each_frame in self.findChildren(QFrame):
            if each_frame.objectName() in other_frames:
                continue
            if xpos in range(each_frame.geometry().left(), each_frame.geometry().right()) and ypos in range(
                    each_frame.geometry().top(), each_frame.geometry().bottom()):
                self.pointer_movable = True
                self.selected_frame_name = each_frame.objectName()
                self.selected_pointer_name = str(self.selected_frame_name).split('_frame')[0] + '_pointer'
                self.selected_label_name = str(self.selected_frame_name).split('_frame')[0] + '_label'
                break

    def mouseReleaseEvent(self, event: QMouseEvent):
        """
        :param event: mouse release event
        :return: no return
        """
        xpos, ypos = event.x(), event.y()
        print('鼠标释放坐标(%s,%s)' % (xpos, ypos))
        self.pointer_movable = False
        self.selected_pointer_name = 'No Selected Pointer'
        self.selected_label_name = 'No Selected Pointer'
        self.selected_frame_name = 'No Selected Pointer'
        self.plot()

    def mouseMoveEvent(self, event: QMouseEvent):
        """
        :param event: mouse movement event
        :return: no return
        """
        xpos, ypos = event.x(), event.y()
        # print('鼠标目前坐标(%s,%s), 追踪状态: %s' % (xpos, ypos, self.pointer_movable))
        if self.pointer_movable:
            '''Sequence is important, there will be mistakes if moving label before frame'''
            self.pointer_move(xpos, ypos, self.selected_pointer_name)
            self.pointer_move(xpos, ypos, self.selected_frame_name)
            self.pointer_move(xpos, ypos, self.selected_label_name)
            # self.plot()

    def pointer_move(self, xpos: int, ypos: int, object_name: str, isInternal: bool = True):
        """
        :param xpos: x coordinate of the mouse, origin point is the right-top of the window
        :param ypos: y coordinate
        :param object_name: object name
        :param isInternal: in order to avoid circulate call the function which connecting table content changed
        :return: no return
        """
        if object_name == 'No Selected Pointer':
            return
        for each_object in self.findChildren((QPushButton, QLabel, QFrame)):
            if each_object.objectName() == object_name:
                break
        try:
            current_object = each_object
        except Exception as e:
            print('Error in finding object: %s' % str(e))
            return
        '''Determine the position to move'''
        width_object = current_object.width()
        height_object = current_object.height()
        left_object = current_object.x()
        right_object = int(current_object.x() + width_object)
        left_boundary = self.line_hor.x()
        right_boundary = int(self.line_hor.x() + self.line_hor.width())
        total_width = self.line_hor.width()
        if left_boundary <= xpos <= right_boundary:
            ax = xpos
        elif xpos < left_boundary:
            ax = left_boundary
        else:
            ax = int(left_boundary + total_width)
        ay = current_object.y()
        '''change position of objects'''
        if '_frame' in object_name:
            if right_object > right_boundary:
                right_object = right_boundary
            if left_object < left_boundary:
                left_object = left_boundary
            aw = int(right_object - left_object)
            ah = height_object
            current_object.setGeometry(ax, ay, aw, ah)
        else:
            current_object.setGeometry(int(ax - width_object / 2), ay, width_object, height_object)
        '''Sort the sample list during movement'''
        if '_label' in object_name:
            if isInternal:
                '''Update the sample info list synchronously'''
                k = [i[1].objectName() for i in self.sample_info].index(object_name)
                k1 = (ax - left_boundary) / 10 * self.ufactor  # bottom value
                k2 = self.sample_info[k][3].width() * self.ufactor / 10  # height value
                k3 = self.bottom_value_index if 'standard' in object_name else 1  # col num of bottom
                k4 = self.height_value_index if 'standard' in object_name else 2  # col num of height
                self.sample_info[k][0][k3] = str(k1)
                self.sample_info[k][0][k4] = str(k2)
            '''read and sort sample info'''
            sorted_sample_info = sorted(self.sample_info, key=lambda item: item[1].x())
            table_list = [i[0] for i in sorted_sample_info]
            label_list = [i[1] for i in sorted_sample_info]
            button_list = [i[2] for i in sorted_sample_info]
            frame_list = [i[2] for i in sorted_sample_info]
            '''change label text'''
            standard_num, unknown_num = 0, 0  # record the row number of standard and unknown sample table
            for each_label in label_list:
                index = label_list.index(each_label)
                each_label.setText(str(index + 1))
                '''exchange table content'''
                if 'standard' in each_label.objectName():
                    for col in range(self.tableWidget.columnCount()):
                        self.change_table(standard_num, col, table_list[index][col], isStandard=True)
                    standard_num += 1
                elif 'unknown' in each_label.objectName():
                    for col in range(self.tableWidget_2.columnCount()):
                        self.change_table(unknown_num, col, table_list[index][col], isStandard=False)
                    unknown_num += 1

    def eventFilter(self, a0: QObject, a1: QEvent):
        if type(a0) == QPushButton:
            if type(a1) == QMouseEvent and a1.type() == 2:  # MouseButtonPress = 2
                # print('click a lineEdit: %s' % a0.objectName())
                if a0.objectName() not in ['pushButton_vial_bottom', 'pushButton_vial_top']:
                    self.selected_pointer_name = a0.objectName()
                    self.selected_label_name = a0.objectName().split('_pointer')[0] + '_label'
                    self.selected_frame_name = a0.objectName().split('_pointer')[0] + '_frame'
                    self.pointer_movable = True
            return False

    def show_scale(self, r: float):
        """
        :param r: r represents actual distance in unit of mm of 1 point in window
        :return: None
        """
        main_stick = self.line_ver_0.height()
        second_stick = 5
        mm_list = [int(i / r + self.line_hor.x()) for i in range(int(self.line_hor.width() + 1))]
        cm_list = [int(i / r + self.line_hor.x()) for i in range(0, int(self.line_hor.width() + 1), 10)]
        color_list = [int(i / r + self.line_hor.x()) for i in range(0, int(self.line_hor.width() + 1), 20)]
        name_prefix = 'line_ver_add_'
        for i in mm_list:
            if i > int(self.line_hor.x() + self.line_hor.width()):
                break
            bar_line = QFrame(self)
            bar_line.setFrameShadow(QFrame.Plain)
            bar_line.setLineWidth(1)
            bar_line.setFrameShape(QFrame.VLine)
            bar_line.setObjectName(name_prefix + str(i))
            if i not in cm_list and i not in color_list:
                bar_line.setGeometry(i, int(self.line_hor.y() - second_stick), 1, second_stick)
            elif i not in color_list:
                bar_line.setGeometry(i, int(self.line_hor.y() - main_stick), 1, main_stick)
            else:
                bar_line.setGeometry(i, int(self.line_hor.y() - main_stick), 1, main_stick)
                bar_line.setStyleSheet('color: rgb(255, 0, 0);')
                bar_line.setLineWidth(2)
            bar_line.show()

    def add_standard(self, text='test', isStandard=True):
        """
        :return: add a row in the standard sample table
        """
        if isStandard:
            table_row_num = self.tableWidget.rowCount() + 1
            self.tableWidget.setRowCount(table_row_num)
        else:
            table_row_num = self.tableWidget_2.rowCount() + 1
            self.tableWidget_2.setRowCount(table_row_num)

        '''Assign names of new button and label'''
        sample_type = 'standard' if isStandard else 'unknown'  # 'standard' or 'unknown'
        num = 1
        while '_' + str(num) in str([i.objectName() for i in self.findChildren(QLabel)]):
            num += 1
        new_button_name = 'sample_' + sample_type + '_' + str(num) + '_pointer'
        new_label_name = 'sample_' + sample_type + '_' + str(num) + '_label'
        new_frame_name = 'sample_' + sample_type + '_' + str(num) + '_frame'
        '''Color map'''
        colors = {'standard': 'yellow', 'unknown': 'blue'}

        '''Determine the bottom and height value'''
        package_bottom_value = 1 * num  # default value in cm
        package_height_value = float(0.5)  # default value in cm
        ufactor: float = self.ufactor  # ufactor = scale / self.frame.width(), unit = cm / x_size
        '''Determine the geometry'''
        x_pos = int(package_bottom_value / ufactor * 10 + self.frame.x())
        y_pos = self.frame.y()
        try:
            max_xpos = sorted(self.sample_info, key=lambda item: item[1].x())[-1][3].x()
            if x_pos < max_xpos:
                x_pos = int(max_xpos + 1 / self.ufactor)
        except Exception as e:
            # print('Error in calculating max_xpos: %s' % str(e))
            pass
        '''Determine the width and height'''
        w_pointer = self.pushButton_vial_bottom.width()
        h_pointer = self.pushButton_vial_bottom.height()
        w_label = self.pushButton_vial_bottom_label.width()
        h_label = self.pushButton_vial_bottom_label.height()
        w_frame = int(package_height_value * 10 / ufactor)
        h_frame = self.frame.height()
        '''Default zero position'''
        zero_xpos = int(self.pushButton_vial_bottom.x())
        zero_ypos = int(self.pushButton_vial_bottom.y())

        '''Create new pointer'''
        button_pointer = QPushButton(self)
        button_pointer.setGeometry(zero_xpos, zero_ypos, w_pointer, h_pointer)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(button_pointer.sizePolicy().hasHeightForWidth())
        button_pointer.setSizePolicy(sizePolicy)
        button_pointer.setMouseTracking(True)
        button_pointer.setStyleSheet("QPushButton{background: transparent;}")
        icon = QIcon()
        icon.addPixmap(QPixmap(os.path.dirname(__file__) + "/../../icons/pointer_green.png"), QIcon.Normal, QIcon.Off)
        button_pointer.setIcon(icon)
        button_pointer.setIconSize(QSize(10, 10))
        button_pointer.setObjectName(new_button_name)
        button_pointer.show()
        button_pointer.installEventFilter(self)

        '''Create new label'''
        label_pointer = QLabel(self)
        label_pointer.setGeometry(zero_xpos, int(zero_ypos + 10), w_label, h_label)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(label_pointer.sizePolicy().hasHeightForWidth())
        label_pointer.setSizePolicy(sizePolicy)
        label_pointer.setAlignment(Qt.AlignCenter)
        label_pointer.setObjectName(new_label_name)
        label_pointer.setText(str(num))
        label_pointer.show()

        '''Create new frame'''
        frame_pointer = QFrame(self)
        frame_pointer.setGeometry(self.frame.x(), self.frame.y(), w_frame, h_frame)
        frame_pointer.setStyleSheet("QFrame{background: %s; border: 1px groove gray;}" % colors[sample_type])
        frame_pointer.setFrameShape(QFrame.StyledPanel)
        frame_pointer.setFrameShadow(QFrame.Raised)
        frame_pointer.setObjectName(new_frame_name)
        frame_pointer.show()
        '''Write table'''
        if isStandard:
            b = text + str(num)
            self.change_table(table_row_num - 1, self.bottom_value_index, '%.2f' % package_bottom_value)  # bottom
            self.change_table(table_row_num - 1, self.height_value_index, '%.2f' % package_height_value)  # height
            self.change_table(table_row_num - 1, 0, b)  # number
            self.change_table(table_row_num - 1, 1, b)  # name
            self.change_table(table_row_num - 1, 2, b)  # age
            self.change_table(table_row_num - 1, 3, b)  # error
            self.change_table(table_row_num - 1, 4, b)  # 40r/39k
            self.change_table(table_row_num - 1, 5, b)  # error
            self.change_table(table_row_num - 1, 8, b)  # J value
            self.change_table(table_row_num - 1, 9, b)  # error
            table_list = [self.tableWidget.item(table_row_num - 1, col).text() for col in
                          range(self.tableWidget.columnCount())]
        else:
            b = text + str(num)
            self.change_table(table_row_num - 1, 0, b, isStandard=False)  # num
            self.change_table(table_row_num - 1, 1, b, isStandard=False)  # bottom
            self.change_table(table_row_num - 1, 2, b, isStandard=False)  # height
            self.change_table(table_row_num - 1, 3, b, isStandard=False)  # J value
            self.change_table(table_row_num - 1, 4, b, isStandard=False)  # error
            table_list = [self.tableWidget_2.item(table_row_num - 1, col).text() for col in
                          range(self.tableWidget_2.columnCount())]

        '''create tuple for each sample'''
        each_sample = (table_list, label_pointer, button_pointer, frame_pointer)
        self.sample_info.append(each_sample)

        '''Setting geometry by pointer move function'''
        self.pointer_move(x_pos, y_pos, new_button_name)
        self.pointer_move(x_pos, y_pos, new_frame_name)
        self.pointer_move(x_pos, y_pos, new_label_name)
        '''plotting'''
        self.plot()

    def del_table(self, a0: int = -1, isStandard: bool = True):
        if isStandard:
            table = self.tableWidget
            sample_type = 'standard'
        else:
            table = self.tableWidget_2
            sample_type = 'unknown'
        if a0 != -1 and a0 in range(table.rowCount()):
            row = a0
        elif table.selectedIndexes():
            row = table.selectedIndexes()[0].row()
        else:
            return
        sorted_table_list = sorted(self.sample_info, key=lambda item: item[1].x())
        num = 0
        for i in sorted_table_list:
            if sample_type in i[1].objectName():
                num += 1
                if num == row + 1:
                    index = sorted_table_list.index(i)  # obtain the index of changed item in sample info list
                    [label, pointer, frame] = i[1:4]
                    break
        try:
            '''remove event filter'''
            pointer.removeEventFilter(self)
            '''delete object'''
            label.deleteLater()
            pointer.deleteLater()
            frame.deleteLater()
            '''delete table'''
            table.removeRow(row)
            '''delete recorded list'''
            self.sample_info.remove(sorted_table_list[index])
        except Exception as e:
            print('Error in deleting row: %s' % str(e))
        '''update label number'''
        sorted_table_list = sorted(self.sample_info, key=lambda item: item[1].x())
        for each_sample in sorted_table_list:
            each_sample[1].setText(str(sorted_table_list.index(each_sample) + 1))
        '''replot'''
        self.plot()

    def plot(self):
        """
        :return: no return
        """
        '''read table'''
        sample_list = sorted(self.sample_info, key=lambda item: item[1].x())
        '''create fig and canvas'''
        fig = plt.Figure(dpi=100, constrained_layout=True)
        canvas = FigureCanvas(fig)
        '''set axes'''
        canvas.axes = fig.subplots()
        font = {'family': 'Times New Roman', 'size': 8, 'style': 'normal'}
        xmax = int(self.line_hor.x() + self.line_hor.width()) * self.ufactor / 10
        canvas.axes.set_xlim(0, xmax)
        canvas.axes.set_xlabel('', fontdict=font)
        canvas.axes.tick_params(labelsize=6, direction='in')

        '''plot scatter'''
        x_standard_list = []
        y_standard_list = []
        x_unknown_list = []
        for i in sample_list:
            if 'standard' in i[1].objectName():
                try:
                    bottom = float(i[0][self.bottom_value_index])
                    height = float(i[0][self.height_value_index])
                    x = bottom + height * self.percentage_center
                    y = float(i[0][self.j_value_index])
                    color = 'yellow'
                except ValueError:
                    continue
                else:
                    x_standard_list.append(x)
                    y_standard_list.append(y)
                    canvas.axes.scatter(x, y, c=color, edgecolors='black', marker='o', s=20)
            elif 'unknown' in i[1].objectName():
                try:
                    x = float(i[0][1]) + float(i[0][2]) * self.percentage_center
                except ValueError:
                    continue
                else:
                    x_unknown_list.append(x)

        '''plot fitting line'''
        color_line = ['black', '#996699', '#CCCC99', '#669999']
        '''average'''
        try:
            mean_y = sum(y_standard_list) / len(y_standard_list)
            canvas.axes.plot([0, xmax], [mean_y, mean_y], c=color_line[0], linewidth=1, linestyle='--')
        except Exception as e:
            # print('Error in average fitting: %s' % str(e))
            y_unknown_average_list = ['None'] * len(x_unknown_list)
            pass
        else:
            y_unknown_average_list = [mean_y] * len(x_unknown_list)
        '''linest: y = b + m * x'''
        try:
            k = ProFunctions.intercept_linest(y_standard_list, x_standard_list)
            b, m = k[0], k[5][0]
            k0 = 0; k1 = b
            k2 = xmax; k3 = k2 * m + k1
            canvas.axes.plot([k0, k2], [k1, k3], c=color_line[1], linewidth=1)
        except Exception as e:
            # print('Error in line fitting: %s' % str(e))
            y_unknown_line_list = ['None'] * len(x_unknown_list)
            line_fit_result = 'None'
        else:
            y_unknown_line_list = list(map(lambda xi: b + m * xi, x_unknown_list))
            line_fit_result = 'y = b + m * x\nb: %s\nm: %s\nr2: %s' % (b, m, k[3])
        '''para fit: y = b + m1 * x + m2 * x ^ 2'''
        try:
            k = ProFunctions.intercept_parabolic(y_standard_list, x_standard_list)
            b, m1, m2 = k[0], k[5][0], k[5][1]
            xlst_para = [i for i in np.arange(0, xmax, 0.1)]
            ylst_para = list(map(lambda xi: b + m1 * xi + m2 * xi * xi, xlst_para))
            canvas.axes.plot(xlst_para, ylst_para, c=color_line[2], linewidth=1)
        except Exception as e:
            # print('Error in para fitting: %s' % str(e))
            y_unknown_para_list = ['None'] * len(x_unknown_list)
            para_fit_result = 'None'
        else:
            y_unknown_para_list = list(map(lambda xi: b + m1 * xi + m2 * xi * xi, x_unknown_list))
            para_fit_result = 'y = b + m1 * x + m2 * x ^ 2\nb: %s\nm1: %s\nm2: %s\nr2: %s' % (b, m1, m2, k[3])
        '''exp fit: y = m * exp(c * x) + b '''
        try:
            slope = ProFunctions.intercept_linest(y_standard_list, x_standard_list)[5][0]
            curvature = ProFunctions.intercept_parabolic(y_standard_list, x_standard_list)[5][1]
            k = ProFunctions.intercept_exponential(y_standard_list, x_standard_list, slope, curvature)
            [m, c, b] = k[5]
            xlst_exp = [i for i in np.arange(0, xmax, 0.1)]
            ylst_exp = list(map(lambda xi: m * exp(c * xi) + b, xlst_exp))
            canvas.axes.plot(xlst_exp, ylst_exp, c=color_line[3], linewidth=1)
        except Exception as e:
            # print('Error in exp fitting: %s' % str(e))
            y_unknown_exp_list = ['None'] * len(x_unknown_list)
            exp_fit_result = 'None'
        else:
            y_unknown_exp_list = list(map(lambda xi: m * exp(c * xi) + b, x_unknown_list))
            exp_fit_result = 'y = m * exp(c * x) + b\nm: %s\nc: %s\nb: %s\nr2: %s' % (m, c, b, k[3])
        '''calculating and showing J value of unknown sample'''
        color = 'blue'
        if self.radioButton_line.isChecked():
            y_unknown_list = y_unknown_line_list
            fit_result = line_fit_result
        elif self.radioButton_exp.isChecked():
            y_unknown_list = y_unknown_exp_list
            fit_result = exp_fit_result
        else:
            y_unknown_list = y_unknown_para_list
            fit_result = para_fit_result
        try:
            for i in range(len(x_unknown_list)):
                if isinstance(y_unknown_list[i], float):
                    canvas.axes.scatter(x_unknown_list[i], y_unknown_list[i], c=color, edgecolors='black', marker='o',
                                        s=20)
                    error = y_unknown_list[i] * self.J_relative_error
                else:
                    error = 'None'
                self.tableWidget_2.setItem(i, 3, QTableWidgetItem(str(y_unknown_list[i])))
                self.tableWidget_2.setItem(i, 4, QTableWidgetItem(str(error)))
            self.textEdit.setText(fit_result)
        except Exception as e:
            # print('Error in plot unknown scatter: %s' % str(e))
            pass
        '''add text'''
        fontsize_pt = 8
        y_height_pt = fig.get_figheight() * 72  # inch * pdi, https://www.cnblogs.com/lijunjie9502/p/10327151.html
        y_height_scale = canvas.axes.get_ylim()[1] - canvas.axes.get_ylim()[0]
        ratio = y_height_scale / y_height_pt
        text_x_pos = xmax - xmax / (fig.get_figwidth() * 72) * (45 / 2)
        try:
            canvas.axes.text(text_x_pos, mean_y + ratio * fontsize_pt / 2, 'Average', fontsize=fontsize_pt,
                             horizontalalignment='center', verticalalignment='center', c=color_line[0])
        except (NameError, IndexError):
            pass
        try:
            canvas.axes.text(text_x_pos, k3 + ratio * fontsize_pt / 2, 'LineFit', fontsize=fontsize_pt,
                             horizontalalignment='center', verticalalignment='center', c=color_line[1])
        except (NameError, IndexError):
            pass
        try:
            canvas.axes.text(text_x_pos, ylst_para[len(ylst_para) - 1] + ratio * fontsize_pt / 2, 'ParaFit',
                             fontsize=fontsize_pt, horizontalalignment='center', verticalalignment='center',
                             c=color_line[2])
        except (NameError, IndexError):
            pass
        try:
            canvas.axes.text(text_x_pos, ylst_exp[len(ylst_exp) - 1] + ratio * fontsize_pt / 2, 'ExpFit',
                             fontsize=fontsize_pt, horizontalalignment='center', verticalalignment='center',
                             c=color_line[3])
        except (NameError, IndexError):
            pass
        '''update canvas'''
        try:
            self.verticalLayout.removeWidget(self.canvas)
            self.canvas.deleteLater()
        except AttributeError:
            pass
        self.canvas = canvas
        self.verticalLayout.addWidget(self.canvas)


class StdSettingDialog(QDialog, UI_StdSettingDialog.Ui_Dialog_StdSetting):
    Signal_StdSetting = pyqtSignal(float, dict)

    def __init__(self, ufactor, width):
        super(StdSettingDialog, self).__init__()
        self.setupUi(self)
        self.spinBox.valueChanged.connect(lambda a0: self.get_total_height(a0, width))
        self.spinBox.setValue(int(1 / ufactor))
        self.pushButton_addrow.clicked.connect(self.add_row)
        self.pushButton_delrow.clicked.connect(self.del_row)
        self.pushButton_apply.clicked.connect(self.apply)
        self.write_table()

    def add_row(self):
        row_count = self.tableWidget.rowCount() + 1
        self.tableWidget.setRowCount(row_count)

    def del_row(self):
        if self.tableWidget.selectedIndexes():
            index = self.tableWidget.selectedIndexes()[0].row()
            self.tableWidget.removeRow(index)

    def apply(self):
        try:
            ufactor = 1 / int(self.spinBox.value())
        except Exception as e:
            print('Error in emit signal: %s' % str(e))
            self.spinBox.setvalue(4)
            ufactor = 0.25
        table_dict = self.get_table()
        '''save'''
        try:
            with open(os.path.dirname(__file__) + '/../../settings/std_dict.json', 'w') as file:
                jsonData = json.dumps(table_dict, indent=4, separators=(',', ': '))
                file.write(jsonData)
        except Exception as e:
            print('Error in save file: %s' % str(e))
        self.Signal_StdSetting.emit(ufactor, table_dict)
        self.close()

    def get_total_height(self, a0: int, width: int):
        if a0 <= 0:
            a0 = 4
            self.spinBox.setValue(a0)
        self.lineEdit.setText(str(1 / a0 * width / 10))

    def write_table(self):
        try:
            with open(os.path.dirname(__file__) + '/../../settings/std_dict.json', 'r') as file:
                table_dict = json.load(file)
        except Exception as e:
            print('Error in open file: %s' % str(e))
        else:
            table_list = list(table_dict.values())
            self.tableWidget.setRowCount(len(table_list))
            for row in range(len(table_list)):
                for col in range(self.tableWidget.columnCount()):
                    self.tableWidget.setItem(row, col, QTableWidgetItem(table_list[row][col]))

    def get_table(self):
        table = []
        for row in range(self.tableWidget.rowCount()):
            table.append([])
            for col in range(self.tableWidget.columnCount()):
                try:
                    text = self.tableWidget.item(row, col).text()
                except Exception as e:
                    print('Error in getting table%s' % str(e))
                    text = ''
                table[row].append(text)
        table_dict = {i[0]: i for i in table}
        return table_dict


class UnkSettingDialog(QDialog, UI_UnkSettingDialog.Ui_Dialog):
    Signal_UnkSetting = pyqtSignal(float, float)

    def __init__(self, params):
        super(UnkSettingDialog, self).__init__()
        self.setupUi(self)
        self.lineEdit.setText(str(params[0] * 100))
        self.lineEdit_2.setText(str(params[1] * 100))
        self.pushButton.clicked.connect(self.apply)

        regx = QRegExp('^\\d+(\\.\\d+)?$')  # 非负浮点数
        validator = QRegExpValidator(regx, self)
        self.lineEdit.setValidator(validator)
        self.lineEdit_2.setValidator(validator)

    def apply(self):
        k0 = self.lineEdit.text()
        k1 = self.lineEdit_2.text()
        try:
            k0 = float(k0) / 100
            k1 = float(k1) / 100
        except ValueError:
            return
        else:
            self.Signal_UnkSetting.emit(k0, k1)
            self.close()


class FileFilterDialog(QDialog, UI_FileFilter.Ui_Dialog):

    apply_clicked: bool = False
    standard_index: List[int] = []
    unknown_index: List[int] = []
    std_col_index: List[int] = [1, 0, 0, 0, 0, 0, 2, 3, 0, 0]
    unk_col_index: List[int] = [1, 2, 3]

    def __init__(self, file_list):
        super(FileFilterDialog, self).__init__()
        self.setupUi(self)

        self.label_hint_2.setStyleSheet('color: rgb(255, 0, 0);')
        self.pushButton.clicked.connect(lambda: self.apply(len(file_list)))

        text = ''
        for line in file_list:
            for i in line:
                if line.index(i) == 0:
                    num = '%02d' % int(file_list.index(line) + 1)
                    text = text + num + ':  ' + i + '\t'
                elif line.index(i) == len(line) - 1:
                    text = text + i + '\n'
                else:
                    text = text + i + '\t'
        self.textBrowser.setText(text)
        self.row_count = len(file_list)
        self.col_counts = [len(i) for i in file_list]
        self.file_list = file_list
        self.file_list_backup = copy.deepcopy(file_list)

        '''constrain the input contents'''
        regx = QRegExp('^\d+$')  # Non-negative int numbers, https://blog.csdn.net/wangrunmin/article/details/7377117
        validator = QRegExpValidator(regx, self)
        for i in self.findChildren(QLineEdit):
            if 'rows' not in i.objectName():
                i.setValidator(validator)
            elif 'standard' in i.objectName():
                i.textChanged.connect(lambda item: self.get_row_index(item, isStandard=True))
            elif 'unknown' in i.objectName():
                i.textChanged.connect(lambda item: self.get_row_index(item, isStandard=False))

        self.lineEdit.textChanged.connect(lambda item: self.get_col_index(item, 0))
        self.lineEdit_2.textChanged.connect(lambda item: self.get_col_index(item, 1))
        self.lineEdit_3.textChanged.connect(lambda item: self.get_col_index(item, 2))
        self.lineEdit_4.textChanged.connect(lambda item: self.get_col_index(item, 3))
        self.lineEdit_5.textChanged.connect(lambda item: self.get_col_index(item, 4))
        self.lineEdit_6.textChanged.connect(lambda item: self.get_col_index(item, 5))
        self.lineEdit_7.textChanged.connect(lambda item: self.get_col_index(item, 6))
        self.lineEdit_8.textChanged.connect(lambda item: self.get_col_index(item, 7))
        self.lineEdit_9.textChanged.connect(lambda item: self.get_col_index(item, 8))
        self.lineEdit_10.textChanged.connect(lambda item: self.get_col_index(item, 9))

        self.lineEdit_11.textChanged.connect(lambda item: self.get_col_index(item, 0, isStandard=False))
        self.lineEdit_12.textChanged.connect(lambda item: self.get_col_index(item, 1, isStandard=False))
        self.lineEdit_13.textChanged.connect(lambda item: self.get_col_index(item, 2, isStandard=False))

    def apply(self, row_count: int):
        if self.standard_index or self.unknown_index:
            pass
        else:
            self.standard_index = [i for i in range(row_count)]
            self.unknown_index = []
        if self.standard_index:
            std_max_col_num = max([self.col_counts[i - 1] for i in self.standard_index])
        else:
            std_max_col_num = 999
        if self.unknown_index:
            unk_max_col_num = max([self.col_counts[i - 1] for i in self.unknown_index])
        else:
            unk_max_col_num = 999
        try:
            if max(self.std_col_index) <= std_max_col_num + 1 and max(self.unk_col_index) <= unk_max_col_num + 1:
                for i in self.std_col_index:
                    if self.std_col_index.count(i) != 1 and i != 0:
                        raise ValueError
                for i in self.unk_col_index:
                    if self.unk_col_index.count(i) != 1 and i != 0:
                        raise ValueError
            else:
                raise ValueError
        except Exception as e:
            print('Error in recording index: %s' % str(e))
            return
        else:
            age_factor = 1 if self.comboBox_age.currentIndex() == 0 else 1
            age_error_factor = 1 if self.comboBox_age_error.currentIndex() == 0 else 0.5
            ratio_error_factor = 1 if self.comboBox_ratio_error.currentIndex() == 0 else 0.5
            bottom_factor = 1 if self.comboBox_bottom.currentIndex() == 0 else 0.1
            height_factor = 1 if self.comboBox_height.currentIndex() == 0 else 0.1
            j_error_factor = 1 if self.comboBox_J_error.currentIndex() == 0 else 0.5
            bottom_2_factor = 1 if self.comboBox_bottom_2.currentIndex() == 0 else 0.1
            height_2_factor = 1 if self.comboBox_height_2.currentIndex() == 0 else 0.1
            try:
                for row in self.standard_index:
                    if self.std_col_index[2] != 0:
                        k = float(self.file_list[row - 1][self.std_col_index[2] - 1]) * age_factor
                        self.file_list[row - 1][self.std_col_index[2] - 1] = str(k)
                    if self.std_col_index[3] != 0:
                        k = float(self.file_list[row - 1][self.std_col_index[3] - 1]) * age_error_factor
                        self.file_list[row - 1][self.std_col_index[3] - 1] = str(k)
                    if self.std_col_index[5] != 0:
                        k = float(self.file_list[row - 1][self.std_col_index[5] - 1]) * ratio_error_factor
                        self.file_list[row - 1][self.std_col_index[5] - 1] = str(k)
                    if self.std_col_index[6] != 0:
                        k = float(self.file_list[row - 1][self.std_col_index[6] - 1]) * bottom_factor
                        self.file_list[row - 1][self.std_col_index[6] - 1] = str(k)
                    if self.std_col_index[7] != 0:
                        k = float(self.file_list[row - 1][self.std_col_index[7] - 1]) * height_factor
                        self.file_list[row - 1][self.std_col_index[7] - 1] = str(k)
                    if self.std_col_index[9] != 0:
                        k = float(self.file_list[row - 1][self.std_col_index[9] - 1]) * j_error_factor
                        self.file_list[row - 1][self.std_col_index[9] - 1] = str(k)
                for row in self.unknown_index:
                    if self.unk_col_index[1] != 0:
                        k = float(self.file_list[row - 1][self.unk_col_index[1] - 1]) * bottom_2_factor
                        self.file_list[row - 1][self.unk_col_index[1] - 1] = str(k)
                    if self.unk_col_index[2] != 0:
                        k = float(self.file_list[row - 1][self.unk_col_index[2] - 1]) * height_2_factor
                        self.file_list[row - 1][self.unk_col_index[2] - 1] = str(k)
            except Exception as e:
                print('Error in changing units: %s' % str(e))
                self.file_list = copy.deepcopy(self.file_list_backup)
            else:
                self.apply_clicked = True
                self.close()

    def get_row_index(self, text: str, isStandard: bool = True):
        try:
            index_list = []
            text_list = []
            for i in text.split(','):
                for j in i.split('，'):
                    for k in j.split('.'):
                        text_list.append(k)
            if '' in text_list:
                text_list.remove('')
            for i in text_list:
                k1 = i.split('-')
                if len(k1) == 1:
                    index_list.append(int(i))
                elif len(k1) == 2:
                    for j in range(min([int(i) for i in k1]), max([int(i) for i in k1]) + 1):
                        index_list.append(j)
                else:
                    raise ValueError
            index_list = list(set(index_list))
            if isStandard:
                self.standard_index = index_list
            else:
                self.unknown_index = index_list
            if isStandard and self.unknown_index:
                for i in index_list:
                    if i in self.unknown_index:
                        raise ValueError
            elif not isStandard and self.standard_index:
                for i in index_list:
                    if i in self.standard_index:
                        raise ValueError
            for i in index_list:
                if i > self.row_count:
                    raise ValueError
        except Exception as e:
            # print('Error in creating index list: %s' % str(e))
            '''undo show hint'''
            if text == '':
                self.label_hint.clear()
                self.pushButton.setDisabled(False)
                if isStandard:
                    self.lineEdit_standard_rows.setStyleSheet('')
                else:
                    self.lineEdit_unknown_rows.setStyleSheet('')
                return
            '''show hint'''
            self.label_hint.setText('Invalid input!')
            self.pushButton.setDisabled(True)
            if isStandard:
                self.lineEdit_standard_rows.setStyleSheet('border: 1px solid rgb(255, 0, 0);')
            else:
                self.lineEdit_unknown_rows.setStyleSheet('border: 1px solid rgb(255, 0, 0);')
        else:
            self.label_hint.clear()
            self.pushButton.setDisabled(False)
            self.lineEdit_unknown_rows.setStyleSheet('')
            self.lineEdit_standard_rows.setStyleSheet('')

    def get_col_index(self, text: str, index: int, isStandard: bool = True):
        self.label_hint_2.setText('')
        try:
            int(text)
        except ValueError:
            self.label_hint_2.setText('Invalid input!')
        else:
            if isStandard:
                self.std_col_index[index] = int(text)
            else:
                self.unk_col_index[index] = int(text)
            for i in self.std_col_index:
                if self.std_col_index.count(i) != 1 and i != 0:
                    self.label_hint_2.setText('Invalid input!')
            for i in self.unk_col_index:
                if self.unk_col_index.count(i) != 1 and i != 0:
                    self.label_hint_2.setText('Invalid input!')


if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    UI = SubWindowJvalueCalculation()
    UI.show()
    sys.exit(app.exec())
