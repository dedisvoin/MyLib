from copy import copy
import pygame
import ctypes
import os
from typing import Tuple
from typing import Any
from GLib.text import *
import keyboard

pygame.init()


class WindowFlags:
    # window flags
    FULLSCREEN = pygame.FULLSCREEN
    RESIZE = pygame.RESIZABLE
    SCALE = pygame.SCALED
    NOFRAME = pygame.NOFRAME
    OPENGL = pygame.OPENGL
    DOUBLEBUF = pygame.DOUBLEBUF

class Window:
    def __init__(self,
                pos: list[int] | str | None = None,
                size: list[int] | str | None = None,
                title: str | None = None,
                flags: Any | None = 0,
                vsync: bool = False,
                statick: bool = False) -> None:

        # create a basic window
        self.__pos = pos
        self.__size = size
        self.__title = title
        self.__flags = flags
        self.__vsync = vsync
        self.__clock = pygame.time.Clock()

        self.__fps = 60
        self.__delta_fps = 60

        self.__window: pygame.Surface | None = None
        self.__running = True
        self.__display_size = [0, 0]
        self.__window_id = None
        self.__statick = statick
        self.__delta = 1

        self.__fps_counter_text: Text | None = None

        self.set_default_values()
        self.parse_attributes()
        self.construct_window_by_parameters()

        self.fps_counter_init()

    def fps_counter_init(self):
        self.__fps_counter_text = Text(font='arial', font_size=15, bold=True, italic=False)

    def view_fps(self):
        fps_surf = self.__fps_counter_text.render_text_surf('fps: '+str(self.fps), 'orange')
        self.__window.blit(fps_surf, [5, 5])

    def view_delta(self):
        delta_surf = self.__fps_counter_text.render_text_surf('delta: '+str(self.delta), 'orange')
        self.__window.blit(delta_surf, [self.__size[0]-delta_surf.get_width()-5, 5])

    def set_default_values(self):
        # set default window values
        if self.__size is None:
            self.__size = [1000, 800]
        if self.__title is None:
            self.__title = "Program"
        if self.__pos is None:
            self.__pos = 'center'

    def parse_attributes(self):
        # attribute parse
        self.__display_size = pygame.display.get_desktop_sizes()[0]
        if self.__pos == 'center':
            self.__pos = [self.__display_size[0]/2-self.__size[0]/2,
                            self.__display_size[1]/2-self.__size[1]/2]

    def construct_window_by_parameters(self) -> None:
        # create window by attributes
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (self.__pos[0], self.__pos[1])
        self.__window = pygame.display.set_mode(self.__size, self.__flags, self.__flags, self.__vsync)
        pygame.display.set_caption(self.__title)
        self.__window_id = pygame.display.get_wm_info()['window']

    def window_events_listen(self):
        # events listener
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False

    def mathing_delta(self):
        if self.fps != 0:
            self.__delta = self.__delta_fps / self.fps

    def update(self, fill_color: Tuple[int, int, int] | str = 'white', exit_hot_key: str = 'esc'):
        # window update method
        self.__clock.tick(self.__fps)
        
        pygame.display.flip()
        self.__window.fill(fill_color)

        self.mathing_delta()

        if self.__statick:
            ctypes.windll.user32.MoveWindow(self.__window_id,
                                            int(self.__pos[0]), int(self.__pos[1]),
                                            int(self.__size[0]), int(self.__size[1]))
            

        self.__size = self.__window.get_size()

        self.window_events_listen()
        if keyboard.is_pressed(exit_hot_key):
            self.__running = False
    
    @property
    def running(self) -> bool:
        return self.__running

    def __call__(self, fill_color: str | Tuple[int, int, int] = 'white'):
        self.update(fill_color)
        return self.__running

    def get_size(self) -> list[int] | None:
        return self.__size

    def set_size(self, size: list[int]):
        self.__size = size
        
    def get_surf_size(self):
        return self.__window.get_size()

    def get_pos(self) -> list[int] | None:
        return self.__pos

    def set_pos(self, pos: list[int]):
        self.__pos = pos

    @property
    def fps(self):
        return round(self.__clock.get_fps(),2)

    @fps.setter
    def fps(self, fps: int):
        self.__fps = fps

    @property
    def surf(self) -> pygame.Surface:
        return self.__window

    @property
    def width(self) -> int:
        return self.__size[0]

    @property
    def height(self) -> int:
        return self.__size[1]

    @property
    def delta(self) -> float:
        return round(self.__delta,3)
    
    @property
    def center(self) -> list:
        return [self.__size[0]/2, self.__size[1]/2]
