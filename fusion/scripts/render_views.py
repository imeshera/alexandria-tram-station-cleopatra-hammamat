# Viewport renders for docs/renders/ (canvases and the Library hidden first, so no third-party image shows).
# run(context) renders every view in VIEWS; run_one(name) renders one.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, common
importlib.reload(common)
import adsk.core, adsk.fusion

here = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(here, '..', '..', 'docs', 'renders')
ns = {'__name__': 'fusion_lib', '__file__': os.path.join(here, 'snap.py')}
exec(compile(open(ns['__file__']).read(), ns['__file__'], 'exec'), ns)

# name: (eye, target, kwargs) in cm; NE colonnade x 1700..3695, axis z -565; SW mirrored through the origin
VIEWS = {
    'overview-iso': ((-2400, 2100, 3900), (0, 150, 0), dict(fov=0.8)),
    'ne-colonnade-iso': ((600, 1300, 1500), (2700, 300, -565), dict(fov=0.8)),
    'ne-colonnade-elevation': ((2700, 420, 3400), (2700, 420, -565), dict(ortho=True, ext=2600)),
    'ne-colonnade-from-crossing': ((-150, 330, -380), (2400, 380, -560), dict(fov=0.9)),
    'sw-platform-eye-level': ((-1350, 210, 520), (-3000, 330, 600), dict(fov=0.95)),
    'cartouche-detail': ((1080, 470, -420), (1700, 400, -565), dict(fov=0.7)),
    'two-tier-unit': ((2700, 380, 900), (2700, 520, -565), dict(fov=0.75)),
    'under-canopy': ((2050, 170, -470), (2900, 330, -600), dict(fov=1.0)),
    'capital-detail': ((2185, 255, -330), (2270, 300, -500), dict(fov=0.5)),
    'end-elevation': ((-1500, 420, -565), (1700, 420, -565), dict(ortho=True, ext=900)),
}


def prepare(design):
    for c in design.rootComponent.canvases:
        c.isLightBulbOn = False
    ns['visible'](design, ['Library'], False)


def run_one(name, prefix='2026-10-17_'):
    doc, design = common.activate()
    prepare(design)
    eye, tgt, kw = VIEWS[name]
    path = os.path.abspath(os.path.join(OUT, prefix + name + '.png'))
    ns['snap'](path, eye, tgt, 2000, 1250, **kw)
    ns['snap'](path, eye, tgt, 2000, 1250, **kw)
    return path


def run(_context: str):
    for n in VIEWS:
        run_one(n)
