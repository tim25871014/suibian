import pygame as pg
from positioning import *

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
            (8, 9): Stone('xiang', 1, 0, True),
            (7, 9): Stone('xiang', 1, 0, True)
        } # map 座標 -> Stone
        self.shiNum = 0
        self.xianRecover = (-1,-1)
        self.deathCount = [
            {'king': 1, 'shi': 1, 'swordman': 1, 'xiang': 2, 'che': 2, 'ma': 2, 'pao': 2, 'soldier': 5},
            {'king': 1, 'shi': 1, 'swordman': 1, 'xiang': 2, 'che': 2, 'ma': 2, 'pao': 2, 'soldier': 5}
        ] # list dict(死亡棋種 -> int)
    def stoneOnLocation(self, loc):
        if self.typeOnLocation.__contains__(loc):
            return self.typeOnLocation[loc]
        else:
            return 0
    def isLegal(self, move):
        a = 1
    def kill(self, locate,source):
        if locate not in self.typeOnLocation:
            return 0
        st = self.typeOnLocation[locate]
        if st.isActive == 0 and st.type == 'shi':
            self.shiNum += 1
            if self.shiNum == 2:
                st.type = 'swordman'
        if st.type == 'soldier':
            self.deathCount[st.type] += st.hp
        else:
            self.deathCount[st.type] += 1
        del self.typeOnLocation[locate]
        if st.type == 'king':
            self.kill(source,source)
    def hurt(self, locate, source):#扣一滴血，回傳是否死亡
        if self.typeOnLocation[locate].type == 'chema':
            self.typeOnLocation[locate].type = 'ma'
            self.deathCount['che'] += 1
            return 0
        if self.typeOnLocation[locate].type == 'mache':
            self.typeOnLocation[locate].type = 'che'
            self.deathCount['ma'] += 1
            return 0
        
        self.typeOnLocation[locate].hp -= 1
        if self.typeOnLocation[locate].type == 'soldier':
            self.deathCount[st.type] += 1
        if self.typeOnLocation[locate].hp == 0:
            kill(self,locate,source)
            return 1
        return 0
    def open(self, locate):
        self.typeOnLocation[move.location].isActive = 1
        if self.typeOnLocation[move.location].type == 'shi':
            self.shiNum += 1
            if self.shiNum == 2:
                self.typeOnLocation[move.location].type = 'swordman'
    def transfer(self, locate1, locate2):#把棋從locate1 動到 locate2
        if locate1 in self.typeOnLocation:
            self.typeOnLocation[locate2] = self.typeOnLocation[locate1]
            del self.typeOnLocation[locate1]
    def inside(self,locate):
        if locate[0] >= 0 and locate[0] < 10 and locate[1] >= 0 and locate[0] < 9:
            return True
        return False

    def makeMove(self, move):
        st = self.typeOnLocation[move.location]
        if self.xianRecover[0] >= 0:
            self.typeOnLocation[self.xianRecover].hp += 1
            self.xianRecover = (-1,-1)
        if st.isActive == 0: #翻棋
            self.open(self,move.location)
            return
        if st.action == 'skill': #技能
            if st.type == 'soldier':
                if move.objects[0] == move.location: # 犧牲救人
                    self.deathcount[st.type] += st.hp
                    self.deathcount[move.summon] -= 1
                    self.typeOnLocation[move.location] = move.summon
                else: # 召喚到旁
                    self.transfer(move.objects[0],move.dest)
                    del self.typeOnLocation[move.objects[0]]
            elif st.type == 'xiang':
                if move.objects[0] == move.location:# 回血
                    self.xianRecover = move.location
                else:#衝撞
                    nx = (move.dest[0] - move.location[0])/2
                    ny = (move.dest[1] - move.location[1])/2
                    self.transfer(move.location,move.dest)
                    self.hurt(move.dest,move.dest)
                    if inside((move.dest[0],move.dest[1])):
                        self.kill((move.dest[0],move.dest[1]),move.dest)
                    if inside((move.dest[0]+nx,move.dest[1])):
                        self.kill((move.dest[0]+nx,move.dest[1]),move.dest)
                    if inside((move.dest[0],move.dest[1]+ny)):
                        self.kill((move.dest[0],move.dest[1]+ny),move.dest)
                    if inside((move.dest[0]+nx,move.dest[1]+ny)):
                        self.kill((move.dest[0]+nx,move.dest[1]+ny),move.dest)
            elif st.type == 'king':#將衝到指定位置
                self.kill(move.objects[0],move.location)
                self.kill(move.objects[1],move.location)
                nx = (move.dest[0] - move.location[0])/2
                ny = (move.dest[1] - move.location[1])/2
                nowx = move.location[0]
                nowy = move.location[1]
                while not (nowx == move.dest[0] and nowy == move.dest[1]):
                    nowx += nx
                    nowy += ny
                    self.kill((nowx,nowy),move.location)
                self.transfer(move.location,move.dest)
            elif st.type == 'shi':
                self.deathcount[move.summon] -= 1
                self.typeOnLocation[move.dest] = move.summon
            elif st.type == 'swordman':
                self.kill(move.dest)
            elif st.type == 'pao':
                self.kill(move.objects[0],move.location)
                nx = (move.dest[0] - move.location[0])/2
                ny = (move.dest[1] - move.location[1])/2
                self.kill(move.dest,move.location)
                if inside((move.dest[0]+nx,move.dest[1]+ny)):
                    self.kill((move.dest[0]+nx,move.dest[1]+ny),move.location)
        else:#走或吃
            if move.dest in self.typeOnLocation:#吃
                if st.type == 'king':
                    if self.typeOnLocation[move.dest].isActive == 0:
                        self.open()
                    else:
                        self.kill(move.dest,move.location)
                    self.transfer(move.location,move.dest)
            else:#走
                transfer(move.location,move.dest)
            

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
            screen.blit(pic, coor_of_point(p))