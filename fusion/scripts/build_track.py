# Street context (root components): "Track" (double track, 1435 mm, flat-bottom rails on concrete sleepers in
# an earth/ballast bed, set in the paved level crossing with flangeway grooves), "Street" (crossing carriageway,
# Sidi Gaber St lanes behind each balustrade, kerbs) and "OCS" (centre poles with twin bracket arms,
# contact wires). Origin: crossing centre at top of rail; X along the track (+X north-east).
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, common
importlib.reload(common)
from common import box, cyl, vcyl, union_all, mat, tbm
import adsk.core, adsk.fusion

X0, X1 = -6000.0, 6000.0          # modelled street length (cm)


def rail(x0, x1, zc, p):
    hw, fw, rh = p.rail_head_w / 2, p.rail_foot_w / 2, p.rail_h
    return union_all([
        box(x0, x1, -rh, -rh + 1.1, zc - fw, zc + fw),              # foot
        box(x0, x1, -rh + 1.1, -rh + 2.0, zc - fw * 0.55, zc + fw * 0.55),
        box(x0, x1, -rh + 1.1, -4.6, zc - 0.8, zc + 0.8),           # web
        box(x0, x1, -4.6, -3.6, zc - hw * 0.8, zc + hw * 0.8),
        box(x0, x1, -3.6, -0.4, zc - hw, zc + hw),                  # head
        box(x0, x1, -0.4, 0.0, zc - hw + 0.4, zc + hw - 0.4),
    ])


def run(_context: str):
    doc, design = common.activate()
    p = common.Params(design)
    g = p.gauge / 2 + p.rail_head_w / 2          # rail centre from track centre (gauge at the head)
    xc = p.road_w / 2 + 150                      # paved crossing extends 1.5 m beyond the carriageway
    tr = common.ensure_comp(design, 'Track')
    common.clear_comp(tr)
    rails, sleepers, beds = [], [], []
    for zt in (-p.track_ctr / 2, p.track_ctr / 2):
        for s in (-1, 1):
            rails.append(rail(X0, X1, zt + s * g, p))
        # sleepers outside the crossing slab, grouped in bodies of ~40
        grp = []
        x = X0 + 30
        while x < X1 - 30:
            if abs(x) > xc + 15:
                grp.append(box(x - 11, x + 11, -p.rail_h - 22, -p.rail_h, zt - 130, zt + 130))
                if len(grp) == 40:
                    sleepers.append(union_all(grp))
                    grp = []
            x += p.sleeper_pitch
        if grp:
            sleepers.append(union_all(grp))
        # earth/ballast bed, filled almost to the sleeper tops
        for (a, b) in ((X0, -xc), (xc, X1)):
            beds.append(box(a, b, -60, -p.rail_h - 4, zt - 175, zt + 175))
    common.deposit(tr, [union_all(rails)], 'Rails')
    common.deposit(tr, sleepers, 'Sleepers')
    common.deposit(tr, [union_all(beds)], 'Track bed')

    # ---------------- street: crossing slab with flangeways, carriageways behind the platforms, kerbs
    st = common.ensure_comp(design, 'Street')
    common.clear_comp(st)
    zs = p.track_ctr / 2 + p.plat_edge + p.plat_w     # back of the platforms
    slab = box(-xc, xc, -30, -0.5, -zs - 900, zs + 900)
    cuts = []
    for zt in (-p.track_ctr / 2, p.track_ctr / 2):
        for s in (-1, 1):
            zr = zt + s * g
            cuts.append(box(-xc - 1, xc + 1, -p.rail_h - 1, 1, zr - p.rail_head_w / 2 - 0.5, zr + p.rail_head_w / 2 + 0.5))
            zf = zr - s * (p.rail_head_w / 2 + 3.5)      # flangeway on the gauge side
            cuts.append(box(-xc - 1, xc + 1, -5, 1, zf - 3.5, zf + 3.5))
    tbm.booleanOperation(slab, union_all(cuts), adsk.fusion.BooleanTypes.DifferenceBooleanType)
    common.deposit(st, [slab], 'Crossing slab')
    lanes = [box(X0, -xc, -30, -1, zs + 20, zs + 900), box(xc, X1, -30, -1, zs + 20, zs + 900),
             box(X0, -xc, -30, -1, -zs - 900, -zs - 20), box(xc, X1, -30, -1, -zs - 900, -zs - 20)]
    common.deposit(st, [union_all(lanes)], 'Carriageway')
    kerbs = []
    for s in (-1, 1):
        for (a, b) in ((X0, -xc), (xc, X1)):
            z = s * (zs + 10)
            kerbs.append(box(a, b, -25, 14, z - 10, z + 10))
    common.deposit(st, [union_all(kerbs)], 'Kerbs')
    # earth verge between the track bed and the kerbs (the platforms stand on it)
    fills = []
    for s in (-1, 1):
        for (a, b) in ((X0, -xc), (xc, X1)):
            z0, z1 = sorted((s * (p.track_ctr / 2 + 175), s * zs))
            fills.append(box(a, b, -40, -12, z0, z1))
    common.deposit(st, [union_all(fills)], 'Verge')

    # ---------------- OCS: centre poles, bracket arms, contact wires
    oc = common.ensure_comp(design, 'OCS')
    common.clear_comp(oc)
    parts = []
    poles = [-4400, -1450, 1450, 4400]
    hc = p.ocs_h
    for x in poles:
        parts.append(box(x - 30, x + 30, -40, 5, -30, 30))                       # foundation cap
        parts.append(vcyl(x, 0, 5, 30, 17))                                     # base collar
        parts.append(vcyl(x, 0, 5, hc + 160, 13.5, 9.0))                        # tapered tubular pole
        parts.append(vcyl(x, 0, hc + 160, hc + 166, 11))
        for s in (-1, 1):
            zt = s * p.track_ctr / 2
            parts.append(cyl((x, hc + 120, 0), (x, hc + 120, zt + s * 40), 3.0))      # bracket arm
            parts.append(cyl((x, hc + 150, 0), (x, hc + 121, zt * 0.7), 1.6))      # stay
            parts.append(cyl((x, hc + 120, zt), (x, hc + 4, zt), 0.8))           # dropper
            parts.append(box(x - 6, x + 6, hc - 1, hc + 4, zt - 2, zt + 2))       # clamp
    for s in (-1, 1):
        zt = s * p.track_ctr / 2
        parts.append(cyl((X0, hc, zt), (X1, hc, zt), 0.6))                      # contact wire (12 mm)
    common.deposit(oc, [union_all(parts)], 'OCS')
    print('track, street and OCS built; crossing slab x +/- %.0f cm' % xc)
