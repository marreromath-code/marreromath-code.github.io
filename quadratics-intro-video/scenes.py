"""Quadratic Functions - Unit Introduction (Marrero Math Design System).

Scenes render in display order S00 ... S12. Every number shown on screen is
checked in verify_math.py.

Mobbin-inspired additions on top of the Marrero base: a lesson progress bar
and "Part n" chip (course-player pattern), rounded option cards for the quick
check (quiz pattern), and a Desmos-style expression/table card.
"""

from marrero_manim_base import *

TOTAL_PARTS = 12
PURPLE = "#B794F6"  # extra role color: function names / notation


# ======================================================================
# Shared scene class: header + lesson progress bar + smooth exit
# ======================================================================
class QScene(MarreroScene):
    PART = 0
    CHAPTER = ""

    def add_header(self, title):
        t = super().add_header(title)
        # lesson progress bar (course-player pattern)
        y = -3.86
        track = Line(LEFT * 6.5 + UP * y, RIGHT * 6.5 + UP * y,
                     stroke_width=4, color=EDGE)
        start = max(self.PART - 1, 0) / TOTAL_PARTS
        end = self.PART / TOTAL_PARTS
        tracker = ValueTracker(start)
        fill = always_redraw(lambda: Line(
            LEFT * 6.5 + UP * y,
            LEFT * 6.5 + RIGHT * (13 * max(tracker.get_value(), 0.001)) + UP * y,
            stroke_width=4, color=ACCENT))
        chip_txt = Text(f"PART {self.PART} · {self.CHAPTER}", font_size=15,
                        color=NAVY, weight=BOLD)
        chip = RoundedRectangle(corner_radius=0.13, width=chip_txt.width + 0.4,
                                height=0.3, fill_color=ACCENT, fill_opacity=1,
                                stroke_width=0)
        chip_txt.move_to(chip)
        chip_g = VGroup(chip, chip_txt).to_corner(DL, buff=0.22).shift(UP * 0.02)
        self.add(track, fill)
        self.play(FadeIn(chip_g, shift=RIGHT * 0.2),
                  tracker.animate.set_value(end), run_time=0.8)
        return t

    def finish(self, t=1.6):
        self.wait(t)
        for m in self.mobjects:
            m.clear_updaters()
        self.mobjects = [m for m in self.mobjects
                         if m.has_points() or len(m.family_members_with_points()) > 0]
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

    def card(self, mobj, pad=0.35, color=EDGE, fill=CARD):
        box = RoundedRectangle(corner_radius=0.15, width=mobj.width + pad * 2,
                               height=mobj.height + pad * 1.4, fill_color=fill,
                               fill_opacity=1, stroke_color=color,
                               stroke_width=1.5)
        box.move_to(mobj)
        return box

    def takeaway(self, s, color=MUTED, size=24):
        t = Text(s, font_size=size, color=color)
        fit(t, 12.0)
        t.move_to(DOWN * 3.3)
        return t


def lbl(s, color=INK, size=24):
    return Text(s, font_size=size, color=color)


# ======================================================================
# S00 - Title + roadmap
# ======================================================================
class S00Title(QScene):
    def construct(self):
        title = Text("Quadratic Functions", font_size=60, color=ACCENT,
                     weight=BOLD).to_edge(UP, buff=0.55)
        sub = Text("Unit Introduction  ·  Where Mathematics Meets Physics",
                   font_size=26, color=MUTED).next_to(title, DOWN, buff=0.2)
        foot = Text("Marrero Math", font_size=16, color=MUTED).to_corner(DR, buff=0.22)
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(sub, shift=UP * 0.2), FadeIn(foot), run_time=0.7)

        items = ["Function notation",
                 "Structure & standard form",
                 "The parent function & parabola",
                 "Vertex, a and c",
                 "Physics: throwing a ball",
                 "Domain, range, min & max"]
        rows = VGroup(*[Text(f"{i+1}.  {s}", font_size=27, color=INK)
                        for i, s in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rows.move_to(LEFT * 3.2 + DOWN * 0.75)

        ax = Axes(x_range=[-3, 3, 1], y_range=[-1, 9, 2], x_length=4.4,
                  y_length=4.0, tips=False,
                  axis_config=dict(color=MUTED, stroke_width=2))
        ax.move_to(RIGHT * 3.6 + DOWN * 0.75)
        grid = NumberPlane(x_range=[-3, 3, 1], y_range=[-1, 9, 1],
                           x_length=4.4, y_length=4.0,
                           background_line_style=dict(stroke_color=EDGE,
                                                      stroke_width=1,
                                                      stroke_opacity=0.6),
                           axis_config=dict(stroke_opacity=0))
        grid.move_to(ax.c2p(0, 4))
        grid.shift(ax.c2p(0, 0) - grid.c2p(0, 0))
        curve = ax.plot(lambda x: x ** 2, x_range=[-2.95, 2.95], color=WARN,
                        stroke_width=5)

        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows],
                              lag_ratio=0.18), FadeIn(grid), Create(ax),
                  run_time=2.2)
        self.play(Create(curve), run_time=1.6)
        tr = ValueTracker(-2.95)
        dot = always_redraw(lambda: Dot(ax.c2p(tr.get_value(), tr.get_value() ** 2),
                                        color=ACCENT, radius=0.11))
        self.add(dot)
        self.play(tr.animate.set_value(2.95), run_time=2.6,
                  rate_func=there_and_back_with_pause)
        tag = Text("the parabola", font_size=22, color=WARN).next_to(ax, UP, buff=0.05)
        self.play(FadeIn(tag, shift=DOWN * 0.15), run_time=0.6)
        self.wait(2.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ======================================================================
# S01 - Function notation f(x) = y
# ======================================================================
class S01FunctionNotation(QScene):
    PART, CHAPTER = 1, "Function Notation"

    def construct(self):
        self.add_header("Start Here: Function Notation")
        eq = MathTex("f", "(", "x", ")", "=", "y", font_size=80)
        eq[0].set_color(PURPLE)
        eq[2].set_color(GOOD)
        eq[5].set_color(ACCENT)
        eq.move_to(UP * 1.55)
        self.play(Write(eq), run_time=1.0)

        n1 = lbl("name of the function", PURPLE, 22).next_to(eq[0], LEFT, buff=0.6).shift(UP * 0.35)
        n2 = lbl("input", GOOD, 22).next_to(eq[2], DOWN, buff=0.45)
        n3 = lbl("output", ACCENT, 22).next_to(eq[5], RIGHT, buff=0.55).shift(UP * 0.35)
        a1 = Arrow(n1.get_right(), eq[0].get_left(), buff=0.1, color=PURPLE, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        a2 = Arrow(n2.get_top(), eq[2].get_bottom(), buff=0.08, color=GOOD, stroke_width=3, max_tip_length_to_length_ratio=0.3)
        a3 = Arrow(n3.get_left(), eq[5].get_right(), buff=0.1, color=ACCENT, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        for n, a in ((n1, a1), (n2, a2), (n3, a3)):
            self.play(FadeIn(n, shift=UP * 0.1), GrowArrow(a), run_time=0.6)
        self.wait(0.6)

        # function machine
        machine_tex = MathTex("f(x) = x^2", font_size=44, color=INK)
        machine = RoundedRectangle(corner_radius=0.2, width=3.4, height=1.3,
                                   fill_color=CARD, fill_opacity=1,
                                   stroke_color=PURPLE, stroke_width=3)
        machine.move_to(DOWN * 1.35)
        machine_tex.move_to(machine)
        in_lbl = lbl("input  x", GOOD, 22).move_to(LEFT * 4.6 + DOWN * 0.55)
        out_lbl = lbl("output  f(x)", ACCENT, 22).move_to(RIGHT * 4.6 + DOWN * 0.55)
        a_in = Arrow(LEFT * 3.7 + DOWN * 1.35, machine.get_left(), buff=0.1, color=MUTED)
        a_out = Arrow(machine.get_right(), RIGHT * 3.7 + DOWN * 1.35, buff=0.1, color=MUTED)
        self.play(FadeIn(machine), Write(machine_tex), GrowArrow(a_in),
                  GrowArrow(a_out), FadeIn(in_lbl), FadeIn(out_lbl), run_time=1.0)

        for xin in ("3", "-3"):
            x_m = MathTex(xin, font_size=56, color=GOOD).move_to(LEFT * 4.6 + DOWN * 1.35)
            self.play(FadeIn(x_m, shift=RIGHT * 0.3), run_time=0.4)
            self.play(x_m.animate.move_to(machine.get_center()).scale(0.3).set_opacity(0),
                      machine.animate.set_stroke(ACCENT), run_time=0.7)
            y_m = MathTex("9", font_size=56, color=ACCENT).move_to(machine.get_center()).scale(0.3)
            self.play(y_m.animate.scale(1 / 0.3).move_to(RIGHT * 4.6 + DOWN * 1.35),
                      machine.animate.set_stroke(PURPLE), run_time=0.7)
            calc = MathTex(f"f({xin}) = ({xin})^2 = 9" if xin == "-3" else "f(3) = 3^2 = 9",
                           font_size=36, color=INK)
            calc.move_to(DOWN * 2.6 + (LEFT * 3.0 if xin == "3" else RIGHT * 3.0))
            self.play(Write(calc), run_time=0.7)
            self.wait(0.5)
            self.remove(x_m)
            self.play(FadeOut(y_m), run_time=0.3)

        tk = self.takeaway("f(x) does NOT mean f times x.  It is the output y for the input x.",
                           ACCENT, 23)
        self.play(FadeIn(tk, shift=UP * 0.15), run_time=0.7)
        self.finish(2.2)


# ======================================================================
# S02 - What makes a function quadratic?
# ======================================================================
class S02WhatIsQuadratic(QScene):
    PART, CHAPTER = 2, "Structure"

    def construct(self):
        self.add_header("What Makes a Function Quadratic?")
        eq = MathTex("f(x)", "=", "x^2", "+", "5x", "+", "10", font_size=78)
        eq.move_to(UP * 1.3)
        self.play(Write(eq), run_time=1.2)

        terms = [eq[2], eq[4], eq[6]]
        boxes = VGroup(*[SurroundingRectangle(t, color=BRANCH, buff=0.12,
                                              corner_radius=0.08) for t in terms])
        self.play(LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.3), run_time=1.0)
        poly = lbl("poly = many  →  several terms added together:  a polynomial", MUTED, 23)
        poly.move_to(UP * 0.0)
        self.play(FadeIn(poly, shift=UP * 0.1), run_time=0.7)
        self.wait(1.2)

        self.play(FadeOut(boxes[1:]), boxes[0].animate.set_color(ACCENT),
                  eq[2].animate.set_color(ACCENT), run_time=0.7)
        arrow = Arrow(eq[2].get_bottom() + DOWN * 1.4, eq[2].get_bottom() + DOWN * 0.15,
                      color=ACCENT, buff=0)
        arrow.shift(DOWN * 0.15)
        note = lbl("highest exponent is 2  →  degree 2", ACCENT, 27)
        note.next_to(arrow, DOWN, buff=0.15)
        self.play(FadeOut(poly), GrowArrow(arrow), FadeIn(note, shift=UP * 0.1), run_time=0.8)
        self.wait(0.8)

        # degree ladder chips
        chips = VGroup()
        for tex, name, col in (("x^1", "linear", MUTED), ("x^2", "quadratic", ACCENT),
                               ("x^3", "cubic", MUTED)):
            m = MathTex(tex, font_size=40, color=col)
            t = lbl(name, col, 22)
            g = VGroup(m, t).arrange(RIGHT, buff=0.25)
            g.add_to_back(self.card(g, pad=0.3, color=col if col == ACCENT else EDGE))
            chips.add(g)
        chips.arrange(RIGHT, buff=0.5).move_to(DOWN * 2.45)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in chips], lag_ratio=0.25),
                  run_time=1.2)
        self.play(Indicate(chips[1], color=ACCENT, scale_factor=1.12), run_time=0.9)
        self.finish(2.0)


# ======================================================================
# S03 - Standard form anatomy
# ======================================================================
class S03StandardForm(QScene):
    PART, CHAPTER = 3, "Standard Form"

    def construct(self):
        self.add_header("Standard Form of a Quadratic Function")
        eq = MathTex("f(x)", "=", "a", "x^2", "+", "b", "x", "+", "c", font_size=84)
        eq.move_to(UP * 0.85)
        self.play(Write(eq), run_time=1.2)

        # leading term
        br1 = Brace(VGroup(eq[2], eq[3]), DOWN, color=ACCENT)
        t1 = lbl("leading term", ACCENT, 23).next_to(br1, DOWN, buff=0.12)
        self.play(eq[2].animate.set_color(ACCENT), eq[3].animate.set_color(ACCENT),
                  GrowFromCenter(br1), FadeIn(t1), run_time=0.8)
        lc = lbl("leading coefficient  (a ≠ 0)", ACCENT, 22)
        lc.next_to(eq[2], UP, buff=0.75).shift(LEFT * 1.1)
        lca = Arrow(lc.get_bottom() + RIGHT * 1.0, eq[2].get_top(), buff=0.08,
                    color=ACCENT, stroke_width=3)
        self.play(FadeIn(lc), GrowArrow(lca), run_time=0.7)
        self.wait(0.6)

        # middle term
        br2 = Brace(VGroup(eq[5], eq[6]), DOWN, color=GOOD)
        t2 = lbl("middle term", GOOD, 23).next_to(br2, DOWN, buff=0.12)
        self.play(eq[5].animate.set_color(GOOD), eq[6].animate.set_color(GOOD),
                  GrowFromCenter(br2), FadeIn(t2), run_time=0.8)
        # constant
        br3 = Brace(eq[8], DOWN, color=WARN)
        t3 = lbl("constant", WARN, 23).next_to(br3, DOWN, buff=0.12).shift(RIGHT * 0.45 + DOWN * 0.42)
        self.play(eq[8].animate.set_color(WARN), GrowFromCenter(br3), FadeIn(t3),
                  run_time=0.8)
        self.wait(0.6)

        # x = x^1 note and constant note
        n1 = MathTex("x = x^1", font_size=40, color=GOOD)
        n1t = lbl("the exponent 1 is never written", INK, 22)
        g1 = VGroup(n1, n1t).arrange(RIGHT, buff=0.3)
        n2 = lbl("c is just a number: positive or negative", INK, 22)
        n2d = Dot(color=WARN, radius=0.09)
        g2 = VGroup(n2d, n2).arrange(RIGHT, buff=0.25)
        notes = VGroup(g1, g2).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        notes.move_to(DOWN * 2.15)
        self.play(FadeIn(g1, shift=UP * 0.1), run_time=0.7)
        self.play(FadeIn(g2, shift=UP * 0.1), run_time=0.7)
        self.wait(1.4)

        # example mapping
        self.play(FadeOut(notes), FadeOut(VGroup(br1, br2, br3, t1, t2, t3, lc, lca)),
                  eq.animate.scale(0.6).move_to(UP * 1.6), run_time=0.8)
        ex = MathTex("f(x)", "=", "3", "x^2", "+", "5", "x", "-", "1", font_size=60)
        ex.move_to(UP * 0.2)
        ex[2].set_color(ACCENT); ex[5].set_color(GOOD); ex[7:9].set_color(WARN)
        self.play(TransformFromCopy(eq, ex), run_time=1.0)
        chips = VGroup()
        for s, col in (("a = 3", ACCENT), ("b = 5", GOOD), ("c = -1", WARN)):
            m = MathTex(s, font_size=44, color=col)
            chips.add(VGroup(self.card(m, pad=0.35, color=col), m))
        chips.arrange(RIGHT, buff=0.6).move_to(DOWN * 1.5)
        srcs = [ex[2], ex[5], ex[7:9]]
        for c, s in zip(chips, srcs):
            self.play(Indicate(s, color=c[1].get_color()), FadeIn(c, shift=UP * 0.2),
                      run_time=0.6)
        tk = self.takeaway("Keep the sign with the number:  − 1  means  c = −1.", MUTED, 22)
        self.play(FadeIn(tk), run_time=0.5)
        self.finish(2.0)


# ======================================================================
# S04 - The parent function y = x^2 (table -> dots -> parabola)
# ======================================================================
class S04ParentFunction(QScene):
    PART, CHAPTER = 4, "Parent Function"

    def construct(self):
        self.add_header("The Parent Function and the Parabola")
        head = MathTex("f(x) = x^2", font_size=46, color=ACCENT).move_to(LEFT * 4.3 + UP * 2.2)
        self.play(Write(head), run_time=0.7)

        xs = list(range(-3, 4))
        col_x = MathTex("x", font_size=36, color=GOOD)
        col_y = MathTex("f(x)", font_size=36, color=ACCENT)
        rows = []
        top = 1.45
        col_x.move_to([-5.1, top, 0]); col_y.move_to([-3.5, top, 0])
        hline = Line([-5.8, top - 0.3, 0], [-2.8, top - 0.3, 0], color=EDGE, stroke_width=2)
        vline = Line([-4.3, top + 0.3, 0], [-4.3, top - 0.3 - 7 * 0.56, 0], color=EDGE, stroke_width=2)
        self.play(FadeIn(col_x), FadeIn(col_y), Create(hline), Create(vline), run_time=0.6)

        ax = Axes(x_range=[-4, 4, 1], y_range=[-1, 10, 1], x_length=6.4, y_length=5.3,
                  tips=False, axis_config=dict(color=MUTED, stroke_width=2,
                                               include_numbers=False))
        ax.move_to(RIGHT * 2.6 + DOWN * 0.3)
        nums = VGroup(*[MathTex(str(v), font_size=22, color=MUTED).next_to(ax.c2p(v, 0), DOWN, buff=0.12)
                        for v in (-3, -2, -1, 1, 2, 3)],
                      *[MathTex(str(v), font_size=22, color=MUTED).next_to(ax.c2p(0, v), LEFT, buff=0.12)
                        for v in (1, 4, 9)])
        self.play(Create(ax), FadeIn(nums), run_time=0.9)

        dots = VGroup()
        for i, x in enumerate(xs):
            y = top - 0.56 * (i + 1)
            rx = MathTex(str(x), font_size=32).move_to([-5.1, y, 0])
            ry = MathTex(str(x * x), font_size=32, color=ACCENT).move_to([-3.5, y, 0])
            d = Dot(ax.c2p(x, x * x), color=ACCENT, radius=0.09)
            self.play(FadeIn(rx, shift=RIGHT * 0.15), run_time=0.22)
            self.play(FadeIn(ry, shift=RIGHT * 0.15), TransformFromCopy(ry, d), run_time=0.4)
            dots.add(d)
        self.wait(0.4)
        curve = ax.plot(lambda x: x ** 2, x_range=[-3.15, 3.15], color=WARN, stroke_width=5)
        self.play(Create(curve), run_time=1.6)
        name = lbl("parabola", WARN, 28).next_to(ax.c2p(3.15, 9.9), LEFT, buff=0.3)
        self.play(FadeIn(name, shift=LEFT * 0.2), run_time=0.5)

        desmos_t = lbl("Try it in Desmos: type", MUTED, 22)
        desmos_m = MathTex("y = x^2", font_size=34, color=INK)
        dg = VGroup(desmos_t, desmos_m).arrange(RIGHT, buff=0.2)
        dg.move_to(LEFT * 4.2 + DOWN * 3.25)
        self.play(FadeIn(dg, shift=UP * 0.1), run_time=0.6)
        self.finish(2.2)


# ======================================================================
# S05 - Behavior left to right, vertex, symmetry
# ======================================================================
class S05VertexBehavior(QScene):
    PART, CHAPTER = 5, "Vertex"

    def construct(self):
        self.add_header("Read the Parabola from Left to Right")
        ax = Axes(x_range=[-4, 4, 1], y_range=[-1, 10, 1], x_length=6.2, y_length=5.0,
                  tips=False, axis_config=dict(color=MUTED, stroke_width=2))
        ax.move_to(LEFT * 3.0 + DOWN * 0.2)
        curve = ax.plot(lambda x: x ** 2, x_range=[-3.0, 3.0], color=INK, stroke_width=4)
        self.play(Create(ax), Create(curve), run_time=1.0)

        tr = ValueTracker(-3.0)
        dot = always_redraw(lambda: Dot(ax.c2p(tr.get_value(), tr.get_value() ** 2),
                                        color=ACCENT, radius=0.12))
        left_branch = ax.plot(lambda x: x ** 2, x_range=[-3.0, 0], color=WARN, stroke_width=7)
        right_branch = ax.plot(lambda x: x ** 2, x_range=[0, 3.0], color=GOOD, stroke_width=7)
        self.add(dot)

        r1 = self.bullet_rows([("Decreasing: the graph goes down", WARN)], font_size=24)
        r2 = self.bullet_rows([("Vertex (0, 0): the turning point", ACCENT)], font_size=24)
        r3 = self.bullet_rows([("Increasing: the graph goes up", GOOD)], font_size=24)
        r4 = self.bullet_rows([("Axis of symmetry: x = 0", PURPLE)], font_size=24)
        col = VGroup(r1, r2, r3, r4).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        col.move_to(RIGHT * 3.6 + UP * 0.6)

        self.play(Create(left_branch), tr.animate.set_value(0), FadeIn(r1, shift=LEFT * 0.2),
                  run_time=2.2, rate_func=linear)
        vring = Circle(radius=0.28, color=ACCENT, stroke_width=4).move_to(ax.c2p(0, 0))
        self.play(Create(vring), FadeIn(r2, shift=LEFT * 0.2), Flash(ax.c2p(0, 0), color=ACCENT),
                  run_time=0.9)
        self.wait(0.5)
        self.play(Create(right_branch), tr.animate.set_value(3.0), FadeIn(r3, shift=LEFT * 0.2),
                  run_time=2.2, rate_func=linear)
        self.wait(0.4)

        axis = DashedLine(ax.c2p(0, -0.8), ax.c2p(0, 9.8), color=PURPLE, stroke_width=4)
        self.play(Create(axis), FadeIn(r4, shift=LEFT * 0.2), run_time=0.9)
        # mirror pairs
        for x in (2, 1, 3):
            p1, p2 = ax.c2p(-x, x * x), ax.c2p(x, x * x)
            seg = DashedLine(p1, p2, color=PURPLE, stroke_width=2.5)
            d1, d2 = Dot(p1, color=PURPLE), Dot(p2, color=PURPLE)
            self.play(Create(seg), FadeIn(d1), FadeIn(d2), run_time=0.45)
        pair = MathTex("f(-2) = f(2) = 4", font_size=34, color=PURPLE)
        pair.next_to(col, DOWN, buff=0.6)
        self.play(Write(pair), run_time=0.7)
        tk = self.takeaway("Two symmetrical branches meet at the vertex.", MUTED, 23)
        self.play(FadeIn(tk), run_time=0.5)
        self.finish(2.0)


# ======================================================================
# S06 - Preview: effect of a
# ======================================================================
class S06EffectOfA(QScene):
    PART, CHAPTER = 6, "Coefficient a"

    def construct(self):
        self.add_header("Preview: How a Shapes the Parabola")
        ax = Axes(x_range=[-4, 4, 1], y_range=[-8, 8, 2], x_length=6.0, y_length=5.6,
                  tips=False, axis_config=dict(color=MUTED, stroke_width=2))
        ax.move_to(LEFT * 3.1 + DOWN * 0.45)
        self.play(Create(ax), run_time=0.8)
        a = ValueTracker(1.0)

        def graph():
            av = a.get_value()
            lim = min(3.6, (7.6 / abs(av)) ** 0.5) if abs(av) > 1e-3 else 3.6
            col = GOOD if av > 0.02 else (BAD if av < -0.02 else MUTED)
            return ax.plot(lambda x: av * x * x, x_range=[-lim, lim], color=col, stroke_width=5)
        g = always_redraw(graph)
        ghost = ax.plot(lambda x: x * x, x_range=[-2.75, 2.75], color=MUTED,
                        stroke_width=2, stroke_opacity=0.5)
        self.add(ghost)
        self.play(Create(g), run_time=1.0)

        lab = MathTex("f(x) =", font_size=46)
        num = DecimalNumber(1.0, num_decimal_places=1, font_size=46, color=ACCENT,
                            include_sign=False)
        xx = MathTex("x^2", font_size=46)
        readout = VGroup(lab, num, xx).arrange(RIGHT, buff=0.15)
        readout.move_to(RIGHT * 3.3 + UP * 2.0)
        num.add_updater(lambda m: m.set_value(a.get_value()))
        avl = MathTex("a =", font_size=34, color=MUTED)
        aval = DecimalNumber(1.0, num_decimal_places=1, font_size=34, color=ACCENT)
        aval.add_updater(lambda m: m.set_value(a.get_value()))
        ag = VGroup(avl, aval).arrange(RIGHT, buff=0.15).next_to(readout, DOWN, buff=0.25)
        self.play(FadeIn(readout), FadeIn(ag), run_time=0.6)

        c1 = self.bullet_rows([("|a| > 1: narrower", INK)], font_size=24)
        c2 = self.bullet_rows([("|a| < 1: wider", INK)], font_size=24)
        c3 = self.bullet_rows([("a > 0: opens up (minimum)", GOOD)], font_size=24)
        c4 = self.bullet_rows([("a < 0: opens down (maximum)", BAD)], font_size=24)
        col = VGroup(c3, c4, c1, c2).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        col.move_to(RIGHT * 3.3 + DOWN * 1.15)

        self.play(FadeIn(c3, shift=LEFT * 0.2), run_time=0.5)
        self.play(a.animate.set_value(3.0), FadeIn(c1, shift=LEFT * 0.2), run_time=1.6)
        self.wait(0.5)
        self.play(a.animate.set_value(0.5), FadeIn(c2, shift=LEFT * 0.2), run_time=1.8)
        self.wait(0.5)
        self.play(a.animate.set_value(-1.0), FadeIn(c4, shift=LEFT * 0.2), run_time=2.2)
        self.wait(0.5)
        self.play(a.animate.set_value(-2.0), run_time=1.2)
        self.wait(0.4)
        self.play(a.animate.set_value(1.0), run_time=1.8)
        tk = self.takeaway("a = 0 would erase the x² term: then it is not quadratic.", WARN, 22)
        self.play(FadeIn(tk), run_time=0.5)
        num.clear_updaters(); aval.clear_updaters()
        self.finish(2.0)


# ======================================================================
# S07 - The constant c is the y-intercept
# ======================================================================
class S07ConstantC(QScene):
    PART, CHAPTER = 7, "Constant c"

    def construct(self):
        self.add_header("The Constant c Is the y-Intercept")
        ax = Axes(x_range=[-3, 2, 1], y_range=[-5, 7, 1], x_length=5.0, y_length=5.2,
                  tips=False, axis_config=dict(color=MUTED, stroke_width=2))
        ax.move_to(LEFT * 3.6 + DOWN * 0.25)
        ynums = VGroup(*[MathTex(str(v), font_size=20, color=MUTED).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                         for v in (-4, -2, 2, 4, 6)])
        xnums = VGroup(*[MathTex(str(v), font_size=20, color=MUTED).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                         for v in (-2, 1)])
        self.play(Create(ax), FadeIn(ynums), FadeIn(xnums), run_time=0.8)

        eq = MathTex("f(x)", "=", "3x^2", "+", "5x", "-", "1", font_size=50)
        eq.move_to(RIGHT * 2.9 + UP * 2.0)
        self.play(Write(eq), run_time=0.9)
        c = ValueTracker(-1.0)
        g = always_redraw(lambda: ax.plot(lambda x: 3 * x * x + 5 * x + c.get_value(),
                                          x_range=[-2.3, 0.7], color=WARN, stroke_width=5))
        self.play(Create(g), run_time=1.2)

        steps = self.steps_column(["f(0) = 3(0)^2 + 5(0) - 1",
                                   "f(0) = 0 + 0 - 1",
                                   "f(0) = -1"], left_x=0.9, top_y=0.95, gap=0.8,
                                  font_size=38, max_w=5.3)
        for m in steps:
            self.play(Write(m), run_time=0.7)
        box = self.answer_box(steps[-1])
        self.play(eq[5:7].animate.set_color(ACCENT), run_time=0.4)

        yd = always_redraw(lambda: Dot(ax.c2p(0, c.get_value()), color=ACCENT, radius=0.12))
        pt = MathTex("(0, -1)", font_size=32, color=ACCENT).next_to(ax.c2p(0, -1), RIGHT, buff=0.25)
        self.play(FadeIn(yd, scale=2), Flash(ax.c2p(0, -1), color=ACCENT), Write(pt), run_time=0.8)
        cross = lbl("where the graph crosses the y-axis", ACCENT, 22)
        cross.move_to(RIGHT * 3.3 + DOWN * 1.65)
        self.play(FadeIn(cross, shift=UP * 0.1), run_time=0.5)
        self.wait(1.0)

        # dynamic: change c, intercept follows
        cl = MathTex("c =", font_size=36, color=MUTED)
        cv = DecimalNumber(-1.0, num_decimal_places=1, font_size=36, color=ACCENT)
        cv.add_updater(lambda m: m.set_value(c.get_value()))
        cg = VGroup(cl, cv).arrange(RIGHT, buff=0.15).move_to(RIGHT * 3.3 + DOWN * 2.35)
        self.play(FadeOut(pt), FadeIn(cg), run_time=0.4)
        self.play(c.animate.set_value(2.0), run_time=1.6)
        self.play(c.animate.set_value(-1.0), run_time=1.6)
        cv.clear_updaters()
        tk = self.takeaway("Change c and the whole parabola slides up or down.", MUTED, 22)
        self.play(FadeIn(tk), run_time=0.5)
        self.finish(1.8)


# ======================================================================
# S08 - Quick check: is it quadratic? (sneaky item: out-of-order terms)
# ======================================================================
class S08QuickCheck(QScene):
    PART, CHAPTER = 8, "Quick Check"

    def construct(self):
        self.add_header("Quick Check: Is It Quadratic?")
        items = [("f(x) = 2x^2 - 7", "Quadratic: degree 2  (b = 0)", GOOD),
                 ("g(x) = 4x + 9", "Linear: degree 1", WARN),
                 ("h(x) = x^3 + x^2", "Cubic: degree 3", WARN),
                 ("k(x) = 5x - x^2 + 1", "Quadratic: degree 2", GOOD)]
        cards = VGroup()
        for tex, _, _ in items:
            m = MathTex(tex, font_size=42)
            box = RoundedRectangle(corner_radius=0.18, width=5.6, height=1.55,
                                   fill_color=CARD, fill_opacity=1, stroke_color=EDGE,
                                   stroke_width=1.5)
            m.move_to(box).shift(UP * 0.22)
            cards.add(VGroup(box, m))
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.5, 0.4)).move_to(UP * 0.15)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.2),
                  run_time=1.4)
        self.wait(1.2)
        for c, (_, verdict, col) in zip(cards, items):
            v = lbl(verdict, col, 21).next_to(c[1], DOWN, buff=0.22)
            self.play(c[0].animate.set_stroke(col, width=3), FadeIn(v, shift=UP * 0.1),
                      run_time=0.6)
            c.add(v)
            self.wait(0.5)
        self.wait(0.8)

        # error analysis on the sneaky item
        focus = cards[3]
        others = VGroup(*cards[:3])
        self.play(FadeOut(others), focus.animate.move_to(UP * 1.45), run_time=0.8)
        claim = MathTex("\\text{Claim: } a = 5", font_size=44, color=INK)
        claim.move_to(LEFT * 1.0 + DOWN * 0.1)
        why = lbl("“5 is in the first term”", MUTED, 22).next_to(claim, DOWN, buff=0.15)
        self.play(Write(claim), FadeIn(why), run_time=0.8)
        x = Cross(scale_factor=0.32, stroke_color=BAD, stroke_width=8).next_to(claim, RIGHT, buff=0.5)
        self.play(Create(x), run_time=0.5)
        self.wait(0.6)
        fix = MathTex("k(x)", "=", "-x^2", "+", "5x", "+", "1", font_size=48)
        fix[2].set_color(ACCENT)
        fix.move_to(DOWN * 1.75)
        lead = lbl("Write it in standard form first (highest power first):", INK, 22)
        lead.next_to(fix, UP, buff=0.22)
        self.play(FadeOut(why), FadeIn(lead), Write(fix), run_time=1.0)
        ans = MathTex("a = -1,\\; b = 5,\\; c = 1", font_size=42, color=ACCENT)
        ans.move_to(DOWN * 2.75)
        self.play(Write(ans), run_time=0.8)
        self.answer_box(ans)
        self.finish(2.0)


# ======================================================================
# S09 - Physics: throw a ball from a 25 ft building
# ======================================================================
class S09ThrowTheBall(QScene):
    PART, CHAPTER = 9, "Physics"

    def construct(self):
        self.add_header("Where Does the Parabola Come From? Motion!")
        ax = Axes(x_range=[0, 3.5, 0.5], y_range=[0, 60, 10], x_length=6.2, y_length=5.0,
                  tips=False, axis_config=dict(color=MUTED, stroke_width=2))
        ax.move_to(LEFT * 2.35 + DOWN * 0.3)
        tnums = VGroup(*[MathTex(str(v), font_size=20, color=MUTED).next_to(ax.c2p(v, 0), DOWN, buff=0.12)
                         for v in (1, 2, 3)])
        hnums = VGroup(*[MathTex(str(v), font_size=20, color=MUTED).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                         for v in (10, 20, 30, 40, 50, 60)])
        tl = lbl("time t (s)", MUTED, 18).next_to(ax.c2p(3.5, 0), DOWN, buff=0.35).shift(LEFT * 0.4)
        hl = lbl("height h (ft)", MUTED, 18).next_to(ax.c2p(0, 60), UP, buff=0.12)
        # building (25 ft) standing on the ground at the left of the h-axis
        b_top = ax.c2p(0, 25)
        bld = Rectangle(width=0.75, height=b_top[1] - ax.c2p(0, 0)[1],
                        fill_color=EDGE, fill_opacity=1, stroke_color=BRANCH, stroke_width=2)
        bld.move_to(ax.c2p(0, 12.5)).shift(LEFT * (0.375 + 0.55))
        wins = VGroup(*[Square(0.13, fill_color=ACCENT, fill_opacity=0.55, stroke_width=0)
                        .move_to(bld.get_center() + RIGHT * dx + UP * dy)
                        for dx in (-0.17, 0.17) for dy in (-0.55, -0.15, 0.25, 0.65)])
        ground = Line(ax.c2p(0, 0) + LEFT * 1.3, ax.c2p(3.5, 0), color=MUTED, stroke_width=2)
        self.play(Create(ax), FadeIn(tnums), FadeIn(hnums), FadeIn(tl), FadeIn(hl),
                  FadeIn(bld), FadeIn(wins), Create(ground), run_time=1.2)

        eq = MathTex("h(t)", "=", "-16", "t^2", "+", "40", "t", "+", "25", font_size=46)
        eq.move_to(RIGHT * 3.75 + UP * 2.05)
        self.play(Write(eq), run_time=1.0)
        labels = [(eq[2], "a = −16: gravity pulls down", BAD),
                  (eq[5], "b = 40: initial velocity (ft/s)", GOOD),
                  (eq[8], "c = 25: initial height (ft)", WARN)]
        rows = VGroup()
        for part, s, col in labels:
            rows.add(self.bullet_rows([(s, col)], font_size=21))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(RIGHT * 3.75 + UP * 0.75)
        for (part, _, col), r in zip(labels, rows):
            self.play(part.animate.set_color(col), FadeIn(r, shift=LEFT * 0.2), run_time=0.6)
            self.wait(0.4)
        self.wait(1.0)

        # live readout
        T = ValueTracker(0.0)
        H = lambda t: -16 * t * t + 40 * t + 25
        V = lambda t: 40 - 32 * t
        ball = always_redraw(lambda: Dot(ax.c2p(T.get_value(), H(T.get_value())),
                                         color=ACCENT, radius=0.13))
        path = TracedPath(ball.get_center, stroke_color=WARN, stroke_width=5)
        varrow = always_redraw(lambda: Arrow(
            ax.c2p(T.get_value(), H(T.get_value())),
            ax.c2p(T.get_value(), H(T.get_value())) + UP * V(T.get_value()) * 0.03,
            buff=0, color=GOOD if V(T.get_value()) >= 0 else BAD, stroke_width=5,
            max_tip_length_to_length_ratio=0.35)
            if abs(V(T.get_value())) > 1.2 else VGroup())

        def readline(name, fn, unit, col):
            n = MathTex(name, font_size=34, color=MUTED)
            d = DecimalNumber(fn(0), num_decimal_places=2, font_size=34, color=col)
            u = MathTex(unit, font_size=30, color=MUTED)
            g = VGroup(n, d, u).arrange(RIGHT, buff=0.15)
            d.add_updater(lambda m: m.set_value(fn(T.get_value())))
            u.add_updater(lambda m: m.next_to(d, RIGHT, buff=0.15))
            return g, d
        r_t, d_t = readline("t =", lambda t: t, "\\text{s}", INK)
        r_h, d_h = readline("h =", H, "\\text{ft}", WARN)
        r_v, d_v = readline("v =", V, "\\text{ft/s}", GOOD)
        panel = VGroup(r_t, r_h, r_v).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        panel.move_to(RIGHT * 3.75 + DOWN * 1.05)
        pbox = self.card(panel, pad=0.4)
        self.play(FadeOut(rows), FadeIn(pbox), FadeIn(panel), FadeIn(ball, scale=2), run_time=0.7)
        self.add(path, varrow)

        phase = fit(lbl("Rising: velocity shrinks", GOOD, 22), 5.6).move_to(RIGHT * 3.75 + DOWN * 2.55)
        self.play(FadeIn(phase), run_time=0.3)
        self.play(T.animate.set_value(1.25), run_time=3.2, rate_func=linear)
        vtx = ax.c2p(1.25, 50)
        vring = Circle(radius=0.25, color=ACCENT, stroke_width=4).move_to(vtx)
        vt = MathTex("(1.25,\\ 50)", font_size=30, color=ACCENT).next_to(vtx, UP, buff=0.3)
        p2 = fit(lbl("v = 0 at the vertex: maximum height 50 ft", ACCENT, 22), 5.6).move_to(RIGHT * 3.75 + DOWN * 2.55)
        self.play(Create(vring), Write(vt), Transform(phase, p2), Flash(vtx, color=ACCENT), run_time=0.9)
        self.wait(1.6)
        p3 = fit(lbl("Falling: gravity speeds it up", BAD, 22), 5.6).move_to(RIGHT * 3.75 + DOWN * 2.55)
        self.play(Transform(phase, p3), run_time=0.4)
        tg = (40 + (40 ** 2 + 4 * 16 * 25) ** 0.5) / 32
        self.play(T.animate.set_value(tg), run_time=3.4, rate_func=linear)
        for d in (d_t, d_h, d_v, r_t[2], r_h[2], r_v[2]):
            d.clear_updaters()
        varrow.clear_updaters()
        self.remove(varrow)
        hit = ax.c2p(tg, 0)
        p4 = fit(lbl("Hits the ground after about 3.02 seconds", INK, 22), 5.6).move_to(RIGHT * 3.75 + DOWN * 2.55)
        self.play(Flash(hit, color=WARN), Transform(phase, p4), run_time=0.8)
        self.finish(2.2)


# ======================================================================
# S10 - Domain, range, minimum, maximum
# ======================================================================
class S10DomainRangeMinMax(QScene):
    PART, CHAPTER = 10, "Key Features"

    def build(self, f, yr, center, color):
        ax = Axes(x_range=[-3, 3, 1], y_range=yr, x_length=4.6, y_length=3.5,
                  tips=False, axis_config=dict(color=MUTED, stroke_width=2))
        ax.move_to(center)
        g = ax.plot(f, x_range=[-2.5, 2.5], color=color, stroke_width=5)
        return ax, g

    def construct(self):
        self.add_header("Domain, Range, Minimum and Maximum")
        axL, gL = self.build(lambda x: x * x, [-1, 7, 1], LEFT * 3.4 + UP * 0.75, GOOD)
        axR, gR = self.build(lambda x: -x * x + 4, [-3, 5, 1], RIGHT * 3.4 + UP * 0.75, BAD)
        tL = MathTex("f(x) = x^2", font_size=36, color=GOOD).next_to(axL, UP, buff=0.05)
        tR = MathTex("g(x) = -x^2 + 4", font_size=36, color=BAD).next_to(axR, UP, buff=0.05)
        self.play(Create(axL), Create(axR), run_time=0.8)
        self.play(Create(gL), Create(gR), Write(tL), Write(tR), run_time=1.3)

        # domain arrows on x-axis
        dL = DoubleArrow(axL.c2p(-3, 0), axL.c2p(3, 0), color=PURPLE, buff=0, stroke_width=5,
                         tip_length=0.2)
        dR = DoubleArrow(axR.c2p(-3, 0), axR.c2p(3, 0), color=PURPLE, buff=0, stroke_width=5,
                         tip_length=0.2)
        self.play(GrowFromCenter(dL), GrowFromCenter(dR), run_time=0.8)
        dom = MathTex("\\text{Domain: all real numbers } (-\\infty, \\infty)", font_size=32, color=PURPLE)
        dom.move_to(DOWN * 1.6)
        self.play(Write(dom), run_time=0.9)
        self.wait(1.0)

        # range bars on y-axis
        rL = Arrow(axL.c2p(0, 0), axL.c2p(0, 7), color=ACCENT, buff=0, stroke_width=7,
                   max_tip_length_to_length_ratio=0.08).shift(LEFT * 0.12)
        rR = Arrow(axR.c2p(0, 4), axR.c2p(0, -3), color=ACCENT, buff=0, stroke_width=7,
                   max_tip_length_to_length_ratio=0.08).shift(LEFT * 0.12)
        mL = Dot(axL.c2p(0, 0), color=ACCENT, radius=0.11)
        mR = Dot(axR.c2p(0, 4), color=ACCENT, radius=0.11)
        self.play(GrowArrow(rL), GrowArrow(rR), FadeIn(mL, scale=2), FadeIn(mR, scale=2), run_time=1.0)
        rgL = MathTex("\\text{Range: } y \\ge 0", font_size=30, color=ACCENT)
        rgR = MathTex("\\text{Range: } y \\le 4", font_size=30, color=ACCENT)
        mnL = MathTex("\\text{Minimum: } 0 \\text{ at } (0, 0)", font_size=30, color=GOOD)
        mxR = MathTex("\\text{Maximum: } 4 \\text{ at } (0, 4)", font_size=30, color=BAD)
        VGroup(rgL, mnL).arrange(DOWN, buff=0.18).move_to(LEFT * 3.4 + DOWN * 2.35)
        VGroup(rgR, mxR).arrange(DOWN, buff=0.18).move_to(RIGHT * 3.4 + DOWN * 2.35)
        dom2 = MathTex("\\text{Domain (both): } (-\\infty, \\infty)", font_size=28, color=PURPLE)
        dom2.move_to(DOWN * 1.55)
        self.play(ReplacementTransform(dom, dom2), run_time=0.6)
        self.play(Write(rgL), Write(rgR), run_time=0.8)
        self.play(Write(mnL), Write(mxR), Flash(mL.get_center(), color=GOOD),
                  Flash(mR.get_center(), color=BAD), run_time=0.9)
        tk = self.takeaway("a > 0  →  minimum          a < 0  →  maximum", INK, 23)
        self.wait(0.6)
        self.play(FadeIn(tk), run_time=0.5)
        self.finish(2.4)


# ======================================================================
# S11 - Tables of values with Desmos
# ======================================================================
class S11DesmosTable(QScene):
    PART, CHAPTER = 11, "Desmos Tables"

    def construct(self):
        self.add_header("Build a Table of Values with Desmos")
        # Desmos-style expression list card
        panel = RoundedRectangle(corner_radius=0.18, width=4.9, height=5.2, fill_color=CARD,
                                 fill_opacity=1, stroke_color=EDGE, stroke_width=1.5)
        panel.move_to(LEFT * 3.85 + DOWN * 0.3)
        row1_n = lbl("1", MUTED, 18).move_to(panel.get_corner(UL) + RIGHT * 0.3 + DOWN * 0.45)
        expr = MathTex("f(x) = x^2 - 2x - 3", font_size=36, color=INK)
        expr.next_to(row1_n, RIGHT, buff=0.35)
        sep = Line(panel.get_left() + UP * (row1_n.get_y() - panel.get_y() - 0.45) + RIGHT * 0.05,
                   panel.get_right() + UP * (row1_n.get_y() - panel.get_y() - 0.45) + LEFT * 0.05,
                   color=EDGE)
        row2_n = lbl("2", MUTED, 18).move_to(row1_n.get_center() + DOWN * 0.95)
        self.play(FadeIn(panel), FadeIn(row1_n), run_time=0.5)
        self.play(Write(expr), Create(sep), run_time=1.0)
        self.play(FadeIn(row2_n), run_time=0.3)

        cx, cy = panel.get_x() - 0.75, row2_n.get_y() - 0.1
        hx = MathTex("x_1", font_size=34, color=GOOD).move_to([cx, cy, 0])
        hy = MathTex("f(x_1)", font_size=34, color=ACCENT).move_to([cx + 1.8, cy, 0])
        hl = Line([cx - 0.9, cy - 0.3, 0], [cx + 2.7, cy - 0.3, 0], color=EDGE)
        vl = Line([cx + 0.9, cy + 0.3, 0], [cx + 0.9, cy - 0.3 - 5 * 0.55, 0], color=EDGE)
        self.play(FadeIn(hx), FadeIn(hy), Create(hl), Create(vl), run_time=0.6)

        ax = Axes(x_range=[-3, 5, 1], y_range=[-5, 6, 1], x_length=6.2, y_length=5.0,
                  tips=False, axis_config=dict(color=MUTED, stroke_width=2))
        ax.move_to(RIGHT * 2.95 + DOWN * 0.25)
        nums = VGroup(*[MathTex(str(v), font_size=20, color=MUTED).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                        for v in (-2, -1, 1, 2, 3, 4)],
                      *[MathTex(str(v), font_size=20, color=MUTED).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                        for v in (-4, -2, 2, 4)])
        self.play(Create(ax), FadeIn(nums), run_time=0.8)

        f = lambda x: x * x - 2 * x - 3
        dots = VGroup()
        for i, x in enumerate(range(-1, 4)):
            y = cy - 0.3 - 0.55 * (i + 0.5)
            rx = MathTex(str(x), font_size=32).move_to([cx, y, 0])
            ry = MathTex(str(f(x)), font_size=32, color=ACCENT).move_to([cx + 1.8, y, 0])
            d = Dot(ax.c2p(x, f(x)), color=ACCENT, radius=0.1)
            self.play(FadeIn(rx, shift=RIGHT * 0.1), run_time=0.25)
            self.play(FadeIn(ry, shift=RIGHT * 0.1), TransformFromCopy(ry, d), run_time=0.45)
            dots.add(d)
        g = ax.plot(f, x_range=[-1.75, 3.75], color=WARN, stroke_width=5)
        self.play(Create(g), run_time=1.3)
        vring = Circle(radius=0.25, color=GOOD, stroke_width=4).move_to(ax.c2p(1, -4))
        vlab = MathTex("\\text{minimum } -4 \\text{ at } (1, -4)", font_size=26, color=GOOD)
        vlab.move_to(ax.c2p(1.6, -4.55), aligned_edge=LEFT)
        self.play(Create(vring), Write(vlab), run_time=0.8)
        sym = DashedLine(ax.c2p(1, -4.8), ax.c2p(1, 5.6), color=PURPLE, stroke_width=3)
        self.play(Create(sym), run_time=0.6)
        tk = self.takeaway("Notice the mirror: 0, −3, −4, −3, 0.  Range: y ≥ −4", MUTED, 22)
        self.play(FadeIn(tk), run_time=0.5)
        self.finish(2.4)


# ======================================================================
# S12 - Wrap-up
# ======================================================================
class S12WrapUp(QScene):
    PART, CHAPTER = 12, "Wrap-Up"

    def construct(self):
        self.add_header("Wrap-Up: Welcome, Quadratic Functions!")
        rows = self.bullet_rows([
            ("f(x) = y: the output for each input x", PURPLE),
            ("Standard form: f(x) = ax² + bx + c, with a ≠ 0", ACCENT),
            ("The graph is a symmetrical curve: the parabola", WARN),
            ("Vertex = turning point (minimum or maximum)", ACCENT),
            ("a: up or down, narrow or wide.   c: the y-intercept", GOOD),
            ("Physics: b = initial velocity, gravity bends the path", BAD),
            ("Domain: all real numbers.  Range depends on the vertex", PURPLE),
        ], font_size=24, buff=0.3)
        fit(rows, 12.0)
        rows.move_to(UP * 0.25)
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.25), run_time=0.45)
            self.wait(0.35)
        self.wait(0.8)

        # decorative toss along the bottom
        p0, p1 = LEFT * 5.8 + DOWN * 3.05, RIGHT * 5.8 + DOWN * 3.05
        path = ArcBetweenPoints(p0, p1, angle=-PI / 3.2, color=WARN, stroke_width=3)
        path.set_stroke(opacity=0.0)
        ball = Dot(p0, color=ACCENT, radius=0.1)
        trace = TracedPath(ball.get_center, stroke_color=WARN, stroke_width=3, stroke_opacity=0.7)
        self.add(trace)
        close = Text("Math describes how the world moves.", font_size=26, color=ACCENT,
                     weight=BOLD).move_to(DOWN * 3.0)
        self.play(MoveAlongPath(ball, path), run_time=2.4, rate_func=linear)
        self.play(FadeOut(trace), FadeOut(ball), FadeIn(close, shift=UP * 0.2), run_time=0.8)
        self.finish(2.6)
