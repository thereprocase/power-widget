# Progress and handoff

## 2026-09-10 — Requirements and design planning

The user requested questions first, then a design brief before research. They replaced the original 10 A/full-EPR scope with 28 V / 6 A plus 20% margin, specified USB 2.0, isolated PC reporting, low-power accuracy, and a cheap-but-good build. They added vendor-specific charging transparency. Connector topology remains open: they lean toward captive male and explicitly allow either that or two receptacles.

The user authorized initialization and ongoing checkpoints in this repository. The existing repository was empty. Its visibility was private and has been retained.

- Requirements checkpoint: `3717ae99631b06e8b059001d02c9f6f5ece083c5`.
- Primary-source checks established a provisional INA228 / 5 mΩ / isolated-I²C architecture.
- Connector topology, higher-current OEM modes, and overrange behavior remain release gates.
- Initial research could not establish exact OEM proprietary signaling or source connector assemblies. Those gaps are explicitly recorded in `sources.md`.

## Requirement change during planning

The user replaced the 6 A rating with **half an amp above the applicable manufacturer current modes**. The retained 20% margin is applied after adding 0.5 A. Numeric OEM maximum remains unresolved; current manufacturer retrieval did not establish it. The analysis now uses explicit scenarios, principally 9 A continuous / 10.8 A design, without presenting that as a verified requirement.

The larger current scenarios changed the proposed ADC range to ±163.84 mV, prompted a shorter/thicker pigtail resistance allocation, and exposed the 1 W shunt's limit in the 12.5 A / 15 A-design scenario. The current sensor and isolated-I²C architecture remain provisional.

Architecture checkpoint: `3a62ac91781fd497afed0c893fcbd64117126e75`.

## Planning package

- Deterministic budget tool and generated Markdown/JSON/CSV results; all assumptions are explicit.
- Manufacturer-current rule and evidence gaps; both connector outcomes remain available.
- Calibration, qualification, prototype sequence, protocol draft, and cost allowances.
- No schematic, PCB, firmware binary, or tested hardware exists at this stage.
- Numerical verification: 19,635 points in the provisional 9 A study; worst allocated precision errors 0.874% at 5 W and 4.539% at 0.5 W, both at 28 V. Deterministic outputs reproduce; local document links resolve; no whitespace errors found.
- A lower-than-5 V measurement range remains an explicit supply/qualification question; the initial sweep does not claim to cover every programmable charger voltage.

## Immediate next steps after this package

1. Obtain current-mode evidence for exact target OEM combinations and close the numeric rating; no global maximum has been claimed.
2. Build the connector feasibility fixture and verify CC/VCONN/e-marker behavior across orientations. Prefer captive male if it passes; retain two receptacles as an allowed outcome.
3. Resolve fault handling and measurement-plane choices.
4. Evaluate the sensing core with a current-limited source/load, then capture a schematic after the gates close.
