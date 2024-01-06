from Ant import AntBot
import pygame as pg


class AntsSpawner:
    def __init__(self, n_bots=10, mutation=False):
        self.Ants = pg.sprite.Group()
        self.n_ants = n_bots
        self.mutated = mutation
        self.timeElapsed = 0

    def begin(self):
        for i in range(0, self.n_ants):
            self.Ants.add(AntBot())

    def update(self, screen, Apples, CopiedPopulation):
        for ant in self.Ants:
            if ant.health < 0:
                CopiedPopulation.add(ant)
                ant.remove(self.Ants)
        self.Ants.update(Apples, screen)
        self.Ants.draw(screen)

    def best_score(self):
        temp = []
        for ant in self.Ants:
            temp.append(ant.score)
        if temp:
            max_val = max(temp)
            temp.clear()
            return max_val
        else: return 0
