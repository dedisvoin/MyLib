from random import randint
from math import sin
from typing import Tuple
import pygame

BASIC_COLORS = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'green': (0, 255, 0),
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
}


class Color:
    def __init__(self, color_value: tuple | str) -> None:
        self.__color_value = color_value

        self.__color = self.generate()

    def generate(self):
        if type(self.__color_value) is str:
            if self.__color_value in BASIC_COLORS:
                return BASIC_COLORS[self.__color_value]
        else:
            return self.__color_value

    @property
    def rgb(self):
        return self.__color

    @rgb.setter
    def rgb(self, rgb: tuple) -> None:
        self.__color = rgb

    @staticmethod
    def random():
        color = Color((0, 0, 0))
        color.rgb = [
            randint(0, 255),
            randint(0, 255),
            randint(0, 255)
        ]
        return color
    
    @staticmethod
    def rgba(r, g, b, a = None):
        return Color([r, g, b])
    
    @staticmethod
    def hsv(hsv: str):
        return hsv

class Gradient:
    class TwoColors:
        def __init__(self, color_1: Color, color_2: Color, steps: int = 255, rgb_deltas=[1, 1, 1]) -> None:
            self._color_1 = color_1
            self._color_2 = color_2
            self._steps = steps
            self._rgb_deltas = rgb_deltas

            self.gradient_surf = pygame.Surface([self._steps, 10])

        def generate(self):
            dr = self._color_2[0] - self._color_1[0]
            dg = self._color_2[1] - self._color_1[1]
            db = self._color_2[2] - self._color_1[2]

            delta_r = dr / self._steps
            delta_g = dg / self._steps
            delta_b = db / self._steps

            for i in range(self._steps):
                color = [
                    self._color_1[0] + dr * sin(i / self._steps * self._rgb_deltas[0]),
                    self._color_1[1] + dg * sin(i / self._steps * self._rgb_deltas[1]),
                    self._color_1[2] + db * sin(i / self._steps * self._rgb_deltas[2]),
                ]
                
                #Draw.draw_rect(self.gradient_surf, [i, 0], [2, 10], color)
                pygame.draw.rect(self.gradient_surf,color, [[i, 0], [2, 10]] )

        def get_percent(self, percent: float):
            color = self.gradient_surf.get_at([int(self._steps * percent), 1])
            
            return [color.r, color.g, color.b]

    class ManyColors:
        def __init__(self, colors: Tuple[Color, ...], colors_steps: Tuple[int, ...], colors_rgb_deltas) -> None:
            self._colors = colors
            self._colors_steps = colors_steps
            self._colors_rgb_deltas = colors_rgb_deltas
            self._pos_x = 0
            self.generate()

        def generate_gradient_surfs(self):
            self.all_step = 0
            for step in self._colors_steps:
                self.all_step += step

            self.gradient_surf = pygame.Surface([self.all_step, 10])

        def generate(self):
            self.generate_gradient_surfs()
            for i in range(len(self._colors)):
                color1 = self._colors[i - 1]
                color2 = self._colors[i]
                step = self._colors_steps[i]
                delta = self._colors_rgb_deltas[i]
                cg = Gradient.TwoColors(color1, color2, step, delta)
                cg.generate()
                
                self.gradient_surf.blit(cg.gradient_surf, [self._pos_x, 0])
                self._pos_x += step
                

        def get_percent(self, percent: float):
            
            color = self.gradient_surf.get_at([int(self.all_step * percent), 1])
            
            return [color.r, color.g, color.b]