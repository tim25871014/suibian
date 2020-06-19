import pygame as pg
from elements import *
from gameplay import *
from network import *
from positioning import *

# settings
FPS = 60
pg.init()
main_clock = pg.time.Clock()
width, height = 522, 675  # fixed
screen = pg.display.set_mode((width, height))
pg.display.set_caption('Wang Zheng Chess DX')

# connection
network = Network()

# elements
background = loadimg('start.png')
board = loadimg('board.png')
multi = StartingButton('multi.png', 'multi_act.png', 44, 270)
single = StartingButton('single.png', 'single_act.png', 44, 380)
rules = StartingButton('rules.png', 'rules_act.png', 44, 490)
hintbox = MessageBox('entercode.png', 44, 240)
hintcancel = RoundButton('cross.png', 'cross_act.png', 50, 241)
word_waiting = MessageBox('word_waiting.png', 113, 14)
word_opponent = MessageBox('word_opponent.png', 113, 14)
word_player = MessageBox('word_player.png', 262, 594)
focus = loadimg('focus.png')
textbox = TextBox(140, 459)

# gameplay
brd = ChessBoard()
isFirst = False
isYourTurn = True
selected = 0
onFocus = (-1, -1)

# program
Program = True
Stage = 'Lobby' # 'Lobby', 'EnterCode', 'ShowRules', 'WaitingConnection', 'GameStart'

while Program:

    if Stage == 'Lobby':
        setbackground('start.png', screen)
        multi.render(screen)
        single.render(screen)
        rules.render(screen)
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Program = False
            if event.type == pg.MOUSEMOTION:
                mouseloc = pg.mouse.get_pos()
                hintcancel.isActive = False
                multi.isActive = multi.isInArea(mouseloc)
                single.isActive = single.isInArea(mouseloc)
                rules.isActive = rules.isInArea(mouseloc)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if multi.isActive:
                    Stage = 'EnterCode'
                if rules.isActive:
                    Stage = 'ShowRules'
                if single.isActive:
                    ThisFeature = 'WIP'
                    print(ThisFeature)
    elif Stage == 'ShowRules':
        screen.blit(background, (0, 0))
        hintbox.render(screen)
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Program = False
                
    elif Stage == 'EnterCode':
        setbackground('start.png', screen)
        hintbox.render(screen)
        hintcancel.render(screen)
        textbox.render(screen)
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Program = False
            if event.type == pg.MOUSEMOTION:
                mouseloc = pg.mouse.get_pos()
                multi.isActive = single.isActive = rules.isActive = False
                hintcancel.isActive = hintcancel.isInArea(mouseloc)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if hintcancel.isActive:
                    textbox.reset()
                    Stage = 'Lobby'
            elif event.type == pg.KEYDOWN:
                textbox.add_chr(pg.key.name(event.key))
                if event.key == pg.K_BACKSPACE:
                    textbox.del_chr()
                if event.key == pg.K_RETURN:
                    # connect to server and start game
                    if len(textbox.text) > 0 and textbox.isvaild():
                        network.send(textbox.text)
                        Stage = 'WaitingConnection'
    elif Stage == 'WaitingConnection':
        setbackground('board.png', screen)
        word_waiting.render(screen)
        word_player.render(screen)
        pg.display.update()
        isConnected = network.load() # get 0 if opponent connected
        if(isConnected == 0):
            isFirst = network.load()
            Stage = 'Gamestart'
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Program = False
    elif Stage == 'Gamestart':
        # isFirst
        setbackground('board.png', screen)
        word_opponent.render(screen)
        word_player.render(screen)

        if onFocus != (-1, -1):
            screen.blit(focus, coor_of_point(onFocus))

        brd.render(screen)
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Program = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouseloc = pg.mouse.get_pos()
                if onFocus == nearest_point(mouseloc):
                    selected = 0
                    onFocus = (-1, -1)
                else:
                    selected = brd.stoneOnLocation(nearest_point(mouseloc))
                    onFocus = nearest_point(mouseloc)
                    print(selected)

    main_clock.tick(FPS)
    
pg.quit()
