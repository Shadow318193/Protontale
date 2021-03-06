import pygame
import random

import entities  # Игровые объекты.
import interface  # Интерфейс.
import buttons  # Внутриигровые кнопки.


screen = None  # Защита от запуска боя при отсутствии экранного объекта.

fps = 60
clock = pygame.time.Clock()  # Тики.

all_sprites = pygame.sprite.Group()  # Позволяет сразу рисовать все спрайты.

background = interface.Background()

wall = entities.Wall((600, 200))

protoshka = entities.Protoshka(all_sprites)  # Враг в данной игре.

buttons_list = [buttons.ButtonFight(all_sprites),
                buttons.ButtonAct(all_sprites),
                buttons.ButtonItem(all_sprites),
                buttons.ButtonMercy(all_sprites)]

player = entities.Player(all_sprites, wall=wall, buttons=buttons_list)

hp_bar = interface.HPBar(player, True, (470, 475, 30, 20))
protoshka_hp_bar = interface.HPBar(protoshka, False, (200, 50, 400, 20))

attack_type = 0  # Варианты атаки Протошки.

pygame.mixer.music.load("data/mus/proton.mp3")
pygame.mixer.music.set_volume(0.1)

bullets = []  # Объекты, от которых игрок получает урон.

# TODO Объекты, которые игрок может подбирать.
# items = []


def init():
    global all_sprites, background, wall, protoshka, buttons_list, player, hp_bar
    global protoshka_hp_bar, attack_type, bullets

    all_sprites = pygame.sprite.Group()  # Позволяет сразу рисовать все спрайты.

    background = interface.Background()

    wall = entities.Wall((600, 200))

    protoshka = entities.Protoshka(all_sprites)  # Враг в данной игре.

    buttons_list = [buttons.ButtonFight(all_sprites),
                    buttons.ButtonAct(all_sprites),
                    buttons.ButtonItem(all_sprites),
                    buttons.ButtonMercy(all_sprites)]

    player = entities.Player(all_sprites, wall=wall, buttons=buttons_list)

    hp_bar = interface.HPBar(player, True, (470, 475, 30, 20))
    protoshka_hp_bar = interface.HPBar(protoshka, False, (200, 50, 400, 20))

    attack_type = 0  # Варианты атаки Протошки.

    pygame.mixer.music.unload()
    pygame.mixer.music.load("data/mus/proton.mp3")


def set_params(surface):
    # Установка экрана в скрипт
    global screen
    screen = surface


# Основной скрипт
def run():

    def update_state():
        # События с клавиатурой.
        global bullets, attack_type

        key = pygame.key.get_pressed()

        # Игрок двигается
        if not player.my_turn:
            player.move(key, protoshka)

        # Рисование объектов, не являющиеся спрайтами.
        background.draw(screen)

        wall.draw(screen, all_sprites, player.items)

        hp_bar.draw(screen)
        protoshka_hp_bar.draw(screen)

        if not player.my_turn:
            if not attack_type:
                if protoshka.hp > 50:
                    bullets.append(entities.NumberBullet(all_sprites,
                                                         player=player,
                                                         size=(16, 16),
                                                         pos=(0, random.randint(200, 500)),
                                                         damage=1,
                                                         direction=[5, 0]))
                else:
                    bullets.append(entities.NumberBullet(all_sprites,
                                                         player=player,
                                                         size=(16, 16),
                                                         pos=(0, random.randint(200, 500)),
                                                         damage=1,
                                                         direction=[8, 0]))
            elif attack_type == 1:
                bullets.append(entities.NumberBullet(all_sprites,
                                                     player=player,
                                                     size=(16, 16),
                                                     pos=(800, random.randint(200, 500)),
                                                     damage=1,
                                                     direction=[-8, 0]))
            elif attack_type == 2:
                bullets.append(entities.NumberBullet(all_sprites,
                                                     player=player,
                                                     size=(16, 16),
                                                     pos=(random.randint(wall.x - 16, wall.x + wall.width), -16),
                                                     damage=1,
                                                     direction=[0, 8]))

            wall.set_size((300, 200))
        else:
            for bullet in bullets:
                bullet.can_damage = False
            wall.set_size((600, 200))

        for bullet in bullets:
            bullet.draw_bullet(screen)
            bullet.update_bullet()
            if not bullet.can_damage:
                bullets.remove(bullet)  # Удаляет пулю, вылетевшую за экран или попавшую в игрока.
                if isinstance(bullet, entities.NumberBullet):
                    # Удаляет спрайт пули, выглядящей как число.
                    all_sprites.remove(bullet)

        # for item in items:
        #     item.draw_item(screen)
        #     item.update_item()
        #     if item.picked:
        #         all_sprites.remove(item)

        if wall.turn >= 10 and protoshka.hp > 50:
            protoshka.can_spare = True
        elif protoshka.hp <= 50:
            wall.pacifist = False

        if player.my_turn:
            if protoshka.hp > 50:
                attack_type = 0
            else:
                attack_type = random.randint(0, 2)

    def is_player_dead():
        global bullets
        nonlocal black_screen

        if player.hp <= 0:
            bullets = []
            black_screen = True
            player.die()

    if isinstance(screen, pygame.Surface):
        t = 0  # Таймер, до истечения которого экран будет чёрным (вступление).

        black_screen = True
        player.can_move = False

        running = True
        while running:

            if not pygame.mixer.music.get_busy() and player.hp > 0 and protoshka.hp > 0 and \
                    not protoshka.spared and not player.attacking:
                pygame.mixer.music.play()

            screen.fill(pygame.Color("black"))  # Очищение экрана.

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if player.my_turn:
                        player.move(pygame.key.get_pressed(), protoshka)

            if t == 90:
                if player.hp > 0:
                    black_screen = False
                    player.can_move = True
            if t <= 90:
                t += 1

            update_state()

            all_sprites.draw(screen)

            is_player_dead()

            if player.attacking:
                player.attack(protoshka, protoshka_hp_bar)

            if black_screen:
                screen.fill(pygame.Color("black"))

            if player.hp <= 0 and not player.died:
                screen.blit(player.image, (player.rect.x, player.rect.y))
            elif player.died:
                t += 1
                if t >= 150:
                    running = False

            pygame.display.flip()

            clock.tick(fps)
