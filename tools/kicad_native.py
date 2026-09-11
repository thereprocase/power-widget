"""Shared access to the canonical KiCad project and its native XML netlist."""
import os
from pathlib import Path
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'hardware/bench-rev-a'
SCHEMATIC = OUT / 'power-widget-bench.kicad_sch'
PCB = OUT / 'power-widget-bench.kicad_pcb'
# Official KiCad 9.0.9 image used for the migration and checked-in exports.
IMAGE = 'kicad/kicad@sha256:e638b79b0321f29395a5b783e94bb9f3c73303e8da15da27b8f5cb4b67a37729'


def run(*args):
    cli = os.environ.get('KICAD_CLI') or shutil.which('kicad-cli')
    if cli:
        command = [cli]
    elif shutil.which('docker'):
        command = ['docker', 'run', '--rm', '--network', 'none',
                   '--user', f'{os.getuid()}:{os.getgid()}',
                   '--mount', f'type=bind,source={ROOT},target={ROOT}',
                   '--workdir', str(ROOT), '--entrypoint', 'kicad-cli',
                   os.environ.get('KICAD_DOCKER_IMAGE', IMAGE)]
    else:
        raise SystemExit('Install KiCad 9+, set KICAD_CLI, or use Docker with the documented KiCad image.')
    result = subprocess.run(command + [str(arg) for arg in args], cwd=ROOT,
                            text=True, capture_output=True)
    if result.returncode:
        raise SystemExit(result.stdout + result.stderr + f'\nKiCad exited with status {result.returncode}')
    return result.stdout.strip()


def read_netlist(directory):
    path = directory / 'native.xml'
    run('sch', 'export', 'netlist', '--format', 'kicadxml', '-o', path, SCHEMATIC)
    return ET.parse(path).getroot()


def circuit_from_native(xml):
    """Electrical data and metadata all come from editable native symbols/wires.

    The historical `sheet` field denotes a functional placement group. There is
    only one actual schematic sheet. CAD-only power flags stay in KiCad, not BOMs.
    """
    root_uuid = re.search(r'\(uuid\s+"([^"]+)"', SCHEMATIC.read_text()).group(1)
    nets = {}
    for net in xml.findall('./nets/net'):
        name = net.attrib['name']
        if name.startswith('unconnected-'):
            continue
        for node in net.findall('node'):
            key = (node.attrib['ref'], node.attrib['pin'])
            if key in nets:
                raise ValueError(f'Pin appears on more than one native net: {key}')
            nets[key] = name
    libs = {(lib.attrib['lib'], lib.attrib['part']): lib for lib in xml.findall('./libparts/libpart')}
    components = []
    for comp in xml.findall('./components/comp'):
        ref = comp.attrib['ref']
        fields = {f.attrib['name']: f.text or '' for f in comp.findall('./fields/field')}
        source = comp.find('libsource')
        lib = libs[source.attrib['lib'], source.attrib['part']]
        symbol_uuid = comp.findtext('tstamps')
        if len(symbol_uuid.split()) != 1:
            raise ValueError(f'{ref}: multiple units require an explicit ghost/matchline review')
        pins = [dict(number=p.attrib['num'], name=p.attrib.get('name', ''),
                     net=nets.get((ref, p.attrib['num'])), type=p.attrib['type'])
                for p in lib.findall('./pins/pin')]
        components.append(dict(ref=ref, value=comp.findtext('value', ''),
            sheet=fields['Section'], domain=fields['Domain'], kind=fields['CircuitKind'],
            footprint=comp.findtext('footprint', ''), note=fields.get('Notes', ''), pins=pins,
            source_footprint=fields['SourceFootprint'],
            schematic_path=f'/{root_uuid}/{symbol_uuid}'))
    return components


def validate_circuit(components):
    refs = {c['ref']: c for c in components}
    assert len(refs) == len(components), 'Duplicate component references'
    domains = {}
    for c in components:
        assert len({p['number'] for p in c['pins']}) == len(c['pins'])
        if c['domain'] == 'BARRIER':
            continue
        for p in c['pins']:
            if p['net']:
                domains.setdefault(p['net'], set()).add(c['domain'])
    assert all(len(v) == 1 for v in domains.values()), 'Joined isolated domains'
    for net, probe in [('CONTACT_A5', 'TP4'), ('CONTACT_B5', 'TP5')]:
        assert {c['ref'] for c in components for p in c['pins'] if p['net'] == net} == {'J1', 'P1', probe}
    assert {p['number'] for p in refs['U3']['pins']} == {str(i) for i in range(1, 49)}
    assert next(p['net'] for p in refs['U3']['pins'] if p['number'] == '36') == '3V3_PC'
