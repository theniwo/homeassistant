# TODO

- [ ] Wake lights should turn on dimmed.
- [ ] Wake lights should turn off when the alarm is stopped.
- [ ] Add a master switch for all automations, excluding lighting control.
- [ ] Smartphone position should also toggle the automation master. Define the exact position trigger when implementing this item.
- [ ] Keep the mailbox reminder announcement after shift start for both early and late shifts.
- [ ] Add a master toggle for automatic voicemail forwarding.
- [ ] Clarify whether `Zum Wecker` should use Alexa's actual next-alarm sensor instead of the calculated shift alarm, accounting for delayed sensor updates.
- [ ] Add a configurable break timer and its Home Assistant helper.
- [x] Verify that each radiator reaches the configured open-window off setpoint (`input_number.window_open_temp`); retry checks using configurable helpers (3 attempts, 15-second interval) and send an alert if it still fails. Keep the retry helpers off the dashboard.
