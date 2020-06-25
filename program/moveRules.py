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