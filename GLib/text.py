import pygame
from typing import Tuple
from GLib.sprites import *
from functools import lru_cache

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
        try:
            self.__font.split('.')
            self.__font_object = pygame.font.Font(self.__font, self.__font_size)
        except:
            self.__font_object = pygame.font.SysFont(self.__font, self.__font_size, self.__bold, self.__italic)

    def render_text_surf(self, text: str, color: Tuple[int, int, int] | str | None = 'black') -> pygame.Surface:
        return self.__font_object.render(text, True, color).convert_alpha()

    def get_text_pre_size(self, text: str) -> Tuple[int, int]:
        return self.__font_object.size(text)

class PixelText:
    def __init__(self, font_file_name) -> None:
        self.name = font_file_name
        self.bukvas = SpriteSheat(self.name).sprites
        self.construct()

    def construct(self):
        self.writed_syms = {
            'a':self.bukvas[0],
            'b':self.bukvas[1],
            'c':self.bukvas[2],
            'd':self.bukvas[3],
            'e':self.bukvas[4],
            'f':self.bukvas[5],
            'g':self.bukvas[6],
            'h':self.bukvas[7],
            'i':self.bukvas[8],
            'j':self.bukvas[9],
            'k':self.bukvas[10],
            'l':self.bukvas[11],
            'm':self.bukvas[12],
            'n':self.bukvas[13],
            'o':self.bukvas[14],
            'p':self.bukvas[15],
            'q':self.bukvas[16],
            'r':self.bukvas[17],
            's':self.bukvas[18],
            't':self.bukvas[19],
            'u':self.bukvas[20],
            'v':self.bukvas[21],
            'w':self.bukvas[22],
            'x':self.bukvas[23],
            'y':self.bukvas[24],
            'z':self.bukvas[25],
            ' ':self.bukvas[26],
            ':':self.bukvas[27],
            '.':self.bukvas[28],
            '1':self.bukvas[29],
            '2':self.bukvas[30],
            '3':self.bukvas[31],
            '4':self.bukvas[32],
            '5':self.bukvas[33],
            '6':self.bukvas[34],
            '7':self.bukvas[35],
            '8':self.bukvas[36],
            '9':self.bukvas[37],
            '0':self.bukvas[38],
            '-':self.bukvas[39],
            '+':self.bukvas[40],
            '/':self.bukvas[41],
            '(':self.bukvas[42],
            ')':self.bukvas[43]
        }

    @lru_cache()    
    def get_text_pre_size(self, text: str, scale) -> Tuple[int, int]:
        rendered_surf_width = 0
        rendered_surf_height = self.writed_syms['a'].start_sprite.get_height()*scale
    
        for sym in text:
            if sym in self.writed_syms:
                symvol_sprite = self.writed_syms[sym].start_sprite
                rendered_surf_width+=(1+symvol_sprite.get_width())*scale

        rendered_surf_width+=(1+symvol_sprite.get_width())*scale

        
        return [rendered_surf_width, rendered_surf_height]

    def render(self, win, pos, text:str, scale = 1, color='red') -> pygame.Surface:
        posr = [0,0]
        text = text.lower()

        rendered_surf_width = 0
        rendered_surf_height = self.writed_syms['a'].start_sprite.get_height()*scale
        
        

        for sym in text:
            if sym in self.writed_syms:
                symvol_sprite = self.writed_syms[sym].start_sprite
                
                rendered_surf_width+=(1+symvol_sprite.get_width())*scale

        text_surf = pygame.Surface([rendered_surf_width, rendered_surf_height]).convert()
        text_surf.set_colorkey((0,0,0))

        
        for sym in text:
            if sym in self.writed_syms:
                symvol_sprite = self.writed_syms[sym].start_sprite
                symvol_sprite = pygame.transform.scale(symvol_sprite, [symvol_sprite.get_width()*scale, symvol_sprite.get_height()*scale])
                text_surf.blit(symvol_sprite, posr)
                posr[0]+=symvol_sprite.get_width()
            posr[0]+=1*scale

        
        color_surf = pygame.Surface([rendered_surf_width, rendered_surf_height]).convert()
        color_surf.fill(color)
        text_surf.blit(color_surf, [0,0], special_flags=pygame.BLEND_MIN)

        win.surf.blit(text_surf, pos)

    def render_with_surf(self, surf_render, pos, text:str, scale = 1, color='red') -> pygame.Surface:
        posr = [0,0]
        text = text.lower()

        rendered_surf_width = 0
        rendered_surf_height = self.writed_syms['a'].start_sprite.get_height()*scale

        for sym in text:
            if sym in self.writed_syms:
                symvol_sprite = self.writed_syms[sym].start_sprite
                
                rendered_surf_width+=(1+symvol_sprite.get_width())*scale

        text_surf = pygame.Surface([rendered_surf_width, rendered_surf_height]).convert()
        text_surf.set_colorkey((0,0,0))

        
        for sym in text:
            if sym in self.writed_syms:
                symvol_sprite = self.writed_syms[sym].start_sprite
                symvol_sprite = pygame.transform.scale(symvol_sprite, [symvol_sprite.get_width()*scale, symvol_sprite.get_height()*scale])
                text_surf.blit(symvol_sprite, posr)
                posr[0]+=symvol_sprite.get_width()
            posr[0]+=1*scale

        
        color_surf = pygame.Surface([rendered_surf_width, rendered_surf_height]).convert()
        color_surf.fill(color)
        text_surf.blit(color_surf, [0,0], special_flags=pygame.BLEND_MIN)

        surf_render.blit(text_surf, pos)

        