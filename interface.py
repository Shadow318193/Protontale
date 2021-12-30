import pygame
import entities


class HPBar:

    def __init__(self, creature: entities.Creature):
        self.can_draw = True
        self.creature = creature

    def draw(self, screen):
        if self.can_draw:

            screen.fill(pygame.Color("yellow"), (500, 500, 50, 20))
            screen.fill(pygame.Color("red"), (500, 500, 50, 20))
