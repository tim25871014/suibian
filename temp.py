# 'king', 'shi','swordman', 'xiang', 'che', 'ma', 'pao', 'soldier, 'mache','chema'
class Stone:
    def __init__(self, stype, hp, owner, isActive):
        self.stype = stype
        self.hp = hp
        self.owner = owner
        self.isActive = isActive      

class Move:
    def __init__(self, location, action, dest, objects,summon):
        self.location = location # 要做事的棋的座標
        self.action = action # 要做的事 ('move', 'skill')
        self.dest = dest # 要移動到、發動技能的座標
        self.objects = objects # 要犧牲的棋座標 (座標 list)
        self.summon = summon # 要召喚的棋(stone)

class ChessBoard:
    def __init__(self):
        self.typeOnLocation = {} # map 座標 -> Stone
        self.shiNum = 0
        self.xianRecover = (-1,-1)
        self.deathCount = [
            {'king': 1, 'shi': 2, 'xiang': 2, 'che': 2, 'ma': 2, 'pao': 2, 'soldier': 5},
            {'king': 1, 'shi': 2, 'xiang': 2, 'che': 2, 'ma': 2, 'pao': 2, 'soldier': 5}
        ] # list dict(死亡棋種 -> int)
    def isLegal(self, move):
        # 1
    def makeMove(self, move):
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




    def isWin(self):
        # 3