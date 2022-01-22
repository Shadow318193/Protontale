import pygame
import random
from buttons import ButtonFight, ButtonAct, ButtonItem, ButtonMercy

from game_core import load_image


channel = pygame.mixer.Channel(0)
channel.set_volume(0.2)


class Item:

    def __init__(self, name, hp_to_restore):
        self.name = name
        self.hp = hp_to_restore


class Wall:

    def __init__(self, size: (int, int)):
        self.width = size[0]
        self.height = size[1]

        self.x = (800 - self.width) // 2
        self.y = (600 - self.height) // 1.5

        self.font = pygame.font.Font("data/fonts/determination.otf", 32)

        self.mode = -1
        self.pre_text = ("Протошка появляется!", "")

        self.turn = 0

        self.power = pygame.sprite.Sprite()
        image = load_image("power.png", (255, 0, 255))
        image = pygame.transform.scale(image, (self.width - 10,
                                               self.height - 10))
        self.power.image = image
        self.power.rect = self.power.image.get_rect()
        self.power.rect.x = self.x + 5
        self.power.rect.y = self.y + 5

        self.line_x = 0
        self.line_move = True
        self.line_invert = False
        self.line_t = 1

    def draw(self, screen, group, items):
        group.remove(self.power)
        if self.mode == -2:
            self.x = (800 - self.width) // 2
            self.y = (600 - self.height) // 1.5
            screen.fill(pygame.Color("white"), (self.x, self.y, self.width, self.height))
            screen.fill(pygame.Color("black"), (self.x + 5, self.y + 5, self.width - 10, self.height - 10))
            self.line_t = 1
        elif self.mode == -1:
            self.x = (800 - self.width) // 2
            self.y = (600 - self.height) // 1.5
            screen.fill(pygame.Color("white"), (self.x, self.y, self.width, self.height))
            screen.fill(pygame.Color("black"), (self.x + 5, self.y + 5, self.width - 10, self.height - 10))
            text = self.font.render("* " + self.pre_text[0], True, (255, 255, 255))
            text2 = self.font.render(self.pre_text[1], True, (255, 255, 255))
            screen.blit(text, (self.x + 20, self.y + 20))
            screen.blit(text2, (self.x + 20, self.y + 60))
        elif self.mode == 0:
            self.x = (800 - self.width) // 2
            self.y = (600 - self.height) // 1.5
            screen.fill(pygame.Color("white"), (self.x, self.y, self.width, self.height))
            screen.fill(pygame.Color("black"), (self.x + 5, self.y + 5, self.width - 10, self.height - 10))
            group.add(self.power)
            if self.line_x <= self.width - 15:
                if self.line_move:
                    screen.fill(pygame.Color("black"), (self.x + self.line_x + 5, self.y + 5, 5, self.height - 10))
                    screen.fill(pygame.Color("white"), (self.x + self.line_x + 6, self.y + 5, 3, self.height - 8))
                    self.line_x += 4
                else:
                    if not self.line_t % 3:
                        if self.line_invert:
                            self.line_invert = False
                        else:
                            self.line_invert = True
                        self.line_t = 0
                    self.line_t += 1
                    if self.line_invert:
                        screen.fill(pygame.Color("white"), (self.x + self.line_x + 5, self.y + 5, 5, self.height - 10))
                        screen.fill(pygame.Color("black"), (self.x + self.line_x + 6, self.y + 5, 3, self.height - 10))
                    else:
                        screen.fill(pygame.Color("black"), (self.x + self.line_x + 5, self.y + 5, 5, self.height - 10))
                        screen.fill(pygame.Color("white"), (self.x + self.line_x + 6, self.y + 5, 3, self.height - 10))
        elif self.mode == 1:
            self.x = (800 - self.width) // 2
            self.y = (600 - self.height) // 1.5
            screen.fill(pygame.Color("white"), (self.x, self.y, self.width, self.height))
            screen.fill(pygame.Color("black"), (self.x + 5, self.y + 5, self.width - 10, self.height - 10))
            text = self.font.render("Оценить", True, (255, 255, 255))
            screen.blit(text, (self.x + 60, self.y + 20))
            text = self.font.render("Говорить", True, (255, 255, 255))
            screen.blit(text, (self.x + 360, self.y + 20))
        elif self.mode == 2:
            self.x = (800 - self.width) // 2
            self.y = (600 - self.height) // 1.5
            screen.fill(pygame.Color("white"), (self.x, self.y, self.width, self.height))
            screen.fill(pygame.Color("black"), (self.x + 5, self.y + 5, self.width - 10, self.height - 10))
            n = 0
            for y in range(0, 2):
                for x in range(0, 2):
                    if len(items) - 1 >= n:
                        text = self.font.render(items[n].name, True, (255, 255, 255))
                        screen.blit(text, (self.x + 60 + 300 * x, self.y + 20 + 100 * y))
                    n += 1
        elif self.mode == 3:
            self.x = (800 - self.width) // 2
            self.y = (600 - self.height) // 1.5
            screen.fill(pygame.Color("white"), (self.x, self.y, self.width, self.height))
            screen.fill(pygame.Color("black"), (self.x + 5, self.y + 5, self.width - 10, self.height - 10))

    def set_size(self, size: (int, int)):
        self.width = size[0]
        self.height = size[1]

        self.x = (800 - self.width) // 2
        self.y = (600 - self.height) // 1.5

    def update_text(self):
        if 1 <= self.turn <= 4:
            self.pre_text = random.choice([
                ("Электромагнитные волны повсюду.", ""),
                ("Протоны щекочат кожу.", ""),
                ("Электричество...", ""),
                ("Ваши волосы встали дыбом.", ""),
                ("Протошка ведёт себя странно.", "")
            ])


class Creature:

    def __init__(self, hp):
        self.max_hp = hp
        self.hp = self.max_hp

    def get_damage(self, damage):
        self.hp -= damage


class Player(Creature, pygame.sprite.Sprite):
    image = load_image("soul.bmp", (255, 255, 255))

    def __init__(self, *group, wall: Wall, buttons: [ButtonFight,
                                                     ButtonAct,
                                                     ButtonItem,
                                                     ButtonMercy]):
        Creature.__init__(self, 20)
        pygame.sprite.Sprite.__init__(self, *group)
        self.can_move = True

        self.my_turn = True
        self.btn = 0
        self.act = 0

        self.in_menu = -1

        self.can_change_size = True
        self.size = (16, 16)
        self.image = pygame.transform.scale(Player.image, self.size)

        self.rect = self.image.get_rect()
        self.rect.x = 33
        self.rect.y = 550

        self.died = False

        self.wall = wall
        self.buttons = buttons

        self.t = 120
        self.attacking = False

        self.items = [
            Item("Кусок пиццы", 20),
            Item("Чипсы", 10),
            Item("Газировка", 10),
            Item("Сухарики", 5)
        ]

        if not self.my_turn:
            buttons[0].change_sprite()

    def move(self, key):
        if self.can_move:
            self.t -= 1
            if self.t <= 0:
                self.change_turn()
            if self.my_turn:
                if self.in_menu == 0:
                    if key[pygame.K_z] and not self.attacking:
                        self.wall.line_move = False
                        self.attacking = True
                    if self.wall.line_x >= self.wall.width - 15:
                        self.wall.x = 0
                        self.change_turn()
                elif self.in_menu == 1:
                    if key[pygame.K_LEFT]:
                        if self.act:
                            self.act = 0
                            self.rect.x = self.wall.x + 30
                    if key[pygame.K_RIGHT]:
                        if not self.act:
                            self.act = 1
                            self.rect.x = self.wall.x + 330
                    if key[pygame.K_x]:
                        self.buttons[self.btn].change_sprite()
                        self.in_menu = -1
                        self.wall.mode = -1
                        self.rect.x = 33 + 200 * self.btn
                        self.rect.y = 550
                elif self.in_menu == 2:
                    if key[pygame.K_LEFT]:
                        if self.act > 0:
                            self.act -= 1
                            self.rect.x = self.wall.x + 30 + 300 * (self.act % 2)
                            self.rect.y = self.wall.y + 30 + 100 * (self.act // 2 % 2)
                    if key[pygame.K_RIGHT]:
                        if self.act < 3:
                            self.act += 1
                            self.rect.x = self.wall.x + 30 + 300 * (self.act % 2)
                            self.rect.y = self.wall.y + 30 + 100 * (self.act // 2 % 2)
                    if key[pygame.K_x]:
                        self.buttons[self.btn].change_sprite()
                        self.in_menu = -1
                        self.wall.mode = -1
                        self.rect.x = 33 + 200 * self.btn
                        self.rect.y = 550
                    if key[pygame.K_z]:
                        self.hp += self.items.pop(self.act).hp
                        if self.hp > self.max_hp:
                            self.hp = self.max_hp
                        self.change_turn()
                elif self.in_menu == 3:
                    if key[pygame.K_x]:
                        self.buttons[self.btn].change_sprite()
                        self.in_menu = -1
                        self.wall.mode = -1
                        self.rect.x = 33 + 200 * self.btn
                        self.rect.y = 550
                else:
                    if key[pygame.K_LEFT]:
                        if 0 < self.btn <= 3:
                            self.buttons[self.btn].change_sprite()
                            self.btn -= 1
                            self.buttons[self.btn].change_sprite()
                            self.rect.x = 33 + 200 * self.btn
                    if key[pygame.K_RIGHT]:
                        if 0 <= self.btn < 3:
                            self.buttons[self.btn].change_sprite()
                            self.btn += 1
                            self.buttons[self.btn].change_sprite()
                            self.rect.x = 33 + 200 * self.btn
                    if key[pygame.K_z]:
                        self.buttons[self.btn].change_sprite()
                        self.in_menu = self.btn
                        self.wall.mode = self.btn
                        self.act = 0
                        if self.in_menu == 0:
                            self.rect.x = -100
                            self.rect.y = -100
                        elif self.in_menu == 1:
                            self.rect.x = self.wall.x + 30
                            self.rect.y = self.wall.y + 30
                        elif self.in_menu == 2:
                            self.rect.x = self.wall.x + 30
                            self.rect.y = self.wall.y + 30
            else:
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

    def change_turn(self):
        if self.my_turn:
            self.rect.x = 400 - self.size[0] // 2
            self.rect.y = 400 - self.size[1] // 2

            self.in_menu = -2
            self.my_turn = False

            self.wall.mode = -2

            self.t = 240
        else:
            self.btn = 0
            self.buttons[self.btn].change_sprite()

            self.rect.x = 33
            self.rect.y = 550

            self.in_menu = -1
            self.my_turn = True

            self.wall.mode = -1
            self.wall.turn += 1
            self.wall.update_text()

            self.wall.line_move = True
            self.wall.line_x = 0
            self.wall.line_invert = False

            self.t = 120

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

    def get_damage(self, damage):
        if self.hp > 0:
            channel.play(pygame.mixer.Sound("data/snd/damage.wav"))
        self.hp -= damage

    def die(self):
        pygame.mixer.music.stop()
        self.can_move = False
        self.can_change_size = False

        x = self.rect.x
        y = self.rect.y

        if not self.my_turn:
            self.t = 120
            self.my_turn = True

        if self.t > 80:
            self.rect.x += random.randint(-2, 2)
            self.rect.y += random.randint(-2, 2)
        if self.t == 80:
            self.image = load_image("soul_damaged.bmp", (255, 255, 255))
            self.image = pygame.transform.scale(self.image, self.size)

            channel.play(pygame.mixer.Sound("data/snd/death1.wav"))

            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        if self.t == 1:
            channel.play(pygame.mixer.Sound("data/snd/death2.wav"))
        if self.t > 0:
            self.t -= 1
        else:
            self.died = True

    def attack(self, enemy, enemy_hp_bar):
        self.t -= 1
        if self.t == 110:
            channel.play(pygame.mixer.Sound("data/snd/attack.wav"))
        if 1 <= self.t <= 60:
            enemy_hp_bar.can_draw = True
        if self.t == 60:
            channel.play(pygame.mixer.Sound("data/snd/damage_enemy.wav"))
            enemy.set_emotion("hurt_spr")
            enemy.get_damage(random.randint(20, 30) - abs(self.wall.line_x - self.wall.width // 2) // 15)
            enemy.rect.x -= 20
        if self.t == 50:
            enemy.rect.x += 40
        if self.t == 40:
            enemy.rect.x -= 30
        if self.t == 30:
            enemy.rect.x += 20
        if self.t == 20:
            enemy.rect.x -= 15
        if self.t == 10:
            enemy.rect.x += 10
        if self.t <= 0:
            enemy.rect.x -= 5
            enemy.set_emotion("normal_spr")
            self.attacking = False
            enemy_hp_bar.can_draw = False
            self.change_turn()


class Protoshka(Creature, pygame.sprite.Sprite):
    sprites = {
        "normal_spr": ("protoshka.png", (350, 30, 20 * 5, 44 * 5)),
        "wink_spr": ("protoshka_ok.png", (310, 30, 36 * 5, 44 * 5)),
        "hurt_spr": ("protoshka_hurt.png", (350, 30, 20 * 5, 44 * 5)),
    }

    def __init__(self, *group):
        Creature.__init__(self, 100)
        pygame.sprite.Sprite.__init__(self, *group)
        self.set_emotion("normal_spr")

        self.can_spare = False

    def set_emotion(self, emotion: str):
        self.image = pygame.transform.scale(load_image(Protoshka.sprites[emotion][0], (255, 0, 255)),
                                            (Protoshka.sprites[emotion][1][2],
                                             Protoshka.sprites[emotion][1][3]))
        self.rect = self.image.get_rect()
        self.rect.x = Protoshka.sprites[emotion][1][0]
        self.rect.y = Protoshka.sprites[emotion][1][1]


class Bullet:

    def __init__(self, player, size: (int, int), pos: (int, int), damage: int, direction: list):
        self.player = player

        self.damage = damage
        self.can_damage = True

        self.size = size

        self.x = pos[0]
        self.y = pos[1]

        self.direction = direction

    def update_bullet(self):
        if -100 <= self.x <= 900 and -100 <= self.y <= 700:
            self.x += self.direction[0]
            self.y += self.direction[1]
        else:
            self.can_damage = False

        if self.player.rect.x <= self.x <= self.player.rect.x + self.player.size[0] and \
                self.player.rect.y <= self.y <= self.player.rect.y + self.player.size[1] and \
                self.can_damage:
            self.player.get_damage(self.damage)

            self.can_damage = False

    def draw_bullet(self, screen):
        pygame.draw.ellipse(screen, pygame.Color("white"), (self.x - self.size[0] // 2,
                                                            self.y - self.size[1] // 2,
                                                            self.size[0], self.size[1]))


class NumberBullet(Bullet, pygame.sprite.Sprite):

    def __init__(self, *group, player, size: (int, int), pos: (int, int), damage: int, direction: list):
        pygame.sprite.Sprite.__init__(self, *group)
        Bullet.__init__(self, player, size, pos, damage, direction)

        self.image = load_image(f"n_{random.randint(0, 9)}.bmp", (0, 0, 0))
        self.image = pygame.transform.scale(self.image, self.size)

        self.rect = self.image.get_rect()
        self.rect.x = self.x - self.size[0] // 2
        self.rect.y = self.y - self.size[0] // 2

    def draw_bullet(self, surface):
        if self.can_damage:
            self.rect.x = self.x - self.size[0] // 2
            self.rect.y = self.y - self.size[1] // 2
