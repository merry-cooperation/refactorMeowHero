import random

import pygame

WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900


def enemy_image_loader(name):
    return pygame.image.load('../drawable/sprites/enemy/' + name.lower().replace(' ', '_') + '.png')


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

        # self.invulnerability = 16
        self.invulnerability = 100000  # debug
        self.three_directions_time = 0

        self.max_weapon_reload = 30
        self.current_reload = 0
        self.rate_of_fire_time_limit = 0

        # shield image
        image = pygame.image.load('../drawable/sprites/cat_hero/meow_shield.png')
        self.image_shield = pygame.transform.scale(image, (self.w, self.h))
        self.shield_rect = self.image_shield.get_rect()

    def draw(self, window):
        if self.invulnerability:
            window.blit(self.image_shield, self.rect)
        window.blit(self.image_surface, self.rect)

    def move(self, x_d, y_d):
        self.rect.move_ip(x_d*self.move_rate, y_d*self.move_rate)

    def attack(self):
        pass


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

        image = pygame.image.load('../drawable/weapons/bullet' + str(level) + '.png')
        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        self.level = level
        self.power = self.level
        self.speed = 14 + self.power*2
        self.life = 1

        self.x = 0
        self.y = self.speed*(-1)

    def move(self):
        self.rect.move_ip(self.x, self.y)

    def draw(self, window):
        window.blit(self.image_surface, self.rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, name, level, width, height):
        super().__init__()

        self.w = int(width)
        self.h = int(height)

        self.name = name
        self.level = level

        self.life = level
        self.speed = 1
        self.reload = 0
        self.reload_time = 14 - level

        image = enemy_image_loader(name)

        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

    def move(self):
        self.rect.move_ip(0, self.speed)

    def draw(self, window):
        window.blit(self.image_surface, self.rect)

    def attack(self, *args):
        if self.reload == self.reload_time:
            bullet = EnemyBullet(self.level, 24, 24)
            bullet.rect.center = self.rect.center
            self.reload = 0
            return bullet
        else:
            self.reload += 1


class Boss(Enemy):
    def __init__(self, name, level, width, height):
        super().__init__(name, level, width, height)

        self.life *= 100


class CommonEnemy(Enemy):
    def __init__(self, name, level, width, height):
        super().__init__(name, level, width, height)


class DogEnemy(Enemy):
    def __init__(self, name, level, width, height):
        super().__init__(name, level, width, height)

        self.reload_time = 10
        self.reload = random.randint(0, 8)

    def attack(self, *args):
        if self.reload == self.reload_time:
            bullet = EnemyBullet(self.level+12, 24, 24)
            bullet.rect.center = self.rect.center
            self.reload = 0
            return bullet
        else:
            self.reload += 1


class ZloyMuzhic(Boss):
    def __init__(self, name, level, width, height):
        super().__init__(name, level, width, height)

        self.move_right = True
        self.move_left = False
        self.speed = 3
        self.move_time = 120

        self.reload_time = 1

    def move(self):
        if self.move_time:
            if self.rect.left < 0:
                self.move_left = False
                self.move_right = True
            if self.rect.right > WINDOW_WIDTH:
                self.move_left = True
                self.move_right = False
            if self.move_right:
                self.rect.move_ip(self.speed, 0)
                self.move_time -= 1
            elif self.move_left:
                self.rect.move_ip(-self.speed, 0)
                self.move_time -= 1
        else:
            self.move_left = False
            self.move_right = False
            dice = random.random()
            if dice < 0.05:
                self.move_time = random.randint(20, 120)
                if random.randint(1, 2) == 2:
                    self.move_right = True
                else:
                    self.move_left = True

    def attack(self, pos):
        if self.reload == self.reload_time:
            bullet = EnemyBullet(1, 100, 100, "In hero", pos, self.rect.center)
            bullet.rect.center = self.rect.center
            self.reload = 0
            return bullet
        else:
            self.reload += 1


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, level, width, height, bullet_type="Simple", *args):
        super().__init__()

        self.w = int(width)
        self.h = int(height)

        image = pygame.image.load('../drawable/weapons/enemy_bullet' + str(level) + '.png')
        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        self.level = level
        self.speed = 5
        self.life = 1

        self.bullet_type = bullet_type

        if self.bullet_type == "In hero":  # calculate direction
            x, y = args[0]
            x0, y0 = args[1]
            x -= x0
            y -= y0
            z = (x**2 + y**2)**(1/2)
            coef = z/self.speed
            self.x = int(x/coef)
            self.y = int(y/coef)
        else:
            self.x = 0
            self.y = self.speed

    def move(self):
        self.rect.move_ip(self.x, self.y)

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
        elif self.bonus_type == "Weapon":
            image = pygame.image.load('../drawable/other/weapon_levelup.png')
        elif self.bonus_type == "Shield":
            image = pygame.image.load('../drawable/other/shield.png')
        elif self.bonus_type == "Mass Attack":
            image = pygame.image.load('../drawable/other/mass_attack.png')
        elif self.bonus_type == "Rate of fire":
            image = pygame.image.load('../drawable/other/rate_of_fire.png')
        elif self.bonus_type == "Three Directions":
            image = pygame.image.load('../drawable/other/three_directions.png')
        elif self.bonus_type == "Freeze":
            image = pygame.image.load('../drawable/other/freeze.png')

        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        self.lifetime = 22

    def draw(self, window):
        window.blit(self.image_surface, self.rect)
