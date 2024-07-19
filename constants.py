import pygame

# Screen Config
SCREEN_WIDTH = 576
SCREEN_HEIGHT = 512
FRAMERATE = 60

# Game Config
GAME_START = False
GAME_OVER = False
SPEED = 4
SCORE = 0

# Ground Config
GROUND_SCROLL = 0

# Pipe Config
PIPE_FREQUENCY = 1200
PIPE_GAP = 150
PIPE_PASSED = False
LAST_PIPE = pygame.time.get_ticks()

# Bird Config
BIRD_AMPL_VELOCITY = 0.5
BIRD_MAX_VELOCITY = 8
BIRD_COLLIDED = False