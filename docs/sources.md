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
| S11 | [ST STM32F042x4/x6 datasheet](https://www.st.com/resource/en/datasheet/stm32f042f6.pdf) | Earlier MCU study, superseded by the F072 bench choice in S20. |
| S12 | [TI SN6505B datasheet](https://www.ti.com/lit/ds/symlink/sn6505b.pdf) | Transformer-driver alternative if sensing is powered across an isolation barrier; not the baseline. |
| S13 | [Infineon CY4500](https://www.infineon.com/evaluation-board/CY4500) | Historical passive PD-observer design precedent. Product page identifies end-of-life status; this is not an EPR/6 A qualification source. |
| S14 | [TI USB PD power negotiations, SLVA842](https://www.ti.com/lit/an/slva842/slva842.pdf) | Source/sink negotiation and trace comparison methodology; predates EPR. |
| S15 | [Lenovo Legion Slim 140W GX21M50625](https://www.lenovo.com/us/en/p/accessories-and-software/chargers-and-batteries/chargers/gx21m50625) | Public HTML's embedded specification was subsequently retrieved: 20 V / 7 A, 19.95 V / 5 A, and 5/9/15 V / 3 A. |
| S16 | [Lenovo Legion 5 15IRX10 PSREF](https://psref.lenovo.com/syspool/Sys/PDF/Legion/Legion_5_15IRX10/Legion_5_15IRX10_Spec.pdf) | Separates USB-C input from higher-power slim-tip adapter offerings; do not infer USB-C current from bundled adapter wattage. |
| S17 | [Bourns CSS4J-4026](https://www.bourns.com/docs/product-datasheets/css4j-4026.pdf) | Higher-power four-terminal shunt alternative; 5 mΩ is on-request and has a different TCR. Not selected; the active design retains WSK2512 for laptop scope. |
| S18 | [Dell 165 W USB-C GaN 450-BFTY](https://www.dell.com/zh-cn/shop/-165w-usb-c-gan-/apd/450-bfty/) | Manufacturer output table: 28 V / 5.893 A and 20 V / 6.5 A; separate fault current limit is not an operating mode. |
| S19 | [Lenovo C170 / LA170 official description](https://www.lenovo.com.cn/wiki/product-doc-46691.html) | 20 V / 8.5 A maximum and marked C-Slim cable; verify regional unit/AC-input conditions. |
| S20 | [ST STM32F072 datasheet DS9826 Rev 6](https://www.st.com/resource/en/datasheet/stm32f072cb.pdf) | F072CB LQFP48 pinout, USB/HSI48, I²C/UART/debug and 128 KB flash / 16 KB RAM. Bench pin map checked against figure 8 and alternate-function tables. |
| S21 | [TI TLV755P](https://www.ti.com/lit/ds/symlink/tlv755p.pdf) | PC 3.3 V regulator candidate and DBV pinout. |
| S22 | [ST USBLC6-2](https://www.st.com/resource/en/datasheet/usblc6-2.pdf) | SC6 paired USB data pins and reporting-port ESD topology. |
| S23 | [TI TPS22919](https://www.ti.com/lit/ds/symlink/tps22919.pdf) | SC70-6 load switch, ON control, output discharge and low off current; switches PC isolator supply. |
| S24 | [TI TPS25751](https://www.ti.com/product/TPS25751) | User-provided PD reference; this is a negotiating controller, not a selected transparent inline part. |
| S25 | [KiCad schematic format](https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/) | Native draft serialization reference; native KiCad 9 loading and ERC now pass; see bench reports. |
| S26 | [Apple 140 W adapter MW2M3AM/A](https://www.apple.com/shop/product/mw2m3am/a/140w-usb-c-power-adapter) | Adapter/cable recommendation; retrieved page did not expose an output-mode table. |

## Unresolved evidence

- Dell and Lenovo primary current-mode evidence now establishes the bounded laptop design target; exact Apple output modes need a unit label/trace. No OEM compatibility or private signaling implementation has been physically verified.
- Obtain exact charger/device/cable identifiers and original connection baselines. Label photographs plus OEM documentation and analyzer captures should establish the current and voltage actually in use.
- No connector or cable assembly has been qualified for the revised manufacturer-current rule and its margin. Generic 5 A parts remain unqualified for larger-current scenarios.
- No supply-chain price, inventory, or assembly quote is presented as verified. Cost tables are explicit planning allowances.
- No full current USB-C standard, OEM private schematic, physical-unit test, waveform capture, thermal image or calibration result is present. Manufacturer component datasheets were consulted for circuit capture. Model outputs and connection sheets are not bench evidence.

## Bench physical-design source additions

- [TI TPS7A43](https://www.ti.com/lit/ds/symlink/tps7a43.pdf): selected 85 V regulator, pin table, stability and DGQ land pattern. Supersedes S10 for U4.
- [GCT USB4115](https://gct.co/connector/usb4115), [USB4155](https://gct.co/connector/usb4155), [USB4105](https://gct.co/connector/usb4105): 48 V / 5 A ratings; **not 9 A**. Individual plug drawing retrieval was unsuccessful, so no mating-plug footprint is claimed.
- [Würth 691137710002](https://www.we-online.com/components/products/datasheet/691137710002.pdf): force-terminal ratings, pitch and drill.
- [Vishay SMBJ](https://www.vishay.com/docs/88392/smbj.pdf): clamp-coordination review; no TVS selected as universally protective.
- [Vishay WSK2512](https://www.vishay.com/docs/30108/wsk2512.pdf): 5 mΩ uses 1.19 mm termination variant; project pin mapping separates current and Kelvin pads.
