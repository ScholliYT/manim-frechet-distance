import hashlib
from manim import *
from manim_editor import PresentationSectionType
from cachier import cachier
from scipy import optimize
from scipy.spatial.distance import directed_hausdorff

# config.background_color=BLACK
config.background_color = WHITE

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


class Titlepage(Scene):
    def construct(self):

        text = Text("Fréchet Distance", color=BLUE, font_size=70)
        self.add(text)
        self.wait()

        self.next_section("Subtitle")
        subtitle = Text("Origin, Variations and Algorithms", color=BLACK)
        self.play(text.animate.to_edge(UP))
        self.play(Write(subtitle))



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

class DistanceOfCurves(Scene):
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
        q_dot = Dot(color=DARK_GRAY).move_to(p_curve.point_from_proportion(0))
        q_dot.add_updater(lambda m: m.move_to(q_curve.point_from_proportion(q_alpha.get_value())))
        self.play(Create(q_dot))

        p_alpha = ValueTracker(0)
        p_dot = Dot(color=DARK_GRAY).move_to(p_curve.point_from_proportion(0))
        p_dot.add_updater(lambda m: m.move_to(p_curve.point_from_proportion(p_alpha.get_value())))
        self.play(Create(p_dot))

        line = Line(p_dot.get_center(), q_dot.get_center(), color=DARK_GRAY)
        line.add_updater(lambda z: z.become(Line(p_dot.get_center(), q_dot.get_center(), color=DARK_GRAY)))
        self.play(Create(line))
        
        def dist_full(alphas: np.ndarray, c1: Polygon, c2: Polygon):
            p = c1.point_from_proportion(alphas[0])
            q = c2.point_from_proportion(alphas[1])
            d = np.linalg.norm(p-q, ord=2)
            return d

        def dist(alphas: np.ndarray):
            return dist_full(alphas, p_curve, q_curve)

        dist_text = Text("d=", color=BLACK).to_edge(RIGHT).shift(LEFT)
        dist_number = DecimalNumber(dist([p_alpha.get_value(), q_alpha.get_value()]), color=BLACK).next_to(dist_text, RIGHT)
        dist_number.add_updater(lambda t: t.set_value(dist([p_alpha.get_value(), q_alpha.get_value()])))
        dist_number.add_updater(lambda t: t.next_to(dist_text, RIGHT))
        self.play(Write(dist_text), Write(dist_number))
        self.wait()
        
        self.next_section("Animate distance around curves")
        self.play(p_alpha.animate.set_value(1), q_alpha.animate.set_value(1), run_time=3, rate_func=linear)
        p_alpha.set_value(0)
        q_alpha.set_value(0)
        self.wait()
        
        self.next_section("Show maximum distance formula")
        max_distance_text = MathTex(
            "\\delta_{max}(P,Q) = \\sup_{p \\in P} \\sup_{q \\in Q} \\text{dist}(p,q)", 
            color = BLACK, font_size=30).to_edge(LEFT)
        self.play(Write(max_distance_text))
        self.wait()

        self.next_section("Go to maximum distance")

        def _distance_func_hasher(distance_func, kwargs):
            print("Hashing func and kwargs", kwargs)
            hash_tuple = (
                # hashlib.sha256(distance_func).hexdigest(),
                hashlib.sha256(p_curve.points.tobytes()).hexdigest(),
                hashlib.sha256(p_curve.color.get_hex().encode("utf-8")).hexdigest(),
                hashlib.sha256(q_curve.points.tobytes()).hexdigest(),
                hashlib.sha256(q_curve.color.get_hex().encode("utf-8")).hexdigest())

            print("Hash", hash_tuple)
            return  hash_tuple

        @cachier(hash_params=_distance_func_hasher)
        def argmin_max_distance(distance_func):
            minimum = optimize.fmin(lambda x: -1*distance_func(x, p_curve, q_curve), [0.5, 0.5], full_output=True)
            print(minimum)
            return minimum[0]
        minimum_alphas = argmin_max_distance(dist_full)
        self.play(p_alpha.animate.set_value(minimum_alphas[0]), q_alpha.animate.set_value(minimum_alphas[1]), run_time=1)
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

        

        self.next_section("Show formula for direct Hausdorff distance from P to Q")
        directed_hausdorff_dist_p_q_text = MathTex(
            "\\delta_{dhd}(P,Q) = \\sup_{p \\in P} \\inf_{q \\in Q} \\text{dist}(p,q)", 
            color = BLACK, font_size=30).to_edge(LEFT)
        self.play(ReplacementTransform(max_distance_text, directed_hausdorff_dist_p_q_text))
        self.wait()
        
        self.next_section("Go to direct Hausdorff distance from P to Q")
        print("Calculating directed Hausdorff distance")
        dh, ip, iq =  directed_hausdorff(p_points, q_points)
        print("Hausdorff distance:", dh, "Found on idxs:", ip, iq, "With alphas:", alphas[ip], alphas[iq])
        self.play(p_alpha.animate.set_value(alphas[ip]), q_alpha.animate.set_value(alphas[iq]), run_time=1)

        self.next_section("Mark directed distance with arrow")
        pq_dist_arrow = Arrow(start=[*p_points[ip], 0], end=[*q_points[iq], 0], color=RED, buff=0.05)
        pq_dist_value = DecimalNumber(dh, color=RED).next_to(pq_dist_arrow).shift(UP + 0.1*RIGHT)
        self.play(Create(pq_dist_arrow), Write(pq_dist_value))
        self.wait()

        

        self.next_section("Show formula for direct Hausdorff distance from P to Q")
        directed_hausdorff_dist_q_p_text = MathTex(
            "\\delta_{dhd}(Q,P) = \\sup_{q \\in Q} \\inf_{p \\in P} \\text{dist}(p,q)", 
            color = BLACK, font_size=30).to_edge(LEFT).shift(DOWN)
        # self.play(hausdorff_dist_p_q_text.animate.shift(UP))
        self.play(Write(directed_hausdorff_dist_q_p_text))
        self.wait()

        self.next_section("Go to direct Hausdorff distance from Q to P")
        dh, iq, ip =  directed_hausdorff(q_points, p_points)
        print("Hausdorff distance:", dh, "Found on idxs:", ip, iq, "With alphas:", alphas[ip], alphas[iq])
        self.play(p_alpha.animate.set_value(alphas[ip]), q_alpha.animate.set_value(alphas[iq]), run_time=1)
        
        self.next_section("Mark directed distance with arrow")
        qp_dist_arrow = Arrow(start=[*q_points[iq], 0], end=[*p_points[ip], 0], color=GREEN, buff=0.05)
        qp_dist_value = DecimalNumber(dh, color=GREEN).next_to(qp_dist_arrow).shift(UP + 0.1*RIGHT)
        self.play(Create(qp_dist_arrow), Write(qp_dist_value))
        dist_number.clear_updaters()
        self.play(Uncreate(line), Uncreate(p_dot), Uncreate(q_dot), Unwrite(dist_text), Unwrite(dist_number))
        self.wait()

        self.next_section("Show formula for Hausdorff distance")
        hausdorff_dist_p_q_text_1 = MathTex(
            "\\delta_{hd}(P,Q)=","\\max \\left(","\\delta_{dhd}(P,Q)",",","\\delta_{dhd}(Q,P)","\\right)", 
            color = BLACK, font_size=30).to_edge(LEFT).shift(3*DOWN)
        self.play(Write(hausdorff_dist_p_q_text_1))
        self.wait()

        hausdorff_dist_p_q_text = MathTex(
            "\\delta_{hd}(P,Q)=","\\max \\left(","\\sup_{p \\in P} \\inf_{q \\in Q} \\text{dist}(p,q)",",","\\sup_{q \\in Q} \\inf_{p \\in P} \\text{dist}(p,q)","\\right)", 
            color = BLACK, font_size=30).to_edge(LEFT).shift(3*DOWN)
        self.play(TransformMatchingTex(hausdorff_dist_p_q_text_1, hausdorff_dist_p_q_text))
        self.wait()

        # TODO: compute with concrete values

            
        
        # square = Union(Square(), Square().rotate(PI/4), color=BLUE)
        # point = Dot().move_to(square.point_from_proportion(0))
        # alpha = ValueTracker(0)
        # point.add_updater(lambda m: m.move_to(square.point_from_proportion(alpha.get_value())))
        # self.add(square, point)
        # self.play(alpha.animate.set_value(1), run_time=3)
        self.wait()


class ProblemsWithHausdorffDistance(Scene):
    def construct(self):
        title = Text("Problems with Hausdorff Distance", color=BLUE).to_edge(UP)
        self.add(title)

        self.next_section("P curve")
        p_curve = Polygon(
            [-2.82, -2.14, 0], [-1.5, 2.6, 0], [-1.1, -2.01, 0], [0.347, 2.68, 0], [0.896, -2.28, 0], [1.88, 2.67, 0], [2.26, -1.869, 0], 
            color=RED)
        self.play(Create(p_curve))
        p_label = Text("P", color=RED).move_to([2.6, -1.5, 0])
        self.play(Write(p_label))

        self.next_section("Q curve")
        q_curve = Polygon(
            [-2.783, 2.731, 0], [2.72, 2.65, 0], [-2.99, 0.79, 0], [2.37, 0.1316, 0], [-3.0, -1.11, 0], [1.53, -1.97, 0], [-1.3, -2.28, 0],
            color=GREEN)
        self.play(Create(q_curve))
        q_label = Text("Q", color=GREEN).move_to([3.1, 2.6, 0])
        self.play(Write(q_label))
    

        self.next_section("Distance line")
        q_alpha = ValueTracker(0)
        q_dot = Dot(color=DARK_GRAY).move_to(p_curve.point_from_proportion(0))
        q_dot.add_updater(lambda m: m.move_to(q_curve.point_from_proportion(q_alpha.get_value())))
        self.play(Create(q_dot))

        p_alpha = ValueTracker(0)
        p_dot = Dot(color=DARK_GRAY).move_to(p_curve.point_from_proportion(0))
        p_dot.add_updater(lambda m: m.move_to(p_curve.point_from_proportion(p_alpha.get_value())))
        self.play(Create(p_dot))

        line = Line(p_dot.get_center(), q_dot.get_center(), color=DARK_GRAY)
        line.add_updater(lambda z: z.become(Line(p_dot.get_center(), q_dot.get_center(), color=DARK_GRAY)))
        self.play(Create(line))
        
        def dist_full(alphas: np.ndarray, c1: Polygon, c2: Polygon):
            p = c1.point_from_proportion(alphas[0])
            q = c2.point_from_proportion(alphas[1])
            d = np.linalg.norm(p-q, ord=2)
            return d

        def dist(alphas: np.ndarray):
            return dist_full(alphas, p_curve, q_curve)

        dist_text = Text("d=", color=BLACK).to_edge(RIGHT).shift(LEFT)
        dist_number = DecimalNumber(dist([p_alpha.get_value(), q_alpha.get_value()]), color=BLACK).next_to(dist_text, RIGHT)
        dist_number.add_updater(lambda t: t.set_value(dist([p_alpha.get_value(), q_alpha.get_value()])))
        dist_number.add_updater(lambda t: t.next_to(dist_text, RIGHT))
        self.play(Write(dist_text), Write(dist_number))
        self.wait()
        
        self.next_section("Animate distance around curves")
        self.play(p_alpha.animate.set_value(1), q_alpha.animate.set_value(1), run_time=3, rate_func=linear)
        p_alpha.set_value(0)
        q_alpha.set_value(0)
        self.wait()

        # we need to provide the directed_hausdorff function with some sample points
        print("Sampling points on curves")
        alphas = np.linspace(0, 1, num=256)
        p_points, q_points = [], []
        debug_dots = []
        for a in alphas:
            p_pos = p_curve.point_from_proportion(a)
            q_pos = q_curve.point_from_proportion(a)
            p_points.append(p_pos[:2])
            q_points.append(q_pos[:2])
            debug_dots.append(Dot(p_pos).set_fill(GRAY, opacity=0.5))
            debug_dots.append(Dot(q_pos).set_fill(GRAY, opacity=0.5))
        debug_dots = Group(*debug_dots)
        self.add(debug_dots)

        self.next_section("Go to direct Hausdorff distance from P to Q")
        print("Calculating directed Hausdorff distance")
        dh, ip, iq =  directed_hausdorff(p_points, q_points)
        print("Hausdorff distance:", dh, "Found on idxs:", ip, iq, "With alphas:", alphas[ip], alphas[iq])
        self.play(p_alpha.animate.set_value(alphas[ip]), q_alpha.animate.set_value(alphas[iq]), run_time=1)

        self.next_section("Mark directed distance with arrow")
        pq_dist_arrow = Arrow(start=[*p_points[ip], 0], end=[*q_points[iq], 0], color=RED, buff=0.05)
        pq_dist_value = DecimalNumber(dh, color=RED).next_to(pq_dist_arrow)
        self.play(Create(pq_dist_arrow), Write(pq_dist_value))
        self.wait()

        self.next_section("Go to direct Hausdorff distance from Q to P")
        dh, iq, ip =  directed_hausdorff(q_points, p_points)
        print("Hausdorff distance:", dh, "Found on idxs:", ip, iq, "With alphas:", alphas[ip], alphas[iq])
        self.play(p_alpha.animate.set_value(alphas[ip]), q_alpha.animate.set_value(alphas[iq]), run_time=1)
        
        self.next_section("Mark directed distance with arrow")
        qp_dist_arrow = Arrow(start=[*q_points[iq], 0], end=[*p_points[ip], 0], color=GREEN, buff=0.05)
        qp_dist_value = DecimalNumber(dh, color=GREEN).next_to(qp_dist_arrow, direction=LEFT)
        self.play(Create(qp_dist_arrow), Write(qp_dist_value))
        dist_number.clear_updaters()
        self.play(Uncreate(line), Uncreate(p_dot), Uncreate(q_dot), Unwrite(dist_text), Unwrite(dist_number))
        self.wait()

        if "debug_dots" in locals():
            self.remove(debug_dots)
            self.wait()


class TestTex(Scene):
    def construct(self):
        hausdorff_dist_p_q_text_1 = MathTex(
            "\\delta_{hd}(P,Q)=","\\max \\left(","\\delta_{dhd}(P,Q)",",","\\delta_{dhd}(Q,P)","\\right)", 
            color = BLACK, font_size=30).to_edge(LEFT).shift(DOWN)
        self.play(Write(hausdorff_dist_p_q_text_1))
        self.wait()

        hausdorff_dist_p_q_text_2 = MathTex(
            "\\delta_{hd}(P,Q)=","\\max \\left(","\\sup_{p \\in P} \\inf_{q \\in Q} \\text{dist}(p,q)",",","\\sup_{q \\in Q} \\inf_{p \\in P} \\text{dist}(p,q)","\\right)", 
            color = BLACK).to_edge(LEFT).shift(DOWN)
        self.play(TransformMatchingTex(hausdorff_dist_p_q_text_1, hausdorff_dist_p_q_text_2))
        self.wait()


        hausdorff_dist_p_q_text = MathTex(
            "\\delta_{hd}(P,Q)=","\\max \\left(","5",",","3","\\right)", 
            # substrings_to_isolate=,
            color = BLACK, font_size=30).to_edge(LEFT).shift(DOWN)
        self.play(TransformMatchingTex(hausdorff_dist_p_q_text_2, hausdorff_dist_p_q_text))
        self.wait()

        self.play(Unwrite(hausdorff_dist_p_q_text))


class FrechetDistanceIntro(Scene):
    def construct(self):
        title = Text("Fréchet Distance", color=BLUE).to_edge(UP)
        self.add(title)

class DiscreteFrechetDistanceIntro(Scene):
    def construct(self):
        title = Text("Discrete Fréchet Distance", color=BLUE).to_edge(UP)
        self.add(title)


class ComputingTheFrechetDistance(Scene):
    def construct(self):
        title = Text("Computing the Fréchet Distance", color=BLUE).to_edge(UP)
        self.add(title)

        blist = BulletedList("Free Space Diagram", "Monotone Path", "Critical values")
        self.play(Write(blist))

class FreeSpaceCell(Scene):
    def construct(self):
        title = Text("Free Space Cell", color=BLUE).to_edge(UP)
        self.add(title)

class FreeSpaceDiagram(Scene):
    def construct(self):
        title = Text("Free Space Diagram", color=BLUE).to_edge(UP)
        self.add(title)

class FrechetDistanceAlgorithmicComplexity(Scene):
    def construct(self):
        title = Text("Algorithmic Complexity", color=BLUE).to_edge(UP)
        self.add(title)

class DiscreteFrechetDistanceAlgorithm(Scene):
    def construct(self):
        title = Text("Discrete Fréchet Distance", color=BLUE).to_edge(UP)
        self.add(title)

class DiscreteFrechetDistanceAlgorithmicComplexity(Scene):
    def construct(self):
        title = Text("Algorithmic Complexity", color=BLUE).to_edge(UP)
        self.add(title)




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



