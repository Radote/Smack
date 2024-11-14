
import os
import sys
from pathlib import Path

from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from autogen.settings import url, import_paths

#@QmlElement
class Bridge(QObject):
    apiKeyReady = Signal(str)

    @Slot(str)
    def api_key_GtoP(self, s):
        print(s)
    
    @Slot(result=str)
    def load_api_key(self):
        self.apiKeyReady.emit("Insert key here")

    @Slot()
    def start_program(self):
        print("START")
        pass
        
    
    

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    bridge = Bridge()
    engine.rootContext().setContextProperty("con", bridge)
    app_dir = Path(__file__).parent.parent

    engine.addImportPath(os.fspath(app_dir))
    for path in import_paths:
        engine.addImportPath(os.fspath(app_dir / path))

    engine.load(os.fspath(app_dir/url))
    bridge.load_api_key()
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
