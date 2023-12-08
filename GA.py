from AntsSpawner import AntsSpawner
from Ant import AntBot
import numpy as np


def best_genes(pop):
    """

    Function used for finding N (default 2) best genes,
    defined my own fitness score function

    """

    fitness_scores: list[[int, ]] = []
    score: int
    for ant in pop:
        if ant.score < 1: ant.score = 1
        score = (ant.score * 100) / ant.distance
        fitness_scores.append((score, ant))

    sorted_scores = sorted(fitness_scores, key=lambda x: x[0], reverse=True)

    return sorted_scores


def mutate_and_inheritance(parents, mutation_chance=70) -> list:
    # proportion_dict = {
    #     "60:40": 0.6,
    #     "70:30": 0.7,
    #     "80:20": 0.8
    # }

    kids = [AntBot() for i in range(0, 2)]

    for id_kid, kid in enumerate(kids):
        for id_layer, (layer, is_activated) in enumerate(kid.Brain.layers):

            # custom_range = [[0, layer.input_size * proportion_dict[variant]],
            #                     [layer.input_size * proportion_dict[variant], layer.input_size]]

            if not is_activated:
                for i in range(0, layer.input_size):
                    for j in range(0, int(layer.output_size /2)):
                        if mutation_chance > np.random.randint(0, 100):
                            layer.weights[i, j] = np.random.randn(1, 1)
                            layer.bias[0, j] = np.random.randn(1, 1)
                        else:
                            layer.weights[i, j] = parents[id_kid].Brain.layers[id_layer][0].weights[i, j]
                            layer.bias[0, j] = parents[id_kid].Brain.layers[id_layer][0].bias[0, j]
                for i in range(0, layer.input_size):
                    for j in range(int(layer.output_size /2), layer.output_size):
                        if mutation_chance > np.random.randint(0, 100):
                            layer.weights[i, j] = np.random.randn(1, 1)
                            layer.bias[0, j] = np.random.randn(1, 1)
                        else:
                            layer.weights[i, j] = parents[id_kid].Brain.layers[id_layer][0].weights[i, j]
                            layer.bias[0, j] = parents[id_kid].Brain.layers[id_layer][0].bias[0, j]
            else:
                pass

    return kids


def population(copied_population, P=2):
    """

    New population consists of:
                                - 2 parents - best ants from previous population
                                - 2 kids that inherit mutated genes from parents
                                - N new randomly generated ants

    """

    sorted_population = [genes[1] for genes in best_genes(copied_population)]
    parents = sorted_population[:2]
    new_population = AntsSpawner()

    for i in range(0, (len(sorted_population)-2)):
        new_population.Ants.add(AntBot())

    for id,ant in enumerate(new_population.Ants):
        ant.Brain = sorted_population[id].Brain

    kids = mutate_and_inheritance(parents)

    for i in range(0, P):
        new_population.Ants.add(kids[i])

    return new_population
