# location of square (x, y) is (33 + x * 49.375, 86 + y * 49.666)
# size of the stone = (58, 58)
# half of the size of the stone = (29, 29)
# the border of board is from (8.5, 61.5) to ()

def center_of_point(point):
    return (62 + point[0] * 49.375, 115 + point[1] * 49.666)

def coor_of_point(point):
    return (33 + point[0] * 49.375, 86 + point[1] * 49.666)

def nearest_point(pos):
    x = round((pos[0] - 62) / 49.375)
    y = round((pos[1] - 115) / 49.666)
    trueloc = center_of_point((x, y))
    if x < 0 or y < 0:
        return (-1, -1)
    elif ((pos[0] - trueloc[0]) ** 2 + (pos[1] - trueloc[1]) ** 2) <= 625:
        return (x, y)
    else:
        # every points are too far away
        return (-1, -1)