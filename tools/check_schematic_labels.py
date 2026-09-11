"""Check actual KiCad-rendered lettering against native wires."""
import re
import xml.etree.ElementTree as ET

NUMBER = r'-?\d+(?:\.\d+)?'
WIRE = re.compile(r'\(wire\s+\(pts\s+\(xy\s+('+NUMBER+r')\s+('+NUMBER+r')\)\s+\(xy\s+('+NUMBER+r')\s+('+NUMBER+r')\)')
SVG = '{http://www.w3.org/2000/svg}'


def text_boxes(svg):
    """Use plotted stroke coordinates, not estimated font metrics."""
    result = []
    for group in ET.parse(svg).getroot().iter(SVG+'g'):
        if group.attrib.get('class') != 'stroked-text':
            continue
        desc = group.find(SVG+'desc')
        if desc is None:
            continue
        points = []
        for path in group.iter(SVG+'path'):
            values = list(map(float, re.findall(NUMBER, path.attrib.get('d', ''))))
            points.extend(zip(values[::2], values[1::2]))
        if points:
            xs, ys = zip(*points)
            result.append((desc.text or '', (min(xs), min(ys), max(xs), max(ys))))
    return list(dict.fromkeys(result))


def intersects(wire, box, clearance=0.15):
    x1, y1, x2, y2 = wire
    left, top, right, bottom = box
    return (max(min(x1, x2), left-clearance) <= min(max(x1, x2), right+clearance)
            and max(min(y1, y2), top-clearance) <= min(max(y1, y2), bottom+clearance))


def check(schematic, svg, nets):
    wires = [tuple(map(float, match)) for match in WIRE.findall(schematic.read_text())]
    all_text = text_boxes(svg)
    labels = [(name, box) for name, box in all_text if name in nets]
    assert sorted(name for name, box in labels) == sorted(nets), 'Missing or duplicate rendered net labels'
    overlaps = [(name, wire) for name, box in all_text for wire in wires if intersects(wire, box)]
    if overlaps:
        raise AssertionError(f'{len(overlaps)} wire/text collisions in native export: {overlaps[:8]}')
    collisions = [(name, other) for i, (name, box) in enumerate(all_text)
                  for other, other_box in all_text[i+1:]
                  if max(box[0], other_box[0]) < min(box[2], other_box[2])
                  and max(box[1], other_box[1]) < min(box[3], other_box[3])]
    if collisions:
        raise AssertionError(f'{len(collisions)} text/text collisions in native export: {collisions[:8]}')
    return len(labels)
