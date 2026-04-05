###########################################################
#
#            UX RULES ABOUT THE CLICK AND DRAG
#
#   Usually, we deploy by clicking first in the reserve, then on the board where it goes
#   Clicking on the board, then in reserve -> doesnt deploy the unit
#           EXCEPT: if the piece on board is empty and the unit is a pilot that can pilot it, then deploy it.
#           Clicking with another piece on the board swap them (maybe should just select the 2nd?)
#           Self click again undeploy the unit

label l_preparation():
    $ g.state = {'preparation'}
    $ chess.side = 'move_first'
    $ chess.ui['moves'] = {}

    show screen s_battlefield(chess) with dissolve

    if not_done('tuto_preparation'):
        pause
        call l_tutorial('preparation')

    play music "music/preparation.mp3"

    label .loop:
        call screen s_pauseScreen(hard_stop=True)
    jump .loop
    return

label l_start_battle():
    $ autosave('battle')

    if 'preparation' in g.state: # FOR NON PREDEPLOYED
        if not chess.PIECELIST[chess.player]['K']:
            "You need a King to lead your army."
            return
        if any(piece.fen == 'i' for piece in chess.PIECELIST[chess.player]['m']):
            "You cannot deploy a Pilot outside a CHESSMAN."
            return
        if chess.get_pieces(2):
            "The [c.FEN_TO_PIECE[chess.get_pieces(2)[0].fen].capitalize()] on [chess.POS_TO_A8(chess.get_pieces(2)[0].pos).upper()] doesn't have any pilot. You won't be able to move it. Double click to store it."
            menu:
                "Deploy anyway?"
                "Yes":
                    pass
                "No":
                    return

    # START BATTLE ANIMATION
    $ f_dismiss()
    scene onlayer characters
    $ chess_camera.reset_dezoom_view(2.0)
    $ g.state = {'cutscene'} # allow the zoomin in at the beginning of the screen
    show screen s_start_battle
    with dissolve
    pause
    $ chess.start()
    $ done_flag["onceEveryFight"] = Set()

    # _START LABEL HAPPENS AFTER CHESS.START AND THE BATTLE SCREEN
    if renpy.has_label(game.level + '_start'):
        pause 0.5
        call expression game.level + '_start'

    $ engine.copy(chess)

    hide screen s_start_battle with Dissolve(.2)
    $ remove_blur_master()
    jump l_gameLoop

screen s_start_battle():
    on "show" action Function(renpy.layer_at_list, [t_blur], layer="master")
    dismiss:
        action Hide(None, Dissolve(.2)),Function(remove_blur_master), Return()
    vbox:
        align 0.5,0.4
        add 'i_start'
        null height 20
        if game.custom_objective:
            text "Objective: " + game.custom_objective size 50 style 'style_3d_txt' xalign 0.5 xsize 1000
        elif chess.win_con == None:
            text "Objective: Checkmate the KING" size 50 style 'style_3d_txt' xalign 0.5 xsize 1000
        elif chess.win_con == 'kill':
            text "Objective: Eliminate the enemy." size 50 style 'style_3d_txt' xalign 0.5 xsize 1000

screen s_preparation_overlay(): 
    use s_inventories()

    # RIGHT SIDE BUTTONS
    vbox:
        align 0.99,0.05
        button at t_interactive:
            style_prefix 'sty_btn'
            text _("START") size 80
            action Call('l_start_battle')

    if renpy.get_mode() == 'pause' or renpy.get_mode() == 'say':
        button: # DISMISS
            xysize 1.0,1.0
            if config.developer:
                text "RETURN" color "#0f0"
            action Return()

screen s_inventories():
    use s_inventory('pilot', (400 + PREP_X_MARGIN*2, 580), (190-PREP_X_MARGIN, -5))
    use s_inventory('robot', (400 + PREP_X_MARGIN*2, 530), (190-PREP_X_MARGIN, 515))

define PREP_X_MARGIN = 15

screen s_inventory(pilot_or_robot, size=(1.0, 1.0), offset=(0,0)):

    $ v_select = chess.ui['selected']
    $ v_inspect = chess.ui['inspected']

    # if square is None, we're not in the battlefield
    default SPCE_TWEEN_P_R = 40
    default PER_ROW = 4

    button:
        style_prefix 'sty_btn'
        at t_show_prep_screen(size)
        xysize size
        if pilot_or_robot == 'pilot':
            pos (offset[0], offset[1])
        else:
            pos (offset[0], offset[1] + SPCE_TWEEN_P_R)
        $ v_select = chess.ui['selected'] or chess.ui['inspected']
            
    if pilot_or_robot == 'pilot':
        button at t_interactive:
            # add "#0f0"
            style 'empty'
            pos (offset[0]+50, offset[1])
            xsize 350
            ysize 80
            action Function(Pilot.sort, TEAM)
            hbox:
                ypos PREP_X_MARGIN*2
                $ inventory = TEAM 
                text _("RESERVE") xalign 0.5 style 'style_purple_text' color COLOR_HIGHLIGHT() size 50
                text _("sort:\n[Pilot.sort_method]") style 'style_purple_text' color COLOR_HIGHLIGHT() text_align 0 ypos -10 size 30
    else:
        $ inventory = ROBOTS
        fixed:
            xysize size
            pos (offset[0], offset[1] + SPCE_TWEEN_P_R + 340)
            hbox:
                xalign 0.5
                add img_piece(Robot_Piece('P')) xysize(80,80) yalign 0.0
                text "=" size 60 style "style_3d_big_txt" yalign 0.5
                text "∞" size 100 style "style_3d_big_txt" yalign 0.5
    draggroup:

        if pilot_or_robot == 'pilot':
            id 'prep_draggroup_pilot'
        else:
            id 'prep_draggroup_robot'

        #
        #           PILOT OR ROBOT
        #        
        $ i = -1
        for element in inventory:
            if not element.deployed:
                $ i += 1
            $ selected = chess.ui['selected']
            drag:
                drag_name element
                xysize (100, 100)
                if element.deployed: # offscreen
                    xpos -250 + offset[0]
                else:
                    xpos i%PER_ROW*100 + offset[0] + PREP_X_MARGIN

                if pilot_or_robot == 'pilot':
                    ypos 50+20+offset[1] + 100*int(i/PER_ROW) +PREP_X_MARGIN
                    if type(v_select) == Robot_Piece:
                        if not v_select.fen in {'i', 'p'}:
                            if not v_select.type in element.can_drive:
                                draggable False
                                hovered NullAction()
                else:
                    ypos SPCE_TWEEN_P_R+offset[1] + 100*int(i/PER_ROW)+PREP_X_MARGIN
                    if isinstance(v_select, Pilot):
                        if not element.fen in {'i', 'p'}:
                            if not element.type in v_select.can_drive:
                                draggable False
                                hovered NullAction()
                                
                fixed: # sprite
                    if v_select == element:
                        at transform:
                            matrixcolor ColorizeMatrix("#7e0000","#ff0")

                    if pilot_or_robot == 'pilot':
                        if type(v_select) == Robot_Piece:
                            if not v_select.fen in {'i', 'p'}:
                                if not v_select.type in element.can_drive:
                                    at transform:
                                        matrixcolor ColorizeMatrix("#000","#999")

                        add element.img_side() xysize (1.0,1.0):
                            if element.health == 1:
                                at t_low_health
                        if Pilot.sort_method == 'default' or Pilot.sort_method == 'STA' or Pilot.sort_method == 'valuable':
                            if element.health == 1:
                                text "{b}[element.health]{size=-10}/[element.max_health]" style "big_numbers" color '#d30000' outlines [ (4, "#f00", 0, 0) ]
                            elif element.health == element.max_health:
                                text "{b}[element.health]{size=-10}/[element.max_health]" style "big_numbers" color '#87fffd' outlines [ (4, "#1d499a", 0, 0) ]
                            else:
                                text "{b}[element.health]{size=-10}/[element.max_health]" style "big_numbers"
                        elif Pilot.sort_method == 'EXP':
                            if len(element.skills['can_learn']) == 0:
                                text _("{b}{size=-15}MAX") style "big_numbers"
                            elif element.xp:
                                grid 3 3:
                                    yspacing -30
                                    for ___ in range(9):
                                        if (element.xp > ___):
                                            text '*' style 'style_3d_big_txt'

                    elif pilot_or_robot == 'robot':

                        if isinstance(v_select, Pilot):
                            if not element.type in v_select.can_drive:
                                at transform:
                                    matrixcolor ColorizeMatrix("#000","#999")
                        elif isinstance(v_select, Robot_Piece) and v_select.fen == 'i':
                            if v_select.pilot[0] is None or not element.type in v_select.pilot[0].can_drive:
                                at transform:
                                    matrixcolor ColorizeMatrix("#000","#999")
                                    
                        add f"white {c.FEN_TO_PIECE[element.fen]} {prefs.style.pieces}" xysize (1.0, 1.0)

                activated f_chessboard_activated 
                dragged f_prep_dragged
                dragging f_chessboard_dragging
                clicked f_prep_clicked
                droppable False
                hovered Function(f_inspect, element)
                unhovered SetDict(chess.ui, 'inspected', None)

        #
        #           MOVING BUTTONS, annoying because i gotta reproduce the chess_camera behavior
        #
        if chess.ui['selected'] and not v_select.deployed:
            if (pilot_or_robot == 'pilot' and isinstance(v_select, Pilot)) or (pilot_or_robot == 'robot' and isinstance(v_select, Robot_Piece)):
                for pos, move in chess.ui['moves'].items():
                    $ x = chess.POS_TO_SXY(pos)[0]
                    $ y = chess.POS_TO_SXY(pos)[1]
                    drag:
                        style 'empty'
                        drag_name pos
                        xysize(absolute(SQUARESIZE), absolute(SQUARESIZE))
                        pos (absolute(x + chess_camera.board_offset()[0]), absolute(y + chess_camera.board_offset()[1]))
                        draggable False
                        droppable True
                        hovered NullAction()
                        if move is None:
                            droppable False
                            if chess.board[pos] is c.EMPTY:
                                idle_child Transform("skin/square/square default movePiece.webp", matrixcolor=SaturationMatrix(0))
                            else:
                                idle_child Transform("skin/square/square default eatPiece.webp", matrixcolor=SaturationMatrix(0))
                        else:
                            clicked f_click_on_move_sq
                            # prevent player from moving enemy pieces
                            if move[0].color != chess.player:
                                droppable False

                            if chess.board[pos] is c.EMPTY:
                                idle_child "skin/square/square default movePiece.webp"
                            else:
                                idle_child "skin/square/square default eatPiece.webp"
                            selected_idle_child "square default highlight"
                            hover_child "square default highlight"

init python:
    def f_unprepare_all():
        for sq in chess.POS_TO_XY:
            if chess.POS_TO_XY[sq][1] <= 1 and isinstance(chess.board[sq], Robot_Piece):
                f_unprepare(chess.board[sq])

    def f_unprepare(target:Robot_Piece, pilot_only = False):
        # pilot_only: only remove pilot or remove the whole robot?
        if target is c.EMPTY:
            return False

        for pilot in target.pilot:
            if pilot is not None:
                pilot.deployed = False
        target.pilot = None

        target.check_for_pilot()
        target.setup_piece()
        if pilot_only:
            return True

        # remove the whole robot
        if not target.unmovable:
            chess.board[target.pos] = c.EMPTY
            target.deployed = False
            target.pos = None
            target.fen = DEFAULT_ROBOT[target.type]
            chess._remove_piece(target)

        if not renpy.music.is_playing(channel='sound'):
            renpy.play("sound/board/cancel.wav", channel='sound')
        # chess.ui['inspected'] = None
        f_dismiss()
        renpy.restart_interaction()

    def f_prep_drop_piece(element, pos):
        if not renpy.music.is_playing(channel='sound'):
            renpy.play("sound/board/tank.wav", channel='sound')
        element.deployed = True
        target = chess.board[pos]
        if isinstance(element, Pilot):
            # PILOT
            if chess.POS_TO_XY[pos][1] == 1: # pawn line, must be a pawn PILOT
                f_unprepare(target)
                new_piece = Robot_Piece('p', pilot=element, color=chess.player, pos=pos)
                chess.drop(new_piece, pos)
            else:
                if type(target) == Robot_Piece:
                    if any(p is not None for p in target.pilot):
                        f_unprepare(target, True) # in the case of an infantry, it will remove the infantry
                        if chess.board[pos] == c.EMPTY:
                            chess.drop(element, pos, chess.player)
                    target.pilot = element
                else:
                    chess.drop(element, pos, chess.player)

        elif type(element) == Robot_Piece:
            # ROBOT
            if element.is_pawn_or_foot():
                f_prep_drop_piece(element.pilot, pos)
                return

            elif type(target) == Robot_Piece: # is there already a robot here?
                if target.fen == 'i':
                    chess.board[pos] = c.EMPTY
                    chess._remove_piece(target)
                    element.pilot = target.pilot
                else:
                    f_unprepare(target)

            chess.drop(element, pos)

        target = chess.board[pos]
        target.check_for_pilot()
        target.setup_piece()
        chess.ui['selected'] = None
        f_select(target)

    def f_prep_click_sq(pos):
        # is it the same piece we just selected? then remove it
        if chess.POS_TO_XY[pos][1] <= 1 and chess.ui['selected'] == pos:
            f_unprepare(chess.board[pos])
            chess.ui['selected'] = None
            chess.state = 'idle'
            return

        chess.state = 'selecting'
        # we dont have anything selected
        if chess.ui['selected'] == None or type(chess.ui['selected']) == int:
            renpy.play("sound/board/select.wav")
            chess.ui['selected'] = pos

    def f_prep_click_sq_swap(pos1, pos2):
        print("SWAP")
        chess.ui['selected'] = None
        chess.state = 'idle'
        target1 = chess.board[pos1]
        target2 = chess.board[pos2]
        renpy.play('sound/misc/flip.ogg', channel='sound')
        chess.board[pos2] = target1
        chess.board[pos1] = target2
        if type(chess.board[pos1]) == Robot_Piece:
            chess.board[pos1].pos = pos1
        if type(chess.board[pos2]) == Robot_Piece:
            chess.board[pos2].pos = pos2
        f_select(chess.board[pos2])
        return
        
    def f_prep_dragged(drags, drop):
        if show_debug_menu:
            print("f_prep_dragged")
        drags[0].child.xysize = (1.0,1.0)
        drag = drags[0]
        piece = drags[0].drag_name
        if drop is None:
            drag.snap(int(drag.start_x), int(drag.start_y), delay=0.1, warper=None)
        elif chess.ui['moves'][drop.drag_name] is None: # normal snap back
            drag.snap(int(drag.start_x), int(drag.start_y), delay=0.1, warper=None)
        else: # valid move
            f_prep_drop_piece(piece, chess.ui['moves'][drop.drag_name][0].to)
            renpy.restart_interaction()
            drag.snap(int(drag.start_x), int(drag.start_y), delay=0, warper=None)

    def f_prep_clicked(drag):
        print(f"f_prep_clicked is draggable? {drag.drag_name} {drag.draggable}")
        ## if we have selected a piece on board, then we click on a pilot in reserve, put the pilot in
        ## if we have selected a infantry, then we click on a robot in reserve it can drive, put robot there
        selected = chess.ui['selected']
        piece = drag.drag_name
        if selected and selected.deployed:
            if isinstance(piece, Pilot) and not any(p is not None for p in selected.pilot) and chess.prep_can_drop_here(piece, selected.pos):
                IF_ACTIVATED = True
                f_prep_drop_piece(piece, selected.pos)
                renpy.restart_interaction()
            elif isinstance(piece, Robot_Piece) and selected.fen == 'i' and chess.prep_can_drop_here(piece, selected.pos):
                IF_ACTIVATED = True
                f_prep_drop_piece(piece, selected.pos)
                renpy.restart_interaction()
            else:
                f_select(drag.drag_name)
                renpy.restart_interaction()
        else:
            f_select(drag.drag_name)
            renpy.restart_interaction()

transform t_show_prep_screen(size):
    on show:
        xysize (0,0)
        linear 0.25 xysize (size)
    on hide:
        linear 0.25 xysize (0,0)