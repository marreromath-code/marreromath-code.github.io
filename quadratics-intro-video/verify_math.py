"""Independent checks for every number shown in the Quadratic Functions intro video."""
from fractions import Fraction as F
import math
ok = True
def check(label, got, want):
    global ok
    good = abs(float(got) - float(want)) < 1e-9 if not isinstance(want, (tuple, list)) else got == want
    ok &= good
    print(f"[{'OK' if good else 'FAIL'}] {label}: {got} (expected {want})")

# S01 function notation: f(x) = x^2
f = lambda x: x**2
check("f(3) for x^2", f(3), 9)
check("f(-3) for x^2", f(-3), 9)

# S02 example f(x) = x^2 + 5x + 10
g = lambda x: x**2 + 5*x + 10
check("g(0) = c", g(0), 10)

# S04 parent table
check("parent table", [f(x) for x in range(-3, 4)], [9, 4, 1, 0, 1, 4, 9])

# S07 f(x) = 3x^2 + 5x - 1
h = lambda x: 3*x**2 + 5*x - 1
check("h(0) y-intercept", h(0), -1)
xv = F(-5, 6)
check("h vertex x", xv, F(-5, 6))
check("h vertex y", 3*xv**2 + 5*xv - 1, F(-111, 36))
check("h(-2.6) in window", round(h(-2.6), 4), 6.28)
check("h(1.05) in window", round(h(1.05), 4), 7.5575)

# S08 quick check: k(x) = 5x - x^2 + 1 -> -x^2 + 5x + 1
k1 = lambda x: 5*x - x**2 + 1
k2 = lambda x: -x**2 + 5*x + 1
check("k rewritten equal (x=0..4)", [k1(x) for x in range(5)], [k2(x) for x in range(5)])

# S09 projectile h(t) = -16 t^2 + 40 t + 25
H = lambda t: -16*t**2 + 40*t + 25
V = lambda t: -32*t + 40
check("h(0) initial height", H(0), 25)
check("v(0) initial velocity", V(0), 40)
check("vertex time 40/32", F(40, 32), F(5, 4))
check("v(1.25) = 0", V(1.25), 0)
check("max height h(1.25)", H(1.25), 50)
tg = (40 + math.sqrt(40**2 + 4*16*25)) / 32
check("ground time", round(tg, 4), 3.0178)
check("h(ground time) ~ 0", round(H(tg), 9), 0)
check("a = -16 = (1/2)(-32)", F(1, 2)*-32, -16)

# S10 key features: y = x^2 (min 0), y = -x^2 + 4 (max 4)
p = lambda x: -x**2 + 4
check("-x^2+4 at 0", p(0), 4)
check("-x^2+4 zeros", [p(-2), p(2)], [0, 0])

# S11 Desmos table: f(x) = x^2 - 2x - 3
q = lambda x: x**2 - 2*x - 3
check("table rows", [q(x) for x in range(-1, 4)], [0, -3, -4, -3, 0])
check("vertex x = -b/2a", F(2, 2), 1)
check("min value", q(1), -4)
check("q(4)", q(4), 5)
check("q(-2)", q(-2), 5)

# S09 slider on b (initial velocity): h(t) = -16t^2 + b t + 25, max = b^2/64 + 25 at t = b/32
for b, tmax, hmax in ((24, 0.75, 34), (40, 1.25, 50), (56, 1.75, 74)):
    Hb = lambda t: -16*t**2 + b*t + 25
    check(f"b={b} vertex time b/32", b/32, tmax)
    check(f"b={b} max height", Hb(b/32), hmax)
    check(f"b={b} max via b^2/64+25", b*b/64 + 25, hmax)
tg56 = (56 + math.sqrt(56**2 + 4*16*25)) / 32
check("b=56 ground time < 4 (fits window)", tg56 < 4, True)
check("b=56 max 74 < 80 (fits window)", 74 < 80, True)

# Predict questions
check("predict f(-3) for x^2 is 9 (not -9)", (-3)**2, 9)

print("\nALL CHECKS PASS" if ok else "\nSOME CHECKS FAILED")
