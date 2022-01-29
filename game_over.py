import pygame
from game_core import load_image

screen = None

all_sprites = pygame.sprite.Group()

player = pygame.sprite.Sprite()
player.image = load_image("soul.bmp", colorkey=(255, 255, 255))
player.rect = player.image.get_rect()
player.rect.x = 275 - 32
player.rect.y = 600 // 1.5 - 8

font = pygame.font.Font("data/fonts/determination.otf", 32)
all_sprites.add(player)


def set_params(surface):
    # Установка экрана в скрипт
    global screen
    screen = surface


def run():
    if isinstance(screen, pygame.Surface):
        global font

        cont = True

        running = True
        while running:

            screen.fill(pygame.Color("black"))

            text = font.render("Продолжить?", True, (255, 255, 255))
            screen.blit(text, (300, 600 // 4))

            text = font.render("Да", True, (255, 255, 255))
            screen.blit(text, (275, 600 // 1.5 - 16))

            text = font.render("Нет", True, (255, 255, 255))
            screen.blit(text, (475, 600 // 1.5 - 16))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if pygame.key.get_pressed()[pygame.K_LEFT] or \
                            pygame.key.get_pressed()[pygame.K_RIGHT]:
                        if cont:
                            cont = False
                            player.rect.x = 475 - 32
                        else:
                            cont = True
                            player.rect.x = 275 - 32
                    if pygame.key.get_pressed()[pygame.K_z]:
                        if cont:
                            running = False
                        else:
                            pygame.quit()

            all_sprites.draw(screen)

            pygame.display.flip()
