#!/usr/bin/env python3
"""CPU++ main-mode caption keeps its sampled effect within one layout slot."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
qml = (ROOT / "widgets/CpuPlusW.qml").read_text(encoding="utf-8")
mode = qml[qml.index("id: modeButton"):qml.index("// TWO-BODY MONITOR ADAPTER")]


def block_at_open_brace(text, open_brace):
    """Extract a brace-balanced QML block, including nested child objects."""
    assert text[open_brace] == "{"
    depth = 0
    for idx in range(open_brace, len(text)):
        if text[idx] == "{":
            depth += 1
        elif text[idx] == "}":
            depth -= 1
            if depth == 0:
                return text[open_brace:idx + 1], idx + 1
    raise AssertionError("Unbalanced QML block")


column_idx = mode.index("Column {")
column_open = mode.index("{", column_idx)
column, column_end = block_at_open_brace(mode, column_open)

slot_id = column.index("id: modeCaptionSlot")
slot_item_idx = column.rfind("Item {", 0, slot_id)
assert slot_item_idx >= 0
slot_open = column.index("{", slot_item_idx)
slot, slot_end = block_at_open_brace(column, slot_open)

# The Column must position the slot, not lay out the caption effect.
assert column[:slot_open].count("{") - column[:slot_open].count("}") == 1
assert "width: modeCaption.implicitWidth" in slot
assert "height: modeCaption.implicitHeight" in slot
assert "anchors.horizontalCenter: parent.horizontalCenter" in slot
assert slot.count("QuietText {") == 1
assert slot.count("TextHashGlow {") == 1
assert "id: modeCaption" in slot
assert "anchors.centerIn: parent" in slot
assert "safeSource: modeCaption" in slot
assert "foregroundColor: modeCaption.color" in slot
assert "preferredGlowColor: Colors.white" in slot
assert "requestedVisible: !modeButton.isPressed" in slot
assert "radius: 5" in slot
assert "samples: 7" in slot
assert "? 0.10 : 0.06" in slot

# One effect for the icon, one for the caption. The caption effect cannot
# also remain as a direct Column child after the semantic slot.
assert column.count("TextHashGlow {") == 2
assert "safeSource: modeCaption" not in column[:slot_open] + column[slot_end:]
assert "safeSource: textModeIcon" in column

# Both icons and captions are individually laid out semantic slots, not
# external source effects treated as independent children by the Column.
icon_id = column.index("id: modeIconSlot")
icon_item = column.rfind("Item {", 0, icon_id)
icon_open = column.index("{", icon_item)
icon, icon_end = block_at_open_brace(column, icon_open)
assert column[:icon_open].count("{") - column[:icon_open].count("}") == 1
assert "GohuText {" in icon
assert "id: textModeIcon" in icon
assert "safeSource: textModeIcon" in icon
assert icon.count("TextHashGlow {") == 1
assert "clip: false" in icon
assert "clip: false" in slot
assert "clip: false" in column
assert column.count("TextHashGlow {") == (
    icon.count("TextHashGlow {") + slot.count("TextHashGlow {")
)

assert "duration: 90" in mode
assert "Easing.OutQuad" in mode
assert "cpuPlusWindow.selectMode(index)" in mode
assert mode.count("ModeButtonCloseHalo {") == 1
assert mode.count("ModeButtonWideHalo {") == 1

# The thermal composition must have ONE owner shared with AppControl.
# Previously CpuPlusW held an almost exact copy of ThermalIcon.qml, which
# makes repairs diverge and lets different icon/glow contracts accumulate.
assert 'import "thermal"' in qml
assert qml.count("id: thermalIconComponent") == 1
component = qml[
    qml.index("id: thermalIconComponent"):
    qml.index("// WINDOW", qml.index("id: thermalIconComponent"))
]
assert component.count("ThermalIcon { }") == 1
assert "id: thermalIconRoot" not in qml
assert "item.glowColor" not in qml
assert qml.count("item.iconColor = Qt.binding") == 4
assert qml.count("item.glowOpacity =") == 4
assert qml.count("item.pressed = Qt.binding") == 3
shared = (ROOT / "widgets/thermal/ThermalIcon.qml").read_text(encoding="utf-8")
assert "property color iconColor:" in shared
assert "property real glowOpacity:" in shared
assert "property bool pressed:" in shared

print("CPU++ caption-slot construction contracts: PASS")
