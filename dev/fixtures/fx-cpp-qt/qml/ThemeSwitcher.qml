// F06z: ThemeSwitcher.qml - widget QML para alternar el tema.
import QtQuick
import QtQuick.Controls

Item {
    width: 200
    height: 60

    Row {
        spacing: 8
        anchors.centerIn: parent

        Label {
            text: "Tema:"
            anchors.verticalCenter: parent.verticalCenter
        }

        Switch {
            id: themeSwitch
            text: themeSwitch.checked ? "Oscuro" : "Claro"
        }
    }
}
