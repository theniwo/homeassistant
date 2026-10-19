#!/usr/bin/env python3
"""Control only the enabled state of the two named FRITZ!Box answering machines."""

import argparse
import json
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

import requests
import yaml

SERVICE_TYPE = "urn:dslforum-org:service:X_AVM-DE_TAM:1"
CONTROL_PATH = "/upnp/control/x_tam"
SOAP_ENVELOPE = "http://schemas.xmlsoap.org/soap/envelope/"
TAM_NAMES = ("Anrufbeantworter Private", "Anrufbeantworter Public")
REQUEST_TIMEOUT_SECONDS = 10


def local_name(element):
    return element.tag.rsplit("}", 1)[-1]


def find_text(root, expected_name):
    for element in root.iter():
        if local_name(element) == expected_name:
            return element.text or ""
    raise RuntimeError(f"FRITZ!Box response lacks {expected_name}.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--enabled", choices=("on", "off", "status"), required=True)
    args = parser.parse_args()

    secrets = yaml.safe_load(Path("/config/secrets.yaml").read_text()) or {}
    host = secrets.get("fritzbox_host", "").strip()
    username = secrets.get("fritzbox_username", "").strip()
    password = secrets.get("fritzbox_password", "")
    if not host or not username or not password:
        raise RuntimeError("FRITZ!Box host or credentials are missing from secrets.yaml.")

    control_url = f"http://{host}:49000{CONTROL_PATH}"
    session = requests.Session()
    session.auth = requests.auth.HTTPDigestAuth(username, password)

    def call(action, arguments=""):
        body = (
            f'<?xml version="1.0"?><s:Envelope xmlns:s="{SOAP_ENVELOPE}" '
            's:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'
            f'<s:Body><u:{action} xmlns:u="{SERVICE_TYPE}">{arguments}'
            f'</u:{action}></s:Body></s:Envelope>'
        )
        response = session.post(
            control_url,
            data=body.encode(),
            headers={
                "Content-Type": 'text/xml; charset="utf-8"',
                "SOAPAction": f'"{SERVICE_TYPE}#{action}"',
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return ET.fromstring(response.content)

    tam_list_response = call("GetList")
    tam_list = ET.fromstring(find_text(tam_list_response, "NewTAMList"))
    indices = {}
    for item in tam_list.iter():
        if local_name(item) != "Item":
            continue
        fields = {local_name(node): node.text or "" for node in item}
        if fields.get("Name") in TAM_NAMES:
            indices[fields["Name"]] = fields["Index"]
    missing = [name for name in TAM_NAMES if name not in indices]
    if missing:
        raise RuntimeError("Could not locate both named answering machines.")

    def get_info(name):
        response = call("GetInfo", f'<NewIndex>{indices[name]}</NewIndex>')
        return {
            "enabled": find_text(response, "NewEnable") == "1",
            "mode": find_text(response, "NewMode"),
        }

    states = {name: get_info(name) for name in TAM_NAMES}
    if args.enabled == "status":
        print(json.dumps({"answering_machines": states}, ensure_ascii=False))
        return 0

    desired = args.enabled == "on"
    changed = False
    for name in TAM_NAMES:
        if states[name]["enabled"] != desired:
            call("SetEnable", f'<NewIndex>{indices[name]}</NewIndex><NewEnable>{1 if desired else 0}</NewEnable>')
            changed = True

    verified = {name: get_info(name) for name in TAM_NAMES}
    if not all(state["enabled"] == desired for state in verified.values()):
        raise RuntimeError("FRITZ!Box did not confirm the requested answering machine state.")
    print(json.dumps({"changed": changed, "enabled": desired, "answering_machines": verified}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
