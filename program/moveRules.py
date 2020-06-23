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