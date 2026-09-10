#!/usr/bin/env python3
"""Generate editable KiCad bench placement and manually constrained power routes.

Requires KiCad 9 pcbnew. Autorouting is a separate, reviewable step; this script
does not certify routing, USB signal integrity, current rating or isolation.
"""
import json, uuid
from pathlib import Path
import pcbnew as k
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'hardware/bench-rev-a'
cs=[c for c in json.loads((OUT/'circuit.json').read_text())['components'] if c['kind']!='flag']
def v(x,y):return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
def layers(*ids):
    s=k.LSET()
    for i in ids:s.AddLayer(i)
    return s
b=k.BOARD();b.SetCopperLayerCount(4)
netnames=sorted({p['net'] for c in cs for p in c['pins'] if p['net']})
nets={}
for n in netnames:
    ni=k.NETINFO_ITEM(b,n);b.Add(ni);nets[n]=ni
pos={
 'J1':(28,27,0),'P1':(108,15,0),'R1':(65,25,0),'J2':(45,14,90),'J3':(85,14,90),
 'J4':(88,36,0),'R2':(28,33,0),
 'TP1':(45,20,0),'TP2':(85,20,0),'TP3':(94,10,0),'TP4':(14,37,0),'TP5':(18,37,0),
 'TP6':(22,42,0),'TP7':(26,42,0),'TP8':(31,39,0),'TP9':(35,39,0),
 'U1':(65,40,0),'R3':(61,33,90),'R4':(69,33,90),'C1':(65,35,0),
 'R5':(74,37,0),'C2':(71,41,90),'C3':(65,45,0),
 'U2':(75,60,90),'C4':(78,54.5,0),'C5':(78,65.5,0),
 'R6':(72,69,0),'R7':(78,69,0),'R8':(72,51,0),'R9':(78,51,0),
 'J5':(110,70,0),'J6':(110,46,90),'TP10':(57,40,0),
 'U4':(40,48,0),'JP3':(40,33,90),'R10':(40,38,90),'C6':(43,42,90),
 'C7':(35,48,90),'C20':(45,47,90),'C21':(51,47,90),'JP1':(32,53,90),'J7':(20,52,90),
 'U5':(46,92,0),'JP2':(38,94,90),'C8':(42,88,90),'C9':(46,87,0),'C10':(51,102,0),
 'U7':(91,71,0),'R25':(96,71,90),'C18':(91,75,0),'C19':(91,67,0),'JP4':(103,67,90),'R26':(103,71,0),
 'J8':(60,107,0),'U3':(75,86,0),'U6':(60,99,90),'R13':(53,106,90),'R14':(67,106,90),
 'R15':(66,99,90),'R16':(70,99,90),'C11':(75,94,0),'C12':(75,78,0),'C13':(83,87,90),
 'C14':(66,82,90),'R17':(65,87,90),'C15':(65,91,0),'C16':(62,87,90),
 'R18':(58,92,90),'R19':(58,87,90),'R20':(53,99,90),
 'J9':(90,88,0),'J10':(15,77,0),'J11':(119,77,0),
 'R21':(58,76,0),'C17':(58,80,0),'SW1':(40,74,0),'R22':(83,78,0),'SW2':(28,74,0),
 'R23':(95,81,0),'SW3':(104,92,0),'R24':(103,101,0),'D1':(110,101,0)
}
assert set(pos)=={c['ref'] for c in cs},(set(pos)^{c['ref'] for c in cs})
fps={}; manifest=[]
for c in cs:
    name=c['footprint'].split(':')[1];f=k.FootprintLoad(str(OUT/'PowerWidget.pretty'),name)
    f.SetReference(c['ref']);f.SetValue(c['value']);f.SetFPID(k.LIB_ID('PowerWidget',name))
    f.SetOrientationDegrees(pos[c['ref']][2]);f.SetPosition(v(*pos[c['ref']][:2]))
    pinmap={p['number']:p['net'] for p in c['pins']}
    for p in f.Pads():
        if p.GetNumber() and p.GetNumber() not in pinmap:raise ValueError((c['ref'],p.GetNumber()))
        n=pinmap.get(p.GetNumber())
        if n:p.SetNet(nets[n])
    f.Reference().SetTextSize(v(.9,.9));f.Reference().SetTextThickness(k.FromMM(.15));f.Value().SetVisible(False)
    refpos={'J2':(40,14),'J3':(80,14),'P1':(108,12),'C20':(46,51),'R17':(68,88),'R20':(50,98),'C10':(51,104)}
    if c['ref'] in refpos:
        f.Reference().SetPosition(v(*refpos[c['ref']]));f.Reference().SetTextAngle(k.EDA_ANGLE(0,k.DEGREES_T))
    b.Add(f);fps[c['ref']]=f
    manifest.append({'reference':c['ref'],'footprint':c['footprint'],'x_mm':pos[c['ref']][0],'y_mm':pos[c['ref']][1],'rotation_deg':pos[c['ref']][2],'domain':c['domain']})
def line(a,z,layer,width=.1):
    s=k.PCB_SHAPE(b);s.SetShape(k.SHAPE_T_SEGMENT);s.SetStart(v(*a));s.SetEnd(v(*z));s.SetLayer(layer);s.SetWidth(k.FromMM(width));b.Add(s)
for a,z in [((5,5),(130,5)),((130,5),(130,112)),((130,112),(5,112)),((5,112),(5,5))]:line(a,z,k.Edge_Cuts)
def text(s,x,y,size=1,layer=k.F_SilkS):
    t=k.PCB_TEXT(b);t.SetText(s);t.SetPosition(v(x,y));t.SetTextSize(v(size,size));t.SetTextThickness(k.FromMM(.15));t.SetLayer(layer);b.Add(t)
text('POWER WIDGET / BENCH A',64,7,1.3)
text('USB POPULATION: 5A MAX',27,19,1)
text('CORE: 9A TARGET / TEST REQUIRED',68,17,1)
text('INLINE / FLOATING INSTRUMENTS ONLY',40,57,1)
text('PC DOMAIN / SWD + USB SERIAL',38,64,1)
text('DRAFT - NOT FOR FABRICATION',37,109,1)
for x,y in [(9,9),(126,9),(9,108),(126,108)]:
    f=k.FOOTPRINT(b);f.SetFPID(k.LIB_ID('','MountingHole_3.2mm'));f.SetReference('H'+str(x)+str(y));f.SetAttributes(k.FP_BOARD_ONLY|k.FP_EXCLUDE_FROM_BOM|k.FP_EXCLUDE_FROM_POS_FILES)
    p=k.PAD(f);p.SetAttribute(k.PAD_ATTRIB_NPTH);p.SetShape(k.PAD_SHAPE_CIRCLE);p.SetSize(v(3.2,3.2));p.SetDrillSize(v(3.2,3.2));p.SetLayerSet(k.LSET.AllCuMask());f.Add(p);f.SetPosition(v(x,y));b.Add(f);f.Reference().SetVisible(False);f.Value().SetVisible(False)
def keepout(x1,y1,x2,y2):
    z=k.ZONE(b);z.SetLayerSet(layers(k.F_Cu,k.In1_Cu,k.In2_Cu,k.B_Cu));z.SetIsRuleArea(True)
    z.SetDoNotAllowTracks(True);z.SetDoNotAllowVias(True);z.SetDoNotAllowCopperPour(True);z.SetDoNotAllowPads(True)
    o=z.Outline();o.NewOutline()
    for x,y in [(x1,y1),(x2,y1),(x2,y2),(x1,y2)]:o.Append(int(k.FromMM(x)),int(k.FromMM(y)))
    b.Add(z)
# Physical clearance across this stripe is a functional isolation design choice,
# not a reinforced/safety isolation rating. Only U2's body crosses it.
keepout(5,58.5,130,61.5)
for y in [58.5,61.5]:
    for a,z in [((6,y),(71,y)),((79,y),(129,y))]:line(a,z,k.F_SilkS,.15)
def track(net,points,width,layer=k.F_Cu):
    for a,z in zip(points,points[1:]):
        t=k.PCB_TRACK(b);t.SetStart(v(*a));t.SetEnd(v(*z));t.SetWidth(k.FromMM(width));t.SetLayer(layer);t.SetNet(nets[net]);t.SetLocked(True);b.Add(t)
def point(ref,pin):
    p=next(p for p in fps[ref].Pads() if p.GetNumber()==pin);p=p.GetPosition();return k.ToMM(p.x),k.ToMM(p.y)
track('VBUS_A',[(45,14),(45,24.365),(59,24.365)],3)
track('VBUS_A',[(59,24.365),point('R1','1')],1.8)
track('VBUS_B',[point('R1','2'),(71,25.635)],1.8)
track('VBUS_B',[(71,25.635),(85,25.635),(85,14)],3)
track('VBUS_B',[(85,14),(98,14),(99,15),(105,15),(105,27)],3)
track('GND_INLINE',[(45,9),(111,9),(111,27)],4,k.B_Cu)
# Each VBUS contact gets its own short fanout; parallel only after the fanout.
for pin in ['A4','A9','B4','B9']:
    x,y=point('J1',pin); end=(x,24.9 if pin.startswith('A') else 29.1)
    track('VBUS_A',[(x,y),end],.2)
    via=k.PCB_VIA(b);via.SetPosition(v(*end));via.SetWidth(k.FromMM(.6));via.SetDrill(k.FromMM(.3));via.SetViaType(k.VIATYPE_THROUGH);via.SetLayerPair(k.F_Cu,k.B_Cu);via.SetNet(nets['VBUS_A']);via.SetLocked(True);b.Add(via)
    track('VBUS_A',[end,(x,23 if pin.startswith('A') else 31)],.3,k.B_Cu)
track('VBUS_A',[(26.75,23),(35,23),(45,23),(45,14)],1.5,k.B_Cu)
track('VBUS_A',[(26.75,31),(35,31),(35,23)],1.5,k.B_Cu)

def ground_plane(net,y1,y2,layer):
    z=k.ZONE(b);z.SetLayer(layer);z.SetNet(nets[net]);z.SetLocalClearance(k.FromMM(.2));z.SetPadConnection(k.ZONE_CONNECTION_FULL)
    z.SetMinThickness(k.FromMM(.15));o=z.Outline();o.NewOutline()
    for x,y in [(5.5,y1),(129.5,y1),(129.5,y2),(5.5,y2)]:o.Append(k.FromMM(x),k.FromMM(y))
    b.Add(z)
for net,y1,y2 in [('GND_INLINE',5.5,58.3),('GND_PC',61.7,111.5)]:ground_plane(net,y1,y2,k.In1_Cu)
# Local copper heat spreading at the regulator's exposed pad comes from filled ground planes.
settings=b.GetDesignSettings();settings.m_CopperEdgeClearance=k.FromMM(.25);settings.m_MinClearance=k.FromMM(.15);settings.m_TrackMinWidth=k.FromMM(.15)
settings.m_ViasMinSize=k.FromMM(.45);settings.m_MinThroughDrill=k.FromMM(.2)
b.BuildListOfNets();b.BuildConnectivity()
k.SaveBoard(str(OUT/'power-widget-bench.kicad_pcb'),b)
b=k.LoadBoard(str(OUT/'power-widget-bench.kicad_pcb'))
filler=k.ZONE_FILLER(b);filler.Fill(b.Zones())
k.SaveBoard(str(OUT/'power-widget-bench.kicad_pcb'),b)
(OUT/'placement.json').write_text(json.dumps(manifest,indent=2)+'\n')
assert k.ExportSpecctraDSN(b,str(OUT/'power-widget-bench.dsn'))
# Routing rule within fine-pitch connector fanouts; retain 0.2 mm plane clearance.
dsn=OUT/'power-widget-bench.dsn'
s=dsn.read_text().replace('(width 200)','(width 150)').replace('(clearance 200)','(clearance 150)')
dsn.write_text(s)
print(f'Placed {len(fps)} circuit footprints on 125 x 107 mm bench PCB; exported DSN. Routing incomplete until route step.')
