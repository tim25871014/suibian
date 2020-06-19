import pygame as pg

def loadimg(filename):
    imgsrc = '../pictures/'
    return pg.image.load(imgsrc + filename).convert_alpha()

# 'king', 'shi','swordman', 'xiang', 'che', 'ma', 'pao', 'soldier, 'mache','chema'
class Stone:
    def __init__(self, stype, hp, owner, isActive):
        self.type = stype
        self.hp = hp
        self.owner = owner
        self.isActive = isActive      

class Move:
    def __init__(self, location, action, dest, objects, summon):
        self.location = location # 要做事的棋的座標
        self.action = action # 要做的事 ('move', 'skill')
        self.dest = dest # 要移動到、發動技能的座標
        self.objects = objects # 要犧牲的棋座標 (座標 list)
        self.summon = summon # 要召喚的棋(stone)

class ChessBoard:
    def __init__(self):
        self.typeOnLocation = {
            (0, 7): Stone('ma', 1, 0, False),
            (4, 8): Stone('soldier', 2, 1, True),
            (2, 5): Stone('king', 1, 1, False),
            (6, 3): Stone('swordman', 1, 1, True),
            (0, 0): Stone('xiang', 1, 0, True),
            (0, 9): Stone('xiang', 1, 0, True),
            (8, 0): Stone('xiang', 1, 0, True),
            (8, 9): Stone('xiang', 1, 0, True)
        } # map 座標 -> Stone
        self.shiNum = 0
        self.xianRecover = (-1,-1)
        self.deathCount = [
            {'king': 1, 'shi': 1, 'swordman': 1, 'xiang': 2, 'che': 2, 'ma': 2, 'pao': 2, 'soldier': 5},
            {'king': 1, 'shi': 1, 'swordman': 1, 'xiang': 2, 'che': 2, 'ma': 2, 'pao': 2, 'soldier': 5}
        ] # list dict(死亡棋種 -> int)
    def isLegal(self, move):
        a = 1
    def makeMove(self, move):
        a = 1
        """
        # 2
        st = self.typeOnLocation[move.location]
        if self.xianRecover[0] >= 0:
            self.typeOnLocation[self.xianRecover].hp += 1
            self.xianRecover = (-1,-1)
        if st.isActive == 0:
            self.typeOnLocation[move.location].isActive = 1
            return
        if st.action == 'skill':
            if st.stype == 'soldier':
                if move.objects[0] == move.location:
        """
    def isWin(self):
        a = 1

    def render(self, screen):
        namelist = ['king', 'shi', 'swordman', 'xiang', 'che', 'ma', 'pao', 'soldier']
        for i in range(0, 8):
            name = namelist[i]
            for c in range(0, self.deathCount[0][name]):
                picname = name
                if name == 'shi' or name == 'swordman':
                    picname = 'shi'
                pic = loadimg('b' + picname + '.png')
                pic = pg.transform.scale(pic, (31, 31))
                screen.blit(pic, (196 + i*28, 635 - c*5))
            for c in range(0, self.deathCount[1][name]):
                picname = name
                if name == 'swordman':
                    picname = 'shi'
                pic = loadimg('g' + picname + '.png')
                pic = pg.transform.scale(pic, (31, 31))
                screen.blit(pic, (99 + i*28, 49 - c*5))
        for p in self.typeOnLocation:
            picname = self.typeOnLocation[p].type
            prefix = 'b'
            if self.typeOnLocation[p].owner == 1:
                prefix = 'g'
            if self.typeOnLocation[p].type == 'swordman':
                picname = 'shi'
            if self.typeOnLocation[p].isActive == False:
                picname = 'back'
            pic = loadimg(prefix + picname + '.png')
            screen.blit(pic, (33 + p[0]*49.375, 86 + p[1]*49.666))
