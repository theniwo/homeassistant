# Home Assistant helper names

GUI helper names use concise English labels. `WHZ`, `AZ`, and `SZ` mean living room, office, and bedroom. `Offset` means a relative duration; Home Assistant shows the helper's unit beside its value. Clock values use `time`.

## State and mode

| Entity ID | GUI name | Purpose |
| --- | --- | --- |
| `input_boolean.tradfri_stop_event` | Tradfri stop event | Internal Tradfri event flag |
| `input_boolean.tradfri_stop_temp` | Tradfri stop temp | Internal Tradfri temporary flag |
| `input_boolean.work_mode_state` | Work mode state | Internal work mode state |
| `input_boolean.sleep_mode_state` | Sleep mode state | Sleep mode state |
| `input_boolean.snom_dnd_state` | Snom DND state | Scheduled Snom DND state |
| `input_boolean.fritz_ab_state` | FRITZ AB state | Scheduled Fritz!Box answering machine state |
| `input_boolean.dnd_override` | DND override | Manual global DND override |
| `input_boolean.gnome_dnd_niwo` | GNOME DND niwo | GNOME DND state for the niwo account |
| `input_boolean.gnome_dnd_work` | GNOME DND work | GNOME DND state for the work account |
| `input_boolean.snom_dnd_status` | Snom DND status | Read-back state from the Snom phone |
| `input_boolean.enforce_sleep` | Enforce sleep | Apply the room shutdown when Sleep Mode starts |
| `input_select.work_schedule_mode` | Work schedule mode | Automatic, free shift, or sick mode |
| `input_select.enforce_sleep_reset_mode` | Enforce sleep reset | Reset policy for Enforce sleep |
| `input_select.whz_sleep_profile` | WHZ sleep profile | Living room profile while Sleep Mode is active |

## Heating

| Entity ID | GUI name | Purpose / unit |
| --- | --- | --- |
| `input_number.whz_target_temp` | WHZ target temp | Living room comfort target, °C |
| `input_number.az_target_temp` | AZ target temp | Office comfort target, °C |
| `input_number.sz_target_temp` | SZ target temp | Bedroom comfort target, °C |
| `input_number.heating_min_temp` | Heating min temp | Base target with windows closed, °C |
| `input_number.window_open_temp` | Window open temp | Target while a window is open, °C |
| `input_number.heating_preheat_offset` | Heating preheat offset | Preheat duration before an event, hours |
| `input_number.heating_cooldown_offset` | Heating cooldown offset | Early shutoff duration before shift end, hours |
| `input_number.sick_temp_offset` | Sick temp offset | Additional heating in sick mode, °C |

## Schedule, reminders, and DND

| Entity ID | GUI name | Purpose / unit |
| --- | --- | --- |
| `input_datetime.early_shift_start` | Early shift start | Early shift start time |
| `input_datetime.early_shift_end` | Early shift end | Early shift end time |
| `input_datetime.late_shift_start` | Late shift start | Late shift start time |
| `input_datetime.late_shift_end` | Late shift end | Late shift end time |
| `input_datetime.free_shift_start` | Free shift start | Start time for free-shift profile |
| `input_datetime.vacation_wake_time` | Vacation wake time | Wake time for the vacation profile |
| `input_number.alarm_offset` | Alarm offset | Hours before shift start |
| `input_datetime.alarm_setup_time` | Alarm check time | Daily time for the next-day calendar check |
| `input_number.sleep_duration` | Sleep duration | Sleep duration, hours |
| `input_number.wind_down_offset` | Wind-down offset | Hours before sleep time |
| `input_number.dnd_offset` | DND offset | Hours before alarm time |
| `input_number.pill_morning_offset` | Pill morning offset | Morning reminder offset, hours |
| `input_number.pill_bedtime_offset` | Pill bedtime offset | Bedtime reminder offset, hours |
| `input_number.sick_pill_offset` | Sick pill offset | Sick-mode reminder offset, hours |

## Phone and Echo

| Entity ID | GUI name | Purpose / unit |
| --- | --- | --- |
| `input_datetime.phone_handover_time` | Phone handover time | Phone handover clock time |
| `input_number.phone_handover_offset` | Phone handover offset | Announcement delay, minutes |
| `input_number.bt_disconnect_offset` | BT disconnect offset | Disconnect before alarm, seconds |
| `input_number.echo_announcement_volume` | Echo announcement volume | Announcement volume on a 0–10 scale |
| `input_number.echo_day_volume` | Echo day volume | Daytime volume on a 0–10 scale |
| `input_number.echo_night_volume` | Echo night volume | Nighttime volume on a 0–10 scale |
| `input_datetime.echo_quiet_time` | Echo quiet time | Start of quiet hours |
| `input_datetime.echo_fallback_time` | Echo fallback time | Fallback time to restore volume |
| `input_text.samsung_work_mode_id` | Samsung Work mode ID | Samsung routine identifier |
| `input_text.samsung_sleep_mode_id` | Samsung Sleep mode ID | Samsung routine identifier |

## Lighting and status

| Entity ID | GUI name | Purpose / unit |
| --- | --- | --- |
| `input_number.motion_off_delay` | Motion off delay | Minutes to wait before switching lights off |
| `input_text.tomorrow_shift_status` | Tomorrow shift status | Text summary used by the dashboard |
