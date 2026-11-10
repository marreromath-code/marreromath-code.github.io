"""Quadratic Functions - Unit Introduction.

Marrero Math light theme (cream / navy / gold, Fraunces + Inter) with
Brilliant-inspired lesson patterns: progress bar, pause-and-predict cards,
live sliders, algebra tiles, navy-header tables and Correct / Incorrect
feedback banners. Every number on screen is checked in verify_math.py.
"""

from marrero_brilliant_base import *


def bullet(s, color, size=22):
    d = Dot(radius=0.08, color=color)
    t = body(s, size)
    t.next_to(d, RIGHT, buff=0.22)
    return VGroup(d, t)


# ======================================================================
# S00 - Title + course path
# ======================================================================
class S00Title(LessonScene):
    def construct(self):
        mark = heading("Marrero Math", 20, GOLD).move_to([5.75, 3.58, 0])
        chip = pill("UNIT INTRODUCTION", GOLD_FILL, GOLD_TXT, size=16, h=0.42)
        title = heading("Quadratic Functions", 60)
        sub = body("Where mathematics meets physics", 26, MUTED)
        top = VGroup(chip, title, sub).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        top.to_corner(UL, buff=0.7).shift(DOWN * 0.15)
        self.play(FadeIn(mark), FadeIn(chip, shift=DOWN * 0.1), run_time=0.5)
        self.play(Write(title), run_time=1.1)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.5)

        items = ["Function notation", "Structure & standard form",
                 "The parent function", "Vertex, a and c",
                 "Physics: throwing a ball", "Domain, range, min & max"]
        nodes = VGroup()
        y0 = 0.55
        for i, s in enumerate(items):
            c = Circle(radius=0.22, fill_color=CARD, fill_opacity=1, stroke_color=EDGE, stroke_width=3)
            n = body(str(i + 1), 18, MUTED, bold=True).move_to(c)
            t = body(s, 23).next_to(c, RIGHT, buff=0.3)
            g = VGroup(c, n, t).move_to([-6.2, y0 - 0.62 * i, 0], aligned_edge=LEFT)
            nodes.add(g)
        path = Line(nodes[0][0].get_center(), nodes[-1][0].get_center(), stroke_color=EDGE, stroke_width=4)
        self.add(path)
        self.play(Create(path), LaggedStart(*[FadeIn(g, shift=RIGHT * 0.2) for g in nodes],
                                            lag_ratio=0.12), run_time=1.6)

        ax = lesson_axes([-3, 3, 1], [-1, 9, 1], 4.2, 3.6)
        ax.move_to([3.85, -0.62, 0])
        gc = self.graph_card(ax)
        curve = ax.plot(lambda x: x ** 2, x_range=[-2.9, 2.9], color=CORAL, stroke_width=6)
        self.play(FadeIn(gc, shift=UP * 0.2), Create(ax), run_time=0.8)
        self.play(Create(curve), run_time=1.3)
        tr = ValueTracker(-2.9)
        ball = always_redraw(lambda: Dot(ax.c2p(tr.get_value(), tr.get_value() ** 2),
                                         color=INK, radius=0.11))
        self.add(ball)
        # light up the path while the ball rolls
        self.play(tr.animate.set_value(2.9), run_time=2.6, rate_func=there_and_back_with_pause)
        self.play(LaggedStart(*[n[0].animate.set_fill(GREEN_FILL).set_stroke(GREEN) for n in nodes],
                              lag_ratio=0.12), run_time=1.2)
        start = pill("Start lesson", INK, WHITE, w=3.4, h=0.62, size=22).move_to([3.85, BOTTOM_Y, 0])
        self.play(FadeIn(start, shift=UP * 0.2), run_time=0.4)
        self.cont_btn = start
        self.finish(1.6)


# ======================================================================
# S01 - Function notation + predict f(-3)
# ======================================================================
class S01FunctionNotation(LessonScene):
    PART = 1

    def construct(self):
        self.lesson_header("Function Notation", "Before quadratics: what does f(x) mean?")
        eq = MathTex("f", "(", "x", ")", "=", "y", font_size=86)
        eq[0].set_color(PURPLE); eq[2].set_color(GREEN); eq[5].set_color(GOLD)
        eq.move_to(UP * 0.85)
        self.play(Write(eq), run_time=0.9)
        n1 = body("name of the function", 21, PURPLE).next_to(eq[0], LEFT, buff=0.7).shift(UP * 0.35)
        n2 = body("input", 21, GREEN).next_to(eq[2], DOWN, buff=0.5)
        n3 = body("output", 21, GOLD_TXT).next_to(eq[5], RIGHT, buff=0.6).shift(UP * 0.35)
        a1 = Arrow(n1.get_right(), eq[0].get_left(), buff=0.1, color=PURPLE, stroke_width=3)
        a2 = Arrow(n2.get_top(), eq[2].get_bottom(), buff=0.08, color=GREEN, stroke_width=3)
        a3 = Arrow(n3.get_left(), eq[5].get_right(), buff=0.1, color=GOLD, stroke_width=3)
        for n, a in ((n1, a1), (n2, a2), (n3, a3)):
            self.play(FadeIn(n, shift=UP * 0.1), GrowArrow(a), run_time=0.5)
        self.wait(0.5)
        part1 = VGroup(eq, n1, n2, n3, a1, a2, a3)
        self.play(part1.animate.scale(0.55).move_to(UP * 1.4), run_time=0.7)

        # function machine
        mc = card(3.6, 1.3, stroke=PURPLE, stroke_width=3)
        mc.move_to(DOWN * 0.45)
        mt = MathTex("f(x) = x^2", font_size=44).move_to(mc)
        a_in = Arrow(LEFT * 3.7 + DOWN * 0.45, mc.get_left(), buff=0.12, color=MUTED)
        a_out = Arrow(mc.get_right(), RIGHT * 3.7 + DOWN * 0.45, buff=0.12, color=MUTED)
        lin = body("input", 20, GREEN).move_to(LEFT * 4.6 + UP * 0.3)
        lout = body("output", 20, GOLD_TXT).move_to(RIGHT * 4.6 + UP * 0.3)
        self.play(FadeIn(mc), Write(mt), GrowArrow(a_in), GrowArrow(a_out), FadeIn(lin), FadeIn(lout),
                  run_time=0.9)
        x_m = MathTex("3", font_size=60, color=GREEN).move_to(LEFT * 4.6 + DOWN * 0.45)
        self.play(FadeIn(x_m, shift=RIGHT * 0.3), run_time=0.4)
        self.play(x_m.animate.move_to(mc.get_center()).scale(0.3).set_opacity(0),
                  mc[1].animate.set_stroke(GOLD), run_time=0.7)
        y_m = MathTex("9", font_size=60, color=GOLD).move_to(mc.get_center()).scale(0.3)
        self.play(y_m.animate.scale(1 / 0.3).move_to(RIGHT * 4.6 + DOWN * 0.45),
                  mc[1].animate.set_stroke(PURPLE), run_time=0.7)
        calc = MathTex("f(3) = 3^2 = 9", font_size=40).move_to(DOWN * 1.75)
        self.play(Write(calc), run_time=0.7)
        self.wait(1.2)
        self.remove(x_m)
        self.play(*[FadeOut(m) for m in (part1, mc, mt, a_in, a_out, lin, lout, y_m, calc)], run_time=0.5)

        # pause & predict
        q = MathTex(r"\text{If } f(x) = x^2\text{, what is } f(-3)\text{?}", font_size=40)
        opts = [MathTex("-9", font_size=48), MathTex("9", font_size=48), MathTex("-6", font_size=48)]
        self.predict(q, opts, correct=1, center=UP * 0.35)
        self.banner_correct("Correct!", "f(−3) = 9")
        self.wait(0.6)
        self.press(self.why_btn)
        self.why_card("Explanation", [
            MathTex(r"f(-3) = (-3)^2 = (-3)(-3) = 9", font_size=38),
            body("A negative times a negative is positive.", 22),
            body("f(x) does not mean f times x. It is the output y for the input x.", 22, PURPLE),
        ])
        self.finish(2.6)


# ======================================================================
# S02 - What makes a function quadratic? (algebra tiles)
# ======================================================================
class S02WhatIsQuadratic(LessonScene):
    PART = 2

    def construct(self):
        self.lesson_header("What Makes a Function Quadratic?")
        eq = MathTex("f(x)", "=", "x^2", "+", "5x", "+", "10", font_size=66)
        eq[2].set_color(BLUE); eq[4].set_color(NAVY_SOFT); eq[6].set_color(GOLD_TXT)
        eq.move_to(UP * 1.65)
        self.play(Write(eq), run_time=1.0)

        big = self.tile_x2()
        xs = VGroup(*[self.tile_x() for _ in range(5)]).arrange(RIGHT, buff=0.08)
        units = VGroup(*[self.tile_1() for _ in range(10)]).arrange_in_grid(rows=2, cols=5, buff=0.07)
        p1 = MathTex("+", font_size=48, color=MUTED)
        p2 = MathTex("+", font_size=48, color=MUTED)
        row = VGroup(big, p1, xs, p2, units).arrange(RIGHT, buff=0.55).move_to(DOWN * 0.15)
        l1 = MathTex("x^2", font_size=34, color=BLUE).next_to(big, DOWN, buff=0.25)
        l2 = MathTex("5x", font_size=34, color=NAVY_SOFT).next_to(xs, DOWN, buff=0.25)
        l3 = MathTex("10", font_size=34, color=GOLD_TXT).next_to(units, DOWN, buff=0.25)
        l2.match_y(l1); l3.match_y(l1)

        self.play(Indicate(eq[2], color=BLUE), GrowFromCenter(big), FadeIn(l1), run_time=0.8)
        self.play(FadeIn(p1), Indicate(eq[4], color=NAVY_SOFT),
                  LaggedStart(*[GrowFromEdge(t, DOWN) for t in xs], lag_ratio=0.15), FadeIn(l2), run_time=1.0)
        self.play(FadeIn(p2), Indicate(eq[6], color=GOLD),
                  LaggedStart(*[GrowFromCenter(t) for t in units], lag_ratio=0.07), FadeIn(l3), run_time=1.0)
        poly = self.note("Several terms added together: a polynomial.", MUTED, 22, y=-1.95)
        self.play(FadeIn(poly, shift=UP * 0.1), run_time=0.5)
        self.wait(1.0)

        # the square tile
        others = VGroup(p1, xs, p2, units, l2, l3)
        self.play(others.animate.set_opacity(0.25), run_time=0.5)
        bt = Brace(big, UP, color=BLUE, buff=0.08)
        bl = Brace(big, LEFT, color=BLUE, buff=0.08)
        tx = MathTex("x", font_size=30, color=BLUE).next_to(bt, UP, buff=0.08)
        lx = MathTex("x", font_size=30, color=BLUE).next_to(bl, LEFT, buff=0.08)
        self.play(GrowFromCenter(bt), GrowFromCenter(bl), FadeIn(tx), FadeIn(lx),
                  big.animate.set_stroke(GOLD, width=5, family=False), run_time=0.8)
        sq = body("Quadratus means square: the x² tile is a square, x · x = x².", 22, BLUE)
        fit(sq, 12.4)
        sq.move_to(poly)
        self.play(ReplacementTransform(poly, sq), run_time=0.6)
        self.wait(1.2)
        deg = self.note("Highest exponent 2  →  degree 2  →  quadratic", GOLD_TXT, 24, y=-2.55)
        self.play(FadeIn(deg, shift=UP * 0.1), others.animate.set_opacity(1), run_time=0.6)
        self.finish(2.0)


# ======================================================================
# S03 - Standard form anatomy
# ======================================================================
class S03StandardForm(LessonScene):
    PART = 3

    def construct(self):
        self.lesson_header("Standard Form of a Quadratic Function")
        eq = MathTex("f(x)", "=", "a", "x^2", "+", "b", "x", "+", "c", font_size=84)
        eq.move_to(UP * 0.95)
        self.play(Write(eq), run_time=1.1)

        br1 = Brace(VGroup(eq[2], eq[3]), DOWN, color=GOLD)
        t1 = body("leading term", 22, GOLD_TXT).next_to(br1, DOWN, buff=0.12)
        self.play(eq[2:4].animate.set_color(GOLD), GrowFromCenter(br1), FadeIn(t1), run_time=0.7)
        lc = body("leading coefficient  (a ≠ 0)", 21, GOLD_TXT).next_to(eq[2], UP, buff=0.75).shift(LEFT * 1.1)
        lca = Arrow(lc.get_bottom() + RIGHT * 1.0, eq[2].get_top(), buff=0.08, color=GOLD, stroke_width=3)
        self.play(FadeIn(lc), GrowArrow(lca), run_time=0.6)
        br2 = Brace(VGroup(eq[5], eq[6]), DOWN, color=GREEN)
        t2 = body("middle term", 22, GREEN_DARK).next_to(br2, DOWN, buff=0.12)
        self.play(eq[5:7].animate.set_color(GREEN), GrowFromCenter(br2), FadeIn(t2), run_time=0.7)
        br3 = Brace(eq[8], DOWN, color=CORAL)
        t3 = body("constant", 22, CORAL).next_to(br3, DOWN, buff=0.12).shift(RIGHT * 0.45 + DOWN * 0.42)
        self.play(eq[8].animate.set_color(CORAL), GrowFromCenter(br3), FadeIn(t3), run_time=0.7)

        n1 = VGroup(MathTex("x = x^1", font_size=38, color=GREEN_DARK),
                    body("the exponent 1 is never written", 21)).arrange(RIGHT, buff=0.3)
        n2 = VGroup(Dot(radius=0.08, color=CORAL), body("c is just a number: positive or negative", 21)
                    ).arrange(RIGHT, buff=0.25)
        notes = VGroup(n1, n2).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(DOWN * 1.95)
        self.play(FadeIn(n1, shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(n2, shift=UP * 0.1), run_time=0.5)
        self.wait(1.4)

        self.play(FadeOut(notes), FadeOut(VGroup(br1, br2, br3, t1, t2, t3, lc, lca)),
                  eq.animate.scale(0.6).move_to(UP * 1.75), run_time=0.7)
        ex = MathTex("f(x)", "=", "3", "x^2", "+", "5", "x", "-", "1", font_size=64)
        ex[2].set_color(GOLD); ex[5].set_color(GREEN); ex[7:9].set_color(CORAL)
        ex.move_to(UP * 0.35)
        self.play(TransformFromCopy(eq, ex), run_time=1.0)
        chips = VGroup()
        for s, col in (("a = 3", GOLD), ("b = 5", GREEN), ("c = -1", CORAL)):
            m = MathTex(s, font_size=44, color=INK)
            c = card(2.4, 0.95, stroke=col, stroke_width=3)
            m.move_to(c)
            chips.add(VGroup(c, m))
        chips.arrange(RIGHT, buff=0.5).move_to(DOWN * 1.15)
        for c, s in zip(chips, [ex[2], ex[5], ex[7:9]]):
            self.play(Indicate(s, color=c[0][1].get_stroke_color()), FadeIn(c, shift=UP * 0.2), run_time=0.55)
        tk = self.note("Keep the sign with the number:  − 1  means  c = −1.", MUTED, 22, y=-2.45)
        self.play(FadeIn(tk), run_time=0.4)
        self.finish(1.8)


# ======================================================================
# S04 - Parent function: table -> points -> parabola
# ======================================================================
class S04ParentFunction(LessonScene):
    PART = 4

    def construct(self):
        self.lesson_header("The Parent Function and the Parabola")
        frame, hm, cell = self.table_frame(["x", "f(x)"], 7, (-6.2, 2.05), colw=1.35, rowh=0.5, size=30)
        self.play(FadeIn(frame, shift=UP * 0.1), FadeIn(hm), run_time=0.6)

        ax = lesson_axes([-4, 4, 1], [-1, 10, 1], 6.4, 4.4)
        ax.move_to([2.75, -0.2, 0])
        gc = self.graph_card(ax)
        nums = axis_numbers(ax, xs=(-3, -2, -1, 1, 2, 3), ys=(1, 4, 9))
        lab = MathTex("f(x) = x^2", font_size=34, color=GOLD_TXT).move_to(ax.c2p(2.75, 2.0))
        self.play(FadeIn(gc), Create(ax), FadeIn(nums), Write(lab), run_time=0.9)

        for i, x in enumerate(range(-3, 4)):
            rx = MathTex(str(x), font_size=30).move_to(cell(i, 0))
            ry = MathTex(str(x * x), font_size=30, color=GOLD_TXT).move_to(cell(i, 1))
            d = Dot(ax.c2p(x, x * x), color=GOLD, radius=0.1)
            self.play(FadeIn(rx, shift=RIGHT * 0.1), run_time=0.2)
            self.play(FadeIn(ry, shift=RIGHT * 0.1), TransformFromCopy(ry, d), run_time=0.4)
        curve = ax.plot(lambda x: x ** 2, x_range=[-3.15, 3.15], color=CORAL, stroke_width=6)
        self.play(Create(curve), run_time=1.5)
        name = body("parabola", 26, CORAL, bold=True).move_to(ax.c2p(1.55, 9.3))
        self.play(FadeIn(name, shift=LEFT * 0.2), run_time=0.4)
        dz = VGroup(body("Try it in Desmos:", 20, MUTED), MathTex("y = x^2", font_size=32)).arrange(RIGHT, buff=0.18)
        dz.move_to([-4.85, -2.45, 0])
        self.play(FadeIn(dz, shift=UP * 0.1), run_time=0.4)
        self.finish(2.0)


# ======================================================================
# S05 - Predict the behavior, then watch: decreasing, vertex, increasing
# ======================================================================
class S05VertexBehavior(LessonScene):
    PART = 5

    def construct(self):
        self.lesson_header("Reading the Parabola from Left to Right")
        q = MathTex(r"\text{Moving left to right along } y = x^2\text{, the graph...}", font_size=38)
        opts = [body("always goes up", 22), body("goes down, then up", 22), body("always goes down", 22)]
        p = self.predict(q, opts, correct=1, center=UP * 0.3)
        self.banner_correct("Correct!", "It turns around at the vertex.")
        self.wait(1.0)
        self.press(self.cont_btn)
        self.play(FadeOut(p["all"]), FadeOut(self.banner), run_time=0.4)
        self.cont_btn = None

        ax = lesson_axes([-4, 4, 1], [-1, 10, 1], 6.0, 4.5)
        ax.move_to([-2.9, -0.2, 0])
        gc = self.graph_card(ax)
        curve = ax.plot(lambda x: x ** 2, x_range=[-3.0, 3.0], color=EDGE, stroke_width=5)
        self.play(FadeIn(gc), Create(ax), Create(curve), run_time=0.9)
        tr = ValueTracker(-3.0)
        dot = always_redraw(lambda: Dot(ax.c2p(tr.get_value(), tr.get_value() ** 2), color=INK, radius=0.12))
        lb = ax.plot(lambda x: x ** 2, x_range=[-3.0, 0], color=CORAL, stroke_width=7)
        rb = ax.plot(lambda x: x ** 2, x_range=[0, 3.0], color=GREEN, stroke_width=7)
        self.add(dot)
        rows = VGroup(bullet("Decreasing: the graph goes down", CORAL),
                      bullet("Vertex (0, 0): the turning point", GOLD),
                      bullet("Increasing: the graph goes up", GREEN),
                      bullet("Axis of symmetry: x = 0", PURPLE)).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        rows.move_to([3.55, 0.75, 0])
        self.play(Create(lb), tr.animate.set_value(0), FadeIn(rows[0], shift=LEFT * 0.2), run_time=2.0, rate_func=linear)
        ring = Circle(radius=0.28, color=GOLD, stroke_width=5).move_to(ax.c2p(0, 0))
        self.play(Create(ring), Flash(ax.c2p(0, 0), color=GOLD), FadeIn(rows[1], shift=LEFT * 0.2), run_time=0.8)
        self.wait(0.4)
        self.play(Create(rb), tr.animate.set_value(3.0), FadeIn(rows[2], shift=LEFT * 0.2), run_time=2.0, rate_func=linear)
        axis = DashedLine(ax.c2p(0, -0.8), ax.c2p(0, 9.8), color=PURPLE, stroke_width=4)
        self.play(Create(axis), FadeIn(rows[3], shift=LEFT * 0.2), run_time=0.8)
        for x in (2, 1, 3):
            p1, p2 = ax.c2p(-x, x * x), ax.c2p(x, x * x)
            self.play(Create(DashedLine(p1, p2, color=PURPLE, stroke_width=2.5)),
                      FadeIn(Dot(p1, color=PURPLE)), FadeIn(Dot(p2, color=PURPLE)), run_time=0.4)
        pair = MathTex("f(-2) = f(2) = 4", font_size=36, color=PURPLE).next_to(rows, DOWN, buff=0.55)
        self.play(Write(pair), run_time=0.6)
        tk = fit(body("Two symmetrical branches meet at the vertex.", 21, MUTED), 6.0).move_to([3.55, -2.15, 0])
        self.play(FadeIn(tk), run_time=0.4)
        self.finish(1.8)


# ======================================================================
# S06 - Effect of a with a live slider
# ======================================================================
class S06EffectOfA(LessonScene):
    PART = 6

    def construct(self):
        self.lesson_header("Preview: How a Shapes the Parabola")
        q = MathTex(r"\text{In } f(x) = ax^2\text{, what happens when } a \text{ becomes negative?}", font_size=36)
        opts = [body("opens downward", 22), body("gets wider", 22), body("moves to the right", 22)]
        p = self.predict(q, opts, correct=0, center=UP * 0.3)
        self.banner_correct("Correct!", "Let's test it with the slider.")
        self.wait(0.8)
        self.press(self.cont_btn)
        self.play(FadeOut(p["all"]), FadeOut(self.banner), run_time=0.4)
        self.cont_btn = None

        ax = lesson_axes([-4, 4, 1], [-8, 8, 2], 5.8, 4.6)
        ax.move_to([-3.1, -0.2, 0])
        gc = self.graph_card(ax)
        self.play(FadeIn(gc), Create(ax), run_time=0.7)
        a = ValueTracker(1.0)

        def graph():
            av = a.get_value()
            lim = min(3.6, (7.6 / abs(av)) ** 0.5) if abs(av) > 1e-3 else 3.6
            col = GREEN if av > 0.02 else (RED if av < -0.02 else MUTED)
            return ax.plot(lambda x: av * x * x, x_range=[-lim, lim], color=col, stroke_width=6)
        ghost = ax.plot(lambda x: x * x, x_range=[-2.75, 2.75], color=EDGE, stroke_width=3)
        self.add(ghost)
        g = always_redraw(graph)
        self.play(Create(g), run_time=0.8)

        lab = MathTex("f(x) =", font_size=46)
        num = DecimalNumber(1.0, num_decimal_places=1, font_size=46, color=GOLD_TXT)
        xx = MathTex("x^2", font_size=46)
        ro = VGroup(lab, num, xx).arrange(RIGHT, buff=0.15).move_to([3.3, 1.75, 0])
        num.add_updater(lambda m: m.set_value(a.get_value()))
        xx.add_updater(lambda m: m.next_to(num, RIGHT, buff=0.15))
        sl = self.slider(a, -3, 3, [3.3, 0.45, 0], width=4.6, color=GOLD, label="a")
        self.play(FadeIn(ro), FadeIn(sl), run_time=0.6)

        rules = VGroup(bullet("a > 0: opens up (minimum)", GREEN, 21),
                       bullet("a < 0: opens down (maximum)", RED, 21),
                       bullet("|a| > 1: narrower      |a| < 1: wider", INK, 21)).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        rules.move_to([3.3, -1.35, 0])
        self.play(FadeIn(rules[0], shift=LEFT * 0.2), run_time=0.4)
        self.play(a.animate.set_value(3.0), run_time=1.5)
        self.play(a.animate.set_value(0.5), FadeIn(rules[2], shift=LEFT * 0.2), run_time=1.7)
        self.wait(0.4)
        self.play(a.animate.set_value(-1.0), FadeIn(rules[1], shift=LEFT * 0.2), run_time=2.0)
        self.play(a.animate.set_value(-2.0), run_time=1.1)
        self.wait(0.4)
        self.play(a.animate.set_value(1.0), run_time=1.6)
        tk = fit(body("a = 0 erases the x² term: then it is not quadratic.", 20, CORAL), 6.2).move_to([3.3, -2.5, 0])
        self.play(FadeIn(tk), run_time=0.4)
        self.finish(1.6)


# ======================================================================
# S07 - c is the y-intercept, with a c slider
# ======================================================================
class S07ConstantC(LessonScene):
    PART = 7

    def construct(self):
        self.lesson_header("The Constant c Is the y-Intercept")
        ax = lesson_axes([-3, 2, 1], [-5, 7, 1], 4.6, 4.6)
        ax.move_to([-3.85, -0.2, 0])
        gc = self.graph_card(ax)
        nums = axis_numbers(ax, xs=(-2, 1), ys=(-4, -2, 2, 4, 6))
        self.play(FadeIn(gc), Create(ax), FadeIn(nums), run_time=0.8)
        eq = MathTex("f(x)", "=", "3x^2", "+", "5x", "-", "1", font_size=50).move_to([2.9, 1.95, 0])
        self.play(Write(eq), run_time=0.8)
        c = ValueTracker(-1.0)
        g = always_redraw(lambda: ax.plot(lambda x: 3 * x * x + 5 * x + c.get_value(),
                                          x_range=[-2.3, 0.7], color=CORAL, stroke_width=6))
        self.play(Create(g), run_time=1.0)

        lines = ["f(0) = 3(0)^2 + 5(0) - 1", "f(0) = 0 + 0 - 1", "f(0) = -1"]
        mobs = []
        for i, s in enumerate(lines):
            m = MathTex(s, font_size=38)
            m.move_to([0, 1.05 - 0.72 * i, 0])
            m.shift(RIGHT * (0.9 - m.get_left()[0]))
            mobs.append(m)
            self.play(Write(m), run_time=0.6)
        box = SurroundingRectangle(mobs[-1], color=GOLD, buff=0.15, corner_radius=0.1, stroke_width=3)
        self.play(Create(box), eq[5:7].animate.set_color(GOLD_TXT), run_time=0.6)
        yd = always_redraw(lambda: Dot(ax.c2p(0, c.get_value()), color=GOLD, radius=0.12))
        pt = MathTex("(0, -1)", font_size=30, color=GOLD_TXT).next_to(ax.c2p(0, -1), RIGHT, buff=0.25)
        self.play(FadeIn(yd, scale=2), Flash(ax.c2p(0, -1), color=GOLD), Write(pt), run_time=0.7)
        cross = body("where the graph crosses the y-axis", 21, GOLD_TXT).move_to([3.0, -0.95, 0])
        self.play(FadeIn(cross, shift=UP * 0.1), run_time=0.4)
        self.wait(0.8)

        sl = self.slider(c, -3, 3, [3.0, -2.05, 0], width=4.2, color=GOLD, label="c")
        self.play(FadeOut(pt), FadeIn(sl), run_time=0.4)
        self.play(c.animate.set_value(2.0), run_time=1.6)
        self.play(c.animate.set_value(-1.0), run_time=1.6)
        tk = fit(body("Change c and the whole parabola slides up or down.", 20, MUTED), 6.0).move_to([3.0, -2.8, 0])
        self.play(FadeIn(tk), run_time=0.4)
        self.finish(1.6)


# ======================================================================
# S08 - Quick check with Incorrect / See answer / Correct
# ======================================================================
class S08QuickCheck(LessonScene):
    PART = 8

    def construct(self):
        self.lesson_header("Quick Check: Is It Quadratic?")
        items = [("f(x) = 2x^2 - 7", "Quadratic: degree 2  (b = 0)", True),
                 ("g(x) = 4x + 9", "Linear: degree 1", False),
                 ("h(x) = x^3 + x^2", "Cubic: degree 3", False),
                 ("k(x) = 5x - x^2 + 1", "Quadratic: degree 2", True)]
        cards = VGroup()
        for tex, _, _ in items:
            c = card(5.4, 1.35)
            m = MathTex(tex, font_size=42).move_to(c).shift(UP * 0.2)
            cards.add(VGroup(c, m))
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.5, 0.35)).move_to(UP * 0.45)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.15), run_time=1.2)
        self.wait(1.0)
        for cd, (_, verdict, ok) in zip(cards, items):
            col = GREEN if ok else CORAL
            ic = (check_icon(GREEN, 0.15) if ok else x_icon(CORAL, 0.15))
            v = body(verdict, 20, GREEN_DARK if ok else CORAL)
            row = VGroup(ic, v).arrange(RIGHT, buff=0.15).next_to(cd[1], DOWN, buff=0.2)
            self.play(cd[0][1].animate.set_stroke(col, width=3.5), FadeIn(row, shift=UP * 0.1), run_time=0.5)
            cd.add(row)
            self.wait(0.35)
        self.wait(0.8)

        focus = cards[3]
        self.play(FadeOut(VGroup(*cards[:3])), focus.animate.move_to(UP * 1.55), run_time=0.7)
        claim = MathTex(r"\text{Claim: the leading coefficient is } a = 5", font_size=40).move_to(UP * 0.1)
        why = body("“5 is in the first term”", 21, MUTED).next_to(claim, DOWN, buff=0.15)
        self.play(Write(claim), FadeIn(why), run_time=0.8)
        self.banner_incorrect("Incorrect.")
        self.wait(1.0)
        self.press(self.see_btn)
        self.play(FadeOut(self.banner), FadeOut(why), run_time=0.3)

        src = MathTex("k(x)", "=", "5x", "-", "x^2", "+", "1", font_size=52).move_to(DOWN * 1.05)
        lead = body("Write it in standard form first (highest power first):", 21).next_to(src, UP, buff=0.2)
        self.play(FadeIn(lead), FadeIn(src), claim.animate.set_opacity(0.35), run_time=0.6)
        dst = MathTex("k(x)", "=", "-", "x^2", "+", "5x", "+", "1", font_size=52).move_to(src)
        self.play(TransformMatchingTex(src, dst), run_time=1.3)
        self.play(dst[2:4].animate.set_color(GOLD), run_time=0.4)
        ans = MathTex("a = -1,\\; b = 5,\\; c = 1", font_size=42).move_to(DOWN * 2.15)
        bx = SurroundingRectangle(ans, color=GOLD, buff=0.16, corner_radius=0.1, stroke_width=3)
        self.play(Write(ans), Create(bx), run_time=0.8)
        self.banner_correct("Got it!", "Rewrite in standard form before naming a, b, c.")
        self.finish(2.0)


# ======================================================================
# S09 - Physics: throw a ball from a 25 ft building
# ======================================================================
class S09ThrowTheBall(LessonScene):
    PART = 9

    def construct(self):
        self.lesson_header("Where Does the Parabola Come From? Motion!")
        ax = Axes(x_range=[-1, 4, 0.5], y_range=[0, 80, 10], x_length=6.0, y_length=4.5, tips=False,
                  axis_config=dict(color=NAVY_SOFT, stroke_width=2.2, tick_size=0.06),
                  x_axis_config=dict(include_ticks=False))
        ax.move_to([-2.75, -0.25, 0])
        gc = self.graph_card(ax)
        ticks = VGroup(*[Line(ax.c2p(v, 0) + UP * 0.06, ax.c2p(v, 0) + DOWN * 0.06, color=NAVY_SOFT, stroke_width=2.2)
                         for v in (1, 2, 3, 4)])
        nums = axis_numbers(ax, xs=(1, 2, 3, 4), ys=(20, 40, 60, 80))
        tl = body("time t (s)", 16, MUTED).next_to(ax.c2p(4, 0), DOWN, buff=0.4).shift(LEFT * 0.5)
        hl = body("height h (ft)", 16, MUTED).next_to(ax.c2p(0, 80), RIGHT, buff=0.15)
        b_bot, b_top = ax.c2p(-0.95, 0), ax.c2p(-0.42, 25)
        bld = Rectangle(width=b_top[0] - b_bot[0], height=b_top[1] - b_bot[1], fill_color=NAVY_SOFT,
                        fill_opacity=1, stroke_width=0).move_to((b_bot + b_top) / 2)
        wins = VGroup(*[Square(0.11, fill_color=TILE_1, fill_opacity=0.9, stroke_width=0)
                        .move_to(bld.get_center() + RIGHT * dx + UP * dy)
                        for dx in (-0.1, 0.1) for dy in (-0.38, -0.1, 0.18, 0.46)])
        self.play(FadeIn(gc), Create(ax), FadeIn(ticks), FadeIn(nums), FadeIn(tl), FadeIn(hl),
                  FadeIn(bld, shift=UP * 0.2), FadeIn(wins), run_time=1.0)

        eq = MathTex("h(t)", "=", "-16", "t^2", "+", "40", "t", "+", "25", font_size=46).move_to([3.85, 1.95, 0])
        self.play(Write(eq), run_time=0.9)
        info = [(eq[2], "a = −16: gravity pulls down", RED),
                (eq[5], "b = 40: initial velocity (ft/s)", GREEN),
                (eq[8], "c = 25: initial height (ft)", CORAL)]
        rows = VGroup(*[bullet(s, col, 21) for _, s, col in info]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rows.move_to([3.85, 0.75, 0])
        for (part, _, col), r in zip(info, rows):
            self.play(part.animate.set_color(col), FadeIn(r, shift=LEFT * 0.2), run_time=0.5)
            self.wait(0.3)
        self.wait(0.8)
        self.play(FadeOut(rows), run_time=0.3)

        q = body("At the very top, the ball's velocity is...", 21)
        opts = [MathTex(r"40 \text{ ft/s}", font_size=34), MathTex(r"0 \text{ ft/s}", font_size=34),
                MathTex(r"-32 \text{ ft/s}", font_size=34)]
        p = self.predict(q, opts, correct=1, center=[3.85, -0.5, 0], layout="col", card_w=3.4, card_h=0.62)
        self.banner_correct("Correct!", "Velocity is 0 at the vertex.")
        self.wait(0.8)
        self.press(self.cont_btn)
        self.play(FadeOut(p["all"]), FadeOut(self.banner), run_time=0.4)
        self.cont_btn = None

        T = ValueTracker(0.0)
        H = lambda t: -16 * t * t + 40 * t + 25
        V = lambda t: 40 - 32 * t
        ball = always_redraw(lambda: Dot(ax.c2p(T.get_value(), H(T.get_value())), color=GOLD, radius=0.13,
                                         stroke_color=INK, stroke_width=2))
        path = TracedPath(ball.get_center, stroke_color=CORAL, stroke_width=6)
        varrow = always_redraw(lambda: Arrow(
            ax.c2p(T.get_value(), H(T.get_value())),
            ax.c2p(T.get_value(), H(T.get_value())) + UP * V(T.get_value()) * 0.02,
            buff=0, color=GREEN if V(T.get_value()) >= 0 else RED, stroke_width=5,
            max_tip_length_to_length_ratio=0.35) if abs(V(T.get_value())) > 1.5 else VGroup())

        def readline(name, fn, unit, col):
            n = MathTex(name, font_size=34, color=MUTED)
            d = DecimalNumber(fn(0), num_decimal_places=2, font_size=34, color=col)
            u = MathTex(unit, font_size=30, color=MUTED)
            g = VGroup(n, d, u).arrange(RIGHT, buff=0.15)
            d.add_updater(lambda m: m.set_value(fn(T.get_value())))
            u.add_updater(lambda m: m.next_to(d, RIGHT, buff=0.15))
            return g, d, u
        r_t, d_t, u_t = readline("t =", lambda t: t, r"\text{s}", INK)
        r_h, d_h, u_h = readline("h =", H, r"\text{ft}", CORAL)
        r_v, d_v, u_v = readline("v =", V, r"\text{ft/s}", GREEN_DARK)
        panel = VGroup(r_t, r_h, r_v).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.85, 0.25, 0])
        pc = card(3.9, panel.height + 0.6).move_to(panel)
        self.play(FadeIn(pc), FadeIn(panel), FadeIn(ball, scale=2), run_time=0.6)
        self.add(path, varrow)

        def cap(s, col):
            return fit(body(s, 21, col), 5.4).move_to([3.85, -1.45, 0])
        phase = cap("Rising: velocity shrinks", GREEN_DARK)
        self.play(FadeIn(phase), run_time=0.3)
        self.play(T.animate.set_value(1.25), run_time=3.0, rate_func=linear)
        vtx = ax.c2p(1.25, 50)
        vring = Circle(radius=0.24, color=GOLD, stroke_width=4).move_to(vtx)
        vt = MathTex("(1.25,\\ 50)", font_size=28, color=GOLD_TXT).next_to(vtx, UP, buff=0.3)
        self.play(Create(vring), Write(vt), Transform(phase, cap("v = 0 at the vertex: max height 50 ft", GOLD_TXT)),
                  Flash(vtx, color=GOLD), run_time=0.8)
        self.wait(1.4)
        self.play(Transform(phase, cap("Falling: gravity speeds it up", RED)), run_time=0.3)
        tg = (40 + (40 ** 2 + 4 * 16 * 25) ** 0.5) / 32
        self.play(T.animate.set_value(tg), run_time=3.2, rate_func=linear)
        for m in (d_t, d_h, d_v, u_t, u_h, u_v, varrow, ball):
            m.clear_updaters()
        self.remove(varrow)
        self.play(Flash(ax.c2p(tg, 0), color=CORAL), Transform(phase, cap("Lands after about 3.02 seconds", INK)),
                  run_time=0.7)
        self.wait(1.2)

        # slider on b: throw harder or softer
        path.clear_updaters()
        self.play(FadeOut(VGroup(pc, panel, ball, vring, vt, phase)), path.animate.set_stroke(opacity=0.25),
                  run_time=0.5)
        eq2 = MathTex("h(t)", "=", "-16", "t^2", "+", "b", "t", "+", "25", font_size=46).move_to(eq)
        eq2[2].set_color(RED); eq2[5].set_color(GREEN); eq2[8].set_color(CORAL)
        self.play(TransformMatchingTex(eq, eq2), run_time=0.8)
        b = ValueTracker(40.0)

        def tland():
            bv = b.get_value()
            return (bv + (bv * bv + 1600) ** 0.5) / 32
        curve = always_redraw(lambda: ax.plot(lambda t: -16 * t * t + b.get_value() * t + 25,
                                              x_range=[0, tland()], color=CORAL, stroke_width=6))
        vdot = always_redraw(lambda: Dot(ax.c2p(b.get_value() / 32, b.get_value() ** 2 / 64 + 25),
                                         color=GOLD, radius=0.12, stroke_color=INK, stroke_width=2))
        mh_l = body("max height", 21, MUTED)
        mh_n = DecimalNumber(50, num_decimal_places=0, font_size=40, color=GOLD_TXT)
        mh_u = MathTex(r"\text{ft}", font_size=32, color=MUTED)
        mh = VGroup(mh_l, mh_n, mh_u).arrange(RIGHT, buff=0.18).move_to([3.85, 0.85, 0])
        mh_n.add_updater(lambda m: m.set_value(b.get_value() ** 2 / 64 + 25))
        mh_u.add_updater(lambda m: m.next_to(mh_n, RIGHT, buff=0.15))
        sl = self.slider(b, 20, 60, [3.85, -0.45, 0], width=4.2, color=GREEN, label="b", decimals=0)
        self.play(FadeIn(curve), FadeIn(vdot), FadeIn(mh), FadeIn(sl), run_time=0.6)
        capb = fit(body("Throw faster  →  higher vertex", 21, GREEN_DARK), 5.4).move_to([3.85, -1.75, 0])
        self.play(FadeIn(capb), run_time=0.3)
        self.play(b.animate.set_value(56), run_time=1.8)
        self.wait(0.5)
        self.play(b.animate.set_value(24), run_time=2.2)
        self.wait(0.5)
        self.play(b.animate.set_value(40), run_time=1.4)
        tk = self.note("b = 24: 34 ft     b = 40: 50 ft     b = 56: 74 ft", MUTED, 21, y=-2.6)
        tk.move_to([3.85, -2.4, 0])
        fit(tk, 5.6)
        self.play(FadeIn(tk), run_time=0.4)
        self.finish(1.8)


# ======================================================================
# S10 - Domain, range, minimum, maximum
# ======================================================================
class S10DomainRangeMinMax(LessonScene):
    PART = 10

    def construct(self):
        self.lesson_header("Domain, Range, Minimum and Maximum")
        q = MathTex(r"\text{What is the range of } g(x) = -x^2 + 4\text{?}", font_size=40)
        opts = [MathTex(r"y \le 4", font_size=42), MathTex(r"y \ge 4", font_size=42),
                MathTex(r"\text{all real numbers}", font_size=36)]
        p = self.predict(q, opts, correct=0, center=UP * 0.3)
        self.banner_correct("Correct!", "The vertex (0, 4) is the highest point.")
        self.wait(0.8)
        self.press(self.cont_btn)
        self.play(FadeOut(p["all"]), FadeOut(self.banner), run_time=0.4)
        self.cont_btn = None

        def build(f, yr, cx, col, tex):
            ax = lesson_axes([-3, 3, 1], yr, 4.6, 3.2)
            ax.move_to([cx, 0.55, 0])
            gc = self.graph_card(ax)
            g = ax.plot(f, x_range=[-2.3, 2.3], color=col, stroke_width=6)
            lab = MathTex(tex, font_size=32, color=col).move_to(ax.c2p(1.75, 6.4))
            return ax, gc, g, lab
        axL, gcL, gL, labL = build(lambda x: x * x, [-1, 7, 1], -3.4, GREEN, "f(x) = x^2")
        axR, gcR, gR, labR = build(lambda x: -x * x + 4, [-3, 5, 1], 3.4, RED, "g(x) = -x^2 + 4")
        labR.move_to(axR.c2p(1.75, -2.4))
        self.play(FadeIn(gcL), FadeIn(gcR), Create(axL), Create(axR), run_time=0.7)
        self.play(Create(gL), Create(gR), Write(labL), Write(labR), run_time=1.1)

        dL = DoubleArrow(axL.c2p(-3, 0), axL.c2p(3, 0), color=PURPLE, buff=0, stroke_width=5, tip_length=0.2)
        dR = DoubleArrow(axR.c2p(-3, 0), axR.c2p(3, 0), color=PURPLE, buff=0, stroke_width=5, tip_length=0.2)
        dom = MathTex(r"\text{Domain (both): all real numbers } (-\infty, \infty)", font_size=32, color=PURPLE)
        dom.move_to(DOWN * 1.65)
        self.play(GrowFromCenter(dL), GrowFromCenter(dR), Write(dom), run_time=1.0)
        self.wait(0.8)
        rL = Arrow(axL.c2p(0, 0), axL.c2p(0, 7), color=GOLD, buff=0, stroke_width=7,
                   max_tip_length_to_length_ratio=0.08).shift(LEFT * 0.12)
        rR = Arrow(axR.c2p(0, 4), axR.c2p(0, -3), color=GOLD, buff=0, stroke_width=7,
                   max_tip_length_to_length_ratio=0.08).shift(LEFT * 0.12)
        mL = Dot(axL.c2p(0, 0), color=GOLD, radius=0.11, stroke_color=INK, stroke_width=2)
        mR = Dot(axR.c2p(0, 4), color=GOLD, radius=0.11, stroke_color=INK, stroke_width=2)
        self.play(GrowArrow(rL), GrowArrow(rR), FadeIn(mL, scale=2), FadeIn(mR, scale=2), run_time=0.9)
        tL = VGroup(MathTex(r"\text{Range: } y \ge 0", font_size=30, color=GOLD_TXT),
                    MathTex(r"\text{Minimum: } 0 \text{ at } (0, 0)", font_size=30, color=GREEN_DARK)
                    ).arrange(DOWN, buff=0.15).move_to([-3.4, -2.4, 0])
        tR = VGroup(MathTex(r"\text{Range: } y \le 4", font_size=30, color=GOLD_TXT),
                    MathTex(r"\text{Maximum: } 4 \text{ at } (0, 4)", font_size=30, color=RED)
                    ).arrange(DOWN, buff=0.15).move_to([3.4, -2.4, 0])
        self.play(Write(tL[0]), Write(tR[0]), run_time=0.7)
        self.play(Write(tL[1]), Write(tR[1]), Flash(mL.get_center(), color=GREEN),
                  Flash(mR.get_center(), color=RED), run_time=0.8)
        self.finish(2.2)


# ======================================================================
# S11 - Tables of values with Desmos
# ======================================================================
class S11DesmosTable(LessonScene):
    PART = 11

    def construct(self):
        self.lesson_header("Build a Table of Values with Desmos")
        dc = card(4.8, 4.75).move_to([-3.9, -0.15, 0])
        r1 = body("1", 16, MUTED).move_to(dc[1].get_corner(UL) + np.array([0.3, -0.42, 0]))
        expr = MathTex("f(x) = x^2 - 2x - 3", font_size=36).next_to(r1, RIGHT, buff=0.3)
        sep = Line(dc[1].get_corner(UL) + np.array([0.02, -0.85, 0]), dc[1].get_corner(UR) + np.array([-0.02, -0.85, 0]),
                   color=EDGE, stroke_width=2)
        r2 = body("2", 16, MUTED).move_to(r1.get_center() + DOWN * 0.85)
        self.play(FadeIn(dc), FadeIn(r1), run_time=0.4)
        self.play(Write(expr), Create(sep), FadeIn(r2), run_time=0.9)
        frame, hm, cell = self.table_frame(["x_1", "f(x_1)"], 5, (-5.5, r2.get_y() + 0.25), colw=1.6, rowh=0.5, size=30)
        self.play(FadeIn(frame), FadeIn(hm), run_time=0.5)

        ax = lesson_axes([-3, 5, 1], [-5, 6, 1], 5.8, 4.4)
        ax.move_to([2.95, -0.15, 0])
        gc = self.graph_card(ax)
        nums = axis_numbers(ax, xs=(-2, -1, 1, 2, 3, 4), ys=(-4, -2, 2, 4))
        self.play(FadeIn(gc), Create(ax), FadeIn(nums), run_time=0.7)

        f = lambda x: x * x - 2 * x - 3
        for i, x in enumerate(range(-1, 4)):
            rx = MathTex(str(x), font_size=30).move_to(cell(i, 0))
            ry = MathTex(str(f(x)), font_size=30, color=GOLD_TXT).move_to(cell(i, 1))
            d = Dot(ax.c2p(x, f(x)), color=GOLD, radius=0.1, stroke_color=INK, stroke_width=1.5)
            self.play(FadeIn(rx, shift=RIGHT * 0.1), run_time=0.22)
            self.play(FadeIn(ry, shift=RIGHT * 0.1), TransformFromCopy(ry, d), run_time=0.4)
        g = ax.plot(f, x_range=[-1.75, 3.75], color=CORAL, stroke_width=6)
        self.play(Create(g), run_time=1.2)
        vring = Circle(radius=0.25, color=GREEN, stroke_width=4).move_to(ax.c2p(1, -4))
        r3 = body("3", 16, MUTED).move_to([r1.get_x(), -2.15, 0])
        vlab = MathTex(r"\text{minimum } -4 \text{ at } (1, -4)", font_size=30, color=GREEN_DARK)
        vlab.next_to(r3, RIGHT, buff=0.3)
        self.add(r3)
        self.play(Create(vring), Write(vlab), run_time=0.7)
        sym = DashedLine(ax.c2p(1, -4.8), ax.c2p(1, 5.6), color=PURPLE, stroke_width=3)
        self.play(Create(sym), run_time=0.5)
        tk = self.note("Notice the mirror: 0, −3, −4, −3, 0.   Range: y ≥ −4", MUTED, 21, y=-2.82)
        self.play(FadeIn(tk), run_time=0.4)
        self.finish(2.2)


# ======================================================================
# S12 - Lesson complete
# ======================================================================
class S12WrapUp(LessonScene):
    PART = 12

    def construct(self):
        self.lesson_header("Lesson Complete: Welcome, Quadratic Functions!")
        items = ["f(x) = y: the output for each input x",
                 "Standard form: f(x) = ax² + bx + c, with a ≠ 0",
                 "The graph is a symmetrical curve called a parabola",
                 "Vertex = turning point (minimum or maximum)",
                 "a: up or down, narrow or wide.   c: the y-intercept",
                 "Physics: b = initial velocity, gravity bends the path",
                 "Domain: all real numbers.  Range depends on the vertex"]
        rows = VGroup()
        for s in items:
            ic = Circle(radius=0.15, fill_color=CARD, fill_opacity=1, stroke_color=EDGE, stroke_width=3)
            t = body(s, 22)
            rows.add(VGroup(ic, t.next_to(ic, RIGHT, buff=0.25)))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        box = card(rows.width + 1.0, rows.height + 0.7).move_to(DOWN * 0.05)
        rows.move_to(box)
        self.play(FadeIn(box, shift=UP * 0.2), FadeIn(rows), run_time=0.7)
        for r in rows:
            ci = check_icon(GREEN, 0.15).move_to(r[0])
            self.play(FadeIn(ci, scale=1.5), r[1].animate.set_color(INK), run_time=0.35)
            self.wait(0.3)

        # celebration burst
        rng = np.random.default_rng(7)
        bits = VGroup()
        cols = [GOLD, GREEN, CORAL, BLUE, PURPLE]
        for i in range(28):
            ang = rng.uniform(0, TAU)
            b = RoundedRectangle(corner_radius=0.03, width=0.16, height=0.08,
                                 fill_color=cols[i % 5], fill_opacity=1, stroke_width=0)
            b.move_to(UP * 2.0).rotate(ang)
            b.target_pt = UP * 2.0 + np.array([np.cos(ang) * rng.uniform(1.5, 5.5), np.sin(ang) * rng.uniform(0.6, 1.6), 0])
            bits.add(b)
        self.play(LaggedStart(*[b.animate.move_to(b.target_pt).rotate(PI).set_opacity(0) for b in bits],
                              lag_ratio=0.02), run_time=1.4)
        close = heading("Math describes how the world moves.", 30, GOLD).move_to([0, -2.55, 0])
        self.play(FadeIn(close, shift=UP * 0.2), run_time=0.6)
        fin = pill("Finish", INK, WHITE, w=3.4, h=0.62, size=22).move_to([0, BOTTOM_Y, 0])
        self.play(FadeIn(fin, shift=UP * 0.2), run_time=0.4)
        self.cont_btn = fin
        self.finish(2.4)
