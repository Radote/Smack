import sys
import os
from PySide6.QtCore import Qt
from PySide6.QtQuick import QQuickView
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import QUrl
from PySide6.QtQml import QQmlApplicationEngine

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
    qml_file = get_resource_path("FromScratch.qml")

    # Check if the QML file exists and load it
    if not qml_file.isValid():
        print("Error: QML file not found.")
        return

    engine.load(qml_file)

    if not engine.rootObjects():
        print("Error: No root object found in QML.")
        return

    sys.exit(app.exec())

if __name__ == "__main__":
    main()


# pyinstaller --onefile --add-data "FromScratch.qml:." FromScratch.py
# pyinstaller --onefile --add-data "FromScratch.qml:." --add-data "images/*:images" FromScratch.py