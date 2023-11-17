from Apple import Apple
import pygame as pg


class AppleSpawner:
    def __init__(self, spawnrate = 1, n_bots = 0):
        self.sr: float = spawnrate
        self.Apples = pg.sprite.Group()
        self.timeElapsed: int = 0
        self.nApples = n_bots

    def begin(self):
        for i in range(0, self.nApples):
            self.Apples.add(Apple())

    def spawn(self, dt = 0):

        if self.nApples == 0:
            self.begin()
        elif self.nApples < 30:
            self.timeElapsed += dt
            if self.timeElapsed >= self.sr:
                self.timeElapsed = 0
                self.Apples.add(Apple())
                self.nApples +=1

    def update(self,dt, screen):
        self.spawn(dt)
        self.Apples.draw(screen)








