# Decisions and open questions

2026-09-10. “Provisional” means a design candidate; “open” means the outcome is deliberately uncommitted.

## D01 — Connector topology: OPEN, leaning captive male

| Consideration | Captive male output | Two inline receptacles |
|---|---|---|
| Added cable | Controlled short assembly | Second user-selected cable |
| Cable discovery | Preserve the original cable's behavior; do not add an unexamined marker | Two cable identities and their power paths must be reconciled |
| Orientation | Carry both relevant CC/VCONN contact paths through the added assembly | Active CC contacts on the two cables may land on different receptacle contacts |
| Resistance | One fewer mating interface than the two-cable arrangement | Additional contacts and cable contribute loss |
| Service | Replace complete pigtail or its internal termination | Replace an external cable |
| Present preference | First feasibility coupon | Retained if proven practical and economical |

TI describes the roles of CC orientation, Rp/Rd, Ra, and VCONN in its [Type-C primer](https://www.ti.com/lit/wp/slyy109b/slyy109b.pdf). **Engineering inference:** joining two standard C-to-C cables is more involved than extending the contacts of one plug. Fixed CC1-to-CC1 routing cannot be assumed to connect the active CC conductor through every two-cable orientation. Sharing a CC bus between two independent marked cables also needs a cable-discovery analysis; do not presume there is a transparent way to merge their responses.

Close D01 only after producing an orientation truth table, checking actual pigtail wiring, comparing source/sink/cable PD traces with a direct baseline, and finding a buildable connector assembly. No shorting CC1 to CC2 as a workaround. No new inline Rp/Rd/Ra networks or e-marker impersonation. If option B needs a PD proxy that replaces the original negotiation, it fails the transparency requirement rather than quietly redefining it.

## D02 — Manufacturer current ceiling: RULE SET; NUMBER OPEN

The user changed the rule during planning: **I_rated = I_manufacturer,max + 0.5 A; I_design = 1.20 × I_rated**. The 6 A requirement is obsolete. Record exact charger, device, cable, labels, and negotiated modes before determining the maximum or claiming brand compatibility.

For example, a verified maximum of 7 A would yield 7.5 A rated and 9 A design; 8.5 A would yield 9 A rated and 10.8 A design. These are conditional calculations, not verified OEM maxima. The [survey and scenario table](manufacturer-modes.md) keep the distinction explicit.

Continue circuit analysis at a provisional 9 A scenario and examine a 12.5 A scenario. This is allowed to inform component choices without silently freezing a numeric requirement. A generic 5 A cable does not acquire a higher rating because the monitor or an OEM protocol can carry more current. Qualification must include connector current sharing and the matched cable assembly.

## D03 — Overrange behavior: OPEN before final hardware

A transparent device does not get to tell the endpoints its 28 V/current limit. EPR includes higher voltages; see TI's [TPS26750 EPR support](https://www.ti.com/lit/ds/symlink/tps26750.pdf). The instrument may encounter a higher contract without having requested it.

Evaluate an independent analog disconnect for overvoltage/overcurrent/overtemperature against the loss, cost, and power-role implications. Alternatively, qualify a wider survival envelope and document controlled bench use. A software alert is not protection; a shunt fuse rating is not a precise current ceiling. A low-voltage TVS must not become a sustained crowbar on a legitimate higher-voltage contract. No arbitrary protection component values are frozen yet. R01 remains unchanged in either case.

## D04 — Measurement: PROVISIONAL

INA228 with one 5 mΩ four-terminal shunt on VBUS. Use the **±163.84 mV ADC range** after the current-rule change; the narrower range clips at about 8.2 A and does not cover the larger design scenarios. Direct raw conversion and per-unit calibration retain useful low-current margin without autoranging. The shunt package must be requalified against the final current; the 1 W WSK2512 candidate is only retained for the 9 A study. INA238 remains a cost-down comparison conditional on a new error budget. No low-side shunt: keep inline ground continuous.

## D05 — Isolation and supply: PROVISIONAL

PC-powered USB MCU; inline-powered sensor; isolate I²C between them with ISO1641. No supply conductor crosses the barrier, so a dedicated isolated DC/DC is not required. An isolated PC-fed sensor supply remains an alternative if inline self-consumption, reverse-power accounting, or sequencing proves troublesome. No USB isolator in the main charging/data path.

## D06 — Accuracy and bandwidth: PROVISIONAL

Qualify a settled precision mode first, with approximately 0.54 s acquisition windows. Offer a faster trend mode only with its own noise limits. The low-power accuracy requirement is not an oscilloscope specification. Confirm the proposed ambient range and accuracy plane before release.

## D07 — Product scope: PROVISIONAL

No built-in PD decoder or trigger. A separate suitably rated analyzer is a development instrument for compatibility validation. Preserve low-frequency/DC charging signatures as well as digital messages; do not attach the MCU to inline D+/D−. SBU and unused high-speed contacts remain part of the early routing investigation, not presumed unused vendor signals. Include USB-C-to-other-connector OEM cables in the survey: a captive USB-C output cannot physically mate with a MagSafe end, so some assemblies may require placing the monitor at the charger side. Recheck reference-plane and self-consumption accounting in that placement.

## D08 — Minimum VBUS / low-voltage programmable modes: OPEN

The 5–28 V accuracy study is an engineering assumption, not a user-imposed 5 V minimum. If the qualified charger roster includes operation below 5 V, extend the accuracy and supply-startup study. The present 3.3 V inline LDO output cannot be assumed to remain regulated down to an equally low VBUS. Evaluate a lower sensor-side rail within INA228/isolator limits, a different supply, or isolated PC-fed sensing. Passive communications may continue while sensing is unavailable; that does not satisfy a promised measurement range. Close this before releasing the operating-voltage specification.
