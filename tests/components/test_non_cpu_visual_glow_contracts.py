#!/usr/bin/env python3
"""Guard the bounded non-CPU sampled-glow normalization slice."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]

# Guard actual sampled items while preserving intentional per-widget layering.
# Duplicate entries are deliberate when more than one semantic effect samples
# the same visible source.
SURFACES = {
    "modules/Clock.qml": (
        "clockLeftStar",
        "clockIcon",
        "clockRightStar",
        "clockHour",
        "clockColon",
        "clockMinute",
        "clockPeriod",
    ),
    "modules/Volumebar.qml": (
        "volumebarIcon",
        "volumebarText",
    ),
    "modules/Workspaces.qml": (
        "workspacesButtonBackground",
        "workspacesText",
        "workspacesText",
    ),
}

for relative, sources in SURFACES.items():
    qml = (ROOT / relative).read_text(encoding="utf-8")
    direct = re.findall(r"(?m)^\s*DropShadow\s*\{", qml)
    safe = re.findall(r"(?m)^\s*SafeDropShadow\s*\{", qml)

    assert not direct, f"{relative}: unguarded source-attached DropShadow"
    assert len(safe) == len(sources), (
        f"{relative}: expected {len(sources)} guarded sampled glows, "
        f"found {len(safe)}"
    )

    for source in set(sources):
        expected = sources.count(source)
        actual = qml.count(f"safeSource: {source}")
        assert actual == expected, (
            f"{relative}: expected {expected} safeSource attachment(s) "
            f"for {source}, found {actual}"
        )

workspaces = (ROOT / "modules/Workspaces.qml").read_text(encoding="utf-8")
assert workspaces.count("id: workspacesTextGlow") == 1
assert workspaces.count("id: workspacesActiveTextGlow") == 1
assert "visible: workspacesWorkspaceButton.isActive" in workspaces
assert "color: Colors.cyan" in workspaces
assert "color: workspacesText.workspaceColor" in workspaces
assert "workspacesButtonMouse.pressed ? 1.0" in workspaces
assert "workspacesButtonMouse.containsMouse ? 0.8" in workspaces

clock = (ROOT / "modules/Clock.qml").read_text(encoding="utf-8")
for source in (
    "clockLeftStar",
    "clockIcon",
    "clockRightStar",
    "clockHour",
    "clockColon",
    "clockMinute",
    "clockPeriod",
):
    assert f"id: {source}" in clock
    assert f"safeSource: {source}" in clock

# The operator-approved direction keeps cyan as the clock's primary identity
# while white carries ornament and punctuation.
assert "clockArea.is24Hour ? Colors.orange : Colors.cyan" in clock
assert "clockArea.is24Hour\n                            ? Colors.orange\n                            : Colors.cyan" in clock
assert "clockArea.is24Hour\n                            ? Colors.orange\n                            : Colors.white" in clock
assert clock.count("color: Colors.white") >= 3
assert "color: Colors.magenta" not in clock
assert "color: Colors.yellow" not in clock

print("Non-CPU sampled-glow structural contracts: PASS")
