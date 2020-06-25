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
        self.typeOnLocation = {} # map 座標 -> Stone
        self.shiNum = [0,0]
        self.xianRecover = [(-1,-1), (-1, -1)]
        self.namelist = ['king', 'shi', 'swordman', 'xiang', 'che', 'ma', 'pao', 'soldier']
        self.deathCount = [
            {'king': 1, 'shi': 1, 'swordman': 1, 'xiang': 2, 'che': 2, 'ma': 2, 'pao': 2, 'soldier': 5},
            {'king': 0, 'shi': 0, 'swordman': 0, 'xiang': 0, 'che': 0, 'ma': 0, 'pao': 0, 'soldier': 0}
        ] # list dict(死亡棋種 -> int)
    def merge_and_hide(self, other):
        self.typeOnLocation.update(other.typeOnLocation)
        for idx in self.typeOnLocation:
            self.typeOnLocation[idx].isActive = False
    def swap_vision(self):
        tmp = {}
        for idx in self.typeOnLocation:
            s = self.typeOnLocation[idx]
            s.owner = 1 - s.owner
            tmp[(8 - idx[0], 9 - idx[1])] = self.typeOnLocation[idx]
        self.deathCount[0], self.deathCount[1] = self.deathCount[1], self.deathCount[0]
        self.shiNum[0], self.shiNum[1] = self.shiNum[1], self.shiNum[0]
        self.typeOnLocation = tmp
        #self.xianRecover[0], self.xianRecover[1] = self.xianRecover[1], self.xianRecover[0]
    def stoneOnLocation(self, loc):
        if self.typeOnLocation.__contains__(loc):
            return self.typeOnLocation[loc]
        else:
            return 0
    def isLegal(self, move):
        a = 1
    def kill(self, locate, source): #殺死位於locate的棋，傷害來源是source
        if locate not in self.typeOnLocation:
            return
        st = self.typeOnLocation[locate]
        if st.isActive == 0 and st.type == 'shi':
            self.shiNum[st.owner] += 1
            if self.shiNum[st.owner] == 2:
                st.type = 'swordman'
        if st.type == 'soldier':
            self.deathCount[self.typeOnLocation[locate].owner][st.type] += st.hp
        else:
            self.deathCount[self.typeOnLocation[locate].owner][st.type] += 1
        del self.typeOnLocation[locate]
        if st.type == 'king':
            self.kill(source, source)
        if st.type == 'xiang' and locate == self.xianRecover[1]:
            self.xianRecover[1] = (-1,-1)

    def hurt(self, locate, source):#扣一滴血，回傳是否死亡
        if locate not in self.typeOnLocation:
            return False
        if self.typeOnLocation[locate].type == 'chema':
            self.typeOnLocation[locate].type = 'ma'
            self.deathCount[self.typeOnLocation[locate].owner]['che'] += 1
            return False
        if self.typeOnLocation[locate].type == 'mache':
            self.typeOnLocation[locate].type = 'che'
            self.deathCount[self.typeOnLocation[locate].owner]['ma'] += 1
            return False
        
        self.typeOnLocation[locate].hp -= 1
        if self.typeOnLocation[locate].type == 'soldier':
            self.deathCount[self.typeOnLocation[locate].owner]['soldier'] += 1
        if self.typeOnLocation[locate].hp == 0:
            self.kill(locate,source)
            return True
        return False
    def open(self, locate):#翻開一顆暗棋
        self.typeOnLocation[locate].isActive = 1
        if self.typeOnLocation[locate].type == 'shi':
            self.shiNum[self.typeOnLocation[locate].owner] += 1
            if self.shiNum[self.typeOnLocation[locate].owner] == 2:
                self.typeOnLocation[locate].type = 'swordman'
    def transfer(self, locate1, locate2):#把棋從locate1 動到 locate2
        if locate1 in self.typeOnLocation:
            self.typeOnLocation[locate2] = self.typeOnLocation[locate1]
            del self.typeOnLocation[locate1]
    def inside(self,locate):
        if locate[0] >= 0 and locate[0] < 10 and locate[1] >= 0 and locate[0] < 9:
            return True
        return False

    def makeMove(self, move):#void
        if move.location[0] == -1: # 初始盤面
            self.deathCount[0][move.summon.type] -= 1
            self.typeOnLocation[move.dest] = move.summon
        if self.xianRecover[1][0] >= 0:
            self.typeOnLocation[self.xianRecover[0]].hp += 1
        self.xianRecover[1] = self.xianRecover[0]
        self.xianRecover[0] = (-1,-1)
        if move.location not in self.typeOnLocation:
            return
        st = self.typeOnLocation[move.location]
        
        if st.isActive == 0: #翻棋
            self.open(move.location)
            return
        if move.action == 'skill': #技能
            if st.type == 'soldier':
                if move.objects[0] == move.location: # 犧牲救人
                    self.deathcount[self.typeOnLocation[move.location].owner][st.type] += st.hp
                    self.deathcount[self.typeOnLocation[move.location].owner][move.summon] -= 1
                    self.typeOnLocation[move.location] = move.summon
                else: # 召喚到旁
                    self.transfer(move.objects[0],move.dest)
            elif st.type == 'xiang':
                if move.objects != [] and move.objects[0] == move.location:# 犧牲自己=回血
                    self.xianRecover[0] = move.location
                else:#衝撞
                    nx = (move.dest[0] - move.location[0])/2
                    ny = (move.dest[1] - move.location[1])/2
                    if self.inside((move.dest[0],move.dest[1])):
                        self.kill((move.dest[0],move.dest[1]),move.dest)
                    if self.inside((move.dest[0]+nx,move.dest[1])):
                        self.kill((move.dest[0]+nx,move.dest[1]),move.dest)
                    if self.inside((move.dest[0],move.dest[1]+ny)):
                        self.kill((move.dest[0],move.dest[1]+ny),move.dest)
                    if self.inside((move.dest[0]+nx,move.dest[1]+ny)):
                        self.kill((move.dest[0]+nx,move.dest[1]+ny),move.dest)
                    self.transfer(move.location,move.dest)
                    self.hurt(move.dest,move.dest)
            elif st.type == 'king':#將衝到指定位置
                self.kill(move.objects[0],move.location)
                self.kill(move.objects[1],move.location)
                nx = (move.dest[0] - move.location[0])
                ny = (move.dest[1] - move.location[1])
                if nx != 0:
                    nx /= abs(nx)
                if ny != 0:
                    ny /= abs(ny)
                nowx = move.location[0]
                nowy = move.location[1]
                while not (nowx == move.dest[0] and nowy == move.dest[1]):
                    nowx += nx
                    nowy += ny
                    self.kill((nowx,nowy),move.location)
                self.transfer(move.location,move.dest)
            elif st.type == 'shi':
                self.deathCount[self.typeOnLocation[move.location].owner][move.summon.type] -= 1
                self.typeOnLocation[move.dest] = move.summon
            elif st.type == 'swordman':
                self.kill(move.dest, move.location)
            elif st.type == 'pao':
                self.kill(move.objects[0],move.location)
                nx = (move.dest[0] - move.location[0])
                ny = (move.dest[1] - move.location[1])
                if nx != 0:
                    nx /= abs(nx)
                if ny != 0:
                    ny /= abs(ny)
                self.kill(move.dest,move.location)
                if self.inside((move.dest[0]+nx,move.dest[1]+ny)):
                    self.kill((move.dest[0]+nx,move.dest[1]+ny),move.location)
                if nx == 0:
                    if self.inside((move.dest[0],move.dest[1]-1)):
                        self.kill((move.dest[0],move.dest[1]-1),move.location)
                    if self.inside((move.dest[0],move.dest[1]+1)):
                        self.kill((move.dest[0],move.dest[1]+1),move.location)
                else:
                    if self.inside((move.dest[0]-1,move.dest[1])):
                        self.kill((move.dest[0]-1,move.dest[1]),move.location)
                    if self.inside((move.dest[0]+1,move.dest[1])):
                        self.kill((move.dest[0]+1,move.dest[1]),move.location)
        else:#走或吃或疊
            nx = (move.dest[0] - move.location[0])
            ny = (move.dest[1] - move.location[1])
            if nx != 0:
                nx /= abs(nx)
            if ny != 0:
                ny /= abs(ny)
            if move.dest in self.typeOnLocation and self.typeOnLocation[move.dest].owner != self.typeOnLocation[move.location].owner:#吃
                if st.type == 'king':
                    if self.typeOnLocation[move.dest].owner == st.owner:
                        self.transfer(move.location,(move.dest[0]-nx,move.dest[1]-ny))
                        return
                    die = self.typeOnLocation[move.dest]
                    self.kill(move.dest,move.location)
                    if die.isActive == 0:
                        if die.type == 'shi' and self.shiNum[st.owner] == 0:
                            self.kill(move.location,move.location)
                    self.transfer(move.location,move.dest)
                elif st.type == 'che':
                    if self.hurt(move.dest,move.location):
                        self.transfer(move.location,move.dest)
                    else:
                        self.transfer(move.location,(move.dest[0]-nx,move.dest[1]-ny))
                elif st.type == 'chema' or st.type == 'mache':
                    if self.hurt(move.dest,move.location):
                        self.transfer(move.location,move.dest)
                        return
                    elif self.hurt(move.dest,move.location):
                        self.transfer(move.location,move.dest)
                        return
                    self.transfer(move.location,(move.dest[0]-nx,move.dest[1]-ny))
                elif st.type == 'soldier':
                    for i in range(0,st.hp):
                        if self.hurt(move.dest,move.location):
                            self.transfer(move.location,move.dest)
                            return
                elif st.type == 'xiang' and st.hp == 2:
                    if self.hurt(move.dest,move.location):
                        self.transfer(move.location,move.dest)
                        return
                    elif self.hurt(move.dest,move.location):
                        self.transfer(move.location,move.dest)
                        return
                else:
                    if self.hurt(move.dest,move.location):
                        self.transfer(move.location,move.dest)
            elif move.dest not in self.typeOnLocation:#走
                self.transfer(move.location,move.dest)
            else:#疊
                if st.type == 'soldier':
                    self.typeOnLocation[move.dest].hp += 1
                    del self.typeOnLocation[move.location]
                elif st.type == 'ma':
                    self.typeOnLocation[move.dest].type = 'mache'
                    del self.typeOnLocation[move.location]
                elif st.type == 'che':
                    self.typeOnLocation[move.dest].type = 'chema'
                    del self.typeOnLocation[move.location]
    def isWin(self):
        if self.deathCount[0]['soldier'] >= 5:
            return 1
        if self.deathCount[1]['soldier'] >= 5:
            return 0
        for key in self.typeOnLocation:
            if self.typeOnLocation[key].hp == 5:
                return self.typeOnLocation[key].owner
        return -1

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