# Prototype and validation plan

No physical tests have been run. Keep every result tied to board revision, firmware revision, calibration ID, cable IDs, fixtures, and ambient conditions.

## Stage 0 — Close the requirements that drive hardware

| Gate | Work | Evidence to close |
|---|---|---|
| G0.1 | Numeric laptop target closed: 8.5 + 0.5 = 9 A; ×1.20 = 10.8 A | Primary roster documented; actual unit labels and physical capacity still require checks |
| G0.2 | Compare captive male and two-receptacle topology | Pin/contact map, orientation table, marker/VCONN analysis, purchasable assembly |
| G0.3 | Define overvoltage, overcurrent, and hot-connector response | Concrete protection/survival architecture and component coordination |
| G0.4 | Fix accuracy plane, ambient range, and timing | Clear calibration and acceptance limits; cable loss explicitly assigned |
| G0.5 | Establish minimum VBUS and programmable charging coverage | Regulator/sensor operation and accuracy at the required low-voltage endpoint |

## Stage 1 — Integrated bench board and transparent path

Use the [full bench A circuit](../hardware/bench-rev-a/README.md), including MCU, isolated sensor, force terminals and debug headers. Review native schematic/footprints/ERC before PCB release. Develop firmware with floating sensor power and current-limited force wiring while connector sourcing proceeds. Verify all contact wiring with power absent, then use qualified assemblies for USB/OEM tests.

Capture a direct charger/cable/device baseline, then insert the bench monitor. An external PD analyzer must be rated for the voltage/current under test; older reference analyzers are not automatically suitable. Do not add a trigger board that negotiates in place of the device.

| Test family | Cases | Acceptance |
|---|---|---|
| Orientation | Every independently reversible plug at every receptacle; label each position | Same usable power modes and required data operation as baseline |
| Cable identification | Unmarked low-current cable, appropriate marked cable, EPR cable, OEM-specific cable | Expected identities/responses preserved; no false increase in cable capability |
| Startup | PC before/after power, source before/after sink, dead-battery device | No new attach failure or unintended VBUS source |
| PD behavior | Discovery, contract selection, reset, detach; supported power and VCONN swaps | No altered identity or contract, no introduced persistent failures |
| OEM charging | Exact Apple/Dell/Lenovo and other qualified roster combinations | Original intended charger identification and charging mode retained |
| USB 2.0 | Low/full/high-speed devices as relevant; bulk transfer integrity | Enumeration and transfers comparable to baseline at tested lengths |
| D+/D− charging signatures | Relevant legacy/proprietary charging sources | Analog signatures and successful charging behavior preserved |
| Alternate cable ends | OEM USB-C-to-MagSafe or other power cables, if in roster | Correct physical placement; no unsupported adapter chain |
| Reporting | PC connect/disconnect, MCU reset, USB suspend/resume | Normal inline charging/data continue; logging state changes are explicit |

For a C-to-C source cable plus captive plug there can be three independently reversible mating locations; test all eight binary combinations when each is independently accessible. Two separate C-to-C cables can create four locations and up to sixteen combinations. Derive the actual fixture matrix rather than testing only one “flipped” state. A topology that works only in some orientations does not close G0.2.

## Stage 2 — Sensing core and calibration

Evaluate the same board through J2/J3 current-limited force connections while connector work proceeds; keep USB power paths disconnected during independent injection. Use Kelvin references at the declared B-side plane. Select reference equipment with a combined uncertainty small enough to resolve the target; aim for ≤0.2% reference power uncertainty for the 1% acceptance region. Record actual equipment specifications and ranges.

1. Inspect soldering and sense routing; verify no reporting-to-inline conductive path. Check the main return is continuous and the PC port cannot backfeed VBUS.
2. Verify regulator startup, no-input state, sensor ID, I²C levels, and PC enumeration. Test each domain powered alone; “input unavailable” must not be reported as a valid zero-watt reading.
3. Warm the instrument and calibrate voltage at 5 V and 28 V. Fit and store offset/gain with reference readings.
4. Establish current offset with the external output genuinely open at multiple VBUS values. Account for meter input/protection leakage. Never silently tare while a real load is attached.
5. Calibrate current at low and high reference levels; verify intermediate points rather than fitting every acceptance point. Include both signs if signed operation is released.
6. Verify 0.5 W, 1 W, just below 5 W, exactly 5 W, intermediate load, and rated current at 5/9/15/20/28 V. Do not demand rated power at a lower voltage if it exceeds rated current.
7. Repeat at proposed ambient extremes and after high-current warm-up. Record shunt, sensor, regulator, contact, and enclosure temperatures independently; sensor die temperature is not contact temperature.

Acceptance uses absolute error relative to the reference: ≤1% at ≥5 W; ≤5% from 0.5 W to below 5 W, for settled one-second logging records within the qualified envelope. Guardband for reference uncertainty. Characterize a population of units before turning a design allocation into a guaranteed specification.

## Stage 3 — Current, thermal, and fault qualification

Use connectors/fixtures qualified for the intended test current. Increase current in controlled steps while monitoring each power-contact region. Test normal rated current continuously to thermal equilibrium at the proposed upper ambient. Suggested equilibrium definition: less than 1°C change over ten minutes; extend the run if conditions are still drifting. Record actual criteria rather than claiming a fixed soak time always suffices.

Verify the additional hot loop resistance against the selected topology budget. For the present captive scenario the target is 15 mΩ. Retest after mating cycles and cable flexing. Establish acceptance limits from connector, wire, PCB, resistor, and enclosure specifications, including touch temperature and solder-joint limits.

The 20% current point is a **design-capacity qualification gate**, with duration and component derating set explicitly. A short survival pulse does not establish continuous margin. Fault testing must verify the chosen hardware response with the PC disconnected and MCU stalled. Do not test an unqualified generic USB cable above its rating.

## Stage 4 — Isolation, reporting, and energy

- Check barrier continuity with every shield, enclosure fastener, debug lead, and PC connector installed. Set working/withstand tests after the final insulation geometry and parts are chosen.
- Test USB suspend, reconnect, dropped records, application exit, sensor NACK, and MCU reset. No backfeed or silent energy accumulation across missing intervals.
- Compare steady and pulsed-load energy against a calibrated reference over matched intervals. Test boundary crossings and voltage transitions; characterize sequential-sampling and internal-averaging error.
- Verify approximately 58 fresh pairs/s, one-second time-weighted V/I/P reports, mean-of-products power, fractional Wh integration, complete/partial coverage and signed reversals.
- Measure JP3 self-consumption over voltage/activity/temperature. Use full reporting-port current for PC-domain accounting and suspend validation; JP2 alone excludes front-end loads.
- Verify any downstream cable correction with actual cold/hot assembly resistance and a terminal-level reference. Include the wall plug's energy quantization, sampling behavior and timestamp uncertainty.
- Keep firmware elapsed time independent of host scheduling. Confirm the timebase and timestamp uncertainty. Wh logging and matched-interval comparison are required; no separate numerical dynamic-energy guarantee is yet established.

Follow the [energy accounting and uncertainty method](energy-comparison.md); no subtraction result is conclusive unless it exceeds the combined uncertainty.

## Release conditions

All Stage 0 gates closed; schematics and layout reviewed; reproducible build artifacts; calibration method and compatibility roster published; power/thermal/isolation results attached. Only then label a hardware revision orderable. There are currently no Gerbers, manufacturing files, or purchase-ready BOM.
