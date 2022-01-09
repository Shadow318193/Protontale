import pygame
import random

import entities  # Игровые объекты.
import interface  # Интерфейс.
import buttons

screen = None  # Защита от запуска боя при отсутствии экранного объекта.

fps = 60
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()  # Позволяет сразу рисовать все спрайты.

background = interface.Background()

wall = entities.Wall((600, 200))

protoshka = entities.Protoshka(all_sprites)  # Враг в данной игре.

buttons = [buttons.ButtonFight(all_sprites),
           buttons.ButtonAct(all_sprites),
           buttons.ButtonItem(all_sprites),
           buttons.ButtonMercy(all_sprites)]

player = entities.Player(all_sprites, wall=wall, buttons=buttons)

hp_bar = interface.HPBar(player)

pygame.mixer.music.load("data/mus/proton.mp3")
pygame.mixer.music.set_volume(0.1)

bullets = []  # Объекты, от которых игрок получает урон.


def set_params(surface):
    # Установка экрана в скрипт
    global screen
    screen = surface


# Основной скрипт
def run():

    def update_state():
        # События с клавиатурой.

        key = pygame.key.get_pressed()

        # Игрок двигается
        if not player.my_turn:
            player.move(key)

        # Рисование объектов, не являющиеся спрайтами.
        background.draw(screen)
        wall.draw(screen)

        hp_bar.draw(screen)

        for bullet in bullets:
            bullet.draw_bullet(screen)
            bullet.update_bullet()
            if not bullet.can_damage:
                bullets.remove(bullet)  # Удаляет пулю, вылетевшую за экран или попавшую в игрока.
                if isinstance(bullet, entities.NumberBullet):
                    # Удаляет спрайт пули, выглядящей как число.
                    all_sprites.remove(bullet)

        if not player.my_turn:
            bullets.append(entities.NumberBullet(all_sprites,
                                                 player=player,
                                                 size=(16, 16),
                                                 pos=(0, random.randint(200, 500)),
                                                 damage=1,
                                                 direction=[1, 0],
                                                 speed=1))

    def is_player_dead():
        global bullets
        nonlocal black_screen

        if player.hp <= 0:
            bullets = []
            player.die()

    if isinstance(screen, pygame.Surface):
        # Таймер, до истечения которого экран будет чёрным (вступление).
        t = 0

        black_screen = True
        player.can_move = False

        running = True
        while running:

            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()

            screen.fill(pygame.Color("black"))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if player.my_turn:
                        player.move(pygame.key.get_pressed())

            if t == 90:
                if player.hp > 0:
                    black_screen = False
                    player.can_move = True
            if t < 90:
                t += 1

            update_state()

            all_sprites.draw(screen)

            is_player_dead()

            if player.died:
                all_sprites.remove(player)

            if black_screen:
                screen.fill(pygame.Color("black"))

            if player.hp <= 0:
                screen.blit(player.image, (player.rect.x, player.rect.y))

            pygame.display.flip()

            clock.tick(fps)
    else:
        print("Initialization Error")