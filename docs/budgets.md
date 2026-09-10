# Budget method and limits

The [generated results](../analysis/results.md) and [input assumptions](../analysis/assumptions.json) are the numerical design record. Run `python tools/budgets.py` to reproduce them; `--check` verifies that committed outputs match the inputs. Python's standard library is sufficient.

The documented laptop-roster maximum is 8.5 A, setting a **9 A continuous design target / 10.8 A margin**. The sweep checks that target. A physical assembly rating and vendor compatibility remain unqualified.

## Low-power accuracy

The demanding point is low power at high voltage: at 28 V / 0.5 W, current is 17.857 mA and a 5 mΩ shunt produces only 89.286 µV. The 5 W transition requires a stricter relative error while its signal is ten times larger. This is why offset, noise, and calibration matter more than the nominal number of ADC bits.

The model uses a conservative arithmetic sum of terms, followed by the multiplicative voltage/current cross-term. It does not use root-sum-square statistics to make the budget smaller:

`E_power = (1 + E_current) × (1 + E_voltage) − 1 + bounded_output_burden / P × (1 + E_voltage)`

| Term | Treatment |
|---|---|
| Current gain after calibration | 0.10% allocated residual, including initial shunt/sensor/filter gain; not the nominal resistor tolerance |
| Voltage gain after calibration | 0.05% allocated residual |
| Sensor offset | Retain the factory maximum conservatively even though calibration is planned |
| Temperature | Allocate up to 25°C sensor change and 35°C shunt change from calibration; these need thermal evidence |
| Shunt TCR | Finished-part 35 ppm/°C for the provisional WSK2512 value |
| Gain drift, offset drift, common-mode and supply effects | Explicit terms from the sensor data; test endpoints do not eliminate these terms |
| Quantization | Half-LSB bounds using the revised wider ADC range |
| Noise | ±1 µV shunt allocation after one-second software averaging, plus a bus-voltage noise allocation |
| Thermal EMF / offset from layout | ±0.5 µV allocation, not a measured value |
| Residual layout gain | 0.05% current and 0.02% voltage allocations |
| Loading and leakage | Full bus-input load plus an additional 10 µA output-leakage allocation; pre-shunt electronics supply excluded in forward use |

Initial factory gain terms are not added again after they have been included in calibrated gain residuals. The model intentionally retains several factory offset and drift terms, so it does not assume perfect calibration. A sensitivity case retains an additional original shunt tolerance to show why unit calibration matters.

See [TI INA228](https://www.ti.com/lit/ds/symlink/ina228.pdf), particularly its electrical and noise tables, and [Vishay WSK2512](https://www.vishay.com/docs/30108/wsk2512.pdf). The noise table is typical characterization, not a system-level guarantee. The selected allocations must be demonstrated across units; a typical ENOB figure cannot certify our product.

## Timing

Normal logging: 540 µs per channel, two channels, 16 averages, giving nominal 17.280 ms sensor windows and about 57.87 fresh pairs/s. Software forms time-weighted one-second reports. The ±1 µV shunt-noise allocation applies to the final one-second result, not each pair. Correlated noise, drift and offsets do not automatically average away. Diagnostic precision remains 1052 µs per channel with 256 averages, or 538.624 ms. Adding temperature conversions changes cadence.

Bus voltage and current are converted sequentially. The budget covers settled DC, not instantaneous multiplication during a load edge or PD voltage transition. Changes within or between windows require characterization. Mark transition-contaminated records where detectable; simple settled endpoint agreement cannot rule out every in-window event. Do not claim guaranteed transient power accuracy from this sensor arrangement.

Reporting more often does not create new independent measurements. Every record needs its actual sample window, sequence number, and validity status. The raw trend stream uses a separately modeled ±3 µV noise allowance and does not meet the low-power precision target; the one-second aggregation allocation remains a hardware validation gate. See [energy-comparison.md](energy-comparison.md) for integration and timestamp rules.

## Loss and temperature

The captive-pigtail study targets **15 mΩ maximum added hot loop resistance**, including positive and return paths, relative to the same charger cable plugged directly into the device. The model allocates PCB copper, one additional mating interface, shunt, and a short pigtail separately. Contact resistance is an assumed procurement/qualification target; it is not a known part rating.

The revised study uses 75 mm of cable with 0.823 mm² copper per polarity, 1.5 mΩ PCB loop resistance, and a 3 mΩ extra mating-interface loop at the cold reference. Ordinary copper temperature scaling and a separate contact-aging/hot multiplier produce the study's hot estimate. Exact cable stranding, crimping, contacts, copper weights, vias, and terminations will replace these allocations.

Loss follows `P = I²R`. This predicts generated heat, **not temperature rise**. Do not convert watts into a claimed connector or enclosure temperature without a thermal model or measurements. The 8 mA inline electronics allowance adds 224 mW at 28 V, most of it in the regulator. It is outside the forward shunt reading but still affects the source and thermal budget.

The two-receptacle topology requires a new resistance model using the actual second cable. It cannot inherit the captive-pigtail result. A longer output cable also moves actual load voltage farther from the PCB measurement plane.

## What the calculations do not establish

- Physical current capacity, charging transparency, cable identity or 28 V overrange behavior. The numeric current target comes from the separate OEM roster.
- Actual noise tails, thermoelectric offsets, assembly variation, long-term drift, contact wear, and temperature-rise limits.
- Transient current fidelity, AC power accuracy, or dynamic energy accuracy with sequential voltage/current sampling.
- Fault clearing, TVS coordination, EMI/ESD performance, or USB signal integrity.
- A mains isolation category or an independent safety protection function.

The modeling gate passes only **conditional feasibility of the measurement budget and selected resistance allocations**. Hardware remains unqualified.
