import random

import pygame

WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900

"""
Основные объекты, появляющиеся в игре
"""


def random_image_loader(path, max_num):
    number = random.randint(1, max_num)
    return pygame.image.load(path + str(number) + '.png')


class MeowHero(pygame.sprite.Sprite):
    # This class represents a Cat Hero. It derives from the "Sprite" class in PyGame.
    def __init__(self, skin_type):
        super().__init__()

        # getting rect
        self.w = int(WINDOW_WIDTH / 15)
        self.h = int(WINDOW_HEIGHT / 8)

        image = pygame.image.load('../drawable/sprites/cat_hero/cat' + str(skin_type) + '.png')

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
    def __init__(self, level, type="Simple"):
        super().__init__()

        self.w = int(WINDOW_WIDTH / 22)
        self.h = int(WINDOW_HEIGHT / 22)

        if type == "Simple":
            image = pygame.image.load('../drawable/weapons/bullets/bullet' + str(level) + '.png')
            self.image_surface = pygame.transform.scale(image, (self.w, self.h))
            self.rect = self.image_surface.get_rect()

            self.level = level
            self.power = 1
            self.speed = 10
            self.life = 1

            self.x = 0
            self.y = self.speed*(-1)

        if type == "Multiplayer":
            # TODO: different images here
            image = pygame.image.load('../drawable/weapons/bullets/bullet' + str(level) + '.png')
            self.image_surface = pygame.transform.scale(image, (self.w, self.h))
            self.rect = self.image_surface.get_rect()

            self.level = level
            self.power = self.level
            self.speed = 14 + self.power * 2
            self.life = 1

        # move direction
        self.x = 0
        self.y = self.speed * (-1)

    def move(self):
        self.rect.move_ip(self.x, self.y)

    def draw(self, window):
        window.blit(self.image_surface, self.rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, name, level):
        super().__init__()

        self.w = int(WINDOW_WIDTH / 18)  # by default
        self.h = int(WINDOW_HEIGHT / 18)  # by default

        self.name = name
        self.level = level

        self.life = level
        self.speed = 1
        self.reload = 0
        self.reload_time = 14 - level

        image = pygame.image.load('../drawable/sprites/enemy/enemy_3.png')  # by default

        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

    def move(self):
        self.rect.move_ip(0, self.speed)

    def draw(self, window):
        window.blit(self.image_surface, self.rect)

    def attack(self, *args):
        if self.reload == self.reload_time:
            bullet = EnemyBullet(self.level)
            bullet.rect.center = self.rect.center
            self.reload = 0
            return bullet
        else:
            self.reload += 1


class CommonEnemy(Enemy):
    def __init__(self, name, level):
        super().__init__(name, level)


class Children(CommonEnemy):
    def __init__(self, name, level):
        super().__init__(name, level)

        self.w = int(WINDOW_WIDTH / 12)
        self.h = int(WINDOW_HEIGHT / 8)

        self.speed = random.randint(2, 7)
        self.direction = random.randint(-4, 4)

        self.life = 4

        image = random_image_loader('../drawable/sprites/enemy/children/children', 6)

        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        self.rect.move_ip(random.randint(50, WINDOW_WIDTH-50), 0)

    def attack(self, *args):
        pass

    def move(self):
        self.rect.move_ip(self.direction, self.speed)


class Dog(CommonEnemy):
    def __init__(self, name, level):
        super().__init__(name, level)

        self.w = int(WINDOW_WIDTH / 12)
        self.h = int(WINDOW_HEIGHT / 12)

        self.speed = random.randint(1, 4)
        self.direction = random.randint(-2, 2)

        self.life = random.randint(4, 7)

        image = random_image_loader('../drawable/sprites/enemy/dog_enemy/dog_enemy', 12)

        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        self.rect.move_ip(random.randint(50, WINDOW_WIDTH-50), 0)

    def attack(self, *args):
        pass

    # TODO: change it pls
    def move(self):
        self.rect.move_ip(self.direction, self.speed)


class DancingCat(CommonEnemy):
    def __init__(self, name, level):
        super().__init__(name, level)

        self.w = int(WINDOW_WIDTH / 12)
        self.h = int(WINDOW_HEIGHT / 12)

        self.speed = random.randint(1, 4)
        self.direction = random.randint(-2, 2)

        self.life = random.randint(4, 7)

        image = random_image_loader('../drawable/sprites/enemy/dancing_cats/dancing_cat', 4)

        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        self.rect.move_ip(random.randint(50, WINDOW_WIDTH-50), 0)

    # TODO: add it
    def attack(self, *args):
        pass

    # TODO: change it =)
    def move(self):
        self.rect.move_ip(self.direction, self.speed)


class DogEnemyMultiplayer(Enemy):
    def __init__(self, name, level):
        super().__init__(name, level)

        self.reload_time = 10
        self.reload = random.randint(0, 8)

        image =  pygame.image.load('../drawable/sprites/enemy/dog_enemy/dog_enemy' + str(level) + '.png')

        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

    def attack(self, *args):
        if self.reload == self.reload_time:
            bullet = EnemyBullet(self.level+12)
            bullet.rect.center = self.rect.center
            self.reload = 0
            return bullet
        else:
            self.reload += 1


class Boss(Enemy):
    def __init__(self, name, level):
        super().__init__(name, level)

        # bosses are bigger
        self.w = int(WINDOW_WIDTH / 5)
        self.h = int(WINDOW_HEIGHT / 6)

        # and stronger
        self.life *= 100


class ZloyMuzhic(Boss):
    def __init__(self, name, level):
        super().__init__(name, level)

        image = pygame.image.load('../drawable/sprites/enemy/bosses/zloy_muzhic.png')

        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

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
            bullet = EnemyBullet(1, "Boss InHero", pos, self.rect.center)
            bullet.rect.center = self.rect.center
            self.reload = 0
            return bullet
        else:
            self.reload += 1


class EGE(Boss):
    def __init__(self, name, level):
        super().__init__(name, level)

        self.w = int(WINDOW_WIDTH / 3)
        self.h = int(WINDOW_HEIGHT / 5)

        image = pygame.image.load('../drawable/sprites/enemy/bosses/ege.png')

        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

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

    # TODO: change this
    def attack(self, pos):
        if self.reload == self.reload_time:
            bullet = EnemyBullet(4, "Boss InHero", pos, self.rect.center)
            bullet.rect.center = self.rect.center
            self.reload = 0
            return bullet
        else:
            self.reload += 1


class Committee(Boss):
    def __init__(self, name, level):
        super().__init__(name, level)

        self.w = int(WINDOW_WIDTH / 3)
        self.h = int(WINDOW_HEIGHT / 5)

        image = pygame.image.load('../drawable/sprites/enemy/bosses/komissia3.png')

        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        self.move_right = True
        self.move_left = False
        self.speed = 1
        self.move_time = 150

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

    # TODO: change this
    def attack(self, pos):
        if self.reload == self.reload_time:
            bullet = EnemyBullet(self.level, "Boss InHero", pos, self.rect.center)
            bullet.rect.center = self.rect.center
            self.reload = 0
            return bullet
        else:
            self.reload += 1


class DiplomCommittee(Committee):
    def __init__(self, name, level):
        super().__init__(name, level)

        image = pygame.image.load('../drawable/sprites/enemy/bosses/komissia2.png')

        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()


class DedMoroz(Boss):
    def __init__(self, name, level):
        super().__init__(name, level)

        self.w = int(WINDOW_WIDTH / 5)
        self.h = int(WINDOW_HEIGHT / 5)

        self.life = 299

        image = pygame.image.load('../drawable/sprites/enemy/bosses/ded_moroz/ded_moroz3.png')

        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        self.move_right = True
        self.move_left = False
        self.speed = 1
        self.move_time = 150

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

    # TODO: change this
    def attack(self, pos):
        if self.reload == self.reload_time:
            bullet = EnemyBullet(self.level, "Boss InHero", pos, self.rect.center)
            bullet.rect.center = self.rect.center
            self.reload = 0
            return bullet
        else:
            self.reload += 1

    def draw(self, window):
        # draw damaged boss
        num = int(self.life / 100) + 1

        image = pygame.image.load('../drawable/sprites/enemy/bosses/ded_moroz/ded_moroz' + str(num) + '.png')
        self.image_surface = pygame.transform.scale(image, (self.w, self.h))

        window.blit(self.image_surface, self.rect)


class Ejudje(Boss):
    def __init__(self, name, level):
        super().__init__(name, level)

        image = pygame.image.load('../drawable/sprites/enemy/bosses/ejudje/ejudje1.png')

        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        self.life = 639

        self.move_right = True
        self.move_left = False
        self.speed = 1
        self.move_time = 150

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

        # TODO: change this
    def attack(self, pos):
        if self.reload == self.reload_time:
            bullet = EnemyBullet(self.level, "Boss InHero", pos, self.rect.center)
            bullet.rect.center = self.rect.center
            self.reload = 0
            return bullet
        else:
            self.reload += 1

    def draw(self, window):
        # draw damaged boss
        num = int(self.life / 80) + 1

        image = pygame.image.load('../drawable/sprites/enemy/bosses/ejudje/ejudje' + str(num) + '.png')
        self.image_surface = pygame.transform.scale(image, (self.w, self.h))

        window.blit(self.image_surface, self.rect)


class Teacher(Boss):
    def __init__(self, name, level):
        super().__init__(name, level)

        self.w = int(WINDOW_WIDTH / 10)
        self.h = int(WINDOW_HEIGHT / 10)

        image = pygame.image.load('../drawable/sprites/enemy/bosses/teachers/teachers' + name + '.png')

        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        self.move_right = True
        self.move_left = False
        self.speed = 1
        self.move_time = 150

        self.reload_time = 1

    # TODO: you know what to do
    def attack(self, *args):
        pass


class OlegAlexeevich(Boss):
    def __init__(self, name, level):
        super().__init__(name, level)

        self.w = int(WINDOW_WIDTH / 5)
        self.h = int(WINDOW_HEIGHT / 5)

        image = pygame.image.load('../drawable/sprites/enemy/bosses/teachers/teachers5.png')

        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        self.move_right = True
        self.move_left = False
        self.speed = 1
        self.move_time = 150

        self.reload_time = 1

    # TODO: change this
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

    # TODO: and this
    def attack(self, pos):
        if self.reload == self.reload_time:
            bullet = EnemyBullet(self.level, "Boss", pos, self.rect.center)
            bullet.rect.center = self.rect.center
            self.reload = 0
            return bullet
        else:
            self.reload += 1


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, level, bullet_type="Simple", *args):
        super().__init__()

        self.bullet_type = bullet_type.split()
        self.level = level

        if "Boss" in self.bullet_type:
            self.w = 100
            self.h = 100
            self.speed = 8
            self.life = 10
        else:
            self.w = 24
            self.h = 24
            self.speed = 5
            self.life = 1

        if level == 5:
            image = random_image_loader('../drawable/weapons/faculty/faculty', 18)
        elif level == 7:
            image = random_image_loader('../drawable/weapons/languages/language', 18)
        elif level == 10:
            image = random_image_loader('../drawable/weapons/questions/question', 15)
        elif level == 12:
            image = random_image_loader('../drawable/weapons/projects/project', 30)
        else:
            image = pygame.image.load('../drawable/weapons/enemy_bullets/enemy_bullet' + str(level) + '.png')

        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        if "InHero" in self.bullet_type:  # calculate direction
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
    def __init__(self, bonus_type):
        super().__init__()

        self.w = int(WINDOW_WIDTH / 24)
        self.h = int(WINDOW_HEIGHT / 24)
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
        elif self.bonus_type == "x2":
            image = pygame.image.load('../drawable/other/x2.png')

        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        self.lifetime = 22

    def draw(self, window):
        window.blit(self.image_surface, self.rect)
