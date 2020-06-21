# location of square (x, y) is (33 + x * 49.375, 86 + y * 49.666)
# size of the stone = (58, 58)
# half of the size of the stone = (29, 29)
# the border of board is from (8.5, 61.5) to ()

def center_of_point(point):
    return (62 + point[0] * 49.375, 115 + point[1] * 49.666)

def coor_of_point(point):
    return (33 + point[0] * 49.375, 86 + point[1] * 49.666)

def center_of_grave_op(point):
    return (99 + 15.5 + point*28, 49 + 15.5)

def center_of_grave_pl(point):
    return (196 + 15.5 + point*28, 635 + 15.5)

def coor_of_grave_op(point):
    return (99 + point*28, 49)

def coor_of_grave_pl(point):
    return (196 + point*28, 635)

def type_of_grave(t):
    res = ['king', 'shi', 'swordman', 'xiang', 'che', 'ma', 'pao', 'soldier']
    return res[t]


# op: 0  1  2  3  4  5  6  7
# pl: 8  9 10 11 12 13 14 15
def nearest_grave(pos):
    lim = 15
    if pos[1] <= 64.5 + lim and pos[1] >= 64.5 - lim:
        x = round((pos[0] - 115.5) / 28)
        if x > 7 or x < 0:
            return (-1, -1)
        trueloc = center_of_grave_op(x)
        if ((pos[0] - trueloc[0]) ** 2 + (pos[1] - trueloc[1]) ** 2) <= lim ** 2:
            return (-1, x)
    elif pos[1] <= 650.5 + lim and pos[1] >= 650.5 - lim:
        x = round((pos[0] - 211.5) / 28)
        if x > 7 or x < 0:
            return (-1, -1)
        trueloc = center_of_grave_pl(x)
        if ((pos[0] - trueloc[0]) ** 2 + (pos[1] - trueloc[1]) ** 2) <= lim ** 2:
            return (-1, x + 8)
    return (-1, -1)



def nearest_point(pos):
    x = round((pos[0] - 62) / 49.375)
    y = round((pos[1] - 115) / 49.666)
    trueloc = center_of_point((x, y))
    if x < 0 or y < 0:
        return (-1, -1)
    if x > 8 or y > 9:
        return (-1, -1)
    elif ((pos[0] - trueloc[0]) ** 2 + (pos[1] - trueloc[1]) ** 2) <= 625:
        return (x, y)
    else:
        # every points are too far away
        return nearest_grave(pos)
