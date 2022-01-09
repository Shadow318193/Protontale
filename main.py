import pygame

# Инициализация.
pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)  # Создание экрана.
pygame.display.set_caption("Protontale")

import battle  # Бой.

if __name__ == '__main__':
    battle.set_params(screen)  # Установка экрана в скрипт.
    battle.run()  # Запуск боя.
