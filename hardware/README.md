# Hardware status

**Architecture study only. No schematic, PCB, Gerbers, pick-and-place files, or purchase-ready BOM.**

Start with the [architecture](../docs/architecture.md), [open decisions](../docs/decisions.md), [manufacturer-current rule](../docs/manufacturer-modes.md), and [validation gates](../docs/validation-plan.md).

Suggested schematic sheets after the gates close:

1. Inline connectors, CC/VCONN/data routing, power path and fault handling.
2. Kelvin shunt, sensor, local regulator and isolated I²C side 2.
3. Reporting USB-C, MCU, local regulator, isolated I²C side 1 and PC-side debug.

Use a reproducible native KiCad project when circuit capture begins. Review symbols and footprints against manufacturer drawings; do not trust library pin numbers for USB-C plugs, mirrored views, or current-sense resistors without checking. Treat the pigtail as an electrical assembly with its own drawing and test specification.

Keep the present 1 W shunt as a **9 A analysis candidate only**. Larger current envelopes may require a different resistor package, new TCR/noise budgeting, and a larger thermal floorplan. No generic USB-C connector has been qualified for the revised rating.
