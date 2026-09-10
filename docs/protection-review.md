# Bench voltage and protection review

## Decision

Use an **85 V TPS7A4333DGQR fixed 3.3 V regulator** for the inline sensing branch instead of TPS7A1601. Preserve a passive main power path. Do not fit a 33 V/36 V TVS across VBUS: it can conduct during an otherwise valid higher-voltage PD contract, which this monitor must not interfere with. No main-path cutoff or PD renegotiation circuit is introduced.

This resolves the schematic architecture choice; it does **not** establish qualified surge protection or full EPR operation. The target for accuracy/continuous operation remains 5–28 V. The selected USB connector population's published 48 V rating must not be treated as a verified 50.4 V or transient rating. Higher-contract, hot-plug and source-fault testing remain release gates.

## Circuit changes and checks

- U4: TPS7A4333DGQR, 4–85 V input, fixed 3.3 V output. EN is intentionally floating, using the datasheet's internal pull-up. **Do not connect EN directly to high VBUS**; its operating limit is lower than IN.
- MVSEL1 and MVSEL2 tied to inline ground select a nominal 15 V intermediate rail. Both NC pins and the unused PG output remain unconnected. Exposed pad 11 is inline ground.
- R10: 10 Ω / 0.25 W branch resistor. At the provisional 8 mA inline draw its drop is 80 mV and dissipation is 0.64 mW, leaving supply headroom at a 5 V input.
- C6: 1 µF / 100 V X7R input reservoir; C2: 10 nF / 100 V VBUS-filter capacitor. These see the high-voltage supply. C1 is 100 nF / 100 V differential, without a connection to PC ground.
- C7: 2.2 µF / 10 V output. C20/C21: two 22 µF / 50 V X7R intermediate-rail capacitors. The datasheet requires effective intermediate capacitance at least three times the effective total OUT-connected capacitance. Verify chosen capacitor tolerance/DC-bias curves, all downstream decoupling and start-up behavior before BOM release. Nominal capacitance alone is insufficient evidence.
- INA228's bus/common-mode operating range is up to 85 V. All ordinary MCU/reporting components remain on their own low-voltage PC domain.
- The 8 mA inline self-consumption allowance remains provisional. At 28 V it implies approximately 198 mW dissipated between the inline regulator stages, plus sensor/isolator dissipation. At 50.4 V the regulator estimate rises to approximately 377 mW. These are allocation calculations, not thermal qualification or permission to operate the USB assembly above its rating.

Primary references: [TI TPS7A43 datasheet, including DGQ package drawing](https://www.ti.com/lit/ds/symlink/tps7a43.pdf), [TI INA228 datasheet](https://www.ti.com/lit/ds/symlink/ina228.pdf).

## Why no blanket TVS claim

The [Vishay SMBJ table](https://www.vishay.com/docs/88392/smbj.pdf) lists SMBJ48A at 48 V stand-off and 77.4 V clamp at the specified 7.8 A pulse. That does not prove an 85 V device is protected under arbitrary cable inductance, source current, temperature or overshoot. A 48 V contract's allowed source tolerance also needs coordination with stand-off/leakage and connector ratings. SMBJ51A leaves still less clamp margin. Neither is fitted or presented as a resolved universal solution.

For the first bench build, use controlled, current-limited sources within the qualified range; no hardware overcurrent cutoff is present. No source-independent hot-plug, ESD, reverse-polarity or surge rating is claimed. Test those conditions with fixtures before OEM equipment is attached. The PC port retains USBLC6-2SC6 data/5 V protection. Verify supply sequencing, USB suspend behavior and both isolation domains before firmware bring-up with external instruments.
