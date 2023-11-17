import pygame
import numpy as np
import math
from random import randint
from NN import NeuralNetwork


def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)


class AntBot(pygame.sprite.Sprite):
    def __init__(self, w=40, h=40):
        super().__init__()
        self.w = w
        self.h = h

        # Basic variables
        self.pos = pygame.math.Vector2(randint(self.w, 1000 - self.w), randint(self.h, 1000 - self.h))
        self.center = [self.pos[0] + self.h / 2, self.pos[1] + self.w / 2]
        self.angle = 0
        self.speed = 5

        # Loading image and rotated image
        self.base_image, self.rect = self.load_image()
        self.image = self.base_image

        # Capture distances to the apples
        self.sensors = []
        self.drawn_sensors = []

        # Track the score
        self.health = 100
        self.score = 0

        # Moves our character
        self.Brain = NeuralNetwork()

    def __del__(self):
        print(f"One ant is dead")

    def load_image(self):
        image = pygame.image.load('graphics/player1.png').convert_alpha()
        player_surf = pygame.transform.scale(image, (self.w, self.h))
        player_rect = player_surf.get_rect(center=self.center)
        player_image = player_surf

        return player_image, player_rect

    def rotate_center(self, image, angle):
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image

    def check_collisions(self, Apples):
        if self.health < 0:
            self.kill()
        for apple in Apples:
            eats_apple = self.rect.colliderect(apple.rect)
            if eats_apple:
                self.score += 1
                self.health += 10
                apple.kill()
        self.health -= 1

    def draw_sensors(self, screen):
        for radar in self.sensors:
            position = radar[0]
            pygame.draw.line(screen, (0, 255, 0), self.center, position, 1)
            pygame.draw.circle(screen, (0, 255, 0), position, 5)

    def move(self, output, pos):

        max_val = max(output)
        choice = np.where(output == max_val)
        skip: bool = False

        temp1 = pos[0]
        temp2 = pos[1]

        if choice[0] == 0:
            self.angle += 10
            skip = True
        elif choice[0] == 1:
            self.angle -= 10
            skip = True
        elif choice[0] == 2:
            temp1 += math.cos(math.radians(360 - self.angle)) * self.speed
            temp2 += math.sin(math.radians(360 - self.angle)) * self.speed
        elif choice[0] == 3:
            temp1 -= math.cos(math.radians(360 - self.angle)) * self.speed
            temp2 -= math.sin(math.radians(360 - self.angle)) * self.speed

        if skip:
            temp1 += math.cos(math.radians(360 - self.angle)) * self.speed
            temp2 += math.sin(math.radians(360 - self.angle)) * self.speed

        if (1000 - self.w / 2 > temp1 > self.w / 2) and (self.h / 2 < temp2 < 1000 - self.h / 2):
            self.image = self.rotate_center(self.base_image, self.angle)
            self.pos = temp1, temp2
            print(self.pos)
            self.center = [self.pos[0] + self.h / 2, self.pos[1] + self.w / 2]
            self.rect = self.image.get_rect(center=self.center)

    def update(self, Apples, screen):
        self.check_collisions(Apples)
        self.draw_sensors(screen)
        params = self.Brain.calculate(self.health, self.score)
        self.move(*params, self.pos)
