from math import tan, pi
from base64 import b64encode

import xml.etree.ElementTree as ET

ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
ET.register_namespace("svg", "http://www.w3.org/2000/svg")
ET.register_namespace("", "http://www.w3.org/2000/svg")

MESSAGE='&-0123456789ABCDEFGHIJKLMNOPQR/STUVWXYZ  :#@\'="¢.<(+|!$*);¬\\,%_>?'

PIXEL_PER_INCH = 96
PAGE_HEIGHT = (3 + 1/4) * PIXEL_PER_INCH
PAGE_WIDTH = (7 + 3/8) * PIXEL_PER_INCH
SPACE_X = 0.087 * PIXEL_PER_INCH
SPACE_Y = 1/4 * PIXEL_PER_INCH
MARGIN_RIGHT = 0.251 * PIXEL_PER_INCH
CORNER_WIDTH = 1/4 * PIXEL_PER_INCH
CORNER_HEIGHT = CORNER_WIDTH * tan(pi * 60 / 180)
CURVE_DIAMETER = 1/4 * PIXEL_PER_INCH
RECT_WIDTH = 0.056 * PIXEL_PER_INCH
RECT_HEIGHT = 0.126 * PIXEL_PER_INCH

# https://homepage.divms.uiowa.edu/~jones/cards/codes.html
IBM_029 = {
    ' ': 0x000,
    '0': 0x001,
    '1': 0x002,
    '2': 0x004,
    '3': 0x008,
    '4': 0x010,
    '5': 0x020,
    '6': 0x040,
    '7': 0x080,
    '8': 0x100,
    '9': 0x200,
    'A': 0x802,
    'B': 0x804,
    'C': 0x808,
    'D': 0x810,
    'E': 0x820,
    'F': 0x840,
    'G': 0x880,
    'H': 0x900,
    'I': 0xa00,
    'J': 0x402,
    'K': 0x404,
    'L': 0x408,
    'M': 0x410,
    'N': 0x420,
    'O': 0x440,
    'P': 0x480,
    'Q': 0x500,
    'R': 0x600,
    'S': 0x005,
    'T': 0x009,
    'U': 0x011,
    'V': 0x021,
    'W': 0x041,
    'X': 0x081,
    'Y': 0x101,
    'Z': 0x201,
    '&': 0x800,
    '¢': 0x904,
    '.': 0x908,
    '<': 0x910,
    '(': 0x920,
    '+': 0x940,
    '|': 0x980,
    '-': 0x400,
    '!': 0x504,
    '$': 0x508,
    '*': 0x510,
    ')': 0x520,
    ';': 0x540,
    '¬': 0x580,
    '/': 0x003,
    '\\': 0x105, # No character in 029, used backslash from IBMEL
    ',': 0x109,
    '%': 0x111,
    '_': 0x121,
    '>': 0x141,
    '?': 0x181,
    ':': 0x104,
    '#': 0x108,
    '@': 0x110,
    '\'': 0x120,
    '=': 0x140,
    '"': 0x180,
}
STYLE='text { font-family: Monospace; font-size: 12; fill: black; stroke: none; stroke-width: 0.6; } ' \
      'rect { fill:white; stroke: black; stroke-width: 0.6; }'

def generate():
    svg = ET.Element("svg")
    svg.set("xmlns", "http://www.w3.org/2000/svg")
    svg.set("xmlns:svg", "http://www.w3.org/2000/svg")
    svg.set("xmlns:xlink", "http://www.w3.org/1999/xlink")
    svg.set("version", "1.1")
    svg.set("width", f"{PAGE_WIDTH:.4f}")
    svg.set("height", f"{PAGE_HEIGHT:.4f}")

    # CSS stylesheet
    elem = ET.SubElement(svg, "style")
    elem.set("type", "text/css")
    elem.text = STYLE

    # Clipping path for background texture
    elem = ET.SubElement(svg, "defs")
    elem = ET.SubElement(elem, "clipPath")
    elem.set("id", "clippath1")
    elem = ET.SubElement(elem, "path")
    elem.set("x", "0")
    elem.set("y", "0")
    elem.set("d", \
             f"M {CORNER_WIDTH} 0 " \
             f"L {PAGE_WIDTH-CURVE_DIAMETER} 0 " \
             f"C {PAGE_WIDTH-CURVE_DIAMETER/2} 0 {PAGE_WIDTH} {CURVE_DIAMETER/2} {PAGE_WIDTH} {CURVE_DIAMETER} " \
             f"L {PAGE_WIDTH} {PAGE_HEIGHT-CURVE_DIAMETER} " \
             f"C {PAGE_WIDTH} {PAGE_HEIGHT-CURVE_DIAMETER/2} {PAGE_WIDTH-CURVE_DIAMETER/2} {PAGE_HEIGHT} {PAGE_WIDTH-CURVE_DIAMETER} {PAGE_HEIGHT} " \
             f"L {CURVE_DIAMETER} {PAGE_HEIGHT} " \
             f"C {CURVE_DIAMETER/2} {PAGE_HEIGHT} 0 {PAGE_HEIGHT-CURVE_DIAMETER/2} 0 {PAGE_HEIGHT-CURVE_DIAMETER} " \
             f"L 0 {CORNER_HEIGHT} " \
             "Z")

    # Background texture
    with open("texture.jpeg", "rb") as img:
        imgdata = b64encode(img.read()).decode('ASCII')
    elem = ET.SubElement(svg, "image")
    svg.set("width", f"{PAGE_WIDTH:.4f}")
    svg.set("height", f"{PAGE_HEIGHT:.4f}")
    elem.set("style", "image-rendering:optimizeQuality;opacity:0.6;")
    elem.set("xlink:href", "data:image/jpeg;base64," + imgdata)
    elem.set("clip-path", "url(#clippath1)")

    # Message in plain text
    group = ET.SubElement(svg, "g")
    for i in range(min(len(MESSAGE), 80)):
        x = PAGE_WIDTH - MARGIN_RIGHT - (79 - i) * SPACE_X
        text = ET.SubElement(group, "text")
        text.set("x", f"{x:.4f}")
        text.set("y", "12")
        text.set("text-anchor", "middle")
        text.text = str(MESSAGE[i])

    group = ET.SubElement(svg, "g")
    for i in range(80):
        x = PAGE_WIDTH - MARGIN_RIGHT - (79 - i) * SPACE_X
        try:
            bits = IBM_029[MESSAGE[i]]
        except IndexError:
            bits = 0x000
        except KeyError:
            print(f"WARNING: Replaced unsupported character {MESSAGE[i]} (0x{ord(MESSAGE[i]):02x}) with space.")
            bits = 0x000

        for j in range(10):
            y = (j + 3) * SPACE_Y
            if (bits & 0x001):
                elem = ET.SubElement(group, "rect")
                elem.set("x", f"{x - RECT_WIDTH / 2:.4f}")
                elem.set("y", f"{y - RECT_HEIGHT / 2:.4f}")
                elem.set("width", f"{RECT_WIDTH:.4f}")
                elem.set("height", f"{RECT_HEIGHT:.4f}")
            else:
                elem = ET.SubElement(group, "text")
                elem.set("x", f"{x:.4f}")
                elem.set("y", f"{y + 4:.4f}")
                elem.set("text-anchor", "middle")
                elem.text = str(j)
            bits >>= 1
        for j in range(2):
            if (bits & 0x001):
                y = (2 - j) * SPACE_Y
                elem = ET.SubElement(group, "rect")
                elem.set("x", f"{x - RECT_WIDTH / 2:.4f}")
                elem.set("y", f"{y - RECT_HEIGHT / 2:.4f}")
                elem.set("width", f"{RECT_WIDTH:.4f}")
                elem.set("height", f"{RECT_HEIGHT:.4f}")
            bits >>= 1

    xml = ET.ElementTree(svg)
    xml.write("output.svg", encoding='UTF-8', xml_declaration=True, method='xml')

if __name__ == '__main__':
    generate()
