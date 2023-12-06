from Ant import AntBot
import pygame as pg

class AntsSpawner:
    def __init__(self, n_bots=8, mutation = False):
        self.Ants = pg.sprite.Group()
        self.n_ants = n_bots
        self.mutated = mutation
        self.timeElapsed = 0

    def begin(self):
        for i in range(0, self.n_ants):
            self.Ants.add(AntBot())

    def update(self,screen,Apples,CopiedPopulation):
        for ant in self.Ants:
            if ant.health < 0:
                CopiedPopulation.add(ant)
                ant.remove(self.Ants)
        self.Ants.update(Apples, screen)
        self.Ants.draw(screen)



