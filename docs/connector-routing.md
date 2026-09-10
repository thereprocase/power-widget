# Connector routing for bench revision A

## Decision

Use **one inline receptacle and a short custom captive male assembly** as the bench baseline. Keep the two-receptacle outcome open for a later proven topology. A fixed passive two-receptacle board with two ordinary C-to-C cables fails the independent-orientation requirement; it is not an interchangeable assembly option for this revision.

This resolves the logical baseline, not procurement or USB qualification. The pigtail needs two independent CC-contact conductors, no new marker, and no local CC terminations. An ordinary cut C-to-C cable is not a substitute: its VCONN contacts and marker circuitry need not form the required contact extension.

Contact functions and orientation are documented in [TI's Type-C primer, figures 13–14](https://www.ti.com/lit/wp/slyy109b/slyy109b.pdf). The map and conclusions below are our circuit analysis. No current USB-IF extension-cable compliance claim is made.

## Contact map

`J_A` is the inline receptacle; `P_B` the captive plug. Names are connector contact designations, **not mirrored solder-pad coordinates**. Verify mating-face drawings before assigning PCB pads.

| J_A contacts | Path | P_B contacts |
|---|---|---|
| A4, A9, B4, B9 | VBUS_A → four-terminal shunt → VBUS_B; parallel power contacts | A4, A9, B4, B9 |
| A1, A12, B1, B12 | Continuous low-resistance inline ground | A1, A12, B1, B12 |
| A5 / CC1 | Independent `CONTACT_A5` | A5 |
| B5 / CC2 | Independent `CONTACT_B5` | B5 |
| A6 and B6 | Join locally at receptacle; `INLINE_DP` | A6 / D+ |
| A7 and B7 | Join locally at receptacle; `INLINE_DM` | A7 / D− |
| A8 / SBU1 | Separate conductor | A8 |
| B8 / SBU2 | Separate conductor | B8 |
| A2, A3 | Preserve each contact as a pair | A2, A3 |
| A10, A11 | Preserve each contact as a pair | A10, A11 |
| B2, B3 | Preserve each contact as a pair | B2, B3 |
| B10, B11 | Preserve each contact as a pair | B10, B11 |
| Shell | Inline shield; separate from PC shell | Shell |

A normal plug has one USB 2.0 pair; P_B B6/B7 are not extra signal wires. Document any proposed nonstandard assembly before substituting it. Retaining the four SuperSpeed pairs preserves contact continuity; USB 3.x, video, and USB4 signal integrity are not promised. Route USB 2.0 at 90 Ω differential and keep observation pads small.

Neither `CONTACT_A5` nor `CONTACT_B5` has a permanently assigned CC-versus-VCONN role: original-cable orientation can exchange them. Route both for VCONN current and PD signaling. Do not connect them together, to VBUS, to an MCU, or to new Rp/Rd/Ra resistors. Do not add an e-marker. Original cable electronics and DC-coupled D+/D− signatures remain in circuit.

## Orientation analysis

Let `a` be the original cable plug's flip at J_A, and `b` the captive plug's flip at the endpoint. The active CC reaches endpoint CC1 if `a XOR b = 0`, otherwise CC2. The other contact remains separate; both endpoint CC positions are legitimate attachment orientations.

| a | b | Active J_A | Active endpoint | Other contact |
|---|---|---|---|---|
| 0 | 0 | CC1 | CC1 | Separate |
| 0 | 1 | CC1 | CC2 | Separate |
| 1 | 0 | CC2 | CC2 | Separate |
| 1 | 1 | CC2 | CC1 | Separate |

A detachable source-end plug adds another independent flip: eight physical combinations for a detachable C-to-C cable plus extension; four for a fixed charger lead. At charger-side placement, interchange endpoint roles and repeat VCONN-source and power-role checks. This proves connectivity only, not attach thresholds, marker power paths, cable discovery, or proprietary behavior.

For fixed F-F CC1→CC1 and CC2→CC2 wiring, both ordinary cable plugs must land their longitudinal CC conductors on the same contact. Two of four local flip combinations fail. A crossed map exchanges the failures. Manually switching them does not solve duplicated marked-cable identities or VCONN paths. No automatic mux or PD proxy is silently inserted.

The reproducible [orientation model](../analysis/orientations.md) enumerates the cases. It is not a USB-PD simulator.

## Assembly requirements

- Obtain a mating drawing and every-contact continuity report before powering. Check for hidden terminations, tied CC contacts, and extra markers.
- Start with 75 mm and ≥0.823 mm² copper per power polarity as resistance-study inputs. Qualify actual copper, insulation, strain relief, current sharing, and contacts; wire gauge alone is insufficient.
- Provide small probe pads on CC, USB 2.0, SBU, and retained pairs. Use a suitable high-impedance CC instrument. No inline signal connects to the reporting MCU.
- Force terminals exercise the sensing core while connector qualification proceeds. Bench injection and a live charger are mutually exclusive because terminals parallel the inline ports.
- Inline shells and probe grounds belong to the inline domain. SWD, UART, reporting USB, and PC-side I²C belong to the PC domain. Grounded instruments can bridge isolation externally.
- Compare original and inserted PD/cable traces and every orientation. A working 5 V attachment alone is insufficient.
