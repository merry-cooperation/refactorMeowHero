import random

import pygame

WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900

"""
Основные объекты, появляющиеся в игре
"""


def random_image_path(path, max_num):
    number = random.randint(1, max_num)
    return path + str(number) + '.png'


def random_image_loader(path, max_num):
    return pygame.image.load(random_image_path(path, max_num))


class MeowHero(pygame.sprite.Sprite):
    # This class represents a Cat Hero. It derives from the "Sprite" class in PyGame.
    def __init__(self, skin_type):
        super().__init__()

        # getting rect
        self.w = int(WINDOW_WIDTH / 15)
        self.h = int(WINDOW_HEIGHT / 8)

        image = pygame.image.load('../drawable/sprites/cat_hero/skins/cat' + str(skin_type) + '.png')

        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        # getting attributes
        self.life = 9
        self.weapon_power = 1
        self.move_rate = 8

        self.invulnerability = 8
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
        self.rect.move_ip(x_d * self.move_rate, y_d * self.move_rate)

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
            window.blit(self.image_surface, [0 + i * self.w, 80])


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
            self.y = self.speed * (-1)

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

        self.w = int(WINDOW_WIDTH / 14)  # by default
        self.h = int(WINDOW_HEIGHT / 14)  # by default

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

        self.rect.move_ip(random.randint(50, WINDOW_WIDTH - 50), 0)

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

        self.life = random.randint(5, 10)

        image = random_image_loader('../drawable/sprites/enemy/dog_enemy/dog_enemy', 12)

        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        self.rect.move_ip(random.randint(50, WINDOW_WIDTH - 50), 0)

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

        self.speed = random.randint(1, 3)
        self.direction = random.randint(-3, 3)

        self.change_direction_time = random.randint(10, 70)

        self.reload_time = 1000
        self.reload = self.reload_time

        self.life = random.randint(4, 7)

        image = random_image_loader('../drawable/sprites/enemy/dancing_cats/dancing_cat', 4)

        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        self.rect.move_ip(random.randint(50, WINDOW_WIDTH - 50), 0)

    def attack(self, pos):
        if self.reload == self.reload_time:
            bullet = EnemyBullet(self.level, "InHero", pos, self.rect.center)
            bullet.rect.center = self.rect.center
            bullet.speed = 1
            self.reload = 0
            return bullet
        else:
            self.reload += 1

    def move(self):
        self.change_direction_time -= 1
        if self.change_direction_time == 0:
            self.direction = -self.direction

        self.rect.move_ip(self.direction, self.speed)


class CatBossEnemy(CommonEnemy):
    def __init__(self, name, level):
        super().__init__(name, level)

        self.w = int(WINDOW_WIDTH / 10)
        self.h = int(WINDOW_HEIGHT / 6)

        image = random_image_loader('../drawable/sprites/enemy/cat_boss/cat_boss', 8)

        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        self.rect.move_ip(random.randint(50, WINDOW_WIDTH - 50), 0)

        self.reload_time = 35
        self.reload = random.randint(0, 26)

        self.life = 24

    def move(self):
        self.rect.move_ip(random.randint(-5, 5), random.randint(-1, 3))

    def attack(self, pos):
        if self.reload == self.reload_time:
            bullet = EnemyBullet(self.level, "InHero RandomSpeed Boss", pos, self.rect.center)
            bullet.rect.center = self.rect.center
            bullet.speed = 1
            self.reload = 0
            return bullet
        else:
            self.reload += 1


class DogEnemyMultiplayer(Enemy):
    def __init__(self, name, level):
        super().__init__(name, level)

        self.reload_time = 10
        self.reload = random.randint(0, 8)

        image = pygame.image.load('../drawable/sprites/enemy/dog_enemy/dog_enemy' + str(level) + '.png')

        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

    def attack(self, *args):
        if self.reload == self.reload_time:
            bullet = EnemyBullet(self.level + 12)
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
        self.life *= 25

        # movement
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


class ZloyMuzhic(Boss):
    def __init__(self, name, level):
        super().__init__(name, level)

        image = pygame.image.load('../drawable/sprites/enemy/bosses/zloy_muzhic.png')

        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        self.reload_time = 2

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

        self.speed = 3
        self.move_time = 150
        # self.life = 250

        self.reload_time = 2

    # TODO: change this
    def attack(self, pos):
        self.speed = random.randint(2, 7)
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

        # self.life = 322

        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

    # TODO: change this
    def attack(self, pos):
        if self.reload == self.reload_time:
            coin = random.randint(1, 3)
            if coin == 1:
                bullet = EnemyBullet(self.level, "Boss InHero", pos, self.rect.center)
            elif coin == 2:
                bullet = EnemyBullet(self.level, "Boss", pos, self.rect.center)
            elif coin == 3:
                bullet = EnemyBullet(self.level, "Boss InHero RandomSpeed", pos, self.rect.center)
            bullet.rect.center = self.rect.center
            self.reload = 0
            return bullet
        else:
            self.reload += 1


class DedMoroz(Boss):
    def __init__(self, name, level):
        super().__init__(name, level)

        self.w = int(WINDOW_WIDTH / 5)
        self.h = int(WINDOW_HEIGHT / 5)

        self.speed = 2

        self.image = pygame.image.load('../drawable/sprites/enemy/bosses/ded_moroz/ded_moroz4.png')
        self.cur_num = 4

        self.image_surface = pygame.transform.scale(self.image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        self.damage_life = self.life / self.cur_num
        self.life -= 1

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
        num = int(self.life / self.damage_life) + 1

        if num != self.cur_num:
            self.cur_num = num
            self.image = pygame.image.load('../drawable/sprites/enemy/bosses/ded_moroz/ded_moroz' + str(num) + '.png')
            self.image_surface = pygame.transform.scale(self.image, (self.w, self.h))
            self.speed += 2

        window.blit(self.image_surface, self.rect)


class Ejudje(Boss):
    def __init__(self, name, level):
        super().__init__(name, level)

        self.image = pygame.image.load('../drawable/sprites/enemy/bosses/ejudje/ejudje8.png')
        self.cur_num = 8

        self.image_surface = pygame.transform.scale(self.image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        self.reload_time = 3

        self.damage_life = self.life / self.cur_num
        self.life -= 1

    def attack(self, pos):
        if self.reload == self.reload_time:
            bullet = EnemyBullet(self.level, "Boss InHero RandomSpeed", pos, self.rect.center)
            bullet.rect.center = self.rect.center
            bullet.speed += 2
            self.reload = 0
            return bullet
        else:
            self.reload += 1

    def draw(self, window):
        # draw damaged boss
        num = int(self.life / self.damage_life) + 1

        if num != self.cur_num:
            self.cur_num = num
            self.image = pygame.image.load('../drawable/sprites/enemy/bosses/ejudje/ejudje' + str(num) + '.png')
            self.image_surface = pygame.transform.scale(self.image, (self.w, self.h))

        window.blit(self.image_surface, self.rect)


class Teacher(Boss):
    def __init__(self, name, level):
        super().__init__(name, level)

        self.w = int(WINDOW_WIDTH / 14)
        self.h = int(WINDOW_HEIGHT / 8)

        self.life = 40

        try:
            image = pygame.image.load('../drawable/sprites/enemy/bosses/teachers/teachers' + name + '.png')
        except Exception:
            self.w = int(WINDOW_WIDTH / 10)
            self.h = int(WINDOW_HEIGHT / 6)
            image = pygame.image.load('../drawable/sprites/enemy/bosses/komissia2.png')
            self.life = 220

        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        self.speed = 4

        self.move_up = False
        self.move_down = False

        self.reload_time = random.randint(12, 20)
        self.reload = random.randint(0, 9)

    def attack(self, pos):
        if self.reload >= self.reload_time:
            bullet = EnemyBullet(self.level, "Boss InHero", pos, self.rect.center)
            bullet.rect.center = self.rect.center
            self.reload = 0
            return bullet
        else:
            self.reload += 1

    def move(self):
        if self.move_time:
            # check border
            if self.rect.left < 0:
                self.move_left = False
                self.move_right = True
            elif self.rect.right > WINDOW_WIDTH:
                self.move_left = True
                self.move_right = False
            elif self.rect.top < 0:
                self.move_up = False
                self.move_down = True
            elif self.rect.bottom > WINDOW_HEIGHT:
                self.move_up = True
                self.move_down = False
            # move enemy
            if self.move_right:
                self.rect.move_ip(self.speed, 0)
                self.move_time -= 1
            elif self.move_left:
                self.rect.move_ip(-self.speed, 0)
                self.move_time -= 1
            elif self.move_up:
                self.rect.move_ip(0, -self.speed)
                self.move_time -= 1
            elif self.move_down:
                self.rect.move_ip(0, self.speed)
                self.move_time -= 1
        else:
            self.move_left = False
            self.move_right = False
            self.move_up = False
            self.move_down = False

            dice = random.random()
            if dice < 0.05:
                self.move_time = random.randint(20, 120)
                coin = random.randint(1, 4)
                if coin == 1:
                    self.move_right = True
                elif coin == 2:
                    self.move_left = True
                elif coin == 3:
                    self.move_up = True
                elif coin == 4:
                    self.move_down = True


class OlegAlexeevich(Boss):
    def __init__(self, name, level):
        super().__init__(name, level)

        self.w = int(WINDOW_WIDTH / 3)
        self.h = int(WINDOW_HEIGHT / 5)

        image = pygame.image.load('../drawable/sprites/enemy/bosses/teachers/teachers6.png')

        # self.life = 300

        self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        self.speed = 5
        self.move_time = 300

    def attack(self, pos):
        if self.reload >= self.reload_time:
            bullet = EnemyBullet(self.level, "Boss NoResize RandomSpeed", pos, self.rect.center)
            bullet.rect.center = (random.randint(100, WINDOW_WIDTH - 100), 0)
            self.reload = 0
            return bullet
        else:
            self.reload += 1


class DiplomCommittee(Teacher):
    def __init__(self, name, level):
        super().__init__(name, level)
        # self.life = 250

        self.reload_time = 3

    def attack(self, pos):
        if self.reload >= self.reload_time:
            bullet = EnemyBullet(self.level, "InHero RandomSpeed", pos, self.rect.center)
            bullet.rect.center = self.rect.center
            self.reload = 0
            return bullet
        else:
            self.reload += 1

        self.speed = random.randint(3, 7)


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
            self.w = 40
            self.h = 40
            self.speed = 5
            self.life = 1

        if "RandomSpeed" in self.bullet_type:
            self.speed = random.randint(2, 9)

        if level == 5:
            image = random_image_loader('../drawable/weapons/faculty/faculty', 18)
        elif level == 6:
            image = random_image_loader('../drawable/weapons/books/book', 6)
        elif level == 7:
            image = random_image_loader('../drawable/weapons/languages/language', 18)
        elif level == 8:
            image = random_image_loader('../drawable/weapons/coctails/coctail', 11)
        elif level == 10:
            image = random_image_loader('../drawable/weapons/questions/question', 15)
        elif level == 12:
            image = random_image_loader('../drawable/weapons/projects/project', 30)
            image = pygame.transform.scale(image, (int(image.get_width() / 2), int(image.get_height() / 2)))
        else:
            image = pygame.image.load('../drawable/weapons/enemy_bullets/enemy_bullet' + str(level) + '.png')

        if "NoResize" in self.bullet_type:
            self.image_surface = pygame.transform.scale(image,
                                                        (int(image.get_width() / 2), int(image.get_height() / 2)))
        else:
            self.image_surface = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image_surface.get_rect()

        if "InHero" in self.bullet_type:  # calculate direction
            x, y = args[0]
            x0, y0 = args[1]
            x -= x0
            y -= y0
            z = (x ** 2 + y ** 2) ** (1 / 2)
            coef = z / self.speed
            self.x = int(x / coef)
            self.y = int(y / coef)
        else:
            self.x = 0
            self.y = self.speed

    def move(self):
        self.rect.move_ip(self.x, self.y)

    def draw(self, window):
        window.blit(self.image_surface, self.rect)


class Bonus(pygame.sprite.Sprite):
    def __init__(self, bonus_type, level=12):
        super().__init__()

        self.w = int(WINDOW_WIDTH / 24)
        self.h = int(WINDOW_HEIGHT / 24)
        self.bonus_type = bonus_type

        # switching bonus type
        if self.bonus_type == "Life":
            image = pygame.image.load('../drawable/other/health1.png')
        elif self.bonus_type == "Coin":
            image = pygame.image.load('../drawable/other/coin' + str(level) + '.png')
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
