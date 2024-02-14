import pygame
from typing import overload

def load_image(file_name: str) -> pygame.Surface:
    return pygame.image.load(file_name)


class Sprite:
    def __init__(self, file_name: str) -> None:
        self.__file_name = file_name
        self.__start_sprite = load_image(file_name)
        
        self.__angle = 0
        self.__scale = 1
        
    @property
    def scale(self) -> float:
        return self.__scale
        
    @scale.setter
    def scale(self, scale):
        self.__scale = scale
    
    @property
    def angle(self) -> float:
        return self.__angle
    
    @angle.setter
    def angle(self, angle):
        self.__angle = angle
        
    def set_attrs(self):
        surf = pygame.transform.scale(self.__start_sprite, [
            self.__start_sprite.get_width()*self.__scale,
            self.__start_sprite.get_height()*self.__scale,
        ])
        surf = pygame.transform.rotate(surf, self.__angle)
        return surf
        
    def render(self, surf: pygame.Surface, center_pos: list[int]):
        render_surf = self.set_attrs()
        pos = [
            center_pos[0]-render_surf.get_width()/2,
            center_pos[1]-render_surf.get_height()/2
        ]
        surf.blit(render_surf, pos)
        
class SpriteSheat:
    def __init__(self, file_name: str) -> None:
        self.__file_name = file_name
        self.__image = load_image(self.__file_name)
        self.__cut_surfs = self.cut()
        
    @property
    def sprites(self) -> list[pygame.Surface]:
        return self.__cut_surfs
        
    def cut(self) -> list[pygame.Surface]:
        width_ = self.__image.get_size()[0]
        height_ = self.__image.get_size()[1]

        spritets_coloms = []
        sizes_poses = []

        for i in range(height_):
            c = self.__image.get_at([0, i])
            color = (c[0], c[1], c[2])
            if color == (255, 0, 255):
                spritets_coloms.append(i)

        for col in spritets_coloms:
            for line in range(width_):
                c = self.__image.get_at([line, col])
                color = (c[0], c[1], c[2])
                if color == (255, 255, 0):
                    pos = [line + 1, col]
                    spw = 0
                    sph = 0
                    for sw in range(width_ - line):
                        c = self.__image.get_at([line + sw, col])
                        color = (c[0], c[1], c[2])
                        if color == (0, 0, 255):
                            spw = sw
                            break
                    for sh in range(height_ - col):
                        c = self.__image.get_at([line, col + sh])
                        color = (c[0], c[1], c[2])
                        if color == (0, 0, 255):
                            sph = sh
                            break
                    sizes_poses.append([[pos[0], pos[1] + 1], [spw, sph]])
        textures = []

        for sp in sizes_poses:
            self.__image.set_clip(sp[0], sp[1])
            texture = self.__image.get_clip()
            surft = self.__image.subsurface(texture)
            textures.append(surft)
        return textures
    
class SpriteAnim:
    
    @overload
    def __init__(self, sprites: list[pygame.Surface]) -> None:
        pass
    
    @overload
    def __init__(self, sprites: list[Sprite]) -> None:
        pass
    
    def __init__(self, sprites: any):
        ...