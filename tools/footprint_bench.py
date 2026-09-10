#!/usr/bin/env python3
"""Vendor selected KiCad footprints and generate explicit bench terminations.

Run with KiCad 9 pcbnew Python and KICAD_FOOTPRINT_DIR set to its footprint tree.
Upstream footprints: KiCad libraries, CC-BY-SA 4.0 with KiCad library exception.
Custom force/harness geometry is a bench wiring interface, not a USB plug land pattern.
"""
import json, os, re
from pathlib import Path
import pcbnew as k
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'hardware/bench-rev-a'
LIB=OUT/'PowerWidget.pretty'; LIB.mkdir(exist_ok=True)
SRC=Path(os.environ.get('KICAD_FOOTPRINT_DIR','/usr/share/kicad/footprints'))
cs=json.loads((OUT/'circuit.json').read_text())['components']
def vec(x,y):return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
def pad(fp,num,x,y,w,h,drill=0):
    p=k.PAD(fp);p.SetNumber(num);p.SetPosition(vec(x,y));p.SetSize(vec(w,h))
    p.SetShape(k.PAD_SHAPE_OVAL if w!=h else k.PAD_SHAPE_CIRCLE)
    p.SetAttribute(k.PAD_ATTRIB_PTH if drill else k.PAD_ATTRIB_SMD)
    layers=k.LSET.AllCuMask() if drill else k.LSET()
    for layer in ([k.F_Mask,k.B_Mask] if drill else [k.F_Cu,k.F_Mask,k.F_Paste]):layers.AddLayer(layer)
    p.SetLayerSet(layers)
    if drill:p.SetDrillSize(vec(drill,drill))
    fp.Add(p)
def box(fp,x1,y1,x2,y2):
    for a,b in [((x1,y1),(x2,y1)),((x2,y1),(x2,y2)),((x2,y2),(x1,y2)),((x1,y2),(x1,y1))]:
        s=k.PCB_SHAPE(fp);s.SetShape(k.SHAPE_T_SEGMENT);s.SetStart(vec(*a));s.SetEnd(vec(*b));s.SetLayer(k.F_CrtYd);s.SetWidth(k.FromMM(.05));fp.Add(s)
def custom(name):
    f=k.FOOTPRINT(None);f.SetFPID(k.LIB_ID('PowerWidget',name));f.SetReference('REF**');f.SetValue(name)
    return f
seen=set(); provenance=[]
for c in cs:
    if c['kind']=='flag':continue
    name=c['footprint'].split(':')[1]
    if name in seen:continue
    seen.add(name); src=c['source_footprint']; lib,original=src.split(':')
    if name=='Force_5mm_2pin':
        f=custom(name);pad(f,'1',0,0,3.2,3.2,1.3);pad(f,'2',5,0,3.2,3.2,1.3)
        box(f,-2.75,-4.25,7.75,4.25)
        provenance.append((name,'Custom: Wurth 691137710002, 5.00 mm pitch / 1.30 mm drill; body clearance conservative, mechanical first article required'))
    elif name=='Captive_Termination':
        f=custom(name)
        # Four independent supply wires and four returns; short all corresponding USB contacts in the harness.
        for i,num in enumerate(['A4','A9','B4','B9']):pad(f,num,-3,i*4,3,3,1.3)
        for i,num in enumerate(['A1','A12','B1','B12']):pad(f,num,3,i*4,3,3,1.3)
        sig=['A2','A3','A5','A6','A7','A8','A10','A11','B2','B3','B5','B8','B10','B11','S']
        for i,num in enumerate(sig):pad(f,num,-5+(i%5)*2.5,18+(i//5)*2.5,1.6,1.6,.8)
        box(f,-6.5,-2,6.5,24.5)
        provenance.append((name,'Custom board-side wire solder pads; harness signal map mandatory; no claimed mating-connector footprint'))
    else:
        remap={}
        if name=='WSK2512_5mR':
            lib='Resistor_SMD';original='R_Shunt_Vishay_WSK2512_6332Metric_T1.19mm';remap={'1':'1','4':'2','2':'3','3':'4'}
        if name=='HVSSOP10_DGQ':lib='Package_SO';original='HVSSOP-10-1EP_3x3mm_P0.5mm_EP1.83x1.89mm_ThermalVias'
        f=k.FootprintLoad(str(SRC/(lib+'.pretty')),original)
        if not f:raise RuntimeError(src)
        for p in f.Pads():
            n=p.GetNumber()
            if n in remap:p.SetNumber(remap[n])
            elif n.startswith('S') and c['ref'] in {'J1','J8'}:p.SetNumber('S')
        f.SetFPID(k.LIB_ID('PowerWidget',name));f.SetValue(name)
        provenance.append((name,f'KiCad 9.0.9 snapshot: {lib}:{original}; '+('pad remap '+str(remap) if remap else 'shell pads renamed S where applicable')))
    k.PCB_IO_MGR.PluginFind(k.PCB_IO_MGR.KICAD_SEXP).FootprintSave(str(LIB),f)
(OUT/'fp-lib-table').write_text('(fp_lib_table (lib (name "PowerWidget") (type "KiCad") (uri "${KIPRJMOD}/PowerWidget.pretty") (options "") (descr "Reviewed bench footprint snapshot")))\n')
(OUT/'footprint-provenance.md').write_text('# Footprint provenance\n\nUpstream KiCad footprint snapshots are licensed CC-BY-SA 4.0 with the KiCad library exception. See https://www.kicad.org/libraries/license/. Custom bench terminations are project designs. No USB assembly is rated above its manufacturer rating by this file.\n\n'+'\n'.join('- **'+a+'**: '+b for a,b in provenance)+'\n')
print(f'Wrote {len(seen)} project footprints')
