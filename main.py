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

AntsPopulation = []
CopyOfPopulation = pygame.sprite.Group()
ApplesSpawner = []

def initialize():
    # Create the population of ants
    AntsPopulation.append(AntsSpawner())
    AntsPopulation[0].begin()

    # Spawn apples in random locations
    ApplesSpawner.append(AppleSpawner(n_bots=50))
    ApplesSpawner[0].begin()
    return True


# drawing characters
def draw(t):

    if len(AntsPopulation[0].Ants) != 0:
        AntsPopulation[0].update(screen, ApplesSpawner[0].Apples, CopyOfPopulation)
        ApplesSpawner[0].update(t, screen)

    else:
        AntsPopulation.clear()
        ApplesSpawner.clear()


initialized = False
pop_counter:int = 0

while True:
    dt = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(background_surface, (0, 0))
    if not AntsPopulation and not initialized:
        initialized = initialize()
        pop_counter += 1
    elif not AntsPopulation and initialized:
        pop_counter += 1
        ApplesSpawner.append(AppleSpawner(n_bots=50))
        ApplesSpawner[0].begin()

        AntsPopulation.append(population(CopyOfPopulation))
        CopyOfPopulation.empty()

    draw(dt)
    text = font.render(f'Population: {pop_counter}', True, color2)
    textRect = text.get_rect()
    textRect.center = (90, 40)
    screen.blit(text, textRect)
    pygame.display.update()
    clock.tick(60)
