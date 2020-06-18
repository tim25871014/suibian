import pygame as pg
from network import *

FPS = 60
pg.init()
main_clock = pg.time.Clock()
width, height = 522, 675  # fixed
screen = pg.display.set_mode((width, height))
pg.display.set_caption('Wang Zheng Chess DX')
network = Network()

def loadimg(filename):
    imgsrc = '../pictures/'
    return pg.image.load(imgsrc + filename).convert_alpha()

class TextBox(pg.sprite.Sprite):
    def __init__(self, top, left):
        super().__init__()
        self.validChars = "1234567890"
        self.text = ''
        self.font = pg.font.Font(None, 100)
        self.rect = (top, left)
        self.limit = 6
    def add_chr(self, char):
        if char in self.validChars and len(self.text) < self.limit:
            self.text += char
    def isvaild(self):
        return len(self.text) == self.limit
    def del_chr(self):
        self.text = self.text[:-1]
    def reset(self):
        self.text = ''
    def render(self):
        self.image = self.font.render(self.text + '|', False, [0, 0, 0])
        screen.blit(self.image, self.rect)

class Stone(pg.sprite.Sprite):
    def __init__(self, picture):
        super().__init__()
        self.image = loadimg(picture)
        self.rect = self.image.get_rect()

class Button(pg.sprite.Sprite):
    def __init__(self, picture, picture_active, top, left):
        super().__init__()
        self.image = loadimg(picture)
        self.image_active = loadimg(picture_active)
        self.rect = (top, left)
        self.isActive = False
    def render(self):
        if self.isActive:
            screen.blit(self.image_active, self.rect)
        else:
            screen.blit(self.image, self.rect)

class MessageBox(pg.sprite.Sprite):
    def __init__(self, picture, top, left):
        super().__init__()
        self.image = loadimg(picture)
        self.rect = (top, left)
    def render(self):
        screen.blit(self.image, self.rect)

class StartingButton(Button):
    def __init__(self, picture, picture_active, top, left):
        super().__init__(picture, picture_active, top, left)
    def isInArea(self, loc):
        return self.rect[0]+46 < loc[0] < self.rect[0]+389 and self.rect[1]+12 < loc[1] < self.rect[1]+75

class RoundButton(Button):
    def __init__(self, picture, picture_active, top, left):
        super().__init__(picture, picture_active, top, left)
    def isInArea(self, loc):
        return (loc[0] - self.rect[0]-17) ** 2 + (loc[1] - self.rect[1]-14) ** 2 <= 512
