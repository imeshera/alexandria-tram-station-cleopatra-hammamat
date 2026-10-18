# "Frame": one transverse portal of the colonnade = two Column instances + the entablature beam on top.
# Local frame: origin at platform level on the frame centre line; X along the track, Z across
# (+Z = track side, -Z = street side), Y up.
# Entablature (ent_h): two-fascia architrave, frieze with a row of dentil blocks, cornice with corona and cyma,
# all wrapped around the four faces (the end faces are visible along the platform).
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, common
importlib.reload(common)
from common import box, union_all, mat, place
import adsk.core, adsk.fusion


def entablature(x_half, z_half, y0, h, dentils=True):
    """Moulded beam: core x in [-x_half, x_half], z in [-z_half, z_half], from y0 to y0 + h."""
    layers = [  # (y from, y to, projection beyond the core)
        (0.00, 0.16, -1.2),   # lower fascia
        (0.16, 0.33, 0.0),    # upper fascia
        (0.33, 0.37, 1.2),    # architrave fillet
        (0.37, 0.70, -0.8),   # frieze (dentils sit on it)
        (0.70, 0.76, 1.6),    # bed moulding
        (0.76, 0.80, 3.0),
        (0.80, 0.93, 6.0),    # corona
        (0.93, 1.00, 4.5),    # cyma / top fillet
    ]
    parts = []
    for (a, b, pr) in layers:
        parts.append(box(-x_half - pr, x_half + pr, y0 + a * h, y0 + b * h, -z_half - pr, z_half + pr))
    if dentils:
        dw, gap, dp = 4.0, 2.6, 2.4
        ya, yb = y0 + 0.42 * h, y0 + 0.64 * h
        core = -0.8
        # long faces (normal +/-X), running along Z
        n = int((2 * z_half) // (dw + gap))
        off = -(n * (dw + gap) - gap) / 2
        for i in range(n):
            z0 = off + i * (dw + gap)
            for s in (-1, 1):
                xf = s * (x_half + core)
                parts.append(box(xf, xf + s * dp, ya, yb, z0, z0 + dw))
        n = int((2 * x_half) // (dw + gap))
        off = -(n * (dw + gap) - gap) / 2
        for i in range(n):
            x0 = off + i * (dw + gap)
            for s in (-1, 1):
                zf = s * (z_half + core)
                parts.append(box(x0, x0 + dw, ya, yb, zf, zf + s * dp))
    return union_all(parts)


def run(_context: str):
    doc, design = common.activate()
    p = common.Params(design)
    col = common.find_comp(design, 'Column')
    fr = common.new_definition_comp(design, 'Frame')
    common.clear_comp(fr)
    for s in (-1, 1):
        place(fr, col, mat(0, 0, s * p.col_w / 2))
    zh = p.col_w / 2 + p.ent_over
    beam = entablature(p.ent_d / 2, zh, p.col_h, p.ent_h)
    common.deposit(fr, [beam], 'Entablature')
    print('Frame built: beam %.0f x %.0f x %.0f cm' % (p.ent_d, 2 * zh, p.ent_h))
