import pygame
import constants

class Pipe(pygame.sprite.Sprite):
    def __init__(self, y, flip):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/sprites/pipe.png')
        self.rect = self.image.get_rect()
        self._position(y, flip)

    def _position(self, y, flip):
        if flip:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = (576, y - (constants.PIPE_GAP / 2))
        else:
            self.rect.topleft = (576, y + (constants.PIPE_GAP / 2))

    def update(self):
        self.rect.x -= constants.SPEED

        if self.rect.right < 0:
            self.kill()

    def _move(self):
        self.rect.x -= constants.SPEED
        
        if self.rect.right < 0:
            self.kill()