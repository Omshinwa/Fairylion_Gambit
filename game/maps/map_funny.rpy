# THIS IS A BUNCH OF CUTSCENE FOR INSTAGRAM / YOUTUBE

label map_mrs_obama:

    show black onlayer screens
    with transition_bars
    scene onlayer screens
    scene
    show bg castle:
        xysize (1.0, 1.0)
    show corner_shadow

    $ game = Game('l_map_0_2')
    $ chess = Chess_control((7,7), bg=None, bg_board='metal')
    $ chess.set_fen("7b/8/8/8/8/8/8/ w - - 0 1")
    # $ chess.drop(young_suzaku, 'c3', 0)
    # $ chess.drop(jagen, 'd3', 0)
    $ chess.drop('K', 'c3', 0)
    $ chess.drop('R', 'd3', 0)
    $ get('K').pilot = young_suzaku
    $ get('R').pilot = jagen
    # $ chess.drop('k', 'd2', color=2)

    # $ chess.ui['camera'].zoom = 1.1
    show screen s_battlefield(chess)
    with dissolve

    "{i}In White's castle."

    show coin onlayer l_chess at chess.t_layer('e4')
    with dissolve
    pause

    with vpunch
    show young_suzaku at left
    with vpunch
    $ chess.ui['camera'].zoom = 1.2
    young_suzaku "What's happening?"

    show jagen at right
    jagen "THERE'S A SNIPER!!!"
    play audio 'sound/funny/mrs obama get down.mp3'
    
    jagen "MR PRINCE, GET DOWN!!!"
    $ chess.board[get('K').pos] = c.EMPTY
    $ get('K').pos = 42
    $ chess.board[42] = get('K')
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

    young_suzaku "[jagen.name]!!! Are you okay? "
    jagen "Y-Yes... But the assailant..."
    $ chess_camera.zoom = 1.1
    $ chess_camera.center_on()
    pause 0.5
    hide corner_shadow onlayer screens with dissolve
    show expression Image("/skin/pieces/merida/black bishop merida.svg", dpi=300) as bishop at right:
        xysize (700,700)
        ypos 200
        
    "Holy Sniper" "Well played"