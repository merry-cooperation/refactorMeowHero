import os
import random
import pygame
from .display_config import WINDOW_WIDTH, WINDOW_HEIGHT

"""
Основные объекты, появляющиеся в игре
"""


def random_image_path(path, max_num):
    number = random.randint(1, max_num)
    return path + str(number) + '.png'


def random_image_loader(path, max_num):
    return pygame.image.load(random_image_path(path, max_num))


class GameObject(pygame.sprite.Sprite):
    def __init__(self, w, h, name, img_path):
        self.w = int(w)
        self.h = int(h)
        self.name = name

        image = pygame.image.load(img_path)
        self.image = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self.image.get_rect()

    def draw(self, window):
        window.blit(self.image, self.rect)


class MoveMixin:
    def __init__(self, speed_x, speed_y, **kwargs):
        super().__init__(**kwargs)
        self.speed_x = speed_x
        self.speed_y = speed_y

    def move(self):
        self.rect.move_ip(self.speed_x, self.speed_y)


class DamagebleMixin:
    def __init__(self, life, **kwargs):
        super().__init__(**kwargs)
        self.life = life

    def is_alive(self):
        return self.life > 0

    def take_damage(self, val=1):
        self.life -= val


class MeowHero(DamagebleMixin, MoveMixin, GameObject):
    def __init__(self, skin_type):
        super().__init__(
            life=9,
            speed_x=8, speed_y=8,
            w=int(WINDOW_WIDTH / 15),
            h=int(WINDOW_HEIGHT / 8),
            name='MeowHero',
            img_path='../drawable/sprites/cat_hero/skins/cat' + str(skin_type) + '.png'
        )

        self.weapon_power = 1

        self.invulnerability = 8
        self.three_directions_time = 0

        self.max_weapon_reload = 30
        self.current_reload = 0
        self.rate_of_fire_time_limit = 0

        self.shield = GameObject(self.w, self.h, 'Shield', '../drawable/sprites/cat_hero/meow_shield.png')

    def draw(self, window):
        if self.invulnerability:
            self.shield.draw(window)
        window.blit(self.image, self.rect)

    def move(self, x_d, y_d):
        self.rect.move_ip(x_d * self.speed_x, y_d * self.speed_y)
        self.shield.rect = self.rect.copy()


class Health(GameObject):
    def __init__(self, level, width, height):
        super().__init__(
            width,
            height,
            'Health',
            '../drawable/other/health' + str(level) + '.png'
        )

    def draw(self, window, count):
        for i in range(count):
            window.blit(self.image, [0 + i * self.w, 80])


class Bullet(DamagebleMixin, MoveMixin, GameObject):
    def __init__(self, level, type="Simple"):
        if type == 'Simple':
            self.power = 1
            life = 1
            speed_y = -10
        elif type == 'Multiplayer':
            self.power = level
            life = 1
            speed_y = -(14 + self.power * 2)

        super().__init__(
            life=life,
            speed_x=0, speed_y=speed_y,
            w=int(WINDOW_WIDTH / 22),
            h=int(WINDOW_WIDTH / 22),
            name='Bullet',
            img_path='../drawable/weapons/bullets/bullet' + str(level) + '.png'
        )


class Enemy(DamagebleMixin, MoveMixin, GameObject):
    def __init__(self, name, level,
                 w=WINDOW_WIDTH / 14,
                 h=WINDOW_HEIGHT / 14,
                 img_path='../drawable/sprites/enemy/enemy_3.png',
                 speed_x=0, speed_y=1):

        super().__init__(life=level, speed_x=speed_x, speed_y=speed_y, w=w, h=h, name=name, img_path=img_path)

        self.level = level

        self.reload = 0
        self.reload_time = 14 - level

    def attack(self, *args):
        if self.reload == self.reload_time:
            bullet = EnemyBullet(self.level)
            bullet.rect.center = self.rect.center
            self.reload = 0
            return bullet
        else:
            self.reload += 1


class Children(Enemy):
    def __init__(self, name, level):
        super().__init__(
            name,
            level,
            int(WINDOW_WIDTH / 12),
            int(WINDOW_HEIGHT / 8),
            random_image_path('../drawable/sprites/enemy/children/children', 6),
            random.randint(-4, 4), random.randint(2, 7)
        )

        self.life = 4

        self.rect.move_ip(random.randint(50, WINDOW_WIDTH - 50), 0)

    def attack(self, *args):
        pass


class Dog(Enemy):
    def __init__(self, name, level):
        super().__init__(
            name,
            level,
            int(WINDOW_WIDTH / 12),
            int(WINDOW_HEIGHT / 12),
            random_image_path('../drawable/sprites/enemy/dog_enemy/dog_enemy', 12),
            random.randint(-2, 2), random.randint(1, 4)
        )

        self.life = random.randint(5, 10)

        self.rect.move_ip(random.randint(50, WINDOW_WIDTH - 50), 0)

    def attack(self, *args):
        pass


class DancingCat(Enemy):
    def __init__(self, name, level):
        super().__init__(
            name,
            level,
            int(WINDOW_WIDTH / 12),
            int(WINDOW_HEIGHT / 12),
            random_image_path('../drawable/sprites/enemy/dancing_cats/dancing_cat', 4),
            random.randint(-3, 3), random.randint(1, 3)
        )

        self.change_direction_time = random.randint(10, 70)

        self.reload_time = 1000
        self.reload = self.reload_time

        self.life = random.randint(4, 7)

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
            self.speed_x = -self.speed_x

        super().move()


class CatBossEnemy(Enemy):
    def __init__(self, name, level):
        super().__init__(
            name,
            level,
            int(WINDOW_WIDTH / 10),
            int(WINDOW_HEIGHT / 6),
            random_image_path('../drawable/sprites/enemy/cat_boss/cat_boss', 8),
        )

        self.rect.move_ip(random.randint(50, WINDOW_WIDTH - 50), 0)

        self.reload_time = 35
        self.reload = random.randint(0, 26)

        self.life = 24

    def move(self):
        self.speed_x = random.randint(-5, 5)
        self.speed_y = random.randint(-1, 3)
        super().move()

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
        super().__init__(
            name,
            level,
            img_path='../drawable/sprites/enemy/dog_enemy/dog_enemy' + str(level) + '.png'
        )

        self.reload_time = 10
        self.reload = random.randint(0, 8)

    def attack(self, *args):
        if self.reload == self.reload_time:
            bullet = EnemyBullet(self.level + 12)
            bullet.rect.center = self.rect.center
            self.reload = 0
            return bullet
        else:
            self.reload += 1


class Boss(Enemy):
    def __init__(self, name, level, w=int(WINDOW_WIDTH / 5), h=int(WINDOW_HEIGHT / 6),
                 img_path=None, speed_x=3, speed_y=0):
        super().__init__(name, level, w, h, img_path, speed_x, speed_y)

        # and stronger
        self.life *= 25

        # movement
        self.move_right = True
        self.move_left = False
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
                self.rect.move_ip(self.speed_x, 0)
                self.move_time -= 1
            elif self.move_left:
                self.rect.move_ip(-self.speed_x, 0)
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
        super().__init__(
            name,
            level,
            img_path='../drawable/sprites/enemy/bosses/zloy_muzhic.png'
        )

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
        super().__init__(
            name,
            level,
            int(WINDOW_WIDTH / 3),
            int(WINDOW_HEIGHT / 5),
            '../drawable/sprites/enemy/bosses/ege.png',
            3, 0
        )

        self.move_time = 150
        # self.life = 250

        self.reload_time = 2

    # TODO: change this
    def attack(self, pos):
        self.speed_x = random.randint(2, 7)
        if self.reload == self.reload_time:
            bullet = EnemyBullet(4, "Boss InHero", pos, self.rect.center)
            bullet.rect.center = self.rect.center
            self.reload = 0
            return bullet
        else:
            self.reload += 1


class Committee(Boss):
    def __init__(self, name, level):
        super().__init__(
            name,
            level,
            int(WINDOW_WIDTH / 3),
            int(WINDOW_HEIGHT / 5),
            '../drawable/sprites/enemy/bosses/komissia3.png'
        )

        # self.life = 322

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
        super().__init__(
            name,
            level,
            int(WINDOW_WIDTH / 5),
            int(WINDOW_HEIGHT / 5),
            '../drawable/sprites/enemy/bosses/ded_moroz/ded_moroz4.png',
            2, 0
        )

        self.cur_num = 4

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
            image = pygame.image.load('../drawable/sprites/enemy/bosses/ded_moroz/ded_moroz' + str(num) + '.png')
            self.image = pygame.transform.scale(image, (self.w, self.h))
            self.speed_x += 2

        window.blit(self.image, self.rect)


class Ejudje(Boss):
    def __init__(self, name, level):
        super().__init__(
            name,
            level,
            img_path='../drawable/sprites/enemy/bosses/ejudje/ejudje8.png'
        )

        self.cur_num = 8

        self.reload_time = 3

        self.damage_life = self.life / self.cur_num
        self.life -= 1

    def attack(self, pos):
        if self.reload == self.reload_time:
            bullet = EnemyBullet(self.level, "Boss InHero RandomSpeed", pos, self.rect.center)
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
            image = pygame.image.load('../drawable/sprites/enemy/bosses/ejudje/ejudje' + str(num) + '.png')
            self.image = pygame.transform.scale(image, (self.w, self.h))

        window.blit(self.image, self.rect)


class Teacher(Boss):
    def __init__(self, name, level):
        w, h = int(WINDOW_WIDTH / 14), int(WINDOW_HEIGHT / 8)
        img_path = '../drawable/sprites/enemy/bosses/teachers/teachers' + name + '.png'
        self.life = 40

        if not os.path.exists(img_path):
            w, h = int(WINDOW_WIDTH / 10), int(WINDOW_HEIGHT / 6)
            img_path = '../drawable/sprites/enemy/bosses/komissia2.png'
            self.life = 220

        super().__init__(name, level, w, h, img_path, 4, 4)

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
                self.rect.move_ip(self.speed_x, 0)
                self.move_time -= 1
            elif self.move_left:
                self.rect.move_ip(-self.speed_x, 0)
                self.move_time -= 1
            elif self.move_up:
                self.rect.move_ip(0, -self.speed_y)
                self.move_time -= 1
            elif self.move_down:
                self.rect.move_ip(0, self.speed_y)
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
        super().__init__(
            name,
            level,
            int(WINDOW_WIDTH / 3),
            int(WINDOW_HEIGHT / 5),
            '../drawable/sprites/enemy/bosses/teachers/teachers6.png',
            5, 0
        )

        # self.life = 300

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

        self.speed_x = random.randint(3, 7)


class EnemyBullet(DamagebleMixin, MoveMixin, GameObject):
    def __init__(self, level, bullet_type="Simple", *args):

        bullet_type = bullet_type.split()

        if "Boss" in bullet_type:
            w = 100
            h = 100
            speed = 8
            life = 10
        else:
            w = 40
            h = 40
            speed = 5
            life = 1

        if "RandomSpeed" in bullet_type:
            speed = random.randint(2, 9)

        if level == 5:
            img_path = random_image_path('../drawable/weapons/faculty/faculty', 18)
        elif level == 6:
            img_path = random_image_path('../drawable/weapons/books/book', 6)
        elif level == 7:
            img_path = random_image_path('../drawable/weapons/languages/language', 18)
        elif level == 8:
            img_path = random_image_path('../drawable/weapons/coctails/coctail', 11)
        elif level == 10:
            img_path = random_image_path('../drawable/weapons/questions/question', 15)
        elif level == 12:
            img_path = random_image_path('../drawable/weapons/projects/project', 30)
            w, h = int(image.get_width() / 2), int(image.get_height() / 2)
        else:
            img_path = '../drawable/weapons/enemy_bullets/enemy_bullet' + str(level) + '.png'

        if "NoResize" in bullet_type:
            w, h = int(image.get_width() / 2), int(image.get_height() / 2)

        if "InHero" in bullet_type:  # calculate direction
            x, y = args[0]
            x0, y0 = args[1]
            x -= x0
            y -= y0
            z = (x ** 2 + y ** 2) ** (1 / 2)
            coef = z / speed
            speed_x = int(x / coef)
            speed_y = int(y / coef)
        else:
            speed_x = 0
            speed_y = speed

        super().__init__(life=life, speed_x=speed_x, speed_y=speed_y, w=w, h=h, name='EnemyBullet', img_path=img_path)


class Bonus(DamagebleMixin, GameObject):
    def __init__(self, bonus_type, level=12, lifetime=22):

        # switching bonus type
        if bonus_type == "Life":
            img_path = '../drawable/other/health1.png'
        elif bonus_type == "Coin":
            img_path = '../drawable/other/coin' + str(level) + '.png'
        elif bonus_type == "Weapon":
            img_path = '../drawable/other/weapon_levelup.png'
        elif bonus_type == "Shield":
            img_path = '../drawable/other/shield.png'
        elif bonus_type == "Mass Attack":
            img_path = '../drawable/other/mass_attack.png'
        elif bonus_type == "Rate of fire":
            img_path = '../drawable/other/rate_of_fire.png'
        elif bonus_type == "Three Directions":
            img_path = '../drawable/other/three_directions.png'
        elif bonus_type == "Freeze":
            img_path = '../drawable/other/freeze.png'
        elif bonus_type == "x2":
            img_path = '../drawable/other/x2.png'

        super().__init__(
            life=lifetime,
            w=int(WINDOW_WIDTH / 24),
            h=int(WINDOW_WIDTH / 24),
            name=bonus_type,
            img_path=img_path
        )
