from functools import partial
import hashlib
from typing import Tuple
from manim import *
from manim_editor import PresentationSectionType
from cachier import cachier
from scipy import optimize
from scipy.spatial.distance import directed_hausdorff, cdist

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

def add_slide_number(scene: Scene, slide_number: int):
    slide_number_text = Text(str(slide_number), font_size=15, color=BLACK)
    slide_number_text.to_corner(RIGHT+DOWN)
    scene.add(slide_number_text)


class Titlepage(Scene):
    def construct(self):

        text = Text("Fréchet Distance", color=BLUE, font_size=70)
        self.add(text)
        self.wait()

        self.next_section("Subtitle")
        subtitle = Text("Origin, Variations and Algorithms", color=BLACK)
        self.play(text.animate.to_edge(UP))
        self.play(Write(subtitle))


class Motivation(Scene):
    def construct(self):
        add_slide_number(self, 1)
        title = Text("Motivation", color=BLUE).to_edge(UP)
        self.add(title)

        self.next_section("World map")
        world_map = ImageMobject("manim_frechet_distance/assets/BlankMap_Europe_Africa.png").shift(0.5*DOWN)
        world_map.height = 6
        self.add(world_map)
        self.wait()

        birds = [
            {
                "bird_path": [
                    [-0.5,1,0],
                    [-1,0.5,0],
                    [-1.3,-0.9,0],
                    [-0.3,-1.1,0],
                ],
                "color": BLUE,
            },
            {
                "bird_path": [
                    [-0.4,1.1,0],
                    [-0.1,0.55,0],
                    [-0.3,0.2,0],
                    [0.2,-1.2,0],
                ],
                "color": RED,
            },
            {
                "bird_path": [
                    [-0.2,1.0,0],
                    [0.5,0.55,0],
                    [0.8,0.5,0],
                    [0.9,0.2,0],
                    [0.6,0,0],
                    [0.5,-1.5,0],
                ],
                "color": GREEN,
            },
        ]


        for bird in birds:
            bird_path = bird["bird_path"]

            self.next_section("Add Bird")
            bird_image = ImageMobject("manim_frechet_distance/assets/icons8-crane-bird-100.png")
            bird_image.set_z_index(3)
            bird_image.scale(0.8)
            bird_image.move_to(bird_path[0])

            trace = TracedPath(bird_image.get_center, stroke_color=GRAY_D)
            bird["traces"] = [trace]
            self.add(trace, bird_image)
            self.wait()

            self.next_section("Move bird along path")
            for pos in bird_path[1:]:
                self.play(bird_image.animate.move_to(pos), run_time=0.75)
                self.wait(0.25)
            self.wait()

        self.next_section("Multiple birds per route")
        np.random.seed(42)
        additional_birds_per_route = 3
        trace_creations = []
        for bird in birds:
            for _ in range(additional_birds_per_route):
                bird_path = np.array(bird["bird_path"])
                noise = (np.random.rand(bird_path.shape[0], 2) - 0.5)/8.0
                noise = np.pad(noise, ((0,0), (0,1)))

                trace_func = partial(polygonal_curve, bird_path+noise)
                trace = ParametricFunction(
                    trace_func,
                    t_range=[0, len(bird_path)-1],
                    color=GRAY_D,
                )
                bird["traces"].append(trace)

                trace_creations.append(Create(trace))
        self.play(LaggedStart(*trace_creations))
        self.wait()


        self.next_section("Cluster routes")
        for bird in birds:
            self.play(*[trace.animate.set_stroke(color=bird["color"]) for trace in bird["traces"]], run_time=2.0/len(birds))
        self.wait()



class DistanceOfCurves(Scene):
    def construct(self):
        add_slide_number(self, 2)
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
        q_label = Text("Q", color=GREEN).move_to([-1.5, 0.2, 0])
        self.play(Write(q_label))


        self.next_section("P curve")
        p_curve = Polygon([0, 3, 0], [4, 2, 0], [3,0,0], [0,-3.5,0], [-3,0,0], color=RED)
        p_curve = p_curve.round_corners(radius=1.5)
        self.play(Create(p_curve))
        p_label = Text("P", color=RED).move_to([2.2, -1.5, 0])
        self.play(Write(p_label))

        self.next_section("Distance line")
        def get_dist_line(pa: float, qa: float):
            p_dot = Dot(color=DARK_GRAY).move_to(p_curve.point_from_proportion(pa))
            q_dot = Dot(color=DARK_GRAY).move_to(q_curve.point_from_proportion(qa))
            line = Line(p_dot.get_center(), q_dot.get_center(), color=DARK_GRAY)
            return p_dot, q_dot, line


        p_alpha = ValueTracker(0)
        q_alpha = ValueTracker(0)
        p_dot, q_dot, line = get_dist_line(0,0)
        
        # q_dot.add_updater(lambda m: m.move_to(q_curve.point_from_proportion(q_alpha.get_value())))
        # p_dot.add_updater(lambda m: m.move_to(p_curve.point_from_proportion(p_alpha.get_value())))
        self.play(Create(p_dot), Create(q_dot))
        # line.add_updater(lambda z: z.become(Line(p_dot.get_center(), q_dot.get_center(), color=DARK_GRAY)))
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
        
        self.next_section("Animate distance at differnt point on curve curves")
        new_point_alphas = (0.3, 0.1)
        new_p_dot, new_q_dot, new_line = get_dist_line(new_point_alphas[0], new_point_alphas[1])
        self.play(
            Transform(p_dot, new_p_dot),
            Transform(q_dot, new_q_dot),
            Transform(line, new_line),
            p_alpha.animate.set_value(new_point_alphas[0]),
            q_alpha.animate.set_value(new_point_alphas[1])
        )
        self.wait()

        self.next_section("Animate distance at differnt point on curve curves")
        new_point_alphas = (0.8, 0.6)
        new_p_dot, new_q_dot, new_line = get_dist_line(new_point_alphas[0], new_point_alphas[1])
        self.play(
            Transform(p_dot, new_p_dot),
            Transform(q_dot, new_q_dot),
            Transform(line, new_line),
            p_alpha.animate.set_value(new_point_alphas[0]),
            q_alpha.animate.set_value(new_point_alphas[1])
        )
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

        new_point_alphas = minimum_alphas
        new_p_dot, new_q_dot, new_line = get_dist_line(new_point_alphas[0], new_point_alphas[1])
        self.play(
            Transform(p_dot, new_p_dot),
            Transform(q_dot, new_q_dot),
            Transform(line, new_line),
            p_alpha.animate.set_value(new_point_alphas[0]),
            q_alpha.animate.set_value(new_point_alphas[1])
        )
        self.wait()

        self.next_section("Hausdorff distance")
        dist_number.clear_updaters()
        self.play(Uncreate(line), Uncreate(p_dot), Uncreate(q_dot), Unwrite(dist_text), Unwrite(dist_number))
        self.play(title.animate.become(Text("Hausdorff distance", color=BLUE).to_edge(UP)))

        # self.next_section("Show formula for direct Hausdorff distance from P to Q")
        directed_hausdorff_dist_p_q_text = MathTex(
            "\\delta_{dhd}(P,Q) = \\sup_{p \\in P} \\inf_{q \\in Q} \\text{dist}(p,q)", 
            color = BLACK, font_size=30).to_edge(LEFT)
        self.play(ReplacementTransform(max_distance_text, directed_hausdorff_dist_p_q_text))
        self.wait()

        # we need to provide the directed_hausdorff function with some sample points
        self.next_section("Show sampling points")
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
        self.play(LaggedStart(*[Create(p) for p in debug_dots]), run_time=2)
        debug_dots = Group(*debug_dots)

        self.next_section("Show all distance arrows from P to Q")
        arrows_from_p_to_q = min_dist_arrows(p_points, q_points, color=RED)
        self.play(LaggedStart(*[Create(a) for a in arrows_from_p_to_q]), run_time=2)
        self.wait()
        
        # self.next_section("Go to direct Hausdorff distance from P to Q")
        print("Calculating directed Hausdorff distance")
        dh, ip, iq =  directed_hausdorff(p_points, q_points)
        print("Hausdorff distance:", dh, "Found on idxs:", ip, iq, "With alphas:", alphas[ip], alphas[iq])
        # self.play(p_alpha.animate.set_value(alphas[ip]), q_alpha.animate.set_value(alphas[iq]), run_time=1)

        self.next_section("Mark directed distance with arrow")
        pq_dist_arrow = Arrow(start=[*p_points[ip], 0], end=[*q_points[iq], 0], color=RED, buff=0.05)
        pq_dist_value = DecimalNumber(dh, color=RED).next_to(pq_dist_arrow).shift(UP + 0.1*RIGHT)
        self.play(Create(pq_dist_arrow))
        self.play(Indicate(pq_dist_arrow))
        self.play(Write(pq_dist_value))
        self.wait()

        self.next_section("Remove arrows from P to Q")
        self.play(LaggedStart(*[Uncreate(a) for a in arrows_from_p_to_q]), run_time=1)


        self.next_section("Show formula for direct Hausdorff distance from Q to P")
        directed_hausdorff_dist_q_p_text = MathTex(
            "\\delta_{dhd}(Q,P) = \\sup_{q \\in Q} \\inf_{p \\in P} \\text{dist}(p,q)", 
            color = BLACK, font_size=30).to_edge(LEFT).shift(DOWN)
        # self.play(hausdorff_dist_p_q_text.animate.shift(UP))
        self.play(Write(directed_hausdorff_dist_q_p_text))
        self.wait()

        self.next_section("Show all distance arrows from Q to P")
        arrows_from_q_to_p = min_dist_arrows(q_points, p_points, color=GREEN)
        self.play(LaggedStart(*[Create(a) for a in arrows_from_q_to_p]), run_time=2)
        self.wait()

        # self.next_section("Go to direct Hausdorff distance from Q to P")
        dh, iq, ip =  directed_hausdorff(q_points, p_points)
        # print("Hausdorff distance:", dh, "Found on idxs:", ip, iq, "With alphas:", alphas[ip], alphas[iq])
        # self.play(p_alpha.animate.set_value(alphas[ip]), q_alpha.animate.set_value(alphas[iq]), run_time=1)
        
        self.next_section("Mark directed distance with arrow")
        qp_dist_arrow = Arrow(start=[*q_points[iq], 0], end=[*p_points[ip], 0], color=GREEN, buff=0.05)
        qp_dist_value = DecimalNumber(dh, color=GREEN).next_to(qp_dist_arrow).shift(UP + 0.1*RIGHT)
        self.play(Create(qp_dist_arrow))
        self.play(Indicate(qp_dist_arrow))
        self.play(Write(qp_dist_value))
        self.wait()

        self.next_section("Remove arrows from Q to P")
        self.play(LaggedStart(*[Uncreate(a) for a in arrows_from_q_to_p]), run_time=1)

        self.next_section("Show formula for Hausdorff distance")
        hausdorff_dist_p_q_text_1 = MathTex(
            "\\delta_{hd}(P,Q)=","\\max \\left(","\\delta_{dhd}(P,Q)",",","\\delta_{dhd}(Q,P)","\\right)", 
            color = BLACK, font_size=30).to_edge(LEFT).shift(3*DOWN)
        self.play(Write(hausdorff_dist_p_q_text_1))
        self.wait()

        self.next_section("Show complete formula for Hausdorff distance")
        hausdorff_dist_p_q_text = MathTex(
            "\\delta_{hd}(P,Q)=","\\max \\left(","\\sup_{p \\in P} \\inf_{q \\in Q} \\text{dist}(p,q)",",","\\sup_{q \\in Q} \\inf_{p \\in P} \\text{dist}(p,q)","\\right)", 
            color = BLACK, font_size=30).to_edge(LEFT).shift(3*DOWN)
        self.play(TransformMatchingTex(hausdorff_dist_p_q_text_1, hausdorff_dist_p_q_text))
        self.wait()

def min_dist_arrows(p_points, q_points, color=GRAY):
    distances = cdist(p_points, q_points,'sqeuclidean') # pairwise distances
    min_distances = np.min(distances, axis=1) # minimal distance for each point on p to a point on q
    min_distance = np.min(min_distances) # global minimal distance
    max_distance = np.max(min_distances) # global maximal distance
    closest_points_on_q = np.argmin(distances,axis=1) # index of closest point on q for each point of p
    arrows_from_p_to_q = []
    for ip,iq in enumerate(closest_points_on_q):
        pq_dist_arrow = Arrow(start=[*p_points[ip], 0], end=[*q_points[iq], 0], color=color, buff=0.05)
        
        opacity =  (min_distances[ip] - min_distance) / (max_distance - min_distance)
        smoothing = lambda x: 1/(1+ np.power(np.e, -3*(x-0.4)))
        pq_dist_arrow.set_opacity(smoothing(opacity))

        arrows_from_p_to_q.append(pq_dist_arrow)
    return arrows_from_p_to_q


class ProblemsWithHausdorffDistance(Scene):
    def construct(self):
        add_slide_number(self, 3)
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

        self.next_section("Sample points on curves")
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
        self.play(*[Create(p) for p in debug_dots], run_time=2)
        debug_dots = Group(*debug_dots)

        print("Calculating directed Hausdorff distance")
        dh, ip, iq =  directed_hausdorff(p_points, q_points)
        print("Hausdorff distance:", dh, "Found on idxs:", ip, iq, "With alphas:", alphas[ip], alphas[iq])

        self.next_section("Show all distance arrows from P to Q")
        arrows_from_p_to_q = min_dist_arrows(p_points, q_points, color=RED)
        self.play(LaggedStart(*[Create(a) for a in arrows_from_p_to_q]), run_time=2)
        self.wait()

        self.next_section("Mark directed distance with arrow")
        pq_dist_arrow = Arrow(start=[*p_points[ip], 0], end=[*q_points[iq], 0], color=RED, buff=0.05)
        pq_dist_value = DecimalNumber(dh, color=RED).next_to(pq_dist_arrow)
        self.play(Create(pq_dist_arrow))
        self.play(Indicate(pq_dist_arrow))
        self.play(Write(pq_dist_value))
        self.wait()

        self.next_section("Remove arrows from P to Q")
        self.play(LaggedStart(*[Uncreate(a) for a in arrows_from_p_to_q]), run_time=1)

        self.next_section("Show all distance arrows from Q to P")
        arrows_from_q_to_p = min_dist_arrows(q_points, p_points, color=GREEN)
        self.play(LaggedStart(*[Create(a) for a in arrows_from_q_to_p]), run_time=2)
        self.wait()

        dh, iq, ip =  directed_hausdorff(q_points, p_points)
        print("Hausdorff distance:", dh, "Found on idxs:", ip, iq, "With alphas:", alphas[ip], alphas[iq])
        
        self.next_section("Mark directed distance with arrow")
        qp_dist_arrow = Arrow(start=[*q_points[iq], 0], end=[*p_points[ip], 0], color=GREEN, buff=0.05)
        qp_dist_value = DecimalNumber(dh, color=GREEN).next_to(qp_dist_arrow, direction=LEFT)
        self.play(Create(qp_dist_arrow))
        self.play(Indicate(qp_dist_arrow))
        self.play(Write(qp_dist_value))
        self.wait()

        self.next_section("Remove arrows from Q to P")
        self.play(LaggedStart(*[Uncreate(a) for a in arrows_from_q_to_p]), run_time=1)
        self.wait()

        # if "debug_dots" in locals():
        #     self.remove(debug_dots)
        #     self.wait()

class FrechetDistanceIntro(Scene):
    def construct(self):
        add_slide_number(self, 4)
        title = Text("Fréchet Distance", color=BLUE).to_edge(UP)
        self.add(title)

        p_curve = Polygon(
            [-5.25,  0.25,  0.  ],
            [-2.25,  0.25,  0.  ],
            [-1.5 ,  1.75,  0.  ],
            [-0.9 ,  1.75,  0.  ],
            [-0.6 ,  0.4 ,  0.  ],
            [ 0.75,  1.75,  0.  ],
            [ 1.5 ,  1.  ,  0.  ],
            [ 3.  ,  0.25,  0.  ],
            [ 3.9 ,  0.7 ,  0.  ],
            [ 3.  , -1.4 ,  0.  ],
            [-4.8 , -1.4 ,  0.  ],
            color=RED)
        q_curve = Polygon(
            [-5.25,  0.25,  0.  ],
            [-4.5 , -0.5 ,  0.  ],
            [-2.25, -0.5 ,  0.  ],
            [-1.2 ,  0.4 ,  0.  ],
            [-0.75, -0.5 ,  0.  ],
            [ 2.25,  1.  ,  0.  ],
            [ 3.  ,  1.  ,  0.  ],
            [ 3.9 , -0.2 ,  0.  ],
            [ 3.3 , -1.7 ,  0.  ],
            [-5.1 , -1.7 ,  0.  ],
            color=GREEN)

        # dog and owner at home
        self.next_section("Show Owner")
        owner = ImageMobject("manim_frechet_distance/assets/icons8-person-pointing-90.png").scale(1.2)
        owner = owner.move_to([-6, -0.5, 0]).set_z_index(3)
        self.add(owner)
        self.wait()

        self.next_section("Show Dog")
        dog = ImageMobject("manim_frechet_distance/assets/icons8-dog-jump-90.png")
        dog = dog.move_to([-6, 1, 0]).set_z_index(3)
        self.add(dog)
        self.wait()

        # show leash
        self.next_section("Distance line")
        line = Line(dog.get_center(), owner.get_center(), color=DARK_GRAY)
        line.add_updater(lambda z: z.become(Line(dog.get_center(), owner.get_center()  + [-0.22, -0.06, 0], color=DARK_GRAY)))
        self.play(Create(line))
        self.wait()

        # show paths
        self.next_section("Owner Curve")
        self.play(Create(q_curve))
        q_label = Text("Owner", color=GREEN).move_to([-4, -2.1, 0])
        self.play(Write(q_label))
        
        self.next_section("Dog Curve")
        self.play(Create(p_curve))
        p_label = Text("Dog", color=RED).move_to([-4, 0.8, 0])
        self.play(Write(p_label))
        self.wait()

        # move dog and owner to starting position
        self.next_section("Move to starting position")
        dog_alpha = ValueTracker(0)
        owner_alpha = ValueTracker(0)
        self.play(
            dog.animate.move_to(p_curve.point_from_proportion(dog_alpha.get_value())),
            owner.animate.move_to(q_curve.point_from_proportion(owner_alpha.get_value()))
        )
        dog.add_updater(lambda m: m.move_to(p_curve.point_from_proportion(dog_alpha.get_value())))
        owner.add_updater(lambda m: m.move_to(q_curve.point_from_proportion(owner_alpha.get_value())))
        self.wait()
        
        def dist_full(alphas: np.ndarray, c1: Polygon, c2: Polygon):
            p = c1.point_from_proportion(alphas[0])
            q = c2.point_from_proportion(alphas[1])
            d = np.linalg.norm(p-q, ord=2)
            return d

        def dist(alphas: np.ndarray):
            return dist_full(alphas, p_curve, q_curve)

        dist_text = Text("d=", color=BLACK).to_edge(RIGHT).shift(LEFT)
        dist_number = DecimalNumber(dist([dog_alpha.get_value(), owner_alpha.get_value()]), color=BLACK).next_to(dist_text, RIGHT)
        dist_number.add_updater(lambda t: t.set_value(dist([dog_alpha.get_value(), owner_alpha.get_value()])))
        dist_number.add_updater(lambda t: t.next_to(dist_text, RIGHT))
        self.play(Write(dist_text), Write(dist_number))
        self.wait()

        
        self.next_section("Animate distance around curves")
        self.play(dog_alpha.animate.set_value(0), owner_alpha.animate.set_value(0.1), run_time=2)
        self.play(dog_alpha.animate.set_value(0.3), owner_alpha.animate.set_value(0.3), run_time=2)
        self.play(dog_alpha.animate.set_value(0.5), owner_alpha.animate.set_value(0.6), run_time=2)
        self.play(dog_alpha.animate.set_value(0.75), owner_alpha.animate.set_value(0.65), run_time=2)
        self.play(dog_alpha.animate.set_value(1), owner_alpha.animate.set_value(1), run_time=2)
        dog_alpha.set_value(0)
        owner_alpha.set_value(0)
        self.wait()

        
        self.next_section("Animate distance around curves")
        self.play(dog_alpha.animate.set_value(1), owner_alpha.animate.set_value(1), run_time=10)
        dog_alpha.set_value(0)
        owner_alpha.set_value(0)
        self.wait()

        self.next_section("Show formula for Fréchet distance")
        frechet_dist_text = MathTex(
            r"\delta_{F}(P,Q) = \inf_{\substack{\alpha: [0,1] \mapsto [a, a'] \\ \beta: [0,1] \mapsto [b, b']}} \max_{t \in [0,1]} \text{dist}(P(\alpha(t)), Q(\beta(t)))",
            color = BLACK, font_size=30).to_edge(DOWN)
        self.play(Write(frechet_dist_text))
        self.wait()

class ComputingTheFrechetDistance(Scene):
    def construct(self):
        add_slide_number(self, 5)
        title = Text("Computing the Fréchet Distance", color=BLUE).to_edge(UP)
        self.add(title)

        self.next_section("Decision Problem")
        decision_problem_text = Text("Decision Problem:", font_size=30).shift(3*LEFT + UP).set_color(BLACK)
        self.add(decision_problem_text)
        self.wait()

        self.next_section("Decision Problem formula")
        decision_problem = MathTex(r"\delta_{F}(P,Q) \leq \varepsilon").set_color(BLACK).next_to(decision_problem_text, DOWN).align_to(decision_problem_text, LEFT).shift(0.5*RIGHT)
        self.play(Write(decision_problem))
        self.wait()
        
        self.next_section("Binary search")
        binary_search_text = Text("Binary search over ", font_size=30).next_to(decision_problem_text, DOWN).align_to(decision_problem_text, LEFT).shift(2*DOWN).set_color(BLACK)
        varepsilon_text = MathTex(r"\varepsilon").set_color(BLACK).next_to(binary_search_text, RIGHT)
        # self.play(LaggedStart(Write(binary_search_text), Write(varepsilon_text), lag_ratio=1.0))
        self.add(binary_search_text, varepsilon_text)
        self.wait()

        self.next_section("Solving the decision problem")
        blist_decision_problem = BulletedList("Free Space Cell", "Free Space Diagram", "Monotone Path").set_color(BLACK).shift(3*RIGHT).align_to(decision_problem_text, UP)
        self.play(Transform(decision_problem.copy(), blist_decision_problem))
        self.wait()

class FreeSpaceCell(Scene):
    def construct(self):
        add_slide_number(self, 6)
        title = Text("Free Space Cell", color=BLUE).to_edge(UP)
        self.add(title)

        ax = Axes(x_range=[-2,2], y_range=[-2,2], x_length=5, y_length=5, tips=False).set_color(BLACK)
        ax.shift(0.5*DOWN)
        self.add(ax)

        self.next_section("P line segment")
        p_points = np.array([
            [-2, 0, 0],
            [2, 0, 0]])
        alpha_p_range = [0, p_points.shape[0]-1]
        p_curve_func = partial(polygonal_curve, p_points)
        p_curve = ax.plot_parametric_curve(
            p_curve_func,
            t_range=alpha_p_range,
            color=RED,
        )
        self.play(Create(p_curve))
        p_label = Text("P", color=RED).move_to(ax.c2p(2.5, 0))
        self.play(Write(p_label))

        self.next_section("Q line segment")
        q_points = np.array([
            [2*np.cos(np.pi + np.pi/4), 2*np.sin(np.pi + np.pi/4), 0],
            [2*np.cos(np.pi/4), 2*np.sin(np.pi/4), 0]])
        alpha_q_range = [0, q_points.shape[0]-1]
        q_curve_func = partial(polygonal_curve, q_points)
        q_curve = ax.plot_parametric_curve(
            q_curve_func,
            t_range=alpha_q_range,
            color=GREEN,
        )
        self.play(Create(q_curve))
        q_label = Text("Q", color=GREEN).move_to(ax.c2p(2.5*np.cos(np.pi/4), 2.5*np.sin(np.pi/4)))
        self.play(Write(q_label))

        self.next_section("Add moving points")
        p_dot = Dot(p_curve.point_from_proportion(0), color=BLACK)
        q_dot = Dot(q_curve.point_from_proportion(0), color=BLACK)
        self.play(Create(p_dot), Create(q_dot))

        self.next_section("Shift graph to left side")
        graph = VGroup(ax, p_curve, p_label, q_curve, q_label, p_dot, q_dot)
        self.play(graph.animate.shift(4*LEFT))
        self.wait()
        
        
        self.next_section("Draw free space cell diagram")

        # Draw plot of cell
        free_space_cell_image = ImageMobject("manim_frechet_distance/assets/free_space_cell_points.png")
        free_space_cell_image.height = 5
        free_space_cell_image.width = 5

        axes_free_space = Axes(
            x_range=[0,1,0.25],
            y_range=[0,1,0.25],
            x_length=5,
            y_length=5,
            tips=False,
            axis_config={"include_numbers": True}
        ).set_color(BLACK)

        ax_p_label = MathTex("\\alpha_P", color=BLACK).next_to(free_space_cell_image, RIGHT).align_to(free_space_cell_image, DOWN)
        ax_q_label = MathTex("\\alpha_Q", color=BLACK).next_to(free_space_cell_image, UP).align_to(free_space_cell_image, LEFT)
        diagram = Group(free_space_cell_image, axes_free_space, ax_p_label, ax_q_label)
        diagram.shift(3.5*RIGHT + 0.5*DOWN)

        self.play(Create(axes_free_space), run_time=2)
        self.play(Write(ax_p_label), Write(ax_q_label))
        self.wait()

        
        self.next_section("Dot in free space cell")
        free_space_dot: Dot = Dot(axes_free_space.c2p(0,0), color=BLACK).set_z_index(5)
        self.play(Create(free_space_dot))
        self.wait()

        self.next_section("Move to (1,0) in free space")
        p_alpha = ValueTracker(0)
        q_alpha = ValueTracker(0)
        p_dot.add_updater(lambda m: m.move_to(p_curve.point_from_proportion(p_alpha.get_value())))
        q_dot.add_updater(lambda m: m.move_to(q_curve.point_from_proportion(q_alpha.get_value())))
        free_space_dot.add_updater(lambda m: m.move_to(axes_free_space.c2p(p_alpha.get_value(), q_alpha.get_value())))
        self.play(p_alpha.animate.set_value(1), q_alpha.animate.set_value(0), run_time=3, rate_func=linear)
        self.wait()


        self.next_section("Move to (1,1) in free space")
        self.play(p_alpha.animate.set_value(1), q_alpha.animate.set_value(1), run_time=3, rate_func=linear)
        self.wait()

        self.next_section("Back to point in middle of free space")
        self.play(p_alpha.animate.set_value(0.5), q_alpha.animate.set_value(0.25), run_time=2, rate_func=linear)
        self.wait()

        self.next_section("Show distance and line")
        line = Line(p_dot.get_center(), q_dot.get_center(), color=BLACK)
        line.add_updater(lambda z: z.become(Line(p_dot.get_center(), q_dot.get_center(), color=BLACK)))
        self.play(Create(line))
        
        def dist_full(alphas: Tuple[float,float], p_point_from_proportion, q_point_from_proportion):
            p = p_point_from_proportion(alphas[0])
            q = q_point_from_proportion(alphas[1])
            d = np.linalg.norm(p-q, ord=2)
            return d

        def dist(alphas: np.ndarray):
            return dist_full(alphas, p_curve_func, q_curve_func) / 2 # adjust for figure scaling

        dist_text = Text("d=", color=BLACK)
        dist_number = DecimalNumber(dist([p_alpha.get_value(), q_alpha.get_value()]), color=BLACK).next_to(dist_text, RIGHT)
        dist_number.add_updater(lambda t: t.set_value(dist([p_alpha.get_value(), q_alpha.get_value()])))
        dist_number.add_updater(lambda t: t.next_to(dist_text, RIGHT))
        dist_group = VGroup(dist_text, dist_number)
        dist_group.next_to(graph, DOWN)

        dist_line_components = (dist_text, dist_number, line, p_dot, q_dot, free_space_dot)
        self.play(Write(dist_text), Write(dist_number))
        self.wait()

        self.next_section("Move over border")
        self.play(p_alpha.animate.set_value(0.8), q_alpha.animate.set_value(0.25), run_time=2, rate_func=linear)
        self.wait()

        self.next_section("Show epsilon value")
        epsilon = ValueTracker(0.4)
        epsilon_text = MathTex("\\varepsilon=", color=BLACK)
        epsilon_number =  DecimalNumber(epsilon.get_value(), color=BLACK).next_to(epsilon_text, RIGHT)
        epslion_group = VGroup(epsilon_text, epsilon_number)
        epslion_group.next_to(free_space_cell_image, UP)
        epsilon_number.add_updater(lambda t: t.set_value(epsilon.get_value()))
        self.play(Write(epsilon_text), Write(epsilon_number))
        # line.clear_updaters()
        # self.play(Indicate(line))
        # line.add_updater(lambda z: z.become(Line(p_dot.get_center(), q_dot.get_center(), color=DARK_GRAY if dist([p_alpha.get_value(), q_alpha.get_value()]) <= epsilon.get_value() else RED)))
        self.wait()

        # animate walking around on the epsilon edge of the free space diagram
        self.next_section("Show epsilon border")
        free_space_graph = axes_free_space.plot_implicit_curve(
            lambda alpha_p,alpha_q: dist((alpha_p,alpha_q)) - epsilon.get_value(),
            color=BLUE_E,
            max_quads = 2000
        )
        self.add(free_space_graph)
        self.wait()

        self.next_section("Move over border")
        self.play(p_alpha.animate.set_value(0.45), q_alpha.animate.set_value(0.55), run_time=2, rate_func=linear)
        self.wait()

        self.next_section("Move outside of border")
        self.play(p_alpha.animate.set_value(0.1), q_alpha.animate.set_value(0.25), run_time=2, rate_func=linear)
        self.wait()


        # animate walking around on the epsilon edge of the free space diagram
        self.next_section("Move to epsilon border")
        free_space_alpha = ValueTracker(0.0)
        free_space_coords = lambda : axes_free_space.p2c(free_space_graph.point_from_proportion(free_space_alpha.get_value()))
        self.play(p_alpha.animate.set_value(free_space_coords()[0]), q_alpha.animate.set_value(free_space_coords()[1]), run_time=1, rate_func=linear)
        self.wait()

        self.next_section("Animate along epsilon border", PresentationSectionType.LOOP)
        p_alpha.add_updater(lambda x: x.set_value(free_space_coords()[0]))
        q_alpha.add_updater(lambda x: x.set_value(free_space_coords()[1]))
        self.play(free_space_alpha.animate.set_value(1), run_time=3)


        self.next_section("Increase epsilon value")
        p_alpha.clear_updaters()
        q_alpha.clear_updaters()
        free_space_graph.add_updater(lambda g: g.become(
            axes_free_space.plot_implicit_curve(
                lambda alpha_p,alpha_q: dist((alpha_p,alpha_q)) - epsilon.get_value(),
                color=BLUE_E,
                max_quads = 2000
            )
        ))
        self.play(epsilon.animate.set_value(0.73))
        free_space_graph.clear_updaters()
        self.wait()

        self.next_section("Add gray free space region")
        self.add(free_space_cell_image)
        self.wait()

        self.next_section("Remove dist line")
        line_updaters = line.get_updaters()
        line.clear_updaters()
        self.play(*[c.animate.set_opacity(0) for c in dist_line_components])
        self.wait()


        # find intersection points of elliplse with unit cell
        def find_intersection_points(eps: float, side: str):
            
            if side == "bottom":
                scalar_func = lambda alpha_p: abs(dist((alpha_p, 0)) - eps)
            elif side == "top":
                scalar_func = lambda alpha_p: abs(dist((alpha_p, 1)) - eps)
            elif side == "left":
                scalar_func = lambda alpha_q: abs(dist((0, alpha_q)) - eps)
            elif side == "right":
                scalar_func = lambda alpha_q: abs(dist((1, alpha_q)) - eps)
            else:
                raise ValueError(side)
            root: optimize.OptimizeResult = optimize.minimize_scalar(scalar_func, bounds=[0,1], options={"xatol": 1e-3})

            if root and not root["success"]:
                return RuntimeError("Optimizer was not sucessful", root)

            # search again because we don't know which minimum / root we found so far
            root1: optimize.OptimizeResult = optimize.minimize_scalar(scalar_func, bounds=[0,root.x], options={"xatol": 1e-3})
            root2: optimize.OptimizeResult = optimize.minimize_scalar(scalar_func, bounds=[root.x,1], options={"xatol": 1e-3})


            if side == "bottom":
                root1_coords = [root1.x, root1.fun]
                root2_coords = [root2.x, root2.fun]
            elif side == "top":
                root1_coords = [root1.x, 1-root1.fun]
                root2_coords = [root2.x, 1-root2.fun]
            elif side == "left":
                root1_coords = [root1.fun, root1.x]
                root2_coords = [root2.fun, root2.x]
            elif side == "right":
                root1_coords = [1-root1.fun, root1.x]
                root2_coords = [1-root2.fun, root2.x]

            return root1_coords, root2_coords

        self.next_section("Draw intersection points")
        intersection_point_dots: List[Tuple[Any, Dot]] = []
        for side in ["bottom", "top", "left", "right"]:
            coords1, coords2 = find_intersection_points(eps=epsilon.get_value(), side=side)
            
            for coords in (coords1, coords2):
                d = Dot(axes_free_space.c2p(*coords), color=DARK_BLUE)
                intersection_point_dots.append((coords, d))
                self.play(Create(d), run_time=0.5)
        self.wait()

        self.next_section("Intersection point calculation")
        self.play(intersection_point_dots[0][1].animate.set_color(ORANGE))
        self.play(intersection_point_dots[1][1].animate.set_color(ORANGE))
        self.wait()

        self.next_section("Intersection point calculation")
        point_on_circle_coords = np.add(q_points[0], [epsilon.get_value() * 2, 0 ,0])
        point_on_circle = ax.c2p(*point_on_circle_coords[:2])  # adjust for scale factor
        radius = np.linalg.norm(np.subtract(point_on_circle, q_curve.point_from_proportion(0)), ord=2)
        intersection_circle = Circle(radius=radius).move_to(q_curve.point_from_proportion(0)).set_color(GRAY_D)
        self.play(Create(intersection_circle))
        
        intersection_point_dot_1 = Dot(p_curve.point_from_proportion(intersection_point_dots[0][0][0]), color=ORANGE)
        intersection_point_dot_2 = Dot(p_curve.point_from_proportion(intersection_point_dots[1][0][0]), color=ORANGE)
        self.play(Create(intersection_point_dot_1), Create(intersection_point_dot_2))
        self.wait()

        self.next_section("Remove intersection points")
        self.play(
            *[Uncreate(d[1]) for d in intersection_point_dots],
            Uncreate(intersection_point_dot_1),
            Uncreate(intersection_point_dot_2),
            Uncreate(intersection_circle)
        )
        self.play(*[c.animate.set_opacity(1) for c in dist_line_components])
        for updater in line_updaters:
            line.add_updater(updater)
        self.wait()

        self.next_section("Move to (0.05,0)")
        self.play(p_alpha.animate.set_value(0.05), q_alpha.animate.set_value(0))
        self.wait()

        self.next_section("Move to (0,0)")
        self.play(p_alpha.animate.set_value(0), q_alpha.animate.set_value(0))
        self.wait()

        self.next_section("Increase epsilon value")
        self.remove(free_space_cell_image)
        free_space_graph.add_updater(lambda g: g.become(
            axes_free_space.plot_implicit_curve(
                lambda alpha_p,alpha_q: dist((alpha_p,alpha_q)) - epsilon.get_value(),
                color=BLUE_E,
                max_quads = 2000
            )
        ))
        self.play(epsilon.animate.set_value(0.8))
        free_space_graph.clear_updaters()
        self.wait()

        self.next_section("Move to (1,1) diagonal")
        trace = TracedPath(free_space_dot.get_center, stroke_color=BLUE)
        self.add(trace)
        self.play(p_alpha.animate.set_value(1), q_alpha.animate.set_value(1), run_time=3)
        self.wait()


        self.next_section("Move to (0,0)")
        self.play(Uncreate(trace))
        self.play(p_alpha.animate.set_value(0), q_alpha.animate.set_value(0))
        self.wait()

        self.next_section("Move to (1,1)")
        trace = TracedPath(free_space_dot.get_center, stroke_color=BLUE)
        self.add(trace)
        self.play(p_alpha.animate.set_value(0.1), q_alpha.animate.set_value(0.25))
        self.play(p_alpha.animate.set_value(0.5), q_alpha.animate.set_value(0.25))
        self.play(p_alpha.animate.set_value(0.7), q_alpha.animate.set_value(0.8))
        self.play(p_alpha.animate.set_value(1), q_alpha.animate.set_value(1))
        self.wait()

        self.next_section("Move to (0,0)")
        self.play(Uncreate(trace))
        self.play(p_alpha.animate.set_value(0), q_alpha.animate.set_value(0))
        self.wait()

        self.next_section("Move to (1,1)")
        trace = TracedPath(free_space_dot.get_center, stroke_color=RED)
        self.add(trace)
        self.play(p_alpha.animate.set_value(0.1), q_alpha.animate.set_value(0.25))
        self.play(p_alpha.animate.set_value(0.2), q_alpha.animate.set_value(0.25))
        self.play(p_alpha.animate.set_value(0.4), q_alpha.animate.set_value(0.9))
        self.play(p_alpha.animate.set_value(1), q_alpha.animate.set_value(1))
        self.wait()

        self.next_section("Move to out of range point")
        self.play(p_alpha.animate.set_value(0.4), q_alpha.animate.set_value(0.9))
        self.wait()


def polygonal_curve(points: np.ndarray, t: float|np.ndarray) -> float|np.ndarray:       
    """Generates a linearly interpolated polygonal curve through points

    Args:
        points (np.ndarray): corner points of the polygonal curve
        t (float | np.ndarray): value of point(s) to be interpolated. Choose 0 for the first corner point, 1 for the second... All values in between, like 0.5, are interpolated between corner points.

    Raises:
        ValueError: The value of t is out of the definition range

    Returns:
        float|np.ndarray: the interpolated point(s)
    """
    if (np.min(t) < 0 or np.max(t) > len(points) -1):
        raise ValueError(f"t ({t}) is not in bounds of [{0}|{len(points) -1}]")
    
    x = points[np.floor(t).astype(np.int64)]
    y = points[np.ceil(t).astype(np.int64)]

    length_factors = np.mod(t,1)
    if isinstance(t, np.ndarray):
        length_factors = length_factors.reshape((len(t),1))
    partial_line_segment = (y-x) * length_factors
    point = x + partial_line_segment

    return point

class FreeSpaceDiagram(Scene):
    def construct(self):
        add_slide_number(self, 7)
        title = Text("Free Space Diagram", color=BLUE).to_edge(UP)
        self.add(title)

        self.next_section("Add Axes Diagrams")
        ax: Axes = Axes(x_range=[-1,1], y_range=[-1,1], x_length=5, y_length=5, tips=False)
        ax.set_color(BLACK).shift(3*LEFT)
        self.add(ax)

        # Draw plot of cell
        free_space_diagram_image = ImageMobject("manim_frechet_distance/assets/free_space_diagram_points_0_4.png")
        free_space_diagram_image.height = 5
        free_space_diagram_image.width = 5

        axes_free_space = Axes(
            x_range=[0,5,1],
            y_range=[0,5,1],
            x_length=5,
            y_length=5,
            tips=False,
            axis_config={"include_numbers": True}
        ).set_color(BLACK)

        ax_p_label = MathTex("\\alpha_P", color=BLACK).next_to(free_space_diagram_image, RIGHT).align_to(free_space_diagram_image, DOWN)
        ax_q_label = MathTex("\\alpha_Q", color=BLACK).next_to(free_space_diagram_image, UP).align_to(free_space_diagram_image, LEFT)
        diagram = Group(free_space_diagram_image, axes_free_space, ax_p_label, ax_q_label)
        diagram.shift(3.5*RIGHT + 0.5*DOWN)

        self.add(axes_free_space, ax_p_label, ax_q_label)
        self.wait()

        self.next_section("Add Curves")
        p_points = np.array([
            [-1, -0.5,0], [0.5, 0.5,0], [-0.5,1,0], [-0.5,-0.5,0], [0.4, -0.15,0], [0.6, -0.3, 0]
        ])
        alpha_p_range = [0, p_points.shape[0]-1]
        p_curve_func = partial(polygonal_curve, p_points)
        p_curve = ax.plot_parametric_curve(
            p_curve_func,
            t_range=alpha_p_range,
            color=RED,
        )

        q_points = np.array([
            [-0.5, -1,0], [-1,0,0], [0,0,0], [0,1,0], [-1,0.5,0], [0.5,-0.5,0]
        ])
        alpha_q_range = [0, q_points.shape[0]-1]
        q_curve_func = partial(polygonal_curve, q_points)
        q_curve = ax.plot_parametric_curve(
            q_curve_func,
            t_range=alpha_q_range,
            color=GREEN,
        )

        self.play(Create(p_curve))
        self.play(Create(q_curve))

        self.next_section("Add Free space diagram image")
        self.add(free_space_diagram_image)
        self.wait()

        self.next_section("Show epsilon value")
        epsilon = ValueTracker(0.4)
        epsilon_text = MathTex("\\varepsilon=", color=BLACK)
        epsilon_number =  DecimalNumber(epsilon.get_value(), color=BLACK).next_to(epsilon_text, RIGHT)
        epslion_group = VGroup(epsilon_text, epsilon_number)
        epslion_group.next_to(free_space_diagram_image, UP)
        epsilon_number.add_updater(lambda t: t.set_value(epsilon.get_value()))
        self.play(Write(epsilon_text), Write(epsilon_number))
        self.wait()

        self.next_section("Add moving points")
        p_dot = Dot(p_curve.point_from_proportion(0), color=BLACK)
        q_dot = Dot(q_curve.point_from_proportion(0), color=BLACK)
        dot: Dot = Dot(axes_free_space.c2p(0,0), color=BLACK).set_z_index(5)
        self.play(Create(p_dot), Create(q_dot), Create(dot))
        self.wait()
        
        p_alpha = ValueTracker(0)
        q_alpha = ValueTracker(0)
        p_dot.add_updater(lambda m: m.move_to(p_curve.point_from_proportion(p_alpha.get_value()/5.0)))
        q_dot.add_updater(lambda m: m.move_to(q_curve.point_from_proportion(q_alpha.get_value()/5.0)))
        dot.add_updater(lambda m: m.move_to(axes_free_space.c2p(p_alpha.get_value(), q_alpha.get_value())))


        self.next_section("Show distance and line")
        line = Line(p_dot.get_center(), q_dot.get_center(), color=BLACK)
        line.add_updater(lambda z: z.become(Line(p_dot.get_center(), q_dot.get_center(), color=BLACK)))
        self.play(Create(line))
        
        def dist_full(alphas: Tuple[float,float], p_point_from_proportion, q_point_from_proportion):
            p = p_point_from_proportion(alphas[0])
            q = q_point_from_proportion(alphas[1])
            d = np.linalg.norm(p-q, ord=2)
            return d

        def dist(alphas: np.ndarray):
            return dist_full(alphas, p_curve_func, q_curve_func)

        dist_text = Text("d=", color=BLACK)
        dist_number = DecimalNumber(dist([p_alpha.get_value(), q_alpha.get_value()]), color=BLACK).next_to(dist_text, RIGHT)
        dist_number.add_updater(lambda t: t.set_value(dist([p_alpha.get_value(), q_alpha.get_value()])))
        dist_number.add_updater(lambda t: t.next_to(dist_text, RIGHT))
        dist_group = VGroup(dist_text, dist_number)
        dist_group.next_to(ax, DOWN)
        self.play(Write(dist_text), Write(dist_number))
        self.wait()

        self.next_section("Increase epsilon value")
        free_space_diagram_image_bigger = ImageMobject("manim_frechet_distance/assets/free_space_diagram_points_0_71.png")
        free_space_diagram_image_bigger.height = free_space_diagram_image.height
        free_space_diagram_image_bigger.width = free_space_diagram_image.width
        free_space_diagram_image_bigger.move_to(free_space_diagram_image.get_center())
        self.play(epsilon.animate.set_value(0.71), Transform(free_space_diagram_image, free_space_diagram_image_bigger))
        self.wait()

        trace = TracedPath(dot.get_center, stroke_color=BLUE)
        self.add(trace)

        self.next_section("Move to (0.4,1.0) in free space")
        self.play(p_alpha.animate.set_value(0.4), q_alpha.animate.set_value(1))
        self.wait()

        self.next_section("Move to (1.0,2.0) in free space")
        self.play(p_alpha.animate.set_value(1.0), q_alpha.animate.set_value(2.0))
        self.wait()

        self.next_section("Move to (2.5,4.0) in free space")
        self.play(p_alpha.animate.set_value(2.5), q_alpha.animate.set_value(4.0))
        self.wait()

        self.next_section("Move to (3.0, 4.5) in free space")
        self.play(p_alpha.animate.set_value(3.0), q_alpha.animate.set_value(4.5))
        self.wait()

        self.next_section("Move to (5.0, 5.0) in free space")
        self.play(p_alpha.animate.set_value(5.0), q_alpha.animate.set_value(5.0))
        self.wait()

class FrechetDistanceAlgorithmicComplexity(Scene):
    def construct(self):
        add_slide_number(self, 8)
        title = Text("Algorithmic Complexity", color=BLUE).to_edge(UP)
        self.add(title)

        # for just a single cell
        self.next_section("Single cell")
        single_cell_text = Text("Single cell:", font_size=30).shift(5*LEFT + UP).set_color(BLACK)
        self.add(single_cell_text)
        self.wait()

        self.next_section("Up to 8 interscection points")
        up_to_8_intersec_points_text = Text("max 8 intersec. points", font_size=30).next_to(single_cell_text, DOWN).align_to(single_cell_text, LEFT).set_color(BLACK).shift(0.5*RIGHT)
        self.add(up_to_8_intersec_points_text)
        self.wait()

        self.next_section("Single cell time complexity")
        single_cell_time_complexity = MathTex(r"\mathcal{O}(1)").set_color(BLACK).next_to(single_cell_text, RIGHT)
        self.play(Write(single_cell_time_complexity))
        self.wait()

        # The decision probelm
        self.next_section("Decision Problem")
        decision_problem_text = Text("Decision Problem:", font_size=30).next_to(single_cell_text, DOWN).align_to(single_cell_text, LEFT).shift(1.5*DOWN).set_color(BLACK)
        self.add(decision_problem_text)
        self.wait()

        self.next_section("Decision Problem formula")
        decision_problem = MathTex(r"\delta_{F}(P,Q) \leq \varepsilon").set_color(BLACK).next_to(decision_problem_text, DOWN).align_to(decision_problem_text, LEFT).shift(0.5*RIGHT)
        self.play(Write(decision_problem))
        self.wait()

        self.next_section("Decision Problem p by q")
        decision_problem_p_by_q = Text("p by q cells", font_size=30).next_to(decision_problem, DOWN).align_to(decision_problem, LEFT).set_color(BLACK)
        self.add(decision_problem_p_by_q)
        self.wait()

        self.next_section("Decision Problem time complexity")
        decision_problem_time_complexity = MathTex(r"\mathcal{O}(pq)").set_color(BLACK).next_to(decision_problem_text, RIGHT)
        self.play(Write(decision_problem_time_complexity))
        self.wait()
        
        # Complete Solution: binary search bits
        self.next_section("Binary search the bits")
        binary_search_bits_text = Text("Binary search bits", font_size=30).shift(2*RIGHT + UP).set_color(BLACK)
        self.add(binary_search_bits_text)
        self.wait()

        self.next_section("Binary search the bits time complexity")
        binary_search_bits_complexity = MathTex(r"\mathcal{O}(","T_{dec}",r"\cdot \log(\text{``accuracy bits''}))").set_color(BLACK).next_to(binary_search_bits_text, DOWN).align_to(binary_search_bits_text, LEFT).shift(0.5*RIGHT)
        self.play(Write(binary_search_bits_complexity))
        self.wait()

        self.next_section("Binary search the bits time complexity full")
        binary_search_bits_complexity_with_pq = MathTex(r"\mathcal{O}(","pq",r"\cdot \log(\text{``accuracy bits''}))").set_color(BLACK).next_to(binary_search_bits_text, DOWN).align_to(binary_search_bits_text, LEFT).shift(0.5*RIGHT)
        self.play(Indicate(decision_problem_time_complexity))
        self.play(TransformMatchingTex(binary_search_bits_complexity, binary_search_bits_complexity_with_pq))
        self.wait()

        self.next_section("Binary search the bits time complexity full")
        binary_search_bits_complexity_full = MathTex(r"\mathcal{O}(","pq",r"\cdot 32)").set_color(BLACK).next_to(binary_search_bits_text, DOWN).align_to(binary_search_bits_text, LEFT).shift(0.5*RIGHT)
        self.play(TransformMatchingTex(binary_search_bits_complexity_with_pq, binary_search_bits_complexity_full))
        self.wait()

        # Complete solution: using critical values
        self.next_section("Critical values")
        critical_values_text = Text("Critical values", font_size=30).next_to(binary_search_bits_text, DOWN).align_to(binary_search_bits_text, LEFT).shift(1.5*DOWN).set_color(BLACK)
        self.add(critical_values_text)
        self.wait()

        self.next_section("Number of Critical values")
        number_of_critical_values = MathTex(r"\text{\#} \mathcal{O}(p^2q + pq^2)").set_color(BLACK).next_to(critical_values_text, DOWN).align_to(critical_values_text, LEFT).shift(0.5*RIGHT)
        self.play(Write(number_of_critical_values))
        self.wait()

        self.next_section("Critical values time complexity")
        critical_values_time_complexity = MathTex(r"\mathcal{O}((p^2q + pq^2) \log (pq))").set_color(BLACK).next_to(number_of_critical_values, DOWN).align_to(number_of_critical_values, LEFT)
        self.play(Write(critical_values_time_complexity))
        self.wait()

        self.next_section("Parametric search time complexity")
        parametric_search_time_complexity = MathTex(r"\mathcal{O}(",r"pq \log (pq)",r")").set_color(BLACK).next_to(critical_values_time_complexity, DOWN).align_to(critical_values_time_complexity, LEFT)
        self.play(critical_values_time_complexity.animate.set_color(GRAY_B), Write(parametric_search_time_complexity))
        self.wait()

        self.next_section("Parametric search time complexity with n")
        parametric_search_time_complexity_with_n = MathTex(r"\mathcal{O}(",r"n^2 \log (n)",r")").set_color(BLACK).next_to(critical_values_time_complexity, DOWN).align_to(critical_values_time_complexity, LEFT)
        self.play(TransformMatchingTex(parametric_search_time_complexity, parametric_search_time_complexity_with_n))
        self.wait()


class DiscreteFrechetDistanceIntro(Scene):
    def construct(self):
        add_slide_number(self, 9)
        title = Text("Discrete Fréchet Distance", color=BLUE).to_edge(UP)
        self.add(title)

        self.next_section("P line segment")
        p_points = np.array([
            [-5.25,  0.25,  0.  ],
            [-2.25,  0.25,  0.  ],
            [-1.5 ,  1.75,  0.  ],
            [-0.9 ,  1.75,  0.  ],
            [-0.6 ,  0.4 ,  0.  ],
            [ 0.75,  1.75,  0.  ],
            [ 1.5 ,  1.  ,  0.  ],
            [ 3.  ,  0.25,  0.  ],
            [ 3.9 ,  0.7 ,  0.  ],
        ])
        alpha_p_range = [0, p_points.shape[0]-1]
        p_curve_func = partial(polygonal_curve, p_points)
        p_curve = ParametricFunction(
            p_curve_func,
            t_range=alpha_p_range,
            color=RED,
        )

        self.next_section("Q line segment")
        q_points = np.array([
            [-5.25,  -1.25,  0.  ],
            [-4.5 , -0.5 ,  0.  ],
            [-2.25, -0.5 ,  0.  ],
            [-1.2 ,  0.4 ,  0.  ],
            [-0.75, -0.5 ,  0.  ],
            [ 2.25,  1.  ,  0.  ],
            [ 3.  ,  1.  ,  0.  ],
            [ 3.9 , -0.2 ,  0.  ],
        ])
        alpha_q_range = [0, q_points.shape[0]-1]
        q_curve_func = partial(polygonal_curve, q_points)
        q_curve = ParametricFunction(
            q_curve_func,
            t_range=alpha_q_range,
            color=GREEN,
        )

        self.play(Create(p_curve))
        self.play(Create(q_curve))


        self.next_section("Distance line")
        frog_p = ImageMobject("manim_frechet_distance/assets/icons8-frog-90.png")
        frog_p_alpha = ValueTracker(0)
        frog_p = frog_p.move_to(p_curve_func(0))
        frog_p.add_updater(lambda m: m.move_to(p_curve_func(frog_p_alpha.get_value())))
        self.add(frog_p)

        frog_q = ImageMobject("manim_frechet_distance/assets/icons8-frog-90.png")
        frog_q_alpha = ValueTracker(0)
        frog_q = frog_q.move_to(p_curve_func(0))
        frog_q.add_updater(lambda m: m.move_to(q_curve_func(frog_q_alpha.get_value())))
        self.add(frog_q)


        self.next_section("Add moving points")

        line = Line(frog_p.get_center(), frog_q.get_center(), color=BLACK)
        line.add_updater(lambda z: z.become(Line(frog_p.get_center(), frog_q.get_center(), color=z.get_color())))
        self.play(Create(line))
        
        def dist_full(alphas: Tuple[float,float], p_point_from_proportion, q_point_from_proportion):
            p = p_point_from_proportion(alphas[0])
            q = q_point_from_proportion(alphas[1])
            d = np.linalg.norm(p-q, ord=2)
            return d

        def dist(alphas: np.ndarray):
            return dist_full(alphas, p_curve_func, q_curve_func) / 2 # adjust for figure scaling


        dist_text = Text("d=", color=BLACK).to_edge(RIGHT).shift(LEFT)
        dist_number = DecimalNumber(dist([frog_p_alpha.get_value(), frog_q_alpha.get_value()]), color=BLACK).next_to(dist_text, RIGHT)
        dist_number.add_updater(lambda t: t.set_value(dist([frog_p_alpha.get_value(), frog_q_alpha.get_value()])))
        dist_number.add_updater(lambda t: t.next_to(dist_text, RIGHT))
        self.play(Write(dist_text), Write(dist_number))
        self.wait()

        self.next_section("Add criteria text")
        t1 = Text("Jump up to next vertex", color=BLACK, font_size=35).shift(2*DOWN)
        self.add(t1)
        self.wait()

        self.next_section("Move one frog")
        frog_q_alpha.set_value(1)
        self.wait()

        self.next_section("Add criteria text")
        t2 = Text("Jump simultaneously", color=BLACK, font_size=35).next_to(t1, DOWN).align_to(t1, LEFT)
        self.add(t2)
        self.wait()
        
        self.next_section("Move both frogs")
        frog_p_alpha.set_value(1)
        frog_q_alpha.set_value(2)
        self.wait()

        self.next_section("Add criteria text")
        t3 = Text("Can't skip verticies", color=BLACK, font_size=35).next_to(t2, DOWN).align_to(t1, LEFT)
        self.add(t3)
        self.wait()

        self.next_section("Move one frog")
        frog_q_alpha.set_value(3)
        self.wait()

        self.next_section("Move one frog")
        frog_p_alpha.set_value(2)
        self.wait()

        self.next_section("Move one frog")
        frog_p_alpha.set_value(3)
        self.wait()

        self.next_section("Move one frog")
        frog_p_alpha.set_value(4)
        self.wait()

        self.next_section("Move one frog")
        frog_q_alpha.set_value(4)
        self.wait()

        self.next_section("Move both frogs")
        frog_p_alpha.set_value(5)
        frog_q_alpha.set_value(5)
        self.wait()

        self.next_section("Move one frog")
        frog_p_alpha.set_value(6)
        self.wait()

        self.next_section("Move one frog")
        frog_p_alpha.set_value(7)
        self.wait()

        self.next_section("Move one frog")
        frog_q_alpha.set_value(6)
        self.wait()

        self.next_section("Frogs to endpoint")
        frog_p_alpha.set_value(8)
        frog_q_alpha.set_value(7)
        self.wait()

class DiscreteFrechetDistanceAlgorithm(Scene):
    def construct(self):
        add_slide_number(self, 10)
        title = Text("Computing Discrete Fréchet Distance", color=BLUE).to_edge(UP)
        self.add(title)

        self.next_section("Steps")
        blist = BulletedList("Partial Curves", "Dynamic Programming", "Recursive Formula")
        blist.set_color(BLACK).shift(3*LEFT+UP)
        self.add(blist)
        self.wait()

        self.next_section("Recursive formula")
        recursive_formula = Tex(r"""
            \begin{align*}
                c(i,j) &= \begin{cases}
                dist(u_1, v_1), &\text{if } i=1 \text{and } j=1 \\
                \max \{c(i-1,1), dist(u_i, v_1)\}, &\text{if } i>1 \text{and } j=1 \\
                \max \{c(1,j-1), dist(u_1, v_j)\}, &\text{if } i=1 \text{and } j>1 \\
                \max \{c(i-1,j), c(i,j-1), c(i-1,j-1), dist(u_i, v_j)\}, &\text{if } i>1 \text{and } j>1
                \end{cases} \\
                &= \delta_{dF}(P',Q')
            \end{align*}
        """).shift(2*DOWN).set_color(BLACK).scale(0.7)
        self.add(recursive_formula)
        self.wait()

        self.next_section("Computation table")
        computation_table: Table = Table(
            [["c(i-1,j)", "c(i,j)"],
            ["c(i-1,j-1)", "c(i,j-1)"]],
            include_outer_lines=True).set_color(BLACK).shift(UP+3*RIGHT).scale(0.6)
        self.add(computation_table)
        self.wait()

        self.next_section("Computation step")
        
        arrows = [
            Arrow(start=computation_table.get_entries((1,1)).get_center(), end=computation_table.get_entries((1,2)).get_center(), buff=SMALL_BUFF, color=RED),
            Arrow(start=computation_table.get_entries((2,2)).get_center(), end=computation_table.get_entries((1,2)).get_center(), buff=SMALL_BUFF, color=RED, stroke_width=10, max_stroke_width_to_length_ratio=20),
            Arrow(start=computation_table.get_entries((2,1)).get_center(), end=computation_table.get_entries((1,2)).get_center(), buff=SMALL_BUFF, color=RED),
        ]
        self.play(*[Create(a) for a in arrows])
        self.wait()
        




class DiscreteFrechetDistanceAlgorithmicComplexity(Scene):
    def construct(self):
        add_slide_number(self, 11)
        title = Text("Algorithmic Complexity", color=BLUE).to_edge(UP)
        self.add(title)

        time_text = Text("Time: ", font_size=30).set_color(BLACK).shift(3*LEFT)
        time_formula = MathTex(r"\mathcal{O}(pq)").next_to(time_text, RIGHT).set_color(BLACK)
        space_text = Text("Space: ", font_size=30).next_to(time_text, DOWN).align_to(time_text, LEFT).set_color(BLACK)
        space_formula = MathTex(r"\mathcal{O}(min(p,q))").next_to(space_text, RIGHT).set_color(BLACK)

        self.add(time_text, time_formula, space_text, space_formula)
        self.wait()

class RecentDevelopments(Scene):
    def construct(self):
        add_slide_number(self, 12)
        title = Text("Recent Developments", color=BLUE).to_edge(UP)
        self.add(title)


        # Cointinous Fréchet distance
        self.next_section("Alt and Godau, 92/95")
        alt_and_godau_text = Text("Alt and Godau, 92/95:", font_size=30).shift(3*LEFT + 2*UP).set_color(BLACK)
        self.add(alt_and_godau_text)
        self.wait()

        self.next_section("Alt and Godau 92/95 time complexity")
        alt_and_godau_time_complexity = MathTex(r"\mathcal{O}(n^2 \log n)").set_color(BLACK).next_to(alt_and_godau_text, RIGHT)
        self.play(Write(alt_and_godau_time_complexity))
        self.wait()


        self.next_section("Buchin et al 2014")
        buchin_text = Text("Buchin et al., 2014:", font_size=30).set_color(BLACK).next_to(alt_and_godau_text, DOWN).align_to(alt_and_godau_text, LEFT)
        self.add(buchin_text)
        self.wait()

        self.next_section("Buchin et al 2014 time complexity")
        buchin_text_time = MathTex(r"\mathcal{O}(n^2 \sqrt{\log n} (\log \log n)^{1.5})").set_color(BLACK).next_to(buchin_text, RIGHT)
        self.play(Write(buchin_text_time))
        self.wait()
        
        self.next_section("Bringmann 2014")
        bringmann_text = Text("Bringmann, 2014: No strongly subquadratic algorithm", font_size=30).set_color(BLACK).next_to(buchin_text, DOWN).align_to(buchin_text, LEFT)
        self.add(bringmann_text)
        self.wait()

        # Discrete Fréchet distance
        self.next_section("Eiter and Mannila 94")
        eiter_and_mannila_text = Text("Eiter and Mannila, 94:", font_size=30).set_color(BLACK).next_to(bringmann_text, DOWN).align_to(bringmann_text, LEFT).shift(0.7*DOWN)
        self.add(eiter_and_mannila_text)
        self.wait()

        self.next_section("Eiter and Mannila 94")
        eiter_and_mannila_time = MathTex(r"\mathcal{O}(n^2)").set_color(BLACK).next_to(eiter_and_mannila_text, RIGHT)
        self.play(Write(eiter_and_mannila_time))
        self.wait()

        self.next_section("Agarwal et al.")
        agarwal_text = Text("Agarwal et al., 2018:", font_size=30).set_color(BLACK).next_to(eiter_and_mannila_text, DOWN).align_to(eiter_and_mannila_text, LEFT).shift(0.3*DOWN)
        self.add(agarwal_text)
        self.wait()

        self.next_section("Agarwal et al.")
        eiter_and_mannila_time = MathTex(r"\mathcal{O}\left(\frac{n^2 \log \log n}{\log n}\right)").set_color(BLACK).next_to(agarwal_text, RIGHT)
        self.play(Write(eiter_and_mannila_time))
        self.wait()

        
        self.next_section("Current research")
        current_research_text = Paragraph(
            "Approximation algorithms", "Uncertain curves", "Efficient implementation",
            font_size=30, color=BLACK).shift(3*DOWN).align_to(agarwal_text, LEFT)
        self.add(current_research_text)
        self.wait()



# class FrechetDistanceExample(Scene):
#     def construct(self):
#         ax = Axes(
#             x_range=[0, 10], y_range=[0, 100, 10], axis_config={"include_tip": False, "include_numbers": True}
#         )
#         labels = ax.get_axis_labels(x_label="x", y_label="y")

#         self.add(ax, labels)
#         self.next_section("Axes", PresentationSectionType.NORMAL)
        
        
#         x1 = ValueTracker(0)
#         x2 = ValueTracker(0)

#         def func1(x):
#             return 2 * (x - 5) ** 2
#         def func2(x):
#             return -1.5 * (x - 2) ** 2 + 81
#         graph1 = ax.plot(func1, color=MAROON)
#         graph2 = ax.plot(func2, color=BLUE)

#         self.next_section("Function 1")
#         self.play(Create(graph1))

#         self.next_section("Function 2")
#         self.play(Create(graph2))


#         initial_point1 = [ax.coords_to_point(x1.get_value(), func1(x1.get_value()))]
#         dot1 = Dot(point=initial_point1)
#         dot1.add_updater(lambda x: x.move_to(ax.c2p(x1.get_value(), func1(x1.get_value()))))

#         initial_point2 = [ax.coords_to_point(x2.get_value(), func2(x2.get_value()))]
#         dot2 = Dot(point=initial_point2)
#         dot2.add_updater(lambda x: x.move_to(ax.c2p(x2.get_value(), func2(x2.get_value()))))
#         dot1.set_z_index(1)
#         dot2.set_z_index(1)

#         self.next_section("Points")
#         self.play(Create(dot1), Create(dot2))

#         self.next_section("Line")
#         line = Line(dot1.get_center(), dot2.get_center()).set_color(ORANGE)
#         line.add_updater(lambda z: z.become(Line(dot1.get_center(), dot2.get_center(), color=ORANGE)))
#         self.play(Create(line))

#         def dist():
#             d = np.sqrt((x1.get_value() - x2.get_value())**2 + (func1(x1.get_value()) - func2(x2.get_value()))**2)
#             return d
#         distNumber = DecimalNumber(dist()).next_to(line.get_center(), RIGHT)
#         distNumber.add_updater(lambda t: t.set_value(dist()))
#         distNumber.add_updater(lambda t: t.next_to(line.get_center(), RIGHT))
#         self.play(Create(distNumber))
#         self.wait(1)

#         x_space = np.linspace(*ax.x_range[:2],200)
#         minimum_index = func1(x_space).argmin()

#         self.next_section("Minimum 1", PresentationSectionType.NORMAL)
#         self.play(x1.animate.set_value(x_space[minimum_index]), run_time=2)
#         self.wait(1)

#         self.next_section("Minimum 2", PresentationSectionType.NORMAL)
#         self.play(x2.animate.set_value(x_space[minimum_index]), run_time=2)
#         self.wait(1)

#         self.next_section("Together to 0", PresentationSectionType.NORMAL)
#         self.play(x1.animate.set_value(0), x2.animate.set_value(0), run_time=3, rate_func=smooth)
#         self.wait(1)

#         self.next_section("Max vertical dist", PresentationSectionType.NORMAL)
#         self.play(x1.animate.set_value(26/7), x2.animate.set_value(26/7), run_time=2)
#         self.wait(1)

#         self.next_section("Max vertical dist right", PresentationSectionType.NORMAL)
#         self.play(x1.animate.set_value(26/7+0.5), x2.animate.set_value(26/7+0.5))

#         self.next_section("Max vertical dist left", PresentationSectionType.NORMAL)
#         self.play(x1.animate.set_value(26/7-0.5), x2.animate.set_value(26/7-0.5))
        
#         self.next_section("Max vertical dist", PresentationSectionType.NORMAL)
#         self.play(x1.animate.set_value(26/7), x2.animate.set_value(26/7))
#         self.wait(1)

#         self.next_section("Diagonal", PresentationSectionType.NORMAL)
#         self.play(x1.animate.set_value(26/7-0.1), x2.animate.set_value(26/7+0.1))
#         self.wait(1)



