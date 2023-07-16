from qgis import utils
from qgis.utils import iface
import os
from PyQt5 import QtWidgets, QtGui
from qgis.core import QgsApplication, QgsProject
import subprocess

class Main(object):
    def __init__(self, iface):
        self.restartAction = None
        self.iface = iface

    def initGui(self):
        self.restartAction = self.createAction(
            'Restart QGIS',
            os.path.join(
                os.path.abspath(os.path.join(
                    os.path.dirname(__file__)
                )),
                'icons',
                'ok.png'
            ),
            self.restart
        )
        self.addActionDigitizeToolBar(self.restartAction)

    def createAction(self, name, iconPath, callback):
        a = QtWidgets.QAction(
            QtGui.QIcon(iconPath),
            name,
            iface.mainWindow()
        )
        a.triggered.connect(callback)
        return a

    def showError(self, title, message):
        err_box = QtWidgets.QMessageBox()
        err_box.setWindowTitle(title)
        err_box.setText(message)
        err_box.setIcon(QtWidgets.QMessageBox.Critical)
        err_box.exec_()

    def restart(self):
        if QgsProject.instance().isDirty():
            self.showError('Erro', 'Salve o projeto antes!')
            return
        
        project_path = QgsProject.instance().absoluteFilePath()
        if not project_path:
            self.showError('Erro', 'Salve o projeto antes!')
            return
            
        subprocess.Popen([QgsApplication.applicationFilePath(), project_path])
        self.iface.actionExit().trigger()
        
    def addActionDigitizeToolBar(self, action):
        iface.digitizeToolBar().addAction(action)

    def removeActionDigitizeToolBar(self, action):
        iface.digitizeToolBar().removeAction(action)

    def unload(self):
        self.removeActionDigitizeToolBar(self.restartAction)