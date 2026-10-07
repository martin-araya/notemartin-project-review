// F06z: PreferencesPage.qml - pagina QML que consume Q_PROPERTY de
// PreferencesProxy (E04: bindings declarativos + Q_INVOKABLE).
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: page
    width: 400
    height: 300
    title: "Preferencias"
    visible: true

    // E04: binding declarativo a Q_PROPERTY. Cuando fontSize cambia
    // en el C++, el SpinBox se actualiza automaticamente.
    ColumnLayout {
        anchors.margins: 16
        anchors.fill: parent
        spacing: 12

        Label { text: "Tamano de fuente:" }
        SpinBox {
            from: 6
            to: 96
            value: proxy.fontSize
            // E04: dos-way binding. El usuario cambia el SpinBox,
            // emite valueChanged, que llama setFontSize en C++.
            onValueModified: proxy.fontSize = value
        }

        CheckBox {
            text: "Tema oscuro"
            checked: proxy.darkTheme
            onCheckedChanged: proxy.darkTheme = checked
        }

        // E04: Q_INVOKABLE invocado desde QML.
        Button {
            text: "Reset to defaults"
            onClicked: proxy.resetToDefaults()
        }

        Label {
            text: proxy.title
            font.pixelSize: 14
        }
    }
}
