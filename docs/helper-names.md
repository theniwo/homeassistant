# Home Assistant helper names

GUI helper names use concise English labels. Temperature helpers use the room name alone; their radiator icon identifies them. For time controls, `Lead` means the action is scheduled before its reference event, and `Delay` means it is scheduled after. Existing entity IDs containing `offset` are retained so current automations keep working; `Sick temp offset` is a temperature difference, not a time control. Clock values use `time`.

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
| `input_boolean.gnome_dnd_niwo` | GNOME DND niwo | Legacy per-account DND request; superseded by its policy selector |
| `input_boolean.gnome_dnd_work` | GNOME DND work | Legacy per-account DND request; superseded by its policy selector |
| `input_boolean.gnome_dnd_niwo_actual` | GNOME DND niwo actual | Read-back state from the niwo desktop agent |
| `input_boolean.gnome_dnd_work_actual` | GNOME DND work actual | Read-back state from the work desktop agent |
| `input_boolean.snom_dnd_status` | Snom DND status | Read-back state from the Snom phone |
| `input_boolean.enforce_sleep` | Enforce sleep | Apply the room shutdown when Sleep Mode starts |
| `input_select.work_schedule_mode` | Work schedule mode | Automatic, free shift, or sick mode |
| `input_select.enforce_sleep_reset_mode` | Enforce sleep reset | Reset policy for Enforce sleep |
| `input_select.whz_sleep_profile` | WHZ sleep profile | Living room profile while Sleep Mode is active |
| `input_select.gnome_dnd_niwo_policy` | GNOME niwo DND policy | Follow global, force on, or force off |
| `input_select.gnome_dnd_work_policy` | GNOME work DND policy | Follow global, force on, or force off |
| `input_select.snom_dnd_policy` | Snom DND policy | Follow global, force on, or force off |
| `input_select.samsung_s25_dnd_policy` | Samsung S25 DND policy | Follow global, force on, or force off |

## Heating

| Entity ID | GUI name | Purpose / unit |
| --- | --- | --- |
| `input_number.whz_target_temp` | Wohnzimmer | Living room comfort target, °C |
| `input_number.az_target_temp` | Arbeitszimmer | Office comfort target, °C |
| `input_number.sz_target_temp` | Schlafzimmer | Bedroom comfort target, °C |
| `input_number.heating_min_temp` | Min temp | Base target with windows closed, °C |
| `input_number.window_open_temp` | Window open temp | Target while a window is open, °C |
| `input_number.heating_preheat_offset` | Preheat lead | Start heating before a schedule event, hours |
| `input_number.heating_cooldown_offset` | Cooldown lead | Begin cooling before shift end, hours |
| `input_number.sick_temp_offset` | Sick temp Increase | Additional heating in sick mode, °C |

## Schedule, reminders, and DND

| Entity ID | GUI name | Purpose / unit |
| --- | --- | --- |
| `input_datetime.early_shift_start` | Early shift start | Early shift start time |
| `input_datetime.early_shift_end` | Early shift end | Early shift end time |
| `input_datetime.late_shift_start` | Late shift start | Late shift start time |
| `input_datetime.late_shift_end` | Late shift end | Late shift end time |
| `input_datetime.free_shift_start` | Free shift start | Start time for free-shift profile |
| `input_datetime.vacation_wake_time` | Vacation wake time | Wake time for the vacation profile |
| `input_number.alarm_offset` | Alarm lead | Hours before shift start |
| `input_datetime.alarm_setup_time` | Alarm check time | Daily time for the next-day calendar check |
| `input_number.sleep_duration` | Sleep duration | Sleep duration, hours |
| `input_number.wind_down_offset` | Wind-down lead | Hours before sleep time |
| `input_number.dnd_offset` | DND lead | Hours before calculated bedtime |
| `input_number.pill_morning_offset` | Meds morning lead | Hours before shift start |
| `input_number.pill_bedtime_offset` | Meds evening lead | Hours before bedtime |
| `input_number.sick_pill_offset` | Sick meds delay | Hours after the free-shift reference time |

## Phone and Echo

| Entity ID | GUI name | Purpose / unit |
| --- | --- | --- |
| `input_datetime.phone_handover_time` | Phone handover time | Phone handover clock time |
| `input_number.phone_handover_offset` | Phone handover delay | Delay after the handover clock time before announcements, minutes |
| `input_number.work_sim_voicemail_prompt_timeout` | Work SIM voicemail prompt timeout | Minutes before the follow-up announcement; current value 10, range 1–30, step 1 |
| `input_select.bt_disconnect_mode` | BT disconnect mode | Select alarm, bedtime, or fixed-time disconnect; starts as `Zum Schlafen` after Home Assistant restarts |
| `input_number.bt_disconnect_offset` | BT alarm lead | Disconnect lead before the alarm, seconds |
| `input_number.bt_sleep_disconnect_offset_hours` | BT sleep delay | Delay after bedtime before Echo Bluetooth disconnects, hours |
| `input_datetime.bt_disconnect_time` | Fixed disconnect time | Daily disconnect time; initial value `00:00` |
| `input_number.bt_connect_offset` | BT connect delay | Connect the phone to the bedroom Echo after scheduled Sleep Mode, minutes; default 5, range 0–20 |
| `input_number.bt_connect_retry_interval` | BT connect retry interval | Minutes between attempts to connect the phone to the bedroom Echo; default 5, range 1–30, step 1 |
| `input_number.bt_connect_retry_attempts` | BT connect retry attempts | Maximum total connection attempts, including the first; default 3, range 1–10, step 1 |
| `input_text.bt_phone_source` | BT phone source | Paired phone source name used by the bedroom Echo |
| `input_number.echo_announcement_volume` | Echo announcement volume | Announcement volume on a 0–10 scale |
| `input_number.echo_wake_delay` | Echo wake delay | Delay after the bedroom alarm is dismissed, seconds; default 15 |
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
| `input_number.hallway_light_max_on` | Hall light max on | Maximum continuous on time for hallway lights, fail-safe, minutes; default 10 |
| `input_number.wake_light_delay` | Wake light delay | Delay after the scheduled wake time before bedroom lights turn on, minutes; default 1, range 0–10, step 1 |
| `input_text.tomorrow_shift_status` | Tomorrow shift status | Text summary used by the dashboard |
