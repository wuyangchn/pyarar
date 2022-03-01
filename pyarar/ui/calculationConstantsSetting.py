import sys
import os
from copy import deepcopy
from PyQt5.QtCore import QCoreApplication, pyqtSignal, QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator, QIcon, QPalette
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QLineEdit, QCheckBox, QRadioButton

from pyarar.sample import UnkSample, AirSample, MonitorSample, Sample
from pyarar.ui import UI_CalculationConstantsWindow
from pyarar.ui import jvalueCalcualtion
from pyarar.params import CalcParams, DefaultParams


class SubWindowCalculation(QDialog, UI_CalculationConstantsWindow.Ui_Dialog_Calculation):
    # 定义信号, 自定义的信号必须在init()函数之前定义, 参考https://blog.csdn.net/The_Time_Runner/article/details/89330862
    signalCalculationWindowAttach = pyqtSignal(UnkSample or AirSample or MonitorSample)
    signalCalculationWindowClose = pyqtSignal(dict)

    def __init__(self, calc_params: dict = None, smp: UnkSample = None):
        super(SubWindowCalculation, self).__init__()
        self.setupUi(self)
        print('Calculation')
        if not calc_params:
            calc_params = deepcopy(CalcParams().__dict__)

        self.currentCalcParams = calc_params

        self.calcParamsBackup = deepcopy(DefaultParams().__dict__)

        self.pushButton_8.setIcon(QIcon(os.path.dirname(__file__) + "/../../tools/info.jpg"))
        self.pushButton_7.setIcon(QIcon(os.path.dirname(__file__) + "/../../tools/info.jpg"))

        fitting_model = ['York-2', 'OLS']
        self.comboBox_1.addItems(fitting_model)

        # 限定输入框仅接受符合验证器的输入
        regx = QRegExp('^\\d+(\\.\\d+)?$')  # 非负浮点数
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
        self.lineEdit_27.setValidator(validator)
        self.lineEdit_28.setValidator(validator)
        self.lineEdit_29.setValidator(validator)
        self.lineEdit_30.setValidator(validator)
        self.lineEdit_31.setValidator(validator)
        self.lineEdit_32.setValidator(validator)
        self.lineEdit_33.setValidator(validator)
        self.lineEdit_34.setValidator(validator)
        self.lineEdit_35.setValidator(validator)
        self.lineEdit_36.setValidator(validator)
        self.lineEdit_37.setValidator(validator)
        self.lineEdit_38.setValidator(validator)
        self.lineEdit_39.setValidator(validator)
        self.lineEdit_40.setValidator(validator)
        self.lineEdit_41.setValidator(validator)
        self.lineEdit_42.setValidator(validator)
        self.lineEdit_43.setValidator(validator)
        self.lineEdit_44.setValidator(validator)
        self.lineEdit_45.setValidator(validator)
        self.lineEdit_46.setValidator(validator)
        self.lineEdit_47.setValidator(validator)
        self.lineEdit_48.setValidator(validator)
        self.lineEdit_49.setValidator(validator)
        self.lineEdit_50.setValidator(validator)
        self.lineEdit_51.setValidator(validator)
        self.lineEdit_52.setValidator(validator)

        self.lineEdit_54.setValidator(validator)
        self.lineEdit_60.setValidator(validator)
        self.lineEdit_64.setValidator(validator)
        self.lineEdit_69.setValidator(validator)
        self.lineEdit_71.setValidator(validator)
        self.lineEdit_72.setValidator(validator)
        self.lineEdit_75.setValidator(validator)
        self.lineEdit_76.setValidator(validator)

        # 每次修改参数均发射信号更新参数字典
        self.lineEdit_1.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_1, text, "K40Const", calc_params, smp))
        self.lineEdit_2.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_2, text, "K40ECConst", calc_params, smp))
        self.lineEdit_3.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_3, text, "K40BetaNConst", calc_params, smp))
        self.lineEdit_4.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_4, text, "K40BetaPConst", calc_params, smp))
        self.lineEdit_5.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_5, text, "Ar39Const", calc_params, smp))
        self.lineEdit_6.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_6, text, "Ar37Const", calc_params, smp))
        self.lineEdit_7.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_7, text, "Cl36Const", calc_params, smp))
        self.lineEdit_8.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_8, text, "K40ECActivity", calc_params, smp))
        self.lineEdit_9.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_9, text, "K40BetaNActivity", calc_params, smp))
        self.lineEdit_10.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_10, text, "K40BetaPActivity", calc_params, smp))
        self.lineEdit_11.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_11, text, "Cl36vs38Productivity", calc_params, smp))
        self.lineEdit_12.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_12, text, "K40Mass", calc_params, smp))
        self.lineEdit_13.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_13, text, "NoConst", calc_params, smp))
        self.lineEdit_14.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_14, text, "YearConst", calc_params, smp))
        self.lineEdit_15.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_15, text, "K40vsKFractions", calc_params, smp))
        self.lineEdit_16.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_16, text, "Cl35vsCl37Fractions", calc_params, smp))
        self.lineEdit_17.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_17, text, "HClvsClFractions", calc_params, smp))
        self.lineEdit_18.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_18, text, "Ar40vsAr36AirConst", calc_params, smp))
        self.lineEdit_19.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_19, text, "K40ConstError", calc_params, smp))
        self.lineEdit_20.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_20, text, "K40ECConstError", calc_params, smp))
        self.lineEdit_21.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_21, text, "K40BetaNConstError", calc_params, smp))
        self.lineEdit_22.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_22, text, "K40BetaPConstError", calc_params, smp))
        self.lineEdit_23.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_23, text, "Ar39ConstError", calc_params, smp))
        self.lineEdit_24.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_24, text, "Ar37ConstError", calc_params, smp))
        self.lineEdit_25.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_25, text, "Cl36ConstError", calc_params, smp))
        self.lineEdit_26.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_26, text, "K40ECActivityError", calc_params, smp))
        self.lineEdit_27.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_27, text, "K40BetaNActivityError", calc_params, smp))
        self.lineEdit_28.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_28, text, "K40BetaPActivityError", calc_params, smp))
        self.lineEdit_29.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_29, text, "Cl36vs38ProductivityError", calc_params, smp))
        self.lineEdit_30.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_30, text, "K40MassError", calc_params, smp))
        self.lineEdit_31.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_31, text, "NoConstError", calc_params, smp))
        self.lineEdit_32.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_32, text, "YearConstError", calc_params, smp))
        self.lineEdit_33.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_33, text, "K40vsKFractionsError", calc_params, smp))
        self.lineEdit_34.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_34, text, "Cl35vsCl37FractionsError", calc_params, smp))
        self.lineEdit_35.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_35, text, "HClvsClFractionsError", calc_params, smp))
        self.lineEdit_36.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_36, text, "Ar40vsAr36AirConstError", calc_params, smp))
        self.lineEdit_37.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_37, text, "JValue", calc_params, smp))
        self.lineEdit_38.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_38, text, "JValueError", calc_params, smp))
        self.lineEdit_39.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_39, text, "MDF", calc_params, smp))
        self.lineEdit_40.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_40, text, "MDFError", calc_params, smp))
        self.lineEdit_41.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_41, text, "Ar36Mass", calc_params, smp))
        self.lineEdit_42.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_42, text, "Ar36MassError", calc_params, smp))
        self.lineEdit_43.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_43, text, "Ar37Mass", calc_params, smp))
        self.lineEdit_44.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_44, text, "Ar37MassError", calc_params, smp))
        self.lineEdit_45.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_45, text, "Ar38Mass", calc_params, smp))
        self.lineEdit_46.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_46, text, "Ar38MassError", calc_params, smp))
        self.lineEdit_47.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_47, text, "Ar39Mass", calc_params, smp))
        self.lineEdit_48.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_48, text, "Ar39MassError", calc_params, smp))
        self.lineEdit_49.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_49, text, "Ar40Mass", calc_params, smp))
        self.lineEdit_50.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_50, text, "Ar40MassError", calc_params, smp))
        self.lineEdit_51.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_51, text, "York2FitConvergence", calc_params, smp))
        self.lineEdit_52.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_52, text, "York2FitIteration", calc_params, smp))

        self.lineEdit_55.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_55, text, "K40Activity", calc_params, smp))
        self.lineEdit_53.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_53, text, "K40ActivityError", calc_params, smp))

        # standard information used to calculate age
        self.lineEdit_70.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_70, text, "PrimaryStdName", calc_params, smp))
        self.lineEdit_69.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_69, text, "PrimaryStdAge", calc_params, smp))
        self.lineEdit_75.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_75, text, "PrimaryStdAgeError", calc_params, smp))
        self.lineEdit_64.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_64, text, "PrimaryStdAr40Conc", calc_params, smp))
        self.lineEdit_54.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_54, text, "PrimaryStdAr40ConcError", calc_params, smp))
        self.lineEdit_71.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_71, text, "PrimaryStdKConc", calc_params, smp))
        self.lineEdit_72.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_72, text, "PrimaryStdKConcError", calc_params, smp))
        self.lineEdit_60.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_60, text, "PrimaryStdAr40vsK", calc_params, smp))
        self.lineEdit_76.textChanged.connect(
            lambda text: self.textChanged(self.lineEdit_76, text, "PrimaryStdAr40vsKError", calc_params, smp))

        self.comboBox_1.currentTextChanged.connect(
            lambda state: self.checkBoxChanged(self.checkBox_1, state, "Fitting", calc_params, smp))
        self.checkBox.toggled.connect(
            lambda state: self.checkBoxChanged(self.checkBox, state, "ForceNegative", calc_params, smp))
        self.checkBox_2.toggled.connect(
            lambda state: self.checkBoxChanged(self.checkBox_2, state, "CorrBlank", calc_params, smp))
        self.checkBox_3.toggled.connect(
            lambda state: self.checkBoxChanged(self.checkBox_3, state, "CorrDiscr", calc_params, smp))
        self.checkBox_4.toggled.connect(
            lambda state: self.checkBoxChanged(self.checkBox_4, state, "Corr37ArDecay", calc_params, smp))
        self.checkBox_5.toggled.connect(
            lambda state: self.checkBoxChanged(self.checkBox_5, state, "Corr39ArDecay", calc_params, smp))
        """({"Corr36ClDecay": state}))"""
        self.checkBox_6.toggled.connect(
            lambda state: self.checkBoxChanged(self.checkBox_6, state, "CorrK", calc_params, smp))
        self.checkBox_7.toggled.connect(
            lambda state: self.checkBoxChanged(self.checkBox_7, state, "CorrCa", calc_params, smp))
        self.checkBox_8.toggled.connect(
            lambda state: self.checkBoxChanged(self.checkBox_8, state, "CorrAtm", calc_params, smp))
        self.checkBox_9.toggled.connect(
            lambda state: self.checkBoxChanged(self.checkBox_9, state, "CorrCl", calc_params, smp))
        self.checkBox_10.toggled.connect(
            lambda state: self.checkBoxChanged(self.checkBox_10, state, "DisplayRelative", calc_params, smp))
        self.checkBox_11.toggled.connect(
            lambda state: self.checkBoxChanged(self.checkBox_11, state, "UseDecayConst", calc_params, smp))
        self.checkBox_12.toggled.connect(
            lambda state: self.checkBoxChanged(self.checkBox_12, state, "UseInterceptCorrAtm", calc_params, smp))
        self.checkBox_13.toggled.connect(
            lambda state: self.checkBoxChanged(self.checkBox_13, state, "RecalibrationToPrimary", calc_params, smp))
        self.checkBox_14.toggled.connect(
            lambda state: self.checkBoxChanged(self.checkBox_14, state, "RecalibrationUseAge", calc_params, smp))
        self.checkBox_15.toggled.connect(
            lambda state: self.checkBoxChanged(self.checkBox_15, state, "RecalibrationUseRatio", calc_params, smp))

        self.radioButton.toggled.connect(
            lambda state: self.checkBoxChanged(self.radioButton, state, "LinMassDiscrLaw", calc_params, smp))
        self.radioButton_2.toggled.connect(
            lambda state: self.checkBoxChanged(self.radioButton_2, state, "ExpMassDiscrLaw", calc_params, smp))
        self.radioButton_3.toggled.connect(
            lambda state: self.checkBoxChanged(self.radioButton_3, state, "PowMassDiscrLaw", calc_params, smp))

        # 单行输入框默认显示打开窗口传入的数值，即上次退出的参数
        self.write_param(calc_params)

        self.pushButton_attach.clicked.connect(lambda: self.apply(calc_params, smp))
        self.pushButton_import.clicked.connect(lambda: self.importParams(smp))
        self.pushButton_reset.clicked.connect(self.readParams)
        self.pushButton_9.clicked.connect(self.get_Jvalue)

        # 问号按钮
        self.pushButton_7.clicked.connect(self.display_info)
        self.pushButton_8.clicked.connect(self.display_info)

    @staticmethod
    def textChanged(lineEdit: QLineEdit, text, key, params, smp: UnkSample = None):
        params.update({key: text})
        Palette = QPalette()
        if text == "":
            text = 0
        if smp:
            if isinstance(text, type(smp.get_data(key))):
                if smp.get_data(key) == text:
                    Palette.setColor(QPalette.Text, Qt.blue)
                    lineEdit.setPalette(Palette)
            else:
                if smp.get_data(key) == float(text):
                    Palette.setColor(QPalette.Text, Qt.blue)
                    lineEdit.setPalette(Palette)
        else:
            Palette.setColor(QPalette.Text, Qt.red)
            lineEdit.setPalette(Palette)

    @staticmethod
    def checkBoxChanged(checkBox: QCheckBox or QRadioButton, state, key, params, smp: UnkSample = None):
        params.update({key: state})
        Palette = QPalette()
        if smp:
            Palette.setColor(QPalette.Foreground, Qt.blue)
            checkBox.setPalette(Palette)
        else:
            Palette.setColor(QPalette.Foreground, Qt.red)
            checkBox.setPalette(Palette)

    def write_param(self, params):
        print('write_param')
        self.lineEdit_1.setText(str(params["K40Const"]))
        self.lineEdit_2.setText(str(params["K40ECConst"]))
        self.lineEdit_3.setText(str(params["K40BetaNConst"]))
        self.lineEdit_4.setText(str(params["K40BetaPConst"]))
        self.lineEdit_5.setText(str(params["Ar39Const"]))
        self.lineEdit_6.setText(str(params["Ar37Const"]))
        self.lineEdit_7.setText(str(params["Cl36Const"]))
        self.lineEdit_8.setText(str(params["K40ECActivity"]))
        self.lineEdit_9.setText(str(params["K40BetaNActivity"]))
        self.lineEdit_10.setText(str(params["K40BetaPActivity"]))
        self.lineEdit_11.setText(str(params["Cl36vs38Productivity"]))
        self.lineEdit_12.setText(str(params["K40Mass"]))
        self.lineEdit_13.setText(str(params["NoConst"]))
        self.lineEdit_14.setText(str(params["YearConst"]))
        self.lineEdit_15.setText(str(params["K40vsKFractions"]))
        self.lineEdit_16.setText(str(params["Cl35vsCl37Fractions"]))
        self.lineEdit_17.setText(str(params["HClvsClFractions"]))
        self.lineEdit_18.setText(str(params["Ar40vsAr36AirConst"]))
        self.lineEdit_19.setText(str(params["K40ConstError"]))
        self.lineEdit_20.setText(str(params["K40ECConstError"]))
        self.lineEdit_21.setText(str(params["K40BetaNConstError"]))
        self.lineEdit_22.setText(str(params["K40BetaPConstError"]))
        self.lineEdit_23.setText(str(params["Ar39ConstError"]))
        self.lineEdit_24.setText(str(params["Ar37ConstError"]))
        self.lineEdit_25.setText(str(params["Cl36ConstError"]))
        self.lineEdit_26.setText(str(params["K40ECActivityError"]))
        self.lineEdit_27.setText(str(params["K40BetaNActivityError"]))
        self.lineEdit_28.setText(str(params["K40BetaPActivityError"]))
        self.lineEdit_29.setText(str(params["Cl36vs38ProductivityError"]))
        self.lineEdit_30.setText(str(params["K40MassError"]))
        self.lineEdit_31.setText(str(params["NoConstError"]))
        self.lineEdit_32.setText(str(params["YearConstError"]))
        self.lineEdit_33.setText(str(params["K40vsKFractionsError"]))
        self.lineEdit_34.setText(str(params["Cl35vsCl37FractionsError"]))
        self.lineEdit_35.setText(str(params["HClvsClFractionsError"]))
        self.lineEdit_36.setText(str(params["Ar40vsAr36AirConstError"]))
        self.lineEdit_37.setText(str(params["JValue"]))
        self.lineEdit_38.setText(str(params["JValueError"]))
        self.lineEdit_39.setText(str(params["MDF"]))
        self.lineEdit_40.setText(str(params["MDFError"]))
        self.lineEdit_41.setText(str(params["Ar36Mass"]))
        self.lineEdit_42.setText(str(params["Ar36MassError"]))
        self.lineEdit_43.setText(str(params["Ar37Mass"]))
        self.lineEdit_44.setText(str(params["Ar37MassError"]))
        self.lineEdit_45.setText(str(params["Ar38Mass"]))
        self.lineEdit_46.setText(str(params["Ar38MassError"]))
        self.lineEdit_47.setText(str(params["Ar39Mass"]))
        self.lineEdit_48.setText(str(params["Ar39MassError"]))
        self.lineEdit_49.setText(str(params["Ar40Mass"]))
        self.lineEdit_50.setText(str(params["Ar40MassError"]))
        self.lineEdit_51.setText(str(params["York2FitConvergence"]))
        self.lineEdit_52.setText(str(params["York2FitIteration"]))

        self.lineEdit_55.setText(str(params["K40Activity"]))
        self.lineEdit_53.setText(str(params["K40ActivityError"]))

        self.lineEdit_70.setText(str(params["PrimaryStdName"]))
        self.lineEdit_69.setText(str(params["PrimaryStdAge"]))
        self.lineEdit_75.setText(str(params["PrimaryStdAgeError"]))
        self.lineEdit_64.setText(str(params["PrimaryStdAr40Conc"]))
        self.lineEdit_54.setText(str(params["PrimaryStdAr40ConcError"]))
        self.lineEdit_71.setText(str(params["PrimaryStdKConc"]))
        self.lineEdit_72.setText(str(params["PrimaryStdKConcError"]))
        self.lineEdit_60.setText(str(params["PrimaryStdAr40vsK"]))
        self.lineEdit_76.setText(str(params["PrimaryStdAr40vsKError"]))
        """"""
        self.checkBox.setChecked(bool(params["ForceNegative"]))
        self.checkBox_2.setChecked(bool(params["CorrBlank"]))
        self.checkBox_3.setChecked(bool(params["CorrDiscr"]))
        self.checkBox_4.setChecked(bool(params["Corr37ArDecay"]))
        self.checkBox_5.setChecked(bool(params["Corr39ArDecay"]))
        k = "Corr36ClDecay"
        self.checkBox_6.setChecked(bool(params["CorrK"]))
        self.checkBox_7.setChecked(bool(params["CorrCa"]))
        self.checkBox_8.setChecked(bool(params["CorrAtm"]))
        self.checkBox_9.setChecked(bool(params["CorrCl"]))
        self.checkBox_10.setChecked(bool(params["DisplayRelative"]))
        self.checkBox_11.setChecked(bool(params["UseDecayConst"]))
        self.checkBox_12.setChecked(bool(params["UseInterceptCorrAtm"]))
        self.checkBox_13.setChecked(bool(params["RecalibrationToPrimary"]))
        self.checkBox_14.setChecked(bool(params["RecalibrationUseAge"]))
        self.checkBox_15.setChecked(bool(params["RecalibrationUseRatio"]))
        self.comboBox_1.setCurrentText(str(params["Fitting"]))
        self.radioButton.setChecked(bool(params["LinMassDiscrLaw"]))
        self.radioButton_2.setChecked(bool(params["ExpMassDiscrLaw"]))
        self.radioButton_3.setChecked(bool(params["PowMassDiscrLaw"]))

    def display_info(self):
        try:
            with open(os.path.dirname(__file__) + '\\..\\tools\\calcParamsInfo.txt', 'r') as file:
                param_info = file.read()
        except FileNotFoundError as e:
            param_info = str(e)
        QMessageBox.about(self, '参数说明', param_info)

    def closeEvent(self, event):
        print('close')
        self.signalCalculationWindowClose.emit(self.currentCalcParams)

    # read from local files
    def readParams(self):
        print('local button')
        self.write_param(self.calcParamsBackup)

    # import from smp
    def importParams(self, smp):
        print("smp button")
        # 退回最后一次apply的参数
        if smp:
            smp_params_dict = smp.get_calc_params()
            """for key, value in smp_params_dict.items():
                if "Error" in key:
                    value = value * 100 / smp_params_dict[key.split("Error")[0]] \
                        if smp_params_dict[key.split("Error")[0]] != 0 else 0
                    smp_params_dict[key] = value"""
            self.write_param(smp_params_dict)

    def apply(self, params, smp):
        if smp:
            for key, value in params.items():
                if isinstance(value, bool):
                    if smp:
                        smp.__dict__[key] = bool(value)
                elif isinstance(value, str):
                    try:
                        value = [float(value), int(float(value))][float(value) == int(float(value))]
                    except Exception as e:
                        value = value
                    if smp:
                        smp.__dict__[key] = value
                else:
                    pass
            print('发射信号')
            self.write_param(params)
            self.signalCalculationWindowAttach.emit(smp)

    def get_Jvalue(self):
        UI_j_calc = jvalueCalcualtion.SubWindowJvalueCalculation()
        UI_j_calc.signal_jvalue.connect(lambda a0: self.show_Jvalue(a0[0], a0[1]))
        UI_j_calc.exec()

    def show_Jvalue(self, a0, a1):
        try:
            float(a0); float(a1)
        except Exception as e:
            return
        else:
            self.lineEdit_37.setText(str(a0))
            self.lineEdit_38.setText(str(a1))


if __name__ == '__main__':
    _calc_param = CalcParams().__dict__
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    UI = SubWindowCalculation(_calc_param)
    UI.show()
    sys.exit(app.exec())
