import pygame
import random


# TODO: move_rate by screen params please
class MeowHero(pygame.sprite.Sprite):
    # This class represents a Cat Hero. It derives from the "Sprite" class in PyGame.
    def __init__(self, skin_type, width, height):
        super().__init__()

        # getting rect
        self.w = int(width)
        self.h = int(height)
        image = pygame.image.load('../drawable/sprites/cat_hero/cat_hero' + str(skin_type) + '.png')
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
    def __init__(self, level, width, height):
        super().__init__()

        self.w = int(width)
        self.h = int(height)

        image = pygame.image.load('../drawable/other/health' + str(level) + '.png')
        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

    def draw(self, window, count):
        for i in range(count):
            window.blit(self.image_surface, [0+i*self.w, 80])


class Bullet(pygame.sprite.Sprite):
    def __init__(self, level, width, height):
        super().__init__()

        self.w = int(width)
        self.h = int(height)

        image = pygame.image.load('../drawable/weapons/bullet' + str(level) +'.png')
        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        self.level = level
        self.speed = 20
        self.life = 1

    def move(self):
        self.rect.move_ip(0, self.speed*(-1))  # another direction

    def draw(self, window):
        window.blit(self.image_surface, self.rect)


class DogEnemy(pygame.sprite.Sprite):
    def __init__(self, level, width, height):
        super().__init__()

        self.w = int(width)
        self.h = int(height)

        image = pygame.image.load('../drawable/sprites/enemy/dog_enemy' + str(level) + '.png')
        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        self.level = level
        self.speed = random.randint(2, 14)
        self.life = level

    def move(self):
        self.rect.move_ip(0, self.speed)

    def draw(self, window):
        window.blit(self.image_surface, self.rect)


class Bonus(pygame.sprite.Sprite):
    def __init__(self, bonus_type, width, height):
        super().__init__()

        self.w = int(width)
        self.h = int(height)
        self.bonus_type = bonus_type
        # switching bonus type
        if self.bonus_type == "Life":
            image = pygame.image.load('../drawable/other/health1.png')
        elif self.bonus_type == "Coin":
            image = pygame.image.load('../drawable/other/coin1.png')
        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        # TODO: add lifetime

    def draw(self, window):
        window.blit(self.image_surface, self.rect)
