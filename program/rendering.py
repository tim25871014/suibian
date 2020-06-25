import pygame as pg
from positioning import *

def loadimg(filename):
    imgsrc = '../pictures/'
    return pg.image.load(imgsrc + filename).convert_alpha()

def render(brd, screen):
    namelist = ['king', 'shi', 'swordman', 'xiang', 'che', 'ma', 'pao', 'soldier']
    for i in range(0, 8):
        name = namelist[i]
        for c in range(0, brd.deathCount[0][name]):
            picname = name
            if name == 'shi' or name == 'swordman':
                picname = 'shi'
            pic = loadimg('b' + picname + '.png')
            pic = pg.transform.scale(pic, (31, 31))
            screen.blit(pic, (196 + i*28, 635 - c*5))
        for c in range(0, brd.deathCount[1][name]):
            picname = name
            if name == 'swordman':
                picname = 'shi'
            pic = loadimg('g' + picname + '.png')
            pic = pg.transform.scale(pic, (31, 31))
            screen.blit(pic, (99 + i*28, 49 - c*5))
    for p in brd.typeOnLocation:
        prefix = 'b'
        if brd.typeOnLocation[p].owner == 1:
            prefix = 'g'
        if brd.typeOnLocation[p].type == 'chema':
            pic = loadimg(prefix + 'ma.png')
            screen.blit(pic, coor_of_point(p))
            pic = loadimg(prefix + 'che.png')
            screen.blit(pic, (coor_of_point(p)[0], coor_of_point(p)[1] - 5))
        elif brd.typeOnLocation[p].type == 'mache':
            pic = loadimg(prefix + 'che.png')
            screen.blit(pic, coor_of_point(p))
            pic = loadimg(prefix + 'ma.png')
            screen.blit(pic, (coor_of_point(p)[0], coor_of_point(p)[1] - 3))
        elif brd.typeOnLocation[p].type == 'soldier':
            if brd.typeOnLocation[p].isActive == False:
                pic = loadimg(prefix + 'back.png')
            else:
                pic = loadimg(prefix + 'soldier.png')
            for i in range(0, brd.typeOnLocation[p].hp):
                screen.blit(pic, (coor_of_point(p)[0], coor_of_point(p)[1] + 3*i))
        else:
            picname = brd.typeOnLocation[p].type
            if brd.typeOnLocation[p].type == 'swordman':
                picname = 'shi'
            if brd.typeOnLocation[p].isActive == False:
                picname = 'back'
            pic = loadimg(prefix + picname + '.png')
            screen.blit(pic, coor_of_point(p))