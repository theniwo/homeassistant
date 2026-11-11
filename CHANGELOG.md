# Changelog

## 2026-11-11

- 🐛 Fixed shift status summaries so Sick mode overrides overlapping shift titles, and added a dedicated **Heute prüfen** dashboard action that refreshes today's read-only calendar summary.

## 2026-11-10

- 🐛 Fixed the hallway “All Off” action to target current Shelly relay entities directly, including both kitchen channels (ceiling light and extractor hood) and both living-room outputs.
- 🐛 Fixed both hallway master-light buttons: “All On” now includes every available light entity and current Shelly lighting relay, while “All Off” uses the same targets. Replaced stale device IDs, corrected the WLED preset entity, and allowed a new button press to supersede the delayed preset action.
