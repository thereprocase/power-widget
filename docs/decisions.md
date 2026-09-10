# Decisions and open questions

2026-09-10. “Provisional” means a design candidate; “open” means the outcome is deliberately uncommitted.

## D01 — Captive baseline selected for bench; final topology OPEN

| Consideration | Captive male output | Two inline receptacles |
|---|---|---|
| Added cable | Controlled short assembly | Second user-selected cable |
| Cable discovery | Preserve the original cable's behavior; do not add an unexamined marker | Two cable identities and their power paths must be reconciled |
| Orientation | Carry both relevant CC/VCONN contact paths through the added assembly | Active CC contacts on the two cables may land on different receptacle contacts |
| Resistance | One fewer mating interface than the two-cable arrangement | Additional contacts and cable contribute loss |
| Service | Replace complete pigtail or its internal termination | Replace an external cable |
| Present preference | First bench prototype | Retained if proven practical and economical |

TI describes the roles of CC orientation, Rp/Rd, Ra, and VCONN in its [Type-C primer](https://www.ti.com/lit/wp/slyy109b/slyy109b.pdf). **Engineering inference:** joining two standard C-to-C cables is more involved than extending the contacts of one plug. Fixed CC1-to-CC1 routing cannot be assumed to connect the active CC conductor through every two-cable orientation. Sharing a CC bus between two independent marked cables also needs a cable-discovery analysis; do not presume there is a transparent way to merge their responses.

Close D01 only after producing an orientation truth table, checking actual pigtail wiring, comparing source/sink/cable PD traces with a direct baseline, and finding a buildable connector assembly. No shorting CC1 to CC2 as a workaround. No new inline Rp/Rd/Ra networks or e-marker impersonation. If option B needs a PD proxy that replaces the original negotiation, it fails the transparency requirement rather than quietly redefining it.

## D02 — Laptop current ceiling: 9 A TARGET / 10.8 A DESIGN

The user excluded extreme proprietary phone charging. The [dated laptop roster](manufacturer-modes.md) includes Lenovo's documented C170 20 V / 8.5 A mode. Apply the accepted rule: 8.5 + 0.5 = 9 A continuous; ×1.20 = 10.8 A design margin. Do not confuse Dell's separate fault current-limit figure with a charging mode.

This closes the numeric target for this roster, not physical qualification or universal brand compatibility. The 5 mΩ / 1 W shunt remains the baseline; 12.5 A phone-derived sizing is excluded. No generic USB-C connector receives a 9 A rating through this decision.

## D03 — Overrange behavior: OPEN before final hardware

A transparent device does not get to tell the endpoints its 28 V/current limit. EPR includes higher voltages; see TI's [TPS26750 EPR support](https://www.ti.com/lit/ds/symlink/tps26750.pdf). The instrument may encounter a higher contract without having requested it.

Evaluate an independent analog disconnect for overvoltage/overcurrent/overtemperature against the loss, cost, and power-role implications. Alternatively, qualify a wider survival envelope and document controlled bench use. A software alert is not protection; a shunt fuse rating is not a precise current ceiling. A low-voltage TVS must not become a sustained crowbar on a legitimate higher-voltage contract. No arbitrary protection component values are frozen yet. R01 remains unchanged in either case.

## D04 — Measurement: PROVISIONAL

INA228 with one 5 mΩ four-terminal shunt on VBUS. Use the **±163.84 mV ADC range** after the current-rule change; the narrower range clips at about 8.2 A and does not cover the larger design scenarios. Direct raw conversion and per-unit calibration retain useful low-current margin without autoranging. The 1 W WSK2512 candidate must be thermally qualified at 9 A and the 10.8 A margin point. INA238 remains a cost-down comparison conditional on a new error budget. No low-side shunt: keep inline ground continuous.

## D05 — Isolation and supply: PROVISIONAL

PC-powered USB MCU; inline-powered sensor; isolate I²C between them with ISO1641. No supply conductor crosses the barrier, so a dedicated isolated DC/DC is not required. An isolated PC-fed sensor supply remains an alternative if inline self-consumption, reverse-power accounting, or sequencing proves troublesome. No USB isolator in the main charging/data path.

## D06 — Accuracy and bandwidth: PROVISIONAL

Use nominal 17.28 ms fresh acquisitions and one-second software averages for normal logging, as requested. Allocate ±1 µV shunt noise at the final one-second DC result; demonstrate this on hardware without assuming correlated errors average away. The 0.54 s mode remains a calibration/diagnostic option. Validate pulsed-load energy separately because voltage and current are sequentially sampled. Confirm ambient range and the PCB_B reference plane before release.

## D07 — Product scope: PROVISIONAL

No built-in PD decoder or trigger. A separate suitably rated analyzer is a development instrument for compatibility validation. Preserve low-frequency/DC charging signatures as well as digital messages; do not attach the MCU to inline D+/D−. The bench retains SBU and each high-speed contact's continuity without claiming USB 3/video performance. Include USB-C-to-other-connector OEM cables in the survey: a captive USB-C output cannot physically mate with a MagSafe end, so some assemblies may require placing the monitor at the charger side. Recheck reference-plane and self-consumption accounting in that placement.

## D08 — Minimum VBUS / low-voltage programmable modes: OPEN

The 5–28 V accuracy study is an engineering assumption, not a user-imposed 5 V minimum. If the qualified charger roster includes operation below 5 V, extend the accuracy and supply-startup study. The present 3.3 V inline LDO output cannot be assumed to remain regulated down to an equally low VBUS. Evaluate a lower sensor-side rail within INA228/isolator limits, a different supply, or isolated PC-fed sensing. Passive communications may continue while sensing is unavailable; that does not satisfy a promised measurement range. Close this before releasing the operating-voltage specification.

## D09 — Full bench prototype: SELECTED

Replace the standalone continuity coupon with an accessible board containing the passive inline path, INA228, isolated I²C, PC reporting USB, an onboard USB MCU, SWD/UART/I²C access, force terminals, Kelvin probe points, and a selectable floating sensor supply. Firmware can start with a current-limited supply/load before high-current USB assemblies are qualified. Production size and enclosure constraints do not apply to this board. See the [captured bench circuit and bring-up sequence](../hardware/bench-rev-a/README.md).

## D10 — Energy diagnostic and transport: SELECTED baseline

Report measured V/I, calculated W and Wh using frequent samples and one-second time-weighted reports over USB serial. The PC may bridge to MQTT or HTTP. Preserve boot identity, time mapping, gaps and calibration provenance. Compare wall and laptop-input energy over matching intervals, accounting for downstream cable loss, board consumption and wall-plug uncertainty. PCB_B energy must not be mislabeled laptop-terminal energy. See [energy-comparison.md](energy-comparison.md).
