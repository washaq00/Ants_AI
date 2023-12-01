import pygame
from sys import exit
from AppleSpawner import AppleSpawner
from AntsSpawner import AntsSpawner

window_size_h = 1000
window_size_w = 1000

# Set up the windows/background
pygame.init()
screen = pygame.display.set_mode((window_size_w, window_size_h))
pygame.display.set_caption('Gierka')
font = pygame.font.Font(None, 50)
background_surface = pygame.image.load('graphics/background.png').convert_alpha()
background_surface = pygame.transform.scale(background_surface, (1000, 1000))

# set the clock
time_elapsed_since_last_action = 0
clock = pygame.time.Clock()

# Colors
color = (255, 0, 0)
color2 = (0, 0, 255)
color3 = (30, 224, 27)


AntsPopulation = []
ApplesSpawner = []


def initialize():
    # Create the population of ants
    AntsPopulation.append(AntsSpawner())
    AntsPopulation[0].begin()

    # Spawn apples in random locations
    ApplesSpawner.append(AppleSpawner(spawnrate=0.0005, n_bots=20))
    ApplesSpawner[0].begin()

    return True


# drawing characters
def draw(dt=0):

    if len(AntsPopulation[0].Ants) != 0:
        AntsPopulation[0].update(screen, ApplesSpawner[0].Apples,dt)
        ApplesSpawner[0].update(dt, screen)
    else:
        AntsPopulation.clear()
        ApplesSpawner.clear()

def new_gen():
    AntsPopulation.append(AntsSpawner())
    AntsPopulation[0].begin()
    ApplesSpawner.append(AppleSpawner(spawnrate=0.0005, n_bots=20))
    ApplesSpawner[0].begin()


initialized = False

while True:  # all actions are being placed and updated in this loop
    dt = pygame.time.get_ticks()
    initialized = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(background_surface, (0, 0))
    if not AntsPopulation and not initialized:
        initialized = initialize()
    elif not AntsPopulation and initialized:
        new_gen()

    draw(dt)

    pygame.display.update()
    clock.tick(60)
