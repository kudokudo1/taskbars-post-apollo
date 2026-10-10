import QtQuick
import Quickshell
import "../components"
import QtQuick.Effects
import Qt5Compat.GraphicalEffects

Item {
    id: clockArea

    width: clockButton.width + 20
    height: clockButton.height + 46

    property bool is24Hour: false

    DockButton {
        id: clockButton

        implicitHeight: 50
        implicitWidth: 151

        contentGlowEnabled: false

        normalDockGlowColor:
            clockArea.is24Hour ? Colors.orange : Colors.cyan
        hoverDockGlowColor: normalDockGlowColor
        pressedDockGlowColor: normalDockGlowColor

        softGlowIdleOpacity: 0.40
        softGlowHoverOpacity: 0.50
        softGlowPressedOpacity: 0.60

        wideGlowIdleOpacity: 0.07
        wideGlowHoverOpacity: 0.09
        wideGlowPressedOpacity: 0.12

        SystemClock {
            id: clock
            precision: SystemClock.Seconds
        }

        // The clock keeps a cyan primary identity in 12-hour mode and shifts
        // that primary identity to orange in alternate 24-hour mode. White
        // punctuation/ornament separates the stars, colon, and AM/PM suffix.
        // Each source-attached glow stays inside the same fixed slot as its
        // visible source so the Row only owns semantic units, never effects.
        Row {
            id: clockRow

            anchors.centerIn: parent
            spacing: 7

            Row {
                id: clockIconContainer

                height: 20
                spacing: 1

                Item {
                    id: clockLeftStarContainer

                    width: clockLeftStar.implicitWidth
                    height: 20

                    GohuText {
                        id: clockLeftStar
                        anchors.centerIn: parent

                        text: " ๋࣭"
                        color: Colors.white
                        font.pixelSize: 20
                    }

                    SafeDropShadow {
                        anchors.fill: clockLeftStar
                        safeSource: clockLeftStar

                        horizontalOffset: 0
                        verticalOffset: 0
                        radius: 10
                        samples: 9
                        z: 2

                        opacity:
                            clockButton.pressed
                            ? 1.0
                            : clockButton.hovered
                            ? 0.76
                            : 0.52

                        color:
                            clockArea.is24Hour
                            ? Colors.orange
                            : Colors.white
                        transparentBorder: true
                    }
                }

                Item {
                    id: clockIconCoreContainer

                    width: clockIcon.implicitWidth
                    height: 20

                    Text {
                        id: clockIcon
                        anchors.centerIn: parent

                        text: "🕰"
                        color:
                            clockArea.is24Hour
                            ? Colors.orange
                            : Colors.cyan
                        font.pixelSize: 20
                    }

                    SafeDropShadow {
                        anchors.fill: clockIcon
                        safeSource: clockIcon

                        horizontalOffset: 0
                        verticalOffset: 0
                        radius: 14
                        samples: 15
                        z: 2

                        opacity:
                            clockButton.pressed
                            ? 1.0
                            : clockButton.hovered
                            ? 0.8
                            : 0.6

                        color:
                            clockArea.is24Hour
                            ? Colors.orange
                            : Colors.cyan
                        transparentBorder: true
                    }
                }

                Item {
                    id: clockRightStarContainer

                    width: clockRightStar.implicitWidth
                    height: 20

                    GohuText {
                        id: clockRightStar
                        anchors.centerIn: parent

                        text: "⭑"
                        color: Colors.white
                        font.pixelSize: 20
                    }

                    SafeDropShadow {
                        anchors.fill: clockRightStar
                        safeSource: clockRightStar

                        horizontalOffset: 0
                        verticalOffset: 0
                        radius: 10
                        samples: 9
                        z: 2

                        opacity:
                            clockButton.pressed
                            ? 1.0
                            : clockButton.hovered
                            ? 0.76
                            : 0.52

                        color: Colors.white
                        transparentBorder: true
                    }
                }
            }

            Row {
                id: clockReadout

                height: 20
                spacing: 1

                Item {
                    id: clockHourContainer

                    width: clockHour.implicitWidth
                    height: 20

                    GohuText {
                        id: clockHour
                        anchors.centerIn: parent

                        text:
                            clockArea.is24Hour
                            ? Qt.formatDateTime(clock.date, "HH")
                            : Qt.formatDateTime(clock.date, "hh")

                        color:
                            clockArea.is24Hour
                            ? Colors.orange
                            : Colors.cyan
                        font.pixelSize: 20
                    }

                    SafeDropShadow {
                        anchors.fill: clockHour
                        safeSource: clockHour

                        horizontalOffset: 0
                        verticalOffset: 0
                        radius: 14
                        samples: 15
                        z: 2

                        opacity:
                            clockButton.pressed
                            ? 1.0
                            : clockButton.hovered
                            ? 0.8
                            : 0.6

                        color:
                            clockArea.is24Hour
                            ? Colors.orange
                            : Colors.cyan
                        transparentBorder: true
                    }
                }

                Item {
                    id: clockColonContainer

                    width: clockColon.implicitWidth
                    height: 20

                    GohuText {
                        id: clockColon
                        anchors.centerIn: parent

                        text: ":"
                        color: Colors.white
                        font.pixelSize: 20
                    }

                    SafeDropShadow {
                        anchors.fill: clockColon
                        safeSource: clockColon

                        horizontalOffset: 0
                        verticalOffset: 0
                        radius: 14
                        samples: 15
                        z: 2

                        opacity:
                            clockButton.pressed
                            ? 1.0
                            : clockButton.hovered
                            ? 0.8
                            : 0.6

                        color: Colors.white
                        transparentBorder: true
                    }
                }

                Item {
                    id: clockMinuteContainer

                    width: clockMinute.implicitWidth
                    height: 20

                    GohuText {
                        id: clockMinute
                        anchors.centerIn: parent

                        text: Qt.formatDateTime(clock.date, "mm")
                        color:
                            clockArea.is24Hour
                            ? Colors.orange
                            : Colors.cyan
                        font.pixelSize: 20
                    }

                    SafeDropShadow {
                        anchors.fill: clockMinute
                        safeSource: clockMinute

                        horizontalOffset: 0
                        verticalOffset: 0
                        radius: 14
                        samples: 15
                        z: 2

                        opacity:
                            clockButton.pressed
                            ? 1.0
                            : clockButton.hovered
                            ? 0.8
                            : 0.6

                        color:
                            clockArea.is24Hour
                            ? Colors.orange
                            : Colors.cyan
                        transparentBorder: true
                    }
                }

                Item {
                    id: clockPeriodContainer

                    width: clockPeriod.implicitWidth
                    height: 20

                    GohuText {
                        id: clockPeriod
                        anchors.centerIn: parent

                        text:
                            clockArea.is24Hour
                            ? "24H"
                            : Qt.formatDateTime(clock.date, "AP")

                        color:
                            clockArea.is24Hour
                            ? Colors.orange
                            : Colors.white
                        font.pixelSize: 11
                    }

                    SafeDropShadow {
                        anchors.fill: clockPeriod
                        safeSource: clockPeriod

                        horizontalOffset: 0
                        verticalOffset: 0
                        radius: 8
                        samples: 9
                        z: 2

                        opacity:
                            clockButton.pressed
                            ? 1.0
                            : clockButton.hovered
                            ? 0.75
                            : 0.52

                        color: Colors.white
                        transparentBorder: true
                    }
                }
            }
        }

        onRightClicked: {
            clockArea.is24Hour = !clockArea.is24Hour;
        }

        onClicked: {
            console.log("clockButton clicked");
        }
    }
}
