label l_map_1_0:
    show black onlayer screens
    with transition_bars
    scene onlayer screens
    scene
    
    jagen "Test, im dead so this shouldnt display."
    "DEV: c'était la dernière map à peu près scripté"
    "Merci d'avoir joué!"
    
    "3 years later into the conflict-"

    $ game = Game('l_map_1_0')
    $ chess = Chess_control((5,5), bg='desert', bg_board='sand')
    $ chess.set_fen("5/5/5/5/5")
    $ chess.drop(kallen, 'c3', 0)
    $ chess.drop(oghi, 'e3', 1)
    show screen s_battlefield(chess) with dissolve
    with dissolve

    show kallen at left
    show oghi at right
    kallen "You traitors!"
    kallen "Not only defecting... but joining the [name('Imperials')]?!"
    oghi "[kallen()], give it up."
    oghi "The war is lost, the Prince is dead."
    kallen "You don't know that!"
    oghi "He's been missing for 2 years. Most of the platoon agree."
    kallen "Regardless, I'll never lick [name('imperial')] boots!"

    oghi "I expected you would say that..."
    $ chess_camera.center_on()
    play sound 'sound/board/foot_road.wav'
    $ chess.drop('i', 'c2', 0)
    with dissolve
    play sound 'sound/board/foot_road.wav'
    $ chess.drop('i', 'c4', 0)
    with dissolve
    show soldier_kingdom zorder 2 at left
    show kallen zorder -19 at left
    kallen "!"
    kallen "Let me go!"
    oghi "No can do, we will use you as leverage. To prove our good faith to [name('the Empire')]."
    oghi "''{b}The Lion of the battlefield{/b}''. Did you know people already gave you a nickname?"
    kallen "!"
    kallen "Gnn! let me GO-OAAAH!"
    call l_move_piece('c3b3', 0.5)
    $ chess.remove_piece(get(kallen))
    with dissolve
    hide kallen
    "[kallen()] ran away."
    oghi "What are you waiting for? Go after her!"
    oghi "Use the CHESSMEN if you have to!"
    scene
    scene onlayer screens
    with dissolve

    show bg desert:
        xysize (1.0, 1.0)
    with dissolve

    $ chess = Chess_control((5,5), bg='desert', bg_board='sand')
    # $ chess.set_fen("8/8/8/8/8/8")
    $ chess.set_fen("7/7/7/7/7/7")
    show screen s_battlefield(chess) with dissolve
    $ chess.drop_with(kallen, 'g3', 0)
    kallen "Ha... Ha..."
    kallen "They're still behind me!"
    # put an arrow on every sq on the A sq
    $ chess.ui['arrows'] = {(chess.XY_TO_POS[0][j], chess.XY_TO_POS[0][j]) for j in range(chess.size[1])}
    $ chess_camera.center_on(chess.XY_TO_POS[0][0])
    pause
    $ AUTO_CENTER_ON_SPEAK_CHAR_BATTLEFIELD = False
    kallen "The mountains are over there."
    kallen "I might just be able to hide."
    $ AUTO_CENTER_ON_SPEAK_CHAR_BATTLEFIELD = True

    $ chess_camera.center_on()

    call l_move_piece('g3f3')
    pause 0.3
    $ chess.drop_with('n', 'g4')
    $ chess_camera.center_on('g4')
    soldier_kingdom "You won't get very far."
    kallen "!"

    # $ chess_camera.move(800, 0, 0.5)
    # pause 0.5
    # show lelouch zorder -1 at left
    # show nunnally at left
    # $ MOVE_SPEAK_CHAR_FORWRD[0] = False
    # nunnally "Brother, she's coming. And she has pursuers."
    # lelouch "Just as expected, let's bail her out."
    # hide lelouch
    # hide nunnally
    # with dissolve

    $ game.custom_objective = _("[kallen()] escapes (reaches column A).")
    jump l_start_battle

    call l_move_piece('g3f3')
    kallen "?! What's this."
    kallen "What is an empty ROOK doing here?"
    "a rook attacks and free kallen, Kallen runs toward the rook but finds it empty."
    "Do you want to live? do you want to beat the empire? Then follow my instructions."
    "Beat the empire..."

init python:
    # lessons:
    # set a -c.MAX_SCORE and a c.MAX_SCORE condition 
    def eval_map_1_0(self):
        if get(0) is None: # get(0) is get(kallen)
            return -c.MAX_SCORE
        kallen_x = self.get(kallen).x
        if kallen_x == 0:
            return c.MAX_SCORE
        kallen_position_bonus = c.MAX_SCORE / (kallen_x + 1)
        return self.eval_default()/10 + kallen_position_bonus

label l_map_1_0_start:
    $ game.win_con = 'get(kallen) and get(kallen).x == 0' # on first rank
    $ chess.stalemate_flag = 2
    python:
        chess.CRITICAL[0] = [get(kallen)]
    $ chess.goal = eval_map_1_0
    return

label l_map_1_0_Lost:
    lelouch "That idiot...!"
    return

label l_map_1_0_endTurn:
    $ sq = get(kallen).pos_a8
    if len(chess.history) > 13 and not_done('1', 'onceEveryFight'):
        kallen "I can't make any progress..."
        $ chess.drop_with('K', 'a5')
        $ get('K').pilot = lelouch
        # $ chess.CRITICAL[0].remove(get('K'))
        kallen "?!"
        kallen "A Chessman KING?"
        lelouch "Let's get her out of here."
    return

label l_map_1_0_Win:
    show kallen at left
    kallen "Good! Let's get out of here."
    
    show lelouch at left
    show nunnally at left
    show kallen at right
    kallen "Who are you?"