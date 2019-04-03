import pygame
from pygame.locals import *
from IARandom import *
from IAMinMax import *

pygame.init()


class GameMenu:
    def __init__(self, screen, items, bg_color=(0, 0, 0), font="comicsansms", font_size=40,
                 font_color=(200, 200, 200)):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        self.bg_color = bg_color
        self.clock = pygame.time.Clock()

        self.items = items
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color

        self.items = []
        for index, item in enumerate(items):
            label = self.font.render(item, 1, font_color)

            width = label.get_rect().width
            height = label.get_rect().height

            posx = (self.scr_width / 2) - (width / 2)
            # t_h: total height of text block
            t_h = len(items) * height
            posy = (self.scr_height / 2) - (t_h / 2) + (index * height)

            self.items.append([item, label, (width, height), (posx, posy)])

    def menu1(self):
        mainloop = True
        while mainloop:
            # Limit frame speed to 50 FPS
            self.clock.tick(50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                elif event.type == KEYDOWN:
                    if event.key == K_a:
                        return 3
                    elif event.key == K_z:
                        return 5
                    elif event.key == K_e:
                        return 7
                    elif event.key == K_r:
                        return 9

            # Redraw the background
            self.screen.fill(self.bg_color)

            for name, label, (width, height), (posx, posy) in self.items:
                self.screen.blit(label, (posx, posy))

            pygame.display.flip()



    def menu2(self):
        mainloop = True
        while mainloop:
            # Limit frame speed to 50 FPS
            self.clock.tick(50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                elif event.type == KEYDOWN:
                    if event.key == K_a:
                        return 1
                    elif event.key == K_z:
                        return 0

            # Redraw the background
            self.screen.fill(self.bg_color)

            for name, label, (width, height), (posx, posy) in self.items:
                self.screen.blit(label, (posx, posy))

            pygame.display.flip()

    def menu3(self,game,player):
        mainloop = True
        while mainloop:
            # Limit frame speed to 50 FPS
            self.clock.tick(50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                elif event.type == KEYDOWN:
                    if event.key == K_a:
                        return IARandom(game,player)
                    elif event.key == K_z:
                        return IAMinMax(game,player)

            # Redraw the background
            self.screen.fill(self.bg_color)

            for name, label, (width, height), (posx, posy) in self.items:
                self.screen.blit(label, (posx, posy))

            pygame.display.flip()