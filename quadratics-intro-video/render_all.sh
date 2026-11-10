#!/usr/bin/env bash
# Render every scene in display order at 1280x720, 30 fps.
set -e
cd "$(dirname "$0")"
PY=${PY:-$HOME/manim-venv/bin/python}
SCENES="S00Title S01FunctionNotation S02WhatIsQuadratic S03StandardForm S04ParentFunction S05VertexBehavior S06EffectOfA S07ConstantC S08QuickCheck S09ThrowTheBall S10DomainRangeMinMax S11DesmosTable S12WrapUp"
for s in ${1:-$SCENES}; do
  $PY -m manim -qm --fps 30 --disable_caching -v WARNING --progress_bar none scenes.py "$s"
done
