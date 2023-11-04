import numpy as np
import pygame
from random import randint



class Apple(pygame.sprite.Sprite):
    def __init__(self, h = 20, w = 20):
        super().__init__()
        self.w = w
        self.h = h
        self.pos = pygame.math.Vector2(randint(self.w, 1000 - self.w),randint(self.h, 1000 - self.h))
        self.image, self.rect = self.load_image()

    def load_image(self):
        image = pygame.image.load('graphics/apple.png').convert_alpha()
        player_surf = pygame.transform.scale(image, (self.w, self.h))
        player_rect = player_surf.get_rect(center=(self.pos))
        player_image = player_surf

        return player_image, player_rect
