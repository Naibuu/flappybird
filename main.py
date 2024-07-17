import pygame
import constants
import random

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

        self.sheet = pygame.image.load('sprites/bird.png')
        self.frame = 0
        self.delay = 0
        self.velocity = 0
        self.pressed = False

        self.image = pygame.Surface((34, 24))
        self.image.blit(self.sheet, (0, 0), (34, 0, 34, 24))
        self.image.set_colorkey("BLACK")
        
        self.rect = self.image.get_rect()
        self.rect.center = (100, 200)

    def update(self):
        if constants.GAME_START == True and constants.GAME_OVER == False:
            # Gravity
            self.velocity += 0.5

            if self.velocity > 8:
                self.velocity = 8

            if self.rect.bottom < 400:
                self.rect.y += int(self.velocity)

            # Pressing
            if pygame.mouse.get_pressed()[0] == 1 and self.pressed == False:
                self.pressed = True
                self.velocity = -8
                pygame.mixer.Sound('sounds/flap.ogg').play()

            if pygame.mouse.get_pressed()[0] == 0:
                self.pressed = False

            # Sprite frames
            self.delay += 1

            if self.delay > 3:
                self.delay = 0
                self.frame += 1

            if self.frame > 2:
                self.frame = 0

            self.image.fill(0)
            self.image.blit(self.sheet, (0, 0), ((self.frame * self.rect.width), 0, self.rect.width, self.rect.height))

bird = Bird()
bird_group = pygame.sprite.Group()
bird_group.add(bird)

# Pipe
class Pipe(pygame.sprite.Sprite):
    def __init__(self, y, flip):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('sprites/pipe.png')
        self.rect = self.image.get_rect()

        # Flip
        if flip == True:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = (576, y - (constants.PIPE_GAP / 2))
        else: 
            self.rect.topleft = (576, y + (constants.PIPE_GAP / 2))

    def update(self):
        self.rect.x -= constants.GAME_SPEED

        if self.rect.right < 0:
            self.kill()

pipe_group = pygame.sprite.Group()

run = True

while run:
    clock.tick(constants.FRAMERATE)

    # Background
    screen.blit(background, (0, 0))

    # Groups
    bird_group.draw(screen)
    bird_group.update()

    # If bird hits the ground
    if bird.rect.bottom >= 400:
        constants.GAME_START = False
        constants.GAME_OVER = True
    # If bird collids with pipe or hits the top
    elif pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or bird.rect.top < 0:
        constants.GAME_START = False
        constants.GAME_OVER = True

    pipe_group.draw(screen)

    # Ground
    screen.blit(ground, (constants.GROUND_SCROLL, 400))

    # If game started
    if constants.GAME_START == True and constants.GAME_OVER == False:
        ticks = pygame.time.get_ticks()

        # Move pipes
        pipe_group.update()

        if ticks - constants.LAST_PIPE > constants.PIPE_FREQUENCY:
            random_y = random.randint(-100, 100)

            top_pipe = Pipe(200 + random_y, True)
            bottom_pipe = Pipe(200 + random_y, False)

            pipe_group.add(top_pipe)                
            pipe_group.add(bottom_pipe)

            constants.LAST_PIPE = ticks

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