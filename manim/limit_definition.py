"""
The Definition of a Limit  —  a Manim scene in the 3Blue1Brown style.

Goal
----
Help a calculus student feel the CORE of the limit idea by weaving together:

  * the CONCEPTUAL idea  — "as x gets close to c, f(x) gets close to L,"
                           shown with a moving point and a hole in the graph;
  * the PROCEDURAL idea  — the formal epsilon-delta "challenge / response"
                           game that makes the word "close" precise.

The running example is the classic removable hole

        f(x) = (x^2 - 1) / (x - 1)  =  x + 1   (for x != 1),

which is UNDEFINED at x = 1 yet has a perfectly good limit of 2 there.
That single picture is the whole reason limits exist, so the scene is built
around it.

Render (Manim Community v0.18+):

    manim -pqh limit_definition.py LimitDefinition      # high quality preview
    manim -pqk limit_definition.py LimitDefinition      # 4k

Requires a LaTeX installation for the MathTex labels.
"""

from manim import *


# --- 3Blue1Brown-flavoured palette -----------------------------------------
BG       = "#000000"     # pure black background
CURVE    = "#3FA9F5"     # the signature "3blue"
TARGET   = "#FFD86E"     # warm yellow for the limit value L
EPS_CLR  = "#7FE0A0"     # green  — the epsilon (output) tolerance
DEL_CLR  = "#FF8A8A"     # red    — the delta   (input)  tolerance
GHOST    = "#5A6173"     # muted grey for de-emphasised text


class LimitDefinition(Scene):
    def construct(self):
        self.camera.background_color = BG

        self.opening()          # 1. the puzzle: 0/0 at x = 1
        self.intuitive_graph()  # 2. conceptual: approach the hole, numbers home in
        self.formal_game()      # 3. procedural: the epsilon-delta challenge
        self.closing()          # 4. tie both ideas together

    # ------------------------------------------------------------------ #
    # 1. The puzzle                                                       #
    # ------------------------------------------------------------------ #
    def opening(self):
        title = Text("What is a limit?", font="sans-serif", weight=BOLD)
        title.scale(1.1).to_edge(UP, buff=1.0)

        f = MathTex(r"f(x)=\frac{x^{2}-1}{x-1}").scale(1.3)

        self.play(FadeIn(title, shift=DOWN * 0.3))
        self.play(Write(f))
        self.wait(0.5)

        # Try to plug in x = 1 ... and break.
        sub = MathTex(r"f(1)=\frac{1-1}{1-1}=\frac{0}{0}").scale(1.3)
        sub.move_to(f)
        undefined = Text("undefined", color=DEL_CLR, font="sans-serif")
        undefined.scale(0.7).next_to(sub, DOWN, buff=0.6)

        self.play(TransformMatchingShapes(f, sub))
        self.play(FadeIn(undefined, shift=UP * 0.2))
        self.wait(0.8)

        # The reframing question — we don't ask about x = 1, but NEAR it.
        question = Text("...so look at what happens NEAR x = 1",
                        font="sans-serif", color=TARGET).scale(0.7)
        question.next_to(undefined, DOWN, buff=0.5)
        self.play(FadeIn(question, shift=UP * 0.2))
        self.wait(1.0)

        self.play(
            *[FadeOut(m) for m in (title, sub, undefined, question)]
        )

    # ------------------------------------------------------------------ #
    # 2. The conceptual picture + the numbers homing in                  #
    # ------------------------------------------------------------------ #
    def intuitive_graph(self):
        c, L = 1.0, 2.0
        func = lambda x: x + 1            # f(x) = (x^2-1)/(x-1) simplified

        axes = Axes(
            x_range=[-1, 3, 1],
            y_range=[-1, 4, 1],
            x_length=7.5,
            y_length=5.2,
            axis_config={"include_tip": True, "stroke_color": GHOST},
            tips=True,
        ).to_edge(LEFT, buff=0.8)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        graph = axes.plot(func, x_range=[-1, 3], color=CURVE, stroke_width=5)

        # The hole: a black-filled circle ringed in the curve colour.
        hole = Circle(radius=0.09, color=CURVE, stroke_width=4)
        hole.set_fill(BG, opacity=1).move_to(axes.c2p(c, L))

        self.play(Create(axes), FadeIn(axes_labels))
        self.play(Create(graph), run_time=1.5)
        self.play(GrowFromCenter(hole))

        # Mark the target limit L = 2 on the y-axis.
        L_line = DashedLine(axes.c2p(0, L), axes.c2p(c, L),
                            color=TARGET, stroke_width=2, dash_length=0.12)
        L_dot  = Dot(axes.c2p(0, L), color=TARGET, radius=0.05)
        L_lbl  = MathTex("L=2", color=TARGET).scale(0.8).next_to(L_dot, LEFT, buff=0.15)
        self.play(Create(L_line), FadeIn(L_dot), Write(L_lbl))
        self.wait(0.3)

        # ---- a live point that slides toward the hole, numbers updating ----
        t = ValueTracker(-0.2)

        moving_dot = always_redraw(
            lambda: Dot(axes.c2p(t.get_value(), func(t.get_value())),
                        color=WHITE, radius=0.07)
        )
        # dashed guide lines from the moving point to both axes
        v_line = always_redraw(
            lambda: axes.get_vertical_line(
                axes.c2p(t.get_value(), func(t.get_value())),
                color=GHOST, stroke_width=2)
        )

        # the read-out panel on the right
        x_read = always_redraw(
            lambda: VGroup(
                MathTex("x="),
                DecimalNumber(t.get_value(), num_decimal_places=3, color=DEL_CLR),
            ).arrange(RIGHT, buff=0.12)
        )
        f_read = always_redraw(
            lambda: VGroup(
                MathTex("f(x)="),
                DecimalNumber(func(t.get_value()), num_decimal_places=3, color=EPS_CLR),
            ).arrange(RIGHT, buff=0.12)
        )
        panel = VGroup(x_read, f_read).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        panel.to_edge(RIGHT, buff=0.9).shift(UP * 0.5)
        panel_box = always_redraw(
            lambda: SurroundingRectangle(panel, color=GHOST, buff=0.35)
        )

        self.play(FadeIn(moving_dot), Create(v_line),
                  FadeIn(panel), Create(panel_box))

        # approach from the LEFT, stopping just shy of the hole
        self.play(t.animate.set_value(0.985), run_time=3, rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.4)
        # jump to the right side and approach back toward the hole
        self.play(t.animate.set_value(2.2), run_time=0.6, rate_func=linear)
        self.play(t.animate.set_value(1.015), run_time=3, rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.5)

        # the verbal takeaway
        idea = VGroup(
            Text("As x → 1,", font="sans-serif").set_color(DEL_CLR),
            Text("f(x) → 2", font="sans-serif").set_color(EPS_CLR),
        ).arrange(RIGHT, buff=0.25).scale(0.8)
        idea.next_to(panel_box, DOWN, buff=0.6)
        self.play(Write(idea))
        self.wait(0.6)

        limit_stmt = MathTex(r"\lim_{x\to 1}\frac{x^{2}-1}{x-1}=2").scale(0.85)
        limit_stmt.next_to(idea, DOWN, buff=0.5)
        self.play(Write(limit_stmt))
        self.wait(1.2)

        # keep the axes/graph/hole/L for the formal section; clear the rest
        self.intuition_keep = VGroup(axes, axes_labels, graph, hole,
                                     L_line, L_dot, L_lbl)
        self.play(
            FadeOut(moving_dot), FadeOut(v_line), FadeOut(panel),
            FadeOut(panel_box), FadeOut(idea), FadeOut(limit_stmt),
        )

    # ------------------------------------------------------------------ #
    # 3. The procedural heart: the epsilon-delta game                    #
    # ------------------------------------------------------------------ #
    def formal_game(self):
        axes, axes_labels, graph, hole, L_line, L_dot, L_lbl = self.intuition_keep
        c, L = 1.0, 2.0

        # slide the existing graph left to make room for the formal text
        keep = self.intuition_keep
        self.play(keep.animate.scale(0.92).to_edge(LEFT, buff=0.4))

        heading = Text("Making “close” precise",
                       font="sans-serif", weight=BOLD, color=TARGET).scale(0.6)
        heading.to_corner(UR, buff=0.6)
        self.play(FadeIn(heading, shift=DOWN * 0.2))

        # --- epsilon: the challenge (a tolerance band around L) ---
        eps = ValueTracker(0.9)

        def hband():
            e = eps.get_value()
            return Rectangle(
                width=axes.x_length,
                height=abs(axes.c2p(0, L + e)[1] - axes.c2p(0, L - e)[1]),
                stroke_width=0,
            ).set_fill(EPS_CLR, opacity=0.20).move_to(axes.c2p(c, L))

        def hlines():
            e = eps.get_value()
            top = DashedLine(axes.c2p(-1, L + e), axes.c2p(3, L + e),
                             color=EPS_CLR, stroke_width=2)
            bot = DashedLine(axes.c2p(-1, L - e), axes.c2p(3, L - e),
                             color=EPS_CLR, stroke_width=2)
            return VGroup(top, bot)

        eps_band  = always_redraw(hband)
        eps_lines = always_redraw(hlines)

        eps_brace = always_redraw(
            lambda: BraceBetweenPoints(
                axes.c2p(c, L), axes.c2p(c, L + eps.get_value()),
                direction=RIGHT, color=EPS_CLR
            ).set_stroke(width=1)
        )
        eps_lbl = always_redraw(
            lambda: MathTex(r"\varepsilon", color=EPS_CLR).scale(0.8)
            .next_to(axes.c2p(c, L + eps.get_value() / 2), RIGHT, buff=0.45)
        )

        challenge = Text("CHALLENGE:  trap f(x) within ε of L",
                         font="sans-serif", color=EPS_CLR).scale(0.42)
        challenge.next_to(heading, DOWN, buff=0.45).align_to(heading, RIGHT)

        self.play(FadeIn(challenge, shift=DOWN * 0.1))
        self.play(FadeIn(eps_band), Create(eps_lines),
                  FadeIn(eps_brace), Write(eps_lbl))
        self.wait(0.6)

        # --- delta: the response (an input window around c) ---
        # For slope-1 line through the hole, delta = epsilon works exactly.
        def delta_of(e):
            return e

        def vband():
            d = delta_of(eps.get_value())
            return Rectangle(
                width=abs(axes.c2p(c + d, 0)[0] - axes.c2p(c - d, 0)[0]),
                height=axes.y_length,
                stroke_width=0,
            ).set_fill(DEL_CLR, opacity=0.18).move_to(axes.c2p(c, L)).set_y(axes.c2p(0, 1.5)[1])

        def vlines():
            d = delta_of(eps.get_value())
            left  = DashedLine(axes.c2p(c - d, -1), axes.c2p(c - d, 4),
                               color=DEL_CLR, stroke_width=2)
            right = DashedLine(axes.c2p(c + d, -1), axes.c2p(c + d, 4),
                               color=DEL_CLR, stroke_width=2)
            return VGroup(left, right)

        del_band  = always_redraw(vband)
        del_lines = always_redraw(vlines)
        del_brace = always_redraw(
            lambda: BraceBetweenPoints(
                axes.c2p(c, -0.6), axes.c2p(c + delta_of(eps.get_value()), -0.6),
                direction=DOWN, color=DEL_CLR
            ).set_stroke(width=1)
        )
        del_lbl = always_redraw(
            lambda: MathTex(r"\delta", color=DEL_CLR).scale(0.8)
            .next_to(axes.c2p(c + delta_of(eps.get_value()) / 2, -0.6), DOWN, buff=0.25)
        )

        response = Text("RESPONSE:  choose a window δ around c",
                        font="sans-serif", color=DEL_CLR).scale(0.42)
        response.next_to(challenge, DOWN, buff=0.3).align_to(challenge, RIGHT)

        self.play(FadeIn(response, shift=DOWN * 0.1))
        self.play(FadeIn(del_band), Create(del_lines),
                  FadeIn(del_brace), Write(del_lbl))
        self.wait(0.8)

        # --- the formal statement, built piece by piece ---
        formal = MathTex(
            r"\forall\,\varepsilon>0",
            r"\;\;\exists\,\delta>0",
            r"\;:\;",
            r"0<|x-1|<\delta",
            r"\;\Rightarrow\;",
            r"|f(x)-2|<\varepsilon",
        ).scale(0.62)
        formal[0].set_color(EPS_CLR)
        formal[1].set_color(DEL_CLR)
        formal[3].set_color(DEL_CLR)
        formal[5].set_color(EPS_CLR)
        formal.next_to(response, DOWN, buff=0.7).align_to(heading, RIGHT)

        self.play(Write(formal), run_time=2)
        self.wait(0.8)

        # --- the punchline: shrink the challenge, the response keeps up ---
        squeeze = Text("No matter how small ε gets, a δ still works.",
                       font="sans-serif", color=WHITE).scale(0.42)
        squeeze.next_to(formal, DOWN, buff=0.6).align_to(heading, RIGHT)
        self.play(FadeIn(squeeze, shift=UP * 0.1))

        self.play(eps.animate.set_value(0.45), run_time=1.6,
                  rate_func=rate_functions.ease_in_out_sine)
        self.play(eps.animate.set_value(0.18), run_time=1.6,
                  rate_func=rate_functions.ease_in_out_sine)
        self.play(eps.animate.set_value(0.30), run_time=1.2,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(1.0)

        self.formal_mobjects = VGroup(
            heading, challenge, response, formal, squeeze,
            eps_band, eps_lines, eps_brace, eps_lbl,
            del_band, del_lines, del_brace, del_lbl,
        )

    # ------------------------------------------------------------------ #
    # 4. Bring it home                                                   #
    # ------------------------------------------------------------------ #
    def closing(self):
        self.play(FadeOut(self.formal_mobjects), FadeOut(self.intuition_keep))

        line1 = Text("A limit is a destination,", font="sans-serif").scale(0.8)
        line2 = Text("not a stop along the way.", font="sans-serif",
                     color=TARGET).scale(0.8)
        lines = VGroup(line1, line2).arrange(DOWN, buff=0.35)

        stmt = MathTex(r"\lim_{x\to c} f(x) = L").scale(1.4)
        group = VGroup(lines, stmt).arrange(DOWN, buff=0.9)

        self.play(Write(lines))
        self.wait(0.4)
        self.play(FadeIn(stmt, shift=UP * 0.3))
        self.wait(1.5)
        self.play(FadeOut(group))
