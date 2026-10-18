# Viewport snapshot with an explicit camera (activates the station document by name).
# snap(path, eye, target, w, h, ortho=False, fov=None): eye/target in cm, Y up.
# show(names) / hide(names): toggle root occurrences by component name before a snapshot.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, common
importlib.reload(common)
import adsk.core, adsk.fusion


def visible(design, names, on):
    for o in design.rootComponent.occurrences:
        if o.component.name in names:
            o.isLightBulbOn = on


def snap(path, eye, target, w=1800, h=1100, ortho=False, fov=None, up=(0, 1, 0), ext=None):
    doc, design = common.activate()
    a = common.app()
    vp = a.activeViewport
    cam = vp.camera
    cam.isSmoothTransition = False
    cam.cameraType = (adsk.core.CameraTypes.OrthographicCameraType if ortho
                      else adsk.core.CameraTypes.PerspectiveCameraType)
    cam.eye = adsk.core.Point3D.create(*eye)
    cam.target = adsk.core.Point3D.create(*target)
    cam.upVector = adsk.core.Vector3D.create(*up)
    if fov:
        cam.perspectiveAngle = fov
    if ortho and ext:
        cam.viewExtents = ext
    vp.camera = cam
    vp.refresh()
    adsk.doEvents()
    ok = vp.saveAsImageFile(path, w, h)
    if not ok:
        adsk.doEvents()
        ok = vp.saveAsImageFile(path, w, h)
    print('saved', ok, path)
    return ok
