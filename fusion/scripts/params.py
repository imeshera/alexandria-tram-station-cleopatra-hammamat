# User parameters for the Cleopatra Hammamat station (one per dimension; comment = source + confidence).
# Re-running updates the expressions of existing parameters, so this table is the single source of truth.
# Sources: OS = owner's iPhone photos (Mar 2026); YT = YouTube frames (2024-2026, see references/SOURCES.md);
# SAT = Esri imagery at 0.255 m/px; DOS = station dossier v0. Full method notes: references/notes/dimensions.md.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, common
importlib.reload(common)
import adsk.core

PARAMS = [
    # name, expression, comment
    # --- track and street
    ('gauge', '1435 mm', 'Track gauge, standard (Raml line). HIGH'),
    ('rail_h', '150 mm', 'Flat-bottom rail height (49E1-class 149 mm). MEDIUM'),
    ('rail_head_w', '67 mm', 'Rail head width (49E1-class). MEDIUM'),
    ('rail_foot_w', '125 mm', 'Rail foot width (49E1-class). MEDIUM'),
    ('sleeper_pitch', '650 mm', 'Sleeper spacing, ballasted/earth-filled track. LOW (YT frames)'),
    ('track_ctr', '3800 mm', 'Track centre spacing, centre-pole double track. LOW (YT 01YNk/hBRSK, SAT 14 +/- 2 m between colonnade axes)'),
    ('road_w', '10 m', 'Level crossing street (Medhat Seif El Yazal Khalifa St) carriageway width. LOW (SAT)'),
    ('ocs_h', '5600 mm', 'Contact wire height above rail (raised for the double-deckers). LOW (DD 224 repo)'),
    # --- platform
    ('plat_h', '500 mm', 'Platform top above rail head. MED-LOW (DOS rail-gauge ground plane 0.55 +/- 0.10; YT car skirts)'),
    ('plat_edge', '1400 mm', 'Track centre to platform edge (2.42 m car + gap). LOW-MED'),
    ('plat_w', '4200 mm', 'Platform width, edge to back face of balustrade. LOW (YT 6IYrh/3nKi, DOS 4-5 m)'),
    ('plat_x0', '6000 mm', 'Crossing centre to foot of the platform ramp. LOW (SAT, OS GPS 10 m from OSM crossing nodes)'),
    ('ramp_l', '3000 mm', 'Platform end ramp length. LOW (YT hBRSK t21m03)'),
    ('plat_len', '38 m', 'Platform length from the top of the ramp. LOW (SAT)'),
    ('coping_w', '300 mm', 'Platform edge coping width. LOW'),
    # --- colonnade layout
    ('n_can', '7', 'Canopies per colonnade (8 transverse frames). MEDIUM (YT 01YNk t13m22, OS IMG_9502, LjFT t06m56-t07m24)'),
    ('tall_idx', '4', 'Canopy number (from the crossing end) carrying the two-tier unit. MEDIUM (centre of 7)'),
    ('pitch', '2850 mm', 'Frame pitch along the track = canopy lip diameter (lips touch over each frame). LOW-MED (SAT 19-21 m / 7; pitch/col_h 1.18 in YT)'),
    ('x_f1', '17 m', 'Crossing centre to the first (crossing-end) frame. LOW (SAT gap 43 m between colonnade ends; OS camera 8.6 m from the SW end)'),
    ('col_front', '1700 mm', 'Platform edge to front (track-side) column centre. LOW (YT 3nKi t01m00, 6IYrh)'),
    ('col_w', '1300 mm', 'Transverse column spacing within a frame, centre to centre (~3.8 D). LOW-MED (YT 6IYrh t01m00, LjFT t05m54)'),
    # --- column (Scamozzi-type Ionic on a square plinth)
    ('col_h', '2400 mm', 'Column: plinth bottom to abacus top. LOW-MED (DOS 2.25-2.9; YT woman 1.6 m beside a column ~1.5x)'),
    ('col_d', '340 mm', 'Shaft lower diameter (H/D 7.1). MEDIUM ratio, LOW-MED absolute'),
    ('entasis', '0.84', 'Top/bottom shaft diameter ratio. LOW (Vignola 5/6)'),
    ('plinth_w', '580 mm', 'Square plinth width (1.7 D). LOW-MED (YT 3nKi t01m00, 6IYrh)'),
    ('plinth_h', '200 mm', 'Plinth height. LOW-MED'),
    ('base_h', '120 mm', 'Attic base height (torus-scotia-torus). LOW'),
    ('cap_h', '280 mm', 'Capital height incl. abacus (diagonal volutes). LOW-MED'),
    ('abacus_w', '480 mm', 'Abacus width (concave-sided). LOW-MED'),
    ('abacus_h', '50 mm', 'Abacus height. LOW'),
    # --- entablature (transverse beam per frame)
    ('ent_h', '380 mm', 'Entablature height: architrave + dentil frieze + cornice (0.16 col_h). LOW-MED (DOS)'),
    ('ent_d', '500 mm', 'Beam depth along the track. LOW-MED'),
    ('ent_over', '300 mm', 'Beam overhang beyond the column centres (each end). LOW'),
    # --- canopy (cast RC half-dome / bell)
    ('lip_d', 'pitch', 'Canopy lip outer diameter (lips touch above each frame). LOW-MED'),
    ('lip_h', '200 mm', 'Moulded lip band height (fillets + dentil band + ovolo). LOW-MED (YT LjFT t06m02)'),
    ('lip_t', '160 mm', 'Lip band radial width. LOW'),
    ('bowl_h', '550 mm', 'Convex bowl below the lip: beam top to lip bottom (0.23 col_h). LOW-MED (YT 01YNk t13m22 model overlay)'),
    ('bowl_d', '2440 mm', 'Bowl bottom rim diameter; the rim bears on the two neighbouring beams. LOW'),
    ('dish_d', '120 mm', 'Rise of the concave soffit dish under the bowl. LOW (OS night shots: lit dish with dark rim)'),
    ('dome_rise', '1250 mm', 'Lip top to crown top (0.44 lip). LOW (YT 01YNk t13m22 model overlay, hBRSK t21m06)'),
    ('crown_d', '1500 mm', 'Crown ring diameter (0.53 lip). LOW-MED (YT LjFT t06m58)'),
    ('crown_h', '300 mm', 'Crown ring height. LOW'),
    ('shell_t', '80 mm', 'RC shell thickness (documented; canopies are modelled solid). MED-LOW (YT Wi4t1 t03m36)'),
    ('finial_h', '420 mm', 'Crown finial spike. LOW'),
    # --- two-tier unit
    ('drum_h', '600 mm', 'Drum wall height above the lip (carries the plaque). LOW (YT LjFT t07m00)'),
    ('ucol_h', '1400 mm', 'Upper colonnette: plinth bottom to abacus top. LOW (0.55-0.6 col_h, YT 01YNk)'),
    ('ucol_d', '220 mm', 'Upper colonnette diameter. LOW'),
    ('ucol_w', '1300 mm', 'Upper colonnette square, centre to centre. LOW'),
    ('uent_h', '300 mm', 'Upper entablature height. LOW'),
    ('ulip_d', '2500 mm', 'Upper canopy lip diameter. LOW (YT LjFT t07m00 ~ drum width)'),
    ('udome_rise', '1150 mm', 'Upper canopy lip top to crown top. LOW (YT 01YNk t13m22)'),
    ('ufinial_h', '650 mm', 'Upper finial spike. LOW'),
    # --- balustrade and furniture
    ('bal_h', '950 mm', 'Balustrade height (top of rail). LOW-MED (YT people, benches)'),
    ('bal_pier_w', '360 mm', 'Balustrade pier width. LOW-MED (YT Wi4t1)'),
    ('bal_pier_pitch', '2850 mm', 'Pier spacing (one per frame bay). LOW'),
    ('baluster_pitch', '220 mm', 'Baluster spacing. LOW-MED'),
    ('bench_l', '1600 mm', 'Bench length. LOW'),
    ('bench_h', '450 mm', 'Bench seat height. MEDIUM (standard)'),
    ('bench_w', '420 mm', 'Bench seat depth. LOW'),
]


def run(_context: str):
    doc, design = common.activate()
    up = design.userParameters
    n_new = 0
    for name, expr, comment in PARAMS:
        p = up.itemByName(name)
        unit = '' if expr.replace('.', '').isdigit() else ('mm' if ('mm' in expr or ' m' in expr or name == 'lip_d') else '')
        if p is None:
            vi = adsk.core.ValueInput.createByString(expr)
            up.add(name, vi, 'mm' if unit else '', comment)
            n_new += 1
        else:
            if p.expression != expr:
                p.expression = expr
            p.comment = comment
    print('parameters:', up.count, 'new', n_new)
