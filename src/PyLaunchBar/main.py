from PyQt5 import QtQuick, QtCore, QtQml
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtQml import *
from PyQt5.QtQuick import QQuickItem
from PyQt5.QtWidgets import QApplication
import json
import os
import importlib.resources as pkg_resources
from . import config
from . import data


class ProgramsListModel(QAbstractListModel):

    def rowCount(self, parent=None, *args, **kwargs):
        if parent.isValid():
            return 0
        else:
            return len(self.entries)

    def roleNames(self):
        return {0: QByteArray(b"icon")}

    def data(self, model_index: QModelIndex, role=None):
        return self.entries[model_index.row()]['icon']

    def __init__(self, entries):
        super().__init__()
        self.entries = entries


class IconController(QObject):
    def __init__(self, command):
        super().__init__()
        self.command = command

    @pyqtSlot()
    def on_click(self):
        os.system(self.command)


def start():
    app = QApplication([])
    view = QQmlApplicationEngine()

    # Getting config file path
    user_config_file_path = os.path.expanduser("~") + "/.config/PyLauncher/config.json"
    # Getting config folder path
    user_config_folder_path = os.path.expanduser("~") + "/.config/PyLauncher/"

    # Check if the config file exists
    if not os.path.exists(user_config_file_path):
        # Create the file if the config file does not exist
        os.mkdir(user_config_folder_path)
        config_json = pkg_resources.read_text(config, "config.json")
        with open(user_config_file_path, 'w+') as file:
            file.write(config_json)

    # Paring from json to Object
    with open(user_config_file_path, 'r') as file:
        json_data = json.load(file)

    # Creating the model for the ListView of icons
    model = QStringListModel()
    strings = []
    for program in json_data:
        strings.append(program['icon'])

    # Setting the list of string containing paths to .svg files
    model.setStringList(strings)

    # Setting QStringListModel() has context property
    view.rootContext().setContextProperty("icons_model", model)

    # Loading file manually because of a strange error that attaches /home/lorenzo in front
    # of the path passed as parameter in the method QQmlApplicationEngine::load(url: QUrl)
    window_qml = pkg_resources.read_text(data, "window.qml")
    # Loading file from an array of bytes
    view.loadData(QByteArray(bytearray(window_qml, "utf_8")))

    view.rootObjects()[0].findChild(QObject, "background")
    app.exec()
