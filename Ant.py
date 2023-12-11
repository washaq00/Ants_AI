import pygame
import numpy as np
import math
from random import randint
from NN import NeuralNetwork

CASTED_RAYS = 1


def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)


def calculate_angle(point1, point2, invert=-1):
    if point2[0] - point1[0] == 0:
        if point2[1] - point1[1] > 0:
            return 90
        else:
            return -90
    else:
        return math.degrees(math.atan2(invert * (point2[1] - point1[1]), (point2[0] - point1[0])))


class AntBot(pygame.sprite.Sprite):
    def __init__(self, w=40, h=40):
        super().__init__()
        self.w = w
        self.h = h

        # Basic variables
        self.pos = pygame.math.Vector2(randint(self.w, 1000 - self.w), randint(self.h, 1000 - self.h))
        self.center = [self.pos[0] + self.h / 2, self.pos[1] + self.w / 2]
        self.angle = np.random.randint(0,360)
        self.speed = 2

        #distance to the closest apple
        self.distance = 0
        self.distance_x = 0
        self.distance_y = 0
        self.angle_diff = 0

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
        distance_x = self.pos[0] - apple.pos[0]
        distance_y = self.pos[1] - apple.pos[1]
        temp_distance = np.sqrt(np.square(distance_x) + np.square(distance_y))
        return temp_distance, distance_x, distance_y

    def collisions_and_distance(self, Apples):
        distance = 10000
        distance_x = 10000
        distance_y = 10000

        for apple in Apples:
            temp_distance, temp_distance_x, temp_distance_y = self.calculate_distance(apple)
            if distance > temp_distance:
                distance_x = temp_distance_x
                distance_y = temp_distance_y
                closest_apple = apple
            eats_apple = self.rect.colliderect(apple.rect)
            if eats_apple:
                self.score += 50
                temp_health = self.health + 100
                if temp_health > 300:
                    self.health = 300
                else:
                    self.health = temp_health
                apple.kill()
        self.distance = distance
        self.distance_x = distance_x
        self.distance_y = distance_y
        self.angle_diff = calculate_angle(self.pos,closest_apple.pos)

        self.health -= 1

    def cast_rays(self, screen):
        self.draw_sensor(screen)

    def move(self, output, pos):

        max_val = max(output)
        choice = np.where(output == max_val)
        skip: bool = False

        temp1 = pos[0]
        temp2 = pos[1]

        temp_angle = self.angle

        if choice[0] == 0:
            temp_angle += 10
            self.angle = temp_angle%360
            skip = True
        elif choice[0] == 1:
            temp_angle -= 10
            self.angle = temp_angle % 360
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

    def draw_sensor(self, screen):
        start_angle, stop_angle = self.angle - 45,self.angle + 45
        rect = self.rect.copy()
        rect.scale_by_ip(4.0,4.0)
        pygame.draw.arc(screen,(255, 0, 0),rect,start_angle*math.pi/180, stop_angle*math.pi/180, 2)

    def calculate_angle_diff(self,org_angle, food_angle):
        food_angle %= 360
        angle_difference = org_angle - food_angle

        if angle_difference > 180:
            angle_difference -= 360
        if angle_difference < -180:
            angle_difference += 360

        return angle_difference

    def update(self, Apples, screen):
        self.collisions_and_distance(Apples)
        self.cast_rays(screen)
        params = self.Brain.forward(self.distance, self.angle_diff,self.health)
        self.move(*params, self.pos)


