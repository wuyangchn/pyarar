# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_AxisSetting.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_AxisSetting(object):
    def setupUi(self, Dialog_AxisSetting):
        Dialog_AxisSetting.setObjectName("Dialog_AxisSetting")
        Dialog_AxisSetting.resize(601, 630)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        Dialog_AxisSetting.setFont(font)
        self.pushButton_apply = QtWidgets.QPushButton(Dialog_AxisSetting)
        self.pushButton_apply.setGeometry(QtCore.QRect(510, 600, 71, 23))
        self.pushButton_apply.setObjectName("pushButton_apply")
        self.pushButton_ok = QtWidgets.QPushButton(Dialog_AxisSetting)
        self.pushButton_ok.setGeometry(QtCore.QRect(420, 600, 71, 23))
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.groupBox = QtWidgets.QGroupBox(Dialog_AxisSetting)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 581, 161))
        self.groupBox.setObjectName("groupBox")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setGeometry(QtCore.QRect(290, 60, 281, 20))
        self.checkBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox.setObjectName("checkBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(110, 20, 54, 12))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(190, 50, 54, 12))
        self.label_2.setObjectName("label_2")
        self.checkBox_3 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_3.setGeometry(QtCore.QRect(390, 90, 161, 20))
        self.checkBox_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox_3.setObjectName("checkBox_3")
        self.lineEdit_bottom = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_bottom.setGeometry(QtCore.QRect(110, 100, 71, 20))
        self.lineEdit_bottom.setObjectName("lineEdit_bottom")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(30, 50, 54, 12))
        self.label_4.setObjectName("label_4")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(110, 130, 54, 12))
        self.label_3.setObjectName("label_3")
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_2.setGeometry(QtCore.QRect(290, 90, 91, 20))
        self.checkBox_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox_2.setObjectName("checkBox_2")
        self.lineEdit_top = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_top.setGeometry(QtCore.QRect(110, 40, 71, 20))
        self.lineEdit_top.setObjectName("lineEdit_top")
        self.lineEdit_right = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_right.setGeometry(QtCore.QRect(190, 70, 71, 20))
        self.lineEdit_right.setObjectName("lineEdit_right")
        self.lineEdit_left = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_left.setGeometry(QtCore.QRect(30, 70, 71, 20))
        self.lineEdit_left.setObjectName("lineEdit_left")
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog_AxisSetting)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 180, 581, 111))
        self.groupBox_2.setObjectName("groupBox_2")
        self.comboBox_scatter_size = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_scatter_size.setGeometry(QtCore.QRect(110, 20, 91, 20))
        self.comboBox_scatter_size.setObjectName("comboBox_scatter_size")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(20, 20, 81, 20))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(20, 50, 81, 20))
        self.label_6.setObjectName("label_6")
        self.comboBox_scatter_b_c = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_scatter_b_c.setGeometry(QtCore.QRect(110, 50, 91, 20))
        self.comboBox_scatter_b_c.setObjectName("comboBox_scatter_b_c")
        self.label_scatter_b_c = QtWidgets.QLabel(self.groupBox_2)
        self.label_scatter_b_c.setGeometry(QtCore.QRect(210, 50, 81, 20))
        self.label_scatter_b_c.setText("")
        self.label_scatter_b_c.setObjectName("label_scatter_b_c")
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setGeometry(QtCore.QRect(300, 20, 81, 20))
        self.label_8.setObjectName("label_8")
        self.comboBox_scatter_style = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_scatter_style.setGeometry(QtCore.QRect(390, 20, 91, 20))
        self.comboBox_scatter_style.setObjectName("comboBox_scatter_style")
        self.label_21 = QtWidgets.QLabel(self.groupBox_2)
        self.label_21.setGeometry(QtCore.QRect(20, 80, 121, 20))
        self.label_21.setObjectName("label_21")
        self.checkBox_show_random_points = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_show_random_points.setGeometry(QtCore.QRect(150, 80, 20, 20))
        self.checkBox_show_random_points.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox_show_random_points.setText("")
        self.checkBox_show_random_points.setObjectName("checkBox_show_random_points")
        self.label_22 = QtWidgets.QLabel(self.groupBox_2)
        self.label_22.setGeometry(QtCore.QRect(260, 80, 111, 20))
        self.label_22.setObjectName("label_22")
        self.lineEdit_random_points_num = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_random_points_num.setGeometry(QtCore.QRect(390, 80, 91, 20))
        self.lineEdit_random_points_num.setObjectName("lineEdit_random_points_num")
        self.groupBox_3 = QtWidgets.QGroupBox(Dialog_AxisSetting)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 390, 581, 81))
        self.groupBox_3.setObjectName("groupBox_3")
        self.label_9 = QtWidgets.QLabel(self.groupBox_3)
        self.label_9.setGeometry(QtCore.QRect(20, 50, 81, 20))
        self.label_9.setObjectName("label_9")
        self.comboBox_ellipse_b_c = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_ellipse_b_c.setGeometry(QtCore.QRect(110, 50, 91, 20))
        self.comboBox_ellipse_b_c.setObjectName("comboBox_ellipse_b_c")
        self.label_10 = QtWidgets.QLabel(self.groupBox_3)
        self.label_10.setGeometry(QtCore.QRect(300, 50, 81, 20))
        self.label_10.setObjectName("label_10")
        self.comboBox_ellipse_f_c = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_ellipse_f_c.setGeometry(QtCore.QRect(390, 50, 91, 20))
        self.comboBox_ellipse_f_c.setObjectName("comboBox_ellipse_f_c")
        self.label_ellipse_b_c = QtWidgets.QLabel(self.groupBox_3)
        self.label_ellipse_b_c.setGeometry(QtCore.QRect(210, 50, 81, 20))
        self.label_ellipse_b_c.setText("")
        self.label_ellipse_b_c.setObjectName("label_ellipse_b_c")
        self.label_ellipse_f_c = QtWidgets.QLabel(self.groupBox_3)
        self.label_ellipse_f_c.setGeometry(QtCore.QRect(490, 50, 81, 20))
        self.label_ellipse_f_c.setText("")
        self.label_ellipse_f_c.setObjectName("label_ellipse_f_c")
        self.checkBox_ellipse = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_ellipse.setGeometry(QtCore.QRect(80, 20, 20, 20))
        self.checkBox_ellipse.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox_ellipse.setText("")
        self.checkBox_ellipse.setObjectName("checkBox_ellipse")
        self.label_11 = QtWidgets.QLabel(self.groupBox_3)
        self.label_11.setGeometry(QtCore.QRect(20, 20, 51, 20))
        self.label_11.setObjectName("label_11")
        self.groupBox_4 = QtWidgets.QGroupBox(Dialog_AxisSetting)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 300, 581, 81))
        self.groupBox_4.setObjectName("groupBox_4")
        self.comboBox_line_w = QtWidgets.QComboBox(self.groupBox_4)
        self.comboBox_line_w.setGeometry(QtCore.QRect(110, 20, 91, 20))
        self.comboBox_line_w.setObjectName("comboBox_line_w")
        self.label_14 = QtWidgets.QLabel(self.groupBox_4)
        self.label_14.setGeometry(QtCore.QRect(20, 20, 81, 20))
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.groupBox_4)
        self.label_15.setGeometry(QtCore.QRect(300, 20, 81, 20))
        self.label_15.setObjectName("label_15")
        self.comboBox_line_s = QtWidgets.QComboBox(self.groupBox_4)
        self.comboBox_line_s.setGeometry(QtCore.QRect(390, 20, 91, 20))
        self.comboBox_line_s.setObjectName("comboBox_line_s")
        self.label_16 = QtWidgets.QLabel(self.groupBox_4)
        self.label_16.setGeometry(QtCore.QRect(20, 50, 81, 20))
        self.label_16.setObjectName("label_16")
        self.comboBox_line_c = QtWidgets.QComboBox(self.groupBox_4)
        self.comboBox_line_c.setGeometry(QtCore.QRect(110, 50, 91, 20))
        self.comboBox_line_c.setObjectName("comboBox_line_c")
        self.label_line_c = QtWidgets.QLabel(self.groupBox_4)
        self.label_line_c.setGeometry(QtCore.QRect(210, 50, 81, 20))
        self.label_line_c.setText("")
        self.label_line_c.setObjectName("label_line_c")
        self.label_scatter_f_c = QtWidgets.QLabel(Dialog_AxisSetting)
        self.label_scatter_f_c.setGeometry(QtCore.QRect(500, 230, 81, 20))
        self.label_scatter_f_c.setText("")
        self.label_scatter_f_c.setObjectName("label_scatter_f_c")
        self.comboBox_scatter_f_c = QtWidgets.QComboBox(Dialog_AxisSetting)
        self.comboBox_scatter_f_c.setGeometry(QtCore.QRect(400, 230, 91, 20))
        self.comboBox_scatter_f_c.setObjectName("comboBox_scatter_f_c")
        self.label_7 = QtWidgets.QLabel(Dialog_AxisSetting)
        self.label_7.setGeometry(QtCore.QRect(310, 230, 81, 20))
        self.label_7.setObjectName("label_7")
        self.groupBox_5 = QtWidgets.QGroupBox(Dialog_AxisSetting)
        self.groupBox_5.setGeometry(QtCore.QRect(10, 480, 581, 111))
        self.groupBox_5.setObjectName("groupBox_5")
        self.label_12 = QtWidgets.QLabel(self.groupBox_5)
        self.label_12.setGeometry(QtCore.QRect(20, 50, 81, 20))
        self.label_12.setObjectName("label_12")
        self.comboBox_spectra_b_c = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_spectra_b_c.setGeometry(QtCore.QRect(110, 50, 91, 20))
        self.comboBox_spectra_b_c.setObjectName("comboBox_spectra_b_c")
        self.label_13 = QtWidgets.QLabel(self.groupBox_5)
        self.label_13.setGeometry(QtCore.QRect(300, 50, 81, 20))
        self.label_13.setObjectName("label_13")
        self.comboBox_spectra_f_c = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_spectra_f_c.setGeometry(QtCore.QRect(390, 50, 91, 20))
        self.comboBox_spectra_f_c.setObjectName("comboBox_spectra_f_c")
        self.label_spectra_b_c = QtWidgets.QLabel(self.groupBox_5)
        self.label_spectra_b_c.setGeometry(QtCore.QRect(210, 50, 81, 20))
        self.label_spectra_b_c.setText("")
        self.label_spectra_b_c.setObjectName("label_spectra_b_c")
        self.label_spectra_f_c = QtWidgets.QLabel(self.groupBox_5)
        self.label_spectra_f_c.setGeometry(QtCore.QRect(490, 50, 81, 20))
        self.label_spectra_f_c.setText("")
        self.label_spectra_f_c.setObjectName("label_spectra_f_c")
        self.label_17 = QtWidgets.QLabel(self.groupBox_5)
        self.label_17.setGeometry(QtCore.QRect(20, 20, 81, 20))
        self.label_17.setObjectName("label_17")
        self.comboBox_spectra_w = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_spectra_w.setGeometry(QtCore.QRect(110, 20, 91, 20))
        self.comboBox_spectra_w.setObjectName("comboBox_spectra_w")
        self.label_18 = QtWidgets.QLabel(self.groupBox_5)
        self.label_18.setGeometry(QtCore.QRect(300, 20, 81, 20))
        self.label_18.setObjectName("label_18")
        self.comboBox_spectra_s = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_spectra_s.setGeometry(QtCore.QRect(390, 20, 91, 20))
        self.comboBox_spectra_s.setObjectName("comboBox_spectra_s")
        self.comboBox_plateau_b_c = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_plateau_b_c.setGeometry(QtCore.QRect(110, 80, 91, 20))
        self.comboBox_plateau_b_c.setObjectName("comboBox_plateau_b_c")
        self.label_19 = QtWidgets.QLabel(self.groupBox_5)
        self.label_19.setGeometry(QtCore.QRect(20, 80, 81, 20))
        self.label_19.setObjectName("label_19")
        self.comboBox_plateau_f_c = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_plateau_f_c.setGeometry(QtCore.QRect(390, 80, 91, 20))
        self.comboBox_plateau_f_c.setObjectName("comboBox_plateau_f_c")
        self.label_20 = QtWidgets.QLabel(self.groupBox_5)
        self.label_20.setGeometry(QtCore.QRect(300, 80, 81, 20))
        self.label_20.setObjectName("label_20")
        self.label_plateau_b_c = QtWidgets.QLabel(self.groupBox_5)
        self.label_plateau_b_c.setGeometry(QtCore.QRect(210, 80, 81, 20))
        self.label_plateau_b_c.setText("")
        self.label_plateau_b_c.setObjectName("label_plateau_b_c")
        self.label_plateau_f_c = QtWidgets.QLabel(self.groupBox_5)
        self.label_plateau_f_c.setGeometry(QtCore.QRect(490, 80, 81, 20))
        self.label_plateau_f_c.setText("")
        self.label_plateau_f_c.setObjectName("label_plateau_f_c")

        self.retranslateUi(Dialog_AxisSetting)
        QtCore.QMetaObject.connectSlotsByName(Dialog_AxisSetting)

    def retranslateUi(self, Dialog_AxisSetting):
        _translate = QtCore.QCoreApplication.translate
        Dialog_AxisSetting.setWindowTitle(_translate("Dialog_AxisSetting", "Dialog"))
        self.pushButton_apply.setText(_translate("Dialog_AxisSetting", "Apply"))
        self.pushButton_ok.setText(_translate("Dialog_AxisSetting", "OK"))
        self.groupBox.setTitle(_translate("Dialog_AxisSetting", "Axis"))
        self.checkBox.setText(_translate("Dialog_AxisSetting", "Same sacle of Horizontal and Vertical Axes"))
        self.label.setText(_translate("Dialog_AxisSetting", "Top"))
        self.label_2.setText(_translate("Dialog_AxisSetting", "Right"))
        self.checkBox_3.setText(_translate("Dialog_AxisSetting", "Ignore isochron line"))
        self.label_4.setText(_translate("Dialog_AxisSetting", "Left"))
        self.label_3.setText(_translate("Dialog_AxisSetting", "Bottom"))
        self.checkBox_2.setText(_translate("Dialog_AxisSetting", "Auto scale"))
        self.groupBox_2.setTitle(_translate("Dialog_AxisSetting", "Scatter"))
        self.label_5.setText(_translate("Dialog_AxisSetting", "Scatter size:"))
        self.label_6.setText(_translate("Dialog_AxisSetting", "Border color:"))
        self.label_8.setText(_translate("Dialog_AxisSetting", "Point style:"))
        self.label_21.setText(_translate("Dialog_AxisSetting", "Show Random Points:"))
        self.label_22.setText(_translate("Dialog_AxisSetting", "Number of Points:"))
        self.groupBox_3.setTitle(_translate("Dialog_AxisSetting", "Ellipse"))
        self.label_9.setText(_translate("Dialog_AxisSetting", "Border color:"))
        self.label_10.setText(_translate("Dialog_AxisSetting", "Fill color:"))
        self.label_11.setText(_translate("Dialog_AxisSetting", "Ellipse:"))
        self.groupBox_4.setTitle(_translate("Dialog_AxisSetting", "Line"))
        self.label_14.setText(_translate("Dialog_AxisSetting", "Line width:"))
        self.label_15.setText(_translate("Dialog_AxisSetting", "Line style:"))
        self.label_16.setText(_translate("Dialog_AxisSetting", "Line color:"))
        self.label_7.setText(_translate("Dialog_AxisSetting", "Fill color:"))
        self.groupBox_5.setTitle(_translate("Dialog_AxisSetting", "Age Spectra"))
        self.label_12.setText(_translate("Dialog_AxisSetting", "Line color:"))
        self.label_13.setText(_translate("Dialog_AxisSetting", "Fill color:"))
        self.label_17.setText(_translate("Dialog_AxisSetting", "Line width:"))
        self.label_18.setText(_translate("Dialog_AxisSetting", "Line style:"))
        self.label_19.setText(_translate("Dialog_AxisSetting", "Plateau color:"))
        self.label_20.setText(_translate("Dialog_AxisSetting", "Plateau fill:"))