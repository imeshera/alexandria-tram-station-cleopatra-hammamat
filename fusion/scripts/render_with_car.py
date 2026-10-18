# Scale render with a Raml car: imports the published STEP of Raml Car 223 (sibling repository
# alexandria-tram-raml-221-223, same axis convention: Y up, X along the car from the cab end, Y = 0 at top of rail),
# stands it at the NE platform, renders, then deletes the imported occurrence again (the station design does not
# keep it, and the tram design is not touched).
# run_doc(step_path): pass the STEP path explicitly (it lives outside this repository).
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, common
importlib.reload(common)
import adsk.core, adsk.fusion

here = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(here, '..', '..', 'docs', 'renders')
ns = {'__name__': 'fusion_lib', '__file__': os.path.join(here, 'render_views.py')}
exec(compile(open(ns['__file__']).read(), ns['__file__'], 'exec'), ns)

CAR_X = 1830.0          # cab end of the car, cm along the track (NE platform starts at 900)
VIEWS = {
    'scale-raml-car-223-iso': ((900, 900, 1700), (2700, 280, -400), dict(fov=0.85)),
    'scale-raml-car-223-elevation': ((2700, 380, 3600), (2700, 380, -400), dict(ortho=True, ext=2300)),
}


def run_doc(step_path):
    doc, design = common.activate()
    root = design.rootComponent
    before = set(o.entityToken for o in root.occurrences)
    im = common.app().importManager
    opts = im.createSTEPImportOptions(step_path)
    im.importToTarget(opts, root)
    new = [o for o in root.occurrences if o.entityToken not in before]
    p = common.Params(design)
    zt = -p.track_ctr / 2
    for o in new:
        o.transform2 = common.mat(CAR_X, 0, zt)
    if design.snapshots.hasPendingSnapshot:
        design.snapshots.add()
    ns['prepare'](design)
    for name, (eye, tgt, kw) in VIEWS.items():
        path = os.path.abspath(os.path.join(OUT, '2026-10-17_' + name + '.png'))
        ns['ns']['snap'](path, eye, tgt, 2000, 1250, **kw)
        ns['ns']['snap'](path, eye, tgt, 2000, 1250, **kw)
    for o in new:
        o.deleteMe()
    print('imported and removed', len(new), 'occurrence(s)')
