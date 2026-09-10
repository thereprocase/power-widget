#!/usr/bin/env python3
"""Reproduce preliminary electrical budgets. No hardware or external packages.

Errors add conservatively; there is no RSS reduction. Allocated residuals and
noise are hypotheses to qualify. This is a steady-state model, not a simulation
of PD, thermal gradients, transient waveforms, protection, or USB integrity.
"""

import argparse
import csv
import io
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def accuracy(a, voltage, power, mode="precision", calibrated=True):
    s, r, b = a["sensor"], a["shunt"], a["allocations"]
    current = power / voltage
    shunt_voltage = current * r["resistance_ohm"]
    i_terms = {
        "current_calibration": b["current_calibration_residual_fraction"],
        "shunt_temperature": r["tcr_ppm_per_c"] * 1e-6 * b["shunt_temperature_delta_c"],
        "sensor_gain_temperature": s["current_gain_drift_ppm_per_c"] * 1e-6 * b["chip_temperature_delta_c"],
        "layout_gain": b["current_layout_gain_fraction"],
        "offset": s["offset_v"] / shunt_voltage,
        "offset_temperature": s["offset_drift_v_per_c"] * b["chip_temperature_delta_c"] / shunt_voltage,
        "common_mode": abs(voltage - s["offset_reference_common_mode_v"]) / 10 ** (s["cmrr_db"] / 20) / shunt_voltage,
        "supply": s["shunt_psrr_v_per_v"] * b["regulated_supply_delta_v"] / shunt_voltage,
        "input_filter_bias": 2 * s["input_bias_a"] * b["sense_filter_each_ohm"] / shunt_voltage,
        "layout_thermal_emf": b["thermoelectric_and_layout_offset_v"] / shunt_voltage,
        "noise_allocation": a["modes"][mode]["shunt_noise_absolute_v_allocation"] / shunt_voltage,
        "quantization_half_lsb": 0.5 * s["shunt_lsb_v"] / shunt_voltage,
    }
    if not calibrated:
        # Conservative sensitivity case: add original shunt tolerance to the
        # calibrated model. This is not a substitute complete uncalibrated spec.
        i_terms["additional_uncalibrated_shunt_tolerance"] = r["initial_tolerance_fraction"]
    v_terms = {
        "voltage_calibration": b["voltage_calibration_residual_fraction"],
        "sensor_gain_temperature": s["bus_gain_drift_ppm_per_c"] * 1e-6 * b["chip_temperature_delta_c"],
        "layout_gain": b["voltage_layout_gain_fraction"],
        "offset": s["bus_offset_v"] / voltage,
        "offset_temperature": s["bus_offset_drift_v_per_c"] * b["chip_temperature_delta_c"] / voltage,
        "supply": s["bus_psrr_v_per_v"] * b["regulated_supply_delta_v"] / voltage,
        "bus_filter_loading": b["bus_filter_max_series_ohm"] / s["bus_input_min_ohm"],
        "noise_allocation": b["bus_noise_absolute_v"] / voltage,
        "quantization_half_lsb": 0.5 * s["bus_lsb_v"] / voltage,
    }
    # The main electronics supply is taken before the shunt. VBUS-input and
    # output protection leakage can remain in the reading. Budget full burden.
    output_burden_w = voltage * (voltage / s["bus_input_min_ohm"] + b["extra_output_leakage_a"])
    i_error, v_error = sum(i_terms.values()), sum(v_terms.values())
    # Bound both multiplicative errors and the output burden conservatively.
    power_error = (1 + i_error) * (1 + v_error) - 1
    power_error += output_burden_w / power * (1 + v_error)
    req = a["requirements"]
    limit = req["normal_power_error_percent"] if power >= req["precision_threshold_w"] else req["low_power_error_percent"]
    return {
        "mode": mode, "voltage_v": voltage, "power_w": power,
        "current_a": current, "shunt_uv": shunt_voltage * 1e6,
        "current_error_percent": i_error * 100,
        "voltage_error_percent": v_error * 100,
        "output_burden_w": output_burden_w,
        "power_error_percent": power_error * 100,
        "target_percent": limit,
        "within_allocation": power_error * 100 <= limit,
        "current_terms_fraction": i_terms, "voltage_terms_fraction": v_terms,
    }


def path_loss(a, current):
    r, p, b = a["shunt"], a["passive_path"], a["allocations"]
    copper_factor = 1 + p["copper_alpha_per_c"] * p["hot_conductor_delta_c"]
    cable_r = 2 * p["pigtail_length_m"] * p["copper_resistivity_ohm_m_at_20c"] / (p["pigtail_each_polarity_area_mm2"] * 1e-6)
    cold = {"shunt": r["resistance_ohm"], "pcb_loop": p["pcb_vbus_and_ground_ohm_at_20c"],
            "added_mating_interface_loop": p["additional_mating_interface_loop_ohm_at_20c"], "pigtail_loop": cable_r}
    hot = {"shunt": cold["shunt"] * (1 + r["tcr_ppm_per_c"] * 1e-6 * p["hot_conductor_delta_c"]),
           "pcb_loop": cold["pcb_loop"] * copper_factor,
           "added_mating_interface_loop": cold["added_mating_interface_loop"] * p["contact_hot_multiplier"],
           "pigtail_loop": cold["pigtail_loop"] * copper_factor}
    return {
        "current_a": current, "cold_parts_ohm": cold, "hot_parts_ohm": hot,
        "hot_loop_ohm": sum(hot.values()), "hot_drop_v": current * sum(hot.values()),
        "hot_passive_loss_w": current * current * sum(hot.values()),
        "shunt_nominal_drop_v": current * r["resistance_ohm"],
        "shunt_nominal_loss_w": current * current * r["resistance_ohm"],
        "meter_supply_power_at_28v_w": a["requirements"]["voltage_max_v"] * b["inline_supply_current_a"],
        "regulator_heat_at_28v_w": (a["requirements"]["voltage_max_v"] - b["inline_supply_output_v"]) * b["inline_supply_current_a"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="check committed outputs without rewriting")
    args = parser.parse_args()
    a = json.loads((ROOT / "analysis/assumptions.json").read_text())
    req, s, r = a["requirements"], a["sensor"], a["shunt"]
    analysis_current = req["current_analysis_scenario_a"]
    design_current = analysis_current * req["margin_factor"]
    selected = []
    for mode in a["modes"]:
        for voltage in [5.0, 9.0, 15.0, 20.0, 28.0]:
            for power in [0.5, 1.0, 5.0, voltage * analysis_current]:
                selected.append(accuracy(a, voltage, power, mode))
    # Cover voltage endpoints and temperature/offset worst-case terms at fine
    # voltage spacing. Include threshold-neighbor powers and current endpoints.
    grid = []
    for step in range(231):
        voltage = 5 + step / 10
        max_power = voltage * analysis_current
        powers = [0.5, 1, 4.999, 5, 5.001, max_power]
        powers += [0.5 * (max_power / 0.5) ** (j / 80) for j in range(81)]
        grid.extend(accuracy(a, voltage, power) for power in sorted(set(powers)))
    worst_normal = max((x for x in grid if x["power_w"] >= 5), key=lambda x: x["power_error_percent"])
    worst_low = max((x for x in grid if x["power_w"] < 5), key=lambda x: x["power_error_percent"])
    modes = {}
    for name, mode in a["modes"].items():
        period_s = mode["conversion_time_us_per_channel"] * 1e-6 * mode["averages"] * mode["enabled_channels"]
        modes[name] = {
            "nominal_window_s": period_s, "nominal_fresh_updates_hz": 1 / period_s,
            "typical_noise_free_step_uv": 2 * s["shunt_range_v"] / 2 ** mode["datasheet_typical_noise_free_enob"] * 1e6,
            "absolute_noise_allocation_uv": mode["shunt_noise_absolute_v_allocation"] * 1e6,
        }
    nominal_limit = s["shunt_range_v"] / r["resistance_ohm"]
    resistance_high = r["resistance_ohm"] * (1 + r["initial_tolerance_fraction"]) * (1 + r["tcr_ppm_per_c"] * 1e-6 * a["allocations"]["shunt_temperature_delta_c"])
    loss_rows = [path_loss(a, i) for i in sorted(set([5, analysis_current, design_current, 12.5, 15]))]
    main_loss = path_loss(a, analysis_current)
    scenarios = []
    for rating in req["current_scenarios_a"]:
        design = rating * req["margin_factor"]
        shunt_heat = design ** 2 * resistance_high
        scenarios.append({
            "hypothetical_oem_max_a": rating - req["manufacturer_allowance_a"],
            "hypothetical_rating_a": rating, "design_current_a": design,
            "rating_power_at_28v_w": rating * req["voltage_max_v"],
            "high_resistance_shunt_heat_at_design_current_w": shunt_heat,
            "within_75_percent_of_1w_shunt_allocation": shunt_heat <= 0.75 * r["rated_power_w_at_70c"],
            "adc_range_covers_design_current": design < s["shunt_range_v"] / resistance_high,
            "hot_passive_loss_at_rating_w": path_loss(a, rating)["hot_passive_loss_w"],
        })
    sensitivity = {
        "retain_shunt_tolerance_28v_5w": accuracy(a, 28, 5, calibrated=False),
        "trend_28v_half_watt": accuracy(a, 28, 0.5, mode="trend"),
    }
    summary = {
        "status": a["status"], "evaluated_grid_points": len(grid),
        "verified_oem_max_current_a": req["verified_oem_max_current_a"],
        "analysis_current_scenario_a": analysis_current,
        "analysis_is_final_current_rating": False,
        "current_scenarios": scenarios,
        "worst_normal_precision": worst_normal, "worst_low_precision": worst_low,
        "nominal_current_adc_limit_a": nominal_limit,
        "high_resistance_current_adc_limit_a": s["shunt_range_v"] / resistance_high,
        "design_voltage_v": req["voltage_max_v"] * req["margin_factor"],
        "scenario_design_current_a": design_current,
        "sense_filter_nominal_corner_hz": 1 / (2 * math.pi * 2 * a["allocations"]["sense_filter_each_ohm"] * a["allocations"]["sense_filter_cap_f"]),
        "modes": modes, "path_loss": loss_rows, "sensitivity": sensitivity,
    }
    # Independent dimensional and boundary sanity checks; these validate the
    # calculator, not hardware. Failing a design allocation is also reported.
    assert math.isclose(6 * .005, .03)
    assert math.isclose(6 ** 2 * .005, .18)
    assert math.isclose(28 * 6, 168)
    assert math.isclose(130 / 20, 6.5)
    assert accuracy(a, 28, 4.999)["target_percent"] == 5
    assert accuracy(a, 28, 5)["target_percent"] == 1
    assert summary["high_resistance_current_adc_limit_a"] > design_current
    assert math.isclose((8.5 + req["manufacturer_allowance_a"]) * req["margin_factor"], 10.8)
    assert not scenarios[-1]["within_75_percent_of_1w_shunt_allocation"], "Larger current scenario needs a different shunt package"
    assert worst_normal["within_allocation"] and worst_low["within_allocation"], "Precision allocation exceeds target"
    assert not sensitivity["trend_28v_half_watt"]["within_allocation"], "Reassess separate trend specification"
    assert main_loss["hot_loop_ohm"] <= a["passive_path"]["hot_added_loop_target_ohm"]

    lines = ["# Calculated budgets", "", "Generated by `python tools/budgets.py` from `analysis/assumptions.json`.", "",
             "**Provisional allocations, not measured performance.** See [method and limitations](../docs/budgets.md).", "",
             f'Current rule: verified OEM maximum + 0.5 A, followed by 20% design margin. **The OEM maximum is unresolved. The {analysis_current:g} A study below is a scenario, not a finalized rating.**', "",
             "## Precision-mode DC error allocation", "",
             "| Voltage | Power | Current | Shunt signal | Calculated error bound | Target |", "|---|---|---|---|---|---|"]
    for x in selected:
        if x["mode"] == "precision":
            lines.append(f'| {x["voltage_v"]:g} V | {x["power_w"]:g} W | {x["current_a"]*1000:.3f} mA | {x["shunt_uv"]:.3f} µV | {x["power_error_percent"]:.3f}% | {x["target_percent"]:g}% |')
    lines += ["", f'The sweep evaluates {len(grid):,} points. Largest precision allocation at ≥5 W: **{worst_normal["power_error_percent"]:.3f}%** ({worst_normal["voltage_v"]:g} V, {worst_normal["power_w"]:g} W). Below 5 W: **{worst_low["power_error_percent"]:.3f}%** ({worst_low["voltage_v"]:g} V, {worst_low["power_w"]:g} W).', "",
              "## Timing and noise", "", "| Mode | Nominal window | Fresh updates | Noise allocation |", "|---|---|---|---|"]
    for name, m in modes.items():
        lines.append(f'| {name} | {m["nominal_window_s"]*1000:.3f} ms | {m["nominal_fresh_updates_hz"]:.2f}/s | ±{m["absolute_noise_allocation_uv"]:g} µV |')
    lines += ["", f'Trend-mode allocation at 28 V / 0.5 W: **{sensitivity["trend_28v_half_watt"]["power_error_percent"]:.3f}%**; it does not meet the low-power precision target.', "",
              "## Added resistance and losses: captive-pigtail candidate", "",
              "| Current | Shunt drop | Shunt heat | Hot added loop | Hot added drop | Hot passive loss |", "|---|---|---|---|---|---|"]
    for x in loss_rows:
        lines.append(f'| {x["current_a"]:g} A | {x["shunt_nominal_drop_v"]*1000:.2f} mV | {x["shunt_nominal_loss_w"]:.4f} W | {x["hot_loop_ohm"]*1000:.3f} mΩ | {x["hot_drop_v"]*1000:.2f} mV | {x["hot_passive_loss_w"]:.3f} W |')
    lines += ["", "These are sizing scenarios, not qualified cable ratings or instructions to overload generic USB connectors.", "",
              f'Inline supply allocation at 28 V: **{main_loss["meter_supply_power_at_28v_w"]:.3f} W**, including about {main_loss["regulator_heat_at_28v_w"]:.3f} W in the linear regulator. Add this to passive losses when estimating total heat; it is excluded from the forward shunt reading.', "",
              "## Manufacturer-current rule sensitivity", "", "| Hypothetical OEM max | Hypothetical rating | Design current | Shunt heat at design current | Within 75% of 1 W allocation? |", "|---|---|---|---|---|"]
    for x in scenarios:
        lines.append(f'| {x["hypothetical_oem_max_a"]:g} A | {x["hypothetical_rating_a"]:g} A | {x["design_current_a"]:g} A | {x["high_resistance_shunt_heat_at_design_current_w"]:.3f} W | {"Yes" if x["within_75_percent_of_1w_shunt_allocation"] else "No — change shunt"} |')
    lines += ["", "The 75% allocation is an engineering derating target assuming the resistor remains within its 70°C full-power condition. It does not replace thermal qualification.", "",
              "## Range and calibration sensitivity", "",
              f'- ADC current range with 5 mΩ: ±{nominal_limit:.3f} A nominal, ±{summary["high_resistance_current_adc_limit_a"]:.3f} A at the modeled high resistance.',
              f'- Retaining an additional 0.5% shunt tolerance raises the 28 V / 5 W allocation to {sensitivity["retain_shunt_tolerance_28v_5w"]["power_error_percent"]:.3f}%; per-unit calibration is a real requirement.',
              "- Connector qualification, thermal gradients, transient response, and long-term drift remain outside this calculator.", ""]
    csv_buffer = io.StringIO(newline="")
    fields = ["mode", "voltage_v", "power_w", "current_a", "shunt_uv", "current_error_percent", "voltage_error_percent", "output_burden_w", "power_error_percent", "target_percent", "within_allocation"]
    writer = csv.DictWriter(csv_buffer, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    writer.writerows(selected)
    outputs = {ROOT / "analysis/results.json": json.dumps(summary, indent=2) + "\n",
               ROOT / "analysis/accuracy.csv": csv_buffer.getvalue(),
               ROOT / "analysis/results.md": "\n".join(lines)}
    for path, content in outputs.items():
        if args.check:
            if not path.exists() or path.read_text() != content:
                raise SystemExit(f"Stale result: {path.relative_to(ROOT)}")
        else:
            path.write_text(content)
    print(f'{"Checked" if args.check else "Wrote"} {len(outputs)} outputs; {analysis_current:g} A scenario; {len(grid):,} points; precision worst {worst_normal["power_error_percent"]:.3f}% / {worst_low["power_error_percent"]:.3f}%; hot loop {main_loss["hot_loop_ohm"]*1000:.3f} mΩ.')


if __name__ == "__main__":
    main()
