# Home Assistant configuration

This repository contains the reviewed YAML configuration and custom helper scripts for the Home Assistant instance.

## Security

Runtime state, `.storage`, backups, databases, logs, and `secrets.yaml` are intentionally excluded. Keep credentials in Home Assistant's local `secrets.yaml` and never commit them.

## Tracked configuration

- `configuration.yaml` loads the automation, template, script, and scene files.
- `automations.yaml`, `scripts.yaml`, `templates.yaml`, and `scenes.yaml` contain the instance configuration.
- `scripts/` contains local integration helpers used by `shell_command`.
- `dashboards/` contains reviewed Lovelace card fragments applied to storage-mode dashboards; Home Assistant does not load these fragments automatically.
