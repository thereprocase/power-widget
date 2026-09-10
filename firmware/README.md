# Firmware and PC reporting contract

Bench A uses **STM32F072CBT6, LQFP48, 128 KB flash / 16 KB RAM**, on the PC side of the isolation barrier. [board_contract.h](board_contract.h) provides register settings, pin constants and raw-value decoding to start implementation. There is no MCU application, USB stack, INA228 hardware driver, logger or tested binary yet.

## Board interface

| Function | MCU connection | Configuration |
|---|---|---|
| USB full-speed device | PA11 pin 32 D−, PA12 pin 33 D+ | HSI48 with USB CRS; native USB CDC ACM |
| INA228 I²C through U2 | PB6 pin 42 SCL, PB7 pin 43 SDA | I²C1 AF1, open drain, 100 kHz; external switched pull-ups |
| Isolator supply enable | PA1 pin 11 | High enables U7; default low via R25 |
| PC VBUS sense | PA0 pin 10 | 100k/100k divider; ADC input, no internal pull |
| Debug UART | PA2 pin 12 TX, PA3 pin 13 RX | USART2 AF1; start at 115200 8N1 |
| SWD | PA13 pin 34 / PA14 pin 37 | Leave debug active during bring-up |
| User button / LED | PB0 pin 18 / PB1 pin 19 | Button active low; LED active high |
| Boot / reset | BOOT0 pin 44 / NRST pin 7 | Physical buttons; boot defaults low |
| Spare headers | PA4–PA7, PB10–PB11 | Leave high impedance until configured |

VDDIO2 pin 36, VDD pins 24/48 and VBAT pin 1 all receive PC 3.3 V; VDDA pin 9 is filtered locally. Use a 64-bit monotonic microsecond clock, for example by extending a 1 MHz TIM2 counter. Handle rollover explicitly. Nominal 48 MHz is not a calibrated timebase: log host/device clock mapping and validate drift. USB suspend stops acquisition, preserves covered energy in RAM and records a gap on resume. A power reset starts a new session.

Before enabling I²C, enable U7 and allow its rail/isolator to settle; start with a conservative 5 ms bench delay and verify it physically. Before suspend, finish or cancel I²C, make PB6/PB7 high impedance with internal pulls disabled, turn PA1 off, extinguish the LED and enter an appropriate MCU low-power state. JP4 must be absent. Verify full reporting-port current; a software sleep call alone does not prove USB suspend compliance. The inline power and charging contacts do not depend on firmware execution.

## Acquisition contract

Use the INA228 at 7-bit address 0x40. Read and validate its identity before configuration. Register payloads are MSB-first; confirm whether the platform I²C API expects a 7-bit or shifted address. Read back configuration and surface discrepancies.

| Setting | Value / intent |
|---|---|
| CONFIG | 0x0000 after reset: wide shunt range, no temperature compensation |
| ADC_CONFIG, normal | 0xB922: continuous shunt + bus, 540 µs per channel, 16 averages |
| ADC_CONFIG, diagnostic | 0xBB6D: 1052 µs per channel, 256 averages |
| DIAG_ALRT configuration | 0x8000: latch status; poll CNVRF bit 1, require MEMSTAT bit 0 healthy |
| Raw VSHUNT | Register 0x04, signed 20-bit value in bits 23:4 of three bytes, 312.5 nV/count |
| Raw VBUS | Register 0x05, positive 20-bit value in bits 23:4, 195.3125 µV/count |

Normal sensor cadence is nominally 17.28 ms, about 57.87 fresh pairs/s. Poll readiness frequently enough to collect each result; begin with a roughly 2 ms poll interval and characterize overhead. Read ready/status, then both raw registers, then status again. If another completed conversion arrived during those reads, discard the potentially mixed pair and retry from the newly completed result; bound retries and flag overruns. A ready flag is not a sample counter, so delayed servicing cannot reveal exactly how many updates were missed. Retain an estimated missed count and mark uncertain coverage.

Calibrate shunt gain/offset and bus gain/offset against the declared PCB_B reference plane. Convert the signed shunt reading to current using calibrated resistance/gain, then multiply each calibrated voltage/current pair. Do not clamp small negative currents to zero or silently auto-zero against an attached laptop. Sensor absence, overflow, calibration failure and a legitimate zero-current reading are distinct states. The wide ADC span is not the board's physical rating.

The baseline uses MCU integration of calibrated readings. Do not treat the on-chip ENERGY register as meaningful without configuring SHUNT_CAL, reviewing its sign/overflow/timebase and applying compatible calibration. It is a useful dynamic-energy comparison during validation because its accumulation differs from multiplying output averages. Temperature conversion is disabled in normal mode; enabling it changes acquisition timing. Die temperature is not contact or shunt temperature.

## One-second reports and energy

Implement the time-weighted averaging, boundary splitting, coverage and integration rules in [energy-comparison.md](../docs/energy-comparison.md). Report V, I, the mean of per-pair watts and cumulative Wh. Keep signed net energy and separate to-B/from-B totals, splitting a reconstructed segment at a zero crossing when necessary. Use sufficient accumulator range and fractional precision; avoid repeated rounding of small energy increments. Never integrate through an unobserved sensor interval without an explicit, separately labeled estimate.

Use UTF-8 JSON Lines over USB CDC ACM. UART can expose the same protocol for bench debugging. Provisional protocol version 1 fields:

| Field | Meaning |
|---|---|
| `version`, `serial`, `boot_id`, `seq` | Protocol, instrument, session identity and monotonic record sequence |
| `mode` | Normally `logging_1s`; diagnostic modes have different noise/cadence |
| `window_start_us`, `window_end_us` | Monotonic one-second report boundaries |
| `covered_us`, `sample_count`, `missed_samples_est` | Coverage and acquisition health; estimated misses may be unknown |
| `plane` | `pcb_b` for primary measurements |
| `voltage_uV`, `current_uA`, `power_uW` | Time-weighted calibrated values; A-to-B current is positive |
| `energy_net_uWh`, `energy_to_b_uWh`, `energy_from_b_uWh` | Cumulative integrals over covered time, with fractional internal state |
| `uncovered_total_us`, `energy_complete` | Cumulative gaps and whether the total covers the whole session interval |
| `valid`, `status`, `calibration_id`, `time_uncertainty_us` | Quality, traceability and acquisition timing bound |
| `self_power_est_uW`, `self_model_id` | Optional characterized inline consumption estimate; otherwise null |

Use null values for unavailable measurements and explicit partial-window status for incomplete averages. A dropped host packet must not reset onboard energy. `reset_energy` starts a new energy epoch identified in records; MCU reset starts a new boot ID and never pretends to continue an old total. Store calibration identity, coefficients and checksum in protected flash; energy stays in RAM without frequent flash writes.

Proposed commands: `info`, `start`, `stop`, `set_mode`, `reset_energy`, `read_calibration`, and a request/reply clock-sync command returning device receive/transmit times. Calibration writes belong to an explicit fixture workflow. Use an authorized VID/PID arrangement before distributing a USB product; none is invented here.

## PC logger and implementation order

The first logger should preserve JSONL records, export CSV, show V/A/W/Wh and gaps, and reconnect by instrument and boot identity. Save host receive UTC plus device-to-UTC mapping and uncertainty. Optional MQTT publication or HTTP posting forwards records from the PC; transport latency must not replace acquisition timestamps. Keep wall-plug records and calibration metadata alongside the meter stream.

Bring up SWD/USB and the timer first, then U7/I²C/raw sensor reads, calibration and the one-second integrator, then serial logging and wall-energy comparison. Verify decoding/sign/range, constant-power integration, irregular timestamps, boundary splitting, power reversal, gaps, rollover and reboot behavior with deterministic vectors as implementation is added. Validate pulsed-load energy on hardware separately; synthetic tests cannot establish ADC fidelity.

Primary references: [ST STM32F072](https://www.st.com/resource/en/datasheet/stm32f072cb.pdf), [TI INA228](https://www.ti.com/lit/ds/symlink/ina228.pdf), [TI ISO1641](https://www.ti.com/lit/ds/symlink/iso1641.pdf), [TI TPS22919](https://www.ti.com/lit/ds/symlink/tps22919.pdf).
