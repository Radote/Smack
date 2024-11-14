
import os
import sys
from pathlib import Path

from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication


from autogen.settings import url, import_paths

daily_plans = None

def set_daily_plans(daily_plan):
    global daily_plans
    daily_plans = daily_plan

#@QmlElement
class Bridge(QObject):
    global daily_plans
    apiKeyReady = Signal(str) # Note, in the scene01 file this is onApiKeyReady (weird QML syntax)
    selfDescriptReady = Signal(str)

    def __init__(self, api_key, self_description):
        super().__init__()
        self.api_key = api_key
        self.self_description = self_description


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
        set_daily_plans(s)
        print("START")
        QApplication.quit()


        
    
def start_GUI(api_key, self_description):
    global daily_plans
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    bridge = Bridge(api_key, self_description)
    engine.rootContext().setContextProperty("con", bridge)
    app_dir = Path(__file__).parent.parent

    engine.addImportPath(os.fspath(app_dir))
    for path in import_paths:
        engine.addImportPath(os.fspath(app_dir / path))

    engine.load(os.fspath(app_dir/url))
    bridge.load_api_key()
    bridge.load_self_description()
    if not engine.rootObjects():
        sys.exit(-1)
    app.exec()
    return daily_plans

if __name__ == '__main__':
    start_GUI("Nuhuh", "That's me")

