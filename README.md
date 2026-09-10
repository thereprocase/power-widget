# Power Widget

An inline USB-C power monitor with an isolated USB connection for PC reporting.

**Status:** requirements captured; design and feasibility planning started on 2026-09-10. No schematic, PCB, or tested hardware exists yet.

## Design brief

- Rated pass-through: **28 V, 6 A continuous (168 W)**.
- Electrical design margin: at least **33.6 V and 7.2 A**, with thermal and transient derating considered separately. Margin is not an operating rating.
- Preserve charging negotiation and charger/cable identity between the original source and load, including vendor-specific Apple, Dell, and Lenovo behavior where supported by the validated signal path.
- USB 2.0 pass-through; no requirement for USB 3, USB4, or video.
- Report voltage, current, power, and accumulated energy. Prefer signed, bidirectional current and power.
- Power accuracy target: **±1% of reading at 5 W and above; ±5% from 0.5 W to below 5 W**, across the rated voltage range.
- Third USB-C receptacle on a long enclosure edge provides PC reporting with galvanically isolated data, power, and ground.
- PC connection and inline power may be required for measurement; no display, battery, or standalone logging required.
- Cost objective: cheap but good. Spend on connector reliability, low loss, measurement quality, and practical calibration.

## First open decision: connector topology

**Open; preference is a short captive USB-C male pigtail on the load side. Both outcomes remain allowed.**

1. Source-side USB-C receptacle, captive male output, separate PC receptacle.
2. Two inline USB-C receptacles, separate PC receptacle.

Choose after checking CC/VCONN continuity, e-marker behavior, plug orientations, proprietary charging, assembly sourcing, resistance, and cost. A captive plug simplifies the assembly but does not by itself prove transparent charging. Do not freeze connector pin routing before this gate.

## Plan

1. Research the charging and cable topology, including limits of 28 V / 6 A compatibility.
2. Compare measurement and isolation architectures; select provisional components.
3. Build explicit accuracy, resistance/heating, and cost budgets.
4. Define calibration, PC reporting, prototype sequence, and acceptance tests.
5. Checkpoint the design package here before schematic/layout work.

The original 10 A/full-EPR request was superseded by 28 V / 6 A. Charging compatibility is a validation objective, not a claim that every USB-C charger/cable/device combination will work. Components rated above 28 V do not make this a full-EPR instrument.
