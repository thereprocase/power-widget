# Bench A physical-design review

The repository now contains an editable, routed **125 × 107 mm, four-layer bench PCB**, the native KiCad project, project symbol/footprint libraries, and reproduction scripts. It is an engineering prototype design, **not a fabrication release or a qualified 9 A USB product**.

## Native check results

KiCad **9.0.9**, checked with errors, warnings and exclusions included:

| Check | Result |
|---|---|
| Schematic ERC | **0 errors, 0 warnings** |
| PCB DRC | **0 violations** |
| PCB connectivity | **0 unconnected items** |
| Schematic/PCB parity | **0 mismatches** |
| Independent pin/net comparison | All **82 circuit footprints / 65 named circuit nets** agree with `circuit.json` |
| Retained routing replay | Import retained SES, apply documented manual repairs, refill: native DRC/parity remain clean |

Evidence: [ERC](../hardware/bench-rev-a/erc.rpt), [DRC including schematic parity](../hardware/bench-rev-a/drc.rpt), [pin/net review](../hardware/bench-rev-a/board-connectivity-review.json). Six mechanical footprints are board-only mounting/strain-relief holes. Six schematic supply flags are nonphysical. No electrical or physical rule violations are hidden by exclusions.

The native schematic was opened/exported and visually reviewed. Fixes included escaped root-sheet text, on-grid pin/wire endpoints, project library resolution and left-side net-label alignment. The PCB's top and bottom plots were inspected after routing. These checks establish CAD consistency; they do not measure accuracy, insertion loss, temperature or charging compatibility.

## Board arrangement and routing

- The upper domain contains the inline receptacle, captive-wire termination, 5 mΩ four-terminal shunt, force terminals, INA228 and its local supply. Force connections allow core testing without USB equipment.
- The lower domain contains USB reporting, STM32F072, SWD, UART/GPIO headers and RESET/BOOT/USER buttons. Current links and floating sensor-power selection remain accessible.
- A **3 mm copper keepout across every copper layer** separates the two domains. U2 is the only signal bridge. Ground pours remain separate; this is a functional isolation design, without a certified creepage/withstand claim.
- Candidate stack: 70 µm outer copper, 35 µm inner copper, nominal 1.6 mm total including mask. In1 carries the split reference plane with routed exceptions; B has separate ground pours, and the inline F layer has ground fill. The fabricator must approve the actual stack and tolerances.
- The force/shunt VBUS routes use 3 mm trunks with 1.8 mm transitions into the current pads. The return has a 4 mm trunk plus ground pours. The USB branch uses independent short fanouts from all four VBUS contacts; its narrower copper is for the **5 A populated USB variant**, not permission to operate the selected connector at 9 A.
- J1's communication signals use explicit 0.4 mm / 0.2 mm drilled via escapes. Their net class permits **0.1 mm inter-signal clearance**; ordinary nets retain 0.15 mm clearance and 0.15 mm tracks. Hole-to-copper clearance is 0.2 mm and copper-to-edge clearance 0.25 mm. Confirm these capabilities specifically with **2 oz outer copper** before ordering. This is a real fabrication constraint, not a DRC exemption.
- Four 3.2 mm mounting holes and two 3 mm captive-cable strain-relief holes are provided. Cable restraint and the selected force-terminal body still require mechanical first-article checks.

The retained routing session was produced with Freerouting 1.9.0 and single-threaded optimization. Native KiCad checks, rather than the router's completion message, determined acceptance. Manual repairs move two signal routes clear of J1's locating hole and remove a redundant ground-via stub; ground fills complete that connection. The commands are recorded in the [bench README](../hardware/bench-rev-a/README.md).

## Open release gates

1. **9 A USB assembly sourcing:** the selected GCT socket and candidate captive plug are rated 5 A aggregate VBUS. No primary-source-backed 9 A mating assembly has been selected. The exact captive plug drawing, both CC/VCONN paths, wiring and strain relief need review. See [connector selection](connector-selection.md).
2. **Power and measurement qualification:** test the force path at 9 A and its 10.8 A margin, including shunt derating, contact sharing and copper temperature. Reconcile measured insertion loss with the budget; the existing 14.879 mΩ hot-loop figure is an allocation, not extracted PCB resistance or a measurement. Establish the defined voltage plane, downstream conductor loss and board self-consumption.
3. **Voltage/protection and passive BOM:** the 85 V sensing regulator removes the former supply-voltage concern, but there is no qualified universal surge clamp, hardware current cutoff or full-EPR rating. Select actual capacitor MPNs using DC-bias/tolerance data and verify regulator stability, start-up and thermal performance. See [protection review](protection-review.md).
4. **USB behavior and fabricator review:** conductor continuity is captured and routed. USB 2.0 impedance, skew, return paths, hot-plug/ESD and actual OEM negotiation are not qualified by DRC. Review/tune the routing against the fabricator's stack and test USB performance and all required orientations before release.

The firmware pin contract is now tied to a native board suitable for further bench development planning. Firmware implementation, fabrication, assembly and physical tests have not been performed in this checkpoint.

## Views

[Top copper with component labels](../hardware/bench-rev-a/pcb-top.svg) and [bottom copper with top-side labels for location reference](../hardware/bench-rev-a/pcb-bottom.svg). Both views look from the top; the bottom plot is not mirrored and is not an assembly drawing.
