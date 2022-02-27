import QtQuick 2.15
import QtQuick.Window 2.15
import QtGraphicalEffects 1.0

Window {
    visible : true
    color: "transparent"
    flags: Qt.X11BypassWindowManagerHint | Qt.NoDropShadowWindowHint
    x: 0
    y: Screen.height - 50
    width: Screen.width
    height: 50
    Rectangle {
        objectName: "background"
        anchors.centerIn: parent
        width: 500
        height: 40
        color: "#d8dee9"
        radius: 5
        layer.enabled: true
        layer.effect: DropShadow {
            transparentBorder: true
            horizontalOffset: 1
            verticalOffset: 1
            color: "#99000000"
        }

        ListView {
            height: parent.height
            width: parent.width
            model: icons_model
            orientation: ListView.Horizontal

            delegate: Component {
                Image {
                    anchors.verticalCenter: parent
                    sourceSize.height: 22
                    source: model.icon
                }
            }
        }
    }
}