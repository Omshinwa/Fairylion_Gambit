init python:
    class Roguelike():
        army_strength = 0 # decide the value of the enemy
        leftover_difficulty = 0 # if a game was easier, make it harder for the next?
        round = 0
        # easy #??? #??? #hard
        enemy_comp = ['k']
        enemy_cost = {'p':1, 'n':3, 'b':3, 'r':5, 'q':9}
        # enemy_bias = {'p':1, 'n':1, 'b':1, 'r':2, 'q':3} # bias how we choose each piece (otherwise the queen is never chosen)
        enemy_bias = {'p':2, 'n':1, 'b':1, 'r':1, 'q':1} # bias how we choose each piece (otherwise the queen is never chosen)

        @property
        def pawns(self):
            return self.enemy_comp.count('p')

        @property
        def pieces(self):
            return len(self.enemy_comp) - self.enemy_comp.count('p')
            
        @staticmethod
        def difficulty_multiplier(round):
            """
            takes a round, output the difficulty modifier for that round (boss fights should be easier?)
            """
            difficulty_multiplier = [0.7, 1, 1, 1.3]
            return difficulty_multiplier[round%len(difficulty_multiplier)]

        def pick_enemies(self, round=None):
            round = round or self.round
            self.enemy_comp = ['k']
            variance = int(renpy.random.randint(-round,round)/2)
            army_strength = round*2.2 #difficulty_multiplier(round)# + leftover_difficulty + variance
            while army_strength >= 1 and len(self.enemy_comp) <= 16:
                available_enemy = [enemy for enemy in self.enemy_cost if army_strength>=self.enemy_cost[enemy]] 
                enemy_list = []
                for enemy in available_enemy: 
                    # we want to bias the picking algo so that if str>9, queen is 9 times as likely as the pawn to get picked
                    for i in range(self.enemy_bias[enemy]):
                        enemy_list.append(enemy)
                
                if len(self.enemy_comp) == 1:
                    print(enemy_list)
                i = renpy.random.choice(enemy_list)
                self.enemy_comp.append(i)
                army_strength -= self.enemy_cost[i]

            print(self.enemy_comp)
            return self.enemy_comp, army_strength
        
        def pick_board(self):
            min_wide = max(self.pawns, self.pieces) 
            # we either want a SQUARE, WIDE or LONG board.
            # they can be of any size.
            min_wide = max(min_wide, 5)
            max_wide = min(min_wide+2,8)

            if min_wide < 8:
                wide = renpy.random.randint(min_wide,max_wide)
            else:
                wide = 8

            # 50% make it square
            if renpy.random.randint(0,1):
                height = wide
            else:
                height = renpy.random.randint(wide,8)

            chess.setup_chess((wide,height))
            return (wide, height)

        
        def setup_comp(self):
            i = 0
            renpy.random.shuffle(self.enemy_comp)  
            # bias = renpy.random.choice('left', 'center', 'right')  
            while len(self.enemy_comp) > 0 and i<50:
                i += 1
                if 'k' in self.enemy_comp:
                    new_piece = 'k'
                    self.enemy_comp.remove('k')
                else:
                    new_piece = self.enemy_comp.pop(0)
                new_piece = Robot_Piece(new_piece, 1-chess.player)
                list_of_sq = []
                for x in range(chess.size[0]):
                    if new_piece.fen == 'p':
                        y = -2
                    else:
                        y = -1
                    # function
                    # 0 1 2 3 4 5 6 etc into
                    # 0 1 -1 2 -2 3 -3
                    x = int(chess.size[0]/2) + ((x%2)*2-1) * int(x/2)
                    pos = chess.XY_TO_POS[x][y]
                    if new_piece.fen == 'k':
                        # add the WHITE king
                        chess.drop(Robot_Piece('k',color=2,unmovable=True), chess.XY_TO_POS[x][0])
                    if chess.board[pos] == c.EMPTY:
                        print(f"DROP: {new_piece} {pos}")
                        chess.drop(new_piece, pos)
                        break

            ## give some extra pieces to white?
            for i in range(int(self.round/4)+1):
                piece = renpy.random.random()
                if piece < 0.3:
                    piece = 'n'
                elif piece < 0.6:
                    piece = 'b'
                elif piece < 0.85:
                    piece = 'r'
                else:
                    piece = 'q'
                print(piece)
                for x in range(chess.size[0]):
                    if chess.board[chess.XY_TO_POS[x][0]] == c.EMPTY:
                        print(f"empty:{x}")
                        new_piece = Robot_Piece(piece,color=2)
                        new_piece.deployed = True
                        print(new_piece.deployed)
                        chess.drop(new_piece, chess.XY_TO_POS[x][0])
                        ROBOTS.append(new_piece)
                        break

        def setup_rogue(self, round=None):
            round = round or self.round
            ROBOTS.sort(key=lambda robot: robot.value, reverse=True)
            self.pick_enemies(round)
            self.pick_board()
            self.setup_comp()

        def won(self):
            self.round += 1

    def play_sound(trans, st, at, filename):
        renpy.sound.play(filename, channel='audio')

screen s_roguelike():
    layer 'master'
    zorder 2
    vbox:            
        if prefs.battlefield_layout_left:
            pos (1.0, 0.0) xanchor 1.1
        else:
            align (0.0, 0.0)
        text _("ROUND [rogue.round]") size 50 font "fonts/Venus+Carrare.otf" color "#fff" outlines [(4, "#696969",0,0)] yanchor -0.1
    use s_shop_coin()

screen s_shop_coin():
    button at t_interactive:
        action Call('l_shop_rogue')
        style_prefix 'sty_btn'
        xysize(INFOBOX_WIDTH-50,110)

        if 'preparation' in g.state:
            anchor(0, 0)
            pos (190, 960)
        else: # The shop button can move depending on the state
            align(1.0, 1.0)

        hbox:
            xpos 20
            ypos -30
            text _("> SHOP") size 50

            fixed:
                # add "#0f0"
                xysize (100,100)
                add Transform("coin", xysize=(100,100), pos=(50,50)) at trs_coin
                text str(g.money):
                    font "fonts/Venus+Cormier.otf" color "#ffffa0" outlines [ (5, "#a98a46", 0, 2) ] size 50 align 0.5,0.5
    
    # THIS IS THE QUESTION MARK BUTTON
    button at t_interactive:
        align (1.0, 1.0)
        if 'preparation' in g.state:
            action Call('l_tutorial', 'preparation')
        elif 'result_screen' in g.state:
            if renpy.current_screen().name == 's_in_between_rounds' and renpy.get_screen_variable('state', screen='s_in_between_rounds') <= 3:
                action Call('l_tutorial', 'results')
            else:
                action Call('l_tutorial', 'recruit')
        add 'info_button'

        
#       :::           :::            :::     :::::::::  :::::::::: :::        
#      :+:            :+:          :+: :+:   :+:    :+: :+:        :+:        
#     +:+             +:+         +:+   +:+  +:+    +:+ +:+        +:+        
#    +#+              +#+        +#++:++#++: +#++:++#+  +#++:++#   +#+        
#   +#+               +#+        +#+     +#+ +#+    +#+ +#+        +#+        
#  #+#                #+#        #+#     #+# #+#    #+# #+#        #+#        
# ###                 ########## ###     ### #########  ########## ########## 

default -2 rogue = False

label l_map_rogue:

    scene onlayer screens
    scene

    if not_done('tuto_basic'):
        call l_tutorial('basic', False) from _call_l_tutorial

    # init stuff
    $ g.money = 10

    $ rogue = Roguelike()
    $ g.items['undo'] = 3

    if g.difficulty == 'easy':
        $ g.items['undo'] = 999

    $ chess = Chess_control((6,5))
    $ TEAM = [lelouch, GenericPilot(), GenericPilot()]
    if g.difficulty == 'easy':
        $ TEAM = [lelouch, kallen, GenericPilot(), GenericPilot()]

    $ ROBOTS = [Robot_Piece('r',color=0), Robot_Piece('n',color=0), Robot_Piece('b',color=0), Robot_Piece('q',color=0)]
    # $ ROBOTS = []

    label .gameloop:
    $ g.state = {'result_screen'}
    show screen s_roguelike
    show screen s_recruit(Pilot.get_rogue_recruits())
    with dissolve

    jump l_result_screen.loop


label l_map_rogue_start:
    $ print(f"chess proms: {chess.promotions}")
    if not 'q' in chess.promotions[1-chess.player]: #add queen promotion to the enemy
        $ chess.promotions[1].append('q')
    return

label l_map_rogue_Lost:
    call screen s_pauseScreen(False)
    menu:
        "Return to main menu?"
        "Yes":
            pass
        "No":
            jump l_map_rogue_Lost
    hide screen s_battlefield
    with transition_bars
    jump start
    return


label l_map_rogue_Win:
    ## win screen
    show screen s_roguelike
    if g.difficulty == 'normal':
        call l_increase_coin(7) from _call_l_increase_coin
    else:
        call l_increase_coin(14) from _call_l_increase_coin_1
    if persistent.free_undo:
        $ g.items['undo'] += 1
        show undo icon onlayer screens:
            xysize (80,80)
            align (0.5,0.5)
            ease 0.5 align(0.01,0.0) alpha 0.5
            ease 0.2 alpha 0
    pause 0.3
    show black onlayer screens zorder 2
    with transition_bars
    jump l_result_screen

label l_result_screen:
    $ g.state = {'result_screen'}
    show screen s_in_between_rounds
    hide screen s_battlefield
    hide black onlayer screens
    with dissolve

    show screen s_recruit(Pilot.get_rogue_recruits())

    pause
    $ renpy.set_screen_variable('state', 1, screen='s_in_between_rounds')

    python: ### remove used robots, rest people
        # remove used robots
        ROBOTS = [robot for i, robot in enumerate(ROBOTS) if not robot.deployed]
        # sort them by value
        ROBOTS.sort(key=lambda r: r.value)

        for pilot in TEAM:
            # ignore the dead
            if pilot.health <= 0:
                continue

            if pilot.deployed:
                pilot.increase_xp(1)
                renpy.play('sound/misc/xp.wav', channel='sound')
                if renpy.get_screen_variable('state', screen='s_in_between_rounds') == 1:
                    renpy.pause(0.3, modal=False)
        
        for pilot in TEAM:
            # ignore the dead
            if pilot.health <= 0:
                continue

            # if we didnt use a pilot, rest it:
            if not pilot.deployed:
                if pilot.rest():
                    renpy.play('sound/misc/xp.wav', channel='sound')
                    if renpy.get_screen_variable('state', screen='s_in_between_rounds') == 1:
                        renpy.pause(0.3, modal=False)

    $ renpy.set_screen_variable('state', 2, screen='s_in_between_rounds')
    pause
    $ renpy.set_screen_variable('state', 3, screen='s_in_between_rounds')

    python: ### give XP to the checkmating piece
        pilot = chess.history[-1].move.piece._pilot
        if len(pilot) == 1:
            pilot[0].increase_xp(2)
        elif len(pilot) >= 2:
            pilot[0].increase_xp(1)
            pilot[1].increase_xp(1)
        renpy.play('sound/misc/boost.wav')

    if renpy.get_screen_variable('state', screen='s_in_between_rounds')<4:
        pause
        $ renpy.set_screen_variable('state', 4, screen='s_in_between_rounds')

    label .loop:
        call screen s_pauseScreen(hard_stop=True)
        if renpy.get_screen('s_recruit'):
            jump .loop

    hide screen s_recruit
    hide screen s_in_between_rounds
    with transition_bars

    python:
        TEAM = [pilot for pilot in TEAM if pilot.health]
        for pilot in TEAM:
            pilot.deployed = False
        for robot in ROBOTS:
            robot.deployed = False
    jump l_rogue_next_map

label l_rogue_next_map:
    $ rogue.round += 1
    if g.difficulty == 'normal':
        $ persistent.best_run = max(persistent.best_run, rogue.round)
    $ rogue.setup_rogue()
    $ Pilot.sort(TEAM, 'default')
    $ ROBOTS.sort(key=lambda element:(-element.value, element.fen=='n'))
    $ game = Game('l_map_rogue')
    jump l_preparation
    return

transform trs_coin(child):
    anchor(0.5,0.5)
    block:
        child
        ease 0.5 xzoom 0.0
        ease 0.5 xzoom -1
        ease 0.5 xzoom 0.0
        ease 0.5 xzoom 1
        child
        pause 5
    repeat

transform trs_add_coins(time_offset):
    alpha 0.0
    pos (0.5,0.5)
    xysize (150,150)
    pause time_offset alpha 1.0
    function renpy.curry(play_sound)(filename="sound/misc/coin.mp3")
    ease 0.5 align(0.99,0.98) alpha 0.5
    ease 0.2 alpha 0

label l_increase_coin(coin):
    $ i = 0
    $ toHide = []

    while coin > i:
        $ renpy.show("coin" + str(i), what="coin", at_list=[trs_add_coins(i*0.15)], layer="screens")
        $ toHide.append("coin" + str(i))
        $ i += 1

    python:
        renpy.pause(1)
        for i in toHide:
            renpy.hide(i, layer="screens")
            g.money += 1
        del toHide
    return