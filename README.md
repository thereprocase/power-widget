# Power Widget

An inline USB-C power monitor with isolated PC reporting. Preserve the original charger's negotiation and cable identity while measuring voltage, current, power, and energy.

**Current status: preliminary design and planning. No orderable hardware yet.** The laptop current target and captive connector wiring are defined. Bench prototype design and connector qualification are in progress.

## Required envelope

| Item | Requirement |
|---|---|
| Voltage | 28 V DC; at least 33.6 V electrical design margin |
| Continuous current | **9 A target: documented laptop maximum 8.5 A + 0.5 A** |
| Current design margin | **10.8 A: 1.20 × the 9 A target** |
| Inline data | USB 2.0; preserve additional contacts needed for validated charging behavior |
| Accuracy | ±1% of power reading at ≥5 W; ±5% from 0.5 W to below 5 W |
| Reporting | Separate USB-C receptacle on a long edge; galvanically isolated |
| Product | Cheap but good; no display, battery, or standalone logger required |

The latest current rule supersedes the earlier 6 A / 168 W brief. The selected laptop roster now supports a **9 A / 10.8 A design target**. Extreme proprietary phone charging is excluded by the latest user instruction. No physical assembly is qualified yet. Voltage remains 28 V, not full EPR.

## First open question: captive male or two receptacles?

**Captive male selected for bench revision A.** Final product topology remains open; a two-receptacle outcome needs a proven solution for orientation and cable discovery.

| Candidate | Arrangement |
|---|---|
| Preferred starting point | Original charger cable → monitor receptacle → short captive male → device; separate PC receptacle |
| Allowed alternative | Two inline USB-C receptacles with external cables; separate PC receptacle |

Choose after proving CC/VCONN routing, cable discovery, plug orientations, vendor behavior, current capacity, and assembly sourcing. Some OEM cables with a different device-end connector may require charger-side placement. A captive plug helps control the added wiring; it does not guarantee compatibility.

## Provisional design

- INA228 with a **5 mΩ four-terminal high-side shunt**, using its wider ADC range for the revised current scenarios.
- Inline-powered sensing and a PC-powered USB MCU, connected through **isolated I²C**. No power conductor crosses the isolation barrier.
- A fixed measurement plane at the output-side PCB sense points; account for any cable beyond it.
- Original source/device negotiation, with no substituted charger, cable, or PD contract.

| Calculation | Preliminary result |
|---|---|
| Largest precision error allocation, ≥5 W | **0.874%**, at 28 V / 5 W |
| Largest precision error allocation, 0.5–<5 W | **4.539%**, at 28 V / 0.5 W |
| Precision acquisition window | About **0.54 s** |
| Added hot loop resistance, captive study | **14.879 mΩ** against a 15 mΩ target |
| Shunt heat, 9 A / 10.8 A scenarios | **0.405 W / 0.583 W** nominal |

These are calculations with stated allocations, not measured specifications. Calibration, noise, thermal gradients, contacts, and charging behavior still require physical qualification. The larger 12.5 A / 15 A-design scenario exceeds the present 1 W shunt's capability.

## Design package

| Read | Purpose |
|---|---|
| [Design brief](docs/design-brief.md) | Current requirements and assumptions |
| [Manufacturer modes and rating rule](docs/manufacturer-modes.md) | Survey gaps and conditional current scenarios |
| [Connector wiring](docs/connector-routing.md) | Contact map and CC/VCONN orientation analysis |
| [Open decisions](docs/decisions.md) | Topology, fault behavior, and architecture gates |
| [Architecture](docs/architecture.md) | Block diagram, candidate parts, signal and isolation paths |
| [Calculated budgets](analysis/results.md) | Accuracy, loss, range, and scenario results |
| [Budget method](docs/budgets.md) | Assumptions, derivation, and limitations |
| [Validation plan](docs/validation-plan.md) | Coupon, calibration, compatibility, and qualification tests |
| [Cost and build plan](docs/cost-and-build.md) | Allowances and prototype sequence |
| [Firmware/reporting plan](firmware/README.md) | Protocol and logging behavior; not implemented yet |
| [Research record](docs/sources.md) | Primary references and unresolved evidence |
| [Progress and handoff](docs/progress.md) | Checkpoints and next actions |

## Reproduce the calculations

```sh
python tools/budgets.py
python tools/budgets.py --check
```

Python standard library only. Inputs: [assumptions.json](analysis/assumptions.json). Outputs: [JSON](analysis/results.json), [CSV](analysis/accuracy.csv), and Markdown. The sweep covers 19,635 settled operating points for the provisional 9 A scenario.

## Next gate

Build one accessible bench prototype with sensing, isolation, MCU, debug access, and connector experiments. It replaces the standalone continuity coupon. Qualify connector assemblies and resolve overrange behavior before a fabrication release. The newest practical build will remain prominent here; earlier designs belong in commit history or tagged revisions.
