import pygame
from pygame import gfxdraw
import typing
from GLib.color import Color
from copy import copy
from GLib.mathematics import *


class Draw:
    @classmethod
    def __outline(self, _color, _width, _type, _surf, **vargs):
        if _type == "rect":
            radius = vargs["radius"]
            pos = vargs["pos"]
            size = vargs["size"]
            Draw.draw_rect(_surf, pos, size, _color, _width, radius=radius)
        elif _type == "circle":
            radius = vargs["radius"]
            pos = vargs["pos"]
            Draw.draw_circle(_surf, pos, radius, _color, _width)
        elif _type == "polygone":
            points = vargs["points"]
            Draw.draw_alines(_surf, points, _color, _width, True)

    @staticmethod
    def draw_rect(
            surface: pygame.Surface,
            pos: list[int],
            size: list[int],
            color: list | str | Color = "gray",
            width: int = 0,
            radius: int = -1,
            outline: typing.Tuple[list | str | Color, int] = None,
    ) -> None:
        if len(size) == 1:
            size = [size[0], size[0]]
        if isinstance(radius, (list, tuple)):
            lt_rad = radius[0]
            rt_rad = radius[1]
            rb_rad = radius[2]
            lb_rad = radius[3]
            radius = -1
        else:
            lt_rad = radius
            rt_rad = radius
            rb_rad = radius
            lb_rad = radius
        if isinstance(color, Color):
            color = color.rgb
        pygame.draw.rect(
            surface, color, (pos, size), width, radius, lt_rad, rt_rad, lb_rad, rb_rad
        )

        if outline is not None:
            Draw.__outline(
                outline[0],
                outline[1],
                "rect",
                surface,
                radius=(lt_rad, rt_rad, rb_rad, lb_rad),
                pos=pos,
                size=size,
            )

    @staticmethod
    def draw_rc_rect(
            surf: pygame.Surface,
            center: list[int],
            size: list[int],
            angle: float = 0,
            color: list | str | Color = "gray",
            width: int = 0,
            outline: typing.Tuple[list | str | Color, int] = None,
    ):

        normal_vector = Vector2(0, 20)
        normal_vector.set_angle(angle)
        normal_vector.normalyze()

        left_rigth_vector = copy(normal_vector)
        left_rigth_vector.rotate(90)

        center_vector = Vector2(center)

        normal_vector *= size[0] / 2
        left_rigth_vector *= size[1] / 2
        pos1 = [
            center_vector.x + normal_vector.x + left_rigth_vector.x,
            center_vector.y + normal_vector.y + left_rigth_vector.y,
        ]
        pos2 = [
            center_vector.x + normal_vector.x - left_rigth_vector.x,
            center_vector.y + normal_vector.y - left_rigth_vector.y,
        ]
        pos3 = [
            center_vector.x - normal_vector.x + left_rigth_vector.x,
            center_vector.y - normal_vector.y + left_rigth_vector.y,
        ]
        pos4 = [
            center_vector.x - normal_vector.x - left_rigth_vector.x,
            center_vector.y - normal_vector.y - left_rigth_vector.y,
        ]

        Draw.draw_polygone(surf, [pos1, pos2, pos4, pos3], color, width, outline)

    @staticmethod
    def draw_rc_triangle(
            surf: pygame.Surface,
            center: list[int],
            size: list[int],
            angle: float = 0,
            color: list | str | Color = "gray",
            width: int = 0,
            outline: typing.Tuple[list | str | Color, int] = None,
    ):
        normal_vector = Vector2(0, 20)
        normal_vector.set_angle(angle)
        normal_vector.normalyze()

        left_rigth_vector = copy(normal_vector)
        left_rigth_vector.rotate(90)

        center_vector = Vector2(center)

        normal_vector *= size[0] / 2
        left_rigth_vector *= size[1] / 2
        pos1 = [
            center_vector.x - normal_vector.x + left_rigth_vector.x,
            center_vector.y - normal_vector.y + left_rigth_vector.y,
        ]
        pos2 = [
            center_vector.x - normal_vector.x - left_rigth_vector.x,
            center_vector.y - normal_vector.y - left_rigth_vector.y,
        ]
        pos4 = [
            center_vector.x + normal_vector.x,
            center_vector.y + normal_vector.y,
        ]

        Draw.draw_polygone(surf, [pos1, pos2, pos4], color, width, outline)

    @staticmethod
    def draw_rp_line(
            surf: pygame.Surface,
            pos: list[int],
            lenght: int = 100,
            angle: float = 0,
            color: list | str | Color = "gray",
            width: int = 1,
            circled: bool = True
    ):
        normal_vector = Vector2(0, 100)
        normal_vector.normalyze()

        normal_vector *= lenght
        normal_vector.set_angle(angle)

        Draw.draw_aline(surf, pos, [pos[0] + normal_vector.x, pos[1] + normal_vector.y], color, width, circled)

    @staticmethod
    def draw_rc_line(
            surf: pygame.Surface,
            center: list[int],
            lenght: int = 100,
            angle: float = 0,
            color: list | str | Color = "gray",
            width: int = 1
    ):
        normal_vector = Vector2(0, 100)
        normal_vector.normalyze()

        normal_vector *= lenght / 2
        normal_vector.set_angle(angle)

        Draw.draw_aline(surf, [center[0] - normal_vector.x, center[1] - normal_vector.y],
                        [center[0] + normal_vector.x, center[1] + normal_vector.y], color, width)

    @staticmethod
    def draw_circle(

            surface: pygame.Surface,
            pos: list[int],
            radius: int,
            color: list | str | Color = "gray",
            width: int = 0,
            outline: typing.Tuple[list | str | Color, int] = None,
            centering: bool = False,
    ) -> None:
        if isinstance(color, Color):
            color = color.rgb
        pygame.draw.circle(surface, color, pos, radius, width)
        if centering:
            pos = [pos[0] + radius, pos[1] + radius]

        if outline is not None:
            Draw.__outline(
                outline[0], outline[1], "circle", surface, pos=pos, radius=radius
            )

    @staticmethod
    def draw_polygone(

            surface: pygame.Surface,
            points: list[list[int]],
            color: list | str | Color = "gray",
            width: int = 0,
            outline: typing.Tuple[list | str | Color, int] = None,
    ) -> None:
        if isinstance(color, Color):
            color = color.rgb
        pygame.draw.polygon(surface, color, points, width)

        if outline is not None:
            Draw.__outline(outline[0], outline[1], "polygone", surface, points=points)

    @staticmethod
    def draw_line(

            surface: pygame.Surface,
            point_1: list | tuple | Vector2,
            point_2: list | tuple | Vector2,
            color: list | str | Color = "gray",
            width: int = 1,
    ) -> None:

        if isinstance(color, Color):
            color = color.rgb
        if isinstance(point_1, Vector2):
            pos1 = point_1.xy
        elif isinstance(point_1, (list, tuple)):
            pos1 = point_1
        if isinstance(point_2, Vector2):
            pos2 = point_2.xy
        elif isinstance(point_2, (list, tuple)):
            pos2 = point_2
        pygame.draw.line(surface, color, pos1, pos2, width)

    @staticmethod
    def draw_vector_line(
            surface: pygame.Surface,
            pos: list | tuple | Vector2,
            vector: Vector2,
            color: list | str | Color = 'gray',
            width: int = 1
    ):
        start_pos = pos
        end_pos = posing(start_pos, vector.x, vector.y)

        left_vector = copy(vector)
        right_vector = copy(vector)
        left_vector.normalyze()
        right_vector.normalyze()
        left_vector *= (18 + width)
        right_vector *= (18 + width)
        left_vector.rotate(150)
        right_vector.rotate(-150)
        Draw.draw_aline(surface, start_pos, end_pos, color, width)
        Draw.draw_aline(surface, end_pos, [end_pos[0] + right_vector.x, end_pos[1] + right_vector.y], color, width)
        Draw.draw_aline(surface, end_pos, [end_pos[0] + left_vector.x, end_pos[1] + left_vector.y], color, width)

    @staticmethod
    def draw_aline(

            surface: pygame.Surface,
            point_1: list | tuple | Vector2,
            point_2: list | tuple | Vector2,
            color: list | str | Color = 'gray',
            width=2,
            circled: bool = True

    ) -> None:
        if isinstance(color, Color):
            color = color.rgb
        if isinstance(point_1, Vector2):
            pos1 = point_1.xy
        elif isinstance(point_1, (list, tuple)):
            pos1 = point_1
        if isinstance(point_2, Vector2):
            pos2 = point_2.xy
        elif isinstance(point_2, (list, tuple)):
            pos2 = point_2

        vector_normal = Vector2([pos1[0] - pos2[0] + 0.00001, pos1[1] - pos2[1]])
        vector_normal.normalyze()
        poses = []

        vector_left = copy(vector_normal)
        vector_left.rotate(90)
        vector_left *= width / 2
        poses.append([pos1[0] + vector_left.x, pos1[1] + vector_left.y])
        poses.append([pos2[0] + vector_left.x, pos2[1] + vector_left.y])

        vector_right = copy(vector_normal)
        vector_right.rotate(-90)
        vector_right *= width / 2
        poses.append([pos2[0] + vector_right.x, pos2[1] + vector_right.y])
        poses.append([pos1[0] + vector_right.x, pos1[1] + vector_right.y])

        Draw.draw_polygone(surface, poses, color)
        if circled:
            Draw.draw_circle(surface, pos1, width / 2, color)
            Draw.draw_circle(surface, pos2, width / 2, color)

    @staticmethod
    def draw_dashed_line(

            surface: pygame.Surface,
            point_1: list | tuple | Vector2,
            point_2: list | tuple | Vector2,
            color: list | str | Color = "gray",
            width: int = 1,
            dash_size: int = 10,
    ) -> None:
        if isinstance(color, Color):
            color = color.rgb
        if isinstance(point_1, Vector2):
            pos1 = point_1.xy
        elif isinstance(point_1, (list, tuple)):
            pos1 = point_1
        if isinstance(point_2, Vector2):
            pos2 = point_2.xy
        elif isinstance(point_2, (list, tuple)):
            pos2 = point_2
        vector = Vector2(pos1[0] - pos2[0], pos1[1] - pos2[1])
        lenght = vector.lenght
        vector.normalyze()
        vector *= dash_size
        delta_pos = pos1
        for i in range(int(lenght // dash_size)):
            delta_pos = [pos1[0] - vector.x, pos1[1] - vector.y]
            if i % 2 == 0:
                Draw.draw_line(surface, pos1, delta_pos, color, width)
            pos1 = delta_pos

    @staticmethod
    def draw_dashed_hline(

            surface: pygame.Surface,
            point_1: list | tuple | Vector2,
            point_2: list | tuple | Vector2,
            color: list | str | Color = "gray",
            width: int = 1,
            dash_size: int = 10,
    ) -> None:
        if isinstance(color, Color):
            color = color.rgb
        if isinstance(point_1, Vector2):
            pos1 = point_1.xy
        elif isinstance(point_1, (list, tuple)):
            pos1 = point_1
        if isinstance(point_2, Vector2):
            pos2 = point_2.xy
        elif isinstance(point_2, (list, tuple)):
            pos2 = point_2
        vector = Vector2(pos1[0] - pos2[0], pos1[1] - pos2[1])
        lenght = vector.lenght
        vector.normalyze()
        vector *= dash_size
        delta_pos = pos1
        for i in range(int(lenght // dash_size)):
            delta_pos = [pos1[0] - vector.x, pos1[1] - vector.y]
            if i % 2 == 0:
                Draw.draw_hline(surface, pos1[1], pos1[0], delta_pos[0], width, color)
            pos1 = delta_pos

    @staticmethod
    def draw_dashed_vline(

            surface: pygame.Surface,
            point_1: list | tuple | Vector2,
            point_2: list | tuple | Vector2,
            color: list | str | Color = "gray",
            width: int = 1,
            dash_size: int = 10,
    ) -> None:
        if isinstance(color, Color):
            color = color.rgb
        if isinstance(point_1, Vector2):
            pos1 = point_1.xy
        elif isinstance(point_1, (list, tuple)):
            pos1 = point_1
        if isinstance(point_2, Vector2):
            pos2 = point_2.xy
        elif isinstance(point_2, (list, tuple)):
            pos2 = point_2
        vector = Vector2(pos1[0] - pos2[0], pos1[1] - pos2[1])
        lenght = vector.lenght
        vector.normalyze()
        vector *= dash_size
        delta_pos = pos1
        for i in range(int(lenght // dash_size)):
            delta_pos = [pos1[0] - vector.x, pos1[1] - vector.y]
            if i % 2 == 0:
                Draw.draw_vline(surface, pos1[0], pos1[1], delta_pos[1], width, color)
            pos1 = delta_pos

    @staticmethod
    def draw_lines(

            surface: pygame.Surface,
            points: Tuple[Tuple[float, float], ...],
            color: Tuple[int, int, int] | str | Color,
            width: int,
            closed: bool = False,
            blend: int = 1,
    ):
        if isinstance(color, Color):
            color = color.rgb
        for i in range(width):
            for j in range(width):
                points_ = list(
                    map(
                        lambda elem: [
                            elem[0] + i - width // 2,
                            elem[1] + j - width // 2,
                        ],
                        points,
                    )
                )
                pygame.draw.aalines(surface, color, closed, points_, blend)

    @staticmethod
    def draw_alines(
            surface: pygame.Surface,
            points: Tuple[Tuple[float, float], ...],
            color: Tuple[int, int, int] | str | Color,
            width: int,
            closed: bool = False,
    ):
        if isinstance(color, Color):
            color = color.rgb

        for i in range(len(points)):
            if closed:
                Draw.draw_aline(surface, points[i - 1], points[i], color, width)
            else:
                if i - 1 >= 0:
                    Draw.draw_aline(surface, points[i - 1], points[i], color, width)

    @staticmethod
    def draw_join_line(
            surface: pygame.Surface,
            point_1: list | tuple | Vector2,
            point_2: list | tuple | Vector2,
            color: list | str | Color = "gray",
            join_width: int = 10,
            join_steps: int = 10,
            width: int = 1,
    ):
        if isinstance(color, Color):
            color = color.rgb
        if isinstance(point_1, Vector2):
            pos1 = point_1.xy
        elif isinstance(point_1, (list, tuple)):
            pos1 = point_1
        if isinstance(point_2, Vector2):
            pos2 = point_2.xy
        elif isinstance(point_2, (list, tuple)):
            pos2 = point_2

        lenght = distance(point_1, point_2)

        vector_speed = Vector2(
            pos1[0] - pos2[0],
            pos1[1] - pos2[1]
        )
        vector_speed.normalyze()
        vector_speed *= (lenght / join_steps)

        vector_joining = copy(vector_speed)
        vector_joining.normalyze()
        vector_joining *= join_width
        vector_joining.rotate(90)
        points = []

        for i in range(join_steps):
            points.append(copy(pos2))
            pos2[0] += vector_speed.x
            pos2[1] += vector_speed.y

            pos2[0] += vector_joining.x
            pos2[1] += vector_joining.y
            if i % 2 == 0:
                vector_joining *= -1
        points.append(pos2)

        Draw.draw_lines(surface, points, color, width)

    @staticmethod
    def draw_vline(

            surface: pygame.Surface,
            x: int,
            y1: int,
            y2: int,
            width: int = 1,
            color: list | str | Color = (100, 100, 100),
    ) -> None:
        if isinstance(color, Color):
            color = color.rgb
        for i in range(width):
            gfxdraw.vline(surface, int(x - int(width / 2) + i), int(y1), int(y2), color)

    @staticmethod
    def draw_hline(

            surface: pygame.Surface,
            y: int,
            x1: int,
            x2: int,
            width: int = 1,
            color: list | str | Color = (100, 100, 100),
    ) -> None:
        if isinstance(color, Color):
            color = color.rgb
        for i in range(width):
            gfxdraw.hline(surface, int(x1), int(x2), int(y - int(width / 2) + i), color)

    @staticmethod
    def draw_bezier(

            surface: pygame.Surface,
            points: Tuple[Tuple[float, float], ...],
            steps: int = 2,
            color: Tuple[int, int, int] | str | Color = (100, 100, 100),
            width: int = 1,
    ):
        if isinstance(color, Color):
            color = color.rgb
        for i in range(width):
            for j in range(width):
                points_ = list(
                    map(
                        lambda elem: [
                            elem[0] + i - width // 2,
                            elem[1] + j - width // 2,
                        ],
                        points,
                    )
                )
                gfxdraw.bezier(surface, points_, steps, color)

    @staticmethod
    def draw_rect_fast(

            surface: pygame.Surface,
            pos: list[int],
            size: list[int],
            color: list | str | Color = "gray",
    ):
        if len(size) == 1:
            size = [size[0], size[0]]
        if isinstance(color, Color):
            color = color.rgb
        rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        gfxdraw.rectangle(surface, rect, color)

    @staticmethod
    def draw_dashed_lines(
            surface: pygame.Surface,
            points: list,
            color: list | str | Color = "gray",
            width: int = 1,
            dash_size: int = 10,
    ):
        for i in range(len(points)):
            if i + 1 < len(points):
                Draw.draw_dashed_line(
                    surface, points[i], points[i + 1], color, width, dash_size
                )

    @staticmethod
    def draw_arc(
            surface: pygame.Surface,
            center_pos: list,
            color: list | str | Color = "gray",
            start_angle: int = 0,
            stop_angle: int = 175,
            radius: int = 100,
            width: int = 50,
            step: int = 20,
            outline_width: int = 0,
    ):
        if isinstance(color, Color):
            color = color.rgb
        if width != 1:
            stop_angle = stop_angle % 361
            toch = step
            ang_step = (start_angle - stop_angle) / toch
            width = min(radius, width)

            start_pos = [
                center_pos[0] + math.sin(math.radians(start_angle)) * (radius - width),
                center_pos[1] + math.cos(math.radians(start_angle)) * (radius - width),
            ]
            poses = []
            poses.append(start_pos)

            for i in range(toch + 1):
                x = center_pos[0] + math.sin(math.radians(start_angle)) * radius
                y = center_pos[1] + math.cos(math.radians(start_angle)) * radius
                start_angle += ang_step

                poses.append([x, y])
            start_angle -= ang_step
            for i in range(toch):
                x = center_pos[0] + math.sin(math.radians(start_angle)) * (radius - width)
                y = center_pos[1] + math.cos(math.radians(start_angle)) * (radius - width)
                start_angle -= ang_step

                poses.append([x, y])

            Draw.draw_polygone(surface, poses, color, outline_width)
        else:
            pygame.draw.arc(
                surface,
                color,
                [
                    center_pos[0] - radius,
                    center_pos[1] - radius,
                    radius * 2,
                    radius * 2,
                ],
                math.radians(start_angle + 90),
                math.radians(stop_angle + 90),
            )

    @classmethod
    def draw_shapes(
            self,
            surface: pygame.Surface,
            shapes: Tuple[callable, ...],
            pos: list | Vector2
    ):
        shapes_functions = [shape[0].__name__ for shape in shapes]
        shapes_kvargs = [shape[1] for shape in shapes]

        for i in range(len(shapes_functions)):
            shapes_kvargs[i]['pos'][0] += pos[0]
            shapes_kvargs[i]['pos'][1] += pos[1]
            Draw.__dict__[shapes_functions[i]].__call__(surface=surface, **shapes_kvargs[i])
