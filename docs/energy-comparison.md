# Measuring the upstream losses

The instrument will report measured voltage and current, calculated watts, and accumulated Wh. Frequent acquisitions feed one-second reports over timestamped USB serial; a PC logger can forward those same records to MQTT or HTTP. There is no network radio on the bench board.

## Define the boundary before subtracting energy

For a normal A-to-B setup, use the same interval [t0, t1] for every term:

`E_wall − E_laptop_input = E_charger_loss + E_cables_loss + E_board_loss`

This is the user's intended diagnostic. A difference large enough to resolve after uncertainty places the missing energy upstream of the laptop input. It does not separate charger loss from cable loss without further measurements. Use intervals long enough that changes in stored energy in the charger and measurement circuit are negligible, or include those boundary terms during startup/voltage changes.

The present board measures **PCB_B**, before the captive lead. Its uncorrected subtraction is:

`E_wall − E_pcb_b ≈ charger + upstream cable + board losses before PCB_B`

Consequently, `E_laptop_input = E_pcb_b − E_path_after_b`. The latter correction includes both positive and return conductor losses and contacts between the B sense pads and the laptop terminals. For a short captive assembly it can be characterized as the integral of `I² × R_path(T)`, with uncertainty for contact variation, temperature and load-dependent effects. Prefer a reference measurement at the actual laptop input for calibration. If the board must sit at the charger end of an OEM MagSafe/slim-tip cable, the entire downstream OEM cable is beyond PCB_B. Do not silently apply the short-pigtail correction there.

The shunt also sees the small B-side sensing burden. Include its measured/calibrated contribution or its uncertainty when translating the board reading to external load energy. The simple equations assume positive A-to-B operation; reverse or charger-side placement needs an explicit boundary diagram and accounting before using them.

| Quantity | How obtained | Reporting rule |
|---|---|---|
| `energy_pcb_b` | Calibrated sensor samples integrated by elapsed time | Primary measured-plane estimate |
| `energy_path_after_b` | Separate reference or qualified resistance model | Identify assembly, temperature assumption and correction uncertainty |
| `energy_laptop_input` | PCB_B energy less downstream path/burden corrections | Publish only when the correction is available; otherwise leave unavailable |
| Inline electronics energy | Characterize JP3 branch plus separate sense/leakage burdens | An 8 mA design allowance is not a measurement |
| PC/reporting energy | Measure full reporting-port current separately | Outside the inline shunt; do not hide it inside charger efficiency |

The board's upstream self-consumption and resistance losses already appear in wall-minus-PCB_B. **Do not subtract them twice.** Characterizing them lets us assign the difference among the board, charger and cable. Keep the reporting PC and unrelated equipment outside the wall meter's circuit, or meter their contribution separately. The same laptop acting as the PC host can also create an external ground path and alter the energy boundary.

## Frequent samples, one-second results

Normal `logging_1s` mode uses nominal 17.28 ms acquisition windows, about 57.87 fresh voltage/current pairs per second. Firmware timestamps conversion readiness with a monotonic timer and records its timing uncertainty. Polling/I²C/USB work must keep pace; reading the same conversion twice does not count as two samples.

Compute calibrated `p_i = v_i × i_i` for each valid pair. Report time-weighted mean V, mean I and mean P separately. **Mean P is not the product of one-second mean V and mean I.** Accumulate `E_Wh = integral(P dt) / 3600`, using real elapsed time rather than a nominal loop period. Preserve fractional energy in the accumulator so small increments do not round to zero.

Assign each pair an estimated acquisition midpoint from successive ready timestamps, retaining the observation interval and uncertainty. A proposed software integrator joins adjacent valid midpoint samples with linear power segments, splits segments at exact one-second boundaries, and emits a completed window once the next bracketing sample arrives. Integrate V and I similarly for their displayed means. Interpolation is a reconstruction assumption, not an additional measurement. Initial/final unbracketed portions and outages stay uncovered; do not extend a sample indefinitely.

On a missed acquisition, sensor reset, supply loss or communication fault, mark the affected interval incomplete. Do not fill it with zero power, silently carry stale readings forward, or claim complete session energy. Keep cumulative energy over covered time and cumulative uncovered time. For a partial second, report averages over covered time plus coverage; do not imply that partial mean describes a full second. Host packet loss is distinct from sensor loss: onboard totals can survive the former, but only while the MCU remains powered and acquiring.

The INA228 converts voltage and shunt sequentially and averages them internally. Software multiplication of the 16-sample means cannot recover their within-window covariance. Load pulses and PD voltage changes therefore need energy-reference testing; the settled DC error calculation does not guarantee dynamic energy accuracy. If this fails the diagnostic's uncertainty requirement, compare the calibrated on-chip energy accumulator or revise acquisition before claiming performance.

## Timestamp and interval contract

Records carry instrument ID, boot/session ID, sequence, monotonic window start/end, covered microseconds, sample count, calibration ID and quality flags. The host estimates a device-time-to-UTC mapping with repeated request/reply timestamps, retains round-trip bounds and clock drift, and stores receive time separately. Host arrival time alone is not the measurement timestamp. The wall plug's reporting latency, integration boundaries and cumulative-counter resolution need their own characterization.

Prefer differences in cumulative wall-energy counters at matched boundaries if the plug exposes them. If it only reports watts, retain each source timestamp and integrate according to its documented sampling semantics; occasional snapshots can miss pulses. Do not claim the plug's display precision as its measurement accuracy.

Compute the residual together with an uncertainty interval. A conservative bound is:

`u_residual ≤ u_wall + u_board_energy + u_downstream_correction + u_time_alignment`

Use uncertainty quantities in Wh with consistent coverage/definitions. Add calibration bias, counter quantization, clock-scale error, start/end alignment and gap handling explicitly. Root-sum-square is appropriate only where statistical independence and uncertainty type are justified. Longer intervals reduce the relative impact of quantization and uncertain boundaries; they do not remove calibration bias or missing samples. If the residual is no larger than its uncertainty, the location of the missing watts remains unresolved.

## Validation cases

Use a steady reference load, a two-level pulsed load and a controlled voltage transition, then compare energy over identical intervals. Include the 0.5 W and 5 W regions, clock drift, one-second boundary crossings, dropped host records, sensor outages and reconnects. Characterize JP3 current at 5/9/15/20/28 V with idle and active I²C and after warm-up. Validate the downstream resistance correction cold/hot and after mating/flex cycles. Record actual wall-plug specifications before assigning a numerical combined energy-accuracy claim.
