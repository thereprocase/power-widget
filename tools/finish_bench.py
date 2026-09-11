#!/usr/bin/env python3
"""Import an explicitly supplied Specctra session, attach schematic UUID paths,
fill planes and save the native PCB. Run native ERC/DRC separately afterwards.
Requires KiCad 9 pcbnew Python. Does not run or silently change autorouting.
"""
import argparse,json,re
from pathlib import Path
import pcbnew as k
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'hardware/bench-rev-a'
ap=argparse.ArgumentParser();ap.add_argument('--session',type=Path);args=ap.parse_args()
p=OUT/'power-widget-bench.kicad_pcb';b=k.LoadBoard(str(p))
if args.session:
    assert k.ImportSpecctraSES(b,str(args.session.resolve())), 'Native session import failed'
cs={c['ref']:c for c in json.loads((OUT/'circuit.json').read_text())['components'] if c['kind']!='flag'}
def vec(x,y):return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
existing={f.GetReference() for f in b.GetFootprints()}
for ref,y in [('H12220',20),('H12230',30)]:
    if ref in existing:continue
    f=k.FOOTPRINT(b);f.SetFPID(k.LIB_ID('','StrainRelief_3mm'));f.SetReference(ref)
    f.SetAttributes(k.FP_BOARD_ONLY|k.FP_EXCLUDE_FROM_BOM|k.FP_EXCLUDE_FROM_POS_FILES)
    pad=k.PAD(f);pad.SetAttribute(k.PAD_ATTRIB_NPTH);pad.SetShape(k.PAD_SHAPE_CIRCLE);pad.SetSize(vec(3,3));pad.SetDrillSize(vec(3,3));pad.SetLayerSet(k.LSET.AllCuMask());f.Add(pad)
    f.SetPosition(vec(122,y));f.Reference().SetVisible(False);f.Value().SetVisible(False);b.Add(f)
labels=[('FORCE A',38,16),('FORCE B',78,20),('CAPTIVE HARNESS',110,42),
        ('RESET',40,79),('BOOT',28,79),('USER',104,97),('SWD',90,84),
        ('UART',15,72),('GPIO',120,73),('PC I2C',113,65),('INLINE I2C',115,51)]
texts={d.GetText() for d in b.GetDrawings() if isinstance(d,k.PCB_TEXT)}
for label,x,y in labels:
    if label in texts:
        for drawing in b.GetDrawings():
            if isinstance(drawing,k.PCB_TEXT) and drawing.GetText()==label:drawing.SetPosition(vec(x,y))
        continue
    t=k.PCB_TEXT(b);t.SetText(label);t.SetPosition(vec(x,y));t.SetTextSize(vec(.9,.9));t.SetTextThickness(k.FromMM(.15));t.SetLayer(k.F_SilkS);b.Add(t)
seen=set()
for f in b.GetFootprints():
    ref=f.GetReference()
    if ref not in cs:
        assert ref.startswith('H'), ('Unexpected extra footprint',ref)
        f.SetAttributes(f.GetAttributes() | k.FP_BOARD_ONLY)
        continue
    c=cs[ref];seen.add(ref);f.SetPath(k.KIID_PATH(c['schematic_path']))
    f.SetValue(c['value'])
    # Pin-level capture currently includes test points in its circuit schedule.
    f.SetAttributes(f.GetAttributes() & ~k.FP_EXCLUDE_FROM_BOM)
    pinmap={x['number']:x['net'] for x in c['pins']}
    for pad in f.Pads():
        if not pad.GetNumber():continue
        assert pad.GetNumber() in pinmap,(ref,pad.GetNumber())
        target=pinmap[pad.GetNumber()]
        if target is None:
            pin=next(x for x in c['pins'] if x['number']==pad.GetNumber())
            name=pin['name'] if pin['name']!=pin['number'] else ''
            target='unconnected-('+ref+'-'+(name+'-' if name else '')+'Pad'+pin['number']+')'
            assert not pad.GetNetname() or pad.GetNetname()==target
            net=b.FindNet(target)
            if not net or net.GetNetCode()<0:
                net=k.NETINFO_ITEM(b,target);b.Add(net)
            pad.SetNet(net)
        assert pad.GetNetname()==target,(ref,pad.GetNumber(),pad.GetNetname(),target)
assert seen==set(cs)
for net,y1,y2,layer in [('GND_INLINE',5.5,58.3,k.B_Cu),('GND_PC',61.7,111.5,k.B_Cu),('GND_INLINE',5.5,58.3,k.F_Cu)]:
    if any(not z.GetIsRuleArea() and z.GetLayer()==layer and z.GetNetname()==net for z in b.Zones()):continue
    z=k.ZONE(b);z.SetLayer(layer);z.SetNet(b.FindNet(net));z.SetLocalClearance(k.FromMM(.2));z.SetPadConnection(k.ZONE_CONNECTION_FULL);z.SetMinThickness(k.FromMM(.15))
    o=z.Outline();o.NewOutline()
    for x,y in [(5.5,y1),(129.5,y1),(129.5,y2),(5.5,y2)]:o.Append(k.FromMM(x),k.FromMM(y))
    b.Add(z)
filler=k.ZONE_FILLER(b);filler.Fill(b.Zones());k.SaveBoard(str(p),b)
# Explicit candidate fabrication stack; impedance and copper tolerances require a fab review.
s=p.read_text()
if '(stackup' not in s:
    stack='''(stackup
      (layer "F.SilkS" (type "Top Silk Screen"))
      (layer "F.Paste" (type "Top Solder Paste"))
      (layer "F.Mask" (type "Top Solder Mask") (thickness 0.01))
      (layer "F.Cu" (type "copper") (thickness 0.07))
      (layer "dielectric 1" (type "prepreg") (thickness 0.18) (material "FR4") (epsilon_r 4.3) (loss_tangent 0.02))
      (layer "In1.Cu" (type "copper") (thickness 0.035))
      (layer "dielectric 2" (type "core") (thickness 1.01) (material "FR4") (epsilon_r 4.3) (loss_tangent 0.02))
      (layer "In2.Cu" (type "copper") (thickness 0.035))
      (layer "dielectric 3" (type "prepreg") (thickness 0.18) (material "FR4") (epsilon_r 4.3) (loss_tangent 0.02))
      (layer "B.Cu" (type "copper") (thickness 0.07))
      (layer "B.Mask" (type "Bottom Solder Mask") (thickness 0.01))
      (layer "B.Paste" (type "Bottom Solder Paste"))
      (layer "B.SilkS" (type "Bottom Silk Screen"))
      (copper_finish "ENIG") (dielectric_constraints no)
    )'''
    s=s.replace('(setup','(setup\n'+stack,1);p.write_text(s)
# Native re-load verifies the stack serialization before reporting success.
b=k.LoadBoard(str(p));assert len(b.GetTracks())>0
report={'kicad_version':k.Version(),'circuit_footprints':len(cs),'named_nets':len({x['net'] for c in cs.values() for x in c['pins'] if x['net']}),'tracks_and_vias':len(b.GetTracks()),'pin_net_map_matches_circuit_json':True,'status':'native ERC and DRC reports determine rule-check status; hardware unqualified'}
(OUT/'board-connectivity-review.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
