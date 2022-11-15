from manim import *
from manim_editor import PresentationSectionType

def make_elements():  # only setting up the mobjects
    dots = VGroup(Dot(), Dot(), Dot(), Dot(), Dot(), Dot(), Dot(), z_index=0)
    dots.arrange(buff=0.7).scale(2).set_color(BLUE)
    dots[0].set_color(ORANGE)
    dots[-1].set_color(ORANGE)
    moving_dot = Dot(color=ORANGE, z_index=1).scale(2.5)
    moving_dot.move_to(dots[0])
    path = VGroup()
    path.add_updater(lambda x: x.become(Line(dots[0], moving_dot, stroke_width=10, z_index=1, color=ORANGE)))
    return dots, moving_dot, path


class MinimalPresentationExample(Scene):
    def construct(self):

        dots, moving_dot, path = make_elements()
        self.add(dots, moving_dot, path)

        self.next_section("A", PresentationSectionType.NORMAL)
        self.play(moving_dot.animate.move_to(dots[1]), rate_func=linear)

        self.next_section("A.1", PresentationSectionType.SUB_NORMAL)
        self.play(moving_dot.animate.move_to(dots[2]), rate_func=linear)

        self.next_section("B", PresentationSectionType.SKIP)
        self.play(moving_dot.animate.move_to(dots[3]), rate_func=linear)

        self.next_section("C", PresentationSectionType.LOOP)
        self.play(moving_dot.animate.move_to(dots[4]), rate_func=linear)

        self.next_section("D", PresentationSectionType.COMPLETE_LOOP)
        self.play(moving_dot.animate.move_to(dots[5]), rate_func=linear)

        self.next_section("E", PresentationSectionType.NORMAL)
        self.play(moving_dot.animate.move_to(dots[6]), rate_func=linear)


class BraceAnnotation(Scene):
    def construct(self):
        
        dot = Dot([-2, -1, 0])
        dot2 = Dot([2, 1, 0])
        line = Line(dot.get_center(), dot2.get_center()).set_color(ORANGE)
        b1 = Brace(line)
        self.add(line, dot, dot2, b1)

        self.next_section("Horizontal distance", PresentationSectionType.NORMAL)
        b1text = b1.get_text("Horizontal distance")
        self.play(Write(b1text))
        

        self.next_section("Diagonal distance", PresentationSectionType.NORMAL)
        b2 = Brace(line, direction=line.copy().rotate(PI / 2).get_unit_vector())
        b2text = b2.get_tex("x-x_1")
        self.play(Create(b2))
        self.play(Write(b2text))


class ArgMinExample(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 10], y_range=[0, 100, 10], axis_config={"include_tip": False}
        )
        labels = ax.get_axis_labels(x_label="x", y_label="f(x)")

        t = ValueTracker(0)

        def func(x):
            return 2 * (x - 5) ** 2
        graph = ax.plot(func, color=MAROON)

        initial_point = [ax.coords_to_point(t.get_value(), func(t.get_value()))]
        dot = Dot(point=initial_point)

        dot.add_updater(lambda x: x.move_to(ax.c2p(t.get_value(), func(t.get_value()))))
        x_space = np.linspace(*ax.x_range[:2],200)
        minimum_index = func(x_space).argmin()

        self.add(ax, labels)
        self.next_section("Axes", PresentationSectionType.NORMAL)

        self.next_section("Function")
        self.play(Create(graph))

        self.next_section("Point")
        self.play(Create(dot))

        self.next_section("Minimum", PresentationSectionType.NORMAL)
        self.play(t.animate.set_value(x_space[minimum_index]))


class FrechetDistanceExample(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 10], y_range=[0, 100, 10], axis_config={"include_tip": False}
        )
        labels = ax.get_axis_labels(x_label="x", y_label="y")

        self.add(ax, labels)
        self.next_section("Axes", PresentationSectionType.NORMAL)
        
        
        x1 = ValueTracker(0)
        x2 = ValueTracker(0)

        def func1(x):
            return 2 * (x - 5) ** 2
        def func2(x):
            return -1.5 * (x - 1) ** 2 + 61.5
        graph1 = ax.plot(func1, color=MAROON)
        graph2 = ax.plot(func2, color=BLUE)

        self.next_section("Function 1")
        self.play(Create(graph1))

        self.next_section("Function 2")
        self.play(Create(graph2))


        initial_point1 = [ax.coords_to_point(x1.get_value(), func1(x1.get_value()))]
        dot1 = Dot(point=initial_point1)
        dot1.add_updater(lambda x: x.move_to(ax.c2p(x1.get_value(), func1(x1.get_value()))))

        initial_point2 = [ax.coords_to_point(x2.get_value(), func2(x2.get_value()))]
        dot2 = Dot(point=initial_point2)
        dot2.add_updater(lambda x: x.move_to(ax.c2p(x2.get_value(), func2(x2.get_value()))))

        self.next_section("Points")
        self.play(Create(dot1), Create(dot2))

        self.next_section("Line")
        line = Line(dot1.get_center(), dot2.get_center()).set_color(ORANGE)
        line.add_updater(lambda z: z.become(Line(dot1.get_center(), dot2.get_center(), color=ORANGE)))
        self.play(Create(line))

        def dist_text():
            d = np.sqrt((x1.get_value() - x2.get_value())**2 + (func1(x1.get_value()) - func2(x2.get_value()))**2)
            return Text(f"{d:.2f}", font_size=0.5 * DEFAULT_FONT_SIZE).next_to(line.get_center(), LEFT)
        dist = dist_text()
        dist.add_updater(lambda t: t.become(dist_text()))
        self.play(Create(dist))
        self.wait(1)

        x_space = np.linspace(*ax.x_range[:2],200)
        minimum_index = func1(x_space).argmin()

        self.next_section("Minimum 1", PresentationSectionType.NORMAL)
        self.play(x1.animate.set_value(x_space[minimum_index]), run_time=2)
        self.wait(1)

        self.next_section("Minimum 2", PresentationSectionType.NORMAL)
        self.play(x2.animate.set_value(x_space[minimum_index]), run_time=2)
        self.wait(1)

        self.next_section("Together to 0", PresentationSectionType.NORMAL)
        self.play(x1.animate.set_value(0), x2.animate.set_value(0), run_time=3, rate_func=linear)
        self.wait(1)

