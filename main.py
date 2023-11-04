import pygame
from sys import exit
from Ant import AntBot
from Apple import Apple

window_size_h = 1000
window_size_w = 1000

#Set up the windows/background
pygame.init()
screen = pygame.display.set_mode((window_size_w,window_size_h))
pygame.display.set_caption('Gierka')
font = pygame.font.Font(None, 50)
background_surface = pygame.image.load('graphics/background.png').convert_alpha()
background_surface = pygame.transform.scale(background_surface,(1000,1000))

#set the clock
time_elapsed_since_last_action = 0
ant_h= 0
clock = pygame.time.Clock()



#Colors
color = (255, 0, 0)
color2 = (0,0,255)
color3 = (30, 224, 27)

# Bots
n_bots = 5
# Ants = pygame.sprite.Group
# for i in range(0,n_bots):
#     ant = AntBot(40,40)
#     Ants.add(ant)
Ants = pygame.sprite.Group()
for i in range(0,n_bots):
    Ants.add(AntBot())


# Apples
n_apples = 20
Apples = pygame.sprite.Group()

for i in range(0,n_apples):
    Apples.add(Apple())


# drawing characters
def draw(ant_h=0):
    ant_h += dt

    for ant in Ants:
        if ant.health < 0:
            ant.kill()
        for apple in Apples:
            eats_apple = ant.rect.colliderect(apple.rect)
            if eats_apple:
                ant.score += 1
                ant.health += 10
                apple.kill()

        if ant_h > 2:
            ant.health -= 1
            ant_h = 0


    Ants.draw(screen)
    Apples.draw(screen)
    Ants.update()


while True: # all actions are being placed and updated in this loop
    dt = clock.tick()
    time_elapsed_since_last_action += dt
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.blit(background_surface, (0, 0))
    draw(clock.tick())

    if time_elapsed_since_last_action > 1:
        Apples.add(Apple())
        time_elapsed_since_last_action = 0

    pygame.display.update()
    clock.tick(24)