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

## D02 — Proprietary charging versus 6 A: OPEN

Keep the 6 A operating rating. Record exact charger, device, cable, labels, and negotiated modes before claiming brand compatibility. A **130 W mode at 20 V requires 6.5 A**; a 140 W mode at 20 V requires 7 A. Either exceeds R01, even though the component margin reaches 7.2 A. These are arithmetic examples, not a claim that every Dell or Lenovo charger uses those modes; exact OEM models and primary documentation remain to be collected.

If an essential OEM mode exceeds 6 A, explicitly choose between increasing the rating and excluding that mode. For example, 6.5 A plus 20% requires 7.8 A design capacity. Never force an OEM charger into such a mode with an arbitrary cable. A generic 5 A cable rating does not qualify 6 A operation.

## D03 — Overrange behavior: OPEN before final hardware

A transparent device does not get to tell the endpoints that it is rated for only 28 V / 6 A. EPR includes higher voltages; see TI's [TPS26750 EPR support](https://www.ti.com/lit/ds/symlink/tps26750.pdf). The instrument may encounter a higher contract without having requested it.

Evaluate an independent analog disconnect for overvoltage/overcurrent/overtemperature against the loss, cost, and power-role implications. Alternatively, qualify a wider survival envelope and document controlled bench use. A software alert is not protection; a shunt fuse rating is not a precise current ceiling. A low-voltage TVS must not become a sustained crowbar on a legitimate higher-voltage contract. No arbitrary protection component values are frozen yet. R01 remains unchanged in either case.

## D04 — Measurement: PROVISIONAL

INA228 with one 5 mΩ four-terminal shunt on VBUS. Direct raw voltage/current conversion in firmware, with per-unit calibration. This offers useful low-current margin without autoranging or a second current path. INA238 remains a cost-down comparison, conditional on a new error budget and calibration evidence. No low-side shunt: keep inline ground continuous.

## D05 — Isolation and supply: PROVISIONAL

PC-powered USB MCU; inline-powered sensor; isolate I²C between them with ISO1641. No supply conductor crosses the barrier, so a dedicated isolated DC/DC is not required. An isolated PC-fed sensor supply remains an alternative if inline self-consumption, reverse-power accounting, or sequencing proves troublesome. No USB isolator in the main charging/data path.

## D06 — Accuracy and bandwidth: PROVISIONAL

Qualify a settled precision mode first, with approximately 0.54 s acquisition windows. Offer a faster trend mode only with its own noise limits. The low-power accuracy requirement is not an oscilloscope specification. Confirm the proposed ambient range and accuracy plane before release.

## D07 — Product scope: PROVISIONAL

No built-in PD decoder or trigger. A separate suitably rated analyzer is a development instrument for compatibility validation. Preserve low-frequency/DC charging signatures as well as digital messages; do not attach the MCU to inline D+/D−. SBU and unused high-speed contacts remain part of the early routing investigation, not presumed unused vendor signals.
