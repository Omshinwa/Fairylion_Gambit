screen s_tarot(tarot, centered_pilot = None):
    default elapsed = True
    add "#0006"
    # frame:
    #     xysize (500,1.0) xalign 0.95
    #     style 'empty'
    #     add "tarot [tarot]" align (.3,.5) ysize 800 fit 'scale-down':
    #         matrixcolor BrightnessMatrix(-0.3)*ContrastMatrix(0.5)
    frame:
        xysize (500,500) align (.5,.2)
        style 'empty'
        text _(tarot.upper()) font "fonts/Trattatello.ttf" align (.5,.5) size 100 color "#fff"
        text SKILLLIST[tarot].desc color "#fff" font "fonts/Trattatello.ttf" align (.5,.5)
        # vbox:
        #     align (.5,.5)
        #     spacing 0
        #     text _(tarot.upper()) font "fonts/Trattatello.ttf" align (.5,.5) size 100 color "#fff" yoffset 50
        #     text TAROT[tarot] color "#fff" font "fonts/Trattatello.ttf" align (.5,.5) line_spacing -40

    if centered_pilot:
        add "square default eatpiece" at t_camera_follow(centered_pilot.pos)

transform t_camera_follow(target):
    function _t_camera_follow_func(target)

init python:
    def _t_camera_follow_func(pos_target):
        def _f(trans, st, at):
            x, y = chess_camera.board_offset_center()
            x += 1920/2.0
            y += 1080/2.0
            x2, y2 = chess.POS_TO_SXY(pos_target, .5)
            x2 -= (SQUARESIZE * chess.size[0])/2.0
            y2 -= (SQUARESIZE * chess.size[1])/2.0
            x += x2 * chess_camera.zoom
            y += y2 * chess_camera.zoom
            trans.pos = (absolute(x), absolute(y))
            trans.anchor = (.5,.5)
            trans.zoom = chess_camera.zoom
            return 0 if st < 0.6 else None
        return _f

    def show_s_tarot(tarot, piece_target:Robot_Piece=None):
        if piece_target:
            chess_camera.center_on(piece_target.pos)
        else:
            pilot = get(kallen) or get('Q')
            if pilot:
                chess_camera.center_on(pilot.pos)
        renpy.show_screen('s_tarot', tarot, pilot)

    def hide_s_tarot():
        chess_camera.center_on(None)
        renpy.hide_screen('s_tarot')

label l_use_item(item, freeItem=False):
    $ f_dismiss(True)
    if not freeItem:
        $ g.items[item] -= 1
    if item == 'undo':
        if len(chess.history):
            play audio 'sound/misc/whoosh1.wav'
            $ chess.undo_item()
            hide draw onlayer screens
            hide lost onlayer screens
            with dissolve
            if chess.side != chess.player and len(chess.history):
                play audio 'sound/misc/whoosh1.wav'
                $ chess.undo_item()
                with dissolve
            $ g.state = {'battle'}
            jump l_gameLoop.gameLoop
            # in case we lost, we dont want to just return
        elif rogue: # return to prep screen
            menu:
                "Return to Deployment Phase?"
                "Yes":
                    if len(chess.history)>0:
                        play audio 'sound/misc/whoosh1.wav'
                        $ chess.undo_item()
                        hide draw onlayer screens
                        hide lost onlayer screens
                        with dissolve
                    # TODO undo the setup skills such as OLD
                    call l_chess_undo_start
                "No":
                    $ g.items[item] += 1
    else:
        call l_use_tarot(item)
    return

label l_use_tarot(tarot):
    hide screen s_tarot with dissolve
    $ renpy.layer_at_list(t_blur, layer='master')
    show expression "tarot [tarot]" onlayer screens:
        align (.5,.5) ysize 800 fit 'scale-down'
    with dissolve
    pause .5
    play sound "images/battle_ui/tarot/activate.mp3"
    $ remove_blur_master()
    hide tarot onlayer screens
    with pointillisme
    pause .5
    $ game.move_callback = tarot
    call expression 'l_tarot_' + tarot
    $ game.undoable_move = len(chess.history)
    return

label l_tarot_fool(undo = False):
    if undo:
        jump .remove_tarot_effect
    python:
        first_piece = chess.get_pieces()[0]
        move = Move(first_piece, first_piece.pos, first_piece.pos)
        chess.make_move(move, check_legality=False)
    return

    label .remove_tarot_effect:
    return

label l_tarot_empress(undo = False):
    if undo:
        jump .remove_tarot_effect
    python:
        queen = None
        for piece in chess.get_pieces(chess.side):
            if piece.fen == 'q':
                piece.range['WARP'] = {'no_capture'}
                queen = piece
        f_select(queen)
    return

    label .remove_tarot_effect:
        python:
            for piece in chess.get_pieces(chess.side):
                if piece.fen == 'q':
                    del piece.range['WARP']
    return

# I am the most free.
# I'll make my dreams reality. # Manifest your destiny
# Keep your third eye open.
# I am the empress. I rule.
# The Wheel of Fortune: What goes up must go down.

# The Hierophant – I seek guidance when I need it.