# Manim — Calculus Visuals

Animated math explainers in the [3Blue1Brown](https://www.3blue1brown.com/)
style, built with [Manim Community Edition](https://www.manim.community/).

## Scenes

| File | Scene class | Topic |
|------|-------------|-------|
| `limit_definition.py` | `LimitDefinition` | The definition of a limit (conceptual **and** ε–δ) |

### `LimitDefinition`

A single ~70-second animation that builds the idea of a limit from the ground
up, deliberately keeping each frame uncluttered:

1. **The puzzle** — `f(x) = (x²−1)/(x−1)` is *undefined* at `x = 1` (you get
   `0/0`). So instead of asking about `x = 1`, we look *near* it.
2. **The conceptual picture** — graph the curve with an open **hole** at
   `(1, 2)`. A point slides toward the hole from both sides while a live
   read-out shows `x → 1` and `f(x) → 2`. This is the intuitive "approach."
3. **The procedural heart** — the formal **ε–δ "challenge / response" game**:
   a green ε-band traps the *output* near `L`; a red δ-window controls the
   *input* near `c`. Shrinking ε shows a δ can always answer the challenge,
   alongside the statement
   `∀ε>0 ∃δ>0 : 0<|x−1|<δ ⇒ |f(x)−2|<ε`.
4. **The takeaway** — *A limit is a destination, not a stop along the way:*
   `lim_{x→c} f(x) = L`.

## Rendering

Requires **Python 3.9+**, **Manim Community v0.18+**, and a **LaTeX**
installation (for the math labels).

```bash
pip install manim                 # plus a TeX distribution, e.g. TeX Live / MiKTeX

# preview (720p), high quality (1080p), or 4K:
manim -pql manim/limit_definition.py LimitDefinition
manim -pqh manim/limit_definition.py LimitDefinition
manim -pqk manim/limit_definition.py LimitDefinition
```

The `-p` flag opens the video when the render finishes; output lands in
`media/videos/limit_definition/<quality>/LimitDefinition.mp4`.

## Style notes

- Pure black background (`#000000`).
- Palette: 3blue `#3FA9F5` curve, warm-yellow `#FFD86E` limit value,
  green `#7FE0A0` for the ε (output) tolerance, red `#FF8A8A` for the δ
  (input) tolerance.
- Color is used as *meaning*: input-side things are red, output-side things
  are green, the target is yellow — so the ε–δ relationship reads at a glance.
