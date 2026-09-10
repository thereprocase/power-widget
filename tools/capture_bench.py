#!/usr/bin/env python3
"""Reproduce the bench circuit, native KiCad draft and SVG connection sheets.

The pin-level circuit below is authoritative until interactive KiCad review.
This generator does not replace KiCad ERC, footprint review, or PCB layout.
Format reference: https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/
"""
import argparse
import html
import json
from pathlib import Path
import uuid

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'hardware/bench-rev-a'
NS = uuid.UUID('de3b4f8f-ed23-4c82-9816-4470ab137d7a')
def uid(key): return str(uuid.uuid5(NS, key))
def q(s): return json.dumps(str(s), ensure_ascii=False)
def fx(n): return f'{n:.3f}'.rstrip('0').rstrip('.')
def effect(size=1.0, extra=''): return f'(effects (font (size {size} {size})) {extra})'

SHEETS = {
 '01-inline': ('Inline path', 'INLINE', '9 A target / 10.8 A margin. Connector assemblies UNQUALIFIED. Force terminals parallel the USB ports.'),
 '02-sensing': ('Sensing and isolation', 'MIXED', 'PC and INLINE grounds stay separate. U2 is the only signal crossing. Kelvin routing is a PCB requirement.'),
 '03-supplies': ('Local supplies', 'MIXED', 'JP1: 1-2 normal; 2-3 floating external 3.3 V. Fit ONE shunt. No isolated power converter is fitted.'),
 '04-usb-mcu': ('Reporting USB and MCU', 'PC', 'All circuits here are PC domain. No inline USB or CC signal reaches U3. USB port footprint remains open.'),
 '05-debug': ('Firmware debug access', 'PC', 'SWD VTref is a reference, not a power input. Headers use PC ground. Never jumper them to inline ground.')
}
C = []
def add(ref, value, sheet, pins, domain, kind='block', footprint='', note=''):
    # pins: (number, function, net or None, optional electrical type)
    C.append(dict(ref=ref, value=value, sheet=sheet, domain=domain,
                  kind=kind, footprint=footprint, note=note,
                  pins=[dict(number=str(p[0]),name=p[1],net=p[2],
                             type=p[3] if len(p)>3 else 'passive') for p in pins]))
def two(ref, value, sheet, a, b, domain, kind='R', note=''):
    add(ref,value,sheet,[('1','',a),('2','',b)],domain,kind,note=note)
def header(ref, value, sheet, nets, domain, note=''):
    add(ref,value,sheet,[(str(i+1),'',n) for i,n in enumerate(nets)],domain,'header',note=note)

I='INLINE'; P='PC'
power={'A4','A9','B4','B9'}; ground={'A1','A12','B1','B12'}
signal={'A5':'CONTACT_A5','B5':'CONTACT_B5','A6':'INLINE_DP','B6':'INLINE_DP',
        'A7':'INLINE_DM','B7':'INLINE_DM','A8':'CONTACT_A8','B8':'CONTACT_B8'}
for row in 'AB':
    for pin in (2,3,10,11): signal[f'{row}{pin}']=f'CONTACT_{row}{pin}'
def usb_pins(bus, reporting=False, plug=False):
    r=[]
    for row in 'AB':
        for n in range(1,13):
            k=f'{row}{n}'
            if plug and k in {'B6','B7'}:continue
            if k in power: net=bus
            elif k in ground:net='GND_PC' if reporting else 'GND_INLINE'
            elif reporting:net={'A5':'PC_CC1','B5':'PC_CC2','A6':'PC_DP_CONN','B6':'PC_DP_CONN',
                                'A7':'PC_DM_CONN','B7':'PC_DM_CONN'}.get(k)
            else:net=signal[k]
            r.append((k,k,net))
    r.append(('S','SHIELD','SHIELD_PC' if reporting else 'SHIELD_INLINE'))
    return r
add('J1','Inline USB-C receptacle; MPN open','01-inline',usb_pins('VBUS_A'),I,
    note='All 24 contacts exposed; current rating not established. Do not substitute a power-only connector.')
add('P1','Custom captive USB-C plug','01-inline',usb_pins('VBUS_B',plug=True),I,
    note='Two independent CC-contact conductors; no e-marker or Rp/Rd/Ra. Pin-to-pad drawing required.')
add('R1','WSK25125L000DEA / 5mR 1W','01-inline',[
 ('1','I1','VBUS_A'),('2','I2','VBUS_B'),('3','E1','SHUNT_SA'),('4','E2','SHUNT_SB')],I,
 note='Symbol uses project numbering 1=I1, 2=I2, 3=E1, 4=E2. Footprint mapping MUST be checked against Vishay drawing.')
header('J2','Force A: source / input','01-inline',['VBUS_A','GND_INLINE'],I,
       'Select terminal/bolted connection rated for at least 10.8 A continuous; no breadboard wiring.')
header('J3','Force B: load / output','01-inline',['VBUS_B','GND_INLINE'],I,
       'Live in parallel with P1. Disconnect OEM devices before independent bench injection.')
header('J4','Kelvin probe pads; NOT force pins','01-inline',['SHUNT_SA','SHUNT_SB','VBUS_B','GND_INLINE'],I,
       'Use small pads near the defined B-plane. No main current through this header.')
for ref,net in [('TP1','VBUS_A'),('TP2','VBUS_B'),('TP3','GND_INLINE'),('TP4','CONTACT_A5'),('TP5','CONTACT_B5'),
                ('TP6','INLINE_DP'),('TP7','INLINE_DM'),('TP8','CONTACT_A8'),('TP9','CONTACT_B8')]:
    add(ref,net,'01-inline',[('1','',net)],I,'tp')
two('R2','0R shield bond','01-inline','SHIELD_INLINE','GND_INLINE',I)

add('U1','INA228AIDGSR','02-sensing',[
 ('1','A1','GND_INLINE','input'),('2','A0','GND_INLINE','input'),('3','ALERT','ALERT_INLINE','open_collector'),
 ('4','SDA','SDA_INLINE','bidirectional'),('5','SCL','SCL_INLINE','input'),('6','VS','3V3_INLINE','power_in'),
 ('7','GND','GND_INLINE','power_in'),('8','VBUS','VBUS_FILTER','input'),('9','IN-','SHUNT_MINUS','input'),
 ('10','IN+','SHUNT_PLUS','input')],I,footprint='Package_SO:VSSOP-10_3x3mm_P0.5mm',
 note='Address 0x40. Wide ADC range. Footprint candidate still requires package drawing review.')
add('U2','ISO1641BD','02-sensing',[
 ('1','VCC1','3V3_ISO_PC','power_in'),('2','SDA1','SDA_PC','bidirectional'),('3','SCL1','SCL_PC','input'),
 ('4','GND1','GND_PC','power_in'),('5','GND2','GND_INLINE','power_in'),('6','SCL2','SCL_INLINE','open_collector'),
 ('7','SDA2','SDA_INLINE','bidirectional'),('8','VCC2','3V3_INLINE','power_in')],'BARRIER',
 footprint='Package_SO:SOIC-8_3.9x4.9mm_P1.27mm',note='Side 1 PC, side 2 inline. SCL is unidirectional; INA228 does not require clock stretching.')
two('R3','10R 0.1% matched','02-sensing','SHUNT_SA','SHUNT_PLUS',I)
two('R4','10R 0.1% matched','02-sensing','SHUNT_SB','SHUNT_MINUS',I)
two('C1','100nF 50V differential','02-sensing','SHUNT_PLUS','SHUNT_MINUS',I,'C')
two('R5','100R','02-sensing','VBUS_B','VBUS_FILTER',I)
two('C2','10nF 63V','02-sensing','VBUS_FILTER','GND_INLINE',I,'C')
two('C3','100nF 10V at U1','02-sensing','3V3_INLINE','GND_INLINE',I,'C')
two('C4','100nF 10V at U2.8','02-sensing','3V3_INLINE','GND_INLINE',I,'C')
two('C5','100nF 10V at U2.1','02-sensing','3V3_ISO_PC','GND_PC',P,'C')
for ref,net,dom in [('R6','SDA_PC',P),('R7','SCL_PC',P),('R8','SDA_INLINE',I),('R9','SCL_INLINE',I)]:
    two(ref,'2k2 pull-up','02-sensing',net,'3V3_ISO_PC' if dom==P else '3V3_INLINE',dom)
header('J5','PC I2C / external MCU','02-sensing',['GND_PC','3V3_ISO_PC','SCL_PC','SDA_PC'],P,
       '3V3 is switched reference/output. Hold onboard MCU in reset and fit JP4 for another open-drain master; no external pull-ups to an always-on rail.')
header('J6','INLINE I2C debug','02-sensing',['GND_INLINE','3V3_INLINE','SCL_INLINE','SDA_INLINE'],I,
       'Only a floating or isolated instrument here; never jumper to J5.')
add('TP10','ALERT: floating scope only','02-sensing',[('1','', 'ALERT_INLINE')],I,'tp',
    note='No pull-up fitted; open drain requires a local pull-up if probing logic. Firmware polls status.')

add('U4','TPS7A1601DGNR','03-supplies',[
 ('1','OUT','3V3_INLINE_LDO','power_out'),('2','FB','INLINE_FB','input'),('3','PG',None,'open_collector'),
 ('4','GND','GND_INLINE','power_in'),('5','EN','INLINE_LDO_IN','input'),('6','NC',None),
 ('7','DELAY',None),('8','IN','INLINE_LDO_IN','power_in'),('9','EP','GND_INLINE','power_in')],I,
 note='60 V component rating is not a system overvoltage cutoff. EP numbering to be checked with footprint.')
header('JP3','INLINE self-current link','03-supplies',['VBUS_A','INLINE_FEED'],I,
       'Fit shunt normally; insert a floating ammeter to characterize sensor-side self-consumption. Not a main-current connection.')
two('R10','47R 0.25W branch feed','03-supplies','INLINE_FEED','INLINE_LDO_IN',I)
two('C6','1uF 63V effective >=0.1uF','03-supplies','INLINE_LDO_IN','GND_INLINE',I,'C')
two('R11','178k 0.1%','03-supplies','3V3_INLINE_LDO','INLINE_FB',I)
two('R12','100k 0.1%','03-supplies','INLINE_FB','GND_INLINE',I)
two('C7','4u7 10V effective >=2u2','03-supplies','3V3_INLINE_LDO','GND_INLINE',I,'C')
header('JP1','SENSOR SUPPLY: one shunt only','03-supplies',['3V3_INLINE_LDO','3V3_INLINE','EXT_3V3_INLINE'],I,
       'Normal 1-2; floating external 3.3 V 2-3. Do not install two shunts.')
header('J7','Floating external 3.3V','03-supplies',['EXT_3V3_INLINE','GND_INLINE'],I,
       'For zero-VBUS/low-voltage bench testing; not connected to PC supply.')
add('U5','TLV75533PDBVR','03-supplies',[
 ('1','IN','PC_5V_LDO','power_in'),('2','GND','GND_PC','power_in'),('3','EN','PC_5V_LDO','input'),
 ('4','NC',None),('5','OUT','3V3_PC','power_out')],P,footprint='Package_TO_SOT_SMD:SOT-23-5')
header('JP2','PC supply current link','03-supplies',['VBUS_PC','PC_5V_LDO'],P,
       'Fit shunt normally. Remove to measure reporting-domain supply current; no external power injection.')
two('C8','1uF 10V','03-supplies','PC_5V_LDO','GND_PC',P,'C')
two('C9','4u7 10V','03-supplies','3V3_PC','GND_PC',P,'C')
two('C10','1uF 10V at connector','03-supplies','VBUS_PC','GND_PC',P,'C')
add('U7','TPS22919DCKR','03-supplies',[
 ('1','IN','3V3_PC','power_in'),('2','GND','GND_PC','power_in'),('3','ON','ISO_EN_PC','input'),
 ('4','NC',None),('5','QOD','3V3_ISO_PC'),('6','VOUT','3V3_ISO_PC','power_out')],P,
 footprint='Package_TO_SOT_SMD:SOT-363_SC-70-6',
 note='Switch U2 side 1 and its pull-ups off in USB suspend. Set PB6/PB7 high impedance first. QOD tied to output.')
two('R25','100k enable pull-down','03-supplies','ISO_EN_PC','GND_PC',P)
two('C18','100nF 10V at U7.1','03-supplies','3V3_PC','GND_PC',P,'C')
two('C19','1uF 10V at U7.6','03-supplies','3V3_ISO_PC','GND_PC',P,'C')
header('JP4','External-master enable; DNF','03-supplies',['3V3_PC','ISO_FORCE_PC'],P,
       'Fit only for external-master bench use with U3 held reset; remove for USB suspend testing.')
two('R26','10k override limiter','03-supplies','ISO_FORCE_PC','ISO_EN_PC',P)

add('J8','PC reporting USB-C; MPN open','04-usb-mcu',usb_pins('VBUS_PC',reporting=True),P,
    note='Long board edge. USB 2.0 receptacle may omit unused SS/SBU contacts after exact footprint selection.')
mp={1:'VBAT',2:'PC13',3:'PC14',4:'PC15',5:'PF0',6:'PF1',7:'NRST',8:'VSSA',9:'VDDA',10:'PA0',11:'PA1',
    12:'PA2',13:'PA3',14:'PA4',15:'PA5',16:'PA6',17:'PA7',18:'PB0',19:'PB1',20:'PB2',21:'PB10',22:'PB11',
    23:'VSS',24:'VDD',25:'PB12',26:'PB13',27:'PB14',28:'PB15',29:'PA8',30:'PA9',31:'PA10',32:'PA11',
    33:'PA12',34:'PA13',35:'VSS',36:'VDDIO2',37:'PA14',38:'PA15',39:'PB3',40:'PB4',41:'PB5',42:'PB6',
    43:'PB7',44:'BOOT0',45:'PB8',46:'PB9',47:'VSS',48:'VDD'}
mn={'VBAT':'3V3_PC','VSSA':'GND_PC','VDDA':'VDDA_PC','VSS':'GND_PC','VDD':'3V3_PC','VDDIO2':'3V3_PC',
    'NRST':'NRST_PC','BOOT0':'BOOT0_PC','PA0':'PC_VBUS_DETECT','PA1':'ISO_EN_PC','PA2':'UART_TX_PC','PA3':'UART_RX_PC',
    'PA4':'GPIO_PA4','PA5':'GPIO_PA5','PA6':'GPIO_PA6','PA7':'GPIO_PA7','PB10':'GPIO_PB10','PB11':'GPIO_PB11',
    'PB0':'BUTTON_PC','PB1':'LED_PC','PA11':'USB_DM_MCU','PA12':'USB_DP_MCU','PA13':'SWDIO_PC','PA14':'SWCLK_PC',
    'PB6':'SCL_PC','PB7':'SDA_PC'}
def mtype(n):
    if n in {'VBAT','VSSA','VDDA','VSS','VDD','VDDIO2'}:return 'power_in'
    if n in {'BOOT0'}:return 'input'
    return 'bidirectional'
add('U3','STM32F072CBT6 / 128K flash','04-usb-mcu',[(str(k),v,mn.get(v),mtype(v)) for k,v in mp.items()],P,
    footprint='Package_QFP:LQFP-48_7x7mm_P0.5mm',note='Pinout checked against ST DS9826 Rev 6 figure 8. 16 KB RAM. HSI48/CRS USB clock.')
add('U6','USBLC6-2SC6','04-usb-mcu',[
 ('1','IO1','PC_DP_CONN'),('2','GND','GND_PC'),('3','IO2','PC_DM_CONN'),
 ('4','IO2','PC_DM_CONN'),('5','VBUS','VBUS_PC'),('6','IO1','PC_DP_CONN')],P,
 footprint='Package_TO_SOT_SMD:SOT-23-6',note='Route lines through paired pads with short ground return. PC port only.')
two('R13','5k1 1% Rd','04-usb-mcu','PC_CC1','GND_PC',P)
two('R14','5k1 1% Rd','04-usb-mcu','PC_CC2','GND_PC',P)
two('R15','0R tuning footprint','04-usb-mcu','PC_DP_CONN','USB_DP_MCU',P)
two('R16','0R tuning footprint','04-usb-mcu','PC_DM_CONN','USB_DM_MCU',P)
for ref,pin in [('C11','24'),('C12','48'),('C13','36'),('C14','1')]:
    two(ref,'100nF 10V at U3.'+pin,'04-usb-mcu','3V3_PC','GND_PC',P,'C')
two('R17','10R VDDA filter','04-usb-mcu','3V3_PC','VDDA_PC',P)
two('C15','100nF 10V at U3.9','04-usb-mcu','VDDA_PC','GND_PC',P,'C')
two('C16','1uF 10V','04-usb-mcu','VDDA_PC','GND_PC',P,'C')
two('R18','100k 1%','04-usb-mcu','VBUS_PC','PC_VBUS_DETECT',P)
two('R19','100k 1%','04-usb-mcu','PC_VBUS_DETECT','GND_PC',P)
two('R20','0R PC shell bond','04-usb-mcu','SHIELD_PC','GND_PC',P)

add('J9','Cortex SWD 2x5 1.27mm','05-debug',[
 ('1','VTref','3V3_PC'),('2','SWDIO','SWDIO_PC'),('3','GND','GND_PC'),('4','SWCLK','SWCLK_PC'),
 ('5','GND','GND_PC'),('6','SWO-NC',None),('7','KEY',None),('8','NC',None),('9','GNDDetect','GND_PC'),
 ('10','nRESET','NRST_PC')],P,'header',note='Key pin 7 absent. No SWO on Cortex-M0. Debug probe must not power this board.')
header('J10','UART 3.3V logic','05-debug',['GND_PC','UART_TX_PC','UART_RX_PC','3V3_PC'],P,
       'TX/RX named from board viewpoint; 3V3 reference only. Not RS-232 voltage levels.')
header('J11','Spare GPIO / SPI','05-debug',['GND_PC','3V3_PC','GPIO_PA4','GPIO_PA5','GPIO_PA6','GPIO_PA7','GPIO_PB10','GPIO_PB11'],P)
two('R21','10k reset pull-up','05-debug','3V3_PC','NRST_PC',P)
two('C17','100nF reset','05-debug','NRST_PC','GND_PC',P,'C')
two('SW1','RESET pushbutton','05-debug','NRST_PC','GND_PC',P,'SW')
two('R22','10k boot pull-down','05-debug','BOOT0_PC','GND_PC',P)
two('SW2','BOOT pushbutton','05-debug','BOOT0_PC','3V3_PC',P,'SW')
two('R23','10k button pull-up','05-debug','3V3_PC','BUTTON_PC',P)
two('SW3','USER pushbutton','05-debug','BUTTON_PC','GND_PC',P,'SW')
two('R24','1k LED limiter','05-debug','LED_PC','LED_ANODE_PC',P)
add('D1','Activity LED','05-debug',[('1','K','GND_PC'),('2','A','LED_ANODE_PC')],P,'LED')

# Basic connectivity review, independent of the visual placement.
assert len({c['ref'] for c in C}) == len(C)
byref={c['ref']:c for c in C}
for c in C:
    assert len({p['number'] for p in c['pins']}) == len(c['pins'])
net_domains={}
for c in C:
    if c['domain']=='BARRIER':continue
    for p in c['pins']:
        if p['net']:net_domains.setdefault(p['net'],set()).add(c['domain'])
assert all(len(v)==1 for v in net_domains.values()), 'Unintended shared PC/inline net'
assert {c['ref'] for c in C if c['domain']=='BARRIER'} == {'U2'}
for n in ('CONTACT_A5','CONTACT_B5'):
    attached={c['ref'] for c in C for p in c['pins'] if p['net']==n}
    assert attached == {'J1','P1','TP4' if n=='CONTACT_A5' else 'TP5'}
assert {p['number'] for p in byref['U3']['pins']}=={str(i) for i in range(1,49)}
assert {p['number']:p['net'] for p in byref['U3']['pins']}['36']=='3V3_PC'

# Self-contained embedded symbols keep drafts independent of local library versions.
def geometry(c):
    ps=c['pins']; n=(len(ps)+1)//2
    h=max(10.16, (n-1)*2.54+10.16)
    bw=35.56 if len(ps)>8 else (25.4 if len(ps)>2 else 10.16)
    pp=[]
    for i,p in enumerate(ps):
        side=0 if i<n else 1; j=i if side==0 else i-n
        y=(n-1)*1.27-j*2.54
        pp.append((p,-bw/2-3.81 if side==0 else bw/2+3.81,y,0 if side==0 else 180))
    return bw,h,pp

def lib(c):
    name='C_'+c['ref']; bw,h,pp=geometry(c)
    lines=[f'(symbol "Bench:{name}" (pin_names (offset 0.6)) (in_bom yes) (on_board yes)',
      f'(property "Reference" {q(c["ref"].rstrip("0123456789"))} (at 0 {fx(h/2+2)} 0) {effect()})',
      f'(property "Value" {q(c["value"])} (at 0 {fx(-h/2-2)} 0) {effect()})',
      f'(symbol "{name}_0_1" (rectangle (start {fx(-bw/2)} {fx(h/2)}) (end {fx(bw/2)} {fx(-h/2)}) (stroke (width 0.254) (type default)) (fill (type background))))',
      f'(symbol "{name}_1_1"']
    for p,x,y,a in pp:
        lines.append(f'(pin {p["type"]} line (at {fx(x)} {fx(y)} {a}) (length 3.81) (name {q(p["name"])} {effect(0.9)}) (number {q(p["number"])} {effect(0.9)}))')
    lines+=['))'];return '\n'.join(lines)

def positions(cs):
    out=[]; y=36
    for start in range(0,len(cs),4):
        group=cs[start:start+4]; hh=max(geometry(c)[1] for c in group)
        for col,c in enumerate(group):out.append((c,75+145*col,y+hh/2))
        y+=hh+28
    assert y<386, ('Sheet too tall', y)
    return out

outputs={}
rootid=uid('root'); project='power-widget-bench'
for sk,(title,domain,note) in SHEETS.items():
    cs=[c for c in C if c['sheet']==sk]; sid=uid('sheet:'+sk)
    placed=positions(cs)
    head=[f'(kicad_sch (version 20231120) (generator "power_widget") (uuid {q(uid("file:"+sk))}) (paper "A2")',
      f'(title_block (title {q(title)}) (date "2026-09-10") (rev "A-DRAFT") (company "Power Widget") (comment 1 "NOT FOR FABRICATION - ERC AND FOOTPRINT REVIEW PENDING"))',
      '(lib_symbols', '\n'.join(lib(c) for c in cs), ')']
    body=[]
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1782" height="1260" viewBox="0 0 594 420">',
      '<rect width="594" height="420" fill="#fff"/>',
      '<style>text{font-family:DejaVu Sans,sans-serif;fill:#182532}.pin{font-size:2.5px}.net{font-size:2.6px}.ref{font-size:3.8px;font-weight:bold}.value{font-size:3px}</style>',
      f'<text x="12" y="14" font-size="6">{html.escape(title)} / A-DRAFT</text>',
      '<text x="12" y="22" font-size="3.5" fill="#af3d20">Connection-sheet preview — not a KiCad render; ERC and footprints pending</text>']
    for c,cx,cy in placed:
        bw,h,pp=geometry(c); ref=c['ref']; path=f'/{rootid}/{sid}'
        body += [f'(symbol (lib_id "Bench:C_{ref}") (at {cx} {fx(cy)} 0) (unit 1) (in_bom yes) (on_board yes) (dnp no) (uuid {q(uid(ref))})',
          f'(property "Reference" {q(ref)} (at {cx} {fx(cy-h/2-6)} 0) {effect(1.27)})',
          f'(property "Value" {q(c["value"])} (at {cx} {fx(cy-h/2-2.5)} 0) {effect(1.0)})',
          f'(property "Footprint" {q(c["footprint"])} (at {cx} {fx(cy)} 0) {effect(1.0,"hide")})']
        for p,*_ in pp:body.append(f'(pin {q(p["number"])} (uuid {q(uid(ref+":"+p["number"]))}))')
        body.append(f'(instances (project {q(project)} (path {q(path)} (reference {q(ref)}) (unit 1)))))')
        color={'PC':'#e7f0fc','INLINE':'#fff2d7','BARRIER':'#e8e3f6'}[c['domain']]
        svg += [f'<rect x="{cx-bw/2}" y="{cy-h/2}" width="{bw}" height="{h}" fill="{color}" stroke="#354b5d" stroke-width=".35"/>',
            f'<text class="ref" x="{cx}" y="{cy-h/2-6}" text-anchor="middle">{ref}</text>',
            f'<text class="value" x="{cx}" y="{cy-h/2-2.5}" text-anchor="middle">{html.escape(c["value"])}</text>']
        for p,lx,ly,a in pp:
            px=cx+lx; py=cy-ly; sign=-1 if a==0 else 1
            end=px+sign*4; inside=cx+sign*(bw/2-1)
            svg.append(f'<line x1="{cx+sign*bw/2}" y1="{py}" x2="{end}" y2="{py}" stroke="#354b5d" stroke-width=".25"/>')
            svg.append(f'<text class="pin" x="{inside}" y="{py+.8}" text-anchor="{"start" if sign==-1 else "end"}">{html.escape(p["name"] or p["number"])}</text>')
            svg.append(f'<text font-size="1.9" x="{px}" y="{py-.7}" text-anchor="middle">{p["number"]}</text>')
            if p['net'] is None:
                body.append(f'(no_connect (at {fx(px)} {fx(py)}) (uuid {q(uid(ref+":"+p["number"]+":nc"))}))')
                svg.append(f'<text class="net" x="{end+sign}" y="{py+.8}" text-anchor="{"end" if sign==-1 else "start"}">NC</text>')
            else:
                body.append(f'(wire (pts (xy {fx(px)} {fx(py)}) (xy {fx(end)} {fx(py)})) (stroke (width 0) (type default)) (uuid {q(uid(ref+":"+p["number"]+":wire"))}))')
                angle=0 if sign==-1 else 180
                # Global labels join the same named nets across all child sheets.
                body.append(f'(global_label {q(p["net"])} (shape bidirectional) (at {fx(end)} {fx(py)} {angle}) {effect(0.9,"(justify left)")} (uuid {q(uid(ref+":"+p["number"]+":label"))}) (property "Intersheetrefs" "${{INTERSHEET_REFS}}" (at {fx(end)} {fx(py)} {angle}) {effect(0.9,"hide")}))')
                svg.append(f'<text class="net" x="{end+sign}" y="{py+.8}" text-anchor="{"end" if sign==-1 else "start"}">{html.escape(p["net"])}</text>')
    body += [f'(text {q(note)} (at 12 397 0) {effect(1.1,"(justify left)")} (uuid {q(uid(sk+":note"))}))',')']
    svg += [f'<text x="12" y="397" font-size="3">{html.escape(note)}</text>',
      '<text x="12" y="409" font-size="3">Same net names connect across sheets. INLINE = amber; PC = blue; isolation component = purple.</text>','</svg>']
    outputs[OUT/(sk+'.kicad_sch')]='\n'.join(head+body)+'\n'
    outputs[OUT/(sk+'.svg')]='\n'.join(svg)+'\n'

root=[f'(kicad_sch (version 20231120) (generator "power_widget") (uuid {q(rootid)}) (paper "A3")',
 '(title_block (title "Power Widget bench prototype") (date "2026-09-10") (rev "A-DRAFT") (comment 1 "NOT FOR FABRICATION"))', '(lib_symbols)']
for i,(sk,(title,_,_)) in enumerate(SHEETS.items()):
    x=25+(i%2)*195; y=42+(i//2)*67
    root.append(f'(sheet (at {x} {y}) (size 155 36) (stroke (width 0.254) (type default)) (fill (color 0 0 0 0)) (uuid {q(uid("sheet:"+sk))}) (property "Sheetname" {q(title)} (at {x} {y-2} 0) {effect(1.27,"(justify left)")}) (property "Sheetfile" {q(sk+".kicad_sch")} (at {x} {y+38} 0) {effect(1.0,"(justify left)")}) (instances (project {q(project)} (path {q("/"+rootid)} (page {q(i+2)})))))')
root += [f'(text "28 V / 9 A target; 10.8 A margin. Laptop charging roster.\nCaptive contact extension; isolated reporting USB; STM32F072 firmware bench.\nNo PCB layout or qualified connector assembly. Review all footprints and run KiCad ERC before fabrication." (at 25 258 0) {effect(1.1,"(justify left)")} (uuid {q(uid("rootnote"))}))',
 '(sheet_instances (path "/" (page "1")))',')']
outputs[OUT/(project+'.kicad_sch')]='\n'.join(root)+'\n'
outputs[OUT/'circuit.json']=json.dumps({'revision':'A-DRAFT','status':'pin-level draft; no PCB or KiCad ERC',
    'sheets':SHEETS,'components':C},indent=2)+'\n'
netlist={}
for c in C:
    for p in c['pins']:
        if p['net']:netlist.setdefault(p['net'],[]).append(f'{c["ref"]}.{p["number"]}')
outputs[OUT/'connections.json']=json.dumps(netlist,indent=2,sort_keys=True)+'\n'
lines=['# Bench component schedule','', '**Draft, not an orderable BOM.** Empty footprints and open connector MPNs are release blockers. Passive package/value ratings need review.','',
       '| Reference | Value / candidate | Domain | Sheet |','|---|---|---|---|']
for c in C:lines.append(f'| {c["ref"]} | {c["value"]} | {c["domain"]} | {c["sheet"]} |')
lines+=['','## Assembly notes','']
for c in C:
    if c['note']:lines.append(f'- **{c["ref"]}:** {c["note"]}')
outputs[OUT/'component-schedule.md']='\n'.join(lines)+'\n'
# Balanced S-expressions are checked separately from electrical topology.
for p,s in outputs.items():
    if p.suffix!='.kicad_sch':continue
    balance=0; string=False; escape=False
    for ch in s:
        if escape:escape=False;continue
        if string and ch=='\\':escape=True;continue
        if ch=='"':string=not string;continue
        if not string:
            balance += (ch=='(')-(ch==')')
            assert balance>=0,p
    assert not string and balance==0,p
parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
for p,s in outputs.items():
    if args.check:
        if not p.exists() or p.read_text()!=s:raise SystemExit(f'Stale generated file: {p}')
    else:
        p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
print(f'{"Checked" if args.check else "Wrote"} {len(outputs)} files; {len(C)} components; {len(netlist)} nets; domain and CC checks pass. KiCad ERC NOT run.')
