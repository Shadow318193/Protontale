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

        self.real_x = (800 - self.width) // 2
        self.x = (800 - self.width) // 2
        self.y = (600 - self.height) // 1.5

        self.font = pygame.font.Font("data/fonts/determination.otf", 32)

        self.mode = -1
        self.pre_text = ("Протошка появляется!", "")

        self.turn = 0
        self.pacifist = True
        self.win = False

        self.power = pygame.sprite.Sprite()
        image = load_image("power.png", (255, 0, 255))
        image = pygame.transform.scale(image, (self.width - 10,
                                               self.height - 10))
        self.power.image = image
        self.power.rect = self.power.image.get_rect()
        self.power.rect.x = self.x + 5
        self.power.rect.y = self.y + 5

        self.miss = pygame.sprite.Sprite()
        image = load_image("miss.png", (255, 0, 255))
        image = pygame.transform.scale(image, (118,
                                               30))
        self.miss.image = image
        self.miss.rect = self.miss.image.get_rect()
        self.miss.rect.x = self.x + self.width // 2 - 118 // 2
        self.miss.rect.y = 20

        self.line = pygame.sprite.Sprite()
        image = load_image("line.bmp", (255, 0, 255))
        image = pygame.transform.scale(image, (9,
                                               self.height - 10))
        self.line.image = image
        self.line.rect = self.line.image.get_rect()
        self.line.rect.x = self.x
        self.line.rect.y = self.y + 5

        self.line_move = True
        self.line_invert = False
        self.line_t = 1

    def draw(self, screen, group, items):
        group.remove(self.power)
        group.remove(self.line)
        group.remove(self.miss)
        if self.mode == -3:
            self.x = (800 - self.width) // 2
            self.y = (600 - self.height) // 1.5
            screen.fill(pygame.Color("white"), (self.x, self.y, self.width, self.height))
            screen.fill(pygame.Color("black"), (self.x + 5, self.y + 5, self.width - 10, self.height - 10))
            text = self.font.render("* ВЫ ПОБЕДИЛИ!", True, (255, 255, 255))
            screen.blit(text, (self.x + 20, self.y + 20))
            text = self.font.render("* Вы получили 0 ОП и 0 М.", True, (255, 255, 255))
            screen.blit(text, (self.x + 20, self.y + 60))
        elif self.mode == -2:
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
            if self.line.rect.x <= self.x + self.width - 15:
                if self.line_move:
                    group.add(self.line)
                    self.line.rect.x += 4
                else:
                    if not self.line_t % 3:
                        if self.line_invert:
                            self.line_invert = False
                        else:
                            self.line_invert = True
                        self.line_t = 0
                    self.line_t += 1
                    if self.line_invert:
                        image = load_image("line_invert.bmp", (255, 0, 255))
                        image = pygame.transform.scale(image, (9,
                                                               self.height - 10))
                        self.line.image = image
                        group.add(self.line)
                    else:
                        image = load_image("line.bmp", (255, 0, 255))
                        image = pygame.transform.scale(image, (9,
                                                               self.height - 10))
                        self.line.image = image
                        group.add(self.line)
            else:
                group.add(self.miss)
        elif self.mode == 1:
            self.x = (800 - self.width) // 2
            self.y = (600 - self.height) // 1.5
            screen.fill(pygame.Color("white"), (self.x, self.y, self.width, self.height))
            screen.fill(pygame.Color("black"), (self.x + 5, self.y + 5, self.width - 10, self.height - 10))
            text = self.font.render("* Оценить", True, (255, 255, 255))
            screen.blit(text, (self.x + 60, self.y + 20))
            text = self.font.render("* Говорить", True, (255, 255, 255))
            screen.blit(text, (self.x + 360, self.y + 20))
            text = self.font.render("Пока что это меню не работает.", True, (255, 255, 255))
            screen.blit(text, (self.x + 25, self.y + self.height - 50))
        elif self.mode == 2:
            self.x = (800 - self.width) // 2
            self.y = (600 - self.height) // 1.5
            screen.fill(pygame.Color("white"), (self.x, self.y, self.width, self.height))
            screen.fill(pygame.Color("black"), (self.x + 5, self.y + 5, self.width - 10, self.height - 10))
            if len(items) > 0:
                n = 0
                for y in range(0, 2):
                    for x in range(0, 2):
                        if len(items) - 1 >= n:
                            text = self.font.render("* " + items[n].name, True, (255, 255, 255))
                            screen.blit(text, (self.x + 60 + 300 * x, self.y + 20 + 100 * y))
                        n += 1
            else:
                text = self.font.render("* Нет вещей.", True, (255, 255, 255))
                screen.blit(text, (self.x + 60, self.y + 20))
        elif self.mode == 3:
            self.x = (800 - self.width) // 2
            self.y = (600 - self.height) // 1.5
            screen.fill(pygame.Color("white"), (self.x, self.y, self.width, self.height))
            screen.fill(pygame.Color("black"), (self.x + 5, self.y + 5, self.width - 10, self.height - 10))
            if self.turn >= 10:
                text = self.font.render("* Пощадить", True, (255, 255, 0))
            else:
                text = self.font.render("* Пощадить", True, (255, 255, 255))
            screen.blit(text, (self.x + 60, self.y + 20))

    def set_size(self, size: (int, int)):
        self.width = size[0]
        self.height = size[1]

        self.x = (800 - self.width) // 2
        self.y = (600 - self.height) // 1.5

    def update_text(self):
        if 1 <= self.turn <= 9 and self.pacifist:
            self.pre_text = random.choice([
                ("Электромагнитные волны повсюду.", ""),
                ("Протоны щекочат кожу.", ""),
                ("Электричество...", ""),
                ("Ваши волосы встали дыбом.", ""),
                ("Протошка ведёт себя странно.", "")
            ])
        elif self.turn >= 10 and self.pacifist:
            self.pre_text = ("Протошка устал и больше не", "хочет сражаться.")
        else:
            self.pre_text = random.choice([
                ("Электромагнитные волны окружили вас.", ""),
                ("Протоны царапают кожу.", ""),
                ("Сильное электричество...", ""),
                ("Ваши волосы начинают рассыпаться.", ""),
                ("Протошка ведёт себя агрессивно.", "")
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

        self.t = 120  # Таймер, который определяет, сколько длится атака, смерть.
        self.attacking = False

        self.items = [
            Item("Кусок пиццы", 20),
            Item("Чипсы", 15),
            Item("Газировка", 15),
            Item("Сухарики", 10)
        ]

        if not self.my_turn:
            buttons[0].change_sprite()

    def move(self, key, enemy):
        if key[pygame.K_ESCAPE]:
            pygame.quit()
        if self.can_move:
            self.t -= 1
            if self.t <= 0:
                self.change_turn()
            if self.my_turn:
                if self.in_menu == 0:
                    if key[pygame.K_z] and not self.attacking and \
                            self.wall.line.rect.x < self.wall.x + self.wall.width - 15:
                        self.wall.line_move = False
                        self.attacking = True
                    elif self.wall.line.rect.x >= self.wall.x + self.wall.width - 15:
                        self.change_turn()
                elif self.in_menu == 1:
                    if key[pygame.K_LEFT]:
                        if self.act:
                            channel.play(pygame.mixer.Sound("data/snd/squeak.wav"))
                            self.act = 0
                            self.rect.x = self.wall.x + 30
                    if key[pygame.K_RIGHT]:
                        if not self.act:
                            channel.play(pygame.mixer.Sound("data/snd/squeak.wav"))
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
                            channel.play(pygame.mixer.Sound("data/snd/squeak.wav"))
                            self.act -= 1
                            self.rect.x = self.wall.x + 30 + 300 * (self.act % 2)
                            self.rect.y = self.wall.y + 30 + 100 * (self.act // 2 % 2)
                    if key[pygame.K_RIGHT]:
                        if self.act < len(self.items) - 1:
                            channel.play(pygame.mixer.Sound("data/snd/squeak.wav"))
                            self.act += 1
                            self.rect.x = self.wall.x + 30 + 300 * (self.act % 2)
                            self.rect.y = self.wall.y + 30 + 100 * (self.act // 2 % 2)
                    if key[pygame.K_UP]:
                        if self.act > 1:
                            channel.play(pygame.mixer.Sound("data/snd/squeak.wav"))
                            self.act -= 2
                            self.rect.x = self.wall.x + 30 + 300 * (self.act % 2)
                            self.rect.y = self.wall.y + 30 + 100 * (self.act // 2 % 2)
                    if key[pygame.K_DOWN]:
                        if self.act < len(self.items) - 2:
                            channel.play(pygame.mixer.Sound("data/snd/squeak.wav"))
                            self.act += 2
                            self.rect.x = self.wall.x + 30 + 300 * (self.act % 2)
                            self.rect.y = self.wall.y + 30 + 100 * (self.act // 2 % 2)
                    if key[pygame.K_x]:
                        self.buttons[self.btn].change_sprite()
                        self.in_menu = -1
                        self.wall.mode = -1
                        self.rect.x = 33 + 200 * self.btn
                        self.rect.y = 550
                    if key[pygame.K_z]:
                        channel.play(pygame.mixer.Sound("data/snd/heal.wav"))
                        if len(self.items) > 0:
                            self.hp += self.items.pop(self.act).hp
                            if self.hp > self.max_hp:
                                self.hp = self.max_hp
                            self.change_turn()
                elif self.in_menu == 3:
                    if key[pygame.K_z]:
                        if enemy.can_spare:
                            channel.play(pygame.mixer.Sound("data/snd/spared.wav"))
                            pygame.mixer.music.stop()
                            self.wall.mode = -3
                            self.rect.x = -100
                            enemy.rect.x = -100
                            enemy.spared = True
                            self.can_move = False
                        else:
                            self.change_turn()
                    if key[pygame.K_x]:
                        self.buttons[self.btn].change_sprite()
                        self.in_menu = -1
                        self.wall.mode = -1
                        self.rect.x = 33 + 200 * self.btn
                        self.rect.y = 550
                elif self.in_menu == -1:
                    if key[pygame.K_LEFT]:
                        if 0 < self.btn <= 3:
                            channel.play(pygame.mixer.Sound("data/snd/squeak.wav"))
                            self.buttons[self.btn].change_sprite()
                            self.btn -= 1
                            self.buttons[self.btn].change_sprite()
                            self.rect.x = 33 + 200 * self.btn
                    if key[pygame.K_RIGHT]:
                        if 0 <= self.btn < 3:
                            channel.play(pygame.mixer.Sound("data/snd/squeak.wav"))
                            self.buttons[self.btn].change_sprite()
                            self.btn += 1
                            self.buttons[self.btn].change_sprite()
                            self.rect.x = 33 + 200 * self.btn
                    if key[pygame.K_z]:
                        channel.play(pygame.mixer.Sound("data/snd/select.wav"))
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
                            if len(self.items) > 0:
                                self.rect.x = self.wall.x + 30
                                self.rect.y = self.wall.y + 30
                            else:
                                self.rect.x = -100
                                self.rect.y = -100
                        elif self.in_menu == 3:
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
        if self.wall.win:
            if key[pygame.K_z]:
                pygame.quit()

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

            self.wall.line.rect.x = self.wall.real_x
            self.wall.line_invert = False
            self.wall.line_move = True

            self.t = 120

    def set_size(self, size: tuple):
        if self.can_change_size:
            channel.play(pygame.mixer.Sound("data/snd/bell.wav"))

            x = self.rect.x
            y = self.rect.y

            self.size = size
            self.image = pygame.transform.scale(Player.image, self.size)

            self.can_move = False

            self.rect = self.image.get_rect()
            self.rect.x = x - self.size[0] // 4
            self.rect.y = y - self.size[1] // 4

            self.max_hp = 30
            self.hp = self.max_hp

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
            enemy.get_damage(random.randint(10, 15) + abs(self.wall.x + self.wall.line.rect.x
                                                          - self.wall.width // 2) // 15)
            if enemy.hp > 50:
                enemy.set_emotion("hurt_spr")
            elif 0 < enemy.hp <= 50:
                enemy.set_emotion("hurt_spr")
                if self.wall.pacifist:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load("data/mus/angry.mp3")
            else:
                enemy.set_emotion("dead_spr")
                pygame.mixer.music.stop()
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
            self.attacking = False
            enemy_hp_bar.can_draw = False
            if enemy.hp > 50:
                enemy.set_emotion("normal_spr")
                self.change_turn()
            elif 0 < enemy.hp <= 50:
                enemy.set_emotion("angry_spr")
                self.set_size((32, 32))

                self.change_turn()
            else:
                channel.play(pygame.mixer.Sound("data/snd/spared.wav"))
                self.rect.x = -100
                self.rect.y = -100
                enemy.rect.x = -100
                self.wall.mode = -3
                self.wall.win = True
                self.can_move = False


class Protoshka(Creature, pygame.sprite.Sprite):
    sprites = {
        "normal_spr": ("protoshka.png", (350, 30, 20 * 5, 44 * 5)),
        "wink_spr": ("protoshka_ok.png", (310, 30, 36 * 5, 44 * 5)),
        "hurt_spr": ("protoshka_hurt.png", (350, 30, 20 * 5, 44 * 5)),
        "dead_spr": ("protoshka_dead.png", (350, 30, 20 * 5, 44 * 5)),
        "angry_spr": ("protoshka_angry.png", (350, 30, 20 * 5, 44 * 5))
    }

    def __init__(self, *group):
        Creature.__init__(self, 100)
        pygame.sprite.Sprite.__init__(self, *group)
        self.set_emotion("normal_spr")

        self.can_spare = False
        self.spared = False

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

    def __init__(self, *group, player: Player, size: (int, int), pos: (int, int), damage: int, direction: list):
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


# TODO Кнопка с числом.
# class NumberButton:
#
#     def __init__(self, text: str, pos: (int, int), player: Player):
#         self.font = self.font = pygame.font.Font("data/fonts/mnc.ttf", 18)
#         self.text = text
#         self.pos = pos
#
#         self.player = player
#
#         self.picked = False
#
#     def update_item(self):
#         if self.player.rect.x <= self.pos[0] <= self.player.rect.x + self.player.size[0] and \
#                 self.player.rect.y <= self.pos[1] <= self.player.rect.y + self.player.size[1] and \
#                 self.picked:
#             self.picked = True
#
#     def draw_item(self, screen):
#         if not self.picked:
#             text = self.font.render(self.text, True, (255, 255, 255))
#             screen.fill(pygame.Color("white"), (self.pos[0], self.pos[1], 24, 24))
#             screen.fill(pygame.Color("black"), (self.pos[0] + 2, self.pos[1] + 2, 20, 20))
#             screen.blit(text, (self.pos[0] + 3, self.pos[1] + 3))
