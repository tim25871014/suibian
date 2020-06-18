import pygame as pg
from elements import *

background = loadimg('start.png')
board = loadimg('board.png')
multi = StartingButton('multi.png', 'multi_act.png', 44, 270)
single = StartingButton('single.png', 'single_act.png', 44, 380)
rules = StartingButton('rules.png', 'rules_act.png', 44, 490)
hintbox = MessageBox('entercode.png', 44, 240)
hintcancel = RoundButton('cross.png', 'cross_act.png', 50, 241)
textbox = TextBox(140, 459)

Program = True
isFirst = False
Stage = 'Lobby' # 'Lobby', 'EnterCode', 'ShowRules', 'WaitingConnection', 'GameStart'

while Program:

    if Stage == 'Lobby':
        screen.blit(background, (0, 0))
        multi.render()
        single.render()
        rules.render()
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

    elif Stage == 'EnterCode':
        screen.blit(background, (0, 0))
        hintbox.render()
        hintcancel.render()
        textbox.render()
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
        screen.blit(board, (0, 0))
        pg.display.update()
        isConnected = network.load()
        print(isConnected) # get 0, or -1 for no opponent connected
        if(isConnected == 0):
            isFirst = network.load()
            print('8888888')
            Stage = 'Gamestart'
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Program = False
    elif Stage == 'Gamestart':
        screen.blit(board, (0, 0))
        print(isFirst)
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Program = False

    main_clock.tick(FPS)
    
pg.quit()
