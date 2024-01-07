import pygame
from sys import exit
from AppleSpawner import AppleSpawner
from AntsSpawner import AntsSpawner
from GA import best_genes, population

window_size_h = 1000
window_size_w = 1000

# Set up the windows/background
pygame.init()
screen = pygame.display.set_mode((window_size_w, window_size_h))
pygame.display.set_caption('Gierka')
background_surface = pygame.image.load('graphics/background.png').convert_alpha()
background_surface = pygame.transform.scale(background_surface, (1000, 1000))
font = pygame.font.Font('freesansbold.ttf', 25)

# set the clock
time_elapsed_since_last_action = 0
clock = pygame.time.Clock()

# Colors
color = (255, 0, 0)
color2 = (0, 0, 255)
color3 = (30, 224, 27)

ants_population = []
copy_population = pygame.sprite.Group()
apples_spawner = []


def initialize():
    # Create the population of ants
    ants_population.append(AntsSpawner())
    ants_population[0].begin()

    # Spawn apples in random locations
    apples_spawner.append(AppleSpawner())
    apples_spawner[0].begin()
    return True


# drawing characters
def draw(t):
    if len(ants_population[0].Ants) != 0:
        ants_population[0].update(screen, apples_spawner[0], copy_population)
        apples_spawner[0].update(t, screen)

    else:
        ants_population.clear()
        apples_spawner.clear()


initialized = False
pop_counter: int = 0
score: int = 0
list_of_scores = []

while pop_counter <= 20:
    dt = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(background_surface, (0, 0))
    if not ants_population and not initialized:
        initialized = initialize()
        pop_counter += 1
        if score:
            list_of_scores.append(score)
            score = 0
    elif not ants_population and initialized:
        pop_counter += 1
        apples_spawner.append(AppleSpawner())
        apples_spawner[0].begin()
        if score:
            list_of_scores.append(score)
            score = 0
        ants_population.append(population(copy_population))
        copy_population.empty()

    score = max(score, ants_population[0].best_score())

    draw(dt)
    text = font.render(f'Population: {pop_counter} | best score: {score}', True, color2)
    textRect = text.get_rect()
    textRect.midleft = (0, 40)
    screen.blit(text, textRect)
    pygame.display.update()
    clock.tick(60)

print(list_of_scores)
