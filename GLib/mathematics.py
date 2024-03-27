from copy import copy
from typing import overload, Tuple
import typing
from typing import Tuple
from typing import Any
import random
import math
import tripy


def posing(pos, sx, sy):
    '''
    applies a value to the components of the position
    '''
    return [pos[0] + sx, pos[1] + sy]


class Vector2:
    '''
    the simplest class of a two-dimensional vector in space
    '''
    @staticmethod
    def Normal(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> 'Vector2':
        return Vector2(pos1[0] - pos2[0], pos1[1] - pos2[1])

    @staticmethod
    def Random(start: int, stop: int):
        return Vector2(random.randint(start, stop), random.randint(start, stop))

    @overload
    def __init__(self, x_y: typing.Tuple[float, float]) -> None:
        ...

    @overload
    def __init__(self, x_: float, y_: float) -> None:
        ...

    def __init__(self, *_args) -> None:
        
        self._y = None
        self._x = None
        self.__args_manager__(*_args)

    def __args_manager__(self, *args):
        if len(args) == 1:
            self._x = args[0][0]
            self._y = args[0][1]
        elif len(args) == 2:
            self._x = args[0]
            self._y = args[1]

    def __str__(self) -> str:
        return f"Vector2 {self._x, self._y}"

    @property
    def lenght(self):
        le = vector_lenght(self._x, self._y)
        if le == 0:
            return 0.0000001
        return le

    @lenght.setter
    def lenght(self, _value: int):
        self._x *= _value / self.lenght
        self._y *= _value / self.lenght

    def rotate(self, angle: int):
        angle = math.radians(angle)
        _x = self._x * math.cos(angle) - self._y * math.sin(angle)
        _y = self._x * math.sin(angle) + self._y * math.cos(angle)
        self._x = _x
        self._y = _y

    def set_angle(self, angle: int):
        lenght = self.lenght
        angle = math.radians(angle)
        self._x = math.cos(angle) * lenght
        self._y = math.sin(angle) * lenght

    def scalar_angle(self, vector: 'Vector2') -> float:
        return (self.lenght * vector.lenght) * math.cos(math.radians(self.get_angle() - vector.get_angle() + 90))

    def scalar_lenght(self, vector: 'Vector2') -> float:
        return (vector.x * self.x) + (vector.y * self.y)

    def get_angle(self) -> float:
        return angle_to_float((0, 0), (self._x, self._y))

    def normalyze(self):
        lenght = self.lenght
        self._x /= lenght
        self._y /= lenght

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @x.setter
    def x(self, value: float) -> None:
        self._x = value

    @y.setter
    def y(self, value: float) -> None:
        self._y = value

    @property
    def sw(self) -> float:
        return self._x

    @property
    def sh(self) -> float:
        return self._y

    @sw.setter
    def sw(self, value: float) -> None:
        self._x = value

    @sh.setter
    def sh(self, value: float) -> None:
        self._y = value

    @property
    def swh(self) -> typing.Tuple[int, int]:
        return self._x, self._y

    @swh.setter
    def swh(self, pos_: typing.Tuple[int, int]):
        self._x = pos_[0]
        self._y = pos_[1]

    @property
    def xy(self) -> typing.Tuple[int, int]:
        return self._x, self._y

    @xy.setter
    def xy(self, pos_: typing.Tuple[int, int]):
        self._x = pos_[0]
        self._y = pos_[1]

    def __iadd__(self, vector_: "Vector2") -> "Vector2":
        self.x += vector_.x
        self.y += vector_.y
        return self

    def __isub__(self, vector_: "Vector2") -> "Vector2":
        self.x -= vector_.x
        self.y -= vector_.y
        return self

    def __imul__(self, value_: float) -> "Vector2":
        self.x *= value_
        self.y *= value_
        return self

    def __idiv__(self, value_: float) -> "Vector2":
        self.x /= value_
        self.y /= value_
        return self

    def __add__(self, vector_: "Vector2") -> "Vector2":
        self.x += vector_.x
        self.y += vector_.y
        return self

    def __mul__(self, value_: float) -> "Vector2":
        self.x *= value_
        self.y *= value_
        return self

    def __sub__(self, vector_: "Vector2") -> "Vector2":
        self.x -= vector_.x
        self.y -= vector_.y
        return self


# auxiliary methods

def two_element_typing_xy(iterable_: list | tuple | Vector2):
    if isinstance(iterable_, (list, tuple)):
        return iterable_[0], iterable_[1]
    elif isinstance(iterable_, Vector2):
        return iterable_.x, iterable_.y


def two_element_typing_x_y(iterable_: list | tuple | Vector2):
    if isinstance(iterable_, (list, tuple)):
        return [iterable_[0], iterable_[1]]
    elif isinstance(iterable_, Vector2):
        return [iterable_.x, iterable_.y]


def distance(
        point_1: Any | typing.Tuple[int, int], point_2: Any | typing.Tuple[int, int]
):
    '''
    finding the distance in pixels between two points using their positions
    '''
    dx = point_1[0] - point_2[0]
    dy = point_1[1] - point_2[1]
    _distance = math.sqrt(dx ** 2 + dy ** 2)
    return _distance


def distance_to_line(
        l_point_1: Any | typing.Tuple[int, int], l_point_2: Any | typing.Tuple[int, int],
        point: Any | typing.Tuple[int, int]
):
    '''
    finds the distance in pixels from a point to a line by lowering the perpendicular to it
    '''
    d1 = distance(l_point_2, point)
    d2 = distance(l_point_1, point)
    le = distance(l_point_2, l_point_1)
    p = (d1 + d2 + le) / 2
    h = (2 * math.sqrt(p * (p - le) * (p - d1) * (p - d2))) / le
    return h


def distance_to_line_stop(
        l_point_1: Any | typing.Tuple[int, int], l_point_2: Any | typing.Tuple[int, int],
        point: Any | typing.Tuple[int, int]
):
    '''
    finds the distance in pixels from a point to a line by lowering the perpendicular to it 
    if possible to lower the perpendicular to the line
    '''
    d1 = distance(l_point_2, point)
    d2 = distance(l_point_1, point)
    le = distance(l_point_2, l_point_1)
    p = (d1 + d2 + le) / 2
    h = (2 * math.sqrt(p * (p - le) * (p - d1) * (p - d2))) / le

    l_angle = angle_to(l_point_1, l_point_2)
    p1_angle = angle_to(l_point_1, point) - l_angle
    p2_angle = angle_to(l_point_2, point) - l_angle

    if (p1_angle < 90 or p1_angle > 270) and (90 < p2_angle < 270):
        return h
    else:
        return None


def rotate_angle(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.
    The angle should be given in radians.
    """
    angle = math.radians(angle)
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


def center_pos(
        point_1: Vector2 | typing.Tuple[int, int], point_2: Vector2 | typing.Tuple[int, int]
):
    '''
    finds the center point between two points
    '''
    x1, y1 = two_element_typing_xy(point_1)
    x2, y2 = two_element_typing_xy(point_2)
    dx = (x1 - x2) / 2
    dy = (y1 - y2) / 2
    return [x2 + dx, y2 + dy]


def center_pos_with_percent(
        point_1: Tuple[int, int], point_2: Tuple[int, int], percent: float = 0.5
):
    dx = point_1[0]-point_2[0]
    dy = point_1[1]-point_2[1]

    return [point_1[0]-dx*percent, point_1[1]-dy*percent]


def vector_lenght(lenght_x: int, lenght_y: int):
    '''
    finds the length of a vector through its components
    '''
    _distance = math.sqrt(lenght_x ** 2 + lenght_y ** 2)
    if _distance == 0:
        return 1
    return _distance


def rect_center(rect_pos: typing.Tuple[int, int], rect_size: typing.Tuple[int, int]):
    '''
    finds the center of a rectangular area
    '''
    return [rect_pos[0] + rect_size[0] / 2, rect_pos[1] + rect_size[1] / 2]


def angle_to(
        point_1: typing.Tuple[int, int] | "Vector2",
        point_2: typing.Tuple[int, int] | "Vector2",
) -> float:
    '''
    finds the angle between two points
    '''
    pos1 = two_element_typing_x_y(point_1)
    pos2 = two_element_typing_x_y(point_2)

    atan = math.atan2(pos1[0] - pos2[0], pos1[1] - pos2[1])
    return int(atan / math.pi * 180 + 180)


def center_rect(
        pos: typing.Tuple[int, int], size: typing.Tuple[int, int], _reverse: bool = False
) -> tuple[float, float]:
    '''
    finds the center of a rectangular area
    '''
    if not _reverse:
        return pos[0] + size[0] / 2, pos[1] + size[1] / 2
    else:
        return pos[0] - size[0] / 2, pos[1] - size[1] / 2


def angle_to_float(
        point_1: typing.Tuple[int, int] | "Vector2",
        point_2: typing.Tuple[int, int] | "Vector2",
) -> float:
    '''
    finds the angle between two points or vectors
    '''
    if isinstance(point_1, Vector2):
        pos1 = point_1.xy
    elif isinstance(point_1, (list, tuple)):
        pos1 = point_1

    if isinstance(point_2, Vector2):
        pos2 = point_2.xy
    elif isinstance(point_2, (list, tuple)):
        pos2 = point_2

    atan = math.atan2(pos1[0] - pos2[0], pos1[1] - pos2[1])
    return (atan / math.pi * 180 + 180) % 360


def triangulate(polygone_points_: Tuple[Tuple[int, int], ...]):
    '''
    divides the polygon into triangles necessary to check the location of a point in the polygon area
    '''
    return tripy.earclip(polygone_points_)


def in_rect(
        rect_pos_: typing.Tuple[float, float] | Vector2,
        rect_size_: typing.Tuple[float, float] | Vector2,
        point_: typing.Tuple[float, float] | Vector2,
):
    '''
    checking the location of a point in a rectangular area
    '''
    if isinstance(rect_pos_, Vector2):
        rect_pos = rect_pos_.xy
    elif isinstance(rect_pos_, (list, tuple)):
        rect_pos = rect_pos_

    if isinstance(rect_size_, Vector2):
        rect_size = rect_size_.xy
    elif isinstance(rect_size_, (list, tuple)):
        rect_size = rect_size_

    if isinstance(point_, Vector2):
        point = point_.xy
    elif isinstance(point_, (list, tuple)):
        point = point_

    if (
            rect_pos[0] < point[0] < rect_pos[0] + rect_size[0]
            and rect_pos[1] < point[1] < rect_pos[1] + rect_size[1]
    ):
        return True
    else:
        return False


def in_circle(
        circle_pos_: typing.Tuple[float, float] | Vector2,
        circle_rad_: float,
        point_: typing.Tuple[float, float] | Vector2
):
    '''
    checking the location of a point in a circle area
    '''
    if isinstance(circle_pos_, Vector2):
        circle_pos = circle_pos_.xy
    elif isinstance(circle_pos_, (list, tuple)):
        circle_pos = circle_pos_

    if isinstance(point_, Vector2):
        point = point_.xy
    elif isinstance(point_, (list, tuple)):
        point = point_
    if distance(circle_pos, point) < circle_rad_:
        return True
    return False


def in_polygone(
        triangles: Tuple[Tuple[int, int, int], ...],
        point_: typing.Tuple[float, float] | Vector2
):
    '''
    checking the location of a point in a polygone area
    '''
    if isinstance(point_, Vector2):
        point = point_.xy
    elif isinstance(point_, (list, tuple)):
        point = point_

    for k, t in enumerate(triangles):
        true = 0
        for i in range(3):

            vec = Vector2.Normal(copy(triangles[k][i]), copy(triangles[k][i - 1]))
            p_vec = Vector2.Normal(copy(triangles[k][i - 1]), point)
            n = vec.scalar_angle(p_vec)
            if n < 0:
                true += 1

        if true == 0:
            return True

    return False

