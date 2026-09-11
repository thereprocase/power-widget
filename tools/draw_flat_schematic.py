#!/usr/bin/env python3
"""Draw the complete bench circuit as one continuously wired SVG sheet.

Only Python's standard library is required. circuit.json remains authoritative.
Symbols may combine pins on the same net; the printed numbers retain every pin.
The router permits perpendicular crossings only, never shared foreign wire edges.
"""
import argparse
from collections import defaultdict
import hashlib
import heapq
import html
import json
from pathlib import Path
import textwrap

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'hardware/bench-rev-a'
G = 10
W, H = 420, 300
INK = '#20272b'
COLORS = {'INLINE': '#155849', 'PC': '#244e88'}

def esc(s): return html.escape(str(s))

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    raw = (OUT / 'circuit.json').read_bytes()
    circuit = json.loads(raw)
    components = {c['ref']: c for c in circuit['components'] if c['kind'] != 'flag'}
    symbols, ports, blocked, bodies = [], {}, set(), []
    def text(x, y, s, size=1.35, anchor='start', weight='normal', color=INK):
        return f'<text x="{x*G:g}" y="{y*G:g}" font-size="{size*G:g}" text-anchor="{anchor}" font-weight="{weight}" fill="{color}">{esc(s)}</text>'
    def line(a,b, color=INK, width=1.5):
        return f'<path d="M {a[0]*G:g},{a[1]*G:g} L {b[0]*G:g},{b[1]*G:g}" fill="none" stroke="{color}" stroke-width="{width}"/>'
    def reserve(ref, x1,y1,x2,y2):
        for old, box in bodies:
            if x1 < box[2] and x2 > box[0] and y1 < box[3] and y2 > box[1]:
                raise ValueError(f'Overlapping symbol reservations: {ref} and {old}')
        bodies.append((ref,(x1,y1,x2,y2)))
        blocked.update((x,y) for x in range(x1,x2+1) for y in range(y1,y2+1))
    def register(ref, nums, xy, inward):
        c=components[ref]
        for n in nums:
            p=next(p for p in c['pins'] if p['number']==n)
            assert p['net'] is not None
            assert (ref,n) not in ports
            ports[ref,n]=(xy,p['net'],inward)
    def block(ref,x,y,w,left,right,title=None,section=None):
        """Sides are lists of pin-number groups, placed in explicit functional order."""
        c=components[ref]
        sides=[[[str(n) for n in group.split(',')] for group in side] for side in (left,right)]
        nc=[p for p in c['pins'] if p['net'] is None]
        n=max(map(len,sides))
        label=title or c['value']
        titlelines=textwrap.wrap(label,width=int(w/0.78))
        top=5+2*len(titlelines)
        nclines=textwrap.wrap('NC: '+', '.join(p['number'] for p in nc),width=int(w/0.72)) if nc else []
        h=top+3*(n-1)+4+len(nclines)*1.7
        h=int(h+0.99)
        reserve(ref,x-1,y-1,x+w+1,y+h+1)
        symbols.append(f'<g id="{ref + ("-"+section if section else "")}"><title>{esc(ref+": "+c["value"]+". "+c.get("note", ""))}</title><rect x="{x*G}" y="{y*G}" width="{w*G}" height="{h*G}" fill="white" stroke="{INK}" stroke-width="2"/>')
        symbols.append(text(x+w/2,y+2.5,ref + (' · '+section if section else ''),1.8,'middle','bold'))
        for i,t in enumerate(titlelines): symbols.append(text(x+w/2,y+4.7+i*1.8,t,1.25,'middle'))
        for side,groups in enumerate(sides):
            for i,nums in enumerate(groups):
                ps=[next(p for p in c['pins'] if p['number']==n) for n in nums]
                assert len({p['net'] for p in ps})==1 and ps[0]['net'] is not None,(ref,nums)
                yy=y+top+i*3
                xx=x if side==0 else x+w
                endpoint=(xx-3 if side==0 else xx+3, yy)
                register(ref,nums,endpoint,(1,0) if side==0 else (-1,0))
                symbols.append(line((xx,yy),endpoint))
                pn=','.join(nums)
                names=list(dict.fromkeys(p['name'] for p in ps if p['name'] and p['name']!=p['number']))
                name='/'.join(names) if names else ps[0]['net'].replace('CONTACT_','').replace('_INLINE','').replace('_PC','')
                # Long power pin groups are legible inside wide package bodies.
                display=pn+(' '+name if name!=pn else '')
                symbols.append(text(xx+(0.7 if side==0 else -0.7),yy-0.55,display,1.1,'start' if side==0 else 'end'))
        for i,t in enumerate(nclines): symbols.append(text(x+1,y+h-1.6-(len(nclines)-1-i)*1.7,t,1.05,color='#656b70'))
        symbols.append('</g>')
    def passive(ref,x,y,vertical=False, label=None):
        c=components[ref]
        kind=c['kind']
        # x,y is symbol center. Text occupies a protected rectangle.
        if vertical:
            reserve(ref,x-2,y-5,x+17,y+5)
            ends=[(x,y-7),(x,y+7)]
            inward=[(0,1),(0,-1)]
            tx,ty,anchor=x+2,y-1,'start'
        else:
            reserve(ref,x-8,y-5,x+8,y+2)
            ends=[(x-10,y),(x+10,y)]
            inward=[(1,0),(-1,0)]
            tx,ty,anchor=x,y-3.4,'middle'
        def pt(a,b):return (x+b,y+a) if vertical else (x+a,y+b)
        def seg(a,b):symbols.append(line(pt(*a),pt(*b)))
        symbols.append(f'<g id="{ref}"><title>{esc(ref+": "+c["value"]+". "+c.get("note", ""))}</title>')
        for i,p in enumerate(c['pins']):
            register(ref,[p['number']],ends[i],inward[i])
        outer=7 if vertical else 10
        seg((-outer,0),(-3,0));seg((3,0),(outer,0))
        if kind=='R':
            ps=[(-3,0),(-2.5,-1),(-1.5,1),(-.5,-1),(.5,1),(1.5,-1),(2.5,1),(3,0)]
            for a,b in zip(ps,ps[1:]):seg(a,b)
        elif kind=='C':
            seg((-3,0),(-.6,0));seg((.6,0),(3,0))
            seg((-.6,-1.7),(-.6,1.7));seg((.6,-1.7),(.6,1.7))
        elif kind=='SW':
            seg((-3,0),(2,-1.8));seg((2.8,-.5),(2.8,.5))
        elif kind=='LED':
            # Source data pin 1=K, 2=A. Cathode is at the first endpoint.
            for a,b in [((-1.5,-1.5),(-1.5,1.5)),((-1.5,0),(1.5,-1.5)),((1.5,-1.5),(1.5,1.5)),((1.5,1.5),(-1.5,0)),((-3,0),(-1.5,0)),((1.5,0),(3,0)),((0,-2),(1,-3)),((1,-2),(2,-3))]:seg(a,b)
        else: raise ValueError(kind)
        symbols.append(text(tx,ty,ref,1.5,anchor,'bold'))
        val=label or c['value']
        # Keep electrical value/tolerance/rating; placement notes live in tooltips.
        val=val.split(' at ')[0]
        for i,t in enumerate(textwrap.wrap(val,24 if vertical else 26)):
            symbols.append(text(tx,ty+1.7*(i+1),t,1.15,anchor))
        symbols.append('</g>')
    def tp(ref,x,y):
        c=components[ref]
        reserve(ref,x-1,y-4,x+8,y)
        register(ref,['1'],(x,y+2),(0,-1))
        symbols.append(f'<g id="{ref}"><title>{esc(c["value"])}</title>')
        symbols.append(line((x,y),(x,y+2)))
        symbols.append(f'<circle cx="{x*G}" cy="{y*G}" r="3.5" fill="white" stroke="{INK}" stroke-width="1.5"/>')
        symbols.append(text(x+1,y-1,ref,1.2));symbols.append('</g>')

    def inline_tp(ref,x,y):
        c=components[ref]
        reserve(ref,x+1,y-2,x+8,y-1)
        register(ref,['1'],(x,y),(1,0))
        symbols.append(f'<g id="{ref}"><title>{esc(c["value"])}</title><circle cx="{x*G}" cy="{y*G}" r="3.5" fill="white" stroke="{INK}" stroke-width="1.5"/>')
        symbols.append(text(x+1,y-.6,ref,1.2));symbols.append('</g>')
    def shunt(x,y):
        reserve('R1',x-8,y-7,x+8,y+2)
        symbols.append('<g id="R1"><title>R1: WSK25125L000DEA, four-terminal 5 mΩ / 1 W shunt. 1/2 force; 3/4 Kelvin.</title>')
        symbols.append(text(x,y-5,'R1  ·  5 mΩ / 1 W',1.6,'middle','bold'))
        symbols.append(text(x,y-3.2,'WSK25125L000DEA',1.2,'middle'))
        points=[(x-5,y),(x-4,y-1),(x-3,y+1),(x-2,y-1),(x-1,y+1),(x,y-1),(x+1,y+1),(x+2,y-1),(x+3,y+1),(x+4,y-1),(x+5,y)]
        for a,b in zip(points,points[1:]):symbols.append(line(a,b,width=2.2))
        for num,xy,d,to in [('1',(x-11,y),(1,0),(x-5,y)),('2',(x+11,y),(-1,0),(x+5,y)),('3',(x-5,y+5),(0,-1),(x-5,y)),('4',(x+5,y+5),(0,-1),(x+5,y))]:
            register('R1',[num],xy,d);symbols.append(line(xy,to,width=2.2 if num in ('1','2') else 1.5))
            symbols.append(text(xy[0]+.7,xy[1]-.7,num+(' I' if num in ('1','2') else ' E'),1.1))
        symbols.append('</g>')
    # Split connector units by function, retaining every numbered physical contact.
    # This keeps the Kelvin branch below its shunt, free of the pass-through bundle.
    power=['A4,A9,B4,B9','A1,A12,B1,B12']
    contact=['A2','A3','A5','B5','A6,B6','A7,B7','A8','B8','A10','A11','B2','B3','B10','B11','S']
    block('J1',12,20,24,[],power,'USB4115-03-C / 5 A max',section='power')
    block('P1',145,20,26,power,[],'Captive harness / output',section='power')
    shunt(91,27)
    block('J2',45,10,24,[],['1','2'],'Force input')
    block('J3',112,10,24,['1','2'],[],'Force output')
    block('J4',115,40,30,['1','2','3','4'],[],'Kelvin sense only')
    for ref,x,y in [('TP1',73,35),('TP2',106,35),('TP3',9,48)]:tp(ref,x,y)
    block('U1',99,70,31,['10','9','8','1,2','7'],['6','4','5','3'],'INA228AIDGSR / address 0x40')
    passive('R3',61,74,label='10 Ω / 0.1% matched')
    passive('R4',61,89,label='10 Ω / 0.1% matched')
    passive('R5',61,104,label='100 Ω')
    passive('C1',76,91,True,label='100 nF / 100 V')
    passive('C2',81,111,True,label='10 nF / 100 V')
    passive('C3',111,120,True,label='100 nF / 10 V')
    passive('R8',141,70,True,label='2.2 kΩ')
    passive('R9',162,70,True,label='2.2 kΩ')
    tp('TP10',141,104)
    block('J6',145,120,28,['1','2','3','4'],[],'Inline I²C debug')
    block('U2',192,77,28,['8','7','6','5'],['1','2','3','4'],'ISO1641BD / isolated I²C')
    passive('C4',174,104,True,label='100 nF / 10 V')
    passive('C5',226,104,True,label='100 nF / 10 V')
    passive('R6',232,69,True,label='2.2 kΩ')
    passive('R7',253,69,True,label='2.2 kΩ')
    block('J5',225,122,28,[],['1','2','3','4'],'PC I²C / external master')

    block('JP3',13,157,25,[],['1','2'],'Inline current link / fitted')
    passive('R10',56,169,label='10 Ω / 0.25 W')
    block('U4',81,159,29,['10','4,5,7,11'],['1','8'],'TPS7A4333DGQR / 3.3 V')
    passive('C6',56,195,True,label='1 µF / 100 V')
    passive('C7',122,195,True,label='2.2 µF / 10 V')
    passive('C20',81,206,True,label='22 µF / 50 V')
    passive('C21',102,206,True,label='22 µF / 50 V')
    block('JP1',132,158,33,['1','2','3'],[],'Sensor supply / 1–2 normal; 2–3 external')
    block('J7',152,197,27,['1','2'],[],'Floating 3.3 V input')
    block('J1',12,225,24,[],contact,'USB4115-03-C / same J1',section='contacts')
    plug=[v.replace(',B6','').replace(',B7','') for v in contact]
    block('P1',145,225,26,plug,[],'Captive harness / same P1',section='contacts')
    passive('R2',26,207,label='0 Ω shield bond')
    for ref,x,y in [('TP4',55,238),('TP5',68,241),('TP6',81,244),('TP7',94,247),('TP8',107,250),('TP9',120,253)]:inline_tp(ref,x,y)

    block('J8',226,20,30,[],['A1,A12,B1,B12','A4,A9,B4,B9','A5','B5','A6,B6','A7,B7','S'],'USB4105 / PC reporting')
    passive('R13',282,39,label='5.1 kΩ / 1% Rd')
    passive('R14',282,51,label='5.1 kΩ / 1% Rd')
    passive('R20',282,65,label='0 Ω shield bond')
    block('U6',306,26,25,['1,6','3,4'],['5','2'],'USBLC6-2SC6 / ESD')
    passive('R15',312,64,label='0 Ω USB D+')
    passive('R16',312,77,label='0 Ω USB D−')
    passive('R18',350,33,True,label='100 kΩ / 1%')
    passive('R19',350,54,True,label='100 kΩ / 1%')
    passive('C10',377,33,True,label='1 µF / 10 V')

    block('U3',280,106,40,
          ['1,24,36,48','9','8,23,35,47','33','32','43','42','11','10'],
          ['34','37','7','12','13','14','15','16','17','21','22','44','18','19'],
          'STM32F072CBT6 / 128 KB / USB MCU')
    block('J9',362,87,35,['1','2','4','10','3,5,9'],[],'Cortex SWD / 2×5 / key 7 absent')
    block('J10',362,124,35,['1','2','3','4'],[],'UART / 3.3 V logic')
    block('J11',362,153,35,['1','2','3','4','5','6','7','8'],[],'GPIO / SPI')
    passive('R21',337,208,True,label='10 kΩ reset pull-up')
    passive('C17',359,208,True,label='100 nF reset')
    passive('SW1',390,208,True,label='RESET / N.O.')
    passive('R22',337,236,True,label='10 kΩ boot pull-down')
    passive('SW2',359,236,True,label='BOOT / N.O.')
    passive('R23',382,236,True,label='10 kΩ user pull-up')
    passive('SW3',403,236,True,label='USER / N.O.')
    passive('R24',365,269,label='1 kΩ LED limiter')
    passive('D1',393,269,label='Activity LED / K ← A')

    block('JP2',196,218,23,[],['1','2'],'PC current link / fitted')
    block('U5',243,216,27,['1,3','2'],['5'],'TLV75533PDBVR / 3.3 V')
    passive('C8',222,251,True,label='1 µF / 10 V')
    passive('C9',248,251,True,label='4.7 µF / 10 V')
    block('U7',293,216,27,['1','3','2'],['5,6'],'TPS22919DCKR / load switch')
    passive('C18',273,250,True,label='100 nF / 10 V')
    passive('C19',304,250,True,label='1 µF / 10 V')
    passive('R25',305,272,label='100 kΩ enable pull-down')
    block('JP4',193,267,30,[],['1','2'],'External master / NOT FITTED')
    passive('R26',250,278,label='10 kΩ override limiter')

    for ref,x in [('C11',265),('C12',286),('C13',307),('C14',328)]:
        passive(ref,x,192,True,label='100 nF / 10 V')
    passive('R17',291,91,label='10 Ω VDDA filter')
    passive('C15',321,91,True,label='100 nF / 10 V')
    passive('C16',342,76,True,label='1 µF / 10 V')

    def heading(x,y,w,title,subtitle=None):
        reserve(title,x-1,y-3,x+w,y+(3 if subtitle else 1))
        symbols.append(text(x,y,title,1.8,weight='bold'))
        if subtitle:symbols.append(text(x,y+2.5,subtitle,1.25,color='#596269'))
    heading(9,15,32,'01  THROUGH POWER')
    heading(46,58,36,'02  MEASUREMENT','Kelvin current + output voltage')
    heading(46,148,44,'03  INLINE SUPPLY','Taken upstream of the shunt')
    heading(45,220,91,'04  TRANSPARENT CONTACTS','Same J1 and P1 as above. No inline PD controller or substituted contract.')
    heading(227,15,66,'05  REPORTING USB')
    heading(280,102,70,'06  ACQUISITION + FIRMWARE')
    heading(225,208,91,'07  PC SUPPLY + SUSPEND')
    heading(189,59,34,'ISOLATED I²C')
    # Internal insulation boundary, not an electrical connection.
    symbols.append('<path d="M 2060,835 L 2060,965" stroke="#b7a77b" stroke-width="2" stroke-dasharray="7 6"/>')

    drawn={key[0] for key in ports}
    assert drawn==set(components), ('Missing components',set(components)-drawn)
    expected={(c['ref'],p['number']):p['net'] for c in components.values() for p in c['pins'] if p['net'] is not None}
    assert {key:value[1] for key,value in ports.items()}==expected
    bynet=defaultdict(set)
    # Pin exit corridors are available only to their owning net.
    corridors={}
    for (ref,num),(xy,net,inward) in ports.items():
        bynet[net].add(xy)
        for i in range(4):
            p=(xy[0]+inward[0]*i,xy[1]+inward[1]*i)
            if p in corridors: assert corridors[p]==net,(ref,num,p)
            corridors[p]=net
    # Reserve fixed headings and footer away from wire routing.
    blocked.update((x,y) for x in range(W+1) for y in list(range(0,7))+list(range(288,H+1)))
    # Each routed grid node records incident directions for each net.
    used=defaultdict(dict)
    edges={}
    netedges=defaultdict(set)
    dirs=[(1,0),(-1,0),(0,1),(0,-1)]
    def edge(a,b):return tuple(sorted((a,b)))
    def allowed(p,net):
        x,y=p
        return 4<=x<=W-4 and 7<=y<288 and (p not in blocked or corridors.get(p)==net) and (p not in terminals_owner or terminals_owner[p]==net)
    terminals_owner={xy:net for xy,net,inward in ports.values()}
    for xy,net,inward in ports.values():
        for i in range(2):
            a=(xy[0]+inward[0]*i,xy[1]+inward[1]*i)
            b=(a[0]+inward[0],a[1]+inward[1])
            d=dirs.index(inward)
            e=edge(a,b)
            edges[e]=net;netedges[net].add(e)
            used[a].setdefault(net,set()).add(d)
            used[b].setdefault(net,set()).add(d^1)
    def route(start,tree,net):
        nearest=min(tree,key=lambda p:(abs(p[0]-start[0])+abs(p[1]-start[1]),p))
        heap=[(0,0,start,-1)]
        dist={(start,-1):0}; prev={}
        while heap:
            _,cost,p,d=heapq.heappop(heap)
            state=p,d
            if dist.get(state)!=cost:continue
            if p in tree:
                path=[p]
                while state in prev:
                    state=prev[state];path.append(state[0])
                return path[::-1]
            for nd,(dx,dy) in enumerate(dirs):
                q=p[0]+dx,p[1]+dy
                if not allowed(q,net):continue
                e=edge(p,q)
                if e in edges and edges[e]!=net:continue
                # At any foreign wire, continue straight and cross perpendicular.
                foreign=[ds for n,ds in used[p].items() if n!=net]
                if foreign and (nd!=d or any(len(ds)!=2 or set(ds) not in ({0,1},{2,3}) or nd in ds for ds in foreign)):continue
                foreignq=[ds for n,ds in used[q].items() if n!=net]
                if foreignq and any(len(ds)!=2 or set(ds) not in ({0,1},{2,3}) or (nd^1) in ds for ds in foreignq):continue
                turn=5 if d!=-1 and d!=nd else 0
                cross=32 if foreignq else 0
                adjacent=sum(bool(used.get((q[0]+ax,q[1]+ay))) for ax,ay in dirs)
                nc=cost+10+turn+cross+adjacent*2
                ns=q,nd
                if nc>=dist.get(ns,float('inf')):continue
                dist[ns]=nc;prev[ns]=p,d
                heuristic=(abs(q[0]-nearest[0])+abs(q[1]-nearest[1]))*10
                heapq.heappush(heap,(nc+heuristic,nc,q,nd))
        raise RuntimeError(f'Cannot route {net} from {start}')
    # Short/local nets first, then global supply/ground trees.
    order=sorted(bynet,key=lambda n:(0 if n.startswith(('CONTACT','INLINE_D','SHIELD_INLINE')) else 1 if n.startswith(('GND','3V3')) else 2, (max(x for x,y in bynet[n])-min(x for x,y in bynet[n])+max(y for x,y in bynet[n])-min(y for x,y in bynet[n])),n))
    for net in order:
        todo=set(bynet[net]);tree={min(todo)};todo-=tree
        while todo:
            start=min(todo,key=lambda p:(min(abs(p[0]-q[0])+abs(p[1]-q[1]) for q in tree),p))
            path=route(start,tree,net)
            for a,b in zip(path,path[1:]):
                e=edge(a,b);assert e not in edges or edges[e]==net
                edges[e]=net;netedges[net].add(e)
                d=dirs.index((b[0]-a[0],b[1]-a[1]))
                used[a].setdefault(net,set()).add(d)
                used[b].setdefault(net,set()).add(d^1)
            tree.update(path);todo-=tree
        print(f'{net}: {len(bynet[net])} terminals, {len(netedges[net])} wire segments',flush=True)
    # Independently flood every rendered wire tree and compare the source pin netlist.
    for net,terminals in bynet.items():
        adj=defaultdict(set)
        for a,b in netedges[net]:adj[a].add(b);adj[b].add(a)
        seen=set();stack=[next(iter(terminals))]
        while stack:
            p=stack.pop()
            if p in seen:continue
            seen.add(p);stack.extend(adj[p]-seen)
        assert terminals<=seen,(net,'disconnected pins')
    for p,nets in used.items():
        if len(nets)>1:
            assert len(nets)==2 and {frozenset(ds) for ds in nets.values()}=={frozenset((0,1)),frozenset((2,3))}, ('Ambiguous crossing',p,nets)
    def domain(net):return 'INLINE' if any(components[r]['domain']=='INLINE' for (r,p),v in ports.items() if v[1]==net) else 'PC'
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*G}" height="{H*G}" viewBox="0 0 {W*G} {H*G}" role="img" aria-labelledby="title desc">',
         '<title id="title">Power Widget — complete single-sheet schematic, bench revision A</title>',
         '<desc id="desc">All 82 physical components and 65 nets on one page. Continuous wires, junction dots and bridged crossings; no off-sheet connections. Green: inline circuit. Blue: isolated PC circuit. Pin groups list every connected pin number. NC pins are listed within the package. Derived from circuit.json; this is a documentation drawing, not the editable KiCad project.</desc>',
         '<rect width="100%" height="100%" fill="white"/>',
         '<g font-family="DejaVu Sans, sans-serif">',
         text(6,4,'POWER WIDGET',2.8,weight='bold'),text(45,4,'BENCH REVISION A  ·  COMPLETE SINGLE-SHEET SCHEMATIC',1.8),
         text(415,4,'28 V design target  /  9 A target  /  SELECTED USB PARTS: 5 A MAX',1.4,'end'),
         '<path d="M 2060,75 L 2060,770 M 2060,990 L 2060,1450 L 1860,1450 L 1860,2860" stroke="#b7a77b" stroke-width="2" stroke-dasharray="9 8" fill="none"/>',
         text(202,11,'INLINE',1.5,'end','bold',COLORS['INLINE']),text(210,11,'ISOLATED PC',1.5,weight='bold',color=COLORS['PC'])]
    # Draw maximal straight runs so SVG stays small and junction geometry is exact.
    horizontal_runs=defaultdict(list)
    for net in sorted(netedges):
        runs=defaultdict(list)
        for (x1,y1),(x2,y2) in netedges[net]:
            if y1==y2:runs['h',y1].append(x1)
            else:runs['v',x1].append(y1)
        color=COLORS[domain(net)]
        width=2.7 if net.startswith(('VBUS','GND','3V3')) else 1.6
        svg.append(f'<g data-net="{esc(net)}"><title>{esc(net)}</title>')
        for (axis,fixed),values in sorted(runs.items()):
            values=sorted(values);start=last=values[0]
            for v in values[1:]+[None]:
                if v is not None and v==last+1:last=v;continue
                a,b=((start,fixed),(last+1,fixed)) if axis=='h' else ((fixed,start),(fixed,last+1))
                svg.append(line(a,b,color,width))
                if axis=='h':horizontal_runs[net].append((a,b))
                start=last=v
        svg.append('</g>')
    svg.extend(symbols)
    crossings=0
    for (x,y),nets in sorted(used.items()):
        if not nets: continue
        if len(nets)>1:
            crossings+=1
            vnet=next(n for n,ds in nets.items() if ds=={2,3})
            color=COLORS[domain(vnet)]
            # White clearance plus a semicircular hop: crossing, never a junction.
            svg.append(f'<path d="M {x*G},{y*G-4} A 4,4 0 0 1 {x*G},{y*G+4}" fill="none" stroke="white" stroke-width="5.5"/>')
            svg.append(f'<path d="M {x*G},{y*G-4} L {x*G},{y*G+4}" stroke="white" stroke-width="4"/>')
            svg.append(f'<path d="M {x*G},{y*G-4} A 4,4 0 0 1 {x*G},{y*G+4}" fill="none" stroke="{color}" stroke-width="1.6"/>')
        else:
            net,ds=next(iter(nets.items()))
            if len(ds)>=3:svg.append(f'<circle cx="{x*G}" cy="{y*G}" r="3.7" fill="{COLORS[domain(net)]}"/>')
    # Names annotate existing continuous rails; they never stand in for a wire.
    preferred={'VBUS_A':(55,27),'VBUS_B':(123,27),
               'GND_INLINE':(70,190),'3V3_INLINE':(133,145),
               'GND_PC':(280,259),'3V3_PC':(281,200),
               '3V3_ISO_PC':(243,65),'SDA_INLINE':(150,90),
               'SCL_INLINE':(150,94),'SDA_PC':(243,91),'SCL_PC':(253,94)}
    for net,(tx,ty) in preferred.items():
        length=int(len(net)*.72+1)
        candidates=[]
        for (x1,y),(x2,_) in horizontal_runs[net]:
            for x in range(x1+1,x2-length):
                for above in (True,False):
                    yy=y-2 if above else y+1
                    box={(xx,yyy) for xx in range(x,x+length+1) for yyy in range(yy,yy+2)}
                    if any(p in blocked or used.get(p) for p in box):continue
                    candidates.append((abs(x-tx)+abs(y-ty),x,y,above,box))
        if candidates:
            _,x,y,above,box=min(candidates,key=lambda c:c[:4])
            blocked.update(box)
            svg.append(text(x,y-.65 if above else y+1.8,net,1.15,color=COLORS[domain(net)]))

    svg.extend([line((6,288),(414,288),'#b2b7ba'),
        text(6,292,'READING THE DRAWING',1.5,weight='bold'),
        text(6,295,'Dot = connected. Hop = no connection. Comma-separated pins are tied. NC = unconnected. J1 / P1 each appear in two sections.',1.25),
        text(6,298,'Green = inline domain; blue = PC domain. GND_INLINE and GND_PC are separate. U2 is the signal isolation barrier.',1.35),
        text(191,292,'82 components · 65 nets · 1 sheet · no off-sheet labels',1.5,weight='bold'),
        text(191,295,'JP1: fit ONE shunt, 1–2 normal / 2–3 external. JP2 and JP3 fitted. JP4 not fitted. Switches shown released.',1.25),
        text(191,298,'Engineering draft; unbuilt and unqualified. Complete values / pin data: circuit.json. Editable circuit: KiCad project.',1.25),
        '</g></svg>'])
    output='\n'.join(svg)+'\n'
    report={
        'source':'circuit.json','source_sha256':hashlib.sha256(raw).hexdigest(),
        'components':len(components),'nets':len(bynet),'connected_numbered_pins':len(ports),
        'unconnected_numbered_pins':sum(p['net'] is None for c in components.values() for p in c['pins']),
        'nonphysical_erc_flags_omitted':sum(c['kind']=='flag' for c in circuit['components']),
        'all_source_pins_accounted_for':True,'all_nets_continuously_connected':True,
        'foreign_shared_wire_edges':0,'ambiguous_crossings':0,'bridged_crossings':crossings,
        'scope':'Documentation drawing connectivity, not KiCad ERC or hardware validation.',
    }
    for name,data in [('single-sheet.svg',output),('single-sheet-check.json',json.dumps(report,indent=2)+'\n')]:
        path=OUT/name
        if args.check:
            if not path.exists() or path.read_text()!=data:raise SystemExit(f'Stale: {path.relative_to(ROOT)}')
        else:path.write_text(data)
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
