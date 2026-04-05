define audio.tank_rolling = "<from 0.098 to 0.22>sound/board/tank.wav"

init python:
    def fen_to_speed(piece):
        if piece.fen == 'i':
            return 2
        else:
            return 10

    def f_play_move_piece_sound(piece, move):
        """Play sound effects for piece movement based on piece type and move flags."""
        
        # TODO: use a custom channel instead of audio to play tank sounds etc
        if move and (move.flag == 'enter' or move.flag == 'rescue'):
            chess.ui['animation_move'].time = 0.1
            renpy.music.queue("sound/board/enter.wav", channel='sound')
            return

        if piece.type == 'L':
            renpy.play("<from 0 to 0.098>sound/board/plane.wav")
            i = 0
            while i < chess.ui['animation_move'].time and i < 3:
                renpy.music.queue(f"<from {0.098+i} to {0.22+i}>sound/board/plane.wav", channel='sound')
                i += 0.1
            renpy.music.queue(f"<from {0.22+i}>sound/board/tank.wav", channel='sound')
            return

        elif piece.type == 'i':
            renpy.play("sound/board/foot_road.wav")
            i = 0
            while i < chess.ui['animation_move'].time and i < 3:
                renpy.music.queue("<silence .15>", channel='sound')
                renpy.music.queue("sound/board/foot_road.wav", channel='sound')
                i += 0.25
            return

        else:
            renpy.play("<from 0 to 0.098>sound/board/tank.wav")
            i = 0
            while i < chess.ui['animation_move'].time and i < 3:
                renpy.music.queue("<from 0.098 to 0.22>sound/board/tank.wav", channel='sound')
                i += 0.1
            renpy.music.queue("<from 0.22>sound/board/tank.wav", channel='sound')
        
        return

init python:
    def MOVE_TO_CHOICE(move): # for menu choices 
        if 'promotion' in move.flag:
            if move.data['p'] == 'p':
                return _(f"NO PROMOTION AVAILABLE")
            return _(f"PROMOTE TO {move.data['p']}")
        if 'castleK' in move.flag:
            return _(f"Castle")
        if 'castleQ' in move.flag:
            return _(f"Castle")
        return _(f"Normal Move")

label l_death_move_piece(robot, move, time):
    python:
        # when a pilot gets taken in a move, do a special anim
        # could be refactored with l_move_piece
        global g, chess, renpy
        g.state = {'cutscene'}
        fr_pos = chess.POS_TO_SXY(move.fr, 0.5)
        to_pos = chess.POS_TO_SXY(move.to, 0.5)

        midway_point = to_pos[:]  # copy
        direction_x = 1 if to_pos[0] > fr_pos[0] else (-1 if to_pos[0] < fr_pos[0] else 0)
        direction_y = 1 if to_pos[1] > fr_pos[1] else (-1 if to_pos[1] < fr_pos[1] else 0)

        midway_point = (absolute(float(midway_point[0]) - SQUARESIZE/2 * direction_x), absolute(float(midway_point[1]) - SQUARESIZE/2 * direction_y))
        chess.state = "move"
        chess.ui['animation_move'] = DotDict(piece=piece, fr=fr_pos, to=midway_point, time=time, capture=move.capture)
        f_play_move_piece_sound(piece, move)
        renpy.pause(time)
    
    $ i = 0
    while i < len(robot.pilot):
        $ pilot = robot.pilot[i]
        if pilot is not None and pilot.health == 0:
            $ pilot.die()
        $ i+=1

    python:
        time = 0.5
        f_create_animation_move(piece, midway_point, to_pos, time, mute=True)
        g.state = {'battle'}
        chess.make_move(move, False)
    return

label l_move_piece(list_of_moves, time=None):
    if type(list_of_moves) == Move:
        $ move = list_of_moves
    elif type(list_of_moves) == str: # something in the form of 'a3a4'
        $ move = chess.coord_to_move(list_of_moves)
        if move is False and 'cutscene' in g.state:
            $ move = chess.create_move_cutscene(list_of_moves)
    elif type(list_of_moves) == list and len(list_of_moves) == 1 and (not 'promotion' in list_of_moves[0].flag or list_of_moves[0].data['p'].fen == 'p'):
        # only 1 move for this sq that is NOT a promotion (or it's promoting to a pawn)
        $ move = list_of_moves[0]
    else: # at this square theres several moves possible IE PROMOTIONS:
        python:
            temp = [(MOVE_TO_CHOICE(move), i) for i, move in enumerate(list_of_moves)]
            temp.append((_("X"), 'CANCEL'))
            temp = renpy.display_menu(temp)
        if type(temp) == int:
            call l_move_piece(list_of_moves[temp], time) from _call_l_move_piece_1
        else:
            $ f_dismiss()
        return

    # OK WE GOT A GOOD SINGLE MOVE WE CAN PLAY THE ANIMATION:

    $ chess.ui['moves'] = {}
    $ piece = move.piece
    $ chess.clean_arrows()

    # if its chess like, time=2.0 instead
    if time is None:
        $ time = chess.real_dist_between_two_pos(piece.pos, move.to)/fen_to_speed(piece)
    
    # remove health
    if move.capture and move.capture.pilot:
        python:
            robot = move.capture
            for pilot in robot.pilot:
                if pilot is not None:
                    pilot.health -= 1

        # IF DEATH, do a dramatic animation:
        $ i = 0
        while i < len(robot.pilot):
            $ pilot = robot.pilot[i]
            if pilot is not None and pilot.health == 0:
                call l_death_move_piece(robot, move, time)
                $ del time, piece, robot, i
                return
            $ i += 1

    $ chess.make_move(move, False)
    $ f_create_animation_move(piece, chess.POS_TO_SXY(move.fr, 0.5), chess.POS_TO_SXY(move.to, 0.5), time)
    $ del time, piece
    return

init python:
    # Play a move animation, it has to finish at the end
    def f_create_animation_move(piece, fr, to, time, capture=None, *, mute=False):
        chess.ui['animation_move'] = DotDict(piece=piece, fr=fr, to=to, time=time, capture=move.capture)
        if (not mute):
            f_play_move_piece_sound(piece, move)
        chess.state = "move"
        renpy.pause(chess.ui['animation_move'].time)
        chess.state = "idle"
        chess.ui['animation_move'] = None
        chess.ui['selected'] = None
        chess.ui['inspected'] = None

#       :::      :::::::::  :::::::::: ::::    ::: :::::::::  :::   ::: 
#      :+:       :+:    :+: :+:        :+:+:   :+: :+:    :+: :+:   :+: 
#     +:+        +:+    +:+ +:+        :+:+:+  +:+ +:+    +:+  +:+ +:+  
#    +#+         +#++:++#:  +#++:++#   +#+ +:+ +#+ +#++:++#+    +#++:   
#   +#+          +#+    +#+ +#+        +#+  +#+#+# +#+           +#+    
#  #+#           #+#    #+# #+#        #+#   #+#+# #+#           #+#    
# ###            ###    ### ########## ###    #### ###           ###    


default persistent.cpu_strength = 3000

label l_enemy_play():
    if chess.side == 1-chess.player and chess.use_engine and not renpy.in_rollback(): #and not show_debug_menu 
        $ chess.wait_for_enemy = True

        if not chess.eq_board(engine):
            $ engine.copy(chess)
        if renpy.variant("web"):
            $ engine_background_think(depth, persistent.cpu_strength)
        else:
            ## allow the move to be played in the background
            $ renpy.invoke_in_thread(engine_background_think, persistent.cpu_strength, True)
    return

init python:

    def engine_background_think(depth, multithread=False):
        # move = engine.think(depth) # for monte carlo
        move = engine.think_minimax(1)
        engine.make_move(move)
        if multithread:
            renpy.invoke_in_main_thread(engine_move, move)
        else:
            engine_move(move)

    def engine_move(move):
        renpy.call("l_engine_move", move)

# this is invoked in the main thread
label l_engine_move(move):
    if move.color != chess.side:
        "MOVE WAS WRONG COLOR [move]"
        $ assert 0
    $ piece = chess.board[move.fr]
    $ f_select(piece)
    $ del piece
    pause 0.3
    # we have the move the computer found, now let's find the corresponding one in our UI:
    $ i = 0
    $ moves = chess.gen_moves()
    while (i < len(moves) and move != moves[i]):
        $ i+=1
    if i == len(moves):
        "[i]"
        "couldnt find the move: [move.data]"
        $ assert False
    $ chess.wait_for_enemy = False
    call l_move_piece(moves[i])
    return

label l_player_move(move):
    call l_move_piece(move)
    # callback like undoing tarot effects

    if renpy.has_label(game.move_callback):
        $ renpy.call('l_tarot_' + tarot, undo=True)
    return

