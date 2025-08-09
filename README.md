# NILM MVP

Home Assistant Add-on für Non-Intrusive Load Monitoring.

## Installation
1. Ordner `addon` nach `/addons/nilm_mvp` auf dem Home Assistant Host kopieren.
2. Im Add-on Store neu laden und das Add-on installieren.
3. Starten und den Anweisungen im Log folgen.

## Konfiguration
Beispiel:

```
sources:
  grid_power_sensor: sensor.ltibber_0100100700ff
  pv_power_sensor: sensor.hub_1200_1_output_home_power
detection:
  sample_interval_s: 3
  min_delta_w: 60
  min_event_duration_s: 10
  deadband_w: 40
  hysteresis_w: 15
classification:
  confidence_threshold: 0.7
locale:
  language: de
```

## Architektur
- `app/`: Python Service
- `addon/`: Home Assistant Add-on Dateien
- `tests/`: Unit-Tests

Die Kernformel lautet:

```
house_load = clamp_deadband(PV + grid_import - grid_export, deadband=40, hysteresis=15)
```
