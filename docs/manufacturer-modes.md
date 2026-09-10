# Manufacturer current survey and rating rule

## Accepted rule

The latest instruction is to rate the instrument half an amp above the manufacturer-specific current modes. Apply it in this order:

1. Establish the maximum charging current among the applicable, documented manufacturer/cable/device combinations at up to 28 V.
2. Add **0.5 A** to obtain the required continuous operating current.
3. Apply the retained **20% margin** to that operating current for power-path design and qualification.

The earlier 6 A / 168 W requirement is superseded. The voltage rating remains 28 V. Do not subtract the 0.5 A allowance from the 20% margin or use reserve as an operating allowance.

## Evidence status

**The manufacturer maximum has not yet been verified.** Available primary retrieval did not expose enough OEM output-mode data to establish a defensible ceiling. This is an unresolved first-phase input, not a completed universal-compatibility survey.

| Roster entry / lead | Evidence obtained | Still required |
|---|---|---|
| Apple USB-C and USB-C-to-MagSafe charging | Manufacturer identified by user | Exact charger/cable/device; label and PD baseline; topology at the USB-C end |
| Dell USB-C proprietary modes | Manufacturer identified by user; direct documentation retrieval unsuccessful | Exact model and output-mode table; do not infer all currents from adapter wattage |
| Lenovo Legion Slim 140W, GX21M50625 | [Official product page](https://www.lenovo.com/us/en/p/accessories-and-software/chargers-and-batteries/chargers/gx21m50625) confirms the product; retrieved text does not list output current | Output label, official mode table, matching cable and device |
| Lenovo higher-power charger leads | No verified mode table in this session | Separate USB-C output from slim-tip output and total multiport wattage |
| Other laptop brands | Not yet enumerated | Include relevant outliers before closing the ceiling |
| Proprietary phone charging | Scope/qualification open; do not claim coverage | If included, survey real output current, cable contacts, and in-production device combinations separately |

Lenovo's [Legion 5 15IRX10 PSREF](https://psref.lenovo.com/syspool/Sys/PDF/Legion/Legion_5_15IRX10/Legion_5_15IRX10_Spec.pdf) demonstrates why adapter wattage alone is insufficient: the listed 170/245 W adapters use slim-tip, while its USB-C input is specified separately. Neither large adapter wattage proves that current flows through USB-C.

## Sizing scenarios, not OEM claims

| Hypothetical verified OEM maximum | Required continuous rating | 20% design current | Rating power at 28 V |
|---|---|---|---|
| 6.5 A | 7.0 A | 8.4 A | 196 W |
| 7.0 A | 7.5 A | 9.0 A | 210 W |
| 8.5 A | 9.0 A | 10.8 A | 252 W |
| 12.0 A | 12.5 A | 15.0 A | 350 W |

The **9 A scenario is the provisional analysis point**, not the finalized required rating. The 12.5 A scenario exposes the cost, connector, and shunt consequences of a substantially larger ceiling. These values permit continued engineering without inventing a researched manufacturer maximum.

## Gate to close the number

Collect primary output specifications or legible original labels for the intended roster, and confirm that the stated current traverses the monitored USB-C path. Record peak versus continuous limits, supply-region differences, cable requirements, and any OEM-only signatures. Use an appropriately rated reference fixture for powered verification. Date and freeze the resulting compatibility roster; unknown or future products do not become supported merely because their logo matches.
