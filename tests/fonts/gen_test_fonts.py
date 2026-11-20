# Added by ibis inc. (2026-11-18). Synthetic outlines, no third-party font input (the ibisOffice fork of gpui's wgpu text system).
# Two fonts with no 'm' glyph: a colour one (a COLR v0 layer and a CPAL palette, as an emoji font has) and a plain symbol one.
from pathlib import Path
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import newTable
from fontTools.colorLib.builder import buildCOLR, buildCPAL

def build(name, colour):
    order = ['.notdef', 'space', 'smile', 'layer']
    fb = FontBuilder(1000, isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap({0x20: 'space', 0x1F600: 'smile'})
    glyphs = {}
    for g in order:
        pen = TTGlyphPen(None)
        if g in ('smile', 'layer'):
            pen.moveTo((100, 0)); pen.lineTo((900, 0)); pen.lineTo((900, 800)); pen.lineTo((100, 800)); pen.closePath()
        glyphs[g] = pen.glyph()
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics({g: (1000, 0) for g in order})
    fb.setupHorizontalHeader(ascent=900, descent=-200)
    fb.setupNameTable({'familyName': name, 'styleName': 'Regular', 'uniqueFontIdentifier': name, 'fullName': name, 'psName': name.replace(' ', '')})
    fb.setupOS2(sTypoAscender=900, sTypoDescender=-200, usWinAscent=900, usWinDescent=200)
    fb.setupPost()
    if colour:
        fb.font['COLR'] = buildCOLR({'smile': [('layer', 0)]}, version=0)
        fb.font['CPAL'] = buildCPAL([[(1.0, 0.0, 0.0, 1.0)]])
    return fb.font

here = Path(__file__).parent
build('Ibis Colour Test', True).save(here / 'colour_no_m.ttf')
build('Ibis Symbol Test', False).save(here / 'symbol_no_m.ttf')
