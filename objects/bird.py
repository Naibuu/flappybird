import pygame
import constants
import random

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self._sheet()
        self.frame = 0
        self.delay = 0
        self.velocity = 0
        self.pressed = False

        self.image = self._get_frame(1)
        self.rect = self.image.get_rect()
        self.rect.center = (100, 200)

    def _get_frame(self, frame):
        image = pygame.Surface((34, 24), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), (frame * 34, 0, 34, 24))
        return image
    
    def _gravity(self):
        self.velocity += constants.BIRD_AMPL_VELOCITY

        if self.velocity > constants.BIRD_MAX_VELOCITY:
            self.velocity = constants.BIRD_MAX_VELOCITY

        if self.rect.bottom < 400:
            self.rect.y += int(self.velocity)
 
    def _input(self):
        is_pressed = pygame.mouse.get_pressed()[0] or pygame.key.get_pressed()[pygame.K_SPACE]

        if is_pressed and not self.pressed:
            self.pressed = True
            self.velocity = -8
            pygame.mixer.Sound('assets/sounds/flap.ogg').play()
        elif not is_pressed:
            self.pressed = False

    def _animate(self):
        self.delay += 1

        if self.delay > 3:
            self.delay = 0
            self.frame = (self.frame + 1) % 3

        self.image = self._get_frame(self.frame)


    def _rotate(self):
        self.image = pygame.transform.rotate(self.image, self.velocity * -5)

    def _sheet(self):
        colors = ['yellow', 'blue', 'green', 'red']
        _color = random.randint(0, len(colors) - 1)

        self.sheet = pygame.image.load(f'assets/sprites/bird_{colors[_color]}.png')

    def update(self):
        if constants.GAME_START and not constants.GAME_OVER:
            self._gravity()
            self._input()
            self._animate()
            self._rotate()

    def reset(self):
        self._sheet()
        self.image = self._get_frame(1)
        self.image = pygame.transform.rotate(self.image, 0)
        self.rect.center = (100, 200)

