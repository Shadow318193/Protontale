import pygame
import sys
import os
import random


def load_image(name, colorkey=None):
    fullname = os.path.join('data', 'sprites', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    return image


class Wall:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = (800 - self.width) // 2
        self.y = (600 - self.height) // 1.5

    def draw(self, screen):
        self.x = (800 - self.width) // 2
        self.y = (600 - self.height) // 1.5
        screen.fill(pygame.Color("white"), (self.x, self.y, self.width, self.height))
        screen.fill(pygame.Color("black"), (self.x + 5, self.y + 5, self.width - 10, self.height - 10))


class Creature:

    def __init__(self, hp, attack, defense):
        self.max_hp = hp
        self.hp = self.max_hp
        self.attack = attack
        self.defense = defense


class Player(Creature, pygame.sprite.Sprite):
    image = load_image("soul.bmp", (255, 255, 255))

    def __init__(self, *group, wall: Wall):
        Creature.__init__(self, 20, 0, 0)
        pygame.sprite.Sprite.__init__(self, *group)
        self.can_move = True

        self.can_change_size = True
        self.size = (16, 16)
        self.image = pygame.transform.scale(Player.image, self.size)

        self.rect = self.image.get_rect()
        self.rect.x = 392
        self.rect.y = 392

        self.wall = wall

    def move(self, key):
        if self.can_move:
            if key[pygame.K_UP]:
                if not self.rect.y - 10 <= self.wall.y:
                    self.rect.y -= 2
            if key[pygame.K_DOWN]:
                if not self.rect.y + 10 + self.size[1] >= self.wall.y + self.wall.height:
                    self.rect.y += 2
            if key[pygame.K_LEFT]:
                if not self.rect.x - 10 <= self.wall.x:
                    self.rect.x -= 2
            if key[pygame.K_RIGHT]:
                if not self.rect.x + 10 + self.size[0] >= self.wall.x + self.wall.width:
                    self.rect.x += 2

    def set_size(self, size: tuple):
        if self.can_change_size:
            x = self.rect.x
            y = self.rect.y

            self.size = size
            self.image = pygame.transform.scale(Player.image, self.size)

            self.can_move = False

            self.rect = self.image.get_rect()
            self.rect.x = x - self.size[0] // 4
            self.rect.y = y - self.size[1] // 4

            self.can_move = True
            self.can_change_size = False


class Bullet:

    def __init__(self, player, size: (int, int), x: int, y: int, damage: int, direction: list, speed: int):
        self.player = player

        self.damage = damage
        self.can_damage = True

        self.size = size

        self.x = x
        self.y = y

        self.direction = direction
        self.speed = speed

    def update(self):
        if -100 <= self.x <= 900 and - 100 <= self.y <= 700:
            self.x += self.direction[0]
            self.y += self.direction[1]
        else:
            del self

        if self.player.rect.x - self.size[0] <= self.x <= self.player.rect.x + self.player.size[0] and \
                self.player.rect.y - self.size[1] <= self.y <= self.player.rect.y + self.player.size[1] and \
                self.can_damage:
            self.player.hp -= self.damage
            self.can_damage = False

    def draw(self, screen):
        pygame.draw.ellipse(screen, pygame.Color("white"), (self.x, self.y, self.size[0], self.size[1]))


class NumberBullet(Bullet, pygame.sprite.Sprite):

    def __init__(self, *group, player, size: (int, int), x: int, y: int, damage: int, direction: list, speed: int):
        Bullet.__init__(self, player, size, x, y, damage, direction, speed)
        pygame.sprite.Sprite.__init__(self, *group)

        self.size = (16, 16)
        self.image = load_image(f"n_{random.randint(0, 1)}.bmp", (0, 0, 0))

    def draw(self, screen):
        pass
