import pygame
import numpy as np
import math
from random import randint



class AntBot(pygame.sprite.Sprite):
    def __init__(self, w=40, h=40):
        super().__init__()
        self.w = w
        self.h = h
        self.pos = pygame.math.Vector2(randint(self.w, 1000 - self.w),randint(self.h, 1000 - self.h))
        self.angle = 0
        self.speed = 3
        self.base_image, self.rect = self.load_image()
        self.image = self.base_image
        self.health = 100
        self.score = 0

    def __del__(self):
        print(f"One ant is dead")

    def load_image(self):
        image = pygame.image.load('graphics/player1.png').convert_alpha()
        player_surf = pygame.transform.scale(image, (self.w, self.h))
        player_rect = player_surf.get_rect(center=self.pos)
        player_image = player_surf

        return player_image, player_rect

    def move(self):
        temp: float = self.pos[0]
        temp2: float = self.pos[1]

        self.angle -= randint(-60, 60)
        temp += self.speed * math.cos(math.radians(self.angle + 90))
        temp2 -= self.speed * math.sin(math.radians(self.angle + 90))
        if (1000 - self.w > temp > self.w) and (self.h < temp2 < 1000 - self.h):
            self.pos[0] = temp
            self.pos[1] = temp2
        self.image = pygame.transform.rotate(self.base_image, self.angle)
        self.rect = self.image.get_rect(center = self.pos)


    def update(self):
        self.move()







