import pygame


class MeowHero(pygame.sprite.Sprite):
    # This class represents a Cat Hero. It derives from the "Sprite" class in PyGame.
    def __init__(self, image, width, height):
        super().__init__()

        # getting rect
        self.w = int(width)
        self.h = int(height)
        self.x = 0
        self.y = 0
        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        # getting attributes
        self.life = 9
        self.weapon_power = 1

    def draw(self, window):
        window.blit(self.image_surface, [self.x, self.y])

    def spawn(self, x, y):
        pass


class Health(pygame.sprite.Sprite):
    def __init__(self, image, width, height):
        super().__init__()

        self.w = int(width)
        self.h = int(height)
        self.x = 0
        self.y = 0
        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

    def draw(self, window, count):
        pass


class DogEnemy(pygame.sprite.Sprite):
    pass
