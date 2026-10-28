#!/usr/bin/env python3
"""Synchronize a GNOME user's Do Not Disturb state with Home Assistant."""

from __future__ import annotations

import json
import logging
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import quote


LOGGER = logging.getLogger("ha_gnome_dnd")
API_TIMEOUT_SECONDS = 10
POLL_SECONDS = 3
SCHEMA = "org.gnome.desktop.notifications"
KEY = "show-banners"
POLICY_FOLLOW_GLOBAL = "Follow global"
POLICY_FORCE_ON = "Force on"
POLICY_FORCE_OFF = "Force off"


def api_request(config, method, path, payload=None):
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        config["ha_url"].rstrip("/") + path,
        data=body,
        method=method,
        headers={
            "Authorization": "Bearer " + config["token"],
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(request, timeout=API_TIMEOUT_SECONDS) as response:
        content = response.read()
        return json.loads(content) if content else None


def read_entity(config, entity_id):
    result = api_request(config, "GET", "/api/states/" + quote(entity_id, safe="."))
    return result.get("state", "unknown")


def read_gnome_dnd():
    result = subprocess.run(
        ["gsettings", "get", SCHEMA, KEY],
        check=True,
        capture_output=True,
        text=True,
        timeout=5,
    )
    value = result.stdout.strip()
    if value not in ("true", "false"):
        raise RuntimeError("GNOME returned an unexpected show-banners value")
    return value == "false"


def set_gnome_dnd(enabled):
    # GNOME's DND switch is the inverse of show-banners; always set, never toggle.
    show_banners = "false" if enabled else "true"
    subprocess.run(
        ["gsettings", "set", SCHEMA, KEY, show_banners],
        check=True,
        capture_output=True,
        text=True,
        timeout=5,
    )
    actual = read_gnome_dnd()
    if actual != enabled:
        raise RuntimeError("GNOME did not confirm the requested DND state")
    return actual


def set_status(config, enabled):
    entity_id = config["status_entity"]
    service = "turn_on" if enabled else "turn_off"
    api_request(
        config,
        "POST",
        "/api/services/input_boolean/" + service,
        {"entity_id": entity_id},
    )


def read_desired_state(config):
    source_states = [read_entity(config, entity) for entity in config["desired_entities"]]
    if any(state not in ("on", "off") for state in source_states):
        raise RuntimeError("A global Home Assistant DND source is unavailable")

    policy_entity = config.get("policy_entity")
    if not policy_entity:
        return any(state == "on" for state in source_states), tuple(source_states)

    policy = read_entity(config, policy_entity)
    if policy == POLICY_FORCE_ON:
        desired = True
    elif policy == POLICY_FORCE_OFF:
        desired = False
    elif policy == POLICY_FOLLOW_GLOBAL:
        desired = any(state == "on" for state in source_states)
    else:
        raise RuntimeError("The per-account GNOME DND policy is unavailable or invalid")

    return desired, tuple(source_states) + (policy,)


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: ha-gnome-dnd-agent.py CONFIG.json")
    config = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    last_sources = None

    while True:
        try:
            desired, sources = read_desired_state(config)
            actual = read_gnome_dnd()

            # Apply HA's state at startup and whenever a source or account policy changes.
            if last_sources is None or sources != last_sources:
                if actual != desired:
                    actual = set_gnome_dnd(desired)
                    LOGGER.info("Applied HA DND state: %s", "on" if desired else "off")

            # Manual GNOME changes are observed and reported without toggling them.
            actual = read_gnome_dnd()
            reported = read_entity(config, config["status_entity"])
            if reported not in ("on", "off") or (reported == "on") != actual:
                set_status(config, actual)

            last_sources = sources
        except (
            OSError,
            RuntimeError,
            ValueError,
            urllib.error.URLError,
            urllib.error.HTTPError,
            subprocess.SubprocessError,
            KeyError,
        ) as error:
            LOGGER.warning("DND synchronization is waiting: %s", error)
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
