# Modules (instancing definitions under 'Library'):
#   "Canopy Module"  the repeating unit: one Frame (2 columns + entablature) at x = 0 and one Canopy centred
#                    half a pitch further on (each canopy rests on two neighbouring frames; lips touch above them).
#   "Tall Unit"      two-tier unit: Drum (lower canopy) + 'Plaque' on its track side + four Colonnettes on the
#                    drum deck + square upper entablature + Upper Canopy + tablet-only 'Cartouche Upper' facing -X.
#                    Local origin at the drum lip bottom.
#   "Tall Module"    Frame at x = 0 + Tall Unit half a pitch on.
# Local frames: X along the track (+X away from the level crossing), Z across (+Z = track side), Y up.
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, common
importlib.reload(common)
from common import box, union_all, mat, place, tbm
import adsk.core, adsk.fusion

here = os.path.dirname(os.path.abspath(__file__))


def _load(name):
    path = os.path.join(here, name)
    ns = {'__name__': 'fusion_lib', '__file__': path}
    exec(compile(open(path).read(), path, 'exec'), ns)
    return ns


def run(_context: str):
    doc, design = common.activate()
    p = common.Params(design)
    fr = common.find_comp(design, 'Frame')
    can = common.find_comp(design, 'Canopy')
    y_lip = p.col_h + p.ent_h

    m = common.new_definition_comp(design, 'Canopy Module')
    common.clear_comp(m)
    place(m, fr, mat(0, 0, 0))
    place(m, can, mat(p.pitch / 2, y_lip, 0))

    # --- two-tier unit
    tu = common.new_definition_comp(design, 'Tall Unit')
    common.clear_comp(tu)
    place(tu, common.find_comp(design, 'Drum'), mat(0, 0, 0))
    R0 = p.lip_d / 2 - 0.45 * p.lip_t
    place(tu, common.find_comp(design, 'Plaque'), mat(0, p.lip_h + 0.45 * p.drum_h, R0 + 0.5))
    yd = p.lip_h + p.drum_h
    uw = p.ucol_w / 2
    col = common.find_comp(design, 'Colonnette')
    for sx in (-1, 1):
        for sz in (-1, 1):
            place(tu, col, mat(sx * uw, yd, sz * uw))
    ent = _load('build_frame.py')['entablature']
    bw = 0.78 * p.ucol_d          # half beam width
    beams = []
    for s in (-1, 1):
        beams.append(ent(uw + bw, bw, yd + p.ucol_h, p.uent_h))      # beam along X at z = s*uw
        tbm.transform(beams[-1], mat(0, 0, s * uw))
        beams.append(ent(bw, uw + bw, yd + p.ucol_h, p.uent_h))
        tbm.transform(beams[-1], mat(s * uw, 0, 0))
    common.deposit(tu, [union_all(beams)], 'Upper entablature')
    y_u = yd + p.ucol_h + p.uent_h
    place(tu, common.find_comp(design, 'Upper Canopy'), mat(0, y_u, 0))
    k = p.ulip_d / p.lip_d
    uR0 = p.ulip_d / 2 - 0.45 * p.lip_t * k
    place(tu, common.find_comp(design, 'Cartouche Upper'), mat(-(uR0 - 4.0), y_u + p.lip_h * k - 34, 0))

    tm = common.new_definition_comp(design, 'Tall Module')
    common.clear_comp(tm)
    place(tm, fr, mat(0, 0, 0))
    place(tm, tu, mat(p.pitch / 2, y_lip, 0))
    print('modules built; tall unit top of upper lip at %.0f cm above platform' % (y_lip + y_u))
