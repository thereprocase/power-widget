# Research record

Checked 2026-09-10. Primary manufacturer and standards-body material only. Links are references, not redistributed copies of third-party documents. Calculated budgets and architecture choices are our engineering analysis.

| ID | Source | What it establishes / limitation |
|---|---|---|
| S01 | [USB-IF Type-C release 2.5 landing page](https://www.usb.org/document-library/usb-type-cr-cable-and-connector-specification-release-25) | Current page identifies release 2.5, dated April 2026. The full downloadable text was not retrieved; exact current normative topology clauses remain an open research item. |
| S02 | [TI Type-C and PD primer, SLYY109B](https://www.ti.com/lit/wp/slyy109b/slyy109b.pdf) | CC orientation and termination roles, VCONN powering cable electronics, and USB 2.0/PD paths. Legacy discussion is not the source for current EPR limits. |
| S03 | [TI TPS26750 datasheet](https://www.ti.com/lit/ds/symlink/tps26750.pdf) | EPR includes 28, 36, and 48 V and AVS. This negotiating controller is a protocol reference, not a selected inline component. |
| S04 | [TI INA228 datasheet, SLYS021A](https://www.ti.com/lit/ds/symlink/ina228.pdf) | Tables/sections 6.5, 8.1.3, 8.1.4: offset and drift, bus error, quantization, noise versus timing, and input filtering. |
| S05 | [TI INA228 product page](https://www.ti.com/product/INA228) | Active product, packaging, INA238/INA229 alternatives. No usable current unit-price quote was returned. |
| S06 | [TI INA238 datasheet](https://www.ti.com/lit/ds/symlink/ina238.pdf) | Lower-cost performance comparison; larger offset and coarser resolution must be re-budgeted. |
| S07 | [TI INA226 datasheet](https://www.ti.com/lit/ds/symlink/ina226.pdf) | 36 V sensor alternative; little voltage headroom above 33.6 V and less attractive low-power budget. |
| S08 | [Vishay WSK2512 datasheet, document 30108](https://www.vishay.com/docs/30108/wsk2512.pdf) | Four-terminal resistor, value/tolerance ordering, finished-part TCR, derating and land-pattern ranges. Supplier stock for the proposed code is not verified. |
| S09 | [TI ISO164x datasheet, SLLSFC2D](https://www.ti.com/lit/ds/symlink/iso1641.pdf) | Supply separation, channel direction, I²C logic constraints, supply-current data, and package-specific insulation. |
| S10 | [TI TPS7A16 datasheet](https://www.ti.com/lit/ds/symlink/tps7a16.pdf) | 60 V regulator family, adjustable output, supply current, thermal and stability constraints. |
| S11 | [ST STM32F042x4/x6 datasheet](https://www.st.com/resource/en/datasheet/stm32f042f6.pdf) | USB full-speed MCU family candidate. Pin allocation and USB firmware/VID/PID choices are not complete. |
| S12 | [TI SN6505B datasheet](https://www.ti.com/lit/ds/symlink/sn6505b.pdf) | Transformer-driver alternative if sensing is powered across an isolation barrier; not the baseline. |
| S13 | [Infineon CY4500](https://www.infineon.com/evaluation-board/CY4500) | Historical passive PD-observer design precedent. Product page identifies end-of-life status; this is not an EPR/6 A qualification source. |
| S14 | [TI USB PD power negotiations, SLVA842](https://www.ti.com/lit/an/slva842/slva842.pdf) | Source/sink negotiation and trace comparison methodology; predates EPR. |

## Unresolved evidence

- Searches did not produce usable primary OEM current-mode documentation in this session. Several Dell pages could not be retrieved. No Apple/Dell/Lenovo protocol, wiring, or compatibility has therefore been declared verified.
- Obtain exact charger/device/cable identifiers and original connection baselines. Label photographs plus OEM documentation and analyzer captures should establish the current and voltage actually in use.
- No connector or cable assembly with documented 6 A continuous service and the requested margin has been selected. Generic 5 A parts remain unqualified for that requirement.
- No supply-chain price, inventory, or assembly quote is presented as verified. Cost tables are explicit planning allowances.
- No downloaded standards text, reference schematic, physical unit, waveform capture, thermal image, or calibration result is present yet. A model output is not bench evidence.
