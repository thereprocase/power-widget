# Cost and build plan

These are rounded engineering allowances for a small bench batch, **not supplier quotes or verified stock prices**. Custom cable tooling/minimum orders and the unresolved fault circuit can dominate cost.

| Block | Bench candidate | Allowance per board, USD |
|---|---|---|
| Sensor | INA228 | 3.50–7.00 |
| Shunt | Four-terminal WSK2512, 5 mΩ | 1.00–3.00 |
| Isolation | ISO1641 | 2.00–4.00 |
| USB MCU | STM32F072CBT6 | 2.00–5.00 |
| Two local supplies | TPS7A16 / TLV75533 | 1.50–4.00 |
| Isolator supply switch | TPS22919 | 0.20–1.00 |
| Reporting receptacle | USB-C, USB 2.0 | 0.50–1.50 |
| Inline connector and pigtail | Assembly not sourced/qualified | 3.00–12.00 |
| Force/debug connectors and controls | Terminals, SWD, UART, GPIO, jumpers, buttons | 4.00–12.00 |
| ESD and passives | Final packages pending | 2.00–5.00 |
| PCB share | Accessible four-layer bench board | 6.00–15.00 |
| Assembly/rework share | Small prototype batch | 8.00–30.00 |
| Base/strain relief | Simple printed base and hardware | 2.00–6.00 |
| Fault-circuit allowance | Architecture open | 2.00–8.00 |
| **Rounded planning total** | **Conditional on suitable assemblies** | **38–114** |

Exclude shipping, taxes, engineering and calibration labor, reference equipment, analyzer/debug probe, and custom cable tooling. No promise is made that a qualified high-current assembly is available in single quantities within its allowance. Obtain quotes after the component schedule becomes an orderable BOM.

Use one precision shunt path and independent local supplies with isolated I²C. Spend on contacts, Kelvin routing and calibration. The F072's flash/RAM and exposed debug access support firmware iteration. Miniaturize and consider a cheaper sensor only after noise, thermal and energy behavior are measured.

## Work sequence

| Milestone | Deliverable | Completion gate |
|---|---|---|
| M0 — definition | Laptop roster, current rule, logical contact map and budgets | Checkpointed; physical compatibility remains open |
| M1 — bench capture | Complete sensing/MCU/debug circuit, connector specification and firmware contract | Draft captured; native KiCad/ERC, footprint and sourcing review next |
| M2 — bench PCB and firmware | Accessible board, INA228 driver, serial logger and calibration workflow | Low-voltage force-input bring-up; one-second/Wh behavior verified |
| M3 — measurement and assemblies | Noise/accuracy/energy results, qualified captive hardware | DC targets and declared dynamic limits supported; added loss and current tested |
| M4 — qualification | Protection, OEM orientations, USB and isolation records | Declared rating and compatibility backed by evidence |
| M5 — practical build | Tagged source, BOM and manufacturing package | Reproducible, reviewed fabrication release linked prominently in README |

The tiny continuity-board milestone is replaced by the full bench prototype. Connector tests and firmware work proceed on that platform; no production enclosure constraint applies yet. Checkpoint each meaningful change and retain previous designs in git history.
