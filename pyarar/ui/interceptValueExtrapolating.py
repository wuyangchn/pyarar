import copy
import os
import sys
import numpy as np
import scipy.stats as stats
import pyqtgraph as pg
from itertools import combinations
from math import exp

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QWidget, QGridLayout, QPushButton, QProgressBar, QFontDialog, QColorDialog, \
    QMessageBox, QApplication
import xlwt
from PyQt5 import QtCore
from pyarar.ui import UI_ExtrapolationWindow
import pyarar.FuncsCalc as FuncsCalc


class SubWindowExtrapolation(QDialog, UI_ExtrapolationWindow.Ui_Dialog):
    Signal_extrapolation = QtCore.pyqtSignal(str)

    def __init__(self, list_all_step, name_of_sample):
        super(SubWindowExtrapolation, self).__init__()
        self.setupUi(self)
        self.path = ""

        # defining class variables
        self.step_data = copy.deepcopy(list_all_step)
        self.sample_name = copy.deepcopy(name_of_sample)

        self.sn: int = None
        self.step_info_text: str = None
        self.analysing_time: list = None
        self.argon_40: list = None
        self.argon_39: list = None
        self.argon_38: list = None
        self.argon_37: list = None
        self.argon_36: list = None
        self.selected_list: list = None
        self.number: int = None
        self.x_scatter: list = None
        self.unselected_list: list = []  # 编号从1开始
        self.extra_result = []
        self.step_info = []
        self.btn_set = []
        self.blank_type_name = ['BLK', 'B', 'b']
        self.sample_type_name = ['UNKNOWN', 'air']

        self.point_number = len(self.step_data[0])
        self.step_number = len(self.step_data)

        # 写窗口标题
        dialog_title = "Filter-%s" % self.sample_name
        self.setWindowTitle(dialog_title)

        # 在顶部为每一个阶段创建按钮
        for i in range(self.step_number):
            self.create_button(i)
            list = [[], [], [], [], []]
            self.unselected_list.append(copy.deepcopy(list))
            self.extra_result.append(copy.deepcopy(list))
            self.step_info.append([])

        # 创建“自动选择”按钮，即Auto Select
        # 利用确定的比较程序，自动选择最佳数据点
        self.btn_autoselect = QPushButton('%s' % 'Auto Select')
        self.horizontalLayout_4.addWidget(self.btn_autoselect)
        self.btn_autoselect.clicked.connect(lambda: self.auto_select(self.step_data))

        # 创建“保存”按钮，即Save Result
        # 点击该窗口，保存选择数据点的结果，安装OriginalExcel的文件形式书写，包括零时刻截距和本底
        self.btn_save = QPushButton('%s' % 'Save Result')
        self.horizontalLayout_4.addWidget(self.btn_save)
        self.btn_save.clicked.connect(
            lambda: self.save_result([self.extra_result, self.unselected_list, self.step_info]))

        # 创建“计算”按钮，即CALC
        # 点击该按钮，选择数据点的窗口消失，同时在主窗口中打开保存的文件
        self.btn_calc = QPushButton('%s' % 'CALC')
        self.horizontalLayout_4.addWidget(self.btn_calc)
        self.btn_calc.clicked.connect(
            lambda: self.calc([self.extra_result, self.unselected_list, self.step_info]))

        # 创建“无处理”按钮，即SKIP
        # 点击该按钮，选择数据点的窗口消失，同时在主窗口中打开保存的文件
        self.btn_skip = QPushButton('%s' % 'SKIP')
        self.horizontalLayout_4.addWidget(self.btn_skip)
        self.btn_skip.clicked.connect(lambda: self.skip(self.step_data))

        # 实例化一个进度条
        self.progressBar = QProgressBar()
        self.horizontalLayout_3.addWidget(self.progressBar)

        # 修改字体字号按钮
        self.btnGetFont.clicked.connect(self.set_font)
        self.btnGetBackgroundColor.clicked.connect(self.set_background_color)
        # 设置默认字体
        font = QFont('Microsoft YaHei Ui', 10)
        self.textBrowser.setFont(font)

        # 确定拟合计算零时刻质谱信号值时的最小拟合点数，一般认为5个是最低可接受的值
        self.least_point_used_to_fit = 5
        # 衡量拟合零时刻质谱信号量的标准（用R_square表示），一般认为0.95代表拟合相对完美
        self.best_fit_R_square = 0.95

        self.plot_widget_closeFigure = QWidget()  # 实例化一个widget部件作为K线图部件
        self.plot_layout_closeFigure = QGridLayout()  # 实例化一个网格布局层
        self.plot_widget_closeFigure.setLayout(self.plot_layout_closeFigure)  # 设置线图部件的布局层
        self.plot_plt_closeFigure = pg.PlotWidget()  # 实例化一个绘图部件
        self.plot_plt_closeFigure.showGrid(x=True, y=True)  # 显示图形网格
        self.plot_layout_closeFigure.addWidget(self.plot_plt_closeFigure)  # 添加绘图部件到线图部件的网格布局层
        self.Layout_closeFigure.addWidget(self.plot_widget_closeFigure)  # 将上述部件添加到布局层中

        self.plot_widget_littleFigure2_1 = QWidget()  # 实例化一个widget部件作为K线图部件
        self.plot_layout_littleFigure2_1 = QGridLayout()  # 实例化一个网格布局层
        self.plot_widget_littleFigure2_1.setLayout(self.plot_layout_littleFigure2_1)  # 设置线图部件的布局层
        self.plot_plt_littleFigure2_1 = pg.PlotWidget()  # 实例化一个绘图部件
        self.plot_plt_littleFigure2_1.showGrid(x=True, y=True)  # 显示图形网格
        self.plot_layout_littleFigure2_1.addWidget(self.plot_plt_littleFigure2_1)  # 添加绘图部件到线图部件的网格布局层
        self.Layout_littleFigure.replaceWidget(self.frame_1, self.plot_widget_littleFigure2_1)  # 将上述部件添加到布局层中

        self.plot_widget_littleFigure2_2 = QWidget()  # 实例化一个widget部件作为K线图部件
        self.plot_layout_littleFigure2_2 = QGridLayout()  # 实例化一个网格布局层
        self.plot_widget_littleFigure2_2.setLayout(self.plot_layout_littleFigure2_2)  # 设置线图部件的布局层
        self.plot_plt_littleFigure2_2 = pg.PlotWidget()  # 实例化一个绘图部件
        self.plot_plt_littleFigure2_2.showGrid(x=True, y=True)  # 显示图形网格
        self.plot_layout_littleFigure2_2.addWidget(self.plot_plt_littleFigure2_2)  # 添加绘图部件到线图部件的网格布局层
        self.Layout_littleFigure.replaceWidget(self.frame_2, self.plot_widget_littleFigure2_2)  # 将上述部件添加到布局层中

        self.plot_widget_littleFigure2_3 = QWidget()  # 实例化一个widget部件作为K线图部件
        self.plot_layout_littleFigure2_3 = QGridLayout()  # 实例化一个网格布局层
        self.plot_widget_littleFigure2_3.setLayout(self.plot_layout_littleFigure2_3)  # 设置线图部件的布局层
        self.plot_plt_littleFigure2_3 = pg.PlotWidget()  # 实例化一个绘图部件
        self.plot_plt_littleFigure2_3.showGrid(x=True, y=True)  # 显示图形网格
        self.plot_layout_littleFigure2_3.addWidget(self.plot_plt_littleFigure2_3)  # 添加绘图部件到线图部件的网格布局层
        self.Layout_littleFigure.replaceWidget(self.frame_3, self.plot_widget_littleFigure2_3)  # 将上述部件添加到布局层中

        self.plot_widget_littleFigure2_4 = QWidget()  # 实例化一个widget部件作为K线图部件
        self.plot_layout_littleFigure2_4 = QGridLayout()  # 实例化一个网格布局层
        self.plot_widget_littleFigure2_4.setLayout(self.plot_layout_littleFigure2_4)  # 设置线图部件的布局层
        self.plot_plt_littleFigure2_4 = pg.PlotWidget()  # 实例化一个绘图部件
        self.plot_plt_littleFigure2_4.showGrid(x=True, y=True)  # 显示图形网格
        self.plot_layout_littleFigure2_4.addWidget(self.plot_plt_littleFigure2_4)  # 添加绘图部件到线图部件的网格布局层
        self.Layout_littleFigure.replaceWidget(self.frame_4, self.plot_widget_littleFigure2_4)  # 将上述部件添加到布局层中

        self.plot_widget_littleFigure2_5 = QWidget()  # 实例化一个widget部件作为K线图部件
        self.plot_layout_littleFigure2_5 = QGridLayout()  # 实例化一个网格布局层
        self.plot_widget_littleFigure2_5.setLayout(self.plot_layout_littleFigure2_5)  # 设置线图部件的布局层
        self.plot_plt_littleFigure2_5 = pg.PlotWidget()  # 实例化一个绘图部件
        self.plot_plt_littleFigure2_5.showGrid(x=True, y=True)  # 显示图形网格
        self.plot_layout_littleFigure2_5.addWidget(self.plot_plt_littleFigure2_5)  # 添加绘图部件到线图部件的网格布局层
        self.Layout_littleFigure.replaceWidget(self.frame_5, self.plot_widget_littleFigure2_5)  # 将上述部件添加到布局层中

        self.figure0_proxy = pg.SignalProxy(
            self.plot_plt_closeFigure.plot().scene().sigMouseClicked, rateLimit=60,
            slot=self.mouse_clicked_close_figure)
        self.figure1_proxy = pg.SignalProxy(
            self.plot_plt_littleFigure2_1.plot().scene().sigMouseClicked, rateLimit=60,
            slot=self.mouse_clicked_little_figure_1)
        self.figure2_proxy = pg.SignalProxy(
            self.plot_plt_littleFigure2_2.plot().scene().sigMouseClicked, rateLimit=60,
            slot=self.mouse_clicked_little_figure_2)
        self.figure3_proxy = pg.SignalProxy(
            self.plot_plt_littleFigure2_3.plot().scene().sigMouseClicked, rateLimit=60,
            slot=self.mouse_clicked_little_figure_3)
        self.figure4_proxy = pg.SignalProxy(
            self.plot_plt_littleFigure2_4.plot().scene().sigMouseClicked, rateLimit=60,
            slot=self.mouse_clicked_little_figure_4)
        self.figure5_proxy = pg.SignalProxy(
            self.plot_plt_littleFigure2_5.plot().scene().sigMouseClicked, rateLimit=60,
            slot=self.mouse_clicked_little_figure_5)

        # 绘图
        self.draw_figures(self.step_data, 1)

    def set_font(self):
        font, ok = QFontDialog.getFont()
        print(font)
        if ok:
            self.textBrowser.setFont(font)

    def set_background_color(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.textBrowser.setStyleSheet("QTextBrowser{background-color:%s}" % col.name())

    def mouse_moved_close_figure(self, evt):
        print(evt[0])
        mouse_position = self.plot_plt_closeFigure.plotItem.vb.mapSceneToView(evt[0])
        print(float(mouse_position.x()))
        print(float(mouse_position.y()))

    def mouse_clicked_close_figure(self, evt):
        print(evt[0])
        position = str(evt[0])
        position = position.split('(')
        position = position[1].split(')')
        position = position[0].split(',')
        print('(x,y) = (%s,%s)' % (position[0], position[1]))
        self.Ar = [self.argon_40, self.argon_39, self.argon_38, self.argon_37, self.argon_36]
        xpos = self.get_clicked_point_num(float(position[0]), float(position[1]), self.analysing_time)
        if xpos in range(1, len(self.analysing_time) + 1):
            print('选中第 %d 个散点' % xpos)
            if (len(self.Ar[self.number]) - len(
                    self.unselected_list[self.sn][self.number])) > self.least_point_used_to_fit and xpos not in \
                    self.unselected_list[self.sn][self.number]:
                self.unselected_list[self.sn][self.number].append(xpos)
                draw_data = self.fitting_program(self.Ar[self.number], self.analysing_time,
                                                 unselected_list=self.unselected_list[self.sn][self.number])
                self.draw_close_figure(draw_data)
            elif xpos in self.unselected_list[self.sn][self.number]:
                self.unselected_list[self.sn][self.number].remove(xpos)
                draw_data = self.fitting_program(self.Ar[self.number], self.analysing_time,
                                                 unselected_list=self.unselected_list[self.sn][self.number])
                self.draw_close_figure(draw_data)
            else:
                reply = QMessageBox.warning(self, "Warning", "The number of points cannot be further reduced",
                                            QMessageBox.Yes | QMessageBox.No)
                print(reply)
                pass
        else:
            pass

    # 判断点的距离
    def get_clicked_point_num(self, clicked_x: float, clicked_y: float, time_list: list):
        if clicked_y <= 0:
            print('clicked out')
            return False
        else:
            pass
        for i in range(len(time_list)):
            right_point = time_list[i]
            if i >= 1:
                left_point = time_list[i - 1]
            else:
                left_point = 0
            if left_point <= clicked_x <= right_point:
                if abs(clicked_x - left_point) < abs(clicked_x - right_point):
                    possible_point = left_point
                    break
                else:
                    possible_point = right_point
                    break
            elif i == len(time_list) - 1 and clicked_x > right_point:
                possible_point = right_point
                break
            else:
                continue

        try:
            relative_distance = abs(clicked_x - possible_point) / max(time_list)
            if relative_distance < 0.1:
                return int(time_list.index(possible_point) + 1)
            else:
                return False
        except UnboundLocalError:
            print('Error')
            return False

    # 自动选择数据点
    def auto_select(self, data):
        data = copy.deepcopy(data)
        unselected_list = []
        autoresult_list = []
        for i in range(len(data)):
            unselected_list.append([])
            autoresult_list.append([])
            unselected_list[i].append([])
            for j in range(1, len(data[i]) - self.least_point_used_to_fit):
                comb = list(combinations([num for num in range(1, len(data[i]))], j))
                for k in range(len(comb)):
                    comb_1 = [each for each in comb[k]]
                    unselected_list[i].append(comb_1)
        for step_number in range(len(data)):
            # self.sn = step_number
            unselected_this_step = sorted(unselected_list[step_number], key=lambda i: len(i), reverse=False)
            # print(unselected_this_step)
            data_this_step = data[step_number]
            n = 1
            total_n = len(unselected_this_step)
            for isotope_number in range(5):
                print('现在计算第%s个阶段第%s个同位素最优解' % (step_number + 1, isotope_number + 1))
                # self.number = isotope_number
                each_step_isotope = [data_this_step[i + 1][isotope_number + 2] for i in
                                     range(len(data_this_step) - 1)]
                analysing_time = [data_this_step[i + 1][1] for i in range(len(data_this_step) - 1)]
                for each_combination in unselected_this_step:
                    each_comb = each_combination.copy()
                    if len(each_step_isotope) - len(each_comb) < self.least_point_used_to_fit:
                        pass
                    else:
                        fit_result = self.fitting_program(each_step_isotope, analysing_time, unselected_list=each_comb,
                                                          operate='auto')
                        relative_error = fit_result[1][4]
                        R_square = fit_result[1][1]
                        if n == 1 + isotope_number * total_n:
                            min_relative_error = relative_error
                            self.extra_result[step_number][isotope_number] = fit_result
                            self.unselected_list[step_number][isotope_number] = each_comb
                        if R_square >= self.best_fit_R_square:
                            min_relative_error = relative_error
                            self.extra_result[step_number][isotope_number] = fit_result
                            self.unselected_list[step_number][isotope_number] = each_comb
                            n = (isotope_number + 1) * total_n
                            self.progressBar.setValue(int(n * 100 / (total_n * 5)))
                            QApplication.processEvents()
                            print('R_square≥0.95，第%s个阶段第%s个同位素最优解, %s' % (
                                step_number + 1, isotope_number + 1, each_combination))
                            break
                        elif relative_error < min_relative_error:
                            min_relative_error = relative_error
                            self.extra_result[step_number][isotope_number] = fit_result
                            self.unselected_list[step_number][isotope_number] = each_comb
                        else:
                            pass
                    self.progressBar.setValue(int(n * 100 / (total_n * 5)))
                    QApplication.processEvents()
                    n += 1
            self.progressBar.setValue(0)
            self.btn_set[step_number].setStyleSheet("background-color:gray")
            self.draw_figures(data, step_number + 1, operate='auto')
            QApplication.processEvents()

    # 不选择点，直接拟合输出
    def skip(self, data):
        print('不选择点，直接拟合输出')
        data = copy.deepcopy(data)
        for step_number in range(len(data)):
            data_this_step = data[step_number]
            self.progressBar.setValue(0)
            QApplication.processEvents()
            for isotope_number in range(5):
                each_step_isotope = [data_this_step[i + 1][isotope_number + 2] for i in range(len(data_this_step) - 1)]
                analysing_time = [data_this_step[i + 1][1] for i in range(len(data_this_step) - 1)]
                fit_result = self.fitting_program(each_step_isotope, analysing_time, unselected_list=None,
                                                  operate='auto')
                self.extra_result[step_number][isotope_number] = fit_result
                self.unselected_list[step_number][isotope_number] = []
                self.progressBar.setValue(int((isotope_number + 1) * 20))
                QApplication.processEvents()
            self.btn_set[step_number].setStyleSheet("background-color:gray")
            self.draw_figures(data, step_number + 1, operate='auto')

    # 判断result是否全为空，返回True表示全部不是空值，可以用来计算和输出
    def is_no_empty_in_list(self, input_a_list):
        test_list = copy.deepcopy(input_a_list)
        if type(test_list) is str or type(test_list) is int or type(test_list) is float:
            return True
        for k in test_list:
            if not k:
                return False
            if not self.is_no_empty_in_list(k):
                return False
        return True

    # 保存结果按钮，按filtered data格式书写，包括零时刻截距和本底两个数据表
    # 输入的result形式是[self.extra_result, self.unselected_list, self.step_info]，其中第二个可以为空
    def save_result(self, result):
        print('点击save_result')
        if self.is_no_empty_in_list(result[2]):
            pass
        else:
            print('尚未完全处理，无法计算和输出, 或文件已打开重写失败')
            return False
        BLK_count, UNKNOWN_count = 0, 0
        BLK_value_backup, BLK_value, UNKNOWN_value = [], [], []
        BLK_index_list, UNKNOWN_index_list = [], []
        extraresult, step_info = result[0], result[2]
        for eachstep in step_info:
            if eachstep[1] in self.blank_type_name:
                BLK_index = step_info.index(eachstep)
                BLK_index_list.append(BLK_index)
                BLK_value_backup.append([])
                BLK_value_backup[BLK_count] = ['', eachstep[1], '%s-%d' % (self.sample_name, eachstep[8]),
                                               extraresult[BLK_index][4][1][0], extraresult[BLK_index][4][1][3],
                                               extraresult[BLK_index][3][1][0], extraresult[BLK_index][3][1][3],
                                               extraresult[BLK_index][2][1][0], extraresult[BLK_index][2][1][3],
                                               extraresult[BLK_index][1][1][0], extraresult[BLK_index][1][1][3],
                                               extraresult[BLK_index][0][1][0], extraresult[BLK_index][0][1][3],
                                               eachstep[3], eachstep[4], eachstep[5], eachstep[6], eachstep[7]]
                BLK_count += 1
            else:
                UNKNOWN_index = step_info.index(eachstep)
                UNKNOWN_index_list.append(UNKNOWN_index)
                UNKNOWN_value.append([])
                UNKNOWN_value[UNKNOWN_count] = ['%s-%d' % (self.sample_name, eachstep[8]), eachstep[1],
                                                extraresult[UNKNOWN_index][4][1][0],
                                                extraresult[UNKNOWN_index][4][1][3],
                                                extraresult[UNKNOWN_index][4][1][1],
                                                extraresult[UNKNOWN_index][3][1][0],
                                                extraresult[UNKNOWN_index][3][1][3],
                                                extraresult[UNKNOWN_index][3][1][1],
                                                extraresult[UNKNOWN_index][2][1][0],
                                                extraresult[UNKNOWN_index][2][1][3],
                                                extraresult[UNKNOWN_index][2][1][1],
                                                extraresult[UNKNOWN_index][1][1][0],
                                                extraresult[UNKNOWN_index][1][1][3],
                                                extraresult[UNKNOWN_index][1][1][1],
                                                extraresult[UNKNOWN_index][0][1][0],
                                                extraresult[UNKNOWN_index][0][1][3],
                                                extraresult[UNKNOWN_index][0][1][1], eachstep[3], eachstep[4],
                                                eachstep[5], eachstep[6], eachstep[7]]
                UNKNOWN_count += 1

        if not BLK_value_backup:
            print('BLK_value is empty')
        elif len(BLK_value_backup) == 1:
            for i in range(len(UNKNOWN_index_list)):
                list_01 = copy.deepcopy(BLK_value_backup[0])
                list_01[0] = UNKNOWN_value[i][0]
                BLK_value.append(list_01)
        elif min(BLK_index_list) < min(UNKNOWN_index_list) and max(BLK_index_list) < max(UNKNOWN_index_list):
            for i in range(len(UNKNOWN_index_list)):
                for j in range(len(BLK_index_list) - 1):
                    if BLK_index_list[j] < UNKNOWN_index_list[i] < BLK_index_list[j + 1]:
                        list_01 = copy.deepcopy(BLK_value_backup[j])
                        list_01[0] = UNKNOWN_value[i][0]
                        BLK_value.append(list_01)
                        break
                    elif UNKNOWN_index_list[i] > BLK_index_list[len(BLK_index_list) - 1]:
                        list_01 = copy.deepcopy(BLK_value_backup[len(BLK_index_list) - 1])
                        list_01[0] = UNKNOWN_value[i][0]
                        BLK_value.append(list_01)
                        break
                    else:
                        pass
        elif min(BLK_index_list) > min(UNKNOWN_index_list) and max(BLK_index_list) > max(UNKNOWN_index_list):
            for i in range(len(UNKNOWN_index_list)):
                for j in range(len(BLK_index_list) - 1):
                    if BLK_index_list[j] < UNKNOWN_index_list[i] < BLK_index_list[j + 1]:
                        list_01 = copy.deepcopy(BLK_value_backup[j + 1])
                        list_01[0] = UNKNOWN_value[i][0]
                        BLK_value.append(list_01)
                        break
                    elif UNKNOWN_index_list[i] < BLK_index_list[0]:
                        list_01 = copy.deepcopy(BLK_value_backup[0])
                        list_01[0] = UNKNOWN_value[i][0]
                        BLK_value.append(list_01)
                        break
                    else:
                        pass
        else:
            for i in range(len(UNKNOWN_index_list)):
                for j in range(len(BLK_index_list) - 1):
                    if BLK_index_list[j] < UNKNOWN_index_list[i] < BLK_index_list[j + 1]:
                        list_01 = copy.deepcopy(BLK_value_backup[j])
                        list_02 = copy.deepcopy(BLK_value_backup[j + 1])
                        list_01[0] = UNKNOWN_value[i][0]
                        list_02[0] = UNKNOWN_value[i][0]
                        if UNKNOWN_index_list[i] - BLK_index_list[j] <= BLK_index_list[j + 1] - UNKNOWN_index_list[i]:
                            BLK_value.append(list_01)
                        else:
                            BLK_value.append(list_02)
                        break
                    elif UNKNOWN_index_list[i] < BLK_index_list[0]:
                        list_01 = copy.deepcopy(BLK_value_backup[0])
                        list_01[0] = UNKNOWN_value[i][0]
                        BLK_value.append(list_01)
                        break
                    elif UNKNOWN_index_list[i] > BLK_index_list[len(BLK_index_list) - 1]:
                        list_01 = copy.deepcopy(BLK_value_backup[len(BLK_index_list) - 1])
                        list_01[0] = UNKNOWN_value[i][0]
                        BLK_value.append(list_01)
                        break
                    else:
                        pass
        print(BLK_value)
        print(UNKNOWN_index_list)
        col_unknown = len(UNKNOWN_value[0])
        col_blk = len(BLK_value[0])
        row_unknown = UNKNOWN_count + 2
        row_blk = UNKNOWN_count + 2

        wb = xlwt.Workbook()
        sheet_1 = wb.add_sheet('Intercept Value', cell_overwrite_ok=True)
        sheet_2 = wb.add_sheet('Procedure Blanks', cell_overwrite_ok=True)

        sheet_1_header = ['Intercept Value', '', '36Ar[fA]', '1σ', 'r2',
                          '37Ar[fA]', '1σ', 'r2', '38Ar[fA]', '1σ', 'r2',
                          '39Ar[fA]', '1σ', 'r2', '40Ar[fA]', '1σ', 'r2',
                          'Day', 'Mouth', 'Year', 'Hour', 'Min']
        sheet_2_header = ['Procedure Blanks', '', 'Real Procedure Blanks', '36Ar[fA]', '1σ', '37Ar[fA]', '1σ',
                          '38Ar[fA]', '1σ', '39Ar[fA]', '1σ', '40Ar[fA]', '1σ', 'Day', 'Mouth', 'Year', 'Hour', 'Min']

        for j in range(col_unknown):
            sheet_1.write(0, j, sheet_1_header[j])
        for j in range(col_blk):
            sheet_2.write(0, j, sheet_2_header[j])
        for i in range(2, row_unknown):
            for j in range(col_unknown):
                sheet_1.write(i, j, UNKNOWN_value[i - 2][j])
        for i in range(2, row_blk):
            for j in range(col_blk):
                sheet_2.write(i, j, BLK_value[i - 2][j])

        path = os.path.dirname(__file__) + "/../../filtered/" + "{}.xls".format(self.sample_name)
        print(path)
        try:
            wb.save(path)
        except PermissionError:
            print('file has already been opened, overwriting is forbidden')
            return False
        else:
            return path

    # CLAC按钮，即在主窗口中打开筛选后的结果
    def calc(self, result):
        print('点击calc')
        path = self.save_result(result)
        # 发射信号
        if not path:
            print('未计算完毕')
            return
        else:
            print("emit signal")
            self.Signal_extrapolation.emit(path)
            print('关闭子窗口')
            self.close()  # 关闭此子窗口

    def mouse_clicked_little_figure_1(self, evt):
        print(evt)
        self.draw_little_figure(1)
        draw_data = self.fitting_program(self.argon_40, self.analysing_time,
                                         unselected_list=self.unselected_list[self.sn][self.number])
        self.draw_close_figure(draw_data)

    def mouse_clicked_little_figure_2(self, evt):
        print(evt)
        self.draw_little_figure(2)
        draw_data = self.fitting_program(self.argon_39, self.analysing_time,
                                         unselected_list=self.unselected_list[self.sn][self.number])
        self.draw_close_figure(draw_data)

    def mouse_clicked_little_figure_3(self, evt):
        print(evt)
        self.draw_little_figure(3)
        draw_data = self.fitting_program(self.argon_38, self.analysing_time,
                                         unselected_list=self.unselected_list[self.sn][self.number])
        self.draw_close_figure(draw_data)

    def mouse_clicked_little_figure_4(self, evt):
        print(evt)
        self.draw_little_figure(4)
        draw_data = self.fitting_program(self.argon_37, self.analysing_time,
                                         unselected_list=self.unselected_list[self.sn][self.number])
        self.draw_close_figure(draw_data)

    def mouse_clicked_little_figure_5(self, evt):
        print(evt)
        self.draw_little_figure(5)
        draw_data = self.fitting_program(self.argon_36, self.analysing_time,
                                         unselected_list=self.unselected_list[self.sn][self.number])
        self.draw_close_figure(draw_data)

    def create_button(self, n):
        button = QPushButton('%s' % (n + 1))
        button.setMinimumSize(QtCore.QSize(15, 15))
        self.horizontalLayout_2.addWidget(button)
        self.btn_set.append(button)
        self.btn_set[n].clicked.connect(lambda: self.draw_figures(self.step_data, n + 1, operate='hand'))

    def draw_figures(self, step_data, step_number, operate='hand'):
        print('这是第%s阶段的图形' % step_number)
        sn = step_number - 1
        self.sn: int = sn  # 全局变量方便鼠标点击调用
        self.step_info_text = 'Data / Time: %s,    Sample Type: %s,    Addition: %s' % (
            step_data[sn][0][1], step_data[sn][0][2], step_data[sn][0][3])
        self.analysing_time = [step_data[sn][i + 1][1] for i in range(len(step_data[0]) - 1)]  # 质谱仪测量时间
        self.argon_40 = [step_data[sn][i + 1][2] for i in range(len(step_data[0]) - 1)]  # Ar40
        self.argon_39 = [step_data[sn][i + 1][3] for i in range(len(step_data[0]) - 1)]  # Ar39
        self.argon_38 = [step_data[sn][i + 1][4] for i in range(len(step_data[0]) - 1)]  # Ar38
        self.argon_37 = [step_data[sn][i + 1][5] for i in range(len(step_data[0]) - 1)]  # Ar37
        self.argon_36 = [step_data[sn][i + 1][6] for i in range(len(step_data[0]) - 1)]  # Ar36
        self.selected_list = [copy.deepcopy(self.argon_40), copy.deepcopy(self.argon_39), copy.deepcopy(self.argon_38),
                              copy.deepcopy(self.argon_37), copy.deepcopy(self.argon_36)]
        datetime_info = step_data[sn][0][1]

        day = datetime_info.split('/')[1]
        mouth = datetime_info.split('/')[0]
        year = datetime_info.split('/')[2].split(' ')[0]
        hour = datetime_info.split('/')[2].split(' ')[2].split(':')[0]
        minute = datetime_info.split('/')[2].split(' ')[2].split(':')[1]

        # 如果后面有PM、AM，需要转换成24小时制。
        try:
            hour_format = datetime_info.split('/')[2].split(' ')[3]
            if hour_format == 'PM' and int(hour) < 12:
                hour = int(hour) + 12
            elif hour_format == 'PM' and int(hour) >= 12:
                pass
            elif hour_format == 'AM' and int(hour) <= 12:
                pass
            elif hour_format == 'AM' and int(hour) > 12:
                pass
            else:
                raise ValueError('hour_format is neither AM nor PM')
        except IndexError:
            pass
        except ValueError as e:
            print(e)
            return
        self.step_info[sn] = [self.sample_name, step_data[sn][0][3], step_data[sn][0][2], day, mouth, year, str(hour),
                              minute, step_data[sn][0][0]]
        # self.step_info[sn] > ['19WHA0106': str, 'B', 'BLK', '16', '6', '2019', '1', '01', 12: int > 阶段数]
        self.draw_little_figure(1)
        draw_data = self.fitting_program(self.argon_40, self.analysing_time,
                                         unselected_list=self.unselected_list[sn][0], operate=operate)
        self.draw_close_figure(draw_data)

    def fitting_program(self, data, analysing_time_list, unselected_list=None, operate='hand'):
        if not unselected_list:
            unselected_list = []
        else:
            pass
        argon_list = copy.deepcopy(data)
        x_scatter = copy.deepcopy(analysing_time_list)
        argon_list_unselected = []
        x_unselected = []
        for i in [argon_list[num - 1] for num in unselected_list]:
            argon_list.remove(i)
            argon_list_unselected.append(i)
        for i in unselected_list:
            x_scatter.remove(analysing_time_list[i - 1])
            x_unselected.append(analysing_time_list[i - 1])

        # exp
        if len(argon_list) >= self.least_point_used_to_fit:
            x_line = copy.deepcopy(analysing_time_list)
            x_line.insert(0, 0)
            np.seterr(invalid='ignore')

            slope = FuncsCalc.intercept_linest(argon_list, x_scatter)[5][0]
            curvature = FuncsCalc.intercept_parabolic(argon_list, x_scatter)[5][1]
            fit_result_exp = FuncsCalc.intercept_exponential(argon_list, x_scatter, slope, curvature)
            y_line_1 = [fit_result_exp[5][0] * exp(fit_result_exp[5][1] * x_line[i]) + fit_result_exp[5][2]
                        for i in range(len(x_line))]
            SSE_1 = sum((y_line_1[i + 1] - argon_list[i]) ** 2 for i in range(len(argon_list)))
            R_square_1 = fit_result_exp[3]
            SE_1 = ((SSE_1 / (len(argon_list) - 2)) ** 0.5)  # * y_line_1[0]
            error_1 = self.obtain_error_of_intercept(SE_1, len(argon_list), x_scatter, confidence_level=0.68)
            error_1 = fit_result_exp[1]
            Relative_error_1 = error_1 * 100 / abs(y_line_1[0])
            Relative_error_1 = fit_result_exp[2]
            # self.plot_plt_closeFigure.plot().setData(x_line, y_line_1, pen='c', symbol=None)
            '''
            fit_result_exp = np.polyfit(x, np.log(y), 1)  # 无权重指数拟合 与EXCEL结果相同
            y_line_1 = [np.exp(fit_result_exp[0] * (x_line[i]) + fit_result_exp[1]) for i in range(len(x_line))]
            SSE_1 = sum((y_line_1[i + 1] - argon_list[i]) ** 2 for i in range(len(argon_list)))
            SST_1 = sum(
                (np.log(argon_list[i]) - np.average([np.log(argon_list[i]) for i in range(len(argon_list))])) ** 2 for i in range(len(argon_list)))
            SSR_1 = sum(
                (np.log(y_line_1[i + 1]) - np.average([np.log(y_line_1[i + 1]) for i in range(len(argon_list))])) ** 2 for i in
                range(len(argon_list)))
            R_square_1 = SSR_1 / SST_1
            SE_1 = ((SSE_1 / (len(argon_list) - 2)) ** 0.5)  # * y_line_1[0]
            error_1 = self.obtain_error_of_intercept(SE_1, len(argon_list), x_scatter, confidence_level=0.68)
            Relative_error_1 = error_1 * 100 / abs(y_line_1[0])
            # self.plot_plt_closeFigure.plot().setData(x_line, y_line_1, pen='c', symbol=None)
            '''
            # parabolic
            try:
                fit_result_par = FuncsCalc.intercept_parabolic(argon_list, x_scatter)
                y_line_3 = [fit_result_par[0] + fit_result_par[5][0] * x_line[i] + fit_result_par[5][1] * x_line[i] ** 2
                            for i in range(len(x_line))]
                SSE_3 = sum((y_line_3[i + 1] - argon_list[i]) ** 2 for i in range(len(argon_list)))
                R_square_3 = fit_result_par[3]
                SE_3 = ((SSE_3 / (len(argon_list) - 3)) ** 0.5)
                error_3 = self.obtain_error_of_intercept(SE_3, len(argon_list), x_scatter, confidence_level=0.68)
                error_3 = fit_result_par[1]
                Relative_error_3 = error_3 * 100 / abs(y_line_3[0])
                Relative_error_3 = fit_result_par[2]
                # self.plot_plt_closeFigure.plot().setData(x_line, y_line_3, pen='m', symbol=None)
            except Exception:
                fit_result_par, y_line_3 = ['nan', 'nan'], ['nan']
                R_square_3, SE_3, error_3, Relative_error_3 = 'nan', 'nan', 'nan', 'nan'

            # 线性回归
            _line_result = FuncsCalc.intercept_linest(argon_list, x_scatter)
            y_line_2 = [_line_result[5][0] * (x_line[i]) + _line_result[0] for i in range(len(x_line))]
            SSE_2 = sum((y_line_2[i + 1] - argon_list[i]) ** 2 for i in range(len(argon_list)))
            R_square_2 = _line_result[3]
            SE_2 = (SSE_2 / (len(argon_list) - 2)) ** 0.5
            error_2 = self.obtain_error_of_intercept(SE_2, len(argon_list), x_scatter, confidence_level=0.68)
            error_2 = _line_result[1]
            Relative_error_2 = _line_result[2]

            fit_result_line = [y_line_2[0], R_square_2, SE_2, error_2, Relative_error_2, x_scatter,
                               argon_list, x_line, y_line_2, x_unselected, argon_list_unselected]
            fit_result_exp = [y_line_1[0], R_square_1, SE_1, error_1, Relative_error_1, x_scatter, argon_list, x_line,
                              y_line_1, x_unselected, argon_list_unselected]
            fit_result_par = [y_line_3[0], R_square_3, SE_3, error_3, Relative_error_3, x_scatter, argon_list, x_line,
                              y_line_3, x_unselected, argon_list_unselected]
            fit_result = [fit_result_exp, fit_result_line, fit_result_par]
            if operate == 'hand':
                self.extra_result[self.sn][self.number] = fit_result
                if sum(len(self.extra_result[self.sn][i]) for i in range(5)) == 15:
                    self.btn_set[self.sn].setStyleSheet("background-color:gray")
                else:
                    pass
            else:
                pass
            return fit_result
        else:
            print('选择的数据点少于%s个，无法调用fitting_program' % self.least_point_used_to_fit)

    # draw_data > [[拟合1], [拟合2], [拟合3]]
    def draw_close_figure(self, draw_data):
        x_scatter = draw_data[0][5]
        Ar = draw_data[0][6]
        x_line = draw_data[0][7]
        y_line_1 = draw_data[0][8]
        y_line_2 = draw_data[1][8]
        y_line_3 = draw_data[2][8]
        x_unselected = draw_data[0][9]
        Ar_unselected = draw_data[0][10]
        R_square_1 = draw_data[0][1]
        R_square_2 = draw_data[1][1]
        R_square_3 = draw_data[2][1]
        SE_1 = draw_data[0][2]
        SE_2 = draw_data[1][2]
        SE_3 = draw_data[2][2]
        error_1 = draw_data[0][3]
        error_2 = draw_data[1][3]
        error_3 = draw_data[2][3]
        Relative_error_1 = draw_data[0][4]
        Relative_error_2 = draw_data[1][4]
        Relative_error_3 = draw_data[2][4]

        self.plot_plt_closeFigure.clear()

        self.plot_plt_closeFigure.plot().setData(x_scatter, Ar, pen=None, symbol='o', symbolPen=None,
                                                 symbolBrush='#4169E1')
        self.plot_plt_closeFigure.plot().setData(x_unselected, Ar_unselected, pen=None, symbol='o', symbolPen='w',
                                                 symbolBrush=None)
        self.plot_plt_closeFigure.plot().setData(x_line, y_line_1, pen='c', symbol=None)
        self.plot_plt_closeFigure.plot().setData(x_line, y_line_3, pen='m', symbol=None)
        self.plot_plt_closeFigure.plot().setData(x_line, y_line_2, pen='g', symbol=None)

        y_line_2[0] = format(y_line_2[0], '.6f')
        R_square_2 = format(R_square_2, '.6f')
        SE_2 = format(SE_2, '.6f')
        error_2 = format(error_2, '.6f')
        Relative_error_2 = format(Relative_error_2, '.6f')

        try:
            y_line_1[0] = format(y_line_1[0], '.6f')
            y_line_3[0] = format(y_line_3[0], '.6f')
            R_square_1 = format(R_square_1, '.6f')
            R_square_3 = format(R_square_3, '.6f')
            SE_1 = format(SE_1, '.6f')
            SE_3 = format(SE_3, '.6f')
            error_1 = format(error_1, '.6f')
            error_3 = format(error_3, '.6f')
            Relative_error_1 = format(Relative_error_1, '.6f')
            Relative_error_3 = format(Relative_error_3, '.6f')
        except Exception:
            print('含有负值无法拟合指数函数')
            pass

        form_1 = '{:<30}{:^18}{:^18}{:^18}'
        form_2 = '{:<18}\t{:^18.6e}{:^18.6e}{:^18.6e}'
        form_3 = '{:<30}\t{:^18}{:^18}{:^18}'
        text_1 = form_1.format('Expolation Results', '%s(exp)' % (y_line_1[0]), '%s(line)' % (y_line_2[0]),
                               '%s(par)' % (y_line_3[0]))
        text_2 = form_3.format('R-square', R_square_1, R_square_2, R_square_3)
        text_3 = form_3.format('SE of OLS', SE_1, SE_2, SE_3)
        text_4 = form_3.format('SE of intercept', error_1, error_2, error_3)
        text_5 = form_3.format('Relative SE(%)', Relative_error_1, Relative_error_2, Relative_error_3)
        text = '%s\n%s\n%s\n%s\n%s\n%s' % (
            self.step_info_text, text_1, text_2, text_3, text_4, text_5)
        # text = '<color = #ff0000>%s</font>' % text
        # text = '<font size = 20>%s</font>' % text
        # reference: https://www.e-learn.cn/content/wangluowenzhang/572183
        self.textBrowser.setText(text)

        try:
            max_argon = max(max(Ar), max(Ar_unselected))
            min_argon = min(min(Ar), min(Ar_unselected))
            max_x = max(max(x_scatter), max(x_unselected))
            min_x = min(min(x_scatter), min(x_unselected))
        except ValueError:
            max_argon = max(Ar)
            min_argon = min(Ar)
            max_x = max(x_scatter)
            min_x = min(x_scatter)
        delta_y = abs(max_argon - min_argon)
        delta_x = abs(max_x - min_x)
        max_scale_y = max_argon + delta_y * 0.1
        min_scale_y = min_argon - delta_y * 0.1
        max_scale_x = max_x + delta_x * 0.1

        self.plot_plt_closeFigure.setYRange(min_scale_y, max_scale_y)
        self.plot_plt_closeFigure.setXRange(0, max_scale_x)
        print('绘图完毕')

    @staticmethod
    def obtain_error_of_intercept(SE, n, x_list, confidence_level=0.68):
        # SSE-误差平方和、k-因变量个数、df-自由度、n-样本点、x_list-x数组、confidence_level-置信度（常用0.68得到1σ置信区间）
        k = 1
        df = n - k - 1
        alpha = 1 - confidence_level
        t_value = stats.t.isf(alpha / 2, df)
        dx_square_list = [(i - np.average(x_list)) ** 2 for i in x_list]
        s_intercept = SE * (1 / n + np.average(x_list) ** 2 / sum(dx_square_list)) ** 0.5
        # 截距的标准误差求解公式见《统计学（第六版）》贾俊平
        # 以及英文版：https://pages.mtu.edu/~fmorriso/cm3215/UncertaintySlopeInterceptOfLeastSquaresFit.pdf
        # 注意：贾俊平书中出现错误，根号下X平均值应该是平方
        confidence_interval = t_value * s_intercept
        return confidence_interval

    def draw_little_figure(self, number):
        self.plot_plt_littleFigure2_1.clear()
        self.plot_plt_littleFigure2_2.clear()
        self.plot_plt_littleFigure2_3.clear()
        self.plot_plt_littleFigure2_4.clear()
        self.plot_plt_littleFigure2_5.clear()

        color = [['b', 'r', 'r', 'r', 'r'],
                 ['r', 'b', 'r', 'r', 'r'],
                 ['r', 'r', 'b', 'r', 'r'],
                 ['r', 'r', 'r', 'b', 'r'],
                 ['r', 'r', 'r', 'r', 'b']]
        number = number - 1
        self.number = number

        self.plot_plt_littleFigure2_1.plot().setData(
            self.analysing_time, self.argon_40, pen=None, symbol='o', symbolPen='k', symbolBrush=color[number][0])
        self.plot_plt_littleFigure2_2.plot().setData(
            self.analysing_time, self.argon_39, pen=None, symbol='o', symbolPen='k', symbolBrush=color[number][1])
        self.plot_plt_littleFigure2_3.plot().setData(
            self.analysing_time, self.argon_38, pen=None, symbol='o', symbolPen='k', symbolBrush=color[number][2])
        self.plot_plt_littleFigure2_4.plot().setData(
            self.analysing_time, self.argon_37, pen=None, symbol='o', symbolPen='k', symbolBrush=color[number][3])
        self.plot_plt_littleFigure2_5.plot().setData(
            self.analysing_time, self.argon_36, pen=None, symbol='o', symbolPen='k', symbolBrush=color[number][4])


if __name__ == '__main__':
    [step_set, sample_name] = [[[[1, '6/16/2019  1:01:08 AM', 'BLK', 'B'],
                                 ['1', 12.288848, 193.54511130971824, 1.6530573508136361, 0.5119330787520514,
                                  0.4485003235454203, 0.7676461364731625],
                                 ['2', 24.611848, 194.11390930074762, 1.3901148576455344, 0.5474028569326816,
                                  0.4046572887844363, 0.6919563502736661],
                                 ['3', 36.920848, 193.66198896914418, 1.4140270144568892, 0.4625987769144513,
                                  0.4131058741949004, 0.7222031537495908],
                                 ['4', 49.233847999999995, 193.7779847891191, 1.4517767055065214, 0.38030039658990983,
                                  0.3112874866499591, 0.727612180339762],
                                 ['5', 61.562847999999995, 193.8898602203611, 1.276647852291761, 0.42034124922557975,
                                  0.36853020248124013, 0.7079810055895502],
                                 ['6', 73.89084799999999, 193.5875050616474, 1.2421195645445124, 0.4203322882196425,
                                  0.2978912938264934, 0.7233851131641252],
                                 ['7', 86.212848, 194.05267067696755, 1.2094293338910047, 0.40698725227471977,
                                  0.32797004712935934, 0.7070068744075242],
                                 ['8', 98.560848, 193.9113522245796, 1.1864406438823962, 0.39273703468655663,
                                  0.34441318076027183, 0.6875137400421043],
                                 ['9', 110.879848, 194.217839180014, 1.2739498367662137, 0.35377465613838804,
                                  0.3072714031948198, 0.6733968386768561],
                                 ['10', 123.185848, 194.08888385574406, 1.3759917497429128, 0.3375392365204388,
                                  0.3258208396059672, 0.6631470434441086]],
                                [[2, '6/16/2019  1:12:38 AM', 'UNKNOWN', '10'],
                                 ['1', 12.233848, 463787.17905540764, 15.591178813997221,
                                  284.7488049398562, 0.2521853652979526, 1357.991324210257],
                                 ['2', 24.562848, 462812.9390877058, 17.197816966136216, 283.1643738227001,
                                  0.24636670095101598, 1350.8922870393385],
                                 ['3', 36.863848, 461660.69523034926, 18.79046630265925,
                                  281.81596006724214, 0.18669325172513185, 1344.0808267456555],
                                 ['4', 49.163848, 460812.5632429486, 20.260124483093577,
                                  280.2356495380042, 0.2720002216852043, 1337.1166133085687],
                                 ['5', 61.476848, 459787.46478997206, 21.936364242750102, 278.849983072516,
                                  0.2795900057685268, 1330.1324196959038],
                                 ['6', 73.80484799999999, 458696.23606592556, 23.698595509938766,
                                  277.1652783459743, 0.24410325919639175, 1323.1887830170826],
                                 ['7', 86.112848, 457732.9902011036, 25.459554535128404, 275.7525591828584,
                                  0.19636206363445702, 1316.546904408929],
                                 ['8', 98.433848, 456840.2612420844, 27.180983683608726,
                                  274.6595498862609, 0.1743669185678982, 1309.4584899099125],
                                 ['9', 110.741848, 455999.6154810081, 28.75709132733012, 273.2280450781974,
                                  0.2308657256283685, 1303.6027882266542],
                                 ['10', 123.046848, 454902.79878703586, 30.302314985831703,
                                  271.63980543381433, 0.23242994711087084, 1296.299141521221]],
                                [[3, '6/16/2019  1:25:21 AM', 'UNKNOWN', '20'],
                                 ['1', 12.294848, 368076.6096973415, 17.536052372036234, 223.66951449962264,
                                  0.2679984708389231, 986.5975615144667],
                                 ['2', 24.615848, 367326.7588267934, 18.999129233731455, 222.4939592554299,
                                  0.20950065490069314, 981.5026490345742],
                                 ['3', 36.922847999999995, 366423.4656384853, 20.566696427916053, 221.25906731597433,
                                  0.18736706354084276, 975.700853872812],
                                 ['4', 49.203848, 365660.7031501489, 21.912071175701332, 220.06418091647146,
                                  0.26012929232991744, 970.8767796978053],
                                 ['5', 61.512848, 364878.5099150285, 23.549004794349884, 218.7468621217625,
                                  0.2070599301010151, 965.3618898162756],
                                 ['6', 73.836848, 364223.2549785129, 25.324384848508778, 217.83734709570572,
                                  0.24872939803361505, 960.6901569561898],
                                 ['7', 86.141848, 363419.3240733225, 26.87356786316328, 216.53050970920788,
                                  0.1867627092974536, 955.597217902963],
                                 ['8', 98.453848, 362649.59824660514, 28.349326667987516, 215.4271741134933,
                                  0.26025708386162294, 950.3936126453406],
                                 ['9', 110.775848, 362024.79165269743, 29.772466441533695, 214.222711811277,
                                  0.19739711987704256, 945.4012017909159],
                                 ['10', 123.095848, 361305.81385388324, 31.391453356742954, 213.15867039004112,
                                  0.1685382398187047, 940.4922382040779]],
                                [[4, '6/16/2019  1:38:09 AM', 'UNKNOWN', '40'],
                                 ['1', 12.271848, 206439.69134456766, 14.746118795584568, 124.8137810361825,
                                  0.18475491795059035, 470.66010722023367],
                                 ['2', 24.627847999999997, 205993.6441300801, 15.868474769883884,
                                  124.03244312764929, 0.15346885077730554, 467.8673628850717],
                                 ['3', 36.957848, 205535.20613098601, 16.77899400701584,
                                  123.44460519124941, 0.12763648320813115, 465.33211572709746],
                                 ['4', 49.281848, 205131.65693207036, 17.733451212143923, 122.79989406671373,
                                  0.22724724668358498, 462.91762481780904],
                                 ['5', 61.590848, 204699.1198856843, 18.871905443794535,
                                  122.03965565684935, 0.13671686776709135, 460.27162396348274],
                                 ['6', 73.915848, 204212.06979300923, 19.968083175321873,
                                  121.29335385551467,
                                  0.20367093342618214, 457.9271053707241],
                                 ['7', 86.227848, 203781.4366194826, 21.045633858651446,
                                  120.64478751034028, 0.16397128853891424, 455.14715364287105],
                                 ['8', 98.561848, 203379.69814233252, 22.083407906452493,
                                  120.08429005561503, 0.09681197835076133, 452.4834350743634],
                                 ['9', 110.876848, 202916.69010593207, 22.97836881870537,
                                  119.36434072857308, 0.14943005918347008, 449.9889746911502],
                                 ['10', 123.189848, 202506.78551174726, 24.032798209202276,
                                  118.79764259663797, 0.1628306789216457, 447.6886669937259]],
                                [[5, '6/16/2019  1:51:07 AM', 'UNKNOWN', '60'],
                                 ['1', 12.319848, 123301.61675786658, 12.863062429821541, 75.58809813975405,
                                  0.12803876356470884, 242.61511520008818],
                                 ['2', 24.663847999999998, 122989.45624429517, 13.379589607127942, 75.00429016384676,
                                  0.1335095119622709, 241.19639898870275],
                                 ['3', 36.991848, 122712.45004277771, 14.10168287070004, 74.77336987997562,
                                  0.05203768310612866, 239.88478317712944],
                                 ['4', 49.320848, 122411.06985897745, 14.818192259437104, 74.29390285503422,
                                  0.165864893832821, 238.29199560441586],
                                 ['5', 61.640848, 122125.40499652369, 15.524047249506578, 73.85297166909795,
                                  0.09731046774354679, 237.24568206936482],
                                 ['6', 73.980848, 121850.69028422433, 16.169336024674667, 73.40388689074278,
                                  0.12553534199615285, 235.62826972073452],
                                 ['7', 86.313848, 121572.53283707684, 17.084265723730677, 73.04285011040652,
                                  0.12645638424114852, 234.4168785006279],
                                 ['8', 98.63784799999999, 121316.99618544568, 17.86895850936403, 72.54086503199213,
                                  0.10164027925653712, 233.06200788803937],
                                 ['9', 110.949848, 121013.32653333707, 18.342503771445937, 72.16960765798208,
                                  0.13030599347719274, 231.78515537557385], ['10', 123.278848, 120767.25672453805,
                                                                             18.964104254161057, 71.91549530954116,
                                                                             0.09297021828880536, 230.51674961655274]],
                                [[6, '6/16/2019  2:04:16 AM', 'UNKNOWN', '80'],
                                 ['1', 12.258848, 88305.3170665071, 11.992982969964785, 55.11665551305564,
                                  0.1665452808949302, 155.70862677886478],
                                 ['2', 24.595847999999997, 88074.22378583926, 12.44685076606663, 54.67200213144036,
                                  0.12177582420089261, 154.72545543723467],
                                 ['3', 36.899848, 87847.6997380444, 12.822582027428892, 54.29937600582554,
                                  0.07362045460797673, 153.8793739582031],
                                 ['4', 49.220848, 87637.9261901739, 13.328998671732265, 54.07347902365953,
                                  0.20768548869745518, 153.05159985567838],
                                 ['5', 61.530848, 87430.7237068678, 14.03789836112074, 53.62831556925069,
                                  0.083022111512352, 152.20613844357453],
                                 ['6', 73.849848, 87219.48611385014, 14.619996080477033, 53.36990681591835,
                                  0.17037596073286548, 151.36875664093472],
                                 ['7', 86.15884799999999, 87027.86174497197, 15.244680260058978, 53.03743356294474,
                                  0.13951701555036827, 150.34484435921163],
                                 ['8', 98.470848, 86822.25620554601, 15.732766576905345, 52.85479923842184,
                                  0.05761685982047543, 149.533265581515],
                                 ['9', 110.78684799999999, 86618.45266551178, 16.20196440182631, 52.566209736424824,
                                  0.10762273320856958, 148.6511513912119],
                                 ['10', 123.099848, 86415.60588482533, 16.61391950182747, 52.25777972421194,
                                  0.09267067781373356, 147.91392455647804]],
                                [[7, '6/16/2019  2:17:34 AM', 'UNKNOWN', '100'],
                                 ['1', 12.283848, 63535.03537237871, 11.324244126153127, 40.51355305917461,
                                  0.1665541872301884, 102.67395505832421],
                                 ['2', 24.616847999999997, 63353.34034902468, 11.684320705813507, 39.92073136071856,
                                  0.10435190357094282, 102.0155641240564],
                                 ['3', 36.949847999999996, 63195.945162017975, 12.062439384663728, 39.83490718555628,
                                  0.04437866173250199, 101.35164339098694],
                                 ['4', 49.269847999999996, 63035.64053530834, 12.345723895026078, 39.70058307177493,
                                  0.17223521912347012, 100.68556934545903],
                                 ['5', 61.585848, 62886.93684708279, 13.038880963958427, 39.30918876013915,
                                  0.10700825979453588, 100.25023814341705],
                                 ['6', 73.877848, 62725.41021901554, 13.501512388889813, 39.10594731974935,
                                  0.15440252857483605, 99.6094837642725],
                                 ['7', 86.183848, 62579.19630203732, 13.955989101357464, 38.90915134778048,
                                  0.10206481073205598, 99.00482041959427],
                                 ['8', 98.491848, 62433.448247820226, 14.184304616080658, 38.62878477158889,
                                  0.09249992234520904, 98.50067013935897],
                                 ['9', 110.826848, 62280.7782497592, 14.64149132557471, 38.409085785358904,
                                  0.13939005971894164, 97.8398872102589],
                                 ['10', 123.129848, 62139.27605142023, 14.924086418385432, 38.352327934607494,
                                  0.07978535948472187, 97.35865709185197]],
                                [[8, '6/16/2019  2:31:02 AM', 'BLK', 'B'],
                                 ['1', 12.254847999999999, 348.67876473377555, 2.6849038034991612, 0.6808054043052113,
                                  0.5532294104886581, 0.9128706822062966],
                                 ['2', 24.586848, 356.9173217730079, 2.805321209294261, 0.6811882801452662,
                                  0.514572527761861, 0.9185169633366321],
                                 ['3', 36.914848, 365.58523665563365, 2.772716251973101, 0.6671933225037496,
                                  0.624812856680793, 0.9016218443331765],
                                 ['4', 49.224848, 373.64076684391796, 2.7606799869622844, 0.626538200528952,
                                  0.4882451194457499, 0.9475292804547747],
                                 ['5', 61.553847999999995, 381.66489341923824, 2.932391996186729, 0.5997277172324832,
                                  0.4250015358112019, 0.8895857312746547],
                                 ['6', 73.868848, 390.04534335000494, 3.040947056139997, 0.5393665344345532,
                                  0.4258646271671234, 0.8979081646381025],
                                 ['7', 86.14984799999999, 398.38780271758884, 3.1084590134040075, 0.575347706346856,
                                  0.39107996638254644, 0.9465570880231917],
                                 ['8', 98.474848, 405.8784332388572, 3.2914258184904686, 0.5415127514552797,
                                  0.3878541791728183, 0.9230660070964242],
                                 ['9', 110.794848, 413.7028640044378, 3.2933223271053156, 0.5539273080410844,
                                  0.36058442850263706, 0.9403756271218491],
                                 ['10', 123.107848, 421.46208031518586, 3.488005483240096, 0.5333256882286741,
                                  0.372856172326728, 0.9087011321214054]],
                                [[9, '6/16/2019  2:42:32 AM', 'UNKNOWN', '140'],
                                 ['1', 12.251848, 48817.90720491059, 11.511915462595397, 32.118817463421486,
                                  0.05778764326370578, 71.0909367398298],
                                 ['2', 24.588848, 48670.79428505383, 11.553874877802738, 31.909872302492463,
                                  -0.00011572054205144511, 70.52856610756298],
                                 ['3', 36.884848, 48526.19879513783, 11.648073530390995, 31.598264055657395,
                                  -0.13164040729537446, 70.20337418017323],
                                 ['4', 49.216848, 48396.63301692505, 11.935057837832822, 31.4335781421315,
                                  -0.0057457715255799235, 69.75513692699242],
                                 ['5', 61.529848, 48249.68554064521, 12.007521463578408, 31.244395046866824,
                                  0.07245471464672942, 69.39293433454455],
                                 ['6', 73.841848, 48119.29765354252, 12.10183468390312, 31.135734197052532,
                                  0.0354790089238447, 68.85958813823117],
                                 ['7', 86.150848, 47998.84427166129, 12.411327772841524, 30.86759332607189,
                                  0.060243964134139794, 68.4407102340596],
                                 ['8', 98.479848, 47864.06537026667, 12.602991322022167, 30.724149038599702,
                                  0.032843875361802055, 68.11264335286982],
                                 ['9', 110.791848, 47737.089602595246, 12.849913088480019, 30.53440023244644,
                                  0.021054723118025587, 67.75972817156247],
                                 ['10', 123.092848, 47609.89291263565, 13.0440113756398, 30.384733670743454,
                                  0.025236091132475824, 67.30643291340246]],
                                [[10, '6/16/2019  2:56:20 AM', 'UNKNOWN', '180'],
                                 ['1', 12.263848, 41175.14570988956, 12.882592672850931, 27.718197205030744,
                                  0.023912107510133285, 55.62816132862156],
                                 ['2', 24.566847999999997, 41042.10855358871, 12.74638743718549, 27.48340169241272,
                                  0.014464639262678936, 55.166792278497155],
                                 ['3', 36.883848, 40919.652807897226, 13.133297300927216, 27.212038474350475,
                                  -0.1075431120314293, 54.84652837053565],
                                 ['4', 49.200848, 40807.4978779039, 13.117427221990553, 27.16710074568498,
                                  -0.02645356888010708, 54.52451874833872],
                                 ['5', 61.512848, 40690.802711684075, 13.144576270734197, 26.942320305448494,
                                  0.04183289957474817, 54.259517517130945],
                                 ['6', 73.821848, 40577.06655946757, 13.466884033870235, 26.865469770988646,
                                  -2.965962479117845e-06, 53.90303873685619],
                                 ['7', 86.125848, 40464.82029704154, 13.624161814938706, 26.6603597300564,
                                  0.016094919900974614, 53.46186490868324],
                                 ['8', 98.41484799999999, 40352.102943212914, 13.613805710198564, 26.423901002728112,
                                  0.03485471388623007, 53.19766491358068],
                                 ['9', 110.734848, 40246.903917843374, 13.887396524008807, 26.38255080648641,
                                  0.01996348027203121, 52.901536073388186],
                                 ['10', 123.04284799999999, 40137.0859503457, 14.015320173346334, 26.236240810579,
                                  0.03794250556406914, 52.565748661371416]],
                                [[11, '6/16/2019  3:10:28 AM', 'UNKNOWN', '220'],
                                 ['1', 12.265848, 33694.521402091406, 14.390943308617452, 23.469472153105464,
                                  0.07904322411724696, 43.941121804890685],
                                 ['2', 24.582848, 33585.90538014882, 14.007409619673053, 23.024146998906357,
                                  0.025472523739986985, 43.605177812641784],
                                 ['3', 36.895848, 33482.378122171154, 14.166138296411077, 22.86473775244042,
                                  -0.08325152951634973, 43.407321402583],
                                 ['4', 49.232848, 33386.686587813594, 14.419055029550304, 22.693674058008416,
                                  0.05308179177290284, 43.08524574486919],
                                 ['5', 61.556847999999995, 33291.42013947861, 14.207646282560477, 22.633185599272963,
                                  0.02591011936615606, 42.85502929633314],
                                 ['6', 73.872848, 33186.893606056154, 14.368395681641546, 22.500395383630465,
                                  0.01991894007101197, 42.58892512034043],
                                 ['7', 86.178848, 33100.02805190598, 14.493866801522774, 22.32268207694381,
                                  0.02359767885650421, 42.263723174026254],
                                 ['8', 98.490848, 33005.57919399635, 14.567450348025838, 22.15532783520184,
                                  0.08133566759111205, 42.04404794514725],
                                 ['9', 110.826848, 32912.660122799185, 14.70947335486255, 22.108969306446276,
                                  0.07016525884843378, 41.82402688455163],
                                 ['10', 123.150848, 32821.27537203909, 14.762546418028494, 21.939670109573402,
                                  0.02169578298127489, 41.588498247414456]],
                                [[12, '6/16/2019  3:24:56 AM', 'UNKNOWN', '260'],
                                 ['1', 12.258848, 26558.149005396142, 14.804701574627273, 18.775248037168254,
                                  0.07260160023507822, 33.042314102717704],
                                 ['2', 24.598847999999997, 26473.71856324733, 14.5653542646268, 18.553283905795045,
                                  -0.024722567245847482, 32.80167928642942],
                                 ['3', 36.922847999999995, 26385.318418241055, 14.640736420227551, 18.40828683452238,
                                  -0.16539137373067248, 32.55136585321323],
                                 ['4', 49.248847999999995, 26309.580460277284, 14.677230049019617, 18.345321766085295,
                                  -0.011484353873222275, 32.37934715499396],
                                 ['5', 61.561848, 26228.58460823238, 14.72246825448733, 18.231915465508887,
                                  0.04143539231979415, 32.22197984674801],
                                 ['6', 73.869848, 26152.397148183816, 14.724744561880664, 18.171875203602283,
                                  -0.00488482041953997, 31.945993647241075],
                                 ['7', 86.190848, 26077.125518278008, 14.81480337348884, 18.017640735769632,
                                  0.05952915689826077, 31.850432869057038],
                                 ['8', 98.486848, 26003.458846308717, 14.84085416615663, 17.874640962883646,
                                  0.03320570466506373, 31.591040451742224],
                                 ['9', 110.794848, 25927.462395528473, 14.802769617032972, 17.80105131819933,
                                  0.09042213883174272, 31.45062310560161],
                                 ['10', 123.124848, 25855.235252784307, 14.699456620101484, 17.73986722851077,
                                  0.026739425906961323, 31.294826091374315]],
                                [[13, '6/16/2019  3:39:44 AM', 'UNKNOWN', '300'],
                                 ['1', 12.247848, 22860.158661849997, 15.530990184508138, 16.52232528933104,
                                  0.00837503682196028, 27.853267514159775],
                                 ['2', 24.593847999999998, 22784.45311520502, 15.438078957854897, 16.444340184111315,
                                  0.05481403431479959, 27.577377469135673],
                                 ['3', 36.909848, 22711.373677508458, 15.397895575091834, 16.27163958429305,
                                  -0.14450376642198032, 27.40634706307803],
                                 ['4', 49.234848, 22640.64900774039, 15.489263870086859, 16.177287551085673,
                                  -0.025723849591731685, 27.193188326877387],
                                 ['5', 61.575848, 22568.332066650204, 15.36405386455167, 16.092407737333716,
                                  0.019503757987870296, 26.93938630775498],
                                 ['6', 73.886848, 22503.140904745065, 15.466262432146282, 16.016512913116053,
                                  0.02520719232769647, 26.859871406611376],
                                 ['7', 86.227848, 22433.441968355815, 15.447185517554097, 15.850668734917226,
                                  0.07069675254570279, 26.64412617005337],
                                 ['8', 98.559848, 22369.359686561333, 15.298214510757683, 15.771828402622923,
                                  -0.0014881472508544435, 26.50435514501174],
                                 ['9', 110.89384799999999, 22305.15290781983, 15.43810546485961, 15.716838986146618,
                                  0.06748393322739821, 26.374186680788977],
                                 ['10', 123.233848, 22240.808923087247, 15.539124466373563, 15.605238903680261,
                                  -2.0755616190304416e-05, 26.239390487627404]]], '19WHA0106']
    QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    UI = SubWindowExtrapolation(step_set, sample_name)
    UI.show()
    sys.exit(app.exec())
