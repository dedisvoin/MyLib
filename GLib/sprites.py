import pygame

def load_image(file_name: str) -> pygame.Surface:
    return pygame.image.load(file_name)


class Sprite:
    def __init__(self, file_name: str = None, rotate_buf = False, rotate_angles = 180) -> None:
        self.__file_name = file_name
        if file_name is not None:
            self.__start_sprite = load_image(file_name).convert_alpha()
        
        self.__rotate_buf = rotate_buf
        self.__r_buffer = {}
        self.__rotate_angles = rotate_angles
        self.__r_delta = 360 // self.__rotate_angles
        self.__end_angle = 0
        self.__end_image = None
        self.__angle = 0
        self.__scale = 1
        self.__mirror_x = 0
        self.__mirror_y = 0
        self.generate_rotate_buf()

    @property
    def start_sprite(self):
        return self.__start_sprite

    def generate_rotate_buf(self):
        if self.__rotate_buf:
            
            for i in range(self.__rotate_angles):
                angle = i*self.__r_delta
                rotate_image = pygame.transform.rotate(self.__start_sprite, angle)
                self.__r_buffer[angle] = rotate_image

        
    def set_start_sprite(self, surf):
        self.__start_sprite = surf
        
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

    @property
    def mirror_x(self, m):
        return self.__mirror_x

    @property
    def mirror_y(self, m):
        return self.__mirror_y

    @mirror_x.setter
    def mirror_x(self, m):
        self.__mirror_x = m

    @mirror_y.setter
    def mirror_y(self, m):
        self.__mirror_y = m
        
    def set_attrs(self):
            surf = None
            if not self.__rotate_buf:
                surf = pygame.transform.rotate(self.__start_sprite, self.__angle)
                surf = pygame.transform.scale(surf, [
                        surf.get_width()*self.__scale,
                        surf.get_height()*self.__scale,
                ])
                return surf
            else:
                
                angle = self.__angle-self.__angle%self.__r_delta
                angle = angle % 360
                
                if self.angle != self.__end_angle:
                    self.__end_image = self.__r_buffer[angle]
                    
                self.__end_angle = self.angle
                if self.__end_image is not None:
                    surf = pygame.transform.scale(self.__end_image, [
                        self.__end_image.get_width()*self.__scale,
                        self.__end_image.get_height()*self.__scale,
                    ])
                return surf
        
        
    def render(self, surf: pygame.Surface, center_pos: list[int]):
        render_surf = self.set_attrs()
        try:
            pos = [
                center_pos[0]-render_surf.get_width()/2,
                center_pos[1]-render_surf.get_height()/2
            ]
            if self.__mirror_x:
                render_surf = pygame.transform.flip(render_surf, 1, 0)
            if self.__mirror_y:
                render_surf = pygame.transform.flip(render_surf, 0, 1)
            surf.blit(render_surf, pos)
        except:...
        
class SpriteSheat:
    def __init__(self, file_name: str) -> None:
        self.__file_name = file_name
        self.__image = load_image(self.__file_name)
        self.__cut_surfs = self.cut()
        
    @property
    def sprites(self) -> list[pygame.Surface]:
        return self.__cut_surfs
    
    def cut(self):
        canvas_ = load_image(self.__file_name)

        width_ = canvas_.get_size()[0]
        height_ = canvas_.get_size()[1]

        spritets_coloms = []
        sizes_poses = []

        for i in range(height_):
            c = canvas_.get_at([0, i])
            color = (c[0], c[1], c[2])
            if color == (255, 0, 255):
                spritets_coloms.append(i)

        for col in spritets_coloms:
            for line in range(width_):
                c = canvas_.get_at([line, col])
                color = (c[0], c[1], c[2])
                if color == (255, 255, 0):
                    pos = [line + 1, col]
                    spw = 0
                    sph = 0
                    for sw in range(width_ - line):
                        c = canvas_.get_at([line + sw, col])
                        color = (c[0], c[1], c[2])
                        if color == (0, 0, 255):
                            spw = sw
                            break
                    for sh in range(height_ - col):
                        c = canvas_.get_at([line, col + sh])
                        color = (c[0], c[1], c[2])
                        if color == (0, 0, 255):
                            sph = sh
                            break
                    sizes_poses.append([[pos[0], pos[1] + 1], [spw, sph]])
        textures = []

        for sp in sizes_poses:
            canvas_.set_clip(sp[0], sp[1])
            texture = canvas_.get_clip()
            surft = canvas_.subsurface(texture)
            image = Sprite()
            image.set_start_sprite(surft)
            textures.append(image)
        return textures
        
class SpriteAnim:
    def __init__(self, sprites: any, speed):
        self.__angle = 0
        self.__scale = 1

        self.__mirror_x = 0
        self.__mirror_y = 0
        
        self.__speed = speed
        
        if type(sprites) == SpriteSheat:
            self.__sprites = sprites.sprites
        
        if type(sprites) == list:
            self.__sprites = sprites
            
        self.__index = 0
        self.__sprites_count = len(self.__sprites)
        self.__timer = 0

    @property
    def mirror_x(self, m):
        return self.__mirror_x

    @property
    def mirror_y(self, m):
        return self.__mirror_y

    @mirror_x.setter
    def mirror_x(self, m):
        self.__mirror_x = m

    @mirror_y.setter
    def mirror_y(self, m):
        self.__mirror_y = m
        
    def update(self, delta):
        self.__timer+=1
        if self.__timer>self.__speed/delta:
            self.__index+=1
            self.__timer = 0
        
        if self.__index==self.__sprites_count:
            self.__index = 0
    
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
        for sprite in self.__sprites:
            sprite.angle = self.__angle
            sprite.scale = self.__scale
            sprite.mirror_x = self.__mirror_x
            sprite.mirror_y = self.__mirror_y
            
    def render(self, surf, center_pos):
        self.set_attrs()
        self.__sprites[self.__index].render(surf, center_pos)

