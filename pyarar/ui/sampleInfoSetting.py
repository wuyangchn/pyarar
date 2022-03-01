import os
import sys
from copy import deepcopy

from PyQt5.QtCore import QCoreApplication, Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QApplication

from pyarar.sample import Sample, UnkSample, AirSample, MonitorSample
from pyarar.ui import UI_SampleInfoWindow


class SubWindowSampleInfo(QDialog, UI_SampleInfoWindow.Ui_Dialog_SampleInfo):
    signalSampleInfoWindowAttach = pyqtSignal(Sample or UnkSample or AirSample or MonitorSample)

    def __init__(self, params, smp: Sample):
        super(SubWindowSampleInfo, self).__init__()
        self.setupUi(self)
        self.smp = deepcopy(smp)
        self.pushButton_3.setIcon(QIcon(os.path.dirname(__file__) + "/../../tools/info.jpg"))
        self.write_param(params)
        self.currentParams: dict = deepcopy(params)
        
        self.lineEdit_1.textChanged.connect(lambda text: setattr(self.smp, "SampleName", text))
        self.lineEdit_2.textChanged.connect(lambda text: setattr(self.smp, "SampleOwner", text))
        self.lineEdit_3.textChanged.connect(lambda text: setattr(self.smp, "SampleRock", text))
        self.lineEdit_4.textChanged.connect(lambda text: setattr(self.smp, "SampleMineral", text))
        self.lineEdit_5.textChanged.connect(lambda text: setattr(self.smp, "SampleLocation", text))
        self.lineEdit_6.textChanged.connect(lambda text: setattr(self.smp, "SampleGrainSize", text))
        self.lineEdit_7.textChanged.connect(lambda text: setattr(self.smp, "SampleGrainMesh", text))
        self.lineEdit_8.textChanged.connect(lambda text: setattr(self.smp, "SampleDescription", text))
        self.lineEdit_9.textChanged.connect(lambda text: setattr(self.smp, "ExperimentName", text))
        self.lineEdit_10.textChanged.connect(lambda text: setattr(self.smp, "ReactorProject", text))
        self.lineEdit_11.textChanged.connect(lambda text: setattr(self.smp, "ExperimentAnalyst", text))
        self.lineEdit_12.textChanged.connect(lambda text: setattr(self.smp, "Instrument", text))
        self.lineEdit_13.textChanged.connect(lambda text: setattr(self.smp, "LaboratoryName", text))
        self.lineEdit_14.textChanged.connect(lambda text: setattr(self.smp, "LaboratoryInfo", text))
        self.lineEdit_15.textChanged.connect(lambda text: setattr(self.smp, "ReactorLocation", text))

        self.pushButton.clicked.connect(lambda: self.signalSampleInfoWindowAttach.emit(self.smp))

    def write_param(self, params):
        self.lineEdit_1.setText(str(params["SampleName"]))
        self.lineEdit_2.setText(str(params["SampleOwner"]))
        self.lineEdit_3.setText(str(params["SampleRock"]))
        self.lineEdit_4.setText(str(params["SampleMineral"]))
        self.lineEdit_5.setText(str(params["SampleLocation"]))
        self.lineEdit_6.setText(str(params["SampleGrainSize"]))
        self.lineEdit_7.setText(str(params["SampleGrainMesh"]))
        self.lineEdit_8.setText(str(params["SampleDescription"]))

        self.lineEdit_9.setText(str(params["ExperimentName"]))
        self.lineEdit_10.setText(str(params["ReactorProject"]))
        self.lineEdit_11.setText(str(params["ExperimentAnalyst"]))
        self.lineEdit_12.setText(str(params["Instrument"]))
        self.lineEdit_13.setText(str(params["LaboratoryName"]))
        self.lineEdit_14.setText(str(params["LaboratoryInfo"]))
        self.lineEdit_15.setText(str(params["ReactorLocation"]))

    def read_param(self):
        self.paramsBackup.update({"CavsClFactor": text})


if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    UI = SubWindowSampleInfo()
    UI.show()
    sys.exit(app.exec())
