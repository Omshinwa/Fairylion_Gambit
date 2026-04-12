
# ::::    ::::      :::     :::::::::  
# +:+:+: :+:+:+   :+: :+:   :+:    :+: 
# +:+ +:+:+ +:+  +:+   +:+  +:+    +:+ 
# +#+  +:+  +#+ +#++:++#++: +#++:++#+  
# +#+       +#+ +#+     +#+ +#+        
# #+#       #+# #+#     #+# #+#        
# ###       ### ###     ### ###        

label l_map_0_4:
    $ TEAM = [young_suzaku, jagen, abel]
    $ jagen.health = 1
    $ young_suzaku.health = young_suzaku.max_health
    $ abel.health = abel.max_health
    call l_black_scene_change

    show bg castle:
        xysize (1.0, 1.0)
    
    $ game = Game('l_map_0_4')
    $ chess = Chess_control(bg=None, bg_board='metal')
    $ chess.set_fen("8/8/8/8/8/8/8/8 w - - 0 1")
    $ chess.drop('K', 'b1', 0)
    $ chess.drop('R', 'f1', 0)
    $ chess.drop('N', 'e1', 0)
    $ get('K').pilot = young_suzaku
    $ get('R').pilot = jagen
    $ get('N').pilot = abel
    show screen s_battlefield(chess)
    with dissolve
    pause 0.2
    $ AUTO_CENTER_ON_SPEAK_CHAR_BATTLEFIELD = True
    jagen "*Huff*"
    abel "Are you alright [jagen()]?"
    jagen "Yes, it's just the wound from earlier."
    jagen "Let's just keep moving."
    call l_move_piece('f1f4', 0.5)
    call l_move_piece('e1g2', 0.3)
    call l_move_piece('g2h4', 0.3)
    call l_move_piece('b1b2', 0.5)
    pause 0.1
    "???" "Gotcha."
    $ chess_camera.center_on()
    $ chess.drop('r', 'a1')
    call l_move_piece('a1a3')
    $ chess.drop('r', 'c1')
    call l_move_piece('c1c3')
    $ chess.drop('r', 'a1')
    play audio "sound/board/tank.wav"
    with dissolve_fast
    $ chess.drop('r', 'c1')
    play audio "sound/board/tank.wav"
    with dissolve_fast
    young_suzaku "!"
    jagen "Prince!"
    $ chess.drop('r', 'd6')
    $ chess.drop('r', 'e6')
    with dissolve
    pause 0.3

    $ chess.drop('k', 'e7')
    with dissolve
    pause 0.3

    $ stanley.color = 1
    $ get('k').pilot = stanley
    pause 0.3
    show stanley at right
    stanley "Seems like the scout unit failed. How typical."
    stanley "Huh?... Isn't that..?"
    show jagen at left
    jagen "Lady [stanley()]."
    stanley "[jagen()]! Haha, you old bones."
    jagen "I never thought we'd meet again like this."
    abel "Sir [jagen()], you know her?"
    jagen "She's a famous general of [name('The Holy Empire')]."
    jagen "We have... a history of battling each other. Hoho."
    stanley "We're basically rivals."
    stanley "I always imagined our last battle to be epic."
    stanley "Shame it's going to be so one-sided."
    jagen "Who's saying this won't be competitive?"
    stanley "...Have you become senile, old man?"
    stanley "Even you won't make it out of this alive."
    stanley "TROOPS!"

    $ chess.drop('r', 'c7')
    $ chess.drop('r', 'f7')
    $ chess.drop('r', 'c8')
    $ chess.drop('r', 'd8')
    $ chess.drop('r', 'e8')
    $ chess.drop('r', 'f8')
    with dissolve
    pause 0.3
    abel "Oh my god."
    stanley "So? Are you still as confident?"
    jagen "I understand this means you're fine with the war?"
    # stanley "I just follow the orders."
    stanley "Spare me your mind games. This is the end [jagen()]!"
    hide stanley
    hide jagen
    $ AUTO_CENTER_ON_SPEAK_CHAR_BATTLEFIELD = True
    young_suzaku "What are we gonna do [jagen()]?"
    abel "Can we just surrender and hope they spare us?"
    jagen "Not yet. This old dog's still got one trick left... Hohoho."
    # gotta set it up before the _start so jagen doesnt die
    $ get(jagen).pilot.skills['setup'] = []

    $ game.custom_objective = _("Draw against the enemy.")
    jump l_start_battle
    
label l_map_0_4_start:
    $ chess.goal = 'survive'
    return

label l_map_0_4_Win:
    young_suzaku "[jagen().upper()]!!!!"
    abel "Prince! Quick let's get out of here!"
    $ g.progress = 100
    return

label l_map_0_4_Lost:
    jagen "No, this is not it..."
    jagen "Prince, do you remember what a stalemate is?"
    young_suzaku "When we can't move but our King isn't directly under attack?"
    jagen "Right. Under Geneva Conventions, this is a draw, and this is how we will escape this situation."
    while (chess.history):
        $ chess.undo_item()
    with pointillisme
    jagen "Our KING had no move, but it isn't attacked by any of the black ROOKs."
    jagen "It is merely trapped, though if we gave one move to the enemy, they will checkmate us next turn."
    jagen "So our goal is to have the enemy take our other pieces, then it will be stalemate!"
    abel "But will they do it?"
    jagen "We will force them."


    return

label l_map_0_4_endTurn:
    if len(chess.history):
        $ move = chess.history[-1].move

    if len(chess.history)==1 and move.piece.fen == 'n' and move.to == 77:
        stanley "Are you getting desperate?"
        pause 0.2
        call l_engine_move(chess.coord_to_move('e6g6'))
        pause 0.2
        return

    # if they didnt do a rook move that leads to check, ignore everything:
    if chess.side == 0 or move.piece.fen != 'r' or not chess.is_in_check(1):
        return
    # can you take the rook? which would lead to stalemate?
    python:
        engine.copy(chess)
        moves = []
        exist_stalemate_capture = True
        # check if there is capturing rook move
        for move in engine.gen_legal_moves(1):
            if move.capture and move.capture.fen == 'r':
                moves.append(move)
        
        if len(moves) == 0: # theres no capture move available.
            exist_stalemate_capture = False
        else: # there is capture moves, do they lead to stalemate?
            for move in moves:
                engine.make_move(move)
                is_stalemate = engine.is_stalemated(0)
                engine.undo()
                if not is_stalemate:
                    # there is a non stalemating capture move, RETURN
                    renpy.return_statement()
                # If it's a stalemate, we don't add it to valid_moves
            moves = []

        # now, either theres no move, or they all lead to stalemate

        # all capture moves lead to stalemate.
        if len(moves) == 0:
            moves = list(engine.gen_legal_moves(1))

        # remove all stalemate moves
        non_stalemate_moves = []
        for move in moves:
            engine.make_move(move)
            is_stalemate = engine.is_stalemated(0)
            engine.undo()
            if not is_stalemate:
                non_stalemate_moves.append(move)
        moves = non_stalemate_moves

        # remove king moves already tried
        for i in range(len(moves) - 1, -1, -1):
            for old_move in chess.history:
                if len(moves)>1 and moves[i].piece.fen == 'k' and moves[i].to == old_move.move.to:
                    del moves[i]
                    break  # Move to next move after deleting

    # REORDER IT TO PRIORITIZE KING MOVES WHILE LEN(HISTORY) IS UNDER 8
    python:
        if len(chess.history) < 10:
            reorder_moves = []
            for move in moves:
                if move.capture:
                    reorder_moves.append(move)
                else:
                    reorder_moves.insert(0, move)
            moves = reorder_moves

    if not_done('stalemate', 'onceEveryFight'):
        $ AUTO_CENTER_ON_SPEAK_CHAR_BATTLEFIELD = True
        stanley "..."
        pause 0.5
    elif exist_stalemate_capture and len(chess.history) > 10 and not_done('stalemate2', 'onceEveryFight'):
        $ AUTO_CENTER_ON_SPEAK_CHAR_BATTLEFIELD = True
        stanley "......"
        pause 0.5
    elif exist_stalemate_capture and len(chess.history) > 16 and not_done('stalemate3', 'onceEveryFight'):
        $ AUTO_CENTER_ON_SPEAK_CHAR_BATTLEFIELD = True
        stanley "........."
        jagen "What's wrong [stanley()]?"
        jagen "I'm defenseless, you can take me any time."
        stanley "It will be a stalemate by the Geneva Conventions."
        stanley "So you're ready to throw your life away?"
        jagen "The cause is just."
        stanley "You fool."
        young_suzaku "[jagen()]!"
        jagen "Do not be scared Prince."
        jagen "I've told [abel()] to take care of you when I'm gone."
        jagen "Just run away from the castle as fast as you can."
        young_suzaku "But..."
        stanley "For me to fall into such a trap..."
        stanley "I'll honor your bravery."
        stanley "You were one fine commander, [jagen()] of [name('the Kingdom')]."
        $ chess_camera.center_on()
        young_suzaku "[jagen()]!!!!"
        call l_tutorial('story_death')

        pause 1.0
        # force the capture
        python:
            moves = []
            for move in engine.gen_legal_moves(1):
                if move.capture and move.capture.fen == 'r':
                    moves.append(move)

    $ g.state = {'battle'}
    pause 1.0
    call l_engine_move(moves[0])

    return