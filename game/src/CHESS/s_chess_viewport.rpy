#  █████   █████ █████ ██████████ █████   ███   █████ ███████████     ███████    ███████████   ███████████
# ░░███   ░░███ ░░███ ░░███░░░░░█░░███   ░███  ░░███ ░░███░░░░░███  ███░░░░░███ ░░███░░░░░███ ░█░░░███░░░█
#  ░███    ░███  ░███  ░███  █ ░  ░███   ░███   ░███  ░███    ░███ ███     ░░███ ░███    ░███ ░   ░███  ░ 
#  ░███    ░███  ░███  ░██████    ░███   ░███   ░███  ░██████████ ░███      ░███ ░██████████      ░███    
#  ░░███   ███   ░███  ░███░░█    ░░███  █████  ███   ░███░░░░░░  ░███      ░███ ░███░░░░░███     ░███    
#   ░░░█████░    ░███  ░███ ░   █  ░░░█████░█████░    ░███        ░░███     ███  ░███    ░███     ░███    
#     ░░███      █████ ██████████    ░░███ ░░███      █████        ░░░███████░   █████   █████    █████   
#      ░░░      ░░░░░ ░░░░░░░░░░      ░░░   ░░░      ░░░░░           ░░░░░░░    ░░░░░   ░░░░░    ░░░░░    

screen s_chessboard_viewport(chess, *args, xinit=None, yinit=None, **kwargs):
    if not 'cutscene' in g.state:
        key 'viewport_wheelup' action Function(chess.ui['camera'].viewport_zoom_in)
        key 'viewport_wheeldown' action Function(chess.ui['camera'].viewport_zoom_out)

    $ board_size = DotDict(x = absolute(SQUARESIZE*chess.size[0]), y = absolute(SQUARESIZE*chess.size[1]))
    default do_transition = False
    viewport:
        if chess.state == "idle":
            draggable True
        else:
            draggable False
        xadjustment chess.ui['camera'].xadj yadjustment chess.ui['camera'].yadj
        xinitial xinit or 0.5
        yinitial yinit or 0.5

        fixed:
            xysize (config.screen_width*2, config.screen_height*2)
            align (0.5, 0.5)

            frame:
                align (0.5, 0.5)
                style 'empty'
                if renpy.get_screen('say'):
                    $ do_transition = True
                    $ chess.ui['camera'].center_if_changed()
                    at transform:
                        ease 0.5 zoom chess.ui['camera'].zoom*0.8 ypos 0.45
                elif 'cutscene' in g.state:
                    $ do_transition = True
                    at transform:
                        ease 0.5 zoom chess.ui['camera'].zoom ypos 0.5
                else: # when the user just normal scroll, dont have a transition
                    at transform:
                        zoom chess.ui['camera'].zoom ypos 0.5

                fixed: #    SHADOW
                    at transform:
                        blur 20 * chess_camera.zoom
                    xysize (board_size.x + 300, board_size.y + 300)
                    align (0.5, 0.5)
                    offset (8,8)
                    add "#000" xysize (board_size.x, board_size.y) align (0.5, 0.5)
                if chess.bg_board:
                    add "bg_board " + chess.bg_board xysize (board_size.x, board_size.y) align (0.5, 0.5)
                
                #######################

                use s_chess_main(chess)

                #######################

                ######################
                #
                #   # coordinates a-h 1-8
                #
                fixed:
                    xysize (board_size.x+100, board_size.y+130)
                    align (0.5, 0.5)
                    for i in range(chess.size[1]):
                        $ coord_pov = str(i+1) if chess.player else str(chess.size[1]-i)
                        text coord_pov font "fonts/cmu_b.ttf" size 40 ypos absolute((i+0.85)*SQUARESIZE) color '#fff' outlines [(2, "#222",0,0)]:
                            if prefs.battlefield_layout_left:
                                xpos 0
                            else:
                                xalign 1.0
                    for i in range(chess.size[0]):
                        $ coord_pov = INDEX_TO_LETTER[chess.size[0]-1-i] if chess.player else INDEX_TO_LETTER[i]
                        text coord_pov font "fonts/cmu_b.ttf" xanchor 0.5 size 40 yalign 1.0 xpos absolute((i+0.5)*SQUARESIZE)+50 color '#fff' outlines [(2, "#222",0,0)]
                
                add 'layer_chess_overlay'

#  ██████   ██████   █████████   █████ ██████   █████  █████████    █████████  ███████████  
# ░░██████ ██████   ███░░░░░███ ░░███ ░░██████ ░░███  ███░░░░░███  ███░░░░░███░░███░░░░░███ 
#  ░███░█████░███  ░███    ░███  ░███  ░███░███ ░███ ░███    ░░░  ███     ░░░  ░███    ░███ 
#  ░███░░███ ░███  ░███████████  ░███  ░███░░███░███ ░░█████████ ░███          ░██████████  
#  ░███ ░░░  ░███  ░███░░░░░███  ░███  ░███ ░░██████  ░░░░░░░░███░███          ░███░░░░░███ 
#  ░███      ░███  ░███    ░███  ░███  ░███  ░░█████  ███    ░███░░███     ███ ░███    ░███ 
#  █████     █████ █████   █████ █████ █████  ░░█████░░█████████  ░░█████████  █████   █████
# ░░░░░     ░░░░░ ░░░░░   ░░░░░ ░░░░░ ░░░░░    ░░░░░  ░░░░░░░░░    ░░░░░░░░░  ░░░░░   ░░░░░ 

screen s_chess_main(chess, demo=False, *args, **kwargs):
    if chess.bg_board:
        $ bg_board_lightness = get_board_color().hls[1]
        $ color_black = get_board_color().replace_lightness(0.05)
        $ color_white = get_board_color().replace_lightness(0.95)
    else:
        $ color_black = persistent.style_colors[-1]
        $ color_white = persistent.style_colors[0]

    $ tooltip = GetTooltip()

    key "mousedown_3" action Function(draw_arrow, tooltip)
    if tooltip or chess.state == "drawing":
        key "mouseup_3" action Function(f_set_arrow, tooltip)

    fixed:
        xysize (SQUARESIZE*chess.size[0], SQUARESIZE*chess.size[1])
        align (0.5, 0.5)
        #####################
        #
        #   square
        #

        add chess.img_board:
            if prefs.style.board is None and chess.bg_board:
                if bg_board_lightness > 0.5:
                    blend "multiply"
                    alpha 0.15
                elif bg_board_lightness < 0.2:
                    blend "add"
                    alpha 0.15
                else:
                    alpha 0.07
            else:
                matrixcolor ColorizeMatrix(persistent.style_colors[-2], persistent.style_colors[1])
    
        #######################
        #
        #   grid square (buttons for arrows, f_dismiss etc)
        #
        #       ::: :::     ::: :::::::::   ::::::::  :::::::::  ::::::::::: :::::::::  
        #      :+:  :+:     :+: :+:    :+: :+:    :+: :+:    :+:     :+:     :+:    :+: 
        #     +:+   +:+     +:+ +:+    +:+ +:+        +:+    +:+     +:+     +:+    +:+ 
        #    +#+    +#+     +:+ +#++:++#+  :#:        +#++:++#:      +#+     +#+    +:+ 
        #   +#+      +#+   +#+  +#+        +#+   +#+# +#+    +#+     +#+     +#+    +#+ 
        #  #+#        #+#+#+#   #+#        #+#    #+# #+#    #+#     #+#     #+#    #+# 
        # ###           ###     ###         ########  ###    ### ########### #########  
        
        vpgrid:
            align (0.5, 0.5)
            cols chess.size[0]
            rows chess.size[1]
            transpose True
            
            # Don't change the double for loop to a single pos for loop, it will mess up with squares placement.
            # We need to have squares above one another be chess.up more

            for i in range(chess.size[0]):
                for j in range(chess.size[1]):
                    if chess.player == 0:
                        $ pos = chess.XY_TO_POS[i][chess.size[1]-1-j]
                    else:
                        $ pos = chess.XY_TO_POS[chess.size[0]-1-i][j]

                    $ target = chess.board[pos]
                    button:
                        xysize (SQUARESIZE, SQUARESIZE)
                        tooltip pos
                        style 'empty'
                        if show_debug_menu:
                            text str(pos)
                        # if we select the same sq we just selected
                        if target == chess.ui['selected']:
                            add "square default highlight"
                            action Function(f_dismiss), Return()
                        elif chess.state == "selecting" or chess.ui['animation_move']:
                            action Function(f_dismiss), Return()
                        else:
                            action Function(f_dismiss)
                    
                        if 'battle' in g.state:
                            if (chess[pos] in chess.CRITICAL[0] and chess.is_sq_atk(pos, 1)) or (chess[pos] in chess.CRITICAL[1] and chess.is_sq_atk(pos, 0)):
                                add "#f005" at t_flashing

        ##########################
        #     draggroup
        #
        draggroup:
            id 'battle_draggroup'

            #       ::: ::::::::: ::::::::::: :::::::::: ::::::::  :::::::::: 
            #      :+:  :+:    :+:    :+:     :+:       :+:    :+: :+:        
            #     +:+   +:+    +:+    +:+     +:+       +:+        +:+        
            #    +#+    +#++:++#+     +#+     +#++:++#  +#+        +#++:++#   
            #   +#+     +#+           +#+     +#+       +#+        +#+        
            #  #+#      #+#           #+#     #+#       #+#    #+# #+#        
            # ###       ###       ########### ########## ########  ########## 

            for piece in chess.get_drag_list():
                if chess.ui['animation_move'] and piece == chess.ui['animation_move'].piece:
                    continue
                $ color = piece.color
                $ x = chess.POS_TO_SXY(piece.pos)[0]
                $ y = chess.POS_TO_SXY(piece.pos)[1]
                drag:
                    id ("piece_%s" % chess.POS_TO_A8(piece.pos))
                    tooltip piece.pos
                    pos (x, y)
                    xysize(SQUARESIZE, SQUARESIZE)
                    hovered Function(f_inspect, piece)
                    unhovered Function(f_uninspect)

                    draggable not chess.wait_for_enemy
                    drag_raise True
                    drag_name piece # we use .drag_name to reference the piece back
                    droppable False
                    mouse_drop True
                    drag_offscreen True
                    
                    activated f_chessboard_activated
                    dragged f_chessboard_dragged
                    dragging f_chessboard_dragging
                    clicked f_chessboard_clicked
                    alternate If(tooltip or chess.state == "drawing", Function(f_set_arrow, tooltip), Function(draw_arrow, tooltip))

                    fixed: # SPRITE
                        add img_piece(piece):
                            if chess.bg_board is None:
                                matrixcolor ColorizeMatrix(color_black, color_white)
                            # is it also in danger of dying?
                            if piece.pilot and any(pilot is not None and pilot.health == 1 for pilot in piece._pilot):
                                at t_low_health
                            if len(chess.history) == 0 and chess.move_first and piece.pilot and any(pilot is not None and 'initiative' in pilot.skills['setup'] for pilot in piece._pilot):
                                at t_highlight

                        # display the pilot in prep
                        if 'preparation' in g.state and piece.pilots:
                            $ pilot = piece.pilots[0]
                            add AlphaMask(Transform(pilot.img_side(), xysize=(360,360), crop=(-200, -150,1.0,1.0)), "triangle_mask") xysize (1.0,1.0) align (1.0,1.0)

                        # temp, display the pilot for infantry
                        elif piece.fen == 'i' and piece.pilots:
                            $ pilot = piece.pilots[0]
                            if pilot.id not in {'kallen', 'lelouch'}:
                                add AlphaMask(Transform(pilot.img_side(), xysize=(360,360), crop=(-200, -150,1.0,1.0)), "triangle_mask") xysize (1.0,1.0) align (1.0,1.0)
                    
                        if show_debug_menu:
                            if type(piece) == Robot_Piece:
                                if not piece.debug_value is None:
                                    text str(piece.debug_value) xalign 0.5 ypos SQUARESIZE-50 style 'style_purple_text' color COLOR_HIGHLIGHT()
                                else:
                                    text str(piece.pid) pos(SQUARESIZE-50,SQUARESIZE-50) color "#f0f"

            #           MOVING BUTTONS, hide it during prep sometimes
            #
            #       ::: ::::::::   ::::::::  :::    :::     :::     :::::::::  :::::::::: 
            #      :+: :+:    :+: :+:    :+: :+:    :+:   :+: :+:   :+:    :+: :+:        
            #     +:+  +:+        +:+    +:+ +:+    +:+  +:+   +:+  +:+    +:+ +:+        
            #    +#+   +#++:++#++ +#+    +:+ +#+    +:+ +#++:++#++: +#++:++#:  +#++:++#   
            #   +#+           +#+ +#+  # +#+ +#+    +#+ +#+     +#+ +#+    +#+ +#+        
            #  #+#     #+#    #+# #+#   +#+  #+#    #+# #+#     #+# #+#    #+# #+#        
            # ###       ########   ###### ### ########  ###     ### ###    ### ########## 

            if demo or not 'preparation' in g.state or (chess.ui['selected'] and chess.ui['selected'].deployed) or chess.state == 'idle':
                for pos, move in chess.ui['moves'].items():
                    $ x = chess.POS_TO_SXY(pos)[0]
                    $ y = chess.POS_TO_SXY(pos)[1]
                    drag:
                        # tooltip pos
                        id ("move_%s" % chess.POS_TO_A8(pos))
                        drag_name pos
                        xysize(SQUARESIZE, SQUARESIZE)
                        pos (x, y)
                        draggable False
                        droppable True
                        hovered NullAction()
                        # alternate If(chess.state == "drawing", Function(f_set_arrow, pos), Function(draw_arrow, pos))

                        if move is None: # this means it's an illegal move
                            droppable False
                            if chess.board[pos] is c.EMPTY:
                                idle_child Transform("skin/square/square default movePiece.webp", matrixcolor=SaturationMatrix(0))
                            else:
                                idle_child Transform("skin/square/square default eatPiece.webp", matrixcolor=SaturationMatrix(0))
                        else:
                            clicked f_click_on_move_sq
                            if show_debug_menu:
                                pass
                            # prevent player from moving enemy pieces
                            elif 'battle' in g.state and (move[0].color != chess.player or move[0].color != chess.side):
                                droppable False
                                clicked None

                            if chess.board[pos] is c.EMPTY:
                                idle_child "skin/square/square default movePiece.webp"
                            else:
                                idle_child "skin/square/square default eatPiece.webp"
                            selected_idle_child "square default highlight"
                            hover_child "square default highlight"
            
            drag: # for the whole board, check if the drag is on board
                style 'empty'
                drag_name None
                fixed:
                    if show_debug_menu:
                        add "#0f01"
                xysize(absolute(SQUARESIZE*chess.size[0]), absolute(SQUARESIZE*chess.size[1]))
                draggable False
                droppable True

        #
        #       ANIMATED PIECE
        #
        
        if chess.ui['animation_move']:
            if chess.ui['animation_move'].capture:
                $ piece = chess.ui['animation_move'].capture
                add img_piece(piece):
                    pos chess.POS_TO_SXY(piece.pos, 0.5)

            add img_piece(chess.ui['animation_move'].piece):
                at transform:
                    pos chess.ui['animation_move'].fr
                    linear chess.ui['animation_move'].time pos chess.ui['animation_move'].to
                        

        #       :::  :::     :::::::::  :::::::::   ::::::::  :::       :::  ::::::::  
        #      :+: :+: :+:   :+:    :+: :+:    :+: :+:    :+: :+:       :+: :+:    :+: 
        #     +:+ +:+   +:+  +:+    +:+ +:+    +:+ +:+    +:+ +:+       +:+ +:+        
        #    +#+ +#++:++#++: +#++:++#:  +#++:++#:  +#+    +:+ +#+  +:+  +#+ +#++:++#++ 
        #   +#+  +#+     +#+ +#+    +#+ +#+    +#+ +#+    +#+ +#+ +#+#+ +#+        +#+ 
        #  #+#   #+#     #+# #+#    #+# #+#    #+# #+#    #+#  #+#+# #+#+#  #+#    #+# 
        # ###    ###     ### ###    ### ###    ###  ########    ###   ###    ########  

        for arrow in chess.ui["arrows"]:
            # if arrow[0] is None: # why would it be none? janvier 2025 
            #     continue
            $ x = chess.POS_TO_SXY(arrow[0],0.5)[0]
            $ y = chess.POS_TO_SXY(arrow[0],0.5)[1]
            $ x2 = chess.POS_TO_SXY(arrow[1],0.5)[0]
            $ y2 = chess.POS_TO_SXY(arrow[1],0.5)[1]
            if arrow[0] == arrow[1]:
                add "arrow circle drawn":
                    pos (x, y) anchor (0.5, 0.5)
                    alpha 0.5
                    matrixcolor ColorizeMatrix("#000",COLOR_HIGHLIGHT())
            else:
                add "i_arrow drawn":
                    pos (x, y)
                    anchor (int(SQUARESIZE/2), int(SQUARESIZE/2))
                    transform_anchor True
                    alpha 0.5
                    rotate math.degrees(math.atan2((y2-y), (x2-x)))
                    xsize absolute(math.sqrt((x2-x)**2 + (y2-y)**2)+SQUARESIZE)
                    ysize SQUARESIZE
                    matrixcolor ColorizeMatrix("#000",COLOR_HIGHLIGHT())

        if chess.ui["drawing"] and tooltip:
            $ arrow = chess.ui["drawing"]
            $ x = chess.POS_TO_SXY(arrow,0.5)[0]
            $ y = chess.POS_TO_SXY(arrow,0.5)[1]
            $ x2 = chess.POS_TO_SXY(tooltip,0.5)[0]
            $ y2 = chess.POS_TO_SXY(tooltip,0.5)[1]
            if arrow == tooltip:
                add "arrow circle drawing":
                    pos (x, y) anchor (0.5, 0.5)
                    alpha 0.5
                    matrixcolor ColorizeMatrix("#000",COLOR_HIGHLIGHT())
            else:
                add "i_arrow drawing":
                    pos (x, y)
                    anchor (int(SQUARESIZE/2), int(SQUARESIZE/2))
                    transform_anchor True
                    alpha 0.5
                    rotate math.degrees(math.atan2((y2-y), (x2-x)))
                    xsize absolute(math.sqrt((x2-x)**2 + (y2-y)**2)+SQUARESIZE)
                    ysize SQUARESIZE
                    matrixcolor ColorizeMatrix("#000",COLOR_HIGHLIGHT())