import pygame as pg

def loadimg(filename):
    imgsrc = '../pictures/'
    return pg.image.load(imgsrc + filename).convert_alpha()

def setbackground(filename, screen):
    imgsrc = '../pictures/'
    background = pg.image.load(imgsrc + filename).convert_alpha()
    screen.blit(background, (0, 0))

class TextBox:
    def __init__(self, top, left):
        self.validChars = "1234567890"
        self.text = ''
        self.font = pg.font.SysFont('consolas', 70)
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
    def render(self, screen):
        self.image = self.font.render(self.text + '|', True, [0, 0, 0])
        if self.text == '':
            screen.blit(self.image, (self.rect[0] - 10, self.rect[1]))
        else:
            screen.blit(self.image, self.rect)

class Timer:
    def __init__(self, top, left, color):
        self.color = color
        self.roundTime = 60 # seconds
        self.initialTime = 300 # seconds
        self.time = 0
        self.font = pg.font.SysFont('consolas', 40)
        self.rect = (top, left)
    def reset(self):
        self.time = self.roundTime
    def reset_long(self):
        self.time = self.initialTime
    def decrease(self):
        self.time -= 1
        if self.time <= 0:
            self.time = 0
    def render(self, screen):
        text = str(self.time)
        if len(text) == 1:
            text = ' ' + text
        self.image = self.font.render(text, True, self.color)
        screen.blit(self.image, self.rect)

class Button:
    def __init__(self, picture, picture_active, top, left):
        self.image = loadimg(picture)
        self.image_active = loadimg(picture_active)
        self.rect = (top, left)
        self.isActive = False
    def render(self, screen):
        if self.isActive:
            screen.blit(self.image_active, self.rect)
        else:
            screen.blit(self.image, self.rect)

class MessageBox:
    def __init__(self, picture, top, left):
        self.image = loadimg(picture)
        self.rect = (top, left)
    def render(self, screen):
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

class SkillButton(Button):
    def __init__(self, picture, picture_active, top, left):
        super().__init__(picture, picture_active, top, left)
    def isInArea(self, loc):
        return self.rect[0]+5 < loc[0] < self.rect[0]+91 and self.rect[1]+7 < loc[1] < self.rect[1]+58

class BackButton(Button):
    def __init__(self, picture, picture_active, top, left):
        super().__init__(picture, picture_active, top, left)
    def isInArea(self, loc):
        return self.rect[0]+11 < loc[0] < self.rect[0]+208 and self.rect[1]+5 < loc[1] < self.rect[1]+52