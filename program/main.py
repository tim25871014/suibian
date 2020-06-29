import pygame as pg
from elements import *
from gameplay import *
from network import *
from positioning import *
from moveRules import *
from rendering import *

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
winbox = MessageBox('win.png', 50, 150)
drawbox = MessageBox('draw.png', 50, 150)
losebox = MessageBox('lose.png', 50, 150)
title = BackButton('title.png', 'title_act.png', 168, 386)
hintcancel = RoundButton('cross.png', 'cross_act.png', 50, 241)
skill = SkillButton('skill.png', 'skill.png', 50, 590)
word_waiting = MessageBox('word_waiting.png', 113, 14)
word_opponent = MessageBox('word_opponent.png', 113, 14)
word_player = MessageBox('word_player.png', 262, 594)
focus = loadimg('focus.png')
focus2 = loadimg('focus2.png')
textbox = TextBox(140, 459)

# gameplay
brd = ChessBoard()
isFirst = False
isYourTurn = True
skillReleased = False
selected = 0
selected2 = 0
selected3 = 0
selected4 = 0
selected5 = 0
onFocus = (-1, -1)
onFirst = (-1, -1)
onSecond = (-1, -1)
onThird = (-1, -1)
onForth = (-1, -1)

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
            t = network.load()
            isFirst = 1 - t
            Stage = 'DesigningBoard'
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Program = False

    elif Stage == 'DesigningBoard':
        setbackground('board.png', screen)
        word_opponent.render(screen)
        word_player.render(screen)
        skill.render(screen)

        if Step == 'Focus':
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    Program = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouseloc = pg.mouse.get_pos()
                    selected = brd.stoneOnLocation(nearest_point(mouseloc))
                    skillReleased = skill.isInArea(mouseloc)
                    onFocus = nearest_point(mouseloc)
            if onFocus[0] == -1 and onFocus[1] >= 8:
                if brd.deathCount[0][type_of_grave(onFocus)] >= 1:
                    print(onFocus)
                    Step = 'First'
            elif selected != 0 and selected.owner == 0:
                brd.kill(onFocus, (-1, -1))

        elif Step == 'First':

            pic = pg.transform.scale(focus, (31, 31))
            screen.blit(pic, coor_of_point(onFocus))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    Program = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouseloc = pg.mouse.get_pos()
                    selected2 = brd.stoneOnLocation(nearest_point(mouseloc))
                    skillReleased = skill.isInArea(mouseloc)
                    onFirst = nearest_point(mouseloc)
            
            if onFirst == onFocus:
                onFocus = (-1, -1)
                onFirst = (-1, -1)
                Step = 'Focus'
            elif selected2 == 0 and onFirst[0] != 4 and onFirst[0] != -1 and onFirst[1] >= 6:
                sum_type = type_of_grave(onFocus)
                sum_hp = 1
                if sum_type == 'xiang':
                    sum_hp = 2
                brd.makeMove(Move(onFocus, 'skill', onFirst, [], Stone(sum_type, sum_hp, 0, True)))
                onFocus = (-1, -1)
                onFirst = (-1, -1)
                Step = 'Focus'

        if skillReleased:
            for i in brd.deathCount[0]:
                for j in range(0, brd.deathCount[0][i]):
                    sum_type = i
                    sum_hp = 1
                    if sum_type == 'xiang':
                        sum_hp = 2
                    brd.makeMove(Move((-1, 0), 'skill', rnd_put(brd), [], Stone(sum_type, sum_hp, 0, False)))
            network.send(brd)
            onFocus = (-1, -1)
            onFirst = (-1, -1)
            Stage = 'WaitingBoard'
        
        render(brd, screen)
        pg.display.update()

    elif Stage == 'WaitingBoard':
        setbackground('board.png', screen)
        word_opponent.render(screen)
        word_player.render(screen)
        render(brd, screen)
        pg.display.update()
        isConnected = network.load() # get 0 if opponent finished
        if(isConnected == 0):
            oppo_brd = network.load()
            oppo_brd.swap_vision()
            brd.merge_and_hide(oppo_brd)
            Stage = 'Gamestart'
            if isFirst:
                Step = 'Focus'
            else:
                Step = 'OppoMove'

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Program = False
            
    elif Stage == 'Lose' or Stage == 'Win' or Stage == 'Draw':
        setbackground('board.png', screen)
        word_opponent.render(screen)
        word_player.render(screen)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Program = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if title.isActive:
                    Stage = 'Lobby'
                    brd = ChessBoard()
                    isFirst = False
                    isYourTurn = True
                    skillReleased = False
                    selected = 0
                    selected2 = 0
                    selected3 = 0
                    selected4 = 0
                    selected5 = 0
                    onFocus = (-1, -1)
                    onFirst = (-1, -1)
                    onSecond = (-1, -1)
                    onThird = (-1, -1)
                    onForth = (-1, -1)
                    Step = 'Focus'
            if event.type == pg.MOUSEMOTION:
                mouseloc = pg.mouse.get_pos()
                title.isActive = title.isInArea(mouseloc)
        render(brd, screen)
        if Stage == 'Lose':
            losebox.render(screen)
        elif Stage == 'Win':
            winbox.render(screen)
        elif Stage == 'Draw':
            drawbox.render(screen)
        title.render(screen)
        pg.display.update()

    elif Stage == 'Gamestart':
        setbackground('board.png', screen)
        word_opponent.render(screen)
        word_player.render(screen)
        if Step == 'Waiting':
            onFocus = (-1, -1)
            onFirst = (-1, -1)
            onSecond = (-1, -1)
            onThird = (-1, -1)
            onForth = (-1, -1)
            skillReleased = False
            network.send(brd)
            if brd.isWin() != -1:
                if brd.isWin() == 0:
                    Stage = 'Win'
                elif brd.isWin() == 1:
                    Stage = 'Lose'
                else:
                    Stage = 'Draw'
                
            Step = 'OppoMove'
        
        elif Step == 'OppoMove':
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    Program = False
            t = network.load()
            if t == 0:
                brd = network.load()
                brd.swap_vision()
                if brd.isWin() != -1:
                    if brd.isWin() == 0:
                        Stage = 'Win'
                    elif brd.isWin() == 1:
                        Stage = 'Lose'
                    else:
                        Stage = 'Draw'
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                    network.send('disconnected')
=======
                    #network.send('finished')
                    network.send('finished')
>>>>>>> parent of f856f6c... modify win/lose/draw
=======
                    network.send('finished')
>>>>>>> parent of 352566b... Update main.py
=======
                    network.send('finished')
>>>>>>> parent of 352566b... Update main.py
=======
                    network.send('disconnected')
>>>>>>> parent of 7fa9c51... merge and commit
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
                    brd.makeMove(Move(onFocus, 'move', 0, [], 0))
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
                    if skillReleased and king_can_rush2(brd):
                            # rush (WIP)
                            Step = 'Second'
                    elif che_can_move(onFocus, onFirst, brd):
                        if selected2 == 0:
                            # move selected to selected2
                            brd.makeMove(Move(onFocus, 'move', onFirst, [], 0))
                            Step = 'Waiting'
                        elif selected2.owner == 1:
                            # eat the selected2 (can be covered)
                            brd.makeMove(Move(onFocus, 'move', onFirst, [], 0))
                            Step = 'Waiting'
                elif selected.type == 'shi':
                    if onFirst[0] == -1 and onFirst[1] >= 9 and shi_can_summon(brd,onFocus): # can't be 8 (king)
                        if brd.deathCount[0][type_of_grave(onFirst)] >= 1:
                            # summon
                            Step = 'Second'
                    elif shi_can_move(onFocus, onFirst):
                        if selected2 == 0:
                            # move selected to selected2
                            brd.makeMove(Move(onFocus, 'move', onFirst, [], 0))
                            Step = 'Waiting'
                elif selected.type == 'swordman':
                    if sword_can_kill(onFocus, onFirst) and selected2 != 0:
                        if selected2.owner == 1:
                            brd.makeMove(Move(onFocus, 'skill', onFirst, [], 0))
                            Step = 'Waiting'
                    elif shi_can_move(onFocus, onFirst):
                        if selected2 == 0:
                            # move selected to selected2
                            brd.makeMove(Move(onFocus, 'move', onFirst, [], 0))
                            Step = 'Waiting'
                elif selected.type == 'xiang':
                    if selected.hp == 2:
                        if skillReleased and (nothing(brd,(onFocus[0]+2,onFocus[1]+2)) or nothing(brd,(onFocus[0]+2,onFocus[1]-2)) or nothing(brd,(onFocus[0]-2,onFocus[1]+2)) or nothing(brd,(onFocus[0]-2,onFocus[1]-2))):
                            # rush (WIP)
                            Step = 'Second'
                        elif xiang2_can_move(onFocus, onFirst):
                            if selected2 == 0:
                                # move selected to selected2
                                brd.makeMove(Move(onFocus, 'move', onFirst, [], 0))
                                Step = 'Waiting'

                            elif selected2.owner == 1 and selected2.isActive:
                                # eat the selected 2
                                brd.makeMove(Move(onFocus, 'move', onFirst, [], 0))
                                Step = 'Waiting'
                    elif selected.hp == 1:
                        if skillReleased:
                            # recover
                            brd.makeMove(Move(onFocus, 'skill', 0, [onFocus], 0))
                            Step = 'Waiting'
                        elif xiang1_can_move(onFocus, onFirst):
                            if selected2 == 0:
                                # move selected to selected2
                                brd.makeMove(Move(onFocus, 'move', onFirst, [], 0))
                                Step = 'Waiting'
                            elif selected2.owner == 1 and selected2.isActive:
                                # eat the selected 2
                                brd.makeMove(Move(onFocus, 'move', onFirst, [], 0))
                                Step = 'Waiting'
                elif selected.type == 'che':
                    if che_can_move(onFocus, onFirst, brd):
                        if selected2 == 0:
                            # move selected to selected2
                            brd.makeMove(Move(onFocus, 'move', onFirst, [], 0))
                            Step = 'Waiting'
                        elif selected2.owner == 1 and selected2.isActive:
                            # eat the selected 2
                            brd.makeMove(Move(onFocus, 'move', onFirst, [], 0))
                            Step = 'Waiting'
                        elif selected2.owner == 0 and selected2.type == 'ma':
                            # make chema
                            brd.makeMove(Move(onFocus, 'move', onFirst, [], 0))
                            Step = 'Waiting'
                elif selected.type == 'ma':
                    if ma_can_move(onFocus, onFirst):
                        if selected2 == 0:
                            # move selected to selected2
                            brd.makeMove(Move(onFocus, 'move', onFirst, [], 0))
                            Step = 'Waiting'
                        elif selected2.owner == 1 and selected2.isActive:
                            # eat the selected 2
                            brd.makeMove(Move(onFocus, 'move', onFirst, [], 0))
                            Step = 'Waiting'
                        elif selected2.owner == 0 and selected2.type == 'che':
                            # make mache
                            brd.makeMove(Move(onFocus, 'move', onFirst, [], 0))
                            Step = 'Waiting'
                elif selected.type == 'mache' or selected.type == 'chema':
                    if ma_can_move(onFocus, onFirst) or che_can_move(onFocus, onFirst, brd):
                        if selected2 == 0:
                            # move selected to selected2
                            brd.makeMove(Move(onFocus, 'move', onFirst, [], 0))
                            Step = 'Waiting'
                        elif selected2.owner == 1 and selected2.isActive:
                            # eat the selected 2
                            brd.makeMove(Move(onFocus, 'move', onFirst, [], 0))
                            Step = 'Waiting'
                elif selected.type == 'pao':
                    if soldier_can_move(onFocus, onFirst) and selected2 == 0:
                        # move selected to selected2
                        brd.makeMove(Move(onFocus, 'move', onFirst, [], 0))
                        Step = 'Waiting'
                    elif shi_can_move(onFocus, onFirst):
                        if selected2 != 0 and selected2.owner == 0 and selected2.isActive and pao_can_shoot(brd,onFocus,onFirst):
                            # select bomb (WIP)
                            Step = 'Second'
                elif selected.type == 'soldier':
                    if skillReleased and selected.hp >= 2:
                        # sacrisfy
                        Step = 'Second'
                    elif soldier_can_move(onFocus, onFirst):
                        if selected2 == 0:
                            # move selected to selected2
                            brd.makeMove(Move(onFocus, 'move', onFirst, [], 0))
                            Step = 'Waiting'
                        elif selected2.owner == 1 and selected2.isActive:
                            # eat the selected 2
                            brd.makeMove(Move(onFocus, 'move', onFirst, [], 0))
                            Step = 'Waiting'
                        elif selected2.owner == 0 and selected2.isActive and selected2.type == 'soldier' and selected.hp == 1:
                            brd.makeMove(Move(onFocus, 'move', onFirst, [], 0))
                            Step = 'Waiting'
                    elif selected2 != 0 and selected2.owner == 0 and selected2.type == 'soldier' and selected2.isActive:
                        # teleport
                        if nothing(brd,(onFocus[0]+1,onFocus[1])) or nothing(brd,(onFocus[0]-1,onFocus[1])) or nothing(brd,(onFocus[0],onFocus[1]+1)) or nothing(brd,(onFocus[0],onFocus[1]-1)):
                            Step = 'Second'

        elif Step == 'Second':

            screen.blit(focus, coor_of_point(onFocus))

            if onFirst[0] == -1:
                pic = pg.transform.scale(focus2, (31, 31))
                screen.blit(pic, coor_of_point(onFirst))
            else:
                screen.blit(focus2, coor_of_point(onFirst))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    Program = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouseloc = pg.mouse.get_pos()
                    selected3 = brd.stoneOnLocation(nearest_point(mouseloc))
                    onSecond = nearest_point(mouseloc)
            
            if onSecond[0] != -1 or onSecond[1] != -1:
                if selected.type == 'king':
                    if selected3 != 0 and (selected3.isActive == True and selected3.owner == 0):
                        Step = 'Third'
                elif selected.type == 'shi':
                    if selected2 == 0 and shi_can_move(onFocus,onSecond) and selected3 == 0:
                        # summon to here
                        sum_type = type_of_grave(onFirst)
                        sum_hp = 1
                        if sum_type == 'xiang':
                            sum_hp = 2
                        brd.makeMove(Move(onFocus, 'skill', onSecond, [], Stone(sum_type, sum_hp, 0, True)))
                        Step = 'Waiting'
                elif selected.type == 'xiang':
                    if selected3 == 0 or (selected3.isActive == True and selected3.owner == 1):
                        if xiang2_can_move(onFocus, onSecond) and not xiang1_can_move(onFocus, onSecond):
                            brd.makeMove(Move(onFocus, 'skill', onSecond, [], 0))
                            Step = 'Waiting'
                elif selected.type == 'pao':
                    if selected3 == 0 or (selected3.isActive == True and selected3.owner == 1):
                        if bomb_can_reach(onFocus, onFirst, onSecond, brd):
                            brd.makeMove(Move(onFocus, 'skill', onSecond, [onFirst], 0))
                            Step = 'Waiting'
                elif selected.type == 'soldier':
                    if skillReleased:
                        if onSecond[0] == -1 and onSecond[1] >= 8: # can be 8 (king)
                            if brd.deathCount[0][type_of_grave(onSecond)] >= 1:
                                # summon
                                sum_type = type_of_grave(onSecond)
                                sum_hp = 1
                                if sum_type == 'xiang':
                                    sum_hp = 2
                                brd.makeMove(Move(onFocus, 'skill', (-1, -1), [onFocus], Stone(sum_type, sum_hp, 0, True)))
                                Step = 'Waiting'
                    elif selected3 == 0:
                        if shi_can_move(onFocus, onSecond):
                            brd.makeMove(Move(onFocus, 'skill', onSecond, [onFirst], 0))
                            Step = 'Waiting'
                
        elif Step == 'Third' or Step == 'Forth':

            screen.blit(focus, coor_of_point(onFocus))
            screen.blit(focus2, coor_of_point(onSecond))

            if Step == 'Forth':
                screen.blit(focus2, coor_of_point(onThird))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    Program = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouseloc = pg.mouse.get_pos()
                    if Step == 'Third':
                        selected4 = brd.stoneOnLocation(nearest_point(mouseloc))
                        onThird = nearest_point(mouseloc)
                    else:
                        selected5 = brd.stoneOnLocation(nearest_point(mouseloc))
                        onForth = nearest_point(mouseloc)
            if Step == 'Third':
                if selected4 != 0 and (selected4.isActive == True and selected4.owner == 0):
                    Step = 'Forth'
            else:
                if king_can_rush(onFocus, onForth):
                    brd.makeMove(Move(onFocus, 'skill', onForth, [onThird, onSecond], 0))
                    Step = 'Waiting'

        render(brd, screen)
        pg.display.update()

    main_clock.tick(FPS)
    
pg.quit()

