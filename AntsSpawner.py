from Ant import AntBot
import pygame as pg

class AntsSpawner:
    def __init__(self, n_bots=0, mutation = False):
        self.Ants = pg.sprite.Group()
        self.n_ants = n_bots
        self.mutated = mutation

    def begin(self):
        for i in range(0, self.n_ants):
            self.Ants.add(AntBot())

    def update(self,screen,Apples):
        self.Ants.update(Apples, screen)
        self.Ants.draw(screen)

