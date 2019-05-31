import pygame
import random


class MeowHero(pygame.sprite.Sprite):
    # This class represents a Cat Hero. It derives from the "Sprite" class in PyGame.
    def __init__(self, image, width, height):
        super().__init__()

        # getting rect
        self.w = int(width)
        self.h = int(height)
        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        # getting attributes
        self.life = 9
        self.weapon_power = 1
        self.move_rate = 12

    def draw(self, window):
        window.blit(self.image_surface, self.rect)

    def move(self, x_d, y_d):
        self.rect.move_ip(x_d*self.move_rate, y_d*self.move_rate)


class Health(pygame.sprite.Sprite):
    def __init__(self, image, width, height):
        super().__init__()

        self.w = int(width)
        self.h = int(height)
        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

    def draw(self, window, count):
        for i in range(count):
            window.blit(self.image_surface, [0+i*self.w, 80])


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, width, height):
        super().__init__()

        self.w = int(width)
        self.h = int(height)
        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        self.speed = 20
        self.life = 1

    def move(self):
        self.rect.move_ip(0, self.speed*(-1))  # another direction

    def draw(self, window):
        window.blit(self.image_surface, self.rect)


class DogEnemy(pygame.sprite.Sprite):
    def __init__(self, image, width, height):
        super().__init__()

        self.w = int(width)
        self.h = int(height)
        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        self.speed = random.randint(3, 20)
        self.life = 1

    def move(self):
        self.rect.move_ip(0, self.speed)

    def draw(self, window):
        window.blit(self.image_surface, self.rect)
