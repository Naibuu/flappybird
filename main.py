import pygame
import constants
import random

pygame.init()

# Screen
screen = pygame.display.set_mode(( constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT ))
pygame.display.set_caption("Flappybird")

# Clock
clock = pygame.time.Clock()

# Graphics
background = pygame.image.load('assets/sprites/background.png')
ground = pygame.image.load("assets/sprites/ground.png")
game_start = pygame.image.load('assets/sprites/game_start.png')
game_over = pygame.image.load('assets/sprites/game_over.png')

# Font
font = pygame.font.Font('assets/munro.ttf', 32)

# Reset
def reset():
    constants.SCORE = 0
    constants.GAME_OVER = False
    pipe_group.empty()
    bird.rect.center = (100, 200)


# Bird
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.sheet = pygame.image.load('assets/sprites/bird.png')
        self.frame = 0
        self.delay = 0
        self.velocity = 0
        self.pressed = False

        self.image = pygame.Surface((34, 24), pygame.SRCALPHA)
        self.image.blit(self.sheet, (0, 0), (34, 0, 34, 24))
        
        self.rect = self.image.get_rect()
        self.rect.center = (100, 200)

    def update(self):
        if constants.GAME_START and not constants.GAME_OVER:
            # Gravity
            self.velocity += 0.5

            if self.velocity > 8:
                self.velocity = 8

            if self.rect.bottom < 400:
                self.rect.y += int(self.velocity)

            # Pressing
            if pygame.mouse.get_pressed()[0] and not self.pressed:
                self.pressed = True
                self.velocity = -8
                pygame.mixer.Sound('assets/sounds/flap.ogg').play()

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
            self.image.blit(self.sheet, (0, 0), (self.frame * 34, 0, 34, 24))

bird = Bird()
bird_group = pygame.sprite.Group(bird)

# Pipe
class Pipe(pygame.sprite.Sprite):
    def __init__(self, y, flip):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('assets/sprites/pipe.png')
        self.rect = self.image.get_rect()

        # Flip
        if flip:
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
    screen.blit(background, (0, 0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    # Bird collision
    if bird.rect.bottom >= 400:
        constants.GAME_START = False
        constants.GAME_OVER = True

    elif pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or bird.rect.top < 0:
        constants.GAME_START = False
        constants.GAME_OVER = True

    screen.blit(ground, (constants.GROUND_SCROLL, 400))

    # Increment score after passing a pipe
    if len(pipe_group) > 0:
        if bird.rect.left < pipe_group.sprites()[0].rect.left and not constants.PIPE_PASSED:
            constants.PIPE_PASSED = True

        if constants.PIPE_PASSED:
            if bird.rect.left > pipe_group.sprites()[0].rect.right - 24:
                constants.SCORE += 1
                pygame.mixer.Sound('assets/sounds/point.ogg').play()
                constants.PIPE_PASSED = False

    # On game start
    if constants.GAME_START and not constants.GAME_OVER:
        ticks = pygame.time.get_ticks()

        # Move pipes
        pipe_group.update()

        if ticks - constants.LAST_PIPE > constants.PIPE_FREQUENCY:
            random_y = random.randint(-100, 80)

            top_pipe = Pipe(200 + random_y, True)
            bottom_pipe = Pipe(200 + random_y, False)

            pipe_group.add(top_pipe)                
            pipe_group.add(bottom_pipe)

            constants.LAST_PIPE = ticks

        # Move ground
        constants.GROUND_SCROLL -= constants.GAME_SPEED

        if abs(constants.GROUND_SCROLL) > 22:
            constants.GROUND_SCROLL = 0
    
    # On game start or over
    if constants.GAME_START or constants.GAME_OVER:
        text = font.render('Score: ' + str(constants.SCORE), True, (215, 168, 76))
        screen.blit(text, (constants.SCREEN_WIDTH / 2 - 50, 450))

    # Game start
    if not constants.GAME_START and not constants.GAME_OVER:
        screen.blit(game_start, (0, 0))


    # Game over
    if constants.GAME_OVER and not constants.GAME_START:
        screen.blit(game_over, (0, 0))
    

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not constants.GAME_START and not constants.GAME_OVER:
                constants.GAME_START = True
        
            if constants.GAME_OVER:
                constants.GAME_OVER = False
                reset()

    pygame.display.update()

pygame.quit()