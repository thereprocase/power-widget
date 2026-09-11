# Power Widget

[![Complete single-sheet schematic: continuous wiring, four-terminal shunt, isolated sensing and USB reporting](hardware/bench-rev-a/single-sheet.svg)](hardware/bench-rev-a/single-sheet.svg)

**Current image: schematic layout mockup.** It is generated from `circuit.json`, not exported from KiCad, and is not the canonical editable schematic. Conversion of this layout into the [native KiCad project](hardware/bench-rev-a/power-widget-bench.kicad_pro) is in progress.

**Reusable agent prompt, including the original inspiration:**

> think through the layout and topology from the perspective of a brilliant 1980s electrical engineer who stayed current on everything straight through to 2026. use his brain to architect the sheet and make it gorgeous
>
> Create a complete, flat, single-sheet schematic from this project's authoritative circuit data. Make the page explain the circuit: power and signal flow, measurement branches, isolation boundaries, supplies and service controls. Use traditional electrical symbols, continuous wires, explicit junction dots and bridged crossings. Keep every component and numbered pin accounted for; annotate wires with net names instead of replacing connections with labels. Preserve the circuit exactly. Use deliberate placement, readable typography and restrained color, with the clarity of a classic service-manual foldout. Verify connectivity against the source, export a zoomable SVG and printable PDF, put the image at the top of the README, and commit and push the result.
>
> Use conventional schematic symbols that engineers recognize on sight: ANSI-style zigzag resistors; parallel-plate nonpolarized capacitors and explicitly marked polarized capacitors; coil inductors; diode anode/cathode symbols with the cathode bar; LEDs with outward light arrows and photodiodes with inward light arrows; normally open or normally closed switch contacts shown in their unactuated state; connector pins, jumper links and test points; four-terminal Kelvin shunts with separate force and sense terminals; and, where present, BJT base/collector/emitter and emitter arrows, MOSFET gate/drain/source and body diodes, and op-amp triangles with +/− inputs. Use functional IC rectangles with named and numbered pins. Distinguish signal common, chassis ground and protective earth; preserve separate isolated returns. Use these symbols only for the devices and functions actually present. Verify each symbol's device type, terminal mapping, polarity, arrow direction and default state against the circuit data and the manufacturer's pinout. Rotate or mirror symbols only while preserving their electrical meaning. A wire crossing is not a junction unless explicitly dotted; a graphic must never imply an unintended connection. Check the rendered drawing as well as its underlying netlist.
>
> Implement the layout in the canonical, editable source of the design system this project actually uses: for KiCad, the native schematic in the existing KiCad project. Preserve component identities, footprints, pin mappings and PCB associations. Export the README image and PDF directly from that native source, and run the design system's electrical checks plus schematic-to-PCB consistency checks. Ensure the normal regeneration workflow cannot overwrite the native design with a competing source of truth. A separately drawn SVG or diagram is only a mockup, even if its netlist matches; label any intermediate mockup explicitly and do not present it as the canonical schematic.

**The whole circuit on one sheet:** [zoomable SVG](hardware/bench-rev-a/single-sheet.svg) · [printable A1 PDF](hardware/bench-rev-a/single-sheet.pdf) · [drawing notes and reproduction](hardware/bench-rev-a/README.md#single-sheet-schematic). All 82 components and 65 nets, with continuous wires, junction dots and bridged crossings. Green is the inline domain; blue is the isolated PC domain. J1 and P1 each have power and signal-contact sections on this same page.

An inline USB-C power monitor with isolated PC reporting. Preserve the original charger and cable negotiation while measuring voltage, current, watts and Wh.

**Newest design: [bench revision A native KiCad project](hardware/bench-rev-a/README.md).** It includes the sensing circuit, isolated USB reporting, STM32 firmware/debug access, assigned footprints and a routed bench PCB. Native KiCad checks report **zero ERC violations, DRC violations, unconnected items and schematic/PCB mismatches**. See the [layout review](docs/layout-review.md) for evidence and open gates. **The selected USB population is 5 A maximum; the project’s 9 A USB assembly is still a sourcing and qualification gate.**

## Board preview and drawings

![Bench revision A: top copper, front silkscreen and board outline](hardware/bench-rev-a/pcb-top.svg)

Actual KiCad 2D plot of the **125 × 107 mm** bench PCB. The reporting USB-C port is on the lower long edge. This is an unbuilt prototype design; no 3D assembly render or hardware photographs are available yet.

| View | Contents |
|---|---|
| [PCB views](hardware/bench-rev-a/README.md#pcb-views) | Top and bottom copper plots from the routed board |
| [Circuit drawings](hardware/bench-rev-a/README.md#circuit-drawings) | Complete single-sheet schematic, five connection-sheet previews and native KiCad sources |
| [Architecture diagram](docs/architecture.md#two-power-domains-and-a-passive-main-path) | Transparent power path, sensing and isolated PC reporting |
| [Editable KiCad project](hardware/bench-rev-a/power-widget-bench.kicad_pro) | Schematic, PCB and local symbol/footprint libraries in the same directory |

## Design target

| Item | Requirement |
|---|---|
| Voltage | 28 V DC; at least 33.6 V component design margin |
| Continuous current | **9 A target: documented laptop maximum 8.5 A + 0.5 A** |
| Current design margin | **10.8 A: 1.20 × the 9 A target** |
| Inline data | USB 2.0; retain other contacts for charging transparency |
| Power accuracy | ±1% of reading at ≥5 W; ±5% from 0.5 W to below 5 W |
| Acquisition | About 58 fresh pairs/s, time-weighted one-second V/A/W reports and accumulated Wh |
| Reporting | Isolated USB-C on a long edge; timestamped serial, optional PC MQTT/HTTP forwarding |
| Product | Cheap but good; no display, battery or standalone logger required |

The selected [Apple/Dell/Lenovo laptop roster](docs/manufacturer-modes.md) drives the target. Extreme proprietary phone charging is excluded. The original 10 A/full-EPR and later 6 A specifications are superseded; voltage remains 28 V. No physical assembly is qualified yet.

## Early open question: captive male or two receptacles?

**Captive male is the bench baseline; final product topology remains open.** The original charger cable enters one receptacle, and a short custom captive plug extends its contacts to the device. The separate PC receptacle is on a long edge. OEM MagSafe/slim-tip cables may require charger-side placement and different energy accounting.

Two inline receptacles remain an allowed outcome if their orientation and cable-discovery behavior can be made transparent. Fixed CC wiring between two ordinary C-to-C cables fails some orientations; the [contact map and truth table](docs/connector-routing.md) explain the constraint. A generic cut cable is not a qualified captive assembly.

## Bench circuit and calculated feasibility

INA228 measures a 5 mΩ four-terminal high-side shunt. An inline LDO powers sensing; a PC-powered STM32F072CBT6 communicates through isolated I²C. The board includes SWD, UART, GPIO, force/Kelvin access and selectable floating sensor power. Dedicated links support measuring board consumption. Original charging contacts have no inline PD controller or substituted contract.

| Calculation | Preliminary result |
|---|---|
| Largest one-second DC error allocation, ≥5 W | **0.874%**, at 28 V / 5 W |
| Largest one-second DC error allocation, 0.5–<5 W | **4.539%**, at 28 V / 0.5 W |
| Sensor window / reporting | **17.28 ms / one second** |
| Added hot loop resistance, captive study | **14.879 mΩ** against a 15 mΩ target |
| Shunt heat at 9 A / 10.8 A | **0.405 W / 0.583 W** nominal |

These are engineering allocations, not measured specifications. One-second noise, dynamic energy accuracy, thermal behavior and connector performance require physical validation. A board-output reading needs a downstream cable correction before being called laptop-input energy.

## Design package

| Read | Purpose |
|---|---|
| [Design brief](docs/design-brief.md) | Current requirements and assumptions |
| [Bench hardware](hardware/bench-rev-a/README.md) | Circuit sheets, component schedule, jumpers and bring-up |
| [Manufacturer modes](docs/manufacturer-modes.md) | Primary laptop evidence and rating rule |
| [Connector wiring](docs/connector-routing.md) | Contact map and orientation proof |
| [Architecture](docs/architecture.md) / [decisions](docs/decisions.md) | Components, domains and unresolved gates |
| [Calculated budgets](analysis/results.md) / [method](docs/budgets.md) | Accuracy, loss, timing and assumptions |
| [Firmware contract](firmware/README.md) | MCU pins, sensor registers, timestamped serial and integration plan |
| [Energy comparison](docs/energy-comparison.md) | Matching intervals, board consumption, cable correction and uncertainty |
| [Validation](docs/validation-plan.md) / [cost and build](docs/cost-and-build.md) | Prototype qualification and planning allowances |
| [Research record](docs/sources.md) / [progress](docs/progress.md) | Sources, evidence gaps and checkpoints |

## Reproduce

```sh
python tools/budgets.py --check
python tools/orientations.py --check
python tools/capture_bench.py --check
python tools/draw_flat_schematic.py --check
```

Omit `--check` to regenerate. Python standard library only. The budget sweep covers 19,635 settled operating points at the 9 A target. Circuit checks validate named connections and reproducibility; they do not run KiCad ERC.

## Next gate

Review the routed PCB against a fabricator's stack and capabilities, finalize the orderable BOM and captive strain relief, and resolve protection/overrange behavior before fabrication release. Source and qualify the required 9 A USB assembly; the selected USB parts support only the 5 A bench population. Firmware can start on the documented interfaces while these gates close. Physical validation must establish thermal capacity, measurement accuracy and OEM charging compatibility. Earlier designs remain in commit history.
