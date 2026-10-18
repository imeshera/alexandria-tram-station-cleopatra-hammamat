# "Station Side": one platform with its colonnade, balustrade and benches, modelled in the coordinates of the
# north-east side (platform on the north-west track, colonnade from x_f1 away from the crossing).
# The root holds two occurrences: "Side NE" (identity) and "Side SW" (rotated 180 deg about Y through the
# crossing centre) - the two colonnades are point-symmetric about the level crossing, each with its cartouche
# end facing the crossing (YouTube 01YNkcHynps / hBRSKXDcvPw, opposite directions, both show this).
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, common
importlib.reload(common)
from common import box, union_all, mat, place, tbm
import adsk.core, adsk.fusion


def run(_context: str):
    doc, design = common.activate()
    p = common.Params(design)
    root = design.rootComponent
    side = common.ensure_comp(design, 'Station Side')
    common.clear_comp(side)

    z_edge = -(p.track_ctr / 2 + p.plat_edge)          # platform edge (track side)
    z_back = z_edge - p.plat_w                          # back face of the balustrade
    z_ax = z_edge - p.col_front - p.col_w / 2           # colonnade axis
    xr0 = p.plat_x0                                     # ramp foot
    xp0 = p.plat_x0 + p.ramp_l                          # top of ramp
    xp1 = xp0 + p.plat_len
    h = p.plat_h
    n = int(round(p.n_can))
    ti = int(round(p.tall_idx)) - 1

    # ---------------- colonnade
    cm = common.find_comp(design, 'Canopy Module')
    tm = common.find_comp(design, 'Tall Module')
    for k in range(n):
        place(side, tm if k == ti else cm, mat(p.x_f1 + k * p.pitch, h, z_ax))
    place(side, common.find_comp(design, 'Frame'), mat(p.x_f1 + n * p.pitch, h, z_ax))
    place(side, common.find_comp(design, 'Cartouche'), mat(p.x_f1, h + p.col_h + p.ent_h, z_ax))

    # ---------------- platform: retaining walls + fill + paving, coping, ramp
    tile = 3.0
    slab = box(xp0, xp1, -35, h - tile, z_back, z_edge - 3)
    ramp = common.poly_extrude(side, [(xr0, -35), (xr0, 2), (xp0, h - tile), (xp0, -35)], z_back, z_edge - 3)[0]
    body = union_all([slab, ramp])
    common.deposit(side, [body], 'Platform')
    # paving: 40 cm tiles with 6 mm joints (grooves), separate tactile band along the column line
    pav = box(xp0, xp1, h - tile, h, z_back, z_edge - p.coping_w)
    grooves = []
    for i in range(1, int((xp1 - xp0) // 40)):
        x = xp0 + i * 40
        grooves.append(box(x - 0.3, x + 0.3, h - 0.5, h + 1, z_back - 1, z_edge + 1))
    zz = z_edge - p.coping_w
    while zz - 40 > z_back:
        zz -= 40
        grooves.append(box(xp0 - 1, xp1 + 1, h - 0.5, h + 1, zz - 0.3, zz + 0.3))
    tbm.booleanOperation(pav, union_all(grooves), adsk.fusion.BooleanTypes.DifferenceBooleanType)
    common.deposit(side, [pav], 'Paving')
    tz0, tz1 = z_ax + p.col_w / 2 + 40, z_ax + p.col_w / 2 + 100
    common.deposit(side, [box(p.x_f1 - 150, p.x_f1 + n * p.pitch + 150, h - 0.4, h + 0.4, tz0, tz1)],
                   'Tactile band')
    cop = box(xp0, xp1, h - 12, h, z_edge - p.coping_w, z_edge + 2.5)
    rcop = common.poly_extrude(side, [(xr0, -2), (xr0, 2), (xp0, h), (xp0, h - 12), (xr0 + 20, -2)],
                               z_edge - p.coping_w, z_edge + 2.5)[0]
    common.deposit(side, [union_all([cop, rcop])], 'Coping')

    # ---------------- balustrade along the street edge
    zb = z_back + 18
    bx0, bx1 = xp0 + 60, xp1 - 20
    piers = []
    xs = []
    x = p.x_f1
    while x - p.bal_pier_pitch >= bx0:
        x -= p.bal_pier_pitch
    while x <= bx1:
        xs.append(x)
        x += p.bal_pier_pitch
    if xs[0] - bx0 > 60:
        xs.insert(0, bx0)
    if bx1 - xs[-1] > 60:
        xs.append(bx1)
    pw = p.bal_pier_w
    for x in xs:
        piers.append(box(x - pw / 2 - 2, x + pw / 2 + 2, h, h + 10, zb - pw / 2 - 2, zb + pw / 2 + 2))
        piers.append(box(x - pw / 2, x + pw / 2, h + 10, h + p.bal_h - 8, zb - pw / 2, zb + pw / 2))
        # sunk panel faces
        piers.append(box(x - pw / 2 - 3, x + pw / 2 + 3, h + p.bal_h - 8, h + p.bal_h - 2, zb - pw / 2 - 3, zb + pw / 2 + 3))
        piers.append(box(x - pw / 2 - 1.5, x + pw / 2 + 1.5, h + p.bal_h - 2, h + p.bal_h + 4, zb - pw / 2 - 1.5, zb + pw / 2 + 1.5))
    rails = []
    bal = common.find_comp(design, 'Baluster')
    n_bal = 0
    for a, b in zip(xs[:-1], xs[1:]):
        x0, x1 = a + pw / 2, b - pw / 2
        rails.append(box(x0, x1, h, h + 12, zb - 13, zb + 13))                       # bottom rail (plinth)
        rails.append(box(x0, x1, h + p.bal_h - 13, h + p.bal_h - 4, zb - 12, zb + 12))  # handrail
        rails.append(box(x0, x1, h + p.bal_h - 4, h + p.bal_h, zb - 14, zb + 14))
        m = max(1, int(round((x1 - x0) / p.baluster_pitch)))
        dx = (x1 - x0) / m
        for i in range(m):
            place(side, bal, mat(x0 + dx * (i + 0.5), h + 12, zb))
            n_bal += 1
    common.deposit(side, [union_all(piers + rails)], 'Balustrade')

    # ---------------- benches: one per bay along the back row, plus one at each platform end
    bench = common.find_comp(design, 'Bench')
    zbench = z_ax - p.col_w / 2
    for k in range(n):
        place(side, bench, mat(p.x_f1 + (k + 0.5) * p.pitch, h, zbench))
    place(side, bench, mat(p.x_f1 - 300, h, zb + 60))
    place(side, bench, mat(p.x_f1 + n * p.pitch + 300, h, zb + 60))

    # ---------------- root occurrences: keep exactly two (NE identity, SW rotated 180 deg about Y)
    occs = [o for o in root.occurrences if o.component.name == 'Station Side']
    for o in occs[2:]:
        o.deleteMe()
    occs = occs[:2]
    while len(occs) < 2:
        occs.append(place(root, side, mat(0, 0, 0)))
    occs[0].transform2 = mat(0, 0, 0)
    occs[1].transform2 = mat(0, 0, 0, rot_y=math.pi)
    if design.snapshots.hasPendingSnapshot:
        design.snapshots.add()
    print('side built: %d piers, %d balusters; colonnade x %.0f..%.0f cm, axis z %.0f' %
          (len(xs), n_bal, p.x_f1, p.x_f1 + n * p.pitch, z_ax))
