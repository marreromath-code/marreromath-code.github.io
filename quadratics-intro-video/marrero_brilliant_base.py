"""Marrero Math light theme for Manim lessons (Brilliant-inspired layout).

Colors and fonts come from the Marrero Math website (cream / navy / gold,
Fraunces headings + Inter body). Layout patterns are inspired by interactive
lesson apps: a top progress bar, left-aligned lesson title, white cards,
live sliders with a value bubble, navy-header tables, algebra tiles,
pause-and-predict option cards, and Correct / Incorrect feedback banners.

    from marrero_brilliant_base import *
    class S01Something(LessonScene): PART = 1 ...
"""

import numpy as np
from manim import *

# ----------------------------------------------------------------- palette ---
BG = "#F9F7F2"          # cream canvas (website --cream)
CARD = "#FFFFFF"
EDGE = "#E3DDCD"        # website --line
GRID = "#ECE6D8"
INK = "#1A2744"         # website --navy
NAVY_SOFT = "#2D3F6E"   # website --navy-soft
MUTED = "#5A5A7A"       # website --muted
GOLD = "#B8960C"        # website --gold
GOLD_TXT = "#8F7400"    # darker gold for small text on cream
GOLD_FILL = "#F7EBB5"
GREEN = "#1E9E5A"
GREEN_DARK = "#157A45"
GREEN_FILL = "#DDF3E6"
CORAL = "#E07A52"       # website --coral
RED = "#D6455D"
YELLOW_FILL = "#FBE9A9"
PURPLE = "#6C4FD8"
BLUE = "#3F63D8"
TILE_X2 = "#5B7BEA"
TILE_X = "#AFC0F7"
TILE_1 = "#F0D060"

HEAD_FONT = "Fraunces"
BODY_FONT = "Inter"

config.background_color = BG
Text.set_default(font=BODY_FONT, color=INK)
MathTex.set_default(color=INK)

TOTAL_PARTS = 12
TITLE_Y = 2.85
BOTTOM_Y = -3.42


def fit(m, max_w):
    if m.width > max_w:
        m.scale_to_fit_width(max_w)
    return m


def heading(s, size=36, color=INK):
    return Text(s, font=HEAD_FONT, weight=BOLD, font_size=size, color=color)


def body(s, size=24, color=INK, bold=False):
    return Text(s, font=BODY_FONT, font_size=size, color=color,
                weight=BOLD if bold else NORMAL)


def card(w, h, fill=CARD, stroke=EDGE, r=0.2, shadow=True, stroke_width=1.6):
    rect = RoundedRectangle(corner_radius=r, width=w, height=h, fill_color=fill,
                            fill_opacity=1, stroke_color=stroke,
                            stroke_width=stroke_width)
    if not shadow:
        return VGroup(rect)
    sh = RoundedRectangle(corner_radius=r, width=w, height=h, fill_color=EDGE,
                          fill_opacity=0.55, stroke_width=0).shift(DOWN * 0.07)
    return VGroup(sh, rect)


def pill(label, fill, txt, w=None, h=0.56, size=20, stroke=None):
    t = Text(label, font=BODY_FONT, font_size=size, color=txt, weight=BOLD)
    w = w or t.width + 0.8
    r = RoundedRectangle(corner_radius=h / 2, width=w, height=h, fill_color=fill,
                         fill_opacity=1, stroke_width=0 if stroke is None else 2,
                         stroke_color=stroke or fill)
    t.move_to(r)
    return VGroup(r, t)


def check_icon(color=GREEN, r=0.2, fg=WHITE):
    c = Circle(radius=r, fill_color=color, fill_opacity=1, stroke_width=0)
    m = VMobject(stroke_color=fg, stroke_width=4.5 * r / 0.2).set_points_as_corners(
        [c.get_center() + np.array([-0.48, 0.02, 0]) * r,
         c.get_center() + np.array([-0.12, -0.36, 0]) * r,
         c.get_center() + np.array([0.5, 0.36, 0]) * r])
    return VGroup(c, m)


def x_icon(color=RED, r=0.2, fg=WHITE):
    c = Circle(radius=r, fill_color=color, fill_opacity=1, stroke_width=0)
    k = 0.38 * r
    a = Line(c.get_center() + np.array([-k, -k, 0]), c.get_center() + np.array([k, k, 0]),
             stroke_color=fg, stroke_width=4.5 * r / 0.2)
    b = Line(c.get_center() + np.array([-k, k, 0]), c.get_center() + np.array([k, -k, 0]),
             stroke_color=fg, stroke_width=4.5 * r / 0.2)
    return VGroup(c, a, b)


def lesson_axes(x_range, y_range, x_length, y_length):
    return Axes(x_range=x_range, y_range=y_range, x_length=x_length,
                y_length=y_length, tips=False,
                axis_config=dict(color=NAVY_SOFT, stroke_width=2.2, tick_size=0.06))


def axis_numbers(ax, xs=(), ys=(), size=20):
    g = VGroup()
    for v in xs:
        g.add(MathTex(str(v), font_size=size, color=MUTED).next_to(ax.c2p(v, 0), DOWN, buff=0.12))
    for v in ys:
        g.add(MathTex(str(v), font_size=size, color=MUTED).next_to(ax.c2p(0, v), LEFT, buff=0.1))
    return g


class LessonScene(Scene):
    PART = 0
    cont_btn = None

    # ---------------------------------------------------------- chrome
    def lesson_header(self, title, subtitle=None):
        y = 3.58
        x0, x1 = -4.4, 3.6
        track = RoundedRectangle(corner_radius=0.08, width=x1 - x0, height=0.16,
                                 fill_color=EDGE, fill_opacity=1, stroke_width=0)
        track.move_to([(x0 + x1) / 2, y, 0])
        dots = VGroup(*[Dot([x1 + 0.32 + 0.3 * i, y, 0], radius=0.075, color=EDGE)
                        for i in range(3)])
        tr = ValueTracker(max(self.PART - 1, 0) / TOTAL_PARTS)

        def bar():
            w = max((x1 - x0) * tr.get_value(), 0.16)
            return RoundedRectangle(corner_radius=0.08, width=w, height=0.16,
                                    fill_color=GREEN, fill_opacity=1,
                                    stroke_width=0).move_to([x0 + w / 2, y, 0])
        fill = always_redraw(bar)
        part = body(f"PART {self.PART}", 16, MUTED, bold=True).move_to([-6.15, y, 0])
        mark = heading("Marrero Math", 20, GOLD).move_to([5.75, y, 0])
        t = heading(title, 36)
        fit(t, 12.6)
        t.move_to([0, TITLE_Y, 0]).to_edge(LEFT, buff=0.7)
        self.add(track, dots, fill, part, mark)
        anims = [FadeIn(t, shift=UP * 0.15), tr.animate.set_value(self.PART / TOTAL_PARTS)]
        sub = None
        if subtitle:
            sub = body(subtitle, 22, MUTED)
            fit(sub, 12.6)
            sub.next_to(t, DOWN, buff=0.15, aligned_edge=LEFT)
            anims.append(FadeIn(sub, shift=UP * 0.1))
        self.play(*anims, run_time=0.9)
        self.title_mob = t
        return t

    def note(self, s, color=MUTED, size=22, y=-2.7):
        t = body(s, size, color)
        fit(t, 12.4)
        t.move_to([0, y, 0])
        return t

    def press(self, btn):
        self.play(btn.animate.scale(0.92), run_time=0.12)
        self.play(btn.animate.scale(1 / 0.92), run_time=0.14)

    def finish(self, wait=1.5, button=True):
        if button and self.cont_btn is None:
            b = pill("Continue", INK, WHITE, w=3.4, h=0.62, size=22)
            b.move_to([0, BOTTOM_Y, 0])
            self.play(FadeIn(b, shift=UP * 0.2), run_time=0.4)
            self.cont_btn = b
        self.wait(wait)
        if button:
            self.press(self.cont_btn)
        for m in self.mobjects:
            m.clear_updaters()
        self.mobjects = [m for m in self.mobjects
                         if len(m.family_members_with_points()) > 0]
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        self.cont_btn = None

    # ------------------------------------------------------- feedback
    def banner_correct(self, msg="Correct!", sub=None):
        panel = Rectangle(width=14.4, height=1.2, fill_color=GREEN_FILL,
                          fill_opacity=1, stroke_width=0).move_to([0, BOTTOM_Y, 0])
        ic = check_icon(GREEN, 0.24).move_to([-5.9, BOTTOM_Y, 0])
        t = body(msg, 26, GREEN_DARK, bold=True).next_to(ic, RIGHT, buff=0.25)
        g = VGroup(panel, ic, t)
        if sub:
            s = body(sub, 20, GREEN_DARK)
            fit(s, 5.6)
            s.next_to(t, RIGHT, buff=0.35)
            g.add(s)
        why = pill("Why?", "#C3E7D1", GREEN_DARK, w=1.5).move_to([3.15, BOTTOM_Y, 0])
        cont = pill("Continue", GREEN, WHITE, w=2.5).move_to([5.3, BOTTOM_Y, 0])
        g.add(why, cont)
        self.play(FadeIn(g, shift=UP * 0.35), run_time=0.5)
        self.cont_btn, self.why_btn, self.banner = cont, why, g
        return g

    def banner_incorrect(self, msg="Incorrect."):
        panel = Rectangle(width=14.4, height=1.2, fill_color=YELLOW_FILL,
                          fill_opacity=1, stroke_width=0).move_to([0, BOTTOM_Y, 0])
        ic = x_icon(RED, 0.24).move_to([-5.9, BOTTOM_Y, 0])
        t = body(msg, 26, INK, bold=True).next_to(ic, RIGHT, buff=0.25)
        again = pill("Try again", INK, WHITE, w=2.2).move_to([2.9, BOTTOM_Y, 0])
        see = pill("See answer", "#EAD58A", INK, w=2.4).move_to([5.35, BOTTOM_Y, 0])
        g = VGroup(panel, ic, t, again, see)
        self.play(FadeIn(g, shift=UP * 0.35), run_time=0.5)
        self.see_btn, self.banner = see, g
        return g

    def why_card(self, title, lines, width=8.4):
        """Explanation modal over a dimmed lesson (press 'Why?' first)."""
        dim = Rectangle(width=15, height=8.2, fill_color=BG, fill_opacity=0.82,
                        stroke_width=0)
        content = VGroup(*lines).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        head = heading(title, 28)
        inner = VGroup(head, content).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        fit(inner, width - 1.0)
        box = card(width, inner.height + 0.9)
        box.move_to(UP * 0.2)
        inner.move_to(box)
        close = x_icon(MUTED, 0.16, WHITE).move_to(box[1].get_corner(UR) + np.array([-0.4, -0.4, 0]))
        g = VGroup(dim, box, inner, close)
        self.play(FadeIn(dim), FadeIn(box, shift=UP * 0.2), FadeIn(inner, shift=UP * 0.2),
                  FadeIn(close), run_time=0.6)
        return g

    # ------------------------------------------------ pause & predict
    def predict(self, question, options, correct, center=ORIGIN, layout="row",
                card_w=3.3, card_h=1.1, hold=3, chip_pos=None):
        """Question + option cards + 3-second countdown, then reveal.

        question: mobject; options: list of mobjects; returns dict of parts.
        """
        chip = pill("PAUSE & PREDICT", GOLD_FILL, GOLD_TXT, size=16, h=0.42)
        cards = VGroup()
        for o in options:
            c = card(card_w, card_h)
            fit(o, card_w - 0.4)
            o.move_to(c)
            cards.add(VGroup(c, o))
        if layout == "row":
            cards.arrange(RIGHT, buff=0.35)
        else:
            cards.arrange(DOWN, buff=0.25)
        block = VGroup(chip, question, cards).arrange(DOWN, buff=0.35)
        block.move_to(center)
        if chip_pos is not None:
            chip.move_to(chip_pos)
        self.play(FadeIn(chip, shift=DOWN * 0.1), FadeIn(question, shift=UP * 0.1), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.15),
                  run_time=0.8)

        # countdown ring
        tr = ValueTracker(1.0)
        ring_c = cards.get_bottom() + DOWN * 0.55
        bg_ring = Circle(radius=0.26, stroke_color=EDGE, stroke_width=5).move_to(ring_c)
        arc = always_redraw(lambda: Arc(radius=0.26, start_angle=PI / 2,
                                        angle=-TAU * max(tr.get_value(), 0.001),
                                        stroke_color=GOLD, stroke_width=5).move_to(ring_c)
                            .shift(0 * UP))
        num = Integer(hold, font_size=26, color=INK).move_to(ring_c)
        num.add_updater(lambda m: m.set_value(int(np.ceil(max(tr.get_value(), 0.0001) * hold))).move_to(ring_c))
        lab = body("Pause the video and choose", 18, MUTED).next_to(bg_ring, RIGHT, buff=0.25)
        timer = VGroup(bg_ring, arc, num, lab)
        self.play(FadeIn(bg_ring), FadeIn(arc), FadeIn(num), FadeIn(lab), run_time=0.3)
        self.play(tr.animate.set_value(0), run_time=hold, rate_func=linear)
        num.clear_updaters()
        arc.clear_updaters()
        self.play(FadeOut(timer), run_time=0.3)

        # reveal
        good = cards[correct]
        badge = check_icon(GREEN, 0.2).move_to(good[0][1].get_corner(UR) + np.array([-0.05, -0.05, 0]))
        anims = [good[0][1].animate.set_stroke(GREEN, width=4).set_fill(GREEN_FILL),
                 FadeIn(badge, scale=1.6)]
        for i, c in enumerate(cards):
            if i != correct:
                anims.append(c.animate.set_opacity(0.4))
        self.play(*anims, run_time=0.6)
        return dict(chip=chip, question=question, cards=cards, badge=badge,
                    all=VGroup(chip, question, cards, badge))

    # --------------------------------------------------------- slider
    def slider(self, tracker, vmin, vmax, center, width=4.4, color=CORAL,
               label=None, decimals=1, end_labels=True):
        left = np.array(center) + LEFT * width / 2

        def xpos(v):
            return left + RIGHT * width * (v - vmin) / (vmax - vmin)
        track = RoundedRectangle(corner_radius=0.06, width=width, height=0.12,
                                 fill_color=EDGE, fill_opacity=1, stroke_width=0).move_to(center)
        g = VGroup(track)
        if end_labels:
            for v in (vmin, vmax):
                g.add(MathTex(f"{v:g}", font_size=24, color=MUTED).next_to(xpos(v), DOWN, buff=0.22))
        if label is not None:
            lab = MathTex(label, font_size=36, color=INK).next_to(track, LEFT, buff=0.35)
            g.add(lab)
        knob = always_redraw(lambda: Circle(radius=0.17, fill_color=color, fill_opacity=1,
                                            stroke_color=WHITE, stroke_width=4)
                             .move_to(xpos(tracker.get_value())))

        def bubble():
            n = DecimalNumber(tracker.get_value(), num_decimal_places=decimals,
                              font_size=24, color=WHITE)
            r = RoundedRectangle(corner_radius=0.08, width=n.width + 0.3, height=0.42,
                                 fill_color=INK, fill_opacity=1, stroke_width=0)
            n.move_to(r)
            return VGroup(r, n).next_to(xpos(tracker.get_value()), UP, buff=0.28)
        bub = always_redraw(bubble)
        g.add(knob, bub)
        return g

    # ------------------------------------------------- graph + table
    def graph_card(self, ax, pad=0.32, grid=True):
        xr, yr = ax.x_range, ax.y_range
        c = card(ax.x_length + 2 * pad, ax.y_length + 2 * pad, r=0.22)
        c.move_to(ax.c2p((xr[0] + xr[1]) / 2, (yr[0] + yr[1]) / 2))
        g = VGroup(c)
        if grid:
            lines = VGroup()
            for x in np.arange(xr[0], xr[1] + 1e-9, xr[2]):
                lines.add(Line(ax.c2p(x, yr[0]), ax.c2p(x, yr[1]), stroke_color=GRID, stroke_width=1.5))
            for y in np.arange(yr[0], yr[1] + 1e-9, yr[2]):
                lines.add(Line(ax.c2p(xr[0], y), ax.c2p(xr[1], y), stroke_color=GRID, stroke_width=1.5))
            g.add(lines)
        return g

    def table_frame(self, headers, nrows, top_left, colw=1.5, rowh=0.52, size=30):
        """Navy header row + white bordered cells. Returns (frame, header_mobs,
        cell_center(r, c) function)."""
        x0, y0 = top_left
        ncol = len(headers)
        frame = VGroup()
        hdr = Rectangle(width=colw * ncol, height=rowh, fill_color=INK, fill_opacity=1,
                        stroke_color=INK, stroke_width=1.5)
        hdr.move_to([x0 + colw * ncol / 2, y0 - rowh / 2, 0])
        frame.add(hdr)
        hm = VGroup()
        for j, h in enumerate(headers):
            m = MathTex(h, font_size=size, color=WHITE)
            m.move_to([x0 + colw * (j + 0.5), y0 - rowh / 2, 0])
            hm.add(m)
        for i in range(nrows):
            for j in range(ncol):
                r = Rectangle(width=colw, height=rowh, fill_color=CARD, fill_opacity=1,
                              stroke_color=EDGE, stroke_width=1.5)
                r.move_to([x0 + colw * (j + 0.5), y0 - rowh * (i + 1.5), 0])
                frame.add(r)

        def cell(i, j):
            return np.array([x0 + colw * (j + 0.5), y0 - rowh * (i + 1.5), 0])
        return frame, hm, cell

    # ---------------------------------------------------------- tiles
    @staticmethod
    def tile_x2(s=1.25):
        sq = Square(side_length=s, fill_color=TILE_X2, fill_opacity=1, stroke_color=WHITE, stroke_width=3)
        sq.add(MathTex("x^2", font_size=34, color=WHITE).move_to(sq))
        return sq

    @staticmethod
    def tile_x(s=1.25, u=0.32):
        r = Rectangle(width=u, height=s, fill_color=TILE_X, fill_opacity=1, stroke_color=WHITE, stroke_width=3)
        r.add(MathTex("x", font_size=24, color=INK).move_to(r))
        return r

    @staticmethod
    def tile_1(u=0.32):
        return Square(side_length=u, fill_color=TILE_1, fill_opacity=1, stroke_color=WHITE, stroke_width=3)
