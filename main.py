import pygame

# Инициализация.
pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)  # Создание экрана.
pygame.display.set_caption("Protontale")

import battle  # Бой.
import game_over  # Экран проигрыша.

if __name__ == '__main__':
    # Установка экрана в скрипты.
    battle.set_params(screen)
    game_over.set_params(screen)

    while True:
        battle.run()  # Запуск боя.
        game_over.run()  # Запуск экрана проигрыша.
        battle.init()
