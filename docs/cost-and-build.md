# Cost and build plan

These are engineering allowances for a small prototype batch, **not supplier quotes or verified stock prices**. The larger-current connector/pigtail assembly and final fault circuit are the largest unresolved costs.

| Block | Provisional choice | Allowance per instrument, USD |
|---|---|---|
| Sensor | INA228 | 3.50–7.00 |
| Shunt | Four-terminal 5 mΩ, provisional WSK2512 | 1.00–3.00 |
| Isolation | ISO1641 | 2.00–4.00 |
| USB MCU | STM32F042 candidate | 1.50–4.00 |
| Two local supplies | Inline high-voltage LDO; PC LDO | 1.50–4.00 |
| Reporting receptacle | USB-C, USB 2.0 | 0.50–1.50 |
| Inline connector and pigtail | Assembly not selected or qualified | 3.00–12.00 |
| Signal protection and passives | Parts pending pin/protection design | 2.00–5.00 |
| PCB share | Small four-layer panel | 2.00–6.00 |
| Assembly/rework share | Small prototype batch | 5.00–20.00 |
| Enclosure/strain relief | Simple printed or machined enclosure | 2.00–6.00 |
| Fault-circuit allowance | Architecture open | 2.00–8.00 |
| **Planning total** | **Conditional on finding a suitable assembly** | **26.00–80.50** |

Exclude shipping, taxes, engineering time, calibration labor, reference equipment, analyzer purchase, and custom cable tooling/minimum-order charges. The table is not a promise that a specialized high-current cable can be bought in single quantities within the allowance. A 12.5 A scenario could move both the shunt and connector costs materially.

## Cost decisions

- Keep one precision shunt path; avoid range-switch MOSFETs and separate low/high-current paths unless measured results force them.
- Isolate the sensor interface and use independent local supplies. This avoids a USB isolator and isolated-power transformer in the baseline.
- Spend on contacts, Kelvin layout, and calibration. A cheap sensor substitution is not worthwhile if it increases losses or requires complicated calibration to meet the 0.5 W requirement.
- Price INA238 only after demonstrating an acceptable replacement budget. A compatible package is not equivalent accuracy.
- Start with a cabled bench prototype and a simple enclosure. Miniaturize after the current ceiling and thermal results are known.

## Work sequence

| Milestone | Deliverable | Completion gate |
|---|---|---|
| M0 — current phase | Requirements, provisional architecture, numerical tools, test and cost plans | Package checkpointed and internally consistent |
| M1 — topology | Connector coupon, OEM mode roster, pigtail/connector sourcing specification | Transparent baseline comparison; finalized current rule input |
| M2 — sensing | Sensor/isolation evaluation, calibration implementation, measured noise | Precision target met at low and high power |
| M3 — integrated PCB | KiCad schematic/layout, BOM, firmware and logger | Circuit review and manufacturing outputs agree |
| M4 — qualification | Thermal, protection, compatibility, USB and isolation records | Declared rating and accuracy supported by evidence |
| M5 — orderable prototype | Tagged build with source and manufacturing files | Latest practical build is prominent in README |

Checkpoint each milestone and meaningful intermediate change. Keep old designs in git history/tags while the README points to the most mature build. Do not label a planning document as an orderable prototype.
