# Hardware status

The newest design is [bench revision A](bench-rev-a/README.md): a complete proposed circuit and routed **125 × 107 mm, four-layer PCB** with sensing, isolation, reporting USB, STM32F072, SWD/UART/GPIO, force terminals and selectable sensor power. It is intended for firmware work and connector experiments on one accessible board.

The package includes a root KiCad schematic, five child sheets, [connection-sheet previews](bench-rev-a/README.md#circuit-drawings), [top and bottom PCB plots](bench-rev-a/README.md#pcb-views), assigned footprints with local libraries, a draft component schedule and machine-readable connections. Native KiCad checks report **zero ERC violations, DRC violations, unconnected items and schematic/PCB mismatches**; see the [layout review](../docs/layout-review.md). There are no fabrication-release Gerbers, purchase-ready BOM, tested assembly or 3D assembly renders.

The design target is 28 V / 9 A continuous with 10.8 A margin. **The selected USB population is limited to 5 A; the 9 A USB assembly remains unsourced and unqualified.** Captive male is the bench baseline; the final product topology remains open. See the [connector map](../docs/connector-routing.md), [architecture](../docs/architecture.md), [open decisions](../docs/decisions.md) and [validation gates](../docs/validation-plan.md).
