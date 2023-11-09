import pygame
import numpy as np
import math
from random import randint
from NN import NeuralNetwork


class AntBot(pygame.sprite.Sprite):
    def __init__(self, w=40, h=40):
        super().__init__()
        self.w = w
        self.h = h
        self.pos = pygame.math.Vector2(randint(self.w, 1000 - self.w), randint(self.h, 1000 - self.h))
        self.angle = 0
        self.base_image, self.rect = self.load_image()
        self.image = self.base_image
        self.health = 100
        self.score = 0
        self.Brain = NeuralNetwork()

    def __del__(self):
        print(f"One ant is dead")

    def load_image(self):
        image = pygame.image.load('graphics/player1.png').convert_alpha()
        player_surf = pygame.transform.scale(image, (self.w, self.h))
        player_rect = player_surf.get_rect(center=self.pos)
        player_image = player_surf

        return player_image, player_rect

    def clamp(self, num, min_value, max_value):
        return max(min(num, max_value), min_value)

    def move(self, pos):
        # describe the movement and clamp it in the range
        LR = self.clamp(pos[0], -2, 2)
        FB = self.clamp(pos[1], -2, 2)

        if (1000 - self.w > LR + self.pos[0] > self.w) and (self.h < FB + self.pos[1] < 1000 - self.h):
            # calculate the angle
            self.angle =  np.degrees(math.atan2(self.pos[0] - self.pos[1], self.pos[0] - self.pos[1] ))
            print(self.angle)
            # negative angle because y-axis is flipped
            # self.image = pygame.transform.rotate(self.base_image, self.angle)
            self.rect = self.image.get_rect(center=self.pos)
            # new position of Ant
            self.pos[0] += LR
            self.pos[1] += FB



    def update(self):
        params = self.Brain.calculate(self.health, self.score)
        print(params)
        self.move(*params)
