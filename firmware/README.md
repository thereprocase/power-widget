# Firmware and PC reporting plan

Design only. No firmware binary or hardware driver implementation exists yet.

Use a small USB-device MCU on the PC side of the isolation barrier, provisionally STM32F042 in a package that exposes USB, I²C, and debug without pin conflicts. Confirm the exact pin map and toolchain before schematic capture. The inline USB 2.0 path does not connect to this MCU.

## Device responsibilities

- Enumerate as USB CDC ACM on the reporting port; use a legitimate VID/PID arrangement for any distributed product.
- Configure/read the INA228 over isolated I²C, initially at 100 kHz.
- Convert raw signed shunt voltage and bus voltage using unit calibration. Use the wider ADC range required by current scenarios; don't reuse low-range scale factors.
- Timestamp each acquisition window and calculate signed power at the fixed B-side PCB plane.
- Maintain signed net energy plus separate positive/negative energy totals in RAM. Track elapsed time and data gaps explicitly. No frequent flash writes for energy logging.
- Store calibration version, coefficients, instrument serial, date, and checksum in protected nonvolatile storage. Detect invalid calibration.
- Poll diagnostic status; distinguish input unavailable, communication fault, overflow, stale data, and valid near-zero current. Alerts are telemetry, not the hardware fault cutout.
- Keep normal charge/data pass-through independent of application firmware activity.

## Protocol draft

One UTF-8 JSON record per line, versioned from the start. A proposed record contains:

| Field | Meaning |
|---|---|
| `version`, `serial`, `seq` | Protocol identity, device identity, increasing record number |
| `mode` | `precision` or `trend`; performance bounds differ |
| `window_start_us`, `window_end_us` | Monotonic device acquisition interval |
| `plane` | `pcb_b`; do not imply voltage at the far end of a cable |
| `voltage_uV`, `current_uA`, `power_uW` | Calibrated integer values; positive current flows A to B |
| `energy_net_uWh`, `energy_to_b_uWh`, `energy_from_b_uWh` | Accumulators with defined sign and reset behavior |
| `valid`, `status`, `calibration_id` | Measurement quality and traceability |

Use `null` measurement values when unavailable. A stopped sensor must not generate synthetic zero readings or carry a stale record forward as new. Report cumulative values even when the host misses packets, but do not pretend to integrate across sensor outages.

Proposed commands: `info`, `start`, `stop`, `set_mode`, `reset_energy`, `read_calibration`. Calibration writes require an explicit calibration workflow and a validated record; ordinary monitoring never auto-zeroes or writes settings to the connected charger.

## Host software

First host deliverable should be a small command-line serial logger with CSV output, a readable live voltage/current/power line, and reconnect handling. Separate a future plotting UI from acquisition. Keep raw records and calibration metadata alongside processed logs. No cloud service is required.

Verify time integration with known constant loads, signed reversals, and deliberate gaps. Test parsing/scale/overflow behavior with synthetic vectors once actual firmware and host code exist. Do not count this protocol plan as implemented or tested software.
