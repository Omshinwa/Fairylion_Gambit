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
    if not_done('tuto_loyalty'): # see src/loyalty.rpy
        call l_tutorial('loyalty')

    play music "music/preparation.mp3"

    label .loop:
        call screen s_pauseScreen(hard_stop=True)
    jump .loop
    return

label l_start_battle():
    $ autosave('battle')
    $ renpy.stop_skipping()

    if 'preparation' in g.state: # FOR NON PREDEPLOYED
        if not chess.PIECELIST[chess.player]['K']:
            "You need a King to lead your army."
            return
        if chess.get_pieces(2):
            "The [c.FEN_TO_PIECE[chess.get_pieces(2)[0].fen].capitalize()] on [chess.POS_TO_A8(chess.get_pieces(2)[0].pos).upper()] doesn't have any pilot. You won't be able to move it. Double click to store it."
            menu:
                "Start Deployement anyway?"
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
    $ character_rules_battle_start() # see src/character_rules.rpy
    $ rewards_battle_start() # see src/battle_rewards.rpy
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
        # add 'i_start'
        null height 20
        if game.custom_objective:
            text "Objective:\n\n" + game.custom_objective size 100 style 'style_3d_txt' xalign 0.5 xsize 1000
        elif chess.goal == None:
            text "Objective:\n\n Checkmate the KING" size 100 style 'style_3d_txt' xalign 0.5 xsize 1000
        elif chess.goal == 'kill':
            text "Objective:\n\n Eliminate the enemy." size 100 style 'style_3d_txt' xalign 0.5 xsize 1000

screen s_preparation_overlay(): 
    use s_inventories()

    if ship_unlocked and not rogue: # who doesn't fight spends the day in a room of the ship (src/ship.rpy)
        # under the pilot reserve: with 16 pilots (4 rows) the grid ends at y=505, the pilot panel at y=575.
        # Drawn here, after s_inventories, so the robot panel (starts at y=555) doesn't cover it.
        button at t_interactive:
            style_prefix 'sty_btn'
            xcenter 190 + 200 # middle of the pilot grid (s_inventory xpos + 4*100/2)
            ypos 505 + 5
            ysize 65
            padding (40, 0)
            text _("SHIP") size 40
            action Function(f_dismiss), Call('l_ship')

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
            action Function(Pilot.sort, TEAM)
            style_prefix 'sty_btn'
            xysize(INFOBOX_WIDTH-50,110)
            anchor(0, 0)
            pos (190, 0)

            hbox:
                ypos PREP_X_MARGIN*2 - 40
                $ inventory = [pilot for pilot in TEAM if ship_room_of(pilot) is None] # pilots in a ship room don't fight (src/ship.rpy)
                text _("Reserve") xalign 0.5 size 50
                text _("sort:\n[Pilot.sort_method]") text_align 0 yoffset -4 size 30

    else:
        # story mode: the PAWN robots are counted below, a pilot dropped on the pawn row takes one (src/story_battles.rpy)
        $ inventory = ROBOTS if rogue else [robot for robot in ROBOTS if robot.type != '^']
        fixed:
            xysize size
            pos (offset[0], offset[1] + SPCE_TWEEN_P_R + 340)
            hbox:
                xalign 0.5
                add "white pawn merida" xysize(80,80) yalign 0.0
                text "=" size 60 style "style_3d_big_txt" yalign 0.5
                if rogue: # unlimited pawns
                    text "∞" size 100 style "style_3d_big_txt" yalign 0.5
                else:
                    text str(len(story_pawns())) size 70 style "style_3d_big_txt" yalign 0.5
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
                    id getattr(element, 'id', element)
                    ypos 75+20+offset[1] + 100*int(i/PER_ROW) +PREP_X_MARGIN
                    if type(v_select) == Robot_Piece:
                        if v_select.fen != 'p':
                            if not pilot_fits_robot(element, v_select.type):
                                draggable False
                                hovered NullAction()
                else:
                    ypos SPCE_TWEEN_P_R+offset[1] + 100*int(i/PER_ROW)+PREP_X_MARGIN
                    if isinstance(v_select, Pilot):
                        if element.fen != 'p':
                            if not pilot_fits_robot(v_select, element.type):
                                draggable False
                                hovered NullAction()
                                
                fixed: # sprite
                    if v_select == element:
                        at transform:
                            matrixcolor ColorizeMatrix("#7e0000","#ff0")

                    if pilot_or_robot == 'pilot': # greyed: can't drive the selected robot. see src/PILOT_screen.rpy
                        use s_pilot_icon(element, greyed=(type(v_select) == Robot_Piece and v_select.fen != 'p' and not pilot_fits_robot(element, v_select.type)))

                    elif pilot_or_robot == 'robot':

                        if isinstance(v_select, Pilot):
                            if not pilot_fits_robot(v_select, element.type):
                                at transform:
                                    matrixcolor ColorizeMatrix("#000","#999")

                        add f"white {c.FEN_TO_PIECE[element.fen]} merida" xysize (1.0, 1.0)

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
                    $ _zoom = chess_camera.zoom
                    $ _boc = chess_camera.board_offset_center()
                    $ _drag_x = _boc[0] + 960 + (x - SQUARESIZE * chess.size[0] / 2.0) * _zoom
                    $ _drag_y = _boc[1] + 540 + (y - SQUARESIZE * chess.size[1] / 2.0) * _zoom
                    $ _sq_size = SQUARESIZE * _zoom
                    drag:
                        draggable False
                        droppable True
                        style 'empty'
                        drag_name pos
                        xysize(absolute(_sq_size), absolute(_sq_size))
                        pos (absolute(_drag_x), absolute(_drag_y))
                        hovered NullAction()
                        if move is None:
                            droppable False
                            if chess.board[pos] is c.EMPTY:
                                idle_child Transform("skin/square/square default movePiece.webp", matrixcolor=SaturationMatrix(0), zoom=_zoom)
                            else:
                                idle_child Transform("skin/square/square default eatPiece.webp", matrixcolor=SaturationMatrix(0), zoom=_zoom)
                        else:
                            clicked f_click_on_move_sq
                            # prevent player from moving enemy pieces
                            if move[0].color != chess.player:
                                droppable False

                            if chess.board[pos] is c.EMPTY:
                                idle_child Transform("skin/square/square default movePiece.webp", zoom=_zoom)
                            else:
                                idle_child Transform("skin/square/square default eatPiece.webp", zoom=_zoom)
                            selected_idle_child Transform("square default highlight", zoom=_zoom)
                            hover_child Transform("square default highlight", zoom=_zoom)


init python:
    def f_unprepare_all():
        for sq in chess.POS_TO_XY:
            if chess.POS_TO_XY[sq][1] <= 1 and isinstance(chess.board[sq], Robot_Piece):
                f_unprepare(chess.board[sq])

    def f_unprepare(target:Robot_Piece, pilot_only = False):
        # pilot_only: only remove pilot or remove the whole robot?
        if target is c.EMPTY:
            return False

        for pilot in target.pilots:
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
        # Yellow and Grey loyalty: won't be deployed if they can die (see src/loyalty.rpy)
        if isinstance(element, Pilot) and not element.deployed and not loyalty_can_deploy(element):
            loyalty_refuse_notify(element)
            return
        # story mode: no PAWN robot left for the pawn row (src/story_battles.rpy)
        if isinstance(element, Pilot) and chess.POS_TO_XY[pos][1] == 1 and not story_pawn_free(pos):
            renpy.notify(_("No PAWN left. More CHESSMEN can be bought from the United Nations."))
            return
        # no lone pilot (INFANTRY) in the deployment phase: on the back row, a pilot needs a robot
        if isinstance(element, Pilot) and chess.POS_TO_XY[pos][1] == 0 and type(chess.board[pos]) != Robot_Piece:
            return
        if not renpy.music.is_playing(channel='sound'):
            renpy.play("sound/board/tank.wav", channel='sound')
        element.deployed = True
        target = chess.board[pos]
        if isinstance(element, Pilot):
            # PILOT
            if chess.POS_TO_XY[pos][1] == 1: # pawn line, must be a pawn PILOT
                f_unprepare(target)
                if rogue: # unlimited pawns
                    new_piece = Robot_Piece('p', pilot=element, color=chess.player, pos=pos)
                else: # story mode: one of the player's PAWN robots (src/story_battles.rpy)
                    new_piece = story_pawns()[0]
                    new_piece.pilot = element
                    new_piece.color = chess.player
                    new_piece.deployed = True
                chess.drop(new_piece, pos)
            elif target.type == '*' and target.pilots and target.has_pilot_room() and element not in target.pilots:
                # a Queen with a free seat: sit next to the first pilot, to co-drive it (src/queen_co_drive.rpy)
                seats = list(target._pilot)
                seats[seats.index(None)] = element
                target.pilot = seats
            else:
                if target.pilots:
                    f_unprepare(target, True)
                target.pilot = element

        elif type(element) == Robot_Piece:
            # ROBOT. A pawn moved along the pawn row keeps its own robot, so no PAWN is used up
            if type(target) == Robot_Piece: # is there already a robot here?
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
        selected = chess.ui['selected']
        piece = drag.drag_name
        if selected and selected.deployed:
            if isinstance(piece, Pilot) and not selected.pilots and chess.prep_can_drop_here(piece, selected.pos):
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