# Progress and handoff

## 2026-09-10 — Requirements and design planning

The user requested questions first, then a design brief before research. They replaced the original 10 A/full-EPR scope with 28 V / 6 A plus 20% margin, specified USB 2.0, isolated PC reporting, low-power accuracy, and a cheap-but-good build. They added vendor-specific charging transparency. Connector topology remains open: they lean toward captive male and explicitly allow either that or two receptacles.

The user authorized initialization and ongoing checkpoints in this repository. The existing repository was empty. Its visibility was private and has been retained.

- Requirements checkpoint: `3717ae99631b06e8b059001d02c9f6f5ece083c5`.
- Primary-source checks established a provisional INA228 / 5 mΩ / isolated-I²C architecture.
- Connector topology, higher-current OEM modes, and overrange behavior remain release gates.
- Initial research could not establish exact OEM proprietary signaling or source connector assemblies. Those gaps are explicitly recorded in `sources.md`.

## Immediate next steps

1. Complete reproducible numerical budgets and calibration/test plan.
2. Checkpoint the full planning package.
3. Start a connector feasibility fixture and obtain exact target charger/device/cable identities before freezing USB-C routing.
4. Evaluate the sensing core with a current-limited source/load separately from charging compatibility.

No schematic, PCB, firmware binary, or tested hardware exists at this stage.
