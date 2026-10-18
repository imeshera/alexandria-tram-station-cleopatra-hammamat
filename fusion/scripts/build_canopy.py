# Cast reinforced-concrete urn / bell canopies (revolved solids), as instancing definitions:
#   "Canopy"        lower canopy: convex bowl ("neck") resting on two neighbouring entablatures, with a shallow
#                   concave soffit dish underneath; moulded lip band at the equator (bead, dentils, ovolo);
#                   pot-shaped dome with raised lotus lappets hanging from the dentilled crown ring; finial.
#   "Drum"          lower tier of the two-tier unit: same bowl and lip, vertical drum wall with a dentilled
#                   cornice and a flat deck carrying the colonnettes.
#   "Upper Canopy"  the two-tier unit's upper canopy (scaled lip/bowl, taller finial).
# Local frame: origin at the centre of the bowl bottom (= top of the entablature), Y up.
# The canopies are modelled solid (the real shells are ~80 mm RC around a void; a closed void is useless for
# printing and invisible), with the concave soffit dish and all outer mouldings.
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, common
importlib.reload(common)
from common import box, vcyl, cyl, sphere, torus, union_all, moved, rot_about, compose, mat, tbm, P3
import adsk.core, adsk.fusion


def lip_segments(R, lh, y0):
    """Outer lip band profile (r, y) from its bottom (y0) to its top ledge."""
    return [
        ('P', (R - 1.5, y0)),
        ('S', [(R - 0.3, y0 + 0.06 * lh), (R - 0.8, y0 + 0.16 * lh)]),     # bottom bead
        ('P', (R - 3.2, y0 + 0.20 * lh)),
        ('P', (R - 3.2, y0 + 0.64 * lh)),                                  # recessed dentil zone
        ('P', (R - 1.8, y0 + 0.68 * lh)),
        ('S', [(R + 0.2, y0 + 0.80 * lh), (R - 1.2, y0 + 0.95 * lh)]),      # ovolo
        ('P', (R - 1.2, y0 + lh)),
    ]


def bowl_segments(R, Rb, bh, dish):
    """From the soffit centre: concave dish out to the bottom rim (Rb), then the convex bowl up to the lip."""
    lip_r = R - 3.0
    return [
        ('P', (0, dish)),
        ('S', [(0.45 * Rb, 0.82 * dish), (Rb - 14, 2.0)]),
        ('P', (Rb - 6, 0)),
        ('P', (Rb, 0)),
        ('S', [(Rb + 0.42 * (lip_r - Rb), 0.08 * bh), (Rb + 0.80 * (lip_r - Rb), 0.36 * bh),
               (lip_r - 0.6, 0.78 * bh), (lip_r, bh - 2.0)]),
        ('P', (R - 1.5, bh)),
    ]


def dentil_ring(R, y0, y1, depth=2.6, w=4.0, gap=2.6):
    n = int(2 * math.pi * (R - 3.2) // (w + gap))
    proto = box(R - 3.6, R - 3.2 + depth, y0, y1, -w / 2, w / 2)
    parts = [moved(proto, rot_about((0, 1, 0), 2 * math.pi * i / n)) for i in range(n)]
    return union_all(parts)


def dome_points(R0, Rc, y0, hd):
    """Pot/bell outer profile from the lip ledge (R0, y0) to the crown ring foot (Rc, y0 + hd)."""
    return [(R0 + 0.010 * R0, y0 + 0.18 * hd), (R0 - 0.035 * R0, y0 + 0.42 * hd),
            (R0 - 0.17 * R0, y0 + 0.68 * hd), (Rc + 0.11 * R0, y0 + 0.90 * hd), (Rc, y0 + hd)]


def lappets(comp, R0, Rc, y0, hd, n=8, proud=2.0):
    """Raised pointed 'lotus' lappets hanging from the crown: a 2 cm skin over the upper dome, trimmed by a
    plan-view pattern of triangles (down-pointing on the dome = radial wedges in plan)."""
    pts = dome_points(R0, Rc, y0, hd)
    up = pts[1:]                                 # from 0.42 hd to the crown foot
    outer = [(r + proud * 1.1, y + proud * 0.5) for (r, y) in up]
    inner = [(r - 1.5, y - 0.6) for (r, y) in up]
    segs = [('P', inner[0]), ('P', outer[0]), ('S', outer[1:]), ('P', inner[-1]), ('S', inner[-2::-1])]
    skin = common.revolve_profile(comp, segs, 'lappet skin')[0]
    # trim: keep only the wedges
    keep = None
    tip_r = up[0][0] + 2
    for k in range(n):
        a = 2 * math.pi * k / n
        d = math.pi / n * 0.78
        base_r = Rc * 0.92
        tri = [(base_r * math.cos(a - d), base_r * math.sin(a - d)),
               (tip_r * math.cos(a), tip_r * math.sin(a)),
               (base_r * math.cos(a + d), base_r * math.sin(a + d))]
        prism = common.poly_extrude(comp, tri, 0, hd + 80)[0]
        # drawn in XY and extruded along +Z: rotate about X by -90 deg so the extrusion runs along +Y
        tbm.transform(prism, compose(rot_about((1, 0, 0), -math.pi / 2), mat(0, y0 - 20, 0)))
        keep = prism if keep is None else union_all([keep, prism])
    tbm.booleanOperation(skin, keep, adsk.fusion.BooleanTypes.IntersectionBooleanType)
    return skin


def finial(y_top, h, r0=3.2):
    parts = [vcyl(0, 0, y_top, y_top + 0.12 * h, r0 * 2.2, r0 * 1.6),
             sphere((0, y_top + 0.22 * h, 0), r0 * 1.9),
             vcyl(0, 0, y_top + 0.28 * h, y_top + h, r0, 0.4)]
    return union_all(parts)


def canopy_bodies(comp, R, Rb, bh, dish, lh, lt, rise, Rc, ch, fin_h, lappet_n=8):
    R0 = R - 0.45 * lt
    y_l = bh + lh                                  # lip top
    hd = rise - ch                                 # lip top -> crown ring foot
    ys = y_l + hd
    yt = ys + ch
    outer = dome_points(R0, Rc, y_l, hd)
    segs = bowl_segments(R, Rb, bh, dish) + lip_segments(R, lh, bh)[1:] + [
        ('P', (R0, y_l)),
        ('S', outer),
        ('P', (Rc + 2.0, ys)),
        ('P', (Rc + 2.0, ys + 0.55 * ch)),
        ('P', (Rc + 7.0, ys + 0.70 * ch)),
        ('P', (Rc + 7.0, ys + 0.86 * ch)),
        ('P', (Rc + 4.0, yt)),
        ('P', (0, yt)),
    ]
    body = common.revolve_profile(comp, segs, 'canopy')
    parts = list(body)
    parts.append(dentil_ring(R, bh + 0.25 * lh, bh + 0.60 * lh))
    parts.append(dentil_ring(Rc + 6.5, ys + 0.30 * ch, ys + 0.50 * ch, depth=1.6, w=3.0, gap=2.2))
    lap = lappets(comp, R0, Rc, y_l, hd, n=lappet_n) if lappet_n else None
    fin = finial(yt, fin_h)
    return union_all(parts), lap, fin


def drum_bodies(comp, R, Rb, bh, dish, lh, lt, drum_h):
    R0 = R - 0.45 * lt
    y_l = bh + lh
    yd = y_l + drum_h
    segs = bowl_segments(R, Rb, bh, dish) + lip_segments(R, lh, bh)[1:] + [
        ('P', (R0, y_l)),
        ('P', (R0, yd - 0.22 * drum_h)),
        ('P', (R0 + 2.0, yd - 0.20 * drum_h)),      # cornice bed
        ('P', (R0 + 2.0, yd - 0.12 * drum_h)),
        ('P', (R0 + 6.5, yd - 0.08 * drum_h)),      # corona
        ('P', (R0 + 6.5, yd - 0.02 * drum_h)),
        ('P', (R0 + 4.5, yd)),
        ('P', (0, yd)),
    ]
    body = common.revolve_profile(comp, segs, 'drum')[0]
    dent = dentil_ring(R0 + 2.4, yd - 0.19 * drum_h, yd - 0.12 * drum_h, depth=2.0, w=3.5, gap=2.4)
    return union_all([body, dentil_ring(R, bh + 0.25 * lh, bh + 0.60 * lh), dent])


def build(design, name, bodies_fn):
    comp = common.new_definition_comp(design, name)
    common.clear_comp(comp)
    return comp, bodies_fn(comp)


def run(_context: str):
    doc, design = common.activate()
    p = common.Params(design)
    R, Rb = p.lip_d / 2, p.bowl_d / 2
    c, (shell, lap, fin) = build(design, 'Canopy', lambda comp: canopy_bodies(
        comp, R, Rb, p.bowl_h, p.dish_d, p.lip_h, p.lip_t, p.dome_rise, p.crown_d / 2, p.crown_h, p.finial_h))
    common.deposit(c, [shell], 'Canopy shell')
    if lap:
        common.deposit(c, [lap], 'Lotus lappets')
    common.deposit(c, [fin], 'Finial')
    k = p.ulip_d / p.lip_d
    u, (ushell, ulap, ufin) = build(design, 'Upper Canopy', lambda comp: canopy_bodies(
        comp, R * k, Rb * k, p.bowl_h * k, p.dish_d * k, p.lip_h * k, p.lip_t * k, p.udome_rise,
        p.crown_d / 2 * k, p.crown_h * k, p.ufinial_h))
    common.deposit(u, [ushell], 'Upper canopy shell')
    if ulap:
        common.deposit(u, [ulap], 'Lotus lappets')
    common.deposit(u, [ufin], 'Finial')
    d, dbody = build(design, 'Drum', lambda comp: drum_bodies(
        comp, R, Rb, p.bowl_h, p.dish_d, p.lip_h, p.lip_t, p.drum_h))
    common.deposit(d, [dbody], 'Drum')
    print('canopies built')
