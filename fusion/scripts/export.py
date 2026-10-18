# Published exports (models/): STEP (AP214) and F3D, both WITHOUT the calibrated canvases (third-party imagery)
# and without the hidden 'Library' occurrence (its definitions stay alive through the placed instances).
# Both are removed in memory only; the document is then closed WITHOUT saving and reopened, so the stored design
# keeps its underlays. Save the document before running this.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, common
importlib.reload(common)
import adsk.core, adsk.fusion

here = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(here, '..', '..', 'models'))


def run(_context: str):
    doc, design = common.activate()
    if doc.isModified:
        raise RuntimeError('save the document first (export closes it without saving)')
    df = doc.dataFile
    root = design.rootComponent
    for i in range(root.canvases.count - 1, -1, -1):
        root.canvases.item(i).deleteMe()
    lib = common.root_occ(design, 'Library')
    if lib:
        lib.deleteMe()
    em = design.exportManager
    step = os.path.join(OUT, common.DOC_NAME + '.step')
    f3d = os.path.join(OUT, common.DOC_NAME + '.f3d')
    print('step', em.execute(em.createSTEPExportOptions(step, root)))
    print('f3d', em.execute(em.createFusionArchiveExportOptions(f3d, root)))
    doc.close(False)
    common.app().documents.open(df)
    print('reopened', common.app().activeDocument.name)
