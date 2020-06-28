import random

def che_can_move(onFocus, onFirst, brd):
    isLegal = False
    if onFocus[0] == onFirst[0] or onFocus[1] == onFirst[1]:
        isLegal = True
        if onFocus[1] == onFirst[1]:
            small = min(onFocus[0], onFirst[0]) + 1
            big = max(onFocus[0], onFirst[0])
            for i in range(small, big):
                if brd.stoneOnLocation((i, onFocus[1])) != 0:
                    isLegal = False
        elif onFocus[0] == onFirst[0]:
            small = min(onFocus[1], onFirst[1]) + 1
            big = max(onFocus[1], onFirst[1])
            for i in range(small, big):
                if brd.stoneOnLocation((onFocus[0], i)) != 0:
                    isLegal = False
    return isLegal

def ma_can_move(onFocus, onFirst):
    return (abs(onFocus[0] - onFirst[0]) == 1 and abs(onFocus[1] - onFirst[1]) == 2) or (abs(onFocus[0] - onFirst[0]) == 2 and abs(onFocus[1] - onFirst[1]) == 1)

def soldier_can_move(onFocus, onFirst):
    return (abs(onFocus[0] - onFirst[0]) == 1 and onFocus[1] == onFirst[1]) or (onFocus[0] == onFirst[0] and abs(onFocus[1] - onFirst[1]) == 1)

def xiang2_can_move(onFocus, onFirst):
    return abs(onFocus[0] - onFirst[0]) == abs(onFocus[1] - onFirst[1]) and abs(onFocus[1] - onFirst[1]) <= 2

def xiang1_can_move(onFocus, onFirst):
    return abs(onFocus[0] - onFirst[0]) == abs(onFocus[1] - onFirst[1]) and abs(onFocus[1] - onFirst[1]) <= 1

def shi_can_move(onFocus, onFirst):
    return soldier_can_move(onFocus, onFirst) or xiang1_can_move(onFocus, onFirst)

def sword_can_kill(onFocus, onFirst):
    return abs(onFocus[0] - onFirst[0]) + abs(onFocus[1] - onFocus[1]) <= 2

def bomb_can_reach(onFocus, onFirst, onSecond, brd):
    isLegal = False
    if onFocus[1] == onSecond[1]:
        small = min(onFocus[0], onSecond[0]) + 1
        big = max(onFocus[0], onSecond[0])
        for i in range(small, big):
            if brd.stoneOnLocation((i, onFocus[1])) != 0 and (i, onFocus[1]) != onFirst:
                isLegal = True
    elif onFocus[0] == onSecond[0]:
        small = min(onFocus[1], onSecond[1]) + 1
        big = max(onFocus[1], onSecond[1])
        for i in range(small, big):
            if brd.stoneOnLocation((onFocus[0], i)) != 0 and (i, onFocus[1]) != onFirst:
                isLegal = True
    return isLegal

def king_can_rush(onFocus, onForth):
    isLegal = False
    if(onFocus[0] == onForth[0]):
        if onForth[1] == 0 or onForth[1] == 9:
            isLegal = True
    else:
        if onForth[0] == 0 or onForth[0] == 8:
            isLegal = True
    if onFocus == onForth:
        isLegal = False
    return isLegal

def rnd_put(brd):
    x = random.randint(0, 8)
    y = random.randint(0, 9)
    while brd.stoneOnLocation((x, y)) != 0 or x == 4 or y < 6:
        x = random.randint(0, 8)
        y = random.randint(0, 9)
    return x, y

def inside(location):
    if location[0] >= 0 and location[0] < 9 and location[1] >= 0 and location[1] < 10:
        return True
    return False

def nothing(brd, location):
    if inside(location) and brd.stoneOnLocation(location) == 0:
        return True
    return False

def shi_can_summon(brd,location):
    return nothing((location[0],location[1]-1)) or nothing((location[0],location[1]+1)) or nothing((location[0]-1,location[1])) or nothing((location[0]+1,location[1])) or nothing((location[0]-1,location[1]-1)) or nothing((location[0]-1,location[1]+1)) or nothing((location[0]+1,location[1]-1)) or nothing((location[0]+1,location[1]+1))

def king_can_rush(brd):
    cnt = 0
    for i in range(0,9):
        for j in range(0,10):
            temp = brd.stoneOnLocation((i,j))
            if temp != 0 and temp.owner == 0 and temp.isActive == 1:
                cnt += 1
    return cnt >= 3

def pao_can_shoot(brd,pao_location,pao_dan):
    ret = False
    can_jump = False
    for i in range(1,10):
        now = (pao_location[0] + i,pao_location[1])
        if not inside(now):
            break
        if now == pao_dan:
            continue
        temp = brd.stoneOnLocation(now)
        if can_jump and (temp == 0 or (temp.isActive == 1 and temp.owner == 1)):
            ret = True
        if brd.stoneOnLocation(now) != 0:
            can_jump = True

    can_jump = False
    for i in range(1,10):
        now = (pao_location[0] - i,pao_location[1])
        if not inside(now):
            break
        if now == pao_dan:
            continue
        temp = brd.stoneOnLocation(now)
        if can_jump and (temp == 0 or (temp.isActive == 1 and temp.owner == 1)):
            ret = True
        if brd.stoneOnLocation(now) != 0:
            can_jump = True
            
    can_jump = False
    for i in range(1,10):
        now = (pao_location[0],pao_location[1]+i)
        if not inside(now):
            break
        if now == pao_dan:
            continue
        temp = brd.stoneOnLocation(now)
        if can_jump and (temp == 0 or (temp.isActive == 1 and temp.owner == 1)):
            ret = True
        if brd.stoneOnLocation(now) != 0:
            can_jump = True

    can_jump = False
    for i in range(1,10):
        now = (pao_location[0],pao_location[1]-i)
        if not inside(now):
            break
        if now == pao_dan:
            continue
        temp = brd.stoneOnLocation(now)
        if can_jump and (temp == 0 or (temp.isActive == 1 and temp.owner == 1)):
            ret = True
        if brd.stoneOnLocation(now) != 0:
            can_jump = True
