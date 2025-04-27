from manim import *
import numpy as np

# Introspection block for Scene
# print(dir(Scene))
# Available methods/attributes include: add, play, wait, remove, clear, render, camera, mobjects

# Introspection block for Circle
# print(dir(Circle))
# Available methods/attributes include: move_to, shift, scale, rotate, set_color, set_fill, set_stroke

# Introspection block for Polygon
# print(dir(Polygon))
# Available methods/attributes include: move_to, shift, scale, rotate, set_color, set_fill, set_stroke

# Introspection block for NumberLine
# print(dir(NumberLine))
# Available methods/attributes include: add_labels, get_tick_marks, get_number_mobjects, number_to_point, point_to_number

# Introspection block for Line
# print(dir(Line))
# Available methods/attributes include: set_points_by_ends, set_angle, move_to, shift, scale, rotate, set_color, set_stroke

# Introspection block for DashedLine
# print(dir(DashedLine))
# Available methods/attributes include: set_points_by_ends, move_to, shift, scale, rotate, set_color, set_stroke

# Introspection block for Text
# print(dir(Text))
# Available methods/attributes include: set_text, set_color, scale, move_to, shift, rotate

# Introspection block for ValueTracker
# print(dir(ValueTracker))
# Available methods/attributes include: get_value, set_value, animate

# Introspection block for always
# print(dir(always))
# 'always' is not a class or function that needs introspection.  It's a helper.

class TheoremScene(Scene):
    def construct(self):
        # Scene 1: The Setup and the Average Journey
        ax = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 5, 1],
            axis_config={"color": "#FFFFFF"},
        )
        labels = ax.get_axis_labels(x_label="x", y_label="y")
        self.add(ax, labels)

        a_val = 1
        b_val = 8

        def func(x):
            return 0.1 * (x - 2)**3 + 2

        path = ax.plot(func, x_range=[a_val, b_val], color="#00FF00")

        start_point = ax.coords_to_point(a_val, func(a_val))
        end_point = ax.coords_to_point(b_val, func(b_val))
        
        start_dot = Dot(start_point, color="#FFFF00")
        end_dot = Dot(end_point, color="#FFFF00")
        
        a_label = Text("a", color="#FFFFFF").next_to(ax.coords_to_point(a_val, 0), DOWN)
        b_label = Text("b", color="#FFFFFF").next_to(ax.coords_to_point(b_val, 0), DOWN)

        self.add(start_dot, end_dot, a_label, b_label)

        average_line = Line(start_point, end_point, color="#FF0000")
        average_line_label = Text("Average Line", color="#FF0000").next_to(average_line, UP)

        self.play(Create(average_line), Write(average_line_label))
        self.wait(1)

        # Scene 2: Finding the Instantaneous Match
        ruler = Line(start=LEFT * 0.5, right=RIGHT * 0.5, color="#00FFFF")
        
        # ValueTracker to move the ruler along the path
        ruler_tracker = ValueTracker(a_val + 0.1)
        
        def update_ruler(ruler):
            x = ruler_tracker.get_value()
            point_on_path = ax.coords_to_point(x, func(x))
            
            # Approximate tangent by taking a small step
            delta = 0.01
            point_ahead = ax.coords_to_point(x + delta, func(x + delta))
            
            # Calculate angle
            angle = np.arctan2(point_ahead[1] - point_on_path[1], point_ahead[0] - point_on_path[0])
            
            ruler.move_to(point_on_path)
            ruler.set_angle(angle)
            return ruler
        
        ruler.add_updater(update_ruler)
        self.add(ruler)
        
        self.play(ruler_tracker.animate.set_value(b_val - 0.1), run_time=5, rate_func=linear)
        self.wait(1)

        # Find a suitable 'c' (approximate by visual inspection)
        c_val = 4.5  # Eyeballed from the animation

        c_point = ax.coords_to_point(c_val, func(c_val))
        c_label = Text("c", color="#FFFFFF").next_to(ax.coords_to_point(c_val, 0), DOWN)
        
        dashed_line = DashedLine(ax.coords_to_point(c_val, 0), c_point, color="#FFFFFF")
        
        match_dot = Dot(c_point, color="#00FFFF")

        self.play(Create(dashed_line), Write(c_label), Create(match_dot))
        self.wait(2)