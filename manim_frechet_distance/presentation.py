from manim import *
from manim_editor import PresentationSectionType
from scipy import optimize
from scipy.spatial.distance import directed_hausdorff

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

class HausdorffDistance(Scene):
    def construct(self):
        title = Text("Distance of Curves", color=BLUE).to_edge(UP)
        self.add(title)


        # p11a = np.array([0, 3, 0])
        # p11h = np.array([1, 0, 0])
        # p12a = np.array([3, 0, 0])
        # p12h = np.array([0, 1, 0])
        # bezier1 = CubicBezier(p11a, p11a + 2* p11h, p12a + 2* p12h, p12a)


        # p21a = p12a
        # p21h = np.array([0, -1, 0])
        # p22a = np.array([0, -3, 0])
        # p22h = np.array([1, 0, 0])
        # bezier2 = CubicBezier(p21a, p21a + 2* p21h, p22a + 2* p22h, p22a)

        # p1 = np.array([-3, 1, 0])
        # p1b = p1 + [1, 0, 0]
        # d1 = Dot(point=p1).set_color(BLUE)
        # l1 = Line(p1, p1b)
        # p2 = np.array([3, -1, 0])
        # p2b = p2 - [1, 0, 0]
        # d2 = Dot(point=p2).set_color(RED)
        # l2 = Line(p2, p2b)
        # bezier2 = CubicBezier(p1b, p1b + 3 * RIGHT, p2b - 3 * RIGHT, p2b)

        # circle = Circle(2)
        # self.play(Create(circle))
        # self.play(Create(bezier1))
        # self.play(Create(bezier2))


        # bezier = Group(bezier1, bezier2)
        # point = Dot().move_to(bezier.point_from_proportion(0))
        # alpha = ValueTracker(0)
        # point.add_updater(lambda m: m.move_to(bezier.point_from_proportion(alpha.get_value())))
        # self.add(bezier, point)
        # self.play(alpha.animate.set_value(1), run_time=3)

        # square = RoundedRectangle(0.5, width=4, height=4).rotate(45)
        # self.play(Create(square))

        # q_square = RoundedRectangle(0.5, width=4, height=4, color=GREEN).rotate(45)
        # self.play(ReplacementTransform(square, q_square))

        # p_square = RoundedRectangle(0.5, width=5, height=5, color=RED).rotate(45)
        # self.play(Transform(q_square.copy(), p_square))

        q_curve = Polygon([0, 2.5, 0], [2.5,0,0], [0,-3,0], [-0.0, -0.5, 0], [-2.5,0,0], color=GREEN)
        q_curve = q_curve.round_corners(radius=0.5)
        self.play(Create(q_curve))
        q_label = Text("Q", color=GREEN).move_to([1, 0.9, 0])
        self.play(Write(q_label))


        self.next_section("P curve")
        p_curve = Polygon([0, 3, 0], [4, 2, 0], [3,0,0], [0,-3.5,0], [-3,0,0], color=RED)
        p_curve = p_curve.round_corners(radius=1.5)
        self.play(Create(p_curve))
        p_label = Text("P", color=RED).move_to([2.2, -1.5, 0])
        self.play(Write(p_label))

        self.next_section("Distance line")
        q_alpha = ValueTracker(0)
        q_dot = Dot().move_to(p_curve.point_from_proportion(0))
        q_dot.add_updater(lambda m: m.move_to(q_curve.point_from_proportion(q_alpha.get_value())))
        self.play(Create(q_dot))

        p_alpha = ValueTracker(0)
        p_dot = Dot().move_to(p_curve.point_from_proportion(0))
        p_dot.add_updater(lambda m: m.move_to(p_curve.point_from_proportion(p_alpha.get_value())))
        self.play(Create(p_dot))

        line = Line(p_dot.get_center(), q_dot.get_center())
        line.add_updater(lambda z: z.become(Line(p_dot.get_center(), q_dot.get_center())))
        self.play(Create(line))

        def dist(alphas: np.ndarray):
            p = p_curve.point_from_proportion(alphas[0])
            q = q_curve.point_from_proportion(alphas[1])
            d = np.linalg.norm(p-q, ord=2)
            return d
        dist_text = Text("d=").to_edge(RIGHT).shift(LEFT)
        dist_number = DecimalNumber(dist([p_alpha.get_value(), q_alpha.get_value()])).next_to(dist_text, RIGHT)
        dist_number.add_updater(lambda t: t.set_value(dist([p_alpha.get_value(), q_alpha.get_value()])))
        dist_number.add_updater(lambda t: t.next_to(dist_text, RIGHT))
        self.play(Write(dist_text), Write(dist_number))
        self.wait()
        
        self.next_section("Animate distance around curves")
        self.play(p_alpha.animate.set_value(1), q_alpha.animate.set_value(1), run_time=3, rate_func=linear)
        p_alpha.set_value(0)
        q_alpha.set_value(0)
        self.wait()
        
        self.next_section("Go to maximum distance")
        minimum = optimize.fmin(lambda x: -1*dist(x), [0.5, 0.5], full_output=True)
        print(minimum)
        self.play(p_alpha.animate.set_value(minimum[0][0]), q_alpha.animate.set_value(minimum[0][1]), run_time=1)
        self.wait()
        
        # we need to provide the directed_hausdorff function with some sample points
        print("Sampling points on curves")
        alphas = np.linspace(0, 1, num=64)
        p_points, q_points = [], []
        debug_dots = []
        for a in alphas:
            p_pos = p_curve.point_from_proportion(a)
            q_pos = q_curve.point_from_proportion(a)
            p_points.append(p_pos[:2])
            q_points.append(q_pos[:2])
            debug_dots.append(Dot(p_pos).set_fill(GRAY, opacity=0.5))
            debug_dots.append(Dot(q_pos).set_fill(GRAY, opacity=0.5))
        self.add(Group(*debug_dots))

        

        self.next_section("To to direct Hausdorff distance from P to Q")
        print("Calculating directed Hausdorff distance")
        dh, ip, iq =  directed_hausdorff(p_points, q_points)
        print("Hausdorff distance:", dh, "Found on idxs:", ip, iq, "With alphas:", alphas[ip], alphas[iq])
        self.play(p_alpha.animate.set_value(alphas[ip]), q_alpha.animate.set_value(alphas[iq]), run_time=1)

        self.next_section("Mark directed distance with arrow")
        pq_dist_arrow = Arrow(start=[*p_points[ip], 0], end=[*q_points[iq], 0], color=RED, buff=0.05)
        pq_dist_value = DecimalNumber(dh, color=RED).next_to(pq_dist_arrow).shift(UP + 0.1*RIGHT)
        self.play(Create(pq_dist_arrow), Write(pq_dist_value))
        self.wait()

        

        self.next_section("To to direct Hausdorff distance from Q to P")
        dh, iq, ip =  directed_hausdorff(q_points, p_points)
        print("Hausdorff distance:", dh, "Found on idxs:", ip, iq, "With alphas:", alphas[ip], alphas[iq])
        self.play(p_alpha.animate.set_value(alphas[ip]), q_alpha.animate.set_value(alphas[iq]), run_time=1)
        
        self.next_section("Mark directed distance with arrow")
        qp_dist_arrow = Arrow(start=[*q_points[iq], 0], end=[*p_points[ip], 0], color=GREEN, buff=0.05)
        qp_dist_value = DecimalNumber(dh, color=GREEN).next_to(qp_dist_arrow).shift(UP + 0.1*RIGHT)
        self.play(Create(qp_dist_arrow), Write(qp_dist_value))
        self.play(Uncreate(line), Uncreate(p_dot), Uncreate(q_dot))
        self.wait()

            
        
        # square = Union(Square(), Square().rotate(PI/4), color=BLUE)
        # point = Dot().move_to(square.point_from_proportion(0))
        # alpha = ValueTracker(0)
        # point.add_updater(lambda m: m.move_to(square.point_from_proportion(alpha.get_value())))
        # self.add(square, point)
        # self.play(alpha.animate.set_value(1), run_time=3)
        self.wait()


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
            x_range=[0, 10], y_range=[0, 100, 10], axis_config={"include_tip": False, "include_numbers": True}
        )
        labels = ax.get_axis_labels(x_label="x", y_label="y")

        self.add(ax, labels)
        self.next_section("Axes", PresentationSectionType.NORMAL)
        
        
        x1 = ValueTracker(0)
        x2 = ValueTracker(0)

        def func1(x):
            return 2 * (x - 5) ** 2
        def func2(x):
            return -1.5 * (x - 2) ** 2 + 81
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
        dot1.set_z_index(1)
        dot2.set_z_index(1)

        self.next_section("Points")
        self.play(Create(dot1), Create(dot2))

        self.next_section("Line")
        line = Line(dot1.get_center(), dot2.get_center()).set_color(ORANGE)
        line.add_updater(lambda z: z.become(Line(dot1.get_center(), dot2.get_center(), color=ORANGE)))
        self.play(Create(line))

        def dist():
            d = np.sqrt((x1.get_value() - x2.get_value())**2 + (func1(x1.get_value()) - func2(x2.get_value()))**2)
            return d
        distNumber = DecimalNumber(dist()).next_to(line.get_center(), RIGHT)
        distNumber.add_updater(lambda t: t.set_value(dist()))
        distNumber.add_updater(lambda t: t.next_to(line.get_center(), RIGHT))
        self.play(Create(distNumber))
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
        self.play(x1.animate.set_value(0), x2.animate.set_value(0), run_time=3, rate_func=smooth)
        self.wait(1)

        self.next_section("Max vertical dist", PresentationSectionType.NORMAL)
        self.play(x1.animate.set_value(26/7), x2.animate.set_value(26/7), run_time=2)
        self.wait(1)

        self.next_section("Max vertical dist right", PresentationSectionType.NORMAL)
        self.play(x1.animate.set_value(26/7+0.5), x2.animate.set_value(26/7+0.5))

        self.next_section("Max vertical dist left", PresentationSectionType.NORMAL)
        self.play(x1.animate.set_value(26/7-0.5), x2.animate.set_value(26/7-0.5))
        
        self.next_section("Max vertical dist", PresentationSectionType.NORMAL)
        self.play(x1.animate.set_value(26/7), x2.animate.set_value(26/7))
        self.wait(1)

        self.next_section("Diagonal", PresentationSectionType.NORMAL)
        self.play(x1.animate.set_value(26/7-0.1), x2.animate.set_value(26/7+0.1))
        self.wait(1)



