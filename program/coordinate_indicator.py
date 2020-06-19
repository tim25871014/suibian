import pygame as pg
from positioning import *

# settings
FPS = 60
pg.init()
main_clock = pg.time.Clock()
width, height = 522, 675  # fixed
screen = pg.display.set_mode((width, height))
pg.display.set_caption('Wang Zheng Chess DX')

background = pg.image.load('../pictures/design.png').convert_alpha()
screen.blit(background, (0, 0))
pg.display.update()

Program = True
while Program:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            Program = False
        if event.type == pg.MOUSEMOTION:
            print(pg.mouse.get_pos())
            print(nearest_point(pg.mouse.get_pos()))
    main_clock.tick(FPS)