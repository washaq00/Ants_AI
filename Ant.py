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


def calculate_angle_diff(org_angle, food_angle):
    food_angle %= 360
    angle_difference = org_angle - food_angle

    if angle_difference > 180:
        angle_difference -= 360
    if angle_difference < -180:
        angle_difference += 360

    return angle_difference


class AntBot(pygame.sprite.Sprite):
    def __init__(self, w=40, h=40):
        super().__init__()
        self.w = w
        self.h = h

        # Basic variables
        self.pos = pygame.math.Vector2(randint(self.w, 1000 - self.w), randint(self.h, 1000 - self.h))
        self.center = 0
        self.angle = np.random.randint(0,360)
        self.speed = 2

        #distance to the closest apple
        self.distance = 0
        self.distance_x = 0
        self.distance_y = 0
        self.vision_angle = 30
        self.vision_radius = 250
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
        player_rect = player_surf.get_rect(topleft=(self.pos[0],self.pos[1]))
        self.center = player_rect.center
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
        return temp_distance

    def eating_food(self, apple):
        eats_apple = self.rect.colliderect(apple.rect)
        if eats_apple:
            self.score += 50
            temp_health = self.health + 100
            if temp_health > 300:
                self.health = 300
            else:
                self.health = temp_health
            apple.kill()
            return True
        return False

    def in_range(self, apple):
        if self.calculate_distance(apple) < self.vision_radius:
            apple_angle = calculate_angle(self.pos, apple.pos)
            left_bound = (self.angle - self.vision_angle) % 360
            right_bound = (self.angle + self.vision_angle) % 360
            if (left_bound < apple_angle % 360 < right_bound) or (right_bound < left_bound and not (right_bound < apple_angle % 360 < left_bound)):
                return True
        return False

    def find_closest(self, apples_list, screen):
        temp_distance = 10000
        for apple in apples_list:
            calculated = self.calculate_distance(apple)
            if calculated < temp_distance:
                temp_distance = calculated
                closest_apple = apple

        if closest_apple is not None:
            pygame.draw.line(screen, (255,0,0),self.pos, closest_apple.pos, width=1)
            self.angle_diff = calculate_angle_diff(self.angle, calculate_angle(self.pos, closest_apple.pos))
            self.distance = temp_distance

    def loop_for_apples(self,Apples, screen):
        apples_in_range = []
        for apple in Apples.Apples:
            if self.eating_food(apple):
                Apples.nApples -= 1
                continue
            if self.in_range(apple):
                apples_in_range.append(apple)
        if len(apples_in_range) > 0:
            self.find_closest(apples_in_range, screen)
        apples_in_range.clear()

    def forward(self, pos):
        temp1 = pos[0]
        temp2 = pos[1]
        temp1 += math.cos(math.radians(360 - self.angle)) * self.speed
        temp2 += math.sin(math.radians(360 - self.angle)) * self.speed
        return temp1, temp2

    def turn_right(self):
        self.angle += 3

    def turn_left(self):
        self.angle -= 3

    def move(self, output, pos):

        max_val = max(output)
        choice = np.where(output == max_val)
        temp1, temp2 = 0,0

        if choice[0] == 0:
            self.turn_left()
        elif choice[0] == 1:
            self.turn_right()

        # elif choice[0] == 2:
        #     temp1, temp2 = self.forward(pos)

        temp1, temp2 = self.forward(pos)

        self.angle = self.angle % 360
        self.image = self.rotate_center(self.base_image)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.center = self.rect.center

        if (1000 - self.w / 2 > temp1 > self.w / 2) and (self.h / 2 < temp2 < 1000 - self.h / 2):
            self.pos = temp1, temp2


    def draw_rect(self, screen):
        pygame.draw.rect(screen,(255,0,0),self.rect)

    def draw_sensor(self, screen):
        start_angle, stop_angle = self.angle - self.vision_angle,self.angle + self.vision_angle
        rect = pygame.Rect(self.pos[0]-self.vision_radius*2*0.5+self.w*0.5, self.pos[1]-self.vision_radius*2*0.5+self.h*0.5, self.vision_radius*2, self.vision_radius*2)
        pygame.draw.arc(screen,(255, 0, 0),rect,start_angle*math.pi/180, stop_angle*math.pi/180, 2)

    def update(self, AppleSpawner, screen):
        self.loop_for_apples(AppleSpawner, screen)
        self.draw_sensor(screen)
        print(self.angle_diff)
        params = self.Brain.forward(self.distance, self.angle_diff)
        self.move(*params, self.pos)
        self.draw_rect(screen)
        self.health -= 1



