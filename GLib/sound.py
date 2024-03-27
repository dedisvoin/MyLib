import pygame
pygame.mixer.init()
class Sound:
    def __init__(self, file_name) -> None:
        self.file_name = file_name
        self.sound = pygame.mixer.Sound(self.file_name)

    def set_volume_by_dist(self, dist, max_dist):
        vol = (1-dist/max_dist)
        self.sound.set_volume(vol)

    def play(self):
        self.sound.play()