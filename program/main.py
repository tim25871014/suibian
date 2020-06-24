import pygame as pg
from elements import *
from gameplay import *
from network import *
from positioning import *
from moveRules import *

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
skill = SkillButton('skill.png', 'skill.png', 50, 590)
word_waiting = MessageBox('word_waiting.png', 113, 14)
word_opponent = MessageBox('word_opponent.png', 113, 14)
word_player = MessageBox('word_player.png', 262, 594)
focus = loadimg('focus.png')
textbox = TextBox(140, 459)

# gameplay
brd = ChessBoard()
isFirst = False
isYourTurn = True
skillReleased = False
selected = 0
selected2 = 0
onFocus = (-1, -1)
onFirst = (-1, -1)

# program
Program = True
Stage = 'Lobby' # 'Lobby', 'EnterCode', 'ShowRules', 'WaitingConnection', 'GameStart'
Step = 'Focus' # 'Waiting', 'Focus', 'First', 'Second', 'Third', 'Forth'

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
            network.send(brd)
            Stage = 'WaitingBoard'
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Program = False
    elif Stage == 'WaitingBoard':
        setbackground('board.png', screen)
        word_opponent.render(screen)
        word_player.render(screen)
        pg.display.update()
        isConnected = network.load() # get 0 if opponent connected
        if(isConnected == 0):
            print("ok1")
            brd = network.load()
            print("ok2")
            Stage = 'Gamestart'
            if isFirst:
                Step = 'Focus'
            else:
                Step = 'OppoMove'

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Program = False
    elif Stage == 'Gamestart':

        setbackground('board.png', screen)
        word_opponent.render(screen)
        word_player.render(screen)

        if Step == 'Waiting':
            onFocus = (-1, -1)
            onFirst = (-1, -1)
            skillReleased = False
            network.send(brd)
            Step = 'OppoMove'
        
        elif Step == 'OppoMove':
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    Program = False
            if network.load() == 0:
                brd = network.load()
            Step = 'Focus'

        elif Step == 'Focus':
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    Program = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouseloc = pg.mouse.get_pos()
                    selected = brd.stoneOnLocation(nearest_point(mouseloc))
                    onFocus = nearest_point(mouseloc)
            if onFocus[0] != -1 and selected != 0 and (selected.owner == 0 or not selected.isActive):
                if not selected.isActive:
                    a = 1
                    # open the covered stone
                    brd.makeMove(Move(onFocus, 'no', 0, [], 0))
                    Step = 'Waiting'
                else:
                    Step = 'First'

        elif Step == 'First':
            screen.blit(focus, coor_of_point(onFocus))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    Program = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouseloc = pg.mouse.get_pos()
                    skillReleased = skill.isInArea(mouseloc)
                    selected2 = brd.stoneOnLocation(nearest_point(mouseloc))
                    onFirst = nearest_point(mouseloc)
            
            skill.render(screen)

            if onFirst == onFocus:
                onFocus = (-1, -1)
                onFirst = (-1, -1)
                skillReleased = False
                Step = 'Focus'

            if onFirst[0] != -1 or onFirst[1] != -1 or skillReleased:

                if selected.type == 'king':
                    if che_can_move(onFocus, onFirst, brd):
                        if selected2 == 0:
                            # move selected to selected2
                            brd.makeMove(Move(onFocus, 'no', onFirst, [], 0))
                            Step = 'Waiting'
                        elif selected2.owner == 1:
                            # eat the selected2 (can be covered)
                            brd.makeMove(Move(onFocus, 'no', onFirst, [], 0))
                            Step = 'Waiting'
                elif selected.type == 'shi':
                    if onFirst[0] == -1 and onFirst[1] >= 8:
                        if brd.deathcount[onFirst[1] - 8] >= 1:
                            # summon
                            Step == 'Second'
                    elif shi_can_move(onFocus, onFirst):
                        if selected2 == 0:
                            # move selected to selected2
                            brd.makeMove(Move(onFocus, 'no', onFirst, [], 0))
                            Step = 'Waiting'
                elif selected.type == 'swordman':
                    if sword_can_kill(onFocus, onFirst) and selected2 != 0:
                        print('a')
                        if selected2.owner == 1:
                            ###########333 >>>>>>>>> ?????????????????????????????????????????????????????????????????????????????????????/
                            ###########333 >>>>>>>>> ?????????????????????????????????????????????????????????????????????????????????????/
                            ###########333 >>>>>>>>> ?????????????????????????????????????????????????????????????????????????????????????/
                            ###########333 >>>>>>>>> ?????????????????????????????????????????????????????????????????????????????????????/
                            ###########333 >>>>>>>>> ?????????????????????????????????????????????????????????????????????????????????????/
                            brd.makeMove(Move(onFocus, 'no', onFirst, [], 0))
                            Step = 'Waiting'
                    elif shi_can_move(onFocus, onFirst):
                        if selected2 == 0:
                            # move selected to selected2
                            brd.makeMove(Move(onFocus, 'no', onFirst, [], 0))
                            Step = 'Waiting'
                elif selected.type == 'xiang':
                    if selected.hp == 2:
                        if skillReleased:
                            # rush (WIP)
                            Step = 'Second'
                        elif xiang2_can_move(onFocus, onFirst):
                            if selected2 == 0:
                                # move selected to selected2
                                brd.makeMove(Move(onFocus, 'no', onFirst, [], 0))
                                Step = 'Waiting'

                            elif selected2.owner == 1 and selected2.isActive:
                                # eat the selected 2
                                brd.makeMove(Move(onFocus, 'no', onFirst, [], 0))
                                Step = 'Waiting'
                    elif selected.hp == 1:
                        if skillReleased:
                            # recover
                            brd.makeMove(Move(onFocus, 'skill', 0, [onFocus], 0))
                            Step = 'Waiting'
                        elif xiang1_can_move(onFocus, onFirst):
                            if selected2 == 0:
                                # move selected to selected2
                                brd.makeMove(Move(onFocus, 'no', onFirst, [], 0))
                                Step = 'Waiting'
                            elif selected2.owner == 1 and selected2.isActive:
                                # eat the selected 2
                                brd.makeMove(Move(onFocus, 'no', onFirst, [], 0))
                                Step = 'Waiting'
                elif selected.type == 'che':
                    if che_can_move(onFocus, onFirst, brd):
                        if selected2 == 0:
                            # move selected to selected2
                            brd.makeMove(Move(onFocus, 'no', onFirst, [], 0))
                            Step = 'Waiting'
                        elif selected2.owner == 1 and selected2.isActive:
                            # eat the selected 2
                            brd.makeMove(Move(onFocus, 'no', onFirst, [], 0))
                            Step = 'Waiting'
                        elif selected2.owner == 0 and selected2.type == 'ma':
                            # make chema
                            brd.makeMove(Move(onFocus, 'no', onFirst, [], 0))
                            Step = 'Waiting'
                elif selected.type == 'ma':
                    if ma_can_move(onFocus, onFirst):
                        if selected2 == 0:
                            # move selected to selected2
                            brd.makeMove(Move(onFocus, 'no', onFirst, [], 0))
                            Step = 'Waiting'
                        elif selected2.owner == 1 and selected2.isActive:
                            # eat the selected 2
                            brd.makeMove(Move(onFocus, 'no', onFirst, [], 0))
                            Step = 'Waiting'
                        elif selected2.owner == 0 and selected2.type == 'che':
                            # make mache
                            brd.makeMove(Move(onFocus, 'no', onFirst, [], 0))
                            Step = 'Waiting'
                elif selected.type == 'pao':
                    if soldier_can_move(onFocus, onFirst):
                        if selected2 == 0:
                            # move selected to selected2
                            brd.makeMove(Move(onFocus, 'no', onFirst, [], 0))
                            Step = 'Waiting'
                    elif shi_can_move(onFocus, onFirst):
                        if selected2 != 0 and selected2.owner == 0 and selected2.isActive:
                            # select bomb (WIP)
                            Step = 'Second'
                elif selected.type == 'soldier':
                    if skillReleased:
                        # sacrisfy
                        Step = 'Second'
                    elif selected2 != 0 and selected2.owner == 0 and selected2.type == 'soldier' and selected2.isActive:
                        # teleport
                        Step = 'Second'
                    elif soldier_can_move(onFocus, onFirst):
                        if selected2 == 0:
                            # move selected to selected2
                            brd.makeMove(Move(onFocus, 'no', onFirst, [], 0))
                            Step = 'Waiting'
                        elif selected2.owner == 1 and selected2.isActive:
                            # eat the selected 2
                            brd.makeMove(Move(onFocus, 'no', onFirst, [], 0))
                            Step = 'Waiting'

        elif Step == 'Second':
             for event in pg.event.get():
                if event.type == pg.QUIT:
                    Program = False
        print("ewvwe")
        brd.render(screen)
        pg.display.update()

    main_clock.tick(FPS)
    
pg.quit()

