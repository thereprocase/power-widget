# Design brief

Revision 0.3 — 2026-09-10. Requirements baseline, including the revised manufacturer-current rule.

## Purpose

Measure power flowing between an original USB-C charger and device, and report it to a PC through a separate, galvanically isolated USB-C connection. Preserve the charging behavior that would occur with the original charger and cable. Target a small, inexpensive, reliable instrument.

## Requirements

| ID | Requirement | Status |
|---|---|---|
| R01 | 28 V DC; rated continuous current = highest applicable manufacturer charging current + 0.5 A | Latest user requirement; numeric current awaits the OEM survey |
| R02 | At least 20% electrical margin: 33.6 V and 1.20 × the R01 current | Retained; the 0.5 A allowance is added before the 20% multiplier |
| R03 | Original source and load negotiate directly; no substitute PD contracts, charger identity, or cable-capability claims | User requirement |
| R04 | Preserve standard and vendor-specific charging communications, including Apple, Dell, Lenovo, and other relevant combinations | User requirement; compatibility must be demonstrated |
| R05 | USB 2.0 inline data; no requirement for higher-speed data or video | User requirement |
| R06 | Separate USB-C reporting receptacle on a long edge | User requirement |
| R07 | Galvanic isolation of reporting data, supply, ground, and unintended shield paths from the inline circuit | User requirement |
| R08 | Voltage, current, power, accumulated energy; prefer signed bidirectional readings | Accepted brief |
| R09 | Power error within ±1% of reading at 5 W and above; ±5% from 0.5 W to below 5 W, within the rated envelope | User requirement |
| R10 | Measurement may require both inline power and a PC connection | User requirement |
| R11 | Cheap but good; no display, battery, or standalone logging required | User requirement |
| R12 | Checkpoint requirements, analysis, decisions, and progress to this repository | User requirement |

The original 10 A/full-EPR request and subsequent 6 A/168 W requirement were superseded. Voltage remains 28 V. Maximum rated power will be 28 V × the finalized current rating. R02 is design reserve, not an operating rating. See the [manufacturer survey](manufacturer-modes.md) for evidence gaps and explicitly hypothetical sizing scenarios.

## Early open question: connector topology

**Keep both outcomes available. The user leans toward a short captive male pigtail on the load side.**

| Option | Physical arrangement | Decision basis |
|---|---|---|
| A — preferred candidate | Original charger cable into one receptacle; short captive USB-C male output; PC receptacle on long edge | Known added wiring, one external charger cable, fewer mating interfaces |
| B — allowed alternative | Two inline receptacles on opposing short edges; PC receptacle on long edge | Serviceability and no captive lead, weighed against two independent cable/marker/orientation states |

Select the topology after a signal-path proof and assembly sourcing review. A generic cut USB-C cable is not automatically a suitable pigtail: its second CC/VCONN contact, marker, terminations, and other conductors must be known. Do not freeze pin routing on the assumption that matching pin labels are sufficient.

## Engineering assumptions to validate

- Initial accuracy qualification: 5–28 V, 0.5 W up to rated current × voltage, 15–35°C ambient, after warm-up. Operation elsewhere may be explored, but is not yet an accuracy promise.
- The initial OEM survey focuses on Apple, Dell, Lenovo, and other laptop chargers identified for compatibility. The user's wording is broad; phone-specific modes remain an explicit scope/qualification question rather than being declared covered. The final ceiling cannot close until the applicable manufacturer roster is bounded and verified.
- A 9 A / 10.8 A-margin scenario is used to continue circuit analysis; 7.5 A and 12.5 A scenarios expose sensitivity. None is represented as the verified required current.
- Accuracy applies to settled DC readings at the defined measurement plane. A faster trend stream has a separate noise/bandwidth characterization.
- Initial measurement plane is the output-side PCB Kelvin points. A captive cable adds loss beyond that plane; laptop-terminal power requires additional sensing or a qualified correction.
- Power pass-through should remain available during MCU reset or PC disconnection. This is a proposed transparency target, distinct from standalone measurement.
- 28 V is a nominal charging level; permitted source tolerance, overshoot, and the eventual overvoltage threshold need explicit treatment.
- Budget figures are planning allowances until actual suppliers, quantities, and assembly charges are checked.

## Required design outputs

1. Connector and charging feasibility assessment with explicit decision gates.
2. Provisional architecture, candidate parts, and measurement reference plane.
3. Reproducible error, voltage-drop, heating, and cost calculations.
4. PC reporting, calibration, prototype, and acceptance-test plans.
5. A maintained next-step handoff. Schematic and PCB release follow the unresolved architecture gates.
