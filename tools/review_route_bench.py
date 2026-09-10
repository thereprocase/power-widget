#!/usr/bin/env python3
"""Apply the documented manual clearance repairs after the retained SES import.

Then run finish_bench.py and native DRC. No DRC violations are excluded here.
The endpoint matches deliberately fail if an upstream routing session changes.
"""
from pathlib import Path
import pcbnew as k
OUT=Path(__file__).resolve().parents[1]/'hardware/bench-rev-a'
p=OUT/'power-widget-bench.kicad_pcb';b=k.LoadBoard(str(p))
def v(x,y):return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
def xy(p):return round(k.ToMM(p.x),4),round(k.ToMM(p.y),4)
removed=[]; ground_removed=[]
def local_ground(q):return 30.7<k.ToMM(q.x)<31.5 and 27.7<k.ToMM(q.y)<28.5
for t in list(b.GetTracks()):
    if t.GetNetname()=='GND_INLINE' and ((isinstance(t,k.PCB_VIA) and local_ground(t.GetPosition())) or (not isinstance(t,k.PCB_VIA) and local_ground(t.GetStart()) and local_ground(t.GetEnd()))):
        b.Remove(t);ground_removed.append(t);continue
    if isinstance(t,k.PCB_VIA):continue
    if t.GetNetname()=='CONTACT_A11' and t.GetLayer()==k.In2_Cu and min(t.GetStart().x,t.GetEnd().x)<k.FromMM(34):
        b.Remove(t);removed.append(t)
    elif t.GetNetname()=='CONTACT_B2' and t.GetLayer()==k.B_Cu:
        mapping={(30.4353,27.5353):(30.55,27.65),(31.5691,27.5353):(31.6838,27.65)}
        for getter,setter in [(t.GetStart,t.SetStart),(t.GetEnd,t.SetEnd)]:
            pt=xy(getter())
            if pt in mapping:setter(v(*mapping[pt]))
assert len(removed)==2, 'Unexpected CONTACT_A11 route; re-review required'
pts=[(30.25,26.65),(31.25,27.65),(32.65,27.65),(32.7647,27.5353),(98.1943,27.5353)]
for a,z in zip(pts,pts[1:]):
    t=k.PCB_TRACK(b);t.SetStart(v(*a));t.SetEnd(v(*z));t.SetLayer(k.In2_Cu);t.SetWidth(k.FromMM(.15));t.SetNet(b.FindNet('CONTACT_A11'));b.Add(t)
k.SaveBoard(str(p),b)
print('Repaired the two routes around J1 locating hole; native DRC required.')
