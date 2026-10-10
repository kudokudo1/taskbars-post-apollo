#!/usr/bin/env python3
"""Guard the first bounded non-CPU sampled-glow normalization slice."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]

# Guard actual sampled items; preserve existing per-widget colors, sizing,
# and interaction state rather than forcing generic glow tokens everywhere.
SURFACES = {
    "modules/Clock.qml": ("clockIcon", "clockText"),
    "modules/Volumebar.qml": ("volumebarIcon", "volumebarText"),
    "modules/Workspaces.qml": ("workspacesButtonBackground", "workspacesText"),
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
    for source in sources:
        assert f"safeSource: {source}" in qml, (relative, source)

workspaces = (ROOT / "modules/Workspaces.qml").read_text(encoding="utf-8")
assert workspaces.count("id: workspacesTextGlow") == 1
assert "id: workspacesActiveTextGlow" not in workspaces
assert "color: workspacesWorkspaceButton.isActive" in workspaces
assert "? workspacesText.workspaceColor : Colors.cyan" in workspaces
assert "workspacesButtonMouse.pressed ? 1.0" in workspaces
assert "workspacesButtonMouse.containsMouse ? 0.8" in workspaces
assert "workspacesWorkspaceButton.isActive ? 0.7 : 0.6" in workspaces

print("Non-CPU sampled-glow structural contracts: PASS")
