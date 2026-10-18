#!/bin/zsh
# Regenerates the Arabic lettering SVGs (mm units, CoreText outlines) used by fusion/scripts/build_lettering.py.
# macOS only (CoreText + the system fonts Diwan Thuluth and DecoType Naskh).
# Usage: ./make_svgs.sh [path-to-compiled-text2svg]   (compiles text2svg.swift to $TMPDIR if omitted)
# Only the legible words are cut. The third cartouche line and the architect's name on the frieze are illegible
# in every available frame and are left blank (see references/notes/dimensions.md).
set -e
cd "$(dirname "$0")"
T=${1:-${TMPDIR:-/tmp}/text2svg}
[ -x $T ] || swiftc -O -o $T text2svg.swift
mkdir -p svg
$T svg/cart_l1.svg  "Diwan Thuluth"        60 0 "شركة"
$T svg/cart_l2.svg  "Diwan Thuluth"       100 0 "قصر السلام"
$T svg/credit.svg   "DecoType Naskh"       60 0 "تصميم المعماري م/"
$T svg/drum.svg     "Diwan Thuluth"       100 0 "كليوباترا"
