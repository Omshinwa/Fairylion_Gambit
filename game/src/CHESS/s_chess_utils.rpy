
#  █████ ██████   ██████   █████████    
# ░░███ ░░██████ ██████   ███░░░░░███   
#  ░███  ░███░█████░███  ███     ░░░    
#  ░███  ░███░░███ ░███ ░███            
#  ░███  ░███ ░░░  ░███ ░███    █████   
#  ░███  ░███      ░███ ░░███  ░░███    
#  █████ █████     █████ ░░█████████  ██
# ░░░░░ ░░░░░     ░░░░░   ░░░░░░░░░  ░░ 

image i_arrow drawing = Frame("arrow line drawing",left=80,right=125,bottom=128)
image i_arrow drawn = Frame("arrow line drawn",left=80,right=125,bottom=128)

#  ███████████ ███████████     █████████   ██████   █████  █████████    
# ░█░░░███░░░█░░███░░░░░███   ███░░░░░███ ░░██████ ░░███  ███░░░░░███   
# ░   ░███  ░  ░███    ░███  ░███    ░███  ░███░███ ░███ ░███    ░░░    
#     ░███     ░██████████   ░███████████  ░███░░███░███ ░░█████████    
#     ░███     ░███░░░░░███  ░███░░░░░███  ░███ ░░██████  ░░░░░░░░███   
#     ░███     ░███    ░███  ░███    ░███  ░███  ░░█████  ███    ░███   
#     █████    █████   █████ █████   █████ █████  ░░█████░░█████████  ██
#    ░░░░░    ░░░░░   ░░░░░ ░░░░░   ░░░░░ ░░░░░    ░░░░░  ░░░░░░░░░  ░░ 

transform t_blend_top:
    blend "max"
    matrixcolor ColorizeMatrix(COLOR_HIGHLIGHT(2),COLOR_HIGHLIGHT(2))
    # blur 10

transform t_blend_bottom:
    blend 'multiply'
    matrixcolor ColorizeMatrix(COLOR_HIGHLIGHT(1),COLOR_HIGHLIGHT(1))
    # blur 10

transform t_text_scroll(up=1):
    block:
        ypos -2000 + 1000*up
        linear 2 ypos -2000
        pause 1
        linear 2 ypos -2000 + 1000*up*-1
        pause 1
        repeat

transform t_eval_anim(old_score):
    on show:
        ysize 0.5 - old_score/2500 
        linear abs(old_score-chess.get_advantage())/2000 ysize 0.5 - chess.get_advantage()/2500

#  ███████████ █████  █████ ██████   █████   █████████    
# ░░███░░░░░░█░░███  ░░███ ░░██████ ░░███   ███░░░░░███   
#  ░███   █ ░  ░███   ░███  ░███░███ ░███  ███     ░░░    
#  ░███████    ░███   ░███  ░███░░███░███ ░███            
#  ░███░░░█    ░███   ░███  ░███ ░░██████ ░███            
#  ░███  ░     ░███   ░███  ░███  ░░█████ ░░███     ███   
#  █████       ░░████████   █████  ░░█████ ░░█████████  ██
# ░░░░░         ░░░░░░░░   ░░░░░    ░░░░░   ░░░░░░░░░  ░░ 


default IF_ACTIVATED = False

init python:
    def f_set_arrow(pos):
        if chess.ui["drawing"] and pos is not None:
            if (chess.ui["drawing"], pos) in chess.ui["arrows"]:
                chess.ui["arrows"].remove((chess.ui["drawing"], pos))
            else:
                chess.ui["arrows"].add((chess.ui["drawing"], pos))
        chess.ui["drawing"] = None
        if chess.state == 'selecting':
            f_dismiss(skip_sound=True)
        chess.state = "idle"
        return

    def draw_arrow(pos):
        if pos == None:
            return
        if chess.state == 'selecting':
            f_dismiss(skip_sound=True)
        chess.ui['selected'] = None
        chess.ui["drawing"] = pos
        chess.state = "drawing"
        return

    def f_inspect(piece):
        if chess.ui['selected'] != piece and chess.ui['inspected'] != piece:
            renpy.play("sound/board/cursor.wav", 'sound')
            chess.ui['inspected'] = piece
            if isinstance(piece, Robot_Piece) and 'preparation' in g.state and piece.deployed and chess.state == 'idle':
                chess.ui["moves"] = piece.get_range()
        return

    def f_uninspect():
        chess.ui['inspected'] = None
        if 'preparation' in g.state and chess.state == 'idle':
            chess.clean_moves()
        return

    def f_select(piece):
        if not isinstance(piece, Simple_Piece) and not isinstance(piece, Pilot):
            return
        if chess.state == 'selecting' and piece == chess.ui['selected']:
            return
        if chess.ui['animation_move']:
            return
            # engine.copy(chess)
        if chess.ui['selected']!=piece: # not renpy.music.is_playing('sound') and 
            renpy.play("sound/board/select.wav", 'audio')
        chess.state = "selecting"
        
        # click on the piece: inspect the piece and show the range
        chess.clean_moves()
        chess.ui['selected'] = piece

        if 'battle' in g.state:
            squares = piece.get_range()
        
            if piece.color != 2:
                for i in squares:
                    if chess.is_move_legal_ui(squares[i][0]):
                        chess.undo()
                        chess.ui["moves"][i] = squares[i]
                    else:
                        chess.ui["moves"][i] = None
            
            elif piece.color == 2:
                for i in squares:
                    chess.ui["moves"][i] = None
                    
        elif 'preparation' in g.state:
            
            # select a piece on your side
            if isinstance(piece, Robot_Piece) and piece.deployed and chess.POS_TO_XY_POV(piece.pos)[1] >= 2:
                return
            for x in range(chess.size[0]):
                for y in range(chess.size[1]):
                    pos = chess.XY_TO_POS[x][y]

                    if chess.POS_TO_XY_POV(pos)[1] < 2:
                        if chess.prep_can_drop_here(piece, pos):
                            chess.ui["moves"][pos] = [Move(piece, fr=chess.XY_TO_POS[0][0], to=pos, color=chess.player)]
                        else:
                            chess.ui["moves"][pos] = None
        return
    
    def f_dismiss(skip_sound = False):
        if chess.state == 'selecting' and 'cutscene' not in g.state and not skip_sound:
            # if not renpy.music.is_playing(channel='sound'):
            renpy.play("sound/board/cancel.wav", channel='audio')
        chess.state = "idle"
        chess.ui['animation_move'] = None
        chess.ui['inspected'] = None
        chess.ui['selected'] = None
        chess.clean_arrows()
        chess.clean_moves()

#  ██████████                                    █████                             
# ░░███░░░░███                                  ░░███                              
#  ░███   ░░███ ████████   ██████    ███████  ███████  ████████   ██████  ████████ 
#  ░███    ░███░░███░░███ ░░░░░███  ███░░███ ███░░███ ░░███░░███ ███░░███░░███░░███
#  ░███    ░███ ░███ ░░░   ███████ ░███ ░███░███ ░███  ░███ ░░░ ░███ ░███ ░███ ░███
#  ░███    ███  ░███      ███░░███ ░███ ░███░███ ░███  ░███     ░███ ░███ ░███ ░███
#  ██████████   █████    ░░████████░░███████░░████████ █████    ░░██████  ░███████ 
# ░░░░░░░░░░   ░░░░░      ░░░░░░░░  ░░░░░███ ░░░░░░░░ ░░░░░      ░░░░░░   ░███░░░  
#                                   ███ ░███                              ░███     
#                                  ░░██████                               █████    
#                                   ░░░░░░                               ░░░░░     
    def f_click_on_move_sq(drag):
        if 'battle' in g.state:
            renpy.call('l_player_move', chess.ui['moves'][drag.drag_name])
        elif 'preparation' in g.state:
            if chess.state == 'selecting':
                if chess.ui['selected'].deployed:
                    # if we reclick on the same piece, it unprepares it
                    if drag.drag_name == chess.ui['selected'].pos:
                        f_unprepare(chess.ui['selected'])
                        return
                drags = [ get_drags(child=chess.ui['selected']) ]
                f_chessboard_dragged(drags, drag)

    def f_chessboard_activated(drags):
        global IF_ACTIVATED
        IF_ACTIVATED = False
        if 'battle' in g.state:
            if chess.state == 'selecting' and drags[0].drag_name == chess.ui['selected']:
                IF_ACTIVATED = True
            f_select(drags[0].drag_name)
            renpy.restart_interaction()
        elif 'preparation' in g.state:
            if chess.state == 'idle':
                f_select(drags[0].drag_name)
                IF_ACTIVATED = True
                renpy.restart_interaction()
            elif chess.state == 'selecting':
                if not drags[0].draggable:
                    dismiss()

    def f_chessboard_dragging(drags):
        drags[0].grab_x = SQUARESIZE/2
        drags[0].grab_y = SQUARESIZE/2
        drags[0].child.xysize = (1.2,1.2)
        if 'preparation' in g.state:
            global IF_ACTIVATED
            if not IF_ACTIVATED:
                f_select(drags[0].drag_name)
                renpy.restart_interaction()

    def f_chessboard_clicked(drag):
        # Click is a callback after activated.
        # DISMISS when ACTIVATED was called when we already selected the same piece
        global IF_ACTIVATED
        if 'battle' in g.state:
            if IF_ACTIVATED:
                f_dismiss()
                del IF_ACTIVATED
            renpy.call('l_gameLoop_everyInteraction') # maybe only on battle
        else:
            if not IF_ACTIVATED: #if we're doing only a click
                pos = drag.drag_name.pos
                if pos in chess.ui['moves'] and chess.ui['moves'][pos]:
                    f_click_on_move_sq(get_drags('battle', child=drag.drag_name.pos))
                else:
                    if isinstance(chess.board[pos], Robot_Piece):
                        f_select(chess.board[pos])
                IF_ACTIVATED = False
            renpy.restart_interaction()
        return
    
    def f_chessboard_dragged(drags, drop):
        drags[0].child.xysize = (1.0,1.0)
        drag = drags[0]
        piece = drags[0].drag_name
        
        if 'battle' in g.state:
            if drop is None or drop.drag_name is None: # invalid target, removed chess.ui['moves'][drop.drag_name] is None
            # now we just snapback on anywhere on the board
                x = chess.POS_TO_SXY(piece.pos)[0]
                y = chess.POS_TO_SXY(piece.pos)[1]
                drag.snap(x, y, delay=0.1, warper=None)
                renpy.call('l_gameLoop_everyInteraction') # maybe only on battle
            else:
                renpy.call('l_player_move', chess.ui['moves'][drop.drag_name])
        
        elif 'preparation' in g.state:
            # offboard: remove it (if movable)
            if (isinstance(piece, Robot_Piece) and not piece.unmovable) and drop is None:
                print(f"REMOVE moving {drag.drag_name}")
                drag.snap(absolute(drag.start_x), absolute(drag.start_y), delay=0, warper=None)
                f_unprepare(piece)
            # greyed square
            elif drop is None or drop.drag_name is None: # normal snap back
                print(f"NONE moving {drag.drag_name}")
                drag.snap(absolute(drag.start_x), absolute(drag.start_y), delay=0.1, warper=None)
            else: # valid move
                print(f"VALID moving {drag.drag_name}")

                dest = chess.ui['moves'][drop.drag_name][0].to

                if isinstance(piece, Robot_Piece) and piece.deployed and isinstance(chess.board[dest], Robot_Piece):
                    if piece.pos == dest:
                        f_chessboard_dragged(drags, DotDict(drag_name=None))
                        return
                    f_prep_click_sq_swap(piece.pos, dest)
                    renpy.restart_interaction()
                    return

                if piece.deployed: # didnt select inventory
                    x, y = chess.POS_TO_SXY(drop.drag_name)
                    drag.snap(x, y, delay=0.1, warper=None)

                renpy.invoke_in_new_context(renpy.pause, 0.1, modal=False)

                if piece.deployed: # didnt select inventory
                    chess.board[piece.pos] = c.EMPTY
                    chess._remove_piece(piece)

                f_prep_drop_piece(piece, dest)

            renpy.restart_interaction()

#              ███ █████  █████ ███████████ █████ █████        █████████ 
#            ███░ ░░███  ░░███ ░█░░░███░░░█░░███ ░░███        ███░░░░░███
#          ███░    ░███   ░███ ░   ░███  ░  ░███  ░███       ░███    ░░░ 
#        ███░      ░███   ░███     ░███     ░███  ░███       ░░█████████ 
#      ███░        ░███   ░███     ░███     ░███  ░███        ░░░░░░░░███
#    ███░          ░███   ░███     ░███     ░███  ░███      █ ███    ░███
#  ███░            ░░████████      █████    █████ ███████████░░█████████ 
# ░░░               ░░░░░░░░      ░░░░░    ░░░░░ ░░░░░░░░░░░  ░░░░░░░░░  
init python:
    import math

    # doing this whole cache thing because it was kinda laggy when you select the moves
    # with 32 pieces, debug mode F2 on and 'grass'
    def get_board_color(x=0,y=0) -> Color:
        if chess.bg_board:
            cached = getattr(chess, '_bg_board_color_cache', None)
            key = (chess.bg_board, chess.bg_board_pixel_coord)
            if cached is None or cached[0] != key:
                color = Color(renpy.load_surface("skin/square/bg_board "+chess.bg_board+".webp").get_at(chess.bg_board_pixel_coord))
                chess._bg_board_color_cache = (key, color)
                chess._bg_board_derived_cache = None
                return color
            return cached[1]
        return None

    def get_board_colors():
        # Returns (lightness, color_black, color_white) for chess.bg_board, cached.
        base = get_board_color()
        if base is None:
            return None
        cached = getattr(chess, '_bg_board_derived_cache', None)
        if cached is None:
            lightness = base.hls[1]
            color_black = base.replace_lightness(0.05)
            color_white = base.replace_lightness(0.95)
            cached = (lightness, color_black, color_white)
            chess._bg_board_derived_cache = cached
        return cached

    # return the color highlight
    def COLOR_HIGHLIGHT(index:int = None) -> Color:
        index = index or -2
        if chess and chess.bg_board:
            color = get_board_color().replace_lightness(0.65) 
        else:
            color =  Color(persistent.style_colors[index])
        return color.rotate_hue(0.5).replace_hls_saturation(1.0)

    # apply a transform to the image given as arg
    def img_square(str, **kwargs):
        return Transform(str, align=(0.5, 0.5), xysize=(SQUARESIZE, SQUARESIZE), **kwargs)

    # Offset for POS_TO_SXY when placing a piece sprite, matching the anchor used in img_piece.
    def PIECE_ALIGNMENT():
        if prefs.style.pieces == 'robot':
            return (0.5, 1.0)
        return (0.5, 0.5)

    def img_piece(piece):
        if piece.fen == "i": #inside a robot
            if piece._pilot[0] and piece._pilot[0].id in {'kallen', 'lelouch'} :
                return img_square(Composite(
                        (1.0, 1.0),
                        (25, 33), Transform(f'body {piece._pilot[0].id}', zoom=.15),
                        (35, 12), Transform(f'head {piece._pilot[0].id}', zoom=.15)), matrixcolor=IdentityMatrix())
            return img_square(Composite(
                    (SQUARESIZE, SQUARESIZE),
                    (40, 40), Transform('body', zoom=2, nearest=True)), matrixcolor=IdentityMatrix())

        if prefs.style.pieces in {'merida'}:
            extension = '.svg'
        elif prefs.style.pieces == 'robot':
            if piece.fen in {'p', 'n'}:
                if piece.color == 0:
                    return Transform(GradientMap(f'robot {piece.fen}', 'pale god'), align=(0.5, 1.0), xzoom=1, xysize=(int(SQUARESIZE*1.4), int(SQUARESIZE*1.4)),)
                else:
                    return Transform(GradientMap(f'robot {piece.fen}', 'noir'), align=(0.5, 1.0), xzoom=-1, xysize=(int(SQUARESIZE*1.4), int(SQUARESIZE*1.4)),)
            return Transform('img_rig_piece idle', align=(0.5, 1.0), xysize=(int(SQUARESIZE*1.5), int(SQUARESIZE*1.5)),)
        else:
            extension = '.webp'
        
        # gotta specify xzoom=1, here because robots have -1 as zoom. 
        if piece.color == 2:
            return img_square(Image(f"/skin/pieces/{prefs.style.pieces}/white {c.FEN_TO_PIECE[piece.fen]} {prefs.style.pieces}{extension}", dpi=288), xzoom=1, matrixcolor=ColorizeMatrix("#555", "#aaa"))
        elif piece.movement == None and piece.fen != 'k':
            if piece.color:
                return img_square(Image(f"/skin/pieces/{prefs.style.pieces}/black {c.FEN_TO_PIECE[piece.fen]} {prefs.style.pieces}{extension}", dpi=288), xzoom=1, matrixcolor=ColorizeMatrix("#0c157a", "#dcfffe"))
            else:
                return img_square(Image(f"/skin/pieces/{prefs.style.pieces}/white {c.FEN_TO_PIECE[piece.fen]} {prefs.style.pieces}{extension}", dpi=288), xzoom=1, matrixcolor=ColorizeMatrix("#01d", "#dcfffe"))
        else:
            return img_square(Image(f"/skin/pieces/{prefs.style.pieces}/{c.COLOR_TO_STR[piece.color]} {c.FEN_TO_PIECE[piece.fen]} {prefs.style.pieces}{extension}", xzoom=1, dpi=288), matrixcolor=SaturationMatrix(1.0)) #matrixcolor=IdentityMatrix()

