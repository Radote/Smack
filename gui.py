import sys
import os
from PySide6.QtCore import Qt
from PySide6.QtQuick import QQuickView
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import QUrl
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtWidgets import QApplication


class Bridge(QObject):
    global daily_plans
    apiKeyReady = Signal(str) # Note, in the scene01 file this is onApiKeyReady (weird QML syntax)
    selfDescriptReady = Signal(str)
    useCacheReady = Signal(bool)

    def __init__(self, api_key, self_description, no_cache):
        super().__init__()
        self.api_key = api_key
        self.self_description = self_description
        self.daily_plans = ""
        self.add_to_wildcardlist = {}
        self.no_cache = no_cache

    @Slot(str)
    def api_key_GtoP(self, s):
        self.api_key = s
    
    @Slot(result=str)
    def load_api_key(self):
        self.apiKeyReady.emit(self.api_key)

    @Slot(result=str)
    def load_self_description(self):
        self.selfDescriptReady.emit(self.self_description)

    @Slot(result=bool)
    def load_no_cache(self):
        print("DONE")
        self.useCacheReady.emit(self.no_cache)

    @Slot(str, str, str, bool)
    def start_program(self, s, t, v, w):
        self.daily_plans = s
        self.api_key = t
        self.self_description = v
        self.no_cache = w
        print("START")
        QApplication.quit()
    
    @Slot(str)
    def allow_word(self, s):
        self.add_to_wildcardlist[s] = True

    @Slot(str)
    def block_word(self, s):
        self.add_to_wildcardlist[s] = False

def get_resource_path(file_name):
    if getattr(sys, 'frozen', False):  # Check if running in a bundled app
        # If running as a bundle, resources are in the _MEIPASS directory
        base_path = sys._MEIPASS
    else:
        # If running in a normal (non-bundled) environment, use the current script directory
        base_path = os.path.dirname(__file__)
    return QUrl.fromLocalFile(os.path.join(base_path, file_name))


def start_GUI(api_key, self_description, no_cache):
    app = QGuiApplication(sys.argv)

    # Set up the QQuickView and load the QML file
    engine = QQmlApplicationEngine()
    bridge = Bridge(api_key, self_description, no_cache)
    engine.rootContext().setContextProperty("con", bridge)
    qml_file = get_resource_path("smack.qml")

    # Check if the QML file exists and load it
    if not qml_file.isValid():
        print("Error: QML file not found.")
        return

    engine.load(qml_file)

    if not engine.rootObjects():
        print("Error: No root object found in QML.")
        return
    
    bridge.load_api_key()
    bridge.load_self_description()
    bridge.load_no_cache()

    app.exec()

    return {
        "plans": bridge.daily_plans, 
        "api-key": bridge.api_key, 
        "self-description": bridge.self_description, 
        "add-to-wildcardlist": bridge.add_to_wildcardlist,
        "no-cache": bridge.no_cache
    }

if __name__ == "__main__":
    start_GUI("Nuhuh", "That's me")


# pyinstaller --onefile --add-data "smack.qml:." --add-data "images/*:images" smack.py
