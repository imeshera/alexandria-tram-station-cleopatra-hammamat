# Calibrated underlay for overlay checks (plan): Esri World Imagery crop (z19, 0.255 m/px upscaled 2x
# = 12.75 cm per image pixel, north up) on a horizontal plane just above the street.
# The image is third-party: it is NOT in the repository (references/images/ is git-ignored) and every canvas is
# deleted from the published exports (export.py). Put the crop in references/images/ to recreate it.
#
# Calibration: the red GPS mark of the owner's photos (pixel 500, 400) sits on the trackbed 8.5 m north-east of
# the SW colonnade end (satellite: 67 px along the track) and 5.6 m north-west of its axis -> model (-850, 5) cm.
# The track runs at azimuth 56 deg in the image (both colonnade bands); +X = 56 deg, +Z = 146 deg.
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, common
importlib.reload(common)
import adsk.core, adsk.fusion

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'references', 'images',
                   '04_cleopatra-hammamat_satellite_esri-z19.jpg')
W_PX, H_PX, S = 1000.0, 700.0, 12.75        # image size, cm per pixel
CAM_PX = (500.0, 400.0)
CAM_XZ = (-850.0, 5.0)
AZ = math.radians(56.0)


def run(_context: str):
    doc, design = common.activate()
    root = design.rootComponent
    for i in range(root.canvases.count - 1, -1, -1):
        root.canvases.item(i).deleteMe()
    for i in range(root.constructionPlanes.count - 1, -1, -1):
        if root.constructionPlanes.item(i).name == 'Underlay plane':
            root.constructionPlanes.item(i).deleteMe()
    pi = root.constructionPlanes.createInput()
    pi.setByOffset(root.xZConstructionPlane, adsk.core.ValueInput.createByReal(1.0))
    pl = root.constructionPlanes.add(pi)
    pl.name = 'Underlay plane'
    pl.isLightBulbOn = False
    # pixel -> model:  X = Xc + S*( sin(az) dpx - cos(az) dpy ),  Z = Zc + S*( cos(az) dpx + sin(az) dpy )
    sa, ca = math.sin(AZ), math.cos(AZ)
    # normalised u = px / W, v = 1 - py / H  ->  dpx = W u - cx,  dpy = H (1 - v) - cy
    def model(u, v):
        dpx, dpy = W_PX * u - CAM_PX[0], H_PX * (1 - v) - CAM_PX[1]
        return (CAM_XZ[0] + S * (sa * dpx - ca * dpy), CAM_XZ[1] + S * (ca * dpx + sa * dpy))
    ci = root.canvases.createInput(IMG, pl)
    # plane coordinates on an XZ-offset plane in a Y-up design: u = +Z, v = +X (queried from Plane.geometry)
    o = model(0, 0)
    ux = model(1, 0)
    vy = model(0, 1)
    m = adsk.core.Matrix2D.create()
    m.setCell(0, 0, ux[1] - o[1]); m.setCell(0, 1, vy[1] - o[1]); m.setCell(0, 2, o[1])
    m.setCell(1, 0, ux[0] - o[0]); m.setCell(1, 1, vy[0] - o[0]); m.setCell(1, 2, o[0])
    ci.transform = m
    ci.opacity = 60
    ci.isDisplayedThrough = True
    cv = root.canvases.add(ci)
    cv.name = 'Underlay satellite (Esri, not distributed)'
    print('canvas added', cv.name)
