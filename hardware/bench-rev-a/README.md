# Bench revision A — circuit draft

**28 V / 9 A continuous design target, 10.8 A design margin. No physical assembly is qualified.** This is the accessible prototype for connector experiments, calibration and MCU firmware development. It contains the complete proposed sensing, reporting, supply and debug circuits rather than a separate continuity fixture.

Open [power-widget-bench.kicad_sch](power-widget-bench.kicad_sch) as the root schematic. The five child sheets use embedded symbols. This is a generated pin-level draft: native KiCad loading, ERC, footprints and PCB layout still need review. KiCad is unavailable in the present workspace. Balanced syntax and connectivity checks are useful but do not establish that KiCad accepts or electrically approves the files. There are no Gerbers or assembly files.

| Circuit | Connection-sheet preview | KiCad source |
|---|---|---|
| Inline connectors, shunt and bench force points | [01-inline.svg](01-inline.svg) | [01-inline.kicad_sch](01-inline.kicad_sch) |
| INA228, filters and isolated I²C | [02-sensing.svg](02-sensing.svg) | [02-sensing.kicad_sch](02-sensing.kicad_sch) |
| Local supplies and current-measurement links | [03-supplies.svg](03-supplies.svg) | [03-supplies.kicad_sch](03-supplies.kicad_sch) |
| Reporting USB and STM32F072 | [04-usb-mcu.svg](04-usb-mcu.svg) | [04-usb-mcu.kicad_sch](04-usb-mcu.kicad_sch) |
| SWD, UART, GPIO, reset and boot controls | [05-debug.svg](05-debug.svg) | [05-debug.kicad_sch](05-debug.kicad_sch) |

The SVG files are readable connection sheets generated from the same circuit data, **not KiCad renders**. [circuit.json](circuit.json) records all 82 components and their numbered pins; [connections.json](connections.json) records the 65 named nets. The [component schedule](component-schedule.md) is a draft, not an orderable BOM.

## Bench arrangement

Allocate approximately 100 × 80 mm initially, four layers with 2 oz outer copper as a layout candidate. Put the main VBUS/shunt/return path along one short, direct edge; the whole board need not carry high current across its length. Place the PC receptacle on a long edge, with the MCU and all grounded debug connections on its side of a 4 mm barrier allocation. Keep metal standoffs, shields and copper away from the barrier. This is a proposed floorplan, not a routed PCB or insulation qualification.

J1 is the inline receptacle and P1 is the custom captive plug. Its individual contact wiring is defined in [connector-routing.md](../../docs/connector-routing.md). All CC-contact, SBU and SuperSpeed contact paths are retained; only USB 2.0 data performance is in scope. No inline PD controller, new e-marker, or charger-identification termination is fitted. Select the actual J1/P1 assembly only after drawings, orientation and current tests. Final product topology remains open.

| Access | Connections / use |
|---|---|
| J2 / J3 | Two-pin force connections: 1 = VBUS_A / VBUS_B, 2 = GND_INLINE. Electrically parallel with USB ports; use qualified terminals and short heavy leads. |
| J4 | 1 = upstream shunt Kelvin, 2 = downstream shunt Kelvin, 3 = PCB_B voltage, 4 = quiet inline ground. Sense only. |
| TP4 / TP5 | Separate A5 / B5 contact probes. Use suitable high-impedance, low-capacitance isolated probes; no grounded PC wire. |
| J5 | PC-side I²C: 1 = GND_PC, 2 = switched 3.3 V reference, 3 = SCL, 4 = SDA. External open-drain master supported with U3 held in reset and JP4 fitted. |
| J6 | Inline I²C: 1 = GND_INLINE, 2 = 3V3_INLINE, 3 = SCL, 4 = SDA. Floating instruments only. |
| J7 | Floating external supply: 1 = 3.3 V input, 2 = GND_INLINE. Current limit for initial bring-up; never tie to PC ground. |
| J9 | Cortex 10-pin SWD, 1.27 mm, keyed pin 7 absent. Pin 1 is target-voltage reference; pin 6 has no SWO. |
| J10 | 3.3 V UART: 1 = GND_PC, 2 = board TX, 3 = board RX, 4 = supply reference. |
| J11 | GPIO: GND_PC, 3V3_PC, PA4, PA5, PA6, PA7, PB10, PB11 in pin order. |

Header supply pins are references/outputs except the explicitly identified J7 input. External debug probes must not inject supply power. Grounded bench supplies, scopes and electronic loads can externally join the domains even when the board itself is isolated.

## Jumpers and power accounting

| Link | Normal state | Bench purpose |
|---|---|---|
| JP1 | One shunt on 1–2 | Selects inline LDO. Move the single shunt to 2–3 for floating external J7 supply; never fit both. |
| JP2 | Fitted | Replace with an ammeter to characterize PC-domain consumption. Input capacitor, ESD and VBUS divider are ahead of this link; use a USB input-current measurement for total PC-port draw. |
| JP3 | Fitted | Replace with a floating ammeter to measure the inline regulator/sensor branch. R10 remains in circuit. |
| JP4 | Not fitted | Forces isolator PC supply on for an external I²C master. Remove for normal firmware/suspend testing. R26 limits conflict with PA1. |

U4 derives sensor power from VBUS_A before the shunt. JP3 measures the main self-consumption branch; output-sense loading remains a separate small burden. The current 8 mA allocation is **not** a measured correction. Characterize actual draw over voltage, activity and temperature, including the measuring instrument's burden. See [energy comparison](../../docs/energy-comparison.md).

U7 switches U2 side 1 and its pull-ups using MCU PA1. The ISO1641 side-1 high-state maximum is 3.2 mA at 3.3 V, so simply sleeping the MCU would leave an excessive suspend burden. Before disabling U7, firmware releases PB6/PB7 and removes internal pull-ups; resume enables the rail and waits for settling before I²C. This circuit addresses the identified load; total USB suspend current still needs measurement.

## Bring-up sequence on this board

1. Review pin/footprint drawings and run KiCad ERC, then inspect assembly unpowered. Verify PC/inline isolation, both independent CC paths and no supply shorts. Leave OEM equipment disconnected.
2. Power J8 only. Establish 3V3_PC, reset/boot/SWD and USB enumeration. Verify PA1 can switch the isolator rail and that suspend removes its load. Sensor absence is a valid diagnostic state.
3. Use current-limited floating 3.3 V at J7 with JP1 on 2–3. Verify INA228 ID, raw readings, calibration commands and logging while VBUS is zero. This permits firmware work before an inline charger is attached.
4. Apply current-limited 5 V through qualified J2/J3 force wiring and a small known load. Verify polarity, the B voltage reference, one-second statistics and energy. Return JP1 to 1–2 and repeat with normal sensor power. Compare the JP3 measurement with the supply budget.
5. Sweep voltage and load for calibration. Increase core current toward 9 A only with rated force connections, monitored temperatures and an appropriately limited supply/load. The 10.8 A point needs an explicit continuous-capacity thermal test; it is not a brief survival pulse.
6. Qualify the actual captive assembly electrically and thermally, then compare direct versus inserted OEM charging across all orientations. Keep the controlled bench at known ≤28 V until overrange handling is resolved.

## Before PCB release

Select J1/P1, force terminals, strain relief, all footprints and passive voltage/power ratings. Verify the WSK2512's four terminals against its land drawing: the draft uses project numbering I1/I2/E1/E2, not an assumed vendor pad convention. Review USB port pad mapping, all IC exposed pads, unpowered pin behavior, USB timing/current and regulator thermals. Resolve inline ESD/overrange protection without compromising CC or low-power leakage. Route Kelvin senses and B-ground separately from force-current necks.

Regenerate with `python tools/capture_bench.py`; use `--check` to detect stale files. Its assertions check independent CC nets, no shared PC/inline nets and the MCU supply pins. These checks do not replace ERC, impedance/thermal layout work or hardware tests.
