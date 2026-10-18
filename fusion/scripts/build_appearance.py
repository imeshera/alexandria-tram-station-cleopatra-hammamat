# Appearances: slightly weathered white/cream render on the colonnade (colours sampled from the 2024 daylight
# frames and desaturated), tan soffits (downward faces of the shells), a grime ring on the column bases,
# green-painted lettering, pink terrazzo benches, grey paving, rusty rails, asphalt.
# Body-level where possible (definition components => every instance); per-face only on the shells and columns.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, common
importlib.reload(common)
import adsk.core, adsk.fusion

COL = {
    'Render cream (weathered)': (226, 214, 188),
    'Render dome (weathered)': (234, 225, 200),
    'Render soffit (stained)': (204, 186, 150),
    'Render white (lappets)': (243, 238, 224),
    'Render grime': (138, 128, 110),
    'Lettering green': (58, 86, 66),
    'Terrazzo pink': (196, 150, 140),
    'Paving grey': (170, 166, 156),
    'Concrete platform': (146, 142, 134),
    'Tactile yellow': (196, 182, 140),
    'Coping': (186, 181, 168),
    'Rail steel (rusty)': (112, 96, 82),
    'Sleeper concrete': (142, 138, 130),
    'Ballast earth': (118, 104, 86),
    'Asphalt': (68, 68, 70),
    'Kerb': (176, 171, 160),
    'OCS grey': (150, 156, 160),
}

BODY = {   # body name prefix -> appearance
    'Column': 'Render cream (weathered)', 'Colonnette': 'Render cream (weathered)',
    'Entablature': 'Render cream (weathered)', 'Upper entablature': 'Render cream (weathered)',
    'Canopy shell': 'Render dome (weathered)', 'Upper canopy shell': 'Render dome (weathered)',
    'Drum': 'Render dome (weathered)', 'Lotus lappets': 'Render white (lappets)', 'Finial': 'Render cream (weathered)',
    'Cartouche lettering': 'Lettering green', 'Plaque lettering': 'Lettering green',
    'Cartouche': 'Render white (lappets)', 'Plaque': 'Render cream (weathered)',
    'Bench': 'Terrazzo pink', 'Baluster': 'Render cream (weathered)', 'Balustrade': 'Render cream (weathered)',
    'Platform': 'Concrete platform', 'Paving': 'Paving grey', 'Tactile band': 'Tactile yellow', 'Coping': 'Coping',
    'Rails': 'Rail steel (rusty)', 'Sleepers': 'Sleeper concrete', 'Track bed': 'Ballast earth',
    'Crossing slab': 'Asphalt', 'Carriageway': 'Asphalt', 'Kerbs': 'Kerb', 'Verge': 'Ballast earth',
    'OCS': 'OCS grey',
}


def run(_context: str):
    doc, design = common.activate()
    p = common.Params(design)
    ap = {n: common.appearance(design, n, rgb, base='Plastic - Matte (White)') for n, rgb in COL.items()}
    n_b = 0
    for comp in design.allComponents:
        for b in comp.bRepBodies:
            key = None
            for k in sorted(BODY, key=len, reverse=True):
                if b.name == k or b.name.startswith(k + ' '):
                    key = k
                    break
            if key:
                b.appearance = ap[BODY[key]]
                n_b += 1
    # soffits: downward-facing faces of the shells
    n_f = 0
    for cname in ('Canopy', 'Upper Canopy', 'Drum'):
        c = common.find_comp(design, cname)
        for b in c.bRepBodies:
            if not (b.name.endswith('shell') or b.name == 'Drum'):
                continue
            for f in b.faces:
                ok, nrm = f.evaluator.getNormalAtPoint(f.pointOnFace)
                if ok and nrm.y < -0.25:
                    f.appearance = ap['Render soffit (stained)']
                    n_f += 1
    # grime ring on the column bases (lower torus + plinth top)
    for cname, yb in (('Column', p.plinth_h + p.base_h * 0.55), ('Colonnette', 0.36 * p.ucol_d * 1.5)):
        c = common.find_comp(design, cname)
        for b in c.bRepBodies:
            for f in b.faces:
                bb = f.boundingBox
                if bb.maxPoint.y <= yb + 0.5 and bb.minPoint.y >= p.plinth_h * 0.8 * (cname == 'Column'):
                    f.appearance = ap['Render grime']
                    n_f += 1
    print('appearances: %d bodies, %d faces' % (n_b, n_f))
