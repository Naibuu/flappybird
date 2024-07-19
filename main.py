import pygame
import constants
import random

from objects import bird, pipe

# Initialize
pygame.init()
clock = pygame.time.Clock()

# Screen
screen = pygame.display.set_mode(( constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT ))
pygame.display.set_caption("FlapPybird")

# Graphics
font = pygame.font.Font('assets/munro.ttf', 32)
background = pygame.image.load('assets/sprites/background.png')
ground = pygame.image.load("assets/sprites/ground.png")
game_start = pygame.image.load('assets/sprites/game_start.png')
game_over = pygame.image.load('assets/sprites/game_over.png')

# Reset
def reset():
    # Constants
    constants.SCORE = 0
    constants.BIRD_COLLIDED = False
    constants.GAME_OVER = False

    constants.SPEED = 4
    constants.PIPE_FREQUENCY = 1200

    # Objects
    pipe_group.empty()
    bird.reset()

# Difficulty
def adjust_difficulty():
    if constants.SCORE > 0 and constants.SCORE % 10 == 0:
        constants.SPEED *= 1.15
        constants.PIPE_FREQUENCY = max(100, constants.PIPE_FREQUENCY * 0.9)

# Objects
bird = bird.Bird()
bird_group = pygame.sprite.Group(bird)
pipe_group = pygame.sprite.Group()

run = True

while run:
    clock.tick(constants.FRAMERATE)
    screen.blit(background, (0, 0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    # Collision
    if bird.rect.bottom >= 400 or\
        pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or\
            bird.rect.top < 0:
                if not constants.BIRD_COLLIDED:
                            pygame.mixer.Sound('assets/sounds/hit.ogg').play()

                constants.GAME_START = False
                constants.BIRD_COLLIDED = True
                constants.GAME_OVER = True
    
    screen.blit(ground, (constants.GROUND_SCROLL, 400))

    # Increment score
    if len(pipe_group) > 0:
        if bird.rect.left < pipe_group.sprites()[0].rect.left and not constants.PIPE_PASSED:
            constants.PIPE_PASSED = True

        if constants.PIPE_PASSED:
            if bird.rect.left > pipe_group.sprites()[0].rect.right - 24:
                constants.SCORE += 1
                adjust_difficulty()
                pygame.mixer.Sound('assets/sounds/point.ogg').play()
                constants.PIPE_PASSED = False

    # On game start
    if constants.GAME_START and not constants.GAME_OVER:
        ticks = pygame.time.get_ticks()

        # Move pipes
        pipe_group.update()

        if ticks - constants.LAST_PIPE > constants.PIPE_FREQUENCY:
            random_y = random.randint(-100, 80)

            top_pipe = pipe.Pipe(200 + random_y, True)
            bottom_pipe = pipe.Pipe(200 + random_y, False)

            pipe_group.add(top_pipe)                
            pipe_group.add(bottom_pipe)

            constants.LAST_PIPE = ticks

        # Move ground
        constants.GROUND_SCROLL -= constants.SPEED

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

        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
            if not constants.GAME_START and not constants.GAME_OVER:
                constants.GAME_START = True
        
            if constants.GAME_OVER:
                constants.GAME_OVER = False
                reset()

    pygame.display.update()

pygame.quit()