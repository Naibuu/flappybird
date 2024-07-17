import pygame
import constants

pygame.init()

# Screen
screen = pygame.display.set_mode(( constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT ))
pygame.display.set_caption("Flappybird")

# Clock
clock = pygame.time.Clock()

# Sprites
background = pygame.image.load('sprites/background.png')
ground = pygame.image.load("sprites/ground.png")

# Bird
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.sheet = pygame.image.load('sprites/bird.png').convert_alpha()
        self.frame = 0
        self.delay = 0

        self.image = pygame.Surface((34, 24))
        self.image.blit(self.sheet, (0, 0), (34, 0, 34, 24))
        self.image.set_colorkey("BLACK")
        
        self.rect = self.image.get_rect()
        self.rect.center = (100, 200)

    def update(self):
        if constants.GAME_START == True and constants.GAME_OVER == False:
            self.delay += 1

            if self.delay > 5:
                self.delay = 0
                self.frame += 1

            if self.frame > 2:
                self.frame = 0

            self.image.fill(0)
            self.image.blit(self.sheet, (0, 0), ((self.frame * self.rect.width), 0, self.rect.width, self.rect.height))

bird = Bird()
bird_group = pygame.sprite.Group()
bird_group.add(bird)

run = True

while run:
    clock.tick(constants.FRAMERATE)

    # Background
    screen.blit(background, (0, 0))

    # Bird
    bird_group.draw(screen)
    bird_group.update()

    # Ground
    screen.blit(ground, (constants.GROUND_SCROLL, 400))

    # If game started
    if constants.GAME_START == True and constants.GAME_OVER == False:
        # Move ground
        constants.GROUND_SCROLL -= constants.GAME_SPEED

        if abs(constants.GROUND_SCROLL) > 22:
            constants.GROUND_SCROLL = 0

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and constants.GAME_START == False and constants.GAME_OVER == False:
            constants.GAME_START = True

    pygame.display.update()

pygame.quit()