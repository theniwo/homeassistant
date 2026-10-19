#!/usr/bin/env python3
"""Set Snom DND without inverting a manually selected state."""

import argparse
import json
import re
import sys
import time
from pathlib import Path

import requests
import yaml

SETTINGS_PATH = "/settings.htm"
COMMAND_PATH = "/command.htm?key=DND"
DND_STATE_PATTERN = re.compile(r"dnd_mode\d+!: (on|off)")
REQUEST_TIMEOUT_SECONDS = 5
VERIFY_ATTEMPTS = 10
VERIFY_DELAY_SECONDS = 0.5


def read_dnd_states(session, base_url):
    response = session.get(base_url + SETTINGS_PATH, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    states = DND_STATE_PATTERN.findall(response.text)
    if not states:
        raise RuntimeError("The Snom settings page did not expose any DND state.")
    return states


def main():
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--desired", choices=("on", "off"))
    action.add_argument("--status", action="store_true")
    args = parser.parse_args()

    secrets = yaml.safe_load(Path("/config/secrets.yaml").read_text()) or {}
    host = secrets.get("snom_host", "").strip()
    if not host:
        raise RuntimeError("Missing snom_host in secrets.yaml.")
    base_url = "http://" + host.rstrip("/")
    session = requests.Session()

    if args.status:
        states = read_dnd_states(session, base_url)
        if len(set(states)) != 1:
            raise RuntimeError("DND states differ between identities; status is ambiguous.")
        print(json.dumps({"state": states[0]}))
        return 0

    # Preserve the known Snom request sequence, then read actual per-identity state.
    response = session.get(
        base_url + SETTINGS_PATH,
        params={"dnd_mode": args.desired},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    states = read_dnd_states(session, base_url)
    if all(state == args.desired for state in states):
        print(json.dumps({"changed": False, "state": args.desired}))
        return 0
    if len(set(states)) != 1:
        raise RuntimeError("DND states differ between identities; refusing to toggle them.")

    response = session.get(base_url + COMMAND_PATH, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    for _ in range(VERIFY_ATTEMPTS):
        time.sleep(VERIFY_DELAY_SECONDS)
        states = read_dnd_states(session, base_url)
        if all(state == args.desired for state in states):
            print(json.dumps({"changed": True, "state": args.desired}))
            return 0
        if len(set(states)) != 1:
            raise RuntimeError("DND states diverged after pressing the DND key.")

    raise RuntimeError("Snom DND state did not reach the requested value.")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
