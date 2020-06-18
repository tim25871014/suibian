import pygame

class Sit():
    def __init__(self):
        self.stage = 0
        self.board = [[],[]]
        self.step = [((0,0),(0,0)),((0,0),(0,0))]
        """
        0 -> one player
        1 -> two players
        2 -> one player finished placing
        3 -> two players finished placing
        4 -> First player's turn
        5 -> second player's turn
        6 -> game ended
        """