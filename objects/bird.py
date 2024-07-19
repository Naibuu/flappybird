import pygame
import constants

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.sheet = pygame.image.load('assets/sprites/bird.png')
        self.frame = 0
        self.delay = 0
        self.velocity = 0
        self.angle = 0
        self.pressed = False

        self.image = pygame.Surface((34, 24), pygame.SRCALPHA)
        self.image.blit(self.sheet, (0, 0), (34, 0, 34, 24))
        
        self.rect = self.image.get_rect()
        self.rect.center = (100, 200)

    def update(self):
        if constants.GAME_START and not constants.GAME_OVER:
            # Gravity
            self.velocity += constants.BIRD_AMPL_VELOCITY

            if self.velocity > constants.BIRD_MAX_VELOCITY:
                self.velocity = constants.BIRD_MAX_VELOCITY

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

            if self.velocity < 0:
                self.angle = max(self.angle + 5, 5)
            else:
                self.angle = min(self.angle - 5, 5)

            self.image = pygame.Surface((34, 24), pygame.SRCALPHA)
            self.image.blit(self.sheet, (0, 0), (self.frame * 34, 0, 34, 24))
            self.image = pygame.transform.rotate(self.image, self.velocity * -2)

    def reset(self):
        self.image = pygame.Surface((34, 24), pygame.SRCALPHA)
        self.image.blit(self.sheet, (0, 0), (1 * 34, 0, 34, 24))
        self.image = pygame.transform.rotate(self.image, 0)

        self.rect.center = (100, 200)

