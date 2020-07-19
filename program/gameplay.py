from positioning import *

# X pygame

# 'king', 'shi','swordman', 'xiang', 'che', 'ma', 'pao', 'soldier, 'mache','chema'
class Stone:
    def __init__(self, stype, hp, owner, isActive):
        self.type = stype
        self.hp = hp
        self.owner = owner
        self.isActive = isActive

class Move:
    def __init__(self, location, action, dest, objects, summon):
        self.location = location 
        self.action = action
        self.dest = dest
        self.objects = objects
        self.summon = summon

class ChessBoard:
    def __init__(self):
        self.typeOnLocation = {}
        self.lastLocation = [(-1,-1), (-1, -1)]
        self.lastUsed = [[],[]]
        self.steps = [0,0]
        self.shiNum = [0,0]
        self.gaveUp = 0
        self.xianRecover = [(-1,-1), (-1, -1)]
        self.peace = 0
        self.namelist = ['king', 'shi', 'swordman', 'xiang', 'che', 'ma', 'pao', 'soldier']
        self.deathCount = [
            {'king': 1, 'shi': 1, 'swordman': 1, 'xiang': 2, 'che': 2, 'ma': 2, 'pao': 2, 'soldier': 5},
            {'king': 0, 'shi': 0, 'swordman': 0, 'xiang': 0, 'che': 0, 'ma': 0, 'pao': 0, 'soldier': 0}
        ]
    def merge_and_hide(self, other):
        self.typeOnLocation.update(other.typeOnLocation)
        for idx in self.typeOnLocation:
            self.typeOnLocation[idx].isActive = False
            if self.typeOnLocation[idx].type == 'swordman':
                self.typeOnLocation[idx].type = 'shi'
    def swap_vision(self):
        tmp = {}
        for idx in self.typeOnLocation:
            s = self.typeOnLocation[idx]
            s.owner = 1 - s.owner
            tmp[(8 - idx[0], 9 - idx[1])] = self.typeOnLocation[idx]
        self.deathCount[0], self.deathCount[1] = self.deathCount[1], self.deathCount[0]
        self.shiNum[0], self.shiNum[1] = self.shiNum[1], self.shiNum[0]
        self.steps[0], self.steps[1] = self.steps[1], self.steps[0]
        self.lastUsed[0], self.lastUsed[1] = self.lastUsed[1], self.lastUsed[0]
        
        temp = self.lastLocation[0]
        self.lastLocation[0] = self.lastLocation[1]
        self.lastLocation[1] = (8 - temp[0], 9 - temp[1])
        
        self.typeOnLocation = tmp

        #self.xianRecover[0], self.xianRecover[1] = self.xianRecover[1], self.xianRecover[0]
    def stoneOnLocation(self, loc):
        if self.typeOnLocation.__contains__(loc):
            return self.typeOnLocation[loc]
        else:
            return 0
    def isLegal(self, move):
        a = 1
    def kill(self, locate, source):
        if locate not in self.typeOnLocation:
            return
        self.peace = 0
        st = self.typeOnLocation[locate]
        if st.isActive == 0 and st.type == 'shi':
            self.shiNum[st.owner] += 1
            if self.shiNum[st.owner] == 2:
                st.type = 'swordman'
        
        if st.type == 'soldier':
            self.deathCount[self.typeOnLocation[locate].owner][st.type] += st.hp
        elif st.type == 'mache' or st.type == 'chema':
            self.deathCount[self.typeOnLocation[locate].owner]['che']+= 1
            self.deathCount[self.typeOnLocation[locate].owner]['ma']+= 1
        else:
            self.deathCount[self.typeOnLocation[locate].owner][st.type] += 1
        del self.typeOnLocation[locate]
        if st.type == 'king':
            self.kill(source, source)
        if st.type == 'xiang' and locate == self.xianRecover[1]:
            self.xianRecover[1] = (-1,-1)

    def hurt(self, locate, source):
        if locate not in self.typeOnLocation:
            return False
        self.peace = 0
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
    def open(self, locate):
        self.typeOnLocation[locate].isActive = 1
        if self.typeOnLocation[locate].type == 'shi':
            self.shiNum[self.typeOnLocation[locate].owner] += 1
            if self.shiNum[self.typeOnLocation[locate].owner] == 2:
                self.typeOnLocation[locate].type = 'swordman'
    def transfer(self, locate1, locate2):
        if locate1 == locate2:
            return
        if locate1 in self.typeOnLocation:
            self.typeOnLocation[locate2] = self.typeOnLocation[locate1]
            del self.typeOnLocation[locate1]
    def inside(self,locate):
        if locate[0] >= 0 and locate[0] < 10 and locate[1] >= 0 and locate[0] < 9:
            return True
        return False

    def makeMove(self, move):#void
        if move.location[0] == -1:
            self.deathCount[0][move.summon.type] -= 1
            self.typeOnLocation[move.dest] = move.summon
            return
        #if self.xianRecover[1][0] >= 0:
        #    self.typeOnLocation[self.xianRecover[1]].hp += 1
        self.xianRecover[1] = (8-self.xianRecover[0][0],9-self.xianRecover[0][1])
        if self.xianRecover[1][0] >= 9:
            self.xianRecover[1] = (-1,-1)
        self.xianRecover[0] = (-1,-1)
        if move.location not in self.typeOnLocation:
            return
        self.peace += 1
        st = self.typeOnLocation[move.location]
        
        if st.isActive == 0:
            self.open(move.location)
            self.steps[0] = 0
            self.lastLocation[0] = move.location
            if self.xianRecover[1][0] >= 0:
                self.typeOnLocation[self.xianRecover[1]].hp += 1
            return
        if move.action == 'skill':
            self.steps[0] = 0
            
            if st.type == 'soldier':
                self.lastLocation[0] = move.location
                if move.objects[0] == move.location:
                    self.deathCount[self.typeOnLocation[move.location].owner][st.type] += st.hp
                    self.deathCount[self.typeOnLocation[move.location].owner][move.summon.type] -= 1
                    #self.kill(move.locate)
                    self.typeOnLocation[move.location] = move.summon
                else:
                    self.transfer(move.objects[0],move.dest)
            elif st.type == 'xiang':
                if move.objects != [] and move.objects[0] == move.location:
                    self.xianRecover[0] = move.location
                    self.lastLocation[0] = move.location
                else:
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
                    self.lastLocation[0] = move.dest
            elif st.type == 'king':
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
                self.lastLocation[0] = move.dest
            elif st.type == 'shi':
                self.deathCount[self.typeOnLocation[move.location].owner][move.summon.type] -= 1
                self.typeOnLocation[move.dest] = move.summon
                self.lastLocation[0] = move.location
            elif st.type == 'swordman':
                self.kill(move.dest, move.location)
                self.lastLocation[0] = move.location
            elif st.type == 'pao':
                self.kill(move.objects[0],move.location)
                self.lastLocation[0] = move.location
                nx = (move.dest[0] - move.location[0])
                ny = (move.dest[1] - move.location[1])
                if nx != 0:
                    nx /= abs(nx)
                if ny != 0:
                    ny /= abs(ny)
                #self.kill(move.dest,move.location)
                #self.kill((move.dest[0]+nx,move.dest[1]+ny),move.location)
                
                self.kill(move.dest,move.location)
                if self.inside((move.dest[0]+nx,move.dest[1]+ny)):
                    self.kill((move.dest[0]+nx,move.dest[1]+ny),move.location)
                if nx == 0:
                    if self.inside((move.dest[0]-1,move.dest[1])):
                        self.kill((move.dest[0]-1,move.dest[1]),move.location)
                    if self.inside((move.dest[0]+1,move.dest[1])):
                        self.kill((move.dest[0]+1,move.dest[1]),move.location)
                else:
                    if self.inside((move.dest[0],move.dest[1]-1)):
                        self.kill((move.dest[0],move.dest[1]-1),move.location)
                    if self.inside((move.dest[0],move.dest[1]+1)):
                        self.kill((move.dest[0],move.dest[1]+1),move.location)
        else:
            nx = (move.dest[0] - move.location[0])
            ny = (move.dest[1] - move.location[1])
            if nx != 0:
                nx /= abs(nx)
            if ny != 0:
                ny /= abs(ny)
            if move.dest in self.typeOnLocation and self.typeOnLocation[move.dest].owner != self.typeOnLocation[move.location].owner:
                self.steps[0] = 0
                if st.type == 'king':
                    if self.typeOnLocation[move.dest].owner == st.owner:
                        self.transfer(move.location,(move.dest[0]-nx,move.dest[1]-ny))
                        self.lastLocation[0] = (move.dest[0]-nx,move.dest[1]-ny)
                        if self.xianRecover[1][0] >= 0:
                            self.typeOnLocation[self.xianRecover[1]].hp += 1
                        return
                    die = self.typeOnLocation[move.dest]
                    self.kill(move.dest,move.location)
                    if die.isActive == 0:
                        if die.type == 'shi' and self.shiNum[st.owner] == 0:
                            self.kill(move.location,move.location)
                    self.transfer(move.location,move.dest)
                    self.lastLocation[0] = move.dest
                elif st.type == 'che':
                    if self.hurt(move.dest,move.location):
                        self.transfer(move.location,move.dest)
                        self.lastLocation[0] = move.dest
                    else:
                        self.transfer(move.location,(move.dest[0]-nx,move.dest[1]-ny))
                        self.lastLocation[0] = (move.dest[0]-nx,move.dest[1]-ny)
                elif st.type == 'chema' or st.type == 'mache':
                    if self.hurt(move.dest,move.location):
                        self.transfer(move.location,move.dest)
                        self.lastLocation[0] = move.dest
                        if self.xianRecover[1][0] >= 0:
                            self.typeOnLocation[self.xianRecover[1]].hp += 1
                        return
                    elif self.hurt(move.dest,move.location):
                        self.transfer(move.location,move.dest)
                        self.lastLocation[0] = move.dest
                        if self.xianRecover[1][0] >= 0:
                            self.typeOnLocation[self.xianRecover[1]].hp += 1
                        return
                    elif move.location[0] == move.dest[0] or move.location[1] == move.dest[1]:
                        self.transfer(move.location,(move.dest[0]-nx,move.dest[1]-ny))
                        self.lastLocation[0] = (move.dest[0]-nx,move.dest[1]-ny)
                    else:
                        self.lastLocation[0] = move.location
                elif st.type == 'soldier':
                    for i in range(0,st.hp):
                        if self.hurt(move.dest,move.location):
                            self.transfer(move.location,move.dest)
                            self.lastLocation[0] = move.dest
                            if self.xianRecover[1][0] >= 0:
                                self.typeOnLocation[self.xianRecover[1]].hp += 1
                            return
                    self.lastLocation[0] = move.location
                elif st.type == 'xiang' and st.hp == 2:
                    if self.hurt(move.dest,move.location):
                        self.transfer(move.location,move.dest)
                        self.lastLocation[0] = move.dest
                        if self.xianRecover[1][0] >= 0:
                            self.typeOnLocation[self.xianRecover[1]].hp += 1
                        return
                    elif self.hurt(move.dest,move.location):
                        self.transfer(move.location,move.dest)
                        self.lastLocation[0] = move.dest
                        if self.xianRecover[1][0] >= 0:
                            self.typeOnLocation[self.xianRecover[1]].hp += 1
                        return
                    self.lastLocation[0] = move.location
                else:
                    if self.hurt(move.dest,move.location):
                        self.transfer(move.location,move.dest)
                        self.lastLocation[0] = move.dest
                    else:
                        self.lastLocation[0] = move.location
            elif move.dest not in self.typeOnLocation:
                self.transfer(move.location,move.dest)
                if move.location == self.lastLocation[0]:
                    self.steps[0] += 1
                else:
                    self.steps[0] = 1
                self.lastLocation[0] = move.dest
                
            else:
                self.steps[0] = 0
                if st.type == 'soldier':
                    self.typeOnLocation[move.dest].hp += 1
                    del self.typeOnLocation[move.location]
                elif st.type == 'ma':
                    self.typeOnLocation[move.dest].type = 'mache'
                    del self.typeOnLocation[move.location]
                elif st.type == 'che':
                    self.typeOnLocation[move.dest].type = 'chema'
                    del self.typeOnLocation[move.location]
                self.lastLocation[0] = move.dest
        if self.xianRecover[1][0] >= 0:
            self.typeOnLocation[self.xianRecover[1]].hp += 1
    def isWin(self):
        if self.deathCount[0]['soldier'] >= 5:
            return 1
        if self.deathCount[1]['soldier'] >= 5:
            return 0
        for key in self.typeOnLocation:
            if self.typeOnLocation[key].hp == 5:
                return self.typeOnLocation[key].owner
        if self.peace >= 25:
            return 2
        return -1
