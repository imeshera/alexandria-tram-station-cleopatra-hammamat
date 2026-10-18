# Build log: Cleopatra Hammamat station

Decisions, measurements and Fusion API gotchas, in the order they happened.

## 2026-10-17 — Research pass: settling the structure and the counts
- Inputs: the research dossier (identification, history, status, v0 photogrammetry from the owner's six night
  photos), ~120 YouTube frames (2022–2026), five aaha.ch thumbnails and Esri crops. Frames are reference only and
  stay out of the repo (`references/manifests/` lists them).
- **The module is a transverse frame, not a square bay.** Two columns across the platform under one beam; the beams
  recede one behind the other in the along-platform views (6IYrhhEwTqE t01m00, LjFTTQorR9o t05m54).
- **Canopies span between frames.** From the trackbed each lip reads as an arch whose feet sit on consecutive
  beam blocks, and the domes are centred between frames (LjFTTQorR9o t06m56–t07m24). I first read the arches as
  bowls centred on the frames; the perspective of a horizontal circle seen from below (near half of the ring
  appears as the arch) resolves it. So N canopies need N + 1 frames, and the lip diameter equals the pitch.
- **Canopies are hollow shells** (concave soffit; the far half of the lip looks like a flat "bottom" from below).
  The broken canopy in Wi4t1OngdrE shows ≈ 8 cm RC on a rebar cage.
- **Counts:** 7 canopies on 8 frames per colonnade; the 4th canopy is the drum of the two-tier unit; the 1st
  (crossing end) carries the cartouche. 01YNkcHynps t13m22 (NE colonnade) gives cartouche + 2 + drum + 3; the
  opposite-direction video hBRSKXDcvPw shows the SW colonnade with the same layout. The dossier's v0 "7 low modules
  + 1 tall unit" becomes "7 canopies, one of which is the tall unit".
- **Two colonnades, point-symmetric about the crossing.** Both 2024 videos (opposite directions) show a colonnade on
  the left of the car just after the crossing, cartouche end first; the satellite shows the SW band on the SE side
  and the NE band on the NW side. Modelled as one "Station Side" component instanced twice (identity + 180° about Y).
- **Lettering:** LjFTTQorR9o t05m58 reads the cartouche as "شركة / قصر السلام / …" and the frieze line as "تصميم المعماري
  م/ …"; the drum plaque is "كليوباترا". The third cartouche line and the architect's name stay blank.
- Dimension sheet v1: `references/notes/dimensions.md`. The weakest numbers are absolute scale (column height,
  ±15 %) and the dome profile.

## 2026-10-17 — Pass 1: fully scripted model
- New design **Cleopatra Hammamat Station** in its own folder; Hybrid design intent; Y-up; origin at the crossing
  centre at top of rail, +X north-east along the track, +Z south-east.
- Unlike the tram models, **everything is scripted** (no interactive timeline features), so the parameter table is
  the single source of truth and an empty design rebuilds completely.
- Geometry pattern: build in a component with sketches + revolve/extrude features, copy the bodies into
  `TemporaryBRepManager`, combine/transform them there, deposit the result into one **base feature**, delete the
  helper features. Keeps the timeline short (one base feature per part) and instancing cheap.
- Instancing: definitions live under a hidden **Library** occurrence; modules and sides place them with
  `occurrences.addExistingComponent(comp, matrix)`. Gotcha (from the tram repos): moving a nested occurrence after
  creation does not persist; **creating it with the matrix does** (tested: no pending snapshot, transforms survive
  recompute).
- Columns: profile revolve (Attic base, entasis spline, astragal, echinus), plinth box, concave abacus (box minus
  four cylinders), 16 egg spheres, four diagonal volutes (disc + bolster + extruded Archimedean spiral ribbon + eye)
  rotated to the diagonals.
- Canopy shell: one closed revolve profile (lip with bead, recessed dentil zone, ovolo; pot-shaped dome spline;
  crown ring with cornice; inner offset spline); 132 radial dentil blocks; lotus lappets = a 2 cm skin over the
  upper dome intersected with eight plan-view wedge prisms (a down-pointing triangle on the dome is a radial wedge
  in plan).
- Gotcha: on an XZ construction plane in a Y-up design the plane axes are **u = +Z, v = +X** (queried from
  `Plane.geometry`), not (X, −Z). The first satellite canvas came out rotated 90°.
- Gotcha: Fusion sketch text cannot shape Arabic (from the tram repos) → `tools/lettering/text2svg.swift`
  (CoreText) writes outlines as SVG; `common.svg_text()` imports on the XY plane (reads correctly from +Z), drops
  counters by matching outer loops against inner loops, extrudes, and the bodies are rotated to face −X.
- Gotcha: long scripts (ornaments with 284 instanced balusters + the appearance pass) time out the MCP call but
  finish in Fusion. Wait, then verify read-only before re-running.
- Gotcha: after one timed-out appearance run, body appearances read back as the default "Steel - Satin" on part of
  the model; re-running `build_appearance.py` fixed it and it survived a save. Check appearances read-only after
  any timed-out run.
- Plan check: Esri crop as a canvas (12.75 cm/px, track azimuth 56°, calibrated on the owner's GPS mark). The SW
  colonnade sits on its satellite band; the NE band lies ≈ 2–3 m further north-west than the model (axes 14 ± 2 m
  apart in the imagery vs 11.3 m modelled).
- Dome rise lowered 2.05 → 1.85 m (0.65 × lip) after comparing with the from-below frames; upper dome 1.65 m.
- Exports: `export.py` deletes the canvases in memory, writes STEP and F3D, closes the document without saving and
  reopens it (the stored design keeps its underlay). F3D image check: none.
- Renders: `render_views.py` (viewport, canvases hidden) → `docs/renders/2026-10-17_*.png`.

## 2026-10-17 — Pass 2: urn canopies, cartouche, scale render
- **Photo-matched check.** A model view set up like 01YNkcHynps t13m22 (camera in the car on the far track, ≈ 26°
  yaw, ≈ 2.4 m above rail) next to the frame showed the canopies were wrong: they are **urns** — a convex bowl below
  the lip resting on the beams, the lip at the equator, and a lower dome cap — not half-domes sitting on the lip.
  Reworked `build_canopy.py`: bowl (0.55 m) from a bottom rim Ø 2.44 m (bearing ≈ 8 cm on each neighbouring beam)
  with a 0.12 m concave soffit dish, lip at the equator, dome rise 1.85 → 1.25 m; upper canopy and drum get the
  same bowl. Tall-unit heights follow `bowl_h`. Overall crown height barely changed (4.83 → 4.78 m).
- The canopies are now modelled solid (outer surfaces only): a closed internal void would be useless for printing.
- Cartouche enlarged to the photographed proportions (tablet 1.52 × 1.12 m, attic 0.40 m) and the lettering with it.
- Drum plaque had been placed 7.5 cm inside the drum wall (only the frame edges showed); moved out to the wall face.
- Scale render: `render_with_car.py` imports `Raml Car 223.step` from the 221-223 repository (same axis convention),
  stands it on the NE platform track, renders and deletes it. The car roof (≈ 3.4 m) reaches just under the canopy
  bowls (3.8 m above rail), as in the 2024 frames with cars at the platform (3nKi0T8XbfM).
- Pattern for long MCP calls: the script writes a flag file at the end; the shell waits for the flag
  (`until [ -f flag ]`) instead of guessing a sleep.

## 2026-10-17 — Export fix
- **Gotcha:** deleting the hidden *Library* occurrence before export (to keep the definitions out of the STEP)
  deleted the definition components and **every instance of them** — the pass-1/pass-2 exports held only the
  platforms, track and street (5 products, planar faces only). The Library now stays; hidden occurrences are left out
  of the STEP anyway. Corrected exports: STEP 26 MB, 599 solids, full assembly structure (Station Side ×2 →
  Canopy Module ×6, Tall Module, Frame, Column, 142 Balusters…); F3D 11 MB, no images.
- Check exports by counting `MANIFOLD_SOLID_BREP` and `NEXT_ASSEMBLY_USAGE_OCCURRENCE` in the STEP, not by size.
