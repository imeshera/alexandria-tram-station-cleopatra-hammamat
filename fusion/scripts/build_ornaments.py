# Ornaments and furniture (instancing definitions under 'Library'):
#   "Cartouche"  attic block on the crossing-end entablature carrying the designer's credit line
#                ("تصميم المعماري م/ ..." - name illegible, not cut) and the oval laurel-and-rose wreath tablet
#                with the sponsor text "شركة / قصر السلام / ..." (third line illegible, left blank).
#                Local frame: origin at the attic bottom on the entablature top (attic 40 cm, tablet 1.52 x 1.12 m), back face on x = 0, faces -X.
#   "Plaque"     framed name plate "كليوباترا" on the drum of the two-tier unit; faces +Z.
#   "Bench"      pink terrazzo bench: slab with a rounded nosing on two waisted pedestals; local origin at floor.
#   "Baluster"   turned vase baluster with square plinth and abacus; local origin at its foot.
# Lettering: CoreText SVG outlines (tools/lettering/make_svgs.sh), raised 15-18 mm.
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, common
importlib.reload(common)
from common import box, vcyl, cyl, sphere, union_all, moved, rot_about, compose, mat, tbm
import adsk.core, adsk.fusion

# reading frame (XY plane, reader at +Z) -> facing -X
TO_MINUS_X = rot_about((0, 1, 0), -math.pi / 2)


def oval_plate(comp, a, b, cy, w0, w1):
    return common.poly_extrude(comp, common.ellipse_pts(a, b, 96, 0, cy), w0, w1)[0]


def oval_ring(comp, a, b, t, cy, w0, w1):
    outer = oval_plate(comp, a, b, cy, w0, w1)
    inner = oval_plate(comp, a - t, b - t, cy, w0 - 1, w1 + 1)
    tbm.booleanOperation(outer, inner, adsk.fusion.BooleanTypes.DifferenceBooleanType)
    return outer


def cartouche(comp, attic=True):
    parts, text = [], []
    if attic:
        # attic block with a small cornice and a bordered credit panel
        parts.append(box(-74, 74, 0, 36, 0, 26))
        parts.append(box(-78, 78, 36, 40, 0, 30))
        parts.append(box(-76, 76, 0, 3, 0, 28))
        fr_out = box(-64, 64, 6, 32, 25.5, 27.0)
        tbm.booleanOperation(fr_out, box(-61.5, 61.5, 8.5, 29.5, 25, 28), adsk.fusion.BooleanTypes.DifferenceBooleanType)
        parts.append(fr_out)
        for b in common.svg_text(comp, common.svg_path('credit.svg'), 22, 12.5, 11.0, 1.5, max_w=72):
            tbm.transform(b, mat(0, 0, 26))
            text.append(b)
    # oval tablet: back plate, rim, laurel wreath, three roses, sponsor text
    a, b_, cy = 76.0, 56.0, 40 + 56
    parts.append(oval_plate(comp, a, b_, cy, 4, 14))
    parts.append(oval_ring(comp, a, b_, 8.5, cy, 14, 16.5))
    # laurel wreath: pairs of leaves set herringbone-fashion along the oval, tips pointing up both sides
    n = 34
    for i in range(n):
        th = 2 * math.pi * i / n
        if abs(math.sin(th) + 1) < 0.12:          # leave the bottom free for the roses
            continue
        x, y = (a - 4.3) * math.cos(th), cy + (b_ - 4.3) * math.sin(th)
        tang = math.atan2((b_ - 4.3) * math.cos(th), -(a - 4.3) * math.sin(th))
        if math.cos(th) < 0:
            tang += math.pi                      # both halves of the wreath grow upwards
        for sgn in (-1, 1):
            leaf = box(-3.6, 3.6, -1.3, 1.3, 16.0, 18.6)
            ang = tang + sgn * 0.55
            tbm.transform(leaf, compose(rot_about((0, 0, 1), ang), mat(x + 2.2 * math.cos(ang), y + 2.2 * math.sin(ang), 0)))
            parts.append(leaf)
    for (u, r) in ((0, 6.5), (-13, 5.2), (13, 5.2)):
        parts.append(sphere((u, cy - b_ + 6, 19.0), r))
    for bb in common.svg_text(comp, common.svg_path('cart_l1.svg'), 0, cy + 22, 13.0, 1.8, max_w=48):
        tbm.transform(bb, mat(0, 0, 14))
        text.append(bb)
    for bb in common.svg_text(comp, common.svg_path('cart_l2.svg'), 0, cy - 15, 32.0, 1.8, max_w=118):
        tbm.transform(bb, mat(0, 0, 14))
        text.append(bb)
    # third line: illegible in every frame -> plain raised band only
    parts.append(box(-38, 38, cy - 31, cy - 23, 14, 14.6))
    body = union_all(parts)
    tbm.transform(body, TO_MINUS_X)
    for t in text:
        tbm.transform(t, TO_MINUS_X)
    return body, union_all(text)


def plaque(comp, w=96.0, h=32.0):
    parts = [box(-w / 2, w / 2, -h / 2, h / 2, -10, 2)]
    fr = box(-w / 2, w / 2, -h / 2, h / 2, 2, 4)
    tbm.booleanOperation(fr, box(-w / 2 + 3, w / 2 - 3, -h / 2 + 3, h / 2 - 3, 1, 5),
                         adsk.fusion.BooleanTypes.DifferenceBooleanType)
    parts.append(fr)
    text = common.svg_text(comp, common.svg_path('drum.svg'), 0, -h / 2 + 4.5, h - 9, 2.0, max_w=w - 12)
    for t in text:
        tbm.transform(t, mat(0, 0, 2))
    return union_all(parts), union_all(text)


def bench(L, H, W):
    t = 7.0
    parts = [box(-L / 2, L / 2, H - t, H, -W / 2, W / 2 - 3)]
    parts.append(cyl((-L / 2, H - t / 2, W / 2 - 3), (L / 2, H - t / 2, W / 2 - 3), t / 2))
    for s in (-1, 1):
        x = s * (L / 2 - 22)
        parts.append(box(x - 14, x + 14, 0, 6, -W / 2 + 4, W / 2 - 6))          # foot
        parts.append(box(x - 8, x + 8, 6, H - t, -W / 2 + 8, W / 2 - 10))       # waist
        parts.append(box(x - 12, x + 12, H - t - 6, H - t, -W / 2 + 5, W / 2 - 7))   # cap
        parts.append(cyl((x - 8, 14, W / 2 - 10), (x + 8, 14, W / 2 - 10), 5))     # scroll roll
        parts.append(cyl((x - 8, H - t - 10, W / 2 - 10), (x + 8, H - t - 10, W / 2 - 10), 4))
    return union_all(parts)


def baluster(comp, h):
    sq = 12.0
    blk = 5.0
    y0, y1 = blk, h - blk
    L = y1 - y0
    segs = [('P', (0, y0)), ('P', (5.2, y0)),
            ('S', [(5.6, y0 + 0.04 * L), (5.0, y0 + 0.08 * L)]),
            ('P', (4.0, y0 + 0.10 * L)),
            ('S', [(6.2, y0 + 0.30 * L), (5.0, y0 + 0.50 * L), (3.0, y0 + 0.68 * L), (2.6, y0 + 0.76 * L)]),
            ('P', (4.2, y0 + 0.80 * L)),
            ('S', [(4.6, y0 + 0.86 * L), (3.8, y0 + 0.92 * L)]),
            ('P', (4.6, y1)), ('P', (0, y1))]
    turned = common.revolve_profile(comp, segs, 'baluster')[0]
    return union_all([turned, box(-sq / 2, sq / 2, 0, blk, -sq / 2, sq / 2),
                      box(-sq / 2 + 0.5, sq / 2 - 0.5, y1, h, -sq / 2 + 0.5, sq / 2 - 0.5)])


def run(_context: str):
    doc, design = common.activate()
    p = common.Params(design)
    c = common.new_definition_comp(design, 'Cartouche')
    common.clear_comp(c)
    body, text = cartouche(c)
    common.deposit(c, [body], 'Cartouche')
    common.deposit(c, [text], 'Cartouche lettering')
    cu = common.new_definition_comp(design, 'Cartouche Upper')
    common.clear_comp(cu)
    body, text = cartouche(cu, attic=False)
    common.deposit(cu, [body], 'Cartouche')
    common.deposit(cu, [text], 'Cartouche lettering')
    pl = common.new_definition_comp(design, 'Plaque')
    common.clear_comp(pl)
    body, text = plaque(pl)
    common.deposit(pl, [body], 'Plaque')
    common.deposit(pl, [text], 'Plaque lettering')
    bc = common.new_definition_comp(design, 'Bench')
    common.clear_comp(bc)
    common.deposit(bc, [bench(p.bench_l, p.bench_h, p.bench_w)], 'Bench')
    bl = common.new_definition_comp(design, 'Baluster')
    common.clear_comp(bl)
    common.deposit(bl, [baluster(bl, p.bal_h - 12 - 13)], 'Baluster')
    print('ornaments built')
