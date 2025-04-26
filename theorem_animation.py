from manim import *

import numpy as np


class TheoremScene(Scene):
    def construct(self):
        # Define points for the triangle
        A = np.array([0, 0, 0])
        B = np.array([3, 0, 0])
        C = np.array([1.5, 2, 0])

        # Create the triangle
        triangle = Polygon(A, B, C, color=BLUE)
        self.add(triangle)

        # Create angle bisector at A
        line_AB = Line(A, B)
        line_AC = Line(A, C)
        angle_A = np.arctan2(C[1] - A[1], C[0] - A[0]) - np.arctan2(B[1] - A[1], B[0] - A[0])
        angle_A_degrees = angle_A * 180 / np.pi

        # Angle A and Angle A/2
        arc_radius = 0.5
        angle_arc = Circle(radius=arc_radius, color=GREEN).move_to(A)
        angle_arc.set_points(angle_arc.get_points()[
                             (len(angle_arc.get_points()) * int(-angle_A_degrees / 2)) // 360:
                             (len(angle_arc.get_points()) * int(0)) // 360
                             ])
        angle_arc_label = MathTex(r"\alpha").scale(0.7).move_to(angle_arc.point_from_proportion(0.5))

        angle_bisector_arc = Circle(radius=arc_radius + 0.2, color=YELLOW).move_to(A)
        angle_bisector_arc.set_points(angle_bisector_arc.get_points()[
                                      (len(angle_bisector_arc.get_points()) * int(-angle_A_degrees / 4)) // 360:
                                      (len(angle_bisector_arc.get_points()) * int(0)) // 360
                                      ])
        angle_bisector_arc_label = MathTex(r"\frac{\alpha}{2}").scale(0.7).move_to(
            angle_bisector_arc.point_from_proportion(0.5))

        angle_bisector = Line(A, C, color=RED)
        angle_bisector.rotate(-angle_A / 2, about_point=A)

        # Add objects to the scene
        self.add(angle_arc, angle_arc_label)
        self.add(angle_bisector_arc, angle_bisector_arc_label)
        self.add(angle_bisector)

        # Create angle bisector at B
        line_BA = Line(B, A)
        line_BC = Line(B, C)
        angle_B = np.arctan2(A[1] - B[1], A[0] - B[0]) - np.arctan2(C[1] - B[1], C[0] - B[0])
        angle_B_degrees = angle_B * 180 / np.pi

        # Angle B and Angle B/2
        arc_radius = 0.5
        angle_arc = Circle(radius=arc_radius, color=GREEN).move_to(B)
        angle_arc.set_points(angle_arc.get_points()[
                             (len(angle_arc.get_points()) * int(-angle_B_degrees / 2)) // 360:
                             (len(angle_arc.get_points()) * int(0)) // 360
                             ])
        angle_arc_label = MathTex(r"\beta").scale(0.7).move_to(angle_arc.point_from_proportion(0.5))

        angle_bisector_arc = Circle(radius=arc_radius + 0.2, color=YELLOW).move_to(B)
        angle_bisector_arc.set_points(angle_bisector_arc.get_points()[
                                      (len(angle_bisector_arc.get_points()) * int(-angle_B_degrees / 4)) // 360:
                                      (len(angle_bisector_arc.get_points()) * int(0)) // 360
                                      ])
        angle_bisector_arc_label = MathTex(r"\frac{\beta}{2}").scale(0.7).move_to(
            angle_bisector_arc.point_from_proportion(0.5))

        angle_bisector = Line(B, C, color=PURPLE)
        angle_bisector.rotate(angle_B / 2, about_point=B)

        # Add objects to the scene
        self.add(angle_arc, angle_arc_label)
        self.add(angle_bisector_arc, angle_bisector_arc_label)
        self.add(angle_bisector)

        # Intersection point of angle bisectors
        intersection_point = np.array([1.2, 0.9, 0])
        intersection_dot = Dot(intersection_point, color=ORANGE)
        intersection_label = MathTex("I", color=ORANGE).next_to(intersection_dot, UP)

        self.add(intersection_dot, intersection_label)

        # Perpendicular distance from I to AB
        perpendicular_line = DashedLine(intersection_point, np.array([intersection_point[0], 0, 0]), color=GREEN)
        perpendicular_dot = Dot(np.array([intersection_point[0], 0, 0]), color=GREEN)

        self.add(perpendicular_line, perpendicular_dot)