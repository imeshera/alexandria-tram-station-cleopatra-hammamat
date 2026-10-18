# Fusion build scripts

The station is one Autodesk Fusion design, **Cleopatra Hammamat Station** (project **Eshera-Personal**, folder
**Alexandria Tram Station - Cleopatra Hammamat**). Unlike the tram models, **everything is scripted**: an empty
design plus the scripts in [`scripts/`](scripts/) rebuilds the whole model. Every dimension is a user parameter
(`params.py`, with source and confidence in the comment); re-running a script deletes what it built before and
rebuilds it from the current parameters, and every instance follows.

Document axes: **Y up**, X along the track (+X north-east, towards Sidi Gaber El Sheikh), Z across (+Z south-east).
Origin: centre of the level crossing at top of rail. Units in the API are cm.

## Exec loader
Each script is a module with a `run(context)` function, executed by a small loader that passes `__file__` (the
scripts import `common.py` and find the lettering SVGs relative to themselves). Run it from *Scripts and Add-Ins*,
the Text Commands Python prompt, or any tool that executes Python inside Fusion (e.g. Fusion's MCP server):

```python
def run(_context: str):
    path = '<repo>/fusion/scripts/<script>.py'
    ns = {'__name__': 'fusion_script', '__file__': path}
    exec(compile(open(path).read(), path, 'exec'), ns)
    ns['run'](_context)
```

All scripts activate the station document **by name** first (`common.activate()`), so other open documents are
never touched; `common.save()` refuses to save outside the project folder above.

## Component structure
```
root
├─ Library (hidden)            instancing definitions
│   ├─ Column, Colonnette      Scamozzi-type Ionic columns
│   ├─ Frame                   2 × Column + transverse entablature
│   ├─ Canopy, Drum, Upper Canopy
│   ├─ Cartouche, Cartouche Upper, Plaque, Bench, Baluster
│   ├─ Canopy Module           Frame + Canopy (the repeating unit)
│   ├─ Tall Unit               Drum + Plaque + 4 Colonnettes + upper entablature + Upper Canopy + Cartouche Upper
│   └─ Tall Module             Frame + Tall Unit
├─ Station Side  (×2)          platform, paving, coping, ramp, balustrade + 142 balusters, 9 benches,
│                              6 Canopy Modules + 1 Tall Module + end Frame + Cartouche
│                              occurrence 1 = NE side (identity), occurrence 2 = SW side (180° about Y)
├─ Track                       rails, sleepers, track bed
├─ Street                      crossing slab with flangeways, carriageways, kerbs, verges
└─ OCS                         centre poles, bracket arms, contact wires
```
Occurrences are created with their transform (`addExistingComponent(comp, matrix)`); positions created that way
persist in the parametric design (moving nested occurrences afterwards does not — see the tram BUILD-LOGs).

## Build order
| # | Script | Builds |
|---|---|---|
| 1 | `params.py` | the user parameter table (creates or updates expressions and comments) |
| 2 | `build_column.py` | Column and Colonnette: plinth, Attic base, shaft with entasis, astragal, egg-and-dart echinus, 4 diagonal volutes with raised spirals, concave abacus |
| 3 | `build_frame.py` | Frame: two columns + entablature (2 fasciae, dentilled frieze, corona, cyma) |
| 4 | `build_canopy.py` | Canopy, Upper Canopy (hollow pot-shaped RC shells: moulded dentilled lip, lotus lappets, crown ring, finial) and Drum |
| 5 | `build_ornaments.py` | Cartouche (attic + credit line + oval laurel wreath tablet with sponsor text), Cartouche Upper, Plaque "كليوباترا", Bench, Baluster |
| 6 | `build_modules.py` | Canopy Module, Tall Unit, Tall Module |
| 7 | `build_side.py` | Station Side and its two root occurrences |
| 8 | `build_track.py` | Track, Street, OCS |
| 9 | `build_appearance.py` | weathered render colours, stained soffits, grime on column bases, lettering, paving, steel |
| – | `canvases.py` | calibrated satellite underlay (plan check); removed from published exports |
| – | `snap.py` | `snap(path, eye, target, ...)` viewport images with an explicit camera |
| – | `export.py` | STEP export and an F3D export with all canvases deleted in memory, then the document is closed without saving |

Changing `pitch`, `n_can`, `tall_idx`, `col_h` etc.: re-run `params.py`, then the scripts from the first one that
uses the parameter (e.g. `pitch` → 6, 7; `col_h` → 2, 3, 6, 7; `dome_rise` → 4).

## Lettering
Fusion's sketch text cannot shape Arabic. `tools/lettering/make_svgs.sh` lays the words out with CoreText
(`text2svg.swift`, from the tram repos) and writes glyph outlines as SVG in mm; `common.svg_text()` imports them,
drops the counters and extrudes raised letters (15–20 mm).
