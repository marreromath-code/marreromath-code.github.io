"""Marrero Math shared base for Manim presentation scenes.

Copy this file into the project folder next to scenes.py and:

    from marrero_manim_base import *

Every scene subclasses MarreroScene. The helpers here carry the design
system (navy background, yellow headers, green=prime/correct,
orange=composite/warning) and the layout conventions that keep 16:9
classroom slides clean: header bar, prompt card, boxed final answers,
left-diagram/right-steps split, and a recursive two-branch tree builder.
"""

import numpy as np
from manim import *

# ---------------------------------------------------------------- palette ---
NAVY = "#0E1B33"      # background
CARD = "#16264A"      # card fill
EDGE = "#2C4270"      # card / rule stroke
INK = "#FFFFFF"       # main text
MUTED = "#9DB2D0"     # secondary text
ACCENT = "#FFD166"    # yellow highlight — headers, answer boxes, key ideas
GOOD = "#38E1B0"      # green — primes, correct answers, checkmarks
WARN = "#FF9E57"      # orange — composites, cautions, second category
BAD = "#FF5C7A"       # red — error marks (Cross), misconceptions
BRANCH = "#5C7BB0"    # tree branches / connector lines

config.background_color = NAVY

MAX_W = 12.6  # safe content width (frame is ~14.2 wide; keep margins)


def fit(m, max_w):
    """Scale a mobject down to max_w if it is too wide. Never rely on
    automatic line wrapping for equations — always fit explicitly."""
    if m.width > max_w:
        m.scale_to_fit_width(max_w)
    return m


class MarreroScene(Scene):
    """Shared header/footer, prompt card, answer box, tree and list helpers."""

    def add_header(self, title):
        t = Text(title, font_size=34, color=ACCENT, weight=BOLD)
        fit(t, MAX_W)
        t.to_edge(UP, buff=0.32)
        line = Line(LEFT * 6.5, RIGHT * 6.5, stroke_width=2, color=EDGE)
        line.next_to(t, DOWN, buff=0.2)
        foot = Text("Marrero Math", font_size=16, color=MUTED)
        foot.to_corner(DR, buff=0.22)
        self.play(FadeIn(t, shift=DOWN * 0.2), Create(line), FadeIn(foot),
                  run_time=0.8)
        self.header_line = line
        return t

    def prompt(self, text_str, font_size=27):
        """One-sentence framing card right under the header."""
        txt = Text(text_str, font_size=font_size, color=INK, line_spacing=0.9)
        fit(txt, 11.6)
        box = RoundedRectangle(corner_radius=0.15, width=txt.width + 0.7,
                               height=txt.height + 0.45, fill_color=CARD,
                               fill_opacity=1, stroke_color=EDGE,
                               stroke_width=1.5)
        txt.move_to(box)
        g = VGroup(box, txt)
        g.next_to(self.header_line, DOWN, buff=0.3)
        self.play(FadeIn(g, shift=UP * 0.1), run_time=0.7)
        return g

    def answer_box(self, mobj):
        """Yellow box around the verified final answer. Every worked
        example should end with exactly one of these."""
        box = SurroundingRectangle(mobj, color=ACCENT, buff=0.22,
                                   corner_radius=0.12, stroke_width=3)
        self.play(Create(box), run_time=0.7)
        return box

    # ---------------------------------------------------------- tree helper
    def play_tree(self, spec, root_pos, x_span=4.0, dy=1.3, scale=1.0,
                  step_time=0.7):
        """Animate a two-branch tree (factor trees, probability trees...).

        spec: int/str (leaf, circled green) or (value, left_spec, right_spec).
        Reveals level by level; leaves get circled green as they appear.
        Returns dict with 'all' group, 'leaves' (VGroups) and 'leaf_vals'.
        """
        nodes = []

        def rec(sp, x, y, span, depth, parent_idx):
            leaf = not isinstance(sp, tuple)
            val = sp if leaf else sp[0]
            label = MathTex(str(val), font_size=int(42 * scale), color=INK)
            label.move_to([x, y, 0])
            ring = None
            if leaf:
                r = max(label.width, label.height) / 2 + 0.17 * scale
                ring = Circle(radius=r, color=GOOD,
                              stroke_width=3.5).move_to(label)
            line = None
            if parent_idx is not None:
                p = nodes[parent_idx]
                top = label.get_top() + UP * (0.28 * scale if leaf else 0.08)
                line = Line(p["label"].get_bottom() + DOWN * 0.08, top,
                            stroke_width=3, color=BRANCH)
            idx = len(nodes)
            nodes.append(dict(val=val, leaf=leaf, label=label, ring=ring,
                              line=line, depth=depth))
            if not leaf:
                rec(sp[1], x - span / 2, y - dy, span / 2, depth + 1, idx)
                rec(sp[2], x + span / 2, y - dy, span / 2, depth + 1, idx)

        rec(spec, root_pos[0], root_pos[1], x_span, 0, None)

        max_depth = max(n["depth"] for n in nodes)
        self.play(Write(nodes[0]["label"]), run_time=step_time)
        for d in range(1, max_depth + 1):
            level = [n for n in nodes if n["depth"] == d]
            anims = []
            for n in level:
                anims.append(Create(n["line"]))
                anims.append(FadeIn(n["label"], shift=DOWN * 0.15))
            self.play(*anims, run_time=step_time)
            rings = [n["ring"] for n in level if n["ring"] is not None]
            if rings:
                self.play(*[Create(r) for r in rings],
                          run_time=step_time * 0.8)

        allm = VGroup(*[m for n in nodes
                        for m in (n["line"], n["label"], n["ring"])
                        if m is not None])
        leaves = [VGroup(n["label"], n["ring"]) for n in nodes if n["leaf"]]
        leaf_vals = [n["val"] for n in nodes if n["leaf"]]
        return dict(all=allm, leaves=leaves, leaf_vals=leaf_vals)

    # ----------------------------------------------------- layout helpers
    def steps_column(self, lines, left_x=2.3, top_y=1.5, gap=0.85,
                     font_size=40, max_w=3.9):
        """Left-aligned MathTex rows for the right-hand worked-steps column
        (diagram on the left, algebra on the right). Returns the mobjects
        WITHOUT playing them so the scene controls pacing."""
        mobs = []
        for i, s in enumerate(lines):
            m = MathTex(s, font_size=font_size, color=INK)
            fit(m, max_w)
            m.move_to([0, top_y - i * gap, 0])
            m.shift(RIGHT * (left_x - m.get_left()[0]))
            mobs.append(m)
        return mobs

    def bullet_rows(self, items, font_size=25, buff=0.4):
        """Rows of (text, color) pairs with colored dots, arranged DOWN and
        left-aligned. Caller positions and plays them."""
        rows = VGroup()
        for s, c in items:
            dot = Dot(color=c, radius=0.09)
            t = Text(s, font_size=font_size, color=INK)
            t.next_to(dot, RIGHT, buff=0.25)
            rows.add(VGroup(dot, t))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=buff)
        return rows

    def hold(self, t=1.5):
        self.wait(t)
