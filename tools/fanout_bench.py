#!/usr/bin/env python3
"""Apply explicit J1 signal escapes before ordinary routing.

This resets only the 14 inline communication nets, then exports a fresh DSN.
The 0.4/0.2 mm signal vias and 0.1 mm inter-signal clearance require fabricator
approval with the proposed 2 oz outer copper. They do not increase current rating.
"""
import json
from pathlib import Path
import pcbnew as k
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'hardware/bench-rev-a'
p=OUT/'power-widget-bench.kicad_pcb';b=k.LoadBoard(str(p))
contacts={n for n in json.loads((OUT/'connections.json').read_text()) if n.startswith('CONTACT_') or n in {'INLINE_DP','INLINE_DM'}}
fps=list(b.GetFootprints()); removed=[]
for t in list(b.GetTracks()):
    if t.GetNetname() in contacts or t.GetNetname()=='SHIELD_INLINE':b.Remove(t);removed.append(t)
    elif not isinstance(t,k.PCB_VIA) and t.GetNetname()=='VBUS_A' and t.GetLayer()==k.B_Cu and abs(k.ToMM(t.GetWidth())-.6)<.001:t.SetWidth(k.FromMM(.3))
def v(x,y):return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
def track(net,pts):
    for a,z in zip(pts,pts[1:]):
        t=k.PCB_TRACK(b);t.SetStart(v(*a));t.SetEnd(v(*z));t.SetWidth(k.FromMM(.15));t.SetLayer(k.F_Cu);t.SetNet(b.FindNet(net));t.SetLocked(True);b.Add(t)
def via(net,x,y):
    t=k.PCB_VIA(b);t.SetPosition(v(x,y));t.SetWidth(k.FromMM(.4));t.SetDrill(k.FromMM(.2));t.SetViaType(k.VIATYPE_THROUGH);t.SetLayerPair(k.F_Cu,k.B_Cu);t.SetNet(b.FindNet(net));t.SetLocked(True);b.Add(t)
j=next(f for f in fps if f.GetReference()=='J1')
for pad in j.Pads():
    pin=pad.GetNumber();net=pad.GetNetname()
    if net not in contacts:continue
    x=k.ToMM(pad.GetPosition().x);y=k.ToMM(pad.GetPosition().y)
    outer=pin in {'A2','A3','A10','A11','B2','B3','B10','B11'}
    ey=(26.65 if pin.startswith('A') else 27.35) if outer else (24.45 if pin.startswith('A') else 29.55)
    pts=[(x,y),(x,ey)]
    if not outer and pin in {'A5','A8','B5','B8'}:
        dx=.05 if x<28 else -.05
        if pin.startswith('A'):pts=[(x,y),(x+dx,25.5),(x+dx,24.85),(x,ey)]
        else:pts=[(x,y),(x+dx,28.5),(x+dx,29.1),(x,ey)]
    track(net,pts);via(net,x,ey)
# MVSEL2's ground pin has a direct local via to the inline reference plane.
if not any(isinstance(t,k.PCB_VIA) and t.GetNetname()=='GND_INLINE' and t.GetPosition()==v(43,48.5) for t in b.GetTracks()):
    track('GND_INLINE',[(42.15,48.5),(43,48.5)]);via('GND_INLINE',43,48.5)
k.SaveBoard(str(p),b)
pro=OUT/'power-widget-bench.kicad_pro';d=json.loads(pro.read_text());base=d['net_settings']['classes'][0]
nc=dict(base,name='USB_contacts',clearance=.1,via_diameter=.4,via_drill=.2)
d['net_settings']['classes']=[base,nc]
d['net_settings']['netclass_patterns']=[{'netclass':'USB_contacts','pattern':n} for n in sorted(contacts)]
d['board']['design_settings']['rules']['min_clearance']=.1
d['board']['design_settings']['rules']['min_hole_clearance']=.2
d['board']['design_settings']['rules']['min_via_diameter']=.4
pro.write_text(json.dumps(d,indent=2)+'\n')
b=k.LoadBoard(str(p));filler=k.ZONE_FILLER(b);filler.Fill(b.Zones());k.SaveBoard(str(p),b);assert k.ExportSpecctraDSN(b,str(OUT/'power-widget-bench.dsn'))
print('Explicit J1 fanout, MVSEL2 ground connection, and USB-contact net class written; reroute and DRC required.')
