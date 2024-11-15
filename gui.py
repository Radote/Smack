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
    
    def __init__(self, api_key, self_description):
        super().__init__()
        self.api_key = api_key
        self.self_description = self_description
        self.daily_plans = ""

    @Slot(str)
    def api_key_GtoP(self, s):
        print(s)
    
    @Slot(result=str)
    def load_api_key(self):
        self.apiKeyReady.emit(self.api_key)

    @Slot(result=str)
    def load_self_description(self):
        self.selfDescriptReady.emit(self.self_description)
    @Slot(str)
    def start_program(self, s):
        self.daily_plans = s
        print("START")
        QApplication.quit()

def get_resource_path(file_name):
    if getattr(sys, 'frozen', False):  # Check if running in a bundled app
        # If running as a bundle, resources are in the _MEIPASS directory
        base_path = sys._MEIPASS
    else:
        # If running in a normal (non-bundled) environment, use the current script directory
        base_path = os.path.dirname(__file__)
    return QUrl.fromLocalFile(os.path.join(base_path, file_name))


def start_GUI(api_key, self_description):
    app = QGuiApplication(sys.argv)

    # Set up the QQuickView and load the QML file
    engine = QQmlApplicationEngine()
    bridge = Bridge(api_key, self_description)
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

    app.exec()

    return bridge.daily_plans

if __name__ == "__main__":
    start_GUI("Nuhuh", "That's me")


# pyinstaller --onefile --add-data "FromScratch.qml:." FromScratch.py
# pyinstaller --onefile --add-data "FromScratch2.qml:." --add-data "images/*:images" FromScratch.py
# pyinstaller --onefile --add-data "smack.qml:." --add-data "images/*:images" FromScratch.py
# pyinstaller --onefile --add-data "smack.qml:." --add-data "images/*:images" smack.py
# pyinstaller --onefile --add-data "input_output/smack.qml:input_output" --add-data "input_output/images/*:input_output/images" smack.py
