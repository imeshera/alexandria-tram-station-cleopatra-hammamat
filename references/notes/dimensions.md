# Dimension sheet v1 — Cleopatra Hammamat station (as intact, c. 2024)

Refines the v0 sheet in the research dossier (owner's night photos, March 2026) with the daylight frames scraped
from YouTube (2022–2026) and the Esri imagery. Every value below is a Fusion user parameter (`fusion/scripts/params.py`);
the parameter comment repeats the source and the confidence.

Confidence: **HIGH** published/standard · **MEDIUM** two independent methods agree within ~10 % · **LOW-MED** one
good method · **LOW** estimate from proportions or a single oblique frame.

Sources (frames are personal reference only and are not in this repository; see `references/SOURCES.md`):
OS = owner's iPhone photos IMG_9502–9511 (24/39/48 mm-eq, EXIF intrinsics); YT = YouTube frames, video ID + time;
SAT = Esri World Imagery, 0.255 m/px (ticks every 5 m); DOS = research dossier v0.

## 1. Layout — what the frames settle

### 1.1 Structure of a module (new in v1)
The night photos could not show how the canopies are carried. The daylight frames do:

- **Transverse frames, not square bays.** Each "frame" is **two columns across the platform** (one at the track
  side, one at the street side) under **one transverse entablature beam**. Looking along the platform
  (YT 6IYrhhEwTqE t01m00/t01m03, LjFTTQorR9o t05m54) the beams recede one behind the other, each on its own pair
  of columns, and the two column rows run along the platform.
- **Each canopy spans between two neighbouring frames.** Seen from the trackbed (LjFTTQorR9o t06m56–t07m24),
  every canopy lip reads as an arch whose feet sit on two consecutive beam blocks, and the dome centres lie midway
  between frames. The lips of neighbouring canopies meet above each beam. So **N canopies stand on N + 1 frames**,
  and the lip diameter equals the frame pitch.
- **The canopies are urns, not half-domes.** A model view set up like YouTube 01YNkcHynps t13m22 showed that a
  plain dome on the lip was wrong: every canopy has a **convex bowl below the lip** ("neck", ≈ 0.55 m deep) whose
  bottom rim bears on the two neighbouring beams, the moulded **lip band at the equator**, and a **lower dome cap**
  above it (≈ 1.25 m to the crown top). Under the bowl is a shallow **concave soffit dish** (lit dish with a darker
  rim in the owner's night shots). The broken canopy in Wi4t1OngdrE t03m36 shows a thin RC shell (≈ 8 cm) on a
  rebar cage; the model keeps the outer surfaces and is solid inside.
- **Capitals are four-faced (Scamozzi-type) Ionic**, with volutes on the diagonals: volutes show both on the
  track-side views and on the along-platform views (6IYrh, LjFT t05m58).

### 1.2 Counts (settled from the 2024 window frames)
| Item | Count | Evidence | Confidence |
|---|---|---|---|
| Canopies per colonnade | **7** | 01YNkcHynps t13m22 (route-1 car, NE colonnade): cartouche canopy + 2 + drum + 3; hBRSKXDcvPw t21m05–t21m08 (opposite direction, SW colonnade): drum with 3 canopies beyond it; OS IMG_9502: 8 front columns visible beyond the tree | MEDIUM |
| Frames (column pairs) per colonnade | **8** (16 columns) | 01YNk t13m22: front columns at x ≈ 345, 690, 880, 1000, 1085, 1150, 1195, 1235 px | MEDIUM |
| Two-tier unit position | **4th canopy from the crossing end** (centre of 7) | 01YNk t13m22 (drum plaque "كليوباترا" on the 4th bowl), LjFT t07m08–t07m24 (three canopies on the far side of the drum) | MEDIUM |
| Upper colonnettes | **4**, on the drum deck, carrying a square entablature and the upper dome | LjFT t07m00, 01YNk t13m22 | MEDIUM |
| Cartouche canopy | **1st canopy, at the crossing end**; the oval wreath tablet stands on an attic block on the end beam and faces the crossing; the upper dome carries a second tablet facing the same way | 01YNk t13m21/22, hBRSK t21m03, LjFT t05m54/t05m58 | MEDIUM |
| Colonnades | **2**, point-symmetric about the level crossing: SW of the crossing on the SE side of the street (the one the owner photographed), NE of the crossing on the NW side; each has its cartouche end facing the crossing | SAT (two white scalloped bands, axes ≈ 14 m apart across the street), 01YNk and hBRSK show a colonnade on the left of the car after the crossing in **both** directions | MEDIUM (design of the NE twin = identical: same counts in both videos) |
| Total columns | 32 main + 8 colonnettes | — | MEDIUM |

The dossier's v0 guess (7 low modules + 1 two-tier unit, "taller central unit at about mid-length") is confirmed
in count, with the correction that the two-tier unit *replaces* the 4th canopy (7 canopies in all, not 8).

### 1.3 Plan positions
| Dimension | Model | Method | Confidence |
|---|---|---|---|
| Frame pitch = lip diameter | 2.85 m | SAT colonnade lengths 19–21 m / 7; YT LjFT t07m12 pitch ≈ 1.18 × column height (foreshortened ≈ 0.88) | LOW-MED |
| Colonnade length (lip to lip) | 19.95 m | 7 × pitch | LOW-MED |
| Crossing centre → first frame | 17 m | OS camera (8.6 m NE of the SW colonnade end on SAT) ~10 m from the OSM crossing nodes; SAT gap between colonnade ends ≈ 43 m incl. the 10 m street | LOW |
| Track centres | 3.8 m (centre poles) | YT 01YNk t13m21 (poles between the tracks); SAT axis spacing 14 ± 2 m minus platform offsets | LOW |
| Track centre → platform edge | 1.40 m | 2.42 m car + gap | LOW-MED |
| Platform width | 4.20 m | YT 6IYrh, 3nKi t01m00; DOS 4–5 m | LOW |
| Platform edge → front column centre | 1.70 m | YT 3nKi t01m00 (car side to column face), 6IYrh | LOW |
| Column spacing across a frame (c–c) | 1.30 m (≈ 3.8 D) | YT 6IYrh t01m00 (pair at equal depth: 3.5 D), LjFT t05m54 (≈ 3.75 D) | LOW-MED |
| Colonnade axis from track centre | 5.65 m | sum of the above; SAT axes 14 ± 2 m apart vs model 11.3 m | LOW |

## 2. Elevations
| Dimension | Model | Method | Confidence |
|---|---|---|---|
| Platform above rail head | 0.50 m | DOS rail-gauge ground plane 0.55 ± 0.10; YT 3nKi car skirt (0.70 m) just above the platform | MED-LOW |
| Column (plinth bottom → abacus top) | 2.40 m | DOS 2.25 (rail gauge) / 2.9 (seated person); YT hBRSK t21m06 standing woman (≈ 1.6 m) ≈ 0.67 of the column at a slightly nearer depth | LOW-MED |
| Column lower diameter | 0.34 m | DOS 0.32–0.38 (90 px at 10 m); H/D 7.1 scale-free | MEDIUM ratio / LOW-MED absolute |
| Plinth | 0.58 m square × 0.20 m | YT 3nKi t01m00, 6IYrh (≈ 1.7 D) | LOW-MED |
| Entablature | 0.38 m (architrave 2 fasciae, frieze with dentil blocks, corona + cyma) | DOS 0.16 H; frames LjFT t06m02, t05m58 | LOW-MED |
| Beam | 0.50 m deep × 1.90 m long | abacus width + overhang | LOW |
| Lip band | 0.20 m high, 0.16 m wide, dentils 40/26 mm | LjFT t06m02 | LOW-MED |
| Bowl below the lip / bottom rim / soffit dish | 0.55 m / Ø 2.44 m / 0.12 m rise | 01YNk t13m22 (bowl ≈ 0.23 of the column height), model overlay | LOW-MED / LOW / LOW |
| Dome rise, lip top → crown top | 1.25 m (0.44 × lip) | 01YNk t13m22 overlay (≈ 0.5 of the column height), hBRSK t21m06 | LOW |
| Crown ring | Ø 1.50 m × 0.30 m, dentilled | LjFT t06m58 (≈ 0.53 lip) | LOW-MED |
| Shell thickness | 80 mm | Wi4t1 t03m36 | MED-LOW |
| Low canopy, platform → crown top | 4.78 m (+ 0.42 m finial) | sum; DOS estimate 5.5–6 m | LOW |
| Drum wall above the lip | 0.60 m + cornice, flat deck | LjFT t07m00 | LOW |
| Upper colonnettes | 1.40 m, Ø 0.22 m, square 1.30 m c–c | 01YNk t13m22 (≈ 0.55–0.6 of the main columns) | LOW |
| Upper entablature / lip / bowl / dome rise | 0.30 m / Ø 2.50 m / 0.48 m / 1.15 m | LjFT t07m00 (upper lip ≈ drum width), 01YNk t13m22 | LOW |
| Two-tier unit, platform → crown top / finial | 7.15 m / 7.80 m | sum; DOS estimate 8–9 m | LOW |
| Balustrade | 0.95 m; piers 0.36 m at 2.85 m; balusters at 0.22 m | YT people/benches, Wi4t1 piers | LOW-MED |
| Benches | 1.60 × 0.42 m, seat 0.45 m | YT LjFT t06m58, 01YNk t13m21 | LOW |

## 3. Lettering
| Where | Text | Status |
|---|---|---|
| Oval wreath tablet on the end canopy and on the upper dome | line 1 "شركة", line 2 "قصر السلام", line 3 illegible | lines 1–2 read on LjFT t05m58 (best daylight close-up) and t05m54; line 3 left as a plain band |
| Attic panel under the end tablet (credit line) | "تصميم المعماري م/ …" | the architect's name is illegible (ends in something like "…نجيب"); only the legible words are cut |
| Plaque on the drum, track side | "كليوباترا" | clear in LjFT t06m58, t07m00, t07m12 |

The sponsor/contractor credit ("شركة قصر السلام", Qasr El Salam company) supports the dossier's reading of the
colonnade as a late-20th-century sponsored shelter rather than an original Alexandria & Ramleh Railway structure.

## 4. Error budget and what would fix it
- Absolute scale hangs on the column height (±15 %). One tape measurement of a surviving column, plinth or the
  platform height would fix all vertical values; the pitch and counts would then fix the plan.
- The pitch couples to the satellite length (±1 m per colonnade). Demolition started in September 2026: one
  colonnade was down by late September (YT U0pAlyOq3yQ, LjFTTQorR9o, Wi4t1OngdrE) while the other still stood in
  early October (9-zDQpju3g8). A tape on any surviving column, plinth or the rubble would still help.
- The dome profile is the least certain shape: side-on daylight silhouettes exist only from moving trams.
