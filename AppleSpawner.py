from Apple import Apple
import pygame as pg


class AppleSpawner:
    def __init__(self, spawnrate = 2, n_bots = 50):
        self.sr: float = spawnrate
        self.Apples = pg.sprite.Group()
        self.timeElapsed: int = 0
        self.nApples = n_bots

    def begin(self):
        for i in range(0, self.nApples):
            self.Apples.add(Apple())

    def spawn(self, dt = 0):

        print(f"time = {self.timeElapsed} spawnrate = {self.sr}")
        if self.nApples < 50:
            self.timeElapsed += dt/100000
            if self.timeElapsed > self.sr:
                self.timeElapsed = 0
                self.Apples.add(Apple())
                self.nApples +=1

    def update(self,dt, screen):
        self.spawn(dt)
        self.Apples.draw(screen)








