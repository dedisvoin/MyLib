import pygame
from typing import Tuple

pygame.init()


class Text:
    def __init__(self,
                font: str | None = 'arial',
                font_size: int = 10,
                bold: bool = False,
                italic: bool = False):
        self.__font = font
        self.__font_size = font_size
        self.__bold = bold
        self.__italic = italic
        self.__font_object: pygame.font.Font | None = None

        self.pre_init_font()

    def pre_init_font(self):
        self.__font_object = pygame.font.SysFont(self.__font, self.__font_size, self.__bold, self.__italic)

    def render_text_surf(self, text: str, color: Tuple[int, int, int] | str | None = 'black') -> pygame.Surface:
        return self.__font_object.render(text, True, color).convert_alpha()

    def get_text_pre_size(self, text: str) -> Tuple[int, int]:
        return self.__font_object.size(text)
