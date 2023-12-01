import pygame
import numpy as np
import math
from random import randint
from NN import NeuralNetwork

CASTED_RAYS = 2


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
        self.angle = np.random.randint(0,90)
        self.speed = 3

        #distance to the closest apple
        self.distance = 1000

        # Loading image and rotated image
        self.base_image, self.rect = self.load_image()
        self.image = self.base_image

        # Track the score
        self.health = 300
        self.score = 0

        # Moves our character
        self.Brain = NeuralNetwork()

    def __del__(self):
        pass

    def load_image(self):
        image = pygame.image.load('graphics/player1.png').convert_alpha()
        player_surf = pygame.transform.scale(image, (self.w, self.h))
        player_surf = pygame.transform.rotate(player_surf, -90)
        player_rect = player_surf.get_rect(center=self.center)
        player_image = player_surf

        return player_image, player_rect

    def rotate_center(self, image):
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, self.angle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image

    def calculate_distance(self, apple):
        temp_distance = np.sqrt(np.square(self.pos[0] - apple.pos[0]) + np.square(self.pos[1] - apple.pos[1]))
        if temp_distance < self.distance:
            self.distance = temp_distance

    def collisions_and_distance(self, Apples):

        for apple in Apples:
            self.calculate_distance(apple)
            eats_apple = self.rect.colliderect(apple.rect)
            if eats_apple:
                self.score += 1
                temp_health = self.health + 50
                self.distance = 1500
                if temp_health > 300:
                    self.health = 300
                else:
                    self.health = temp_health
                apple.kill()
        self.health -= 1

    def cast_rays(self, screen):
        start_angle = self.angle-30

        for ray in range(CASTED_RAYS):
            end = int(self.pos[0] - (math.sin(360-start_angle)) * 100), int(self.pos[1] + (math.cos(360-start_angle)) * 100)
            pygame.draw.line(screen, (0, 255, 0), self.center, end, 2)
            start_angle += 60

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

        if skip:
            temp1 += math.cos(math.radians(360 - self.angle)) * self.speed
            temp2 += math.sin(math.radians(360 - self.angle)) * self.speed

        if (1000 - self.w / 2 > temp1 > self.w / 2) and (self.h / 2 < temp2 < 1000 - self.h / 2):
            self.image = self.rotate_center(self.base_image)
            self.pos = temp1, temp2
            self.center = [self.pos[0] + self.h / 2, self.pos[1] + self.w / 2]
            self.rect = self.image.get_rect(center=self.center)

    def update(self, Apples, screen):
        self.collisions_and_distance(Apples)
        # self.cast_rays(screen)
        params = self.Brain.forward(self.distance, self.health, self.score)
        self.move(*params, self.pos)
