import QtQuick 
import QtQuick.Controls 

ApplicationWindow {
    visible: true
    width: 640
    height: 480
    title: "PySide6 QML Example"

    Button {
        text: "Click Me"
        anchors.centerIn: parent
        onClicked: {
            console.log("Button clicked!")
        }
    }

    Image {
            id: settingsicon
            x: 26
            y: 300
            width: 52
            height: 52
            source: "images/gear-solid.svg"
            z: 1
            fillMode: Image.PreserveAspectFit
        }
}
