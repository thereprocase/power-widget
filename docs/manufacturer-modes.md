# Laptop charging envelope

2026-09-10. The user narrowed the scope to practical laptop charging after the phone survey exposed a 12 A mode. **Extreme proprietary phone charging is excluded.** Apple, Dell, and Lenovo laptop setups drive this revision.

## Selected electrical target

**28 V nominal maximum, 9 A continuous design target, 10.8 A current qualification margin.** Voltage component margin remains at least 33.6 V. These are instrument requirements; no connector assembly or built instrument has been qualified yet.

The highest documented mode in this laptop roster is 8.5 A: 8.5 + 0.5 = 9 A; 9 × 1.20 = 10.8 A. At 28 V the rectangular instrument envelope is 252 W. That does not imply an OEM offers 28 V / 9 A. Source tolerance and transients need separate treatment.

## Primary evidence

| Setup | Documented output / evidence | Cable and placement consequence |
|---|---|---|
| Apple 140 W USB-C, MW2M3AM/A | [Apple](https://www.apple.com/shop/product/mw2m3am/a/140w-usb-c-power-adapter) specifies 140 W and recommends MagSafe 3 or a 240 W C-to-C cable. The retrieved page does **not** give its voltage/current table; obtain the actual unit label and PD trace. | Preserve the original cable. Insert at the charger for MagSafe; either end is physically possible for C-to-C. Do not infer proprietary current from watts alone. |
| Dell 165 W USB-C GaN, 450-BFTY, China listing | [Dell output table](https://www.dell.com/zh-cn/shop/-165w-usb-c-gan-/apd/450-bfty/): 28 V / 5.893 A, 20 V / 6.5 A, and 5/9/15 V / 3 A. Its separate <10.5 A current-limit entry is **not** a continuous charging mode. | Retain the original output assembly and negotiation; test charger identification and both higher-current modes with a listed compatible laptop. |
| Lenovo Legion Slim 140 W USB-C, GX21M50625 | [Lenovo product page](https://www.lenovo.com/us/en/p/accessories-and-software/chargers-and-batteries/chargers/gx21m50625), embedded product specification: 20.0 V / 7.0 A; 19.95 V / 5 A; 5/9/15 V / 3 A. Verified from the publicly returned HTML; the text-only page omits the field. | Include a matching Legion laptop and its original output assembly. |
| Lenovo C170 / LA170, Black Myth edition, product 1047372 | [Official Lenovo description](https://www.lenovo.com.cn/wiki/product-doc-46691.html), linked to the [official SKU](https://item.lenovo.com.cn/product/1047372.html): 20 V / 8.5 A maximum, also 20 V / 7 A; matching C-Slim cable contains an E-Mark chip. | Monitor the USB-C **charger end** of the C-to-Slim path. Verify the regional adapter label, AC-input-dependent limits, and exact cable before powered qualification. |

This is a dated, bounded design roster, not an exhaustive guarantee for every product under these brands. The C170 entry is a published maximum, not evidence of continuous laptop draw; the monitor is deliberately sized continuously above it. Physical labels, cable identities, and traces remain acceptance evidence.

## Scope interpretation

- The researched 12 A phone mode no longer drives this design. The 12.5 A / 15 A calculation remains only historical sensitivity analysis.
- Exclude demonstrations, battery-side currents, total multiport wattage, and ordinary barrel/slim-tip adapters whose path contains no USB-C connection.
- Include standards-based laptop PD and the documented Dell/Lenovo modes above. Add exact charger/cable/device entries before extending coverage.
- A USB-C-to-Slim cable still carries its input current through the USB-C source connector. This differs from a fixed slim-tip adapter with no USB-C connection.
- Brand compatibility is a test result; contact continuity alone does not prove authentication, EPR entry, cable identity, or full charging power.

## Bench evidence

Photograph output labels and cable markings; record device and region; compare direct and inserted source capabilities, accepted contracts, cable-discovery responses, charger identification, attained power under equivalent load/battery conditions, orientations, voltage drop, and temperatures. Save captures against the hardware revision. Do not force OEM modes with a substitute trigger.
