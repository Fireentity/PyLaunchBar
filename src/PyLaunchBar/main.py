from enum import Enum

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


class IconController(QObject):

    @pyqtSlot()
    def on_click(self, command):
        os.system(command)


class Roles(Enum):
    ICON = 0,
    COMMAND = 1


class IconsListModel(QAbstractListModel):

    def __init__(self, config_folder_path, entries):
        super().__init__()
        self.entries = entries
        self.config_folder_path = config_folder_path

    def roleNames(self):
        return {0: QByteArray(b"icon"), 1: QByteArray(b"command")}

    def rowCount(self, parent=None, *args, **kwargs):
        if parent.isValid():
            return 0
        else:
            return len(self.entries)

    def data(self, model_index: QModelIndex, role=None):
        if role == Roles.ICON.value:
            return self.config_folder_path + "/" + self.entries[model_index.row()]['icon']

        if role == Roles.COMMAND.value:
            return self.entries[model_index.row()]['command']


def start():
    app = QApplication([])
    view = QQmlApplicationEngine()

    # Initializing config folder path
    config_folder_path = "/.config/PyLaunchBar"

    icons_folder_path = "/icons"

    # Getting config folder path
    user_config_folder_path = os.path.expanduser("~") + config_folder_path

    # Getting config file path
    user_config_file_path = user_config_folder_path + "/config.json"

    user_icons_folder_path = user_config_folder_path + icons_folder_path

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
    model = IconsListModel(user_icons_folder_path, json_data)

    icon_controller = IconController()

    # Setting QStringListModel() has context property
    view.rootContext().setContextProperty("icons_model", model)
    view.rootContext().setContextProperty("icon_controller", icon_controller)

    # Loading file manually because of a strange error that attaches /home/lorenzo in front
    # of the path passed as parameter in the method QQmlApplicationEngine::load(url: QUrl)
    window_qml = pkg_resources.read_text(data, "window.qml")
    # Loading file from an array of bytes
    view.loadData(QByteArray(bytearray(window_qml, "utf_8")))

    view.rootObjects()[0].findChild(QObject, "background")
    app.exec()
