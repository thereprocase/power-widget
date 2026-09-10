# Bench component schedule

**Draft, not an orderable BOM.** Empty footprints and open connector MPNs are release blockers. Passive package/value ratings need review.

| Reference | Value / candidate | Domain | Sheet |
|---|---|---|---|
| J1 | USB4115-03-C / USB path 5A MAX | INLINE | 01-inline |
| P1 | Captive harness solder termination | INLINE | 01-inline |
| R1 | WSK25125L000DEA / 5mR 1W | INLINE | 01-inline |
| J2 | 691137710002 / force terminal | INLINE | 01-inline |
| J3 | 691137710002 / force terminal | INLINE | 01-inline |
| J4 | Kelvin probe pads; NOT force pins | INLINE | 01-inline |
| TP1 | VBUS_A | INLINE | 01-inline |
| TP2 | VBUS_B | INLINE | 01-inline |
| TP3 | GND_INLINE | INLINE | 01-inline |
| TP4 | CONTACT_A5 | INLINE | 01-inline |
| TP5 | CONTACT_B5 | INLINE | 01-inline |
| TP6 | INLINE_DP | INLINE | 01-inline |
| TP7 | INLINE_DM | INLINE | 01-inline |
| TP8 | CONTACT_A8 | INLINE | 01-inline |
| TP9 | CONTACT_B8 | INLINE | 01-inline |
| R2 | 0R shield bond | INLINE | 01-inline |
| U1 | INA228AIDGSR | INLINE | 02-sensing |
| U2 | ISO1641BD | BARRIER | 02-sensing |
| R3 | 10R 0.1% matched | INLINE | 02-sensing |
| R4 | 10R 0.1% matched | INLINE | 02-sensing |
| C1 | 100nF 100V differential | INLINE | 02-sensing |
| R5 | 100R | INLINE | 02-sensing |
| C2 | 10nF 100V X7R | INLINE | 02-sensing |
| C3 | 100nF 10V at U1 | INLINE | 02-sensing |
| C4 | 100nF 10V at U2.8 | INLINE | 02-sensing |
| C5 | 100nF 10V at U2.1 | PC | 02-sensing |
| R6 | 2k2 pull-up | PC | 02-sensing |
| R7 | 2k2 pull-up | PC | 02-sensing |
| R8 | 2k2 pull-up | INLINE | 02-sensing |
| R9 | 2k2 pull-up | INLINE | 02-sensing |
| J5 | PC I2C / external MCU | PC | 02-sensing |
| J6 | INLINE I2C debug | INLINE | 02-sensing |
| TP10 | ALERT: floating scope only | INLINE | 02-sensing |
| U4 | TPS7A4333DGQR | INLINE | 03-supplies |
| JP3 | INLINE self-current link | INLINE | 03-supplies |
| R10 | 10R 0.25W branch feed | INLINE | 03-supplies |
| C6 | 1uF 100V X7R | INLINE | 03-supplies |
| C7 | 2u2 10V X7R | INLINE | 03-supplies |
| C20 | 22uF 50V X7R MID | INLINE | 03-supplies |
| C21 | 22uF 50V X7R MID | INLINE | 03-supplies |
| JP1 | SENSOR SUPPLY: one shunt only | INLINE | 03-supplies |
| J7 | Floating external 3.3V | INLINE | 03-supplies |
| U5 | TLV75533PDBVR | PC | 03-supplies |
| JP2 | PC supply current link | PC | 03-supplies |
| C8 | 1uF 10V | PC | 03-supplies |
| C9 | 4u7 10V | PC | 03-supplies |
| C10 | 1uF 10V at connector | PC | 03-supplies |
| U7 | TPS22919DCKR | PC | 03-supplies |
| R25 | 100k enable pull-down | PC | 03-supplies |
| C18 | 100nF 10V at U7.1 | PC | 03-supplies |
| C19 | 1uF 10V at U7.6 | PC | 03-supplies |
| JP4 | External-master enable; DNF | PC | 03-supplies |
| R26 | 10k override limiter | PC | 03-supplies |
| J8 | USB4105-GF-A-120 / reporting | PC | 04-usb-mcu |
| U3 | STM32F072CBT6 / 128K flash | PC | 04-usb-mcu |
| U6 | USBLC6-2SC6 | PC | 04-usb-mcu |
| R13 | 5k1 1% Rd | PC | 04-usb-mcu |
| R14 | 5k1 1% Rd | PC | 04-usb-mcu |
| R15 | 0R tuning footprint | PC | 04-usb-mcu |
| R16 | 0R tuning footprint | PC | 04-usb-mcu |
| C11 | 100nF 10V at U3.24 | PC | 04-usb-mcu |
| C12 | 100nF 10V at U3.48 | PC | 04-usb-mcu |
| C13 | 100nF 10V at U3.36 | PC | 04-usb-mcu |
| C14 | 100nF 10V at U3.1 | PC | 04-usb-mcu |
| R17 | 10R VDDA filter | PC | 04-usb-mcu |
| C15 | 100nF 10V at U3.9 | PC | 04-usb-mcu |
| C16 | 1uF 10V | PC | 04-usb-mcu |
| R18 | 100k 1% | PC | 04-usb-mcu |
| R19 | 100k 1% | PC | 04-usb-mcu |
| R20 | 0R PC shell bond | PC | 04-usb-mcu |
| J9 | Cortex SWD 2x5 1.27mm | PC | 05-debug |
| J10 | UART 3.3V logic | PC | 05-debug |
| J11 | Spare GPIO / SPI | PC | 05-debug |
| R21 | 10k reset pull-up | PC | 05-debug |
| C17 | 100nF reset | PC | 05-debug |
| SW1 | RESET pushbutton | PC | 05-debug |
| R22 | 10k boot pull-down | PC | 05-debug |
| SW2 | BOOT pushbutton | PC | 05-debug |
| R23 | 10k button pull-up | PC | 05-debug |
| SW3 | USER pushbutton | PC | 05-debug |
| R24 | 1k LED limiter | PC | 05-debug |
| D1 | Activity LED | PC | 05-debug |
| #FLG1 | PWR_FLAG | INLINE | 02-sensing |
| #FLG2 | PWR_FLAG | INLINE | 02-sensing |
| #FLG3 | PWR_FLAG | PC | 02-sensing |
| #FLG4 | PWR_FLAG | INLINE | 03-supplies |
| #FLG5 | PWR_FLAG | PC | 03-supplies |
| #FLG6 | PWR_FLAG | PC | 04-usb-mcu |

## Assembly notes

- **J1:** 24 contacts, 48 V / 5 A manufacturer rating. This bench population is limited to 5 A via USB; a 9 A assembly remains a procurement gate.
- **P1:** Board-side termination, not a USB mating footprint. Candidate USB4155-03-C plug is 48 V / 5 A only; custom harness drawing/qualification remains open.
- **R1:** Project pad numbering 1=I1, 2=I2, 3=E1, 4=E2. 5 mOhm uses T=1.19 mm termination variant; current pads and Kelvin pads mapped from Vishay drawing.
- **J2:** Wurth 16 A UL / 24 A VDE, 5.00 mm pitch, 1.30 mm drills. Force path capacity still requires PCB thermal testing.
- **J3:** Wurth 16 A UL / 24 A VDE, 5.00 mm pitch, 1.30 mm drills. Force path capacity still requires PCB thermal testing.
- **J4:** Use small pads near the defined B-plane. No main current through this header.
- **U1:** Address 0x40. Wide ADC range. Footprint candidate still requires package drawing review.
- **U2:** Side 1 PC, side 2 inline. SCL is unidirectional; INA228 does not require clock stretching.
- **J5:** 3V3 is switched reference/output. Hold onboard MCU in reset and fit JP4 for another open-drain master; no external pull-ups to an always-on rail.
- **J6:** Only a floating or isolated instrument here; never jumper to J5.
- **TP10:** No pull-up fitted; open drain requires a local pull-up if probing logic. Firmware polls status.
- **U4:** 85 V fixed 3.3 V regulator. EN intentionally floating per internal pull-up; never tie EN to high VBUS. MID selected 15 V, with capacitors sized >=3x total OUT capacitance.
- **JP3:** Fit shunt normally; insert a floating ammeter to characterize sensor-side self-consumption. Not a main-current connection.
- **JP1:** Normal 1-2; floating external 3.3 V 2-3. Do not install two shunts.
- **J7:** For zero-VBUS/low-voltage bench testing; not connected to PC supply.
- **JP2:** Fit shunt normally. Remove to measure reporting-domain supply current; no external power injection.
- **U7:** Switch U2 side 1 and its pull-ups off in USB suspend. Set PB6/PB7 high impedance first. QOD tied to output.
- **JP4:** Fit only for external-master bench use with U3 held reset; remove for USB suspend testing.
- **J8:** Long board edge. USB 2.0 receptacle may omit unused SS/SBU contacts after exact footprint selection.
- **U3:** Pinout checked against ST DS9826 Rev 6 figure 8. 16 KB RAM. HSI48/CRS USB clock.
- **U6:** Route lines through paired pads with short ground return. PC port only.
- **J9:** Key pin 7 absent. No SWO on Cortex-M0. Debug probe must not power this board.
- **J10:** TX/RX named from board viewpoint; 3V3 reference only. Not RS-232 voltage levels.
- **#FLG1:** ERC supply declaration at a passive feed; no physical component.
- **#FLG2:** ERC supply declaration at a passive feed; no physical component.
- **#FLG3:** ERC supply declaration at a passive feed; no physical component.
- **#FLG4:** ERC supply declaration at a passive feed; no physical component.
- **#FLG5:** ERC supply declaration at a passive feed; no physical component.
- **#FLG6:** ERC supply declaration at a passive feed; no physical component.
