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
    AntsPopulation.append(AntsSpawner(n_bots=5))
    AntsPopulation[0].begin()

    # Spawn apples in random locations
    ApplesSpawner.append(AppleSpawner(spawnrate=0.0005, n_bots=20))
    ApplesSpawner[0].begin()

    return AntsPopulation


# drawing characters
def draw(dt=0):

    if AntsPopulation[0].Ants.has:
        for ant in AntsPopulation[0].Ants:
            if ant.health < 0:
                ant.kill()
            for apple in ApplesSpawner[0].Apples:
                eats_apple = ant.rect.colliderect(apple.rect)
                if eats_apple:
                    ant.score += 1
                    ant.health += 10
                    apple.kill()
            ant.health -= 1

        ApplesSpawner[0].spawn(dt)
        AntsPopulation[0].Ants.draw(screen)
        ApplesSpawner[0].Apples.draw(screen)
        AntsPopulation[0].Ants.update()


while True:  # all actions are being placed and updated in this loop
    dt = clock.tick()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(background_surface, (0, 0))
    if not AntsPopulation:
        initialize()
        CopyPopulation = AntsPopulation[0].Ants.copy()


    draw(dt)

    pygame.display.update()
    clock.tick(24)
