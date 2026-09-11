#!/usr/bin/env python3
"""Export circuit JSON and schedules FROM the canonical native KiCad schematic.

This command never writes a schematic, symbol library or PCB. Edit in KiCad,
then export; there is no competing Python circuit definition to overwrite it.
"""
import argparse
import json
from pathlib import Path
import tempfile
from kicad_native import ROOT, OUT, read_netlist, circuit_from_native, validate_circuit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='.kicad-', dir=ROOT) as directory:
        components = circuit_from_native(read_netlist(Path(directory)))
    validate_circuit(components)
    netlist = {}
    for c in components:
        for p in c['pins']:
            if p['net']:
                netlist.setdefault(p['net'], []).append(f'{c["ref"]}.{p["number"]}')
    capture = dict(revision='A', canonical_source='power-widget-bench.kicad_sch',
        status='native schematic export; engineering draft; see ERC/DRC and release gates',
        functional_groups={c['sheet']: c['sheet'].split('-', 1)[1] for c in components},
        components=components)
    lines = ['# Bench component schedule', '',
        '**Exported from the canonical native KiCad schematic. Draft, not an orderable BOM.**',
        'The group column is a functional placement group, not a separate schematic sheet.', '',
        '| Reference | Value / candidate | Domain | Group |', '|---|---|---|---|']
    for c in components:
        lines.append(f'| {c["ref"]} | {c["value"]} | {c["domain"]} | {c["sheet"]} |')
    lines += ['', '## Assembly notes', '']
    for c in components:
        if c['note']:
            lines.append(f'- **{c["ref"]}:** {c["note"]}')
    outputs = {
        'circuit.json': json.dumps(capture, indent=2) + '\n',
        'connections.json': json.dumps(netlist, indent=2, sort_keys=True) + '\n',
        'component-schedule.md': '\n'.join(lines) + '\n',
    }
    for name, data in outputs.items():
        path = OUT / name
        if args.check:
            if not path.exists() or path.read_text() != data:
                raise SystemExit(f'Stale native export: {path.relative_to(ROOT)}')
        else:
            path.write_text(data)
    print(f'{"Checked" if args.check else "Exported"} {len(outputs)} files from KiCad; '
          f'{len(components)} components; {len(netlist)} named nets; domain and CC checks pass.')


if __name__ == '__main__':
    main()
