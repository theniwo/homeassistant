#!/usr/bin/env python3
"""Update this user's GNOME DND agent and bind its per-account policy helper."""

from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import sys
from datetime import datetime
from pathlib import Path


GLOBAL_DND_SOURCES = [
    "input_boolean.sleep_mode_state",
    "input_boolean.dnd_override",
    "input_boolean.snom_dnd_state",
]
STATUS_PREFIX = "input_boolean.gnome_dnd_"
STATUS_SUFFIX = "_actual"
AGENT_SOURCE_NAME = "ha_gnome_dnd_agent.py"
SERVICE_NAME = "ha-gnome-dnd.service"


def main():
    repository_root = Path(__file__).resolve().parent.parent
    source_path = repository_root / "scripts" / AGENT_SOURCE_NAME
    config_root = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    config_path = config_root / "ha-gnome-dnd" / "config.json"
    agent_path = Path.home() / ".local" / "lib" / "ha-gnome-dnd" / "agent.py"

    if not config_path.is_file():
        raise SystemExit(f"Agent configuration was not found: {config_path}")
    if not source_path.is_file():
        raise SystemExit(f"Agent source was not found: {source_path}")

    config = json.loads(config_path.read_text(encoding="utf-8"))
    status_entity = config.get("status_entity", "")
    if not status_entity.startswith(STATUS_PREFIX) or not status_entity.endswith(STATUS_SUFFIX):
        raise SystemExit("The configured status_entity does not identify a GNOME account")
    account = status_entity[len(STATUS_PREFIX) : -len(STATUS_SUFFIX)]
    config["desired_entities"] = GLOBAL_DND_SOURCES
    config["policy_entity"] = f"input_select.gnome_dnd_{account}_policy"

    backup_root = config_root / "codex" / "backups"
    backup_root.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    config_backup = backup_root / f"ha-gnome-dnd-config-{timestamp}.json"
    agent_backup = backup_root / f"ha-gnome-dnd-agent-{timestamp}.py"
    shutil.copy2(config_path, config_backup)
    if agent_path.exists():
        shutil.copy2(agent_path, agent_backup)

    agent_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, agent_path)
    agent_path.chmod(agent_path.stat().st_mode | stat.S_IXUSR)

    temporary_path = config_path.with_suffix(".json.tmp")
    temporary_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    temporary_path.chmod(config_path.stat().st_mode & 0o777)
    temporary_path.replace(config_path)

    subprocess.run(["systemctl", "--user", "restart", SERVICE_NAME], check=True)
    print(f"Updated the GNOME DND agent for account policy {config['policy_entity']}.")
    print(f"Backups saved under {backup_root}.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Update failed: {error}", file=sys.stderr)
        raise SystemExit(1)
