import sys
from PyQt5.QtCore import QCoreApplication, Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QApplication, QSpinBox, QLabel
import pyarar.ui.UI_DisplaySettingWindow as UI_DisplaySettingWindow

class SubWindowDisplaySetting(QDialog, UI_DisplaySettingWindow.Ui_Dialog_DisplaySetting):
    Signal_displaySettingWindow = pyqtSignal(list)

    def __init__(self, setting_list):
        super(SubWindowDisplaySetting, self).__init__()
        self.setupUi(self)
        print('DisplaySetting')
        if not setting_list:
            setting_list = [[False, False, True], [4] * 10, [5] * 10]
        self.pushButton_apply.clicked.connect(self.button_apply)
        self.pushButton_ok.clicked.connect(self.button_ok)

        self.checkBox_2.stateChanged.connect(self.checkBox_state_changed)
        self.checkBox_3.stateChanged.connect(self.checkBox_state_changed)
        self.checkBox.stateChanged.connect(self.checkBox_state_changed)

        self.spinBox_list_1 = self.groupBox.findChildren(QSpinBox)
        self.spinBox_list_2 = self.groupBox_2.findChildren(QSpinBox)

        self.auto_write(setting_list)

    def button_apply(self):
        print('点击了apply')
        setting_list = [[], [], []]
        setting_list[0].append(self.checkBox_2.isChecked())
        setting_list[0].append(self.checkBox_3.isChecked())
        setting_list[0].append(self.checkBox.isChecked())
        setting_list[1] = [i.value() for i in self.spinBox_list_1]
        setting_list[2] = [i.value() for i in self.spinBox_list_2]
        # 发射信号
        print('传回参数: %s' % setting_list)
        print('将从apply发射信号')
        self.Signal_displaySettingWindow.emit(setting_list)

    def button_ok(self):
        self.button_apply()
        self.close()

    def auto_write(self, setting_list):
        print("auto write")
        self.checkBox_2.setChecked(setting_list[0][0])
        self.checkBox_3.setChecked(setting_list[0][1])
        self.checkBox.setChecked(setting_list[0][2])
        for i in range(len(self.spinBox_list_1)):
            self.spinBox_list_1[i].setValue(setting_list[1][i])
        for i in range(len(self.spinBox_list_2)):
            self.spinBox_list_2[i].setValue(setting_list[2][i])

    def checkBox_state_changed(self):
        for i in self.groupBox.findChildren((QLabel, QSpinBox)) + self.groupBox_2.findChildren((QLabel, QSpinBox)):
            i.setDisabled(True)
        if self.checkBox_2.isChecked():
            for i in self.groupBox.findChildren((QLabel, QSpinBox)):
                i.setDisabled(False)
        if self.checkBox_3.isChecked():
            for i in self.groupBox_2.findChildren((QLabel, QSpinBox)):
                i.setDisabled(False)


if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    display_setting = [[False, False, True], [4] * 10, [5] * 10]
    UI = SubWindowDisplaySetting(display_setting)
    UI.show()
    sys.exit(app.exec())
