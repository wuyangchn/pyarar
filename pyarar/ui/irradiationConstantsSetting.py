import json
import os
from copy import deepcopy
from PyQt5.QtCore import QCoreApplication, pyqtSignal, QRegExp, QDateTime, QRect, Qt
from PyQt5.QtGui import QRegExpValidator, QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QInputDialog, QLabel, \
    QWidget, QDateTimeEdit, QDoubleSpinBox, QPushButton
import sys

from pyarar.sample import Sample
from pyarar.ui import UI_IrradiationConstantsWindow
from pyarar.params import IrraParams, DefaultParams

# static function, moving QWidget
def setWidgetGeometry(widget: QWidget, delta_x, delta_y, delta_width, delta_height):
    widget.setGeometry(QRect(widget.x() + delta_x, widget.y() + delta_y,
                             widget.width() + delta_width, widget.height() + delta_height))

# static function, 对比两个dict是否完全一致，返回False或True
def dictEq(dict1, dict2):
    if type(dict1) is str or type(dict1) is float or type(dict1) is int or type(dict1) is list:
        if str(dict1) == str(dict2):
            pass
        else:
            return False
    else:
        for k in set(dict1) | set(dict2):
            if k not in dict1 or k not in dict2:
                return False
            if not dictEq(dict1[k], dict2[k]):
                return False
    return True

# 创建新widget
def copyWidget(newWidget: QWidget, parentWidget: QWidget):
    newWidget.setSizePolicy(parentWidget.sizePolicy())
    newWidget.setMinimumSize(parentWidget.minimumSize())
    newWidget.setMaximumSize(parentWidget.maximumSize())
    newWidget.setGeometry(parentWidget.geometry())
    try:
        newWidget.setAlignment(parentWidget.alignment())
    except AttributeError:
        pass


current_param = dict()


class SubWindowIrradiation(QDialog, UI_IrradiationConstantsWindow.Ui_Dialog_Irradiation):
    # 定义信号, 自定义的信号必须在init()函数之前定义, 参考https://blog.csdn.net/The_Time_Runner/article/details/89330862
    Signal_irradiationWindow = pyqtSignal(dict)
    signalIrradiationWindowClose = pyqtSignal(dict)
    signalIrradiationWindowAttach = pyqtSignal(Sample)

    def __init__(self, irra_param, smp: Sample):
        super(SubWindowIrradiation, self).__init__()
        self.setupUi(self)
        self.smp = deepcopy(smp)
        global current_param
        if irra_param != {}:
            current_param = irra_param
        else:
            current_param = deepcopy(IrraParams().__dict__)
            self.currentIrraParams = current_param
            self.irraParamsBackup = deepcopy(DefaultParams().__dict__)

        # 备份修改前的参数, 在未点击apply, reset, close, cancel等任何一个选项前，对参数的修改仅对data做修改
        self.reactor_backup = deepcopy(current_param)
        self.reactor_output = deepcopy(current_param)

        # 由于Pydisigner中Icon添加的是相对路径，因此在MainWindow中调用子窗口时路径不对，
        # 在此修改Icon路径，两者显示效果有细微差别
        self.button_info.setIcon(QIcon(os.path.dirname(__file__) + "/../../tools/info.jpg"))
        self.buttonAdd.setIcon(QIcon(os.path.dirname(__file__) + "/../../tools/button_add.jpg"))

        # 尝试打开已保存的文件，如果没有则建立储存Project参数的字典
        try:
            with open(os.path.dirname(__file__) + '/../../tools/reactor_projects.json', 'r') as file:
                self.reactor_projects = json.load(file)
            print('打开reactor_projects文件')
        except Exception as e:
            print('error in open json: %s' % str(e))
            self.reactor_projects = dict()
            self.reactor_projects['temp'] = {}

        if current_param["IrradiationName"] in set(self.reactor_projects):
            self.writeEdit(current_param)
            self.saveProjectAs(current_param)
        else:
            self.reactor_projects[current_param["IrradiationName"]] = deepcopy(current_param)

        # 清空UI默认的下拉条目
        self.comboBox.clear()
        # 写入self.reacotr_projects中的条目
        for project in set(self.reactor_projects):
            self.comboBox.addItem(project)

        self.irradiation_number = 1
        self.btn_del_set = []
        self.buttonAdd.clicked.connect(self.addIrradiationCycles)
        self.button_apply.clicked.connect(lambda: self.apply())
        self.button_cancel.clicked.connect(self.cancel)
        self.button_info.clicked.connect(self.showInfo)
        self.button_reset.clicked.connect(self.reset)
        self.button_saveAs.clicked.connect(lambda: self.saveProjectAs(current_param))
        self.toolButton_3.clicked.connect(self.deleteProject)
        self.toolButton_2.clicked.connect(lambda: self.saveCurrentProject(current_param))
        self.comboBox.currentIndexChanged.connect(
            lambda index_num: self.changeProject(self.comboBox.itemText(index_num)))
        # 对比输入的参数和条目中的参数, 写入子窗体中，key可能为Project名或False

        key = self.getProjectName(current_param)
        print('输入参数对比结果%s' % key)
        if type(key) is str:
            if key != self.comboBox.currentText():
                self.comboBox.setCurrentText(key)
            else:
                self.writeEdit(current_param)
        elif 'temp' != self.comboBox.currentText():
            # 对比结果返回为False，则将temp更新为当前的reactor_param
            self.reactor_projects['temp'] = deepcopy(current_param)
            self.comboBox.setCurrentText('temp')
        else:
            self.reactor_projects['temp'] = deepcopy(current_param)
            self.writeEdit(current_param)

        # 限定输入框仅接受符合验证器的输入
        regx = QRegExp('^\d+(\.\d+)?$')  # 非负浮点数
        validator = QRegExpValidator(regx, self.lineEdit_1)
        self.lineEdit_1.setValidator(validator)
        self.lineEdit_2.setValidator(validator)
        self.lineEdit_3.setValidator(validator)
        self.lineEdit_4.setValidator(validator)
        self.lineEdit_5.setValidator(validator)
        self.lineEdit_6.setValidator(validator)
        self.lineEdit_7.setValidator(validator)
        self.lineEdit_8.setValidator(validator)
        self.lineEdit_9.setValidator(validator)
        self.lineEdit_10.setValidator(validator)
        self.lineEdit_11.setValidator(validator)
        self.lineEdit_12.setValidator(validator)
        self.lineEdit_13.setValidator(validator)
        self.lineEdit_14.setValidator(validator)
        self.lineEdit_15.setValidator(validator)
        self.lineEdit_16.setValidator(validator)
        self.lineEdit_17.setValidator(validator)
        self.lineEdit_18.setValidator(validator)
        self.lineEdit_19.setValidator(validator)
        self.lineEdit_20.setValidator(validator)
        self.lineEdit_21.setValidator(validator)
        self.lineEdit_22.setValidator(validator)
        self.lineEdit_23.setValidator(validator)
        self.lineEdit_24.setValidator(validator)
        self.lineEdit_25.setValidator(validator)
        self.lineEdit_26.setValidator(validator)

        # 绑定更新, 将输入框中参数的修改与储存字典相对应
        # 注意，由于以下的绑定，reactor_param将永远以子窗口中显示的数据完全一致
        self.lineEdit_1.textChanged.connect(lambda text: current_param.update({"Ar40vsAr36Trapped": text}))
        self.lineEdit_2.textChanged.connect(lambda text: current_param.update({"Ar40vsAr36Cosmo": text}))
        self.lineEdit_3.textChanged.connect(lambda text: current_param.update({"Ar38vsAr36Trapped": text}))
        self.lineEdit_4.textChanged.connect(lambda text: current_param.update({"Ar38vsAr36Cosmo": text}))
        self.lineEdit_5.textChanged.connect(lambda text: current_param.update({"Ar39vsAr37Ca": text}))
        self.lineEdit_6.textChanged.connect(lambda text: current_param.update({"Ar38vsAr37Ca": text}))
        self.lineEdit_7.textChanged.connect(lambda text: current_param.update({"Ar36vsAr37Ca": text}))
        self.lineEdit_8.textChanged.connect(lambda text: current_param.update({"Ar40vsAr39K": text}))
        self.lineEdit_9.textChanged.connect(lambda text: current_param.update({"Ar38vsAr39K": text}))
        self.lineEdit_10.textChanged.connect(lambda text: current_param.update({"Ar36vsAr38Cl": text}))
        self.lineEdit_11.textChanged.connect(lambda text: current_param.update({"KvsCaFactor": text}))
        self.lineEdit_12.textChanged.connect(lambda text: current_param.update({"KvsClFactor": text}))
        self.lineEdit_13.textChanged.connect(lambda text: current_param.update({"CavsClFactor": text}))
        self.lineEdit_14.textChanged.connect(lambda text: current_param.update({"Ar40vsAr36TrappedError": text}))
        self.lineEdit_15.textChanged.connect(lambda text: current_param.update({"Ar40vsAr36CosmoError": text}))
        self.lineEdit_16.textChanged.connect(lambda text: current_param.update({"Ar38vsAr36TrappedError": text}))
        self.lineEdit_17.textChanged.connect(lambda text: current_param.update({"Ar38vsAr36CosmoError": text}))
        self.lineEdit_18.textChanged.connect(lambda text: current_param.update({"Ar39vsAr37CaError": text}))
        self.lineEdit_19.textChanged.connect(lambda text: current_param.update({"Ar38vsAr37CaError": text}))
        self.lineEdit_20.textChanged.connect(lambda text: current_param.update({"Ar36vsAr37CaError": text}))
        self.lineEdit_21.textChanged.connect(lambda text: current_param.update({"Ar40vsAr39KError": text}))
        self.lineEdit_22.textChanged.connect(lambda text: current_param.update({"Ar38vsAr39KError": text}))
        self.lineEdit_23.textChanged.connect(lambda text: current_param.update({"Ar36vsAr38ClError": text}))
        self.lineEdit_24.textChanged.connect(lambda text: current_param.update({"KvsCaFactorError": text}))
        self.lineEdit_25.textChanged.connect(lambda text: current_param.update({"KvsClFactorError": text}))
        self.lineEdit_26.textChanged.connect(lambda text: current_param.update({"CavsClFactorError": text}))
        # dateTimeEdit and doubleSpinBox value changed
        self.dateTimeEdit.dateTimeChanged.connect(lambda: self.updateIrradiationDate(current_param))
        self.doubleSpinBox.valueChanged.connect(lambda: self.updateIrradiationDate(current_param))
        print('运行结束')

    def writeEdit(self, param):
        """
        :param param:
        :return:
        """
        print('运行writeEdit')
        # write constants
        self.lineEdit_1.setText(str(param["Ar40vsAr36Trapped"]))
        self.lineEdit_2.setText(str(param["Ar40vsAr36Cosmo"]))
        self.lineEdit_3.setText(str(param["Ar38vsAr36Trapped"]))
        self.lineEdit_4.setText(str(param["Ar38vsAr36Cosmo"]))
        self.lineEdit_5.setText(str(param["Ar39vsAr37Ca"]))
        self.lineEdit_6.setText(str(param["Ar38vsAr37Ca"]))
        self.lineEdit_7.setText(str(param["Ar36vsAr37Ca"]))
        self.lineEdit_8.setText(str(param["Ar40vsAr39K"]))
        self.lineEdit_9.setText(str(param["Ar38vsAr39K"]))
        self.lineEdit_10.setText(str(param["Ar36vsAr38Cl"]))
        self.lineEdit_11.setText(str(param["KvsCaFactor"]))
        self.lineEdit_12.setText(str(param["KvsClFactor"]))
        self.lineEdit_13.setText(str(param["CavsClFactor"]))
        self.lineEdit_14.setText(str(param["Ar40vsAr36TrappedError"]))
        self.lineEdit_15.setText(str(param["Ar40vsAr36CosmoError"]))
        self.lineEdit_16.setText(str(param["Ar38vsAr36TrappedError"]))
        self.lineEdit_17.setText(str(param["Ar38vsAr36CosmoError"]))
        self.lineEdit_18.setText(str(param["Ar39vsAr37CaError"]))
        self.lineEdit_19.setText(str(param["Ar38vsAr37CaError"]))
        self.lineEdit_20.setText(str(param["Ar36vsAr37CaError"]))
        self.lineEdit_21.setText(str(param["Ar40vsAr39KError"]))
        self.lineEdit_22.setText(str(param["Ar38vsAr39KError"]))
        self.lineEdit_23.setText(str(param["Ar36vsAr38ClError"]))
        self.lineEdit_24.setText(str(param["KvsCaFactorError"]))
        self.lineEdit_25.setText(str(param["KvsClFactorError"]))
        self.lineEdit_26.setText(str(param["CavsClFactorError"]))
        # write irradiation date, time and duration

        endDateTimeList = param['IrradiationEndTimeList']
        durationList = param['IrradiationDurationList']

        # reset the irradiation layout
        self.irradiation_number = 1
        rows = len(self.groupBox_2.findChildren(QPushButton))
        widgets = self.groupBox_2.findChildren((QPushButton, QLabel, QDateTimeEdit, QDoubleSpinBox))
        for widget in widgets:
            if '_' in widget.objectName():
                widget.setObjectName('deleteLater')
                self.gridLayout_2.removeWidget(widget)
                widget.deleteLater()
        setWidgetGeometry(self.groupBox_2, 0, 0, 0, -30 * (rows - 1))
        setWidgetGeometry(self.gridLayoutWidget, 0, 0, 0, -30 * (rows - 1))
        self.resize(self.size().width(), self.size().height() - 30 * (rows - 1))
        widgets = [self.groupBox_3, self.button_cancel, self.button_apply, self.button_reset, self.button_saveAs,
                   self.button_info]
        for widget in widgets:
            setWidgetGeometry(widget, 0, -30 * (rows - 1), 0, 0)

        self.dateTimeEdit.setDateTime(QDateTime.fromSecsSinceEpoch(endDateTimeList[0]))
        self.doubleSpinBox.setValue(durationList[0])

        if endDateTimeList and durationList and len(endDateTimeList) == len(durationList) > 1:
            for i in range(1, len(endDateTimeList)):
                self.addIrradiationCycles(endDateTimeList[i], durationList[i])

    # 点击问号显示说明文档
    def showInfo(self):
        here = os.path.dirname(__file__)
        try:
            with open(here + '/../../settings/reactorParamsInfo.txt', 'r') as file:
                param_info = file.read()
        except Exception:
            param_info = '本地说明文档缺失'
        QMessageBox.about(self, '参数说明', param_info)

    def updateIrradiationDate(self, param):
        dateTimeEdit_list = self.groupBox_2.findChildren(QDateTimeEdit)
        duration_list = self.groupBox_2.findChildren(QDoubleSpinBox)
        k0, k1 = [], []
        dateTimeEdit_list.sort(key=lambda x: x.geometry().y())
        duration_list.sort(key=lambda x: x.geometry().y())

        for i in dateTimeEdit_list:
            if i.objectName() != 'deleteLater':
                k0.append(i.dateTime().toSecsSinceEpoch())
        for i in duration_list:
            if i.objectName() != 'deleteLater':
                k1.append(i.value())

        param["IrradiationEndTimeList"] = k0
        param["IrradiationDurationList"] = k1

    # 添加辐照
    def addIrradiationCycles(self, dateTimeSecond=None, durationHour=None):
        """
        :param dateTimeSecond:
        :param durationHour:
        :return:
        """
        global current_param
        param = current_param
        self.irradiation_number += 1
        widgets = [self.groupBox_3, self.button_cancel, self.button_apply, self.button_reset, self.button_saveAs,
                   self.button_info]
        for each_widget in widgets:
            setWidgetGeometry(each_widget, 0, 30, 0, 0)
        setWidgetGeometry(self.groupBox_2, 0, 0, 0, 30)
        setWidgetGeometry(self.gridLayoutWidget, 0, 0, 0, 30)
        self.resize(self.size().width(), self.size().height() + 30)

        self.new_label_endDate = QLabel(self.gridLayoutWidget)
        copyWidget(self.new_label_endDate, self.labelEndDate)
        setWidgetGeometry(self.new_label_endDate, 0, 30, 0, 0)
        self.new_label_endDate.setObjectName('new_label_endDate_%s' % self.irradiation_number)
        self.gridLayout_2.addWidget(self.new_label_endDate, self.irradiation_number - 1, 0, 1, 1)
        self.new_label_endDate.setText(self.labelEndDate.text())

        widgets = self.groupBox_2.findChildren(QDateTimeEdit)
        widgets.sort(key=lambda x: x.y())
        last_widget = widgets[-1]
        self.new_dateTimeEdit = QDateTimeEdit(self.gridLayoutWidget)
        copyWidget(self.new_dateTimeEdit, last_widget)
        setWidgetGeometry(self.new_dateTimeEdit, 0, 30, 0, 0)
        self.new_dateTimeEdit.setObjectName('new_dateTimeEdit_%s' % self.irradiation_number)
        self.gridLayout_2.addWidget(self.new_dateTimeEdit, self.irradiation_number - 1, 1, 1, 1)
        self.new_dateTimeEdit.setCalendarPopup(last_widget.calendarPopup())
        self.new_dateTimeEdit.setDisplayFormat(last_widget.displayFormat())
        self.new_dateTimeEdit.dateTimeChanged.connect(lambda: self.updateIrradiationDate(param))
        if dateTimeSecond:
            self.new_dateTimeEdit.setDateTime(QDateTime.fromSecsSinceEpoch(int(dateTimeSecond)))
        else:
            self.new_dateTimeEdit.setDateTime(last_widget.dateTime())

        self.new_label_duration = QLabel(self.gridLayoutWidget)
        copyWidget(self.new_label_duration, self.labelDuration)
        setWidgetGeometry(self.new_label_duration, 0, 30, 0, 0)
        self.new_label_duration.setObjectName('new_label_duration_%s' % self.irradiation_number)
        self.gridLayout_2.addWidget(self.new_label_duration, self.irradiation_number - 1, 2, 1, 1)
        self.new_label_duration.setText(self.labelDuration.text())

        widgets = self.groupBox_2.findChildren(QDoubleSpinBox)
        widgets.sort(key=lambda x: x.y())
        last_widget = widgets[-1]
        self.new_doubleSpinBox = QDoubleSpinBox(self.gridLayoutWidget)
        copyWidget(self.new_doubleSpinBox, last_widget)
        setWidgetGeometry(self.new_doubleSpinBox, 0, 30, 0, 0)
        self.new_doubleSpinBox.setObjectName('new_doubleSpinBox_%s' % self.irradiation_number)
        self.gridLayout_2.addWidget(self.new_doubleSpinBox, self.irradiation_number - 1, 3, 1, 1)
        self.new_doubleSpinBox.valueChanged.connect(lambda: self.updateIrradiationDate(param))
        if durationHour:
            self.new_doubleSpinBox.setValue(durationHour)
        else:
            self.new_doubleSpinBox.setValue(last_widget.value())

        self.new_label_unit = QLabel(self.gridLayoutWidget)
        copyWidget(self.new_label_unit, self.labelUnit)
        setWidgetGeometry(self.new_label_unit, 0, 30, 0, 0)
        self.new_label_unit.setObjectName('new_label_unit_%s' % self.irradiation_number)
        self.gridLayout_2.addWidget(self.new_label_unit, self.irradiation_number - 1, 4, 1, 1)
        self.new_label_unit.setText(self.labelUnit.text())

        widgets = self.groupBox_2.findChildren(QPushButton)
        widgets.sort(key=lambda x: x.y())
        last_widget = widgets[-1]
        self.new_button_del = QPushButton(self.gridLayoutWidget)
        copyWidget(self.new_button_del, last_widget)
        setWidgetGeometry(self.new_button_del, 0, 30, 0, 0)
        self.new_button_del.setObjectName('new_button_del_%s' % self.irradiation_number)
        self.gridLayout_2.addWidget(self.new_button_del, self.irradiation_number - 1, 5, 1, 1)
        self.new_button_del.setIcon(QIcon(os.path.dirname(__file__) + "/../../tools/button_del.jpg"))
        self.btn_del_set.append(self.new_button_del)
        btn_del = self.btn_del_set[-1]
        row_index = int(btn_del.objectName().split('_')[-1]) - 1
        btn_del.clicked.connect(lambda: self.delIrradiationCycles(param, row_index))

    def delIrradiationCycles(self, param, row_index):
        """
        :param param:
        :param row_index:
        :return:
        """
        print("删除的行数：%s" % row_index)
        param["IrradiationEndTimeList"].pop(row_index)
        param["IrradiationDurationList"].pop(row_index)
        self.writeEdit(param)

    # 判断输入的reactor_param在self.reactor_projects中是否已经存在, 如果是则返回name, 否则返回temp
    def getProjectName(self, param):
        for key, values in self.reactor_projects.items():
            if dictEq(values, param) and key != 'temp':
                return key
            else:
                continue
        return False

    # 重置参数, 退回到刚打开子窗体时显示的参数
    def reset(self):
        print('点击了reset')
        # 退回到刚打开子窗体时的参数, 即self.reactor_bakeup
        key = self.getProjectName(self.reactor_backup)
        if not type(key) is str:
            key = 'temp'
            self.reactor_projects['temp'] = deepcopy(self.reactor_backup)
        if key != self.comboBox.currentText():
            self.comboBox.setCurrentText(key)
        else:
            self.writeEdit(self.reactor_backup)

    # 保存当前参数
    def saveProjectAs(self, param):
        print('点击了saveProjectAs')
        num = self.comboBox.count()  # 当前已存在的Project数量
        current_project = [self.comboBox.itemText(i) for i in range(num)]
        print('当前有%s个辐照参数集合，名称分别为%s' % (num, current_project))

        for key, value in param.items():
            try:
                param.update({key: [float(value), int(float(value))][float(value) == int(float(value))]})
            except ValueError:
                pass
            except TypeError:
                pass

        name_num = 0
        while True:
            name_num += 1
            text = 'Project_' + str(name_num)
            if text not in current_project:
                break
            else:
                continue

        while True:
            text, state = QInputDialog.getText(self, '保存为', '请输入保存名称', text=str(text))
            if not state:
                return
            elif ' ' in text:
                QMessageBox.warning(self, "Warning", '不能有空格', QMessageBox.Yes | QMessageBox.No)
                continue
            elif text in current_project:
                tip = '该名称已存在，请重新输入'
                QMessageBox.question(self, "Question", tip, QMessageBox.Yes | QMessageBox.No)
                continue
            else:
                print('新Project名为%s' % text)
                break

        num = self.comboBox.count()  # 目前已存在的Project数量
        current_project = [self.comboBox.itemText(i) for i in range(num)]
        keys = [key for key in self.reactor_projects.keys()]
        if text not in keys and text in current_project:
            print('将%s保存到self.reactor_projects中' % text)
            self.reactor_projects[str(text)] = deepcopy(param)  # 尤其注意不能用data，用data两者将同步更改

        # 保存为文件或修改已存在文件
        with open(os.path.dirname(__file__) + '/../../tools/reactor_projects.json', 'w') as file:
            jsonData = json.dumps(self.reactor_projects, indent=4, separators=(',', ': '))
            file.write(jsonData)
            print('保存reactor_projects')
        # 应用新project
        self.apply()
        return text

    # 下拉选项选择Project
    def changeProject(self, text):
        print('选中%s' % text)
        global current_param
        for key in current_param.keys():
            try:
                current_param[key] = self.reactor_projects[str(text)][key]
            except KeyError:
                continue
        self.writeEdit(self.reactor_projects[str(text)])

    # 删除当前选中的Project
    def deleteProject(self):
        print('点击了deleteProject')
        a = self.comboBox.currentIndex()
        b = self.comboBox.currentText()
        if b == 'temp':
            tip = '临时项目不能删除'
            QMessageBox.information(self, "Information", tip, QMessageBox.Yes)
            return
        else:
            print('将删除%s:%s' % (a, b))
            # 首先在列表中删除
            try:
                del self.reactor_projects[b]
            except KeyError:
                pass
            # 其次修改存档文件
            with open(os.path.dirname(__file__) + '/../../tools/reactor_projects.json', 'w') as file:
                jsonData = json.dumps(self.reactor_projects, indent=4, separators=(',', ': '))
                file.write(jsonData)
            # 还要删除下拉菜单
            self.comboBox.removeItem(a)

    # 将参数修改保存为当前的条目，同时会激活apply
    def saveCurrentProject(self, param):
        a = self.comboBox.currentIndex()
        b = self.comboBox.currentText()

        num = self.comboBox.count()  # 当前已存在的Project数量
        current_project = [self.comboBox.itemText(i) for i in range(num)]

        # 如果参数与已有的Project相同, 禁止另存, 即Project各个条目必须参数不同
        for key, values in self.reactor_projects.items():
            if dictEq(values, param) and key != 'temp' and key != b:
                tip = '与<%s>参数相同，将%s重命名为%s，原%s将被删除?' % (key, key, b, b)
                messageBox = QMessageBox.question(self, "Question", tip, QMessageBox.Yes | QMessageBox.No)
                if messageBox == QMessageBox.Yes:
                    self.comboBox.currentIndexChanged.disconnect()
                    self.comboBox.removeItem(current_project.index(key))
                    del self.reactor_projects[key]
                    self.comboBox.currentIndexChanged.connect(
                        lambda index_num: self.changeProject(self.comboBox.itemText(index_num)))
                    print('已删除%s' % key)
                    break
                elif messageBox == QMessageBox.No:
                    self.comboBox.setCurrentText(key)
                    return
            else:
                pass

        self.reactor_projects[b] = deepcopy(param)
        # 修改存档文件
        with open(os.path.dirname(__file__) + '/../../tools/reactor_projects.json', 'w') as file:
            jsonData = json.dumps(self.reactor_projects, indent=4, separators=(',', ': '))
            file.write(jsonData)
            print('保存文件')
        self.apply()

    # 关闭窗体
    def closeEvent(self, event):
        print('点击了close，等效于cancel')
        self.cancel()

    # 取消修改
    def cancel(self):
        print('点击了cancel')
        # 退回到最后一次apply时的参数
        key = self.getProjectName(self.reactor_output)
        if type(key) == str and key != self.comboBox.currentText():
            self.comboBox.setCurrentText(key)
        elif type(key) == str and key == self.comboBox.currentText():
            self.writeEdit(self.reactor_output)
        else:
            self.reactor_projects['temp'] = deepcopy(self.reactor_output)
            self.changeProject('temp')

    # 应用修改, 将修改保存到self.reactor_output, 但不发射信号
    def apply(self):
        global current_param
        param = current_param
        print('点击了apply')
        for key, value in param.items():
            try:
                param.update({key: [float(value), int(float(value))][float(value) == int(float(value))]})
            except ValueError:
                pass
            except TypeError:
                pass
        self.reactor_output = deepcopy(param)
        # 应用当前参数
        key = self.getProjectName(self.reactor_output)
        if key and key != self.comboBox.currentText():
            self.comboBox.setCurrentText(key)
        elif key and key == self.comboBox.currentText():
            pass
        else:
            key = "temp"
            self.reactor_projects['temp'] = deepcopy(self.reactor_output)
            self.comboBox.setCurrentText('temp')
        # 发射信号
        print('将从apply发射信号, self.reactor_output发射的参数：%s' % self.reactor_output["IrradiationDurationList"])
        for _key, _value in self.reactor_output.items():
            setattr(self.smp, _key, _value)
        self.smp.IrradiationName = key
        self.signalIrradiationWindowAttach.emit(self.smp)


if __name__ == '__main__':
    reactor_param = {
        "40/36Trapped": "298.56",
        "40/36Cosmo": "0.018",
        "38/36Trapped": "0.1869",
        "38/36Cosmo": "1.493",
        "39/37Ca": "0.000699",
        "38/37Ca": "0",
        "36/37Ca": "0.000270",
        "40/39K": "0.010240",
        "38/39K": "0",
        "36/38Cl": "262.80",
        "K/Ca": "0.570",
        "K/Cl": "0",
        "Ca/Cl": "0",
        "Ca/ClError": "0",
        "K/ClError": "0",
        "K/CaError": "2",
        "36/38ClError": "0",
        "38/39KError": "0.1",
        "40/39KError": "24.9",
        "36/37CaError": "0.37",
        "38/37CaError": "21.9",
        "39/37CaError": "1.83",
        "38/36CosmoError": "3",
        "38/36TrappedError": "0",
        "40/36CosmoError": "35",
        "40/36TrappedError": "0",
        "dateTime": 1522797300,
        "duration": 38.0,
        "dateTime_list": [1522797300, 1522798400],
        "duration_list": [38.0, 40.0]}
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    UI = SubWindowIrradiation(reactor_param)
    UI.show()
    sys.exit(app.exec())
