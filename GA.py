from AntsSpawner import AntsSpawner
from Ant import AntBot
def best_genes(population, N = 2):

    """Function used for finding N (default 2) best genes
        defined my own fitness score function"""

    fitness_scores: list[[int,]] = []
    score: int
    for ant in population:
        if ant.score < 1: ant.score = 1
        score = (ant.score * 1000) / ant.distance
        fitness_scores.append([score,ant])

    sorted_scores = sorted(fitness_scores, key= lambda x: x[0], reverse=True)

    return sorted_scores[:N][1]

def inheritance(parents):
    kid1 = AntBot()
    kid2 = AntBot()

    self.score = Ant.score
    self.distance = Ant.distance
    self.Brain = Ant.Brain

    return

def new_population(copied_population, P=2):

    """New population consists of:
                                - 2 parents - best ants from previous population
                                - 2 kids that inherit mutated genes from parents
                                - N new randomly generated ants
    """

    parents = best_genes(copied_population)

    new_pop = AntsSpawner()
    for i in range(0, new_pop.n_ants-P**2):
        new_pop.Ants.add(AntBot())

    for i in range(0,P):
        new_pop.Ants.add(parents[i])

    kids = inheritance(parents)

    for i in range(0,P):
        new_pop.Ants.add(kids[i])

    return new_pop




