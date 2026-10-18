# Column definitions: "Column" (main order) and "Colonnette" (upper tier of the two-tier unit).
# Scamozzi-type Ionic: square plinth, Attic base (torus-scotia-torus), shaft with entasis, astragal,
# egg-and-dart echinus, four diagonal volutes with raised spiral ribbons and eyes, concave-sided abacus.
# Local frame: origin at the plinth bottom centre, Y up. Both components live under the 'Library' occurrence
# (hidden) and are instanced by the frame / two-tier unit components.
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, common
importlib.reload(common)
from common import box, vcyl, cyl, sphere, union_all, moved, rot_about, compose, mat, tbm
import adsk.core, adsk.fusion


def volute_proto(comp, rv, tv, bolster_len):
    """One volute in a local frame: face normal +Z, centre at the origin; bolster runs towards -Z."""
    turns, n = 2.6, 52
    w = 0.13 * rv
    outer, inner = [], []
    for i in range(int(turns * n) + 1):
        th = 2 * math.pi * i / n
        r = rv * 0.97 * (1 - th / (2 * math.pi * turns)) + 0.17 * rv
        outer.append((r * math.cos(th + math.pi / 2), r * math.sin(th + math.pi / 2)))
        ri = r - w
        inner.append((ri * math.cos(th + math.pi / 2), ri * math.sin(th + math.pi / 2)))
    ribbon = common.poly_extrude(comp, outer + inner[::-1], 0, 0.08 * rv + 0.4)
    disc = cyl((0, 0, -tv), (0, 0, 0), rv)
    eye = cyl((0, 0, 0), (0, 0, 0.1 * rv + 0.6), 0.18 * rv)
    bol = cyl((0, 0, -tv - bolster_len), (0, 0, -tv * 0.5), rv * 0.78, rv * 0.9)
    return union_all([disc, bol, eye] + ribbon)


def column_bodies(comp, H, D, pw, ph, bh, ch, aw, ah, ent):
    R = D / 2.0
    Re = R * ent
    y0 = ph
    yb1 = y0 + bh
    ys1 = H - ch                       # shaft top / capital bottom
    ya0 = H - ah                       # abacus bottom
    yech0 = ys1 + 0.22 * ch            # echinus bottom
    yech1 = ys1 + 0.52 * ch            # echinus top
    Rech = Re + 0.17 * D
    Rcan = Re + 0.11 * D
    segs = [
        ('P', (0, y0)),
        ('P', (R * 1.30, y0)),
        ('S', [(R * 1.38, y0 + 0.18 * bh), (R * 1.30, y0 + 0.36 * bh)]),
        ('P', (R * 1.14, y0 + 0.40 * bh)),
        ('S', [(R * 1.10, y0 + 0.52 * bh), (R * 1.20, y0 + 0.64 * bh)]),
        ('S', [(R * 1.24, y0 + 0.78 * bh), (R * 1.13, y0 + 0.92 * bh)]),
        ('P', (R * 1.07, yb1)),
        ('S', [(R * 1.01, yb1 + 0.04 * D), (R, yb1 + 0.10 * D)]),
        # shaft with entasis (straight lower third, then diminishing)
        ('S', [(R * 1.002, yb1 + (ys1 - yb1) * 0.33), (R - (R - Re) * 0.45, yb1 + (ys1 - yb1) * 0.66),
               (Re, ys1 - 0.02 * D)]),
        # astragal (bead) + fillet
        ('P', (Re + 0.035 * D, ys1)),
        ('S', [(Re + 0.065 * D, ys1 + 0.05 * ch), (Re + 0.035 * D, ys1 + 0.10 * ch)]),
        ('P', (Re + 0.01 * D, ys1 + 0.12 * ch)),
        ('P', (Re + 0.01 * D, yech0)),
        # echinus (ovolo)
        ('S', [(Re + 0.09 * D, yech0 + 0.12 * ch), (Rech, yech1)]),
        ('P', (Rcan, yech1)),
        ('P', (Rcan, ya0)),
        ('P', (0, ya0)),
    ]
    rev = common.revolve_profile(comp, segs, 'shaft')
    parts = list(rev)
    # plinth with a small top chamfer slab
    parts.append(box(-pw / 2, pw / 2, 0, ph * 0.86, -pw / 2, pw / 2))
    parts.append(box(-pw / 2 + 0.6, pw / 2 - 0.6, ph * 0.86 - 0.01, ph, -pw / 2 + 0.6, pw / 2 - 0.6))
    # abacus: concave-sided square
    ab = box(-aw / 2, aw / 2, ya0, H, -aw / 2, aw / 2)
    cut_r = aw * 0.9
    sag = 0.07 * aw
    for (dx, dz) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        c = vcyl(dx * (aw / 2 + cut_r - sag), dz * (aw / 2 + cut_r - sag), ya0 - 1, H + 1, cut_r)
        tbm.booleanOperation(ab, c, adsk.fusion.BooleanTypes.DifferenceBooleanType)
    # abacus top fillet strip (ovolo look): slightly smaller slab on top
    parts.append(ab)
    # egg-and-dart: eggs around the echinus
    n_egg = 16
    for i in range(n_egg):
        a = 2 * math.pi * (i + 0.5) / n_egg
        re = Re + 0.10 * D
        parts.append(sphere((re * math.cos(a), (yech0 + yech1) / 2 + 0.01 * ch, re * math.sin(a)), 0.065 * D))
    # four diagonal volutes under the abacus corners
    rv = 0.24 * D
    tv = 0.15 * D
    dv = aw / 2 * math.sqrt(2) - rv * 0.75
    yv = ya0 - rv * 0.92
    proto = volute_proto(comp, rv, tv, dv - Rcan + 0.5 * tv)
    for k in range(4):
        beta = math.pi / 4 + k * math.pi / 2
        m = compose(rot_about((0, 1, 0), beta), mat(dv * math.sin(beta), yv, dv * math.cos(beta)))
        parts.append(moved(proto, m))
    return union_all(parts)


def build(design, name, H, D, pw, ph, bh, ch, aw, ah, ent):
    comp = common.new_definition_comp(design, name)
    common.clear_comp(comp)
    body = column_bodies(comp, H, D, pw, ph, bh, ch, aw, ah, ent)
    return common.deposit(comp, [body], name)


def run(_context: str):
    doc, design = common.activate()
    p = common.Params(design)
    build(design, 'Column', p.col_h, p.col_d, p.plinth_w, p.plinth_h, p.base_h, p.cap_h, p.abacus_w,
          p.abacus_h, p.entasis)
    d = p.ucol_d
    build(design, 'Colonnette', p.ucol_h, d, 1.6 * d, 0.36 * d, 0.36 * d, 0.85 * d, 1.42 * d, 0.15 * d, p.entasis)
    lib = common.root_occ(design, 'Library')
    print('built Column, Colonnette; library occurrence', lib.name if lib else None)
