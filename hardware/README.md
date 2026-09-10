# Hardware status

The newest design is [bench revision A](bench-rev-a/README.md): a full pin-level circuit draft with sensing, isolation, reporting USB, STM32F072, SWD/UART/GPIO, force terminals and selectable sensor power. It is intended for firmware work and connector experiments on one accessible board.

The package includes a root KiCad schematic, five child sheets, readable connection-sheet previews, a component schedule and machine-readable connections. Native KiCad loading/ERC and footprints still need review; no PCB, Gerbers, purchase-ready BOM, tested assembly or qualified USB-C cable is available.

The design target is 28 V / 9 A continuous with 10.8 A margin. Captive male is the bench baseline; the final product topology remains open. See the [connector map](../docs/connector-routing.md), [architecture](../docs/architecture.md), [open decisions](../docs/decisions.md) and [validation gates](../docs/validation-plan.md).
