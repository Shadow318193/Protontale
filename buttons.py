import pygame
from game_core import load_image


class ButtonFight(pygame.sprite.Sprite):
    image = load_image("fight_btn.bmp")
    image_use = load_image("fight_btn_use.bmp")

    def __init__(self, *group):
        pygame.sprite.Sprite.__init__(self, *group)
        self.image = ButtonFight.image_use
        self.image = pygame.transform.scale(self.image, (220 // 1.5, 84 // 1.5))

        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = 530

        self.used = True

        self.can_draw = True

    def change_sprite(self):
        if self.used:
            self.image = ButtonFight.image
            self.image = pygame.transform.scale(self.image, (220 // 1.5, 84 // 1.5))

            self.used = False
        else:
            self.image = ButtonFight.image_use
            self.image = pygame.transform.scale(self.image, (220 // 1.5, 84 // 1.5))

            self.used = True


class ButtonAct(pygame.sprite.Sprite):
    image = load_image("act_btn.bmp")
    image_use = load_image("act_btn_use.bmp")

    def __init__(self, *group):
        pygame.sprite.Sprite.__init__(self, *group)
        self.image = ButtonAct.image
        self.image = pygame.transform.scale(self.image, (220 // 1.5, 84 // 1.5))

        self.rect = self.image.get_rect()
        self.rect.x = 220
        self.rect.y = 530

        self.used = False

        self.can_draw = True

    def change_sprite(self):
        if self.used:
            self.image = ButtonAct.image
            self.image = pygame.transform.scale(self.image, (220 // 1.5, 84 // 1.5))

            self.used = False
        else:
            self.image = ButtonAct.image_use
            self.image = pygame.transform.scale(self.image, (220 // 1.5, 84 // 1.5))

            self.used = True


class ButtonItem(pygame.sprite.Sprite):
    image = load_image("item_btn.bmp")
    image_use = load_image("item_btn_use.bmp")

    def __init__(self, *group):
        pygame.sprite.Sprite.__init__(self, *group)
        self.image = ButtonItem.image
        self.image = pygame.transform.scale(self.image, (220 // 1.5, 84 // 1.5))

        self.rect = self.image.get_rect()
        self.rect.x = 420
        self.rect.y = 530

        self.used = False

        self.can_draw = True

    def change_sprite(self):
        if self.used:
            self.image = ButtonItem.image
            self.image = pygame.transform.scale(self.image, (220 // 1.5, 84 // 1.5))

            self.used = False
        else:
            self.image = ButtonItem.image_use
            self.image = pygame.transform.scale(self.image, (220 // 1.5, 84 // 1.5))

            self.used = True


class ButtonMercy(pygame.sprite.Sprite):
    image = load_image("mercy_btn.bmp")
    image_use = load_image("mercy_btn_use.bmp")

    def __init__(self, *group):
        pygame.sprite.Sprite.__init__(self, *group)
        self.image = ButtonMercy.image
        self.image = pygame.transform.scale(self.image, (220 // 1.5, 84 // 1.5))

        self.rect = self.image.get_rect()
        self.rect.x = 620
        self.rect.y = 530

        self.used = False

        self.can_draw = True

    def change_sprite(self):
        if self.used:
            self.image = ButtonMercy.image
            self.image = pygame.transform.scale(self.image, (220 // 1.5, 84 // 1.5))

            self.used = False
        else:
            self.image = ButtonMercy.image_use
            self.image = pygame.transform.scale(self.image, (220 // 1.5, 84 // 1.5))

            self.used = True
