# Design brief

Revision 0.5 — 2026-09-10. Laptop scope, full firmware-capable bench prototype and matched-interval energy logging.

## Purpose

Measure power flowing between an original USB-C charger and device, and report it to a PC through a separate, galvanically isolated USB-C connection. Preserve the charging behavior that would occur with the original charger and cable. Target a small, inexpensive, reliable instrument.

## Requirements

| ID | Requirement | Status |
|---|---|---|
| R01 | 28 V DC; 9 A continuous target = documented laptop maximum 8.5 A + 0.5 A | Selected for the dated Apple/Dell/Lenovo roster; physical rating unqualified |
| R02 | At least 20% electrical margin: 33.6 V and 10.8 A | Retained; the 0.5 A allowance is added before the 20% multiplier |
| R03 | Original source and load negotiate directly; no substitute PD contracts, charger identity, or cable-capability claims | User requirement |
| R04 | Preserve standard and vendor-specific charging communications, including Apple, Dell, Lenovo, and other relevant combinations | User requirement; compatibility must be demonstrated |
| R05 | USB 2.0 inline data; no requirement for higher-speed data or video | User requirement |
| R06 | Separate USB-C reporting receptacle on a long edge | User requirement |
| R07 | Galvanic isolation of reporting data, supply, ground, and unintended shield paths from the inline circuit | User requirement |
| R08 | Measured voltage/current, calculated watts and accumulated Wh; prefer signed bidirectional readings | User requirement |
| R09 | Power error within ±1% of reading at 5 W and above; ±5% from 0.5 W to below 5 W, within the rated envelope | User requirement |
| R10 | Measurement may require both inline power and a PC connection | User requirement |
| R11 | Cheap but good; no display, battery, or standalone logging required | User requirement |
| R12 | Checkpoint requirements, analysis, decisions, and progress to this repository | User requirement |
| R13 | Frequent fresh acquisitions feeding time-weighted one-second averages, with explicit coverage and gaps | Latest user requirement; nominal 57.87 fresh pairs/s candidate |
| R14 | Timestamped serial output; MQTT/HTTP can be PC-side bridges | Latest user requirement; USB serial baseline |
| R15 | Low insertion loss and accounted board consumption; compare wall and laptop-input energy over matching intervals | Latest user requirement; define measurement plane and combined uncertainty |
| R16 | First board includes onboard MCU, isolated sensing, force connections and accessible firmware/debug interfaces | User replaces the small fixture with a complete bench prototype |

The original 10 A/full-EPR request and subsequent 6 A/168 W requirement were superseded. Voltage remains 28 V. The rectangular design envelope is 252 W, without implying an OEM offers 28 V / 9 A. R02 is design reserve, not an operating rating. Extreme proprietary phone modes are excluded. See the [manufacturer survey](manufacturer-modes.md) for the evidence and remaining physical tests.

## Early open question: connector topology

**Keep both outcomes available. The user leans toward a short captive male pigtail on the load side.**

| Option | Physical arrangement | Decision basis |
|---|---|---|
| A — preferred candidate | Original charger cable into one receptacle; short captive USB-C male output; PC receptacle on long edge | Known added wiring, one external charger cable, fewer mating interfaces |
| B — allowed alternative | Two inline receptacles on opposing short edges; PC receptacle on long edge | Serviceability and no captive lead, weighed against two independent cable/marker/orientation states |

Captive male is the bench baseline after the [logical contact/orientation analysis](connector-routing.md); final product topology remains open through assembly sourcing and physical tests. A generic cut USB-C cable is not automatically a suitable pigtail: its second CC/VCONN contact, marker, terminations, and other conductors must be known. Do not freeze pin routing on the assumption that matching pin labels are sufficient.

## Engineering assumptions to validate

- Initial accuracy qualification: 5–28 V, 0.5 W up to rated current × voltage, 15–35°C ambient, after warm-up. Operation elsewhere may be explored, but is not yet an accuracy promise.
- The initial OEM survey focuses on Apple, Dell, Lenovo, and other laptop chargers identified for compatibility. The user's wording is broad; extreme proprietary phone modes are now excluded. The initial laptop roster is now bounded and documented; physical compatibility remains unqualified.
- The 9 A / 10.8 A design target follows the documented 8.5 A laptop maximum. Excluded phone-current studies remain in history.
- Accuracy applies initially to settled one-second DC reports at the defined plane. Frequent sampling and integration are required; pulsed-load energy accuracy and one-second noise need separate validation.
- Initial measurement plane is the output-side PCB Kelvin points. A captive cable adds loss beyond that plane; laptop-terminal power requires additional sensing or a qualified correction.
- Power pass-through should remain available during MCU reset or PC disconnection. This is a proposed transparency target, distinct from standalone measurement.
- 28 V is a nominal charging level; permitted source tolerance, overshoot, and the eventual overvoltage threshold need explicit treatment.
- Budget figures are planning allowances until actual suppliers, quantities, and assembly charges are checked.

Use matched energy intervals, clock/coverage metadata, characterized self-consumption and an explicit downstream cable correction; see [energy-comparison.md](energy-comparison.md).

## Required design outputs

1. Connector and charging feasibility assessment with explicit decision gates.
2. Provisional architecture, candidate parts, and measurement reference plane.
3. Reproducible error, voltage-drop, heating, and cost calculations.
4. PC reporting, calibration, prototype, and acceptance-test plans.
5. A complete bench circuit draft and firmware pin/register contract, with force, calibration and debug access.
6. A maintained next-step handoff. PCB/fabrication release follows schematic/ERC, footprint, connector and protection review.
