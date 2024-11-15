import sys
import os
from PySide6.QtCore import Qt
from PySide6.QtQuick import QQuickView
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import QUrl
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtWidgets import QApplication

daily_plans = None


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


def main():
    app = QGuiApplication(sys.argv)

    # Set up the QQuickView and load the QML file
    engine = QQmlApplicationEngine()
    api_key = "Hi"
    self_description = "bye"
    bridge = Bridge(api_key, self_description)
    engine.rootContext().setContextProperty("con", bridge)
    qml_file = get_resource_path("FromScratch2.qml")

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

    

    sys.exit(app.exec())

if __name__ == "__main__":
    main()


# pyinstaller --onefile --add-data "FromScratch.qml:." FromScratch.py
# pyinstaller --onefile --add-data "FromScratch.qml:." --add-data "images/*:images" FromScratch.py