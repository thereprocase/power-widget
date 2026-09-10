# Bench connector and harness selection

The project target remains **28 V / 9 A continuous, 10.8 A current design margin**. The selected catalog USB population is a **5 A maximum bench variant**. It does not meet the project's 9 A USB assembly requirement. Force terminals permit separate current-limited core testing with all USB power equipment disconnected.

| Interface | Selection | Published rating / decision |
|---|---|---|
| J1 inline receptacle | GCT USB4115-03-C | 24 contacts, vertical SMT, 48 V DC / 5 A aggregate VBUS; use at 5 A maximum |
| Captive plug candidate | GCT USB4155-03-C | Full-contact PCB-edge plug, 48 V DC / 5 A aggregate VBUS; drawing and harness construction are procurement gates |
| P1 on bench PCB | Custom wire solder termination | Board-side interface only; **not** the mating plug footprint or a purchased cable assembly |
| J8 reporting | GCT USB4105-GF-A-120 | USB 2.0, 16 contacts, 48 V DC / 5 A catalog rating; reporting port uses ordinary USB power limits |
| J2/J3 force connections | Würth 691137710002 | Two poles, **5.00 mm** pitch, 1.30 mm recommended holes, 16 A UL / 24 A VDE; 0.4 Nm terminal torque |

Primary sources: [GCT USB4115](https://gct.co/connector/usb4115), [GCT USB4155](https://gct.co/connector/usb4155), [GCT USB4105](https://gct.co/connector/usb4105), [Würth terminal drawing and ratings](https://www.we-online.com/components/products/datasheet/691137710002.pdf).

## Captive assembly drawing requirements

P1 uses four separate plated wire holes for VBUS and four for return, plus 15 smaller signal/shield holes. The cavity/pad labels in `circuit.json` are the electrical reference. Wire each correspondingly named plug contact; omit the plug's duplicate B6/B7 contacts as specified in the logical plug map. Maintain A5 and B5 independently. Preserve SBU, the eight other signal contacts and shield continuity. No new CC pull resistors, PD controller, e-marker or inline D+/D− charger-signature network is fitted.

The small pads form three rows of five: A2 A3 A5 A6 A7; A8 A10 A11 B2 B3; B5 B8 B10 B11 S. The two larger columns carry VBUS A4/A9/B4/B9 and GND A1/A12/B1/B12 respectively. This is a wiring interface, not permission to swap USB pin labels based on a visual plug view. Verify contact continuity against the actual plug drawing before power. Keep USB 2.0 D+/D− as a short pair, maintain shielding and add independent cable strain relief; solder joints must not take cable pull loads.

No orderable 9 A USB mating assembly has been established from primary manufacturer evidence. A 240 W advertisement establishes neither 9 A nor adequate contact temperature. Larger wires and parallel PCB copper cannot increase the mating contacts' published rating. Qualification must cover both possible CC/VCONN paths, contact current sharing, insertion loss, repeated mating, temperature and the target OEM chargers/laptops. The final topology question remains open, with captive male preferred. The vertical J1 is an accessible bench choice, not a commitment to the final enclosure.

## Force fixture limitations

The terminal's 20 mΩ maximum contact-resistance specification means fixture losses cannot be assumed negligible. Measure at the PCB Kelvin planes and de-embed terminal/wire losses when comparing instruments. The low insertion-loss allocation for the USB product does not include force-fixture terminal loss. Perform 9 A and 10.8 A core tests only with current-limited bench source/load, sized leads and independently monitored contact/PCB temperature; the PCB's current rating is not yet established by measurement.
