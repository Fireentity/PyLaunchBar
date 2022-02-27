import QtQuick 2.15

Image {
    id: "icon"
    sourceSize.height: 22

    MouseArea {
        anchors.fill: parent
        onClicked: {
            controller.on_click(this)
        }
    }
}
