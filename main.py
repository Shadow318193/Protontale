import pygame
import random

# Инициализация.
pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

import entities  # Персонажи.
import interface  # Интерфейс боя.


if __name__ == '__main__':
    all_sprites = pygame.sprite.Group()
    wall = entities.Wall(400, 200)
    player = entities.Player(all_sprites, wall=wall)
    hp_bar = interface.HPBar(player)

    pygame.mixer.music.load("data/mus/proton.mp3")


    def update_state():
        # События с клавиатурой.
        key = pygame.key.get_pressed()

        player.move(key)
        wall.draw(screen)
        hp_bar.draw(screen)

        for bullet in bullets:
            bullet.draw(screen)
            bullet.update()
            if not bullet.can_damage:
                bullets.remove(bullet)


    pygame.display.set_caption("ProtonTale")

    bullets = [entities.Bullet(player, (16, 16), 0, 400, 10, [1, 0], 1)]

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

        if t == 90:
            black_screen = False
            player.can_move = True
        if t < 90:
            t += 1

        update_state()

        all_sprites.draw(screen)

        if black_screen:
            screen.fill(pygame.Color("black"))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
