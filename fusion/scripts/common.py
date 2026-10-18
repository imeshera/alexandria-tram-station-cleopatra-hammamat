# Shared helpers for the Cleopatra Hammamat station build scripts.
# Every script imports this module through the exec loader (see fusion/README.md), which passes __file__.
# Units: the Fusion API works in cm. Document is Y-up: X along the track (+X = north-east, towards
# Sidi Gaber El Sheikh), Y up from the top of rail, Z across (+Z = south-east side of the street).
import math
import adsk.core, adsk.fusion

DOC_NAME = 'Cleopatra Hammamat Station'
PROJECT = 'Eshera-Personal'
FOLDER = 'Alexandria Tram Station - Cleopatra Hammamat'

V3 = adsk.core.Vector3D.create
P3 = adsk.core.Point3D.create
tbm = adsk.fusion.TemporaryBRepManager.get()


def app():
    return adsk.core.Application.get()


def activate(name=DOC_NAME):
    """Activate this project's document by name (another agent may be using Fusion) and return the design."""
    a = app()
    docs = [d for d in a.documents if d.name == name]
    if not docs:
        raise RuntimeError('document not open: ' + name)
    doc = docs[0]
    if a.activeDocument != doc:
        doc.activate()
    return doc, adsk.fusion.Design.cast(doc.products.itemByProductType('DesignProductType'))


def save(doc, msg):
    """Save guard: only ever save into our own project folder."""
    df = doc.dataFile
    if df.parentProject.name != PROJECT or df.parentFolder.name != FOLDER:
        raise RuntimeError('refusing to save: wrong project/folder')
    return doc.save(msg)


class Params:
    """Evaluate user parameters: p.x -> value in cm (or unitless)."""
    def __init__(self, design):
        self._um = design.unitsManager
        self._d = design

    def __getattr__(self, name):
        prm = self._d.userParameters.itemByName(name)
        if prm is None:
            raise AttributeError('missing user parameter ' + name)
        return prm.value


# ---------------------------------------------------------------- components
def find_comp(design, name):
    for c in design.allComponents:
        if c.name == name:
            return c
    return None


def root_occ(design, name):
    root = design.rootComponent
    for o in root.occurrences:
        if o.component.name == name:
            return o
    return None


def ensure_comp(design, name, parent=None):
    """Return a component by name, creating it (one occurrence under parent/root, identity) if missing."""
    c = find_comp(design, name)
    if c is not None:
        return c
    parent = parent or design.rootComponent
    o = parent.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    o.component.name = name
    return o.component


def new_definition_comp(design, name):
    """A component used only as an instancing definition: kept in a hidden 'Library' occurrence group."""
    c = find_comp(design, name)
    if c is not None:
        return c
    lib = ensure_comp(design, 'Library')
    o = lib.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    o.component.name = name
    return o.component


def clear_comp(comp, keep_occurrences=False):
    """Delete everything a script built in a component (features, sketches, planes, bodies, child occurrences)."""
    if not keep_occurrences:
        for i in range(comp.occurrences.count - 1, -1, -1):
            comp.occurrences.item(i).deleteMe()
    feats = comp.features
    for i in range(feats.count - 1, -1, -1):
        f = feats.item(i)
        if f.isValid:
            f.deleteMe()
    for i in range(comp.sketches.count - 1, -1, -1):
        comp.sketches.item(i).deleteMe()
    for i in range(comp.constructionPlanes.count - 1, -1, -1):
        comp.constructionPlanes.item(i).deleteMe()
    for i in range(comp.bRepBodies.count - 1, -1, -1):
        comp.bRepBodies.item(i).deleteMe()


def mat(tx=0.0, ty=0.0, tz=0.0, rot_y=0.0):
    m = adsk.core.Matrix3D.create()
    if rot_y:
        m.setToRotation(rot_y, V3(0, 1, 0), P3(0, 0, 0))
    m.translation = V3(tx, ty, tz)
    return m


def place(parent, comp, m):
    return parent.occurrences.addExistingComponent(comp, m)


# ---------------------------------------------------------------- temporary B-Rep primitives
def box(x0, x1, y0, y1, z0, z1):
    c = P3((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)
    return tbm.createBox(adsk.core.OrientedBoundingBox3D.create(
        c, V3(1, 0, 0), V3(0, 1, 0), abs(x1 - x0), abs(y1 - y0), abs(z1 - z0)))


def cyl(p0, p1, r0, r1=None):
    return tbm.createCylinderOrCone(P3(*p0), r0, P3(*p1), r0 if r1 is None else r1)


def vcyl(x, z, y0, y1, r0, r1=None):
    return cyl((x, y0, z), (x, y1, z), r0, r1)


def torus(c, axis, R, r):
    return tbm.createTorus(P3(*c), V3(*axis), R, r)


def sphere(c, r):
    return tbm.createSphere(P3(*c), r)


def union_all(bodies):
    bodies = [b for b in bodies if b is not None]
    if not bodies:
        return None
    acc = bodies[0]
    for b in bodies[1:]:
        tbm.booleanOperation(acc, b, adsk.fusion.BooleanTypes.UnionBooleanType)
    return acc


def moved(body, m):
    b = tbm.copy(body)
    tbm.transform(b, m)
    return b


def rot_about(axis, ang, origin=(0, 0, 0)):
    m = adsk.core.Matrix3D.create()
    m.setToRotation(ang, V3(*axis), P3(*origin))
    return m


def compose(*ms):
    """compose(a, b, c) applies a, then b, then c."""
    out = adsk.core.Matrix3D.create()
    for m in ms:
        out.transformBy(m)
    return out


def deposit(comp, bodies, name, appearance=None):
    """Add temporary bodies to a component inside one base feature; returns the new BRepBodies."""
    bodies = [b for b in bodies if b is not None]
    bf = comp.features.baseFeatures.add()
    bf.startEdit()
    out = []
    for b in bodies:
        out.append(comp.bRepBodies.add(b, bf))
    bf.finishEdit()
    bf.name = name
    res = [bb for bb in bf.bodies]
    for i, bb in enumerate(res):
        bb.name = name if len(res) == 1 else '%s %d' % (name, i + 1)
        if appearance is not None:
            bb.appearance = appearance
    return res


# ---------------------------------------------------------------- revolve helper
def revolve_profile(comp, segs, name, axis='y'):
    """Revolve a closed (r, y) profile (cm) about the component Y axis; returns temporary copies of the bodies
    and deletes the sketch/feature.  segs: list of ('P', (r, y)) / ('S', [(r, y), ...]) items walking the loop;
    the loop starts at the first point of the first item and closes back to it."""
    sk = comp.sketches.add(comp.xYConstructionPlane)
    sk.isComputeDeferred = True
    lines = sk.sketchCurves.sketchLines
    spl = sk.sketchCurves.sketchFittedSplines
    cur = None          # Point3D before the first curve exists, then a SketchPoint
    first_sp = None
    for kind, data in segs:
        if kind == 'P':
            p = P3(data[0], data[1], 0)
            if cur is None:
                cur = p
                continue
            ln = lines.addByTwoPoints(cur, p)
            if first_sp is None:
                first_sp = ln.startSketchPoint
            cur = ln.endSketchPoint
        elif kind == 'S':
            oc = adsk.core.ObjectCollection.create()
            oc.add(cur)
            for (r, y) in data:
                oc.add(P3(r, y, 0))
            s_ = spl.add(oc)
            if first_sp is None:
                first_sp = s_.startSketchPoint
            cur = s_.endSketchPoint
    lines.addByTwoPoints(cur, first_sp)
    sk.isComputeDeferred = False
    prof = None
    best = 0
    for i in range(sk.profiles.count):
        a = sk.profiles.item(i).areaProperties().area
        if a > best:
            best, prof = a, sk.profiles.item(i)
    ri = comp.features.revolveFeatures.createInput(prof, comp.yConstructionAxis,
                                                    adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ri.setAngleExtent(False, adsk.core.ValueInput.createByReal(2 * math.pi))
    rf = comp.features.revolveFeatures.add(ri)
    out = [tbm.copy(b) for b in rf.bodies]
    rf.deleteMe()
    sk.deleteMe()
    return out


def poly_extrude(comp, pts, z0, z1):
    """Extrude a closed polygon drawn on the component XY plane (sketch x = X, y = Y) from Z = z0 to z1;
    returns temporary copies and removes the sketch/feature."""
    sk = comp.sketches.add(comp.xYConstructionPlane)
    sk.isComputeDeferred = True
    lines = sk.sketchCurves.sketchLines
    ln = lines.addByTwoPoints(P3(pts[0][0], pts[0][1], 0), P3(pts[1][0], pts[1][1], 0))
    first = ln.startSketchPoint
    prev = ln.endSketchPoint
    for (x, y) in pts[2:]:
        prev = lines.addByTwoPoints(prev, P3(x, y, 0)).endSketchPoint
    lines.addByTwoPoints(prev, first)
    sk.isComputeDeferred = False
    prof = max([sk.profiles.item(i) for i in range(sk.profiles.count)], key=lambda p: p.areaProperties().area)
    ei = comp.features.extrudeFeatures.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ei.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(z1 - z0)),
                        adsk.fusion.ExtentDirections.PositiveExtentDirection)
    ei.startExtent = adsk.fusion.OffsetStartDefinition.create(adsk.core.ValueInput.createByReal(z0))
    ef = comp.features.extrudeFeatures.add(ei)
    out = [tbm.copy(b) for b in ef.bodies]
    ef.deleteMe()
    sk.deleteMe()
    return out


# ---------------------------------------------------------------- appearances
def appearance(design, name, rgb, base='Paint - Enamel Glossy (White)', gloss=None):
    """Get or create a local appearance with the given colour (copied from a library appearance)."""
    a = design.appearances.itemByName(name)
    if a is None:
        lib = None
        for l in app().materialLibraries:
            if l.name in ('Fusion Appearance Library', 'Fusion 360 Appearance Library'):
                lib = l
        src = lib.appearances.itemByName(base)
        a = design.appearances.addByCopy(src, name)
    for i in range(a.appearanceProperties.count):
        pr = a.appearanceProperties.item(i)
        if isinstance(pr, adsk.core.ColorProperty) and pr.id in ('generic_diffuse', 'opaque_albedo', 'surface_albedo'):
            pr.value = adsk.core.Color.create(rgb[0], rgb[1], rgb[2], 255)
    return a


# ---------------------------------------------------------------- lettering (CoreText SVG -> raised solids)
PX_PER_MM = 3.7795275591      # Fusion reads SVG user units as 96-dpi px
SVG_DIR = None


def svg_path(name):
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, '..', '..', 'tools', 'lettering', 'svg', name)


def _ink_box(sk):
    bbs = [cv.boundingBox for cv in sk.sketchCurves]
    return (min(b.minPoint.x for b in bbs), min(b.minPoint.y for b in bbs),
            max(b.maxPoint.x for b in bbs), max(b.maxPoint.y for b in bbs))


def _loop_key(lp):
    pts = []
    for c in lp.profileCurves:
        b = c.boundingBox
        pts += [b.minPoint, b.maxPoint]
    return (round(min(p.x for p in pts), 3), round(min(p.y for p in pts), 3),
            round(max(p.x for p in pts), 3), round(max(p.y for p in pts), 3))


def svg_text(comp, svgfile, cx, by, h, depth, max_w=None):
    """Raised text from a CoreText SVG, drawn on the component XY plane (reads correctly from +Z):
    ink box centred on x = cx, bottom at y = by, ink height h (or narrower to fit max_w); extruded from
    z = 0 to z = depth. Returns temporary bodies and removes the sketch/feature."""
    sk = comp.sketches.add(comp.xYConstructionPlane)
    sk.importSVG(svgfile, 0, 0, PX_PER_MM)
    x0, y0, x1, y1 = _ink_box(sk)
    sk.deleteMe()
    s = h / (y1 - y0)
    if max_w and s * (x1 - x0) > max_w:
        s = max_w / (x1 - x0)
    sk = comp.sketches.add(comp.xYConstructionPlane)
    sk.isComputeDeferred = True
    sk.importSVG(svgfile, cx - s * (x0 + x1) / 2, by - s * y0, PX_PER_MM * s)
    sk.isComputeDeferred = False
    holes = set()
    for i in range(sk.profiles.count):
        for lp in sk.profiles.item(i).profileLoops:
            if not lp.isOuter:
                holes.add(_loop_key(lp))
    profs = adsk.core.ObjectCollection.create()
    for i in range(sk.profiles.count):
        pr = sk.profiles.item(i)
        outer = [lp for lp in pr.profileLoops if lp.isOuter][0]
        if _loop_key(outer) not in holes:
            profs.add(pr)
    ei = comp.features.extrudeFeatures.createInput(profs, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ei.setDistanceExtent(False, adsk.core.ValueInput.createByReal(depth))
    f = comp.features.extrudeFeatures.add(ei)
    out = [tbm.copy(b) for b in f.bodies]
    f.deleteMe()
    sk.deleteMe()
    return out


def ellipse_pts(a, b, n=72, cx=0.0, cy=0.0):
    return [(cx + a * math.cos(2 * math.pi * i / n), cy + b * math.sin(2 * math.pi * i / n)) for i in range(n)]
