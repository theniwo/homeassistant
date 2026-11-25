# Changelog

## 2026-11-25

- ✨ Added a Samsung S25 warning when a spoken Alexa alarm-setting command specifies a time inside the configured Echo quiet hours; it checks both transcript fields and names the Echo that heard it.
- 🐛 Kept Echo announcements at Night Volume until the alarm or no-alarm fallback, in addition to the fixed quiet interval.
- ✨ Grouped the editable quiet-hours start and end in the Home dashboard’s Echo & Light card.

## 2026-11-24

- 🐛 Echo announcements and volume scheduling now respect a configurable night window from 22:00 to 07:00 by default; the night level cannot be raised during it.

## 2026-11-21

- 🐛 The tomorrow overview now retains the scheduled shift label while marking Sick mode as suppressing the alarm.
- 🐛 Suppressed shift-start and morning pill announcements when Samsung Work Mode is already active.
- 🐛 Work-Mode-only DND now stays on the Snom; Samsung follows scheduled or global DND and Sleep Mode without inheriting the Work Mode request.

## 2026-11-20

- ✨ Added a configurable 0–10 minute lead for the Work SIM voicemail-off prompt before early and late shifts; the default is three minutes and the helper is available in the Home dashboard.

## 2026-11-11

- 🐛 Fixed shift status summaries so Sick mode overrides overlapping shift titles, and added a dedicated **Heute prüfen** dashboard action that refreshes today's read-only calendar summary.

## 2026-11-10

- 🐛 Fixed the hallway “All Off” action to target current Shelly relay entities directly, including both kitchen channels (ceiling light and extractor hood) and both living-room outputs.
- 🐛 Fixed both hallway master-light buttons: “All On” now includes every available light entity and current Shelly lighting relay, while “All Off” uses the same targets. Replaced stale device IDs, corrected the WLED preset entity, and allowed a new button press to supersede the delayed preset action.
