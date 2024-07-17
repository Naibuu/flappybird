import pygame

# Screen Config
SCREEN_WIDTH = 576
SCREEN_HEIGHT = 512
FRAMERATE = 60

# Game Config
GAME_START = False
GAME_OVER = False
GAME_SPEED = 6
SCORE = 0

# Ground Config
GROUND_SCROLL = 0

# Pipe Config
PIPE_FREQUENCY = 1200
PIPE_GAP = 150
LAST_PIPE = pygame.time.get_ticks()

# Bird Config
BIRD_COLLIDED = False