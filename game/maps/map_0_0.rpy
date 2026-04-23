label l_intro:
    $ init_pilots()
    scene
    scene onlayer screens
    show cg_intro

    # "[name('The Middle Kingdom')] was this vast country with a rich history."
    # "Unfortunally, wealth was poorly distributed and the folk often suffered from famine and harsh winters."
    # "In the year 1950, a popular civil war broke out. It gathered all kinds of factions with the Royal Family as common enemy"
    # "The revolution was successful and the royal family had to escape to a remote island."
    # "But the time was not for peace. The factions that constitued the revolution clashed  over the future direction of the country."
    # "In the end, a new country was born: [name('The Holy Empire')]. The remote island was still a target, but was left alone while the country while rebuilding itself."
    # "Several generation passed. [name('The Holy Empire')] became this authoritarian, belligerent country."
    # "Meanwhile, the new [name('The Middle Kingdom')] became much more democratic, supported by [name('The United Nations')]."
    # "In 2000, the [name('The Middle Kingdom')] asked to join [name('the United Nations')]."
    # "This sparked the invasion by [name('the Holy Empire')]..."
    # "6 months ago..."
    "Story: [name('the Holy Empire')] (black) is invading [name('The Middle Kingdom')] (white)."

    jump l_map_select

label l_map_0_0:
    call l_black_scene_change
    show bg desert:
        xysize (1.0, 1.0)
    with dissolve
    play music "music/Fire emblem a beckoning guest uninvinted visitor.mp3"
    "Middle Kingdom, on the battlefield."
    show stanley at left
    stanley "We have such a numeric advantage... Why even bother deploying me?"
    $ game = Game('l_map_0_0')
    $ chess = Chess_control((7,7), bg="desert", bg_board="sand", win_con='kill')
    $ chess.player = 1
    $ chess.set_fen("1rrkrr1/1rrrrr1/7/7/7/4P2/1P1P2P/7 b - - 0 1")

    $ stanley.color = 1
    $ get('k').pilot = stanley
    $ engine.copy(chess)
    
    show screen s_battlefield(chess) with dissolve
    # show stanley at left
    
    $ AUTO_CENTER_ON_SPEAK_CHAR_BATTLEFIELD = False
    stanley "This is the battlefield, our units, the CHESSMEN are the black ones."
    stanley "The enemy is made up of CHESSMEN Model PAWN. This should be trivial."
    show soldier_kingdom at right
    soldier_kingdom "?!"
    soldier_kingdom "It's [name('the Holy Empire')]!"
    show soldier_empire at left
    soldier_empire " They saw us!"
    # stanley "Tsk, forget it, let me inside the KING."
    stanley "Don't let any of them get away! We don't want reinforcements here."
    $ game.custom_objective = _("Don't let any pawn reach the bottom.")
    jump l_start_battle

init python:
    def eval_map_0_0(self):
        if any(pawn.y == 7 for pawn in self.PIECELIST[0]['p']):
            return c.MAX_SCORE
        if len(self.get_pieces(0)) == 0:
            return -c.MAX_SCORE
        return self.eval_default()

label l_map_0_0_start:
    call l_tutorial('story_commands')
    # $ del get('P').range['double move']
    # $ del get('P 2').range['double move']
    # $ del get('P 3').range['double move']
    # $ del get('P 4').range['double move']
    $ chess.stalemate_flag = 0
    $ chess.goal = eval_map_0_0
    $ chess.promotions = [[],[]]
    # overwrite lose_con so that stalemate condition doesnt get triggered,
    # overwise the game would stop on stalemate before reaching endTurn
    $ game.lose_con = "any(pawn.y == 7 for pawn in chess.PIECELIST[0]['p'])"
    $ game.win_con = "len(chess.get_pieces(0)) == 0"
    return

label l_map_0_0_endTurn:
    if chess.side == 1 and chess.state == 'selecting' and chess.ui['selected'] and type(chess.ui['selected']) == Robot_Piece:
        if chess.ui['selected'].color == 1:
            # if we selected a rook for the first time:
            if chess.ui['selected'].fen == 'r' and not_done('select_rook', 'onceEveryFight'):
                stanley "This is a CHESSMAN Class + Model ROOK. It moves up and down, left and right, with unlimited range."
                stanley "It's one of the most powerful CHESSMAN. Only the most skilled can pilot them."
                $ f_select(chess.board[31])
                stanley "The enemy is only made up of CHESSMEN Class ^ Model PAWN, the cheapest models."
                $ chess.ui['arrows'].add((31,41))
                $ chess.ui['arrows'].add((31,39))
                stanley "Just remember, they move 1 square forward but attack 1 square diagonally."
                $ chess.ui['arrows'] = set()
                call l_tutorial('story_chessman')
                $ f_dismiss()
            elif chess.ui['selected'].fen == 'k' and chess.ui['selected'].color == 1 and not_done('select_king', 'onceEveryFight'):
                stanley "This is a CHESSMAN Class # Model KING. That's the CHESSMAN I'm piloting and giving orders from."
                stanley "It moves in every direction but only has a range of 1. Losing it means losing the battle, so protect it."
    elif chess.is_stalemated(0): # we dont teach about stalemates yet
        "White skips their turn."
        $ chess.side = 1
    return

label l_map_0_0_Win:
    show stanley at left
    stanley "Let's keep going. The castle shouldn't be too far."
    $ g.progress += 1
    return 

label l_map_0_0_Lost:
    show stanley at left
    stanley "How did you butcher this? Try again."
    return 

# ::::    ::::      :::     :::::::::  
# +:+:+: :+:+:+   :+: :+:   :+:    :+: 
# +:+ +:+:+ +:+  +:+   +:+  +:+    +:+ 
# +#+  +:+  +#+ +#++:++#++: +#++:++#+  
# +#+       +#+ +#+     +#+ +#+        
# #+#       #+# #+#     #+# #+#        
# ###       ### ###     ### ###  

label l_map_0_1:
    call l_black_scene_change

    $ game = Game('l_map_0_1')
    $ chess = Chess_control((7,7), bg="desert", bg_board="sand")
    $ chess.set_fen("1rrkrr2/1rrrrr2/8/8/1PPPPPP1/5K2 b - - 0 1")
    $ chess.player = 1

    $ engine.copy(chess)
    
    show screen s_battlefield(chess) with dissolve

    show soldier_kingdom at right
    soldier_kingdom "[name('The Holy Empire')] have breached our defense! Send a message to the castle!"
    soldier_kingdom "Don't let them get any further!"

    show stanley at left
    stanley "Here they are. At least this time they have a CHESSMAN Model KING leading them."
    jump l_start_battle


label l_map_0_1_start:
    call l_tutorial('story_checkmate')
    call l_tutorial('story_stalemate')
    return


label l_map_0_1_Win:
    return

# ::::    ::::      :::     :::::::::  
# +:+:+: :+:+:+   :+: :+:   :+:    :+: 
# +:+ +:+:+ +:+  +:+   +:+  +:+    +:+ 
# +#+  +:+  +#+ +#++:++#++: +#++:++#+  
# +#+       +#+ +#+     +#+ +#+        
# #+#       #+# #+#     #+# #+#        
# ###       ### ###     ### ###  


label l_map_0_2:
    call l_black_scene_change
    show bg castle_gates:
        xysize (1.0, 1.0)
    show stanley at left
    stanley "COME ON TROOPS!"
    stanley "This is their final line of defense; once it falls, we'll storm their castle."
    show soldier_empire at right
    soldier_empire "YES SIR."

    scene

    $ game = Game('l_map_0_2')
    $ chess = Chess_control((7,7), bg="castle_gates", bg_board='grass')
    $ chess.player = 1
    $ chess.set_fen("1r1k1r1/1rrrrr1/7/7/7/1N1P3/2PNP2/3K3 b - - 0 1")
    $ get('k').pilot = stanley
    $ stanley.color = 1
    $ AUTO_CENTER_ON_SPEAK_CHAR_BATTLEFIELD = False
    show screen s_battlefield(chess) with dissolve
    stanley "Here they are. At least this time they have a few minor pieces, and a KING leading them."
    $ f_select(get('N 2'))
    $ chess.ui['arrows'] = {(31,50),(31,24),(31,20),(31,38),(31,48),(31,42)}
    stanley "Just be careful of this CHESSMAN. A Class L model KNIGHT. It has a tricky movement pattern."
    stanley "Still, this will be trivial, this time the objective will be to capture the KING."
    jump l_start_battle

label l_map_0_2_start:
    call l_tutorial('story_checkmate')
    call l_tutorial('story_stalemate')
    return

label l_map_0_2_Lost:
    show stanley at left
    stanley "A failure huh? I'll give you some tips."
    stanley "You should destroy a KNIGHT when you have the occasion. Even if it's protected."
    stanley "Usually that would be a bad idea since we would lose a ROOK, which is more valuable than a KNIGHT."
    stanley "But our position is so overwhelming, you can just trade every KNIGHT for a ROOK."
    stanley "Then prey on the remaining PAWNs and the KING."
    return

label l_map_0_2_Win:
    show stanley at left
    stanley "Hey you! Come out of your KING."
    show soldier_kingdom at right
    soldier_kingdom "?! What do you want."
    stanley "You're more valuable to me alive than dead. Now, tell me about this castle we're heading in."
    return



# ::::    ::::      :::     :::::::::  
# +:+:+: :+:+:+   :+: :+:   :+:    :+: 
# +:+ +:+:+ +:+  +:+   +:+  +:+    +:+ 
# +#+  +:+  +#+ +#++:++#++: +#++:++#+  
# +#+       +#+ +#+     +#+ +#+        
# #+#       #+# #+#     #+# #+#        
# ###       ### ###     ### ###        

label l_map_0_3:
    show stanley at left
    show soldier_empire at right
    soldier_empire "Commander Stanley."
    stanley "What is it?"
    soldier_empire "Please let our platoon be the first one to scout the castle!"
    stanley "Heh, want all the glory? You're a true [name('imperial')]. Fine, you can go ahead."
    stanley "But you're on your own, don't come back crying."
    soldier_empire "Yessir!"
    hide soldier_empire
    pause 0.5

    stanley "And like all [name('imperials')], you underestimate the enemy."


    show black onlayer screens
    with transition_queen

    scene onlayer screens
    scene
    show bg castle:
        xysize (1.0, 1.0)
    show corner_shadow onlayer screens
    
    $ game = Game('l_map_0_3')
    $ chess = Chess_control((7,7), bg=None, bg_board='metal')
    $ chess.set_fen("7b/8/8/8/8/8/8/ w - - 0 1")
    $ chess.drop(young_suzaku, 'c3', 0)
    $ chess_camera.zoom = 1.06
    show screen s_battlefield(chess)
    with dissolve

    "{i}In White's castle."

    with vpunch
    show young_suzaku at left
    with vpunch
    $ chess_camera.zoom = 1.2
    young_suzaku "What's happening?"

    $ chess.drop('K', 'c1')
    with dissolve
    call l_move_piece('c1c2', 0.3)

    pause 0.3
    young_suzaku "[jagen()]? Is that you?"

    $ chess.drop(jagen, 'd3')
    $ piece = get('K')
    $ chess._remove_piece(piece)
    $ piece.color = 2
    $ chess._append_piece(piece)
    $ del piece
    show jagen at right
    jagen "Prince! We must evacuate."
    young_suzaku "What's happening [jagen()]!"

    with vpunch
    show jagen at right
    jagen "It's not safe out here. [name('The Holy Empire')] has breached in the castle."
    young_suzaku "What?! What happened to father?"
    jagen "We don't have time to discuss-"
    jagen "A SNIPER!!!"
    play audio 'sound/funny/mrs obama get down.mp3'
    
    jagen "MR PRINCE, GET DOWN!!!"
    $ chess.board[get(young_suzaku).pos] = c.EMPTY
    $ get(young_suzaku).pos = 42
    $ chess.board[42] = get(young_suzaku)
    call l_move_piece('d3c3', 0.2)
    # $ get('R').pos = 43
    show jagen at left
    with hpunch
    play audio 'sound/funny/Gunshot03.wav'
    pause 0.05
    $ chess.ui['arrows'] = {(98,87)}
    pause 0.05
    $ chess.ui['arrows'] = {(98,76)}
    pause 0.05
    $ chess.ui['arrows'] = {(98,65)}
    pause 0.05
    $ chess.ui['arrows'] = {(98,54)}
    pause 0.05
    $ chess.ui['arrows'] = {(98,43)}
    pause 0.05
    $ chess.ui['arrows'] = {(98,32)}
    pause 0.05
    $ chess.ui['arrows'] = {(98,21)}
    pause 0.2
    $ chess.ui['arrows'] = {}
    with dissolve

    show young_suzaku zorder -1
    young_suzaku "[jagen.name]!!! Are you okay? "
    jagen "Y-Yes, it barely missed... But the assailant..."
    $ chess_camera.center_on()
    $ chess_camera.zoom = 0.9
    $ AUTO_CENTER_ON_SPEAK_CHAR_BATTLEFIELD = False
    pause 0.5
    hide corner_shadow onlayer screens with dissolve
    
    show soldier_empire at right
    soldier_empire "You won't get so lucky next time old man."
    soldier_empire "Just hand over the Prince."

    pause 0.5

    $ chess.drop_with('r', 'g8')
    with dissolve
    $ chess.drop_with('k', 'f8')

    young_suzaku "!"
    jagen "...Prince, do you remember how to pilot a CHESSMAN?"
    young_suzaku "Y-yes, a bit..."
    jagen "Enter this KING, you'll be the commander."
    jagen "I'll pilot a ROOK."
    young_suzaku "Shouldn't you be piloting the KING and give orders?"
    jagen "No, I'm the only one left who can pilot a ROOK."
    young_suzaku "The only one left..."
    # young_suzaku "Be careful [jagen()]."
    # call l_move_piece('b3b2')
    # python:
    #     piece = get(young_suzaku)
    #     chess._remove_piece(piece)
    #     chess.board[piece.pos] = c.EMPTY
    # with dissolve
    # hide young_suzaku
    # "{i}[young_suzaku()] left the battlefield."
    jagen "Quick! Get in the CHESSMAN!"
    call l_move_piece('b3c2')
    jagen "[abel()]!"
    abel "!"
    jagen "Stop hiding and come out. I need you."
    abel "Oh man... We're totally done for aren't we?"
    jagen "The only way I'm dying is from old age! Hoho."
    
    play audio "sound/board/tank.wav"
    $ chess.drop('P', 'a2')
    with dissolve
    play audio "sound/board/tank.wav"
    $ chess.drop('P', 'b2')
    with dissolve
    play audio "sound/board/tank.wav"
    $ chess.drop('P', 'd2')
    with dissolve
    play audio "sound/board/tank.wav"
    $ chess.drop('N', 'b1')
    with dissolve
    play audio "sound/board/tank.wav"
    $ chess.drop('R', 'd1', 2)
    with dissolve
    pause 0.5
    play audio "sound/board/enter.wav"
    $ chess.remove_piece(get(jagen))
    $ get('RR').pilot = jagen
    $ get('RR').setup_piece()
    with dissolve
    $ get('N').pilot = abel
    $ chess.side = 0

    if g.difficulty == 'easy':
        play audio "sound/board/tank.wav"
        $ chess.drop('N', 'a1', 0)
        with dissolve
        play audio "sound/board/tank.wav"
        $ chess.drop('P', 'e2', 0)
        with dissolve
        play audio "sound/board/tank.wav"
        $ chess.drop('P', 'f2', 0)
        with dissolve

    # $ game.lose_con = "get(jagen) is None"
    $ get(jagen).pilot.skills['setup'] = []
    $ get(jagen).pilot.health = 2
    jump l_start_battle
    

label l_map_0_3_start:
    return

label l_map_0_3_Win:
    young_suzaku "Hah... Is... this over?"
    abel "Phew, can't believe we won this."
    jagen "Hoho, you can rejoice when we're out of this castle."
    return

label l_map_0_3_Lost:
    show jagen at left
    jagen "Prince, I know you can do it."
    jagen "Let's analyze the starting position."
    play audio 'sound/misc/whoosh1.wav'
    while (chess.undo_item()):
        pass
    with dissolve
    python:
        for piece in chess.get_pieces(0):
            if piece.fen == 'p':
                chess.ui['arrows'].add((piece.pos, piece.pos))
    jagen "You have to exploit your extra PAWNs."
    $ chess.ui['arrows'].add((34, 94)) # d2 -> d8
    jagen "They have a special ability when they reach the top of the board."
    move chess['d2'] 6 up
    pause 0.5
    $ chess['d8'].fen = 'r'
    jagen "They can transform into any of our starting pieces, like the ROOK."
    jagen "So trade your pieces when you can, and slowly advance your PAWNs."
    $ game.is_over = 'loss'