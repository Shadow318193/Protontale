import pygame
import entities


class Background:

    def __init__(self):
        self.x = 350
        self.direction = 1

    def draw(self, screen):
        for y in range(50, 251, 50):
            pygame.draw.line(screen, pygame.Color("green"), (300, y), (500, y))
        for x in range(self.x, self.x + 101, 50):
            pygame.draw.line(screen, pygame.Color("green"), (x, 10), (x, 300))

        if not 300 <= self.x <= 400:
            self.direction = -self.direction
        self.x += self.direction


class HPBar:

    def __init__(self, creature: entities.Creature, is_player: bool, pos: (int, int, int, int)):
        self.can_draw = is_player
        self.is_player = is_player
        self.creature = creature
        if self.is_player:
            self.font = pygame.font.Font("data/fonts/determination.otf", 20)
            self.font2 = pygame.font.Font("data/fonts/mnc.ttf", 26)
        self.pos = pos

    def draw(self, screen):
        if self.can_draw:
            screen.fill(pygame.Color("red"), self.pos)
            screen.fill(pygame.Color("yellow"), (self.pos[0], self.pos[1],
                                                 self.pos[2] * self.creature.hp // self.creature.max_hp,
                                                 self.pos[3]))
            if self.is_player:
                text = self.font.render("HP", True, (255, 255, 255))
                text2 = self.font2.render("YOU", True, (255, 255, 255))
                text3 = self.font2.render("LV1", True, (255, 255, 255))
                text4 = self.font2.render(str(self.creature.hp) + "/" + str(self.creature.max_hp),
                                         True, (255, 255, 255))
                screen.blit(text, (437, 472))
                screen.blit(text2, (200, 472))
                screen.blit(text3, (300, 472))
                screen.blit(text4, (510, 472))
