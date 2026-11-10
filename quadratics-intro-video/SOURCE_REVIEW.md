# Source Review: Quadratic Functions, Unit Introduction

**Request:** a dynamic MP4 presentation in the Marrero Math design system that introduces
quadratic functions, using the teacher's written summary. Relaxing background music from
Epidemic Sound. Version 2: restyled with the Marrero Math website palette and
fonts, with lesson patterns inspired by Brilliant screens (Mobbin "Education" collection).

**Level (assumed):** Algebra 1 / Foundations of Algebra, unit introduction.

**What the summary asks students to understand**
1. Function notation: f(x) = y.
2. Structure: polynomial with a leading term of degree 2. Example f(x) = x² + 5x + 10.
3. Standard form f(x) = ax² + bx + c: leading term, leading coefficient, middle term
   (x = x¹), constant (positive or negative).
4. Parent function y = x² (Desmos), the parabola, two symmetric branches, decreasing,
   vertex as turning point, then increasing (read left to right).
5. Preview: a changes the graph; c is the y-intercept (example f(x) = 3x² + 5x − 1 → −1).
6. Physics: a ball thrown from a building. b = initial velocity, gravity bends the path,
   velocity is 0 at the vertex, then the ball falls to the ground.
7. Key features: domain, range, minimum, maximum, tables of values with Desmos.

**Notes on the summary**
- "dx²" in the summary was read as "ax²" (the leading term).
- The physics example uses the standard Algebra 1 model h(t) = −16t² + v₀t + h₀ (feet,
  seconds), with v₀ = 40 ft/s and h₀ = 25 ft (the 25-foot building from the summary).
  The graph shows height against time.

## Verification table (run `python3 verify_math.py`, all checks pass)

| Item on screen | Check |
|---|---|
| f(x) = x²: f(3) = 9, f(−3) = 9 | computed |
| Parent table x = −3..3 → 9, 4, 1, 0, 1, 4, 9 | computed |
| f(x) = 3x² + 5x − 1: f(0) = −1; vertex (−5/6, −37/12) stays inside graph window | computed |
| k(x) = 5x − x² + 1 = −x² + 5x + 1 → a = −1, b = 5, c = 1 | equal at x = 0..4 |
| h(t) = −16t² + 40t + 25: h(0) = 25, v(0) = 40 | computed |
| v(t) = 40 − 32t = 0 at t = 1.25; h(1.25) = 50 ft | computed |
| Ground: t = (40 + √3200)/32 ≈ 3.02 s; v ≈ −56.57 ft/s | computed |
| a = −16 = ½(−32 ft/s²) | computed |
| Slider b: max height b²/64 + 25 → b = 24: 34 ft, 40: 50 ft, 56: 74 ft (fits 0–80 ft, 0–4 s window) | computed |
| g(x) = −x² + 4: max 4 at (0, 4); range y ≤ 4 | computed |
| f(x) = x² − 2x − 3 table x = −1..3 → 0, −3, −4, −3, 0; min −4 at (1, −4) | computed |
