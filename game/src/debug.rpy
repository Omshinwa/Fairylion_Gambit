init python:
    from fairylion.mcts_debug import save_mcts_tree_json
    # from numbers_parser import Document
     
    def remove(str_or_pilot):
        piece = get(str_or_pilot)
        chess.board[piece.pos] = c.EMPTY
        chess._remove_piece(piece)

    # get('K') get('P 3')
    # to find a NEUTRAL piece, write the letter twice ie QQ for a grey queen
    def get(str_or_pilot, board=None) -> Robot_Piece:
        board = board or chess
        if type(str_or_pilot) is str or type(str_or_pilot) is int:
            return board.get(str_or_pilot)
        else: # if Pilot or Piece obj
            for piece in board.get_pieces():
                for pilot in piece._pilot:
                    if pilot and str_or_pilot.id == pilot.id:
                        return piece
        return None
    
    # DURING PREP, can be used to quickly get a drag from the BATTLE or PREP
    def get_drags(battle_or_prep='prep', child=False, field=False):

        if battle_or_prep == 'battle' or (chess.ui['selected'] and chess.ui['selected'].deployed):
            drags = renpy.get_displayable('s_battlefield', 'battle_draggroup', layer='master')
        elif isinstance(chess.ui['selected'], Pilot):
            drags = renpy.get_displayable('s_battlefield', 'prep_draggroup_pilot', layer='master')
        else:
            drags = renpy.get_displayable('s_battlefield', 'prep_draggroup_robot', layer='master')

        for drag in drags.children:
            if show_debug_menu:
                if field:
                    print(f"{drag.drag_name :   {getattr(drag, field)} }")
                else:
                    print(f"{drag.drag_name}")
            if child == drag.drag_name:
                return drag
        if child:
            raise Exception(f"even though a child ({child}) was supplied, no drag was found in {drags}")
        return drags


style style_debug_text:
    size 30 color "#FF0" ypos 0 outlines [ (4, "#050505", 0, 2) ]

default show_debug_menu = False

init python:
    import subprocess

    def f_debug_menu():
        global show_debug_menu, chess
        show_debug_menu = 1 - show_debug_menu
        g.items['undo'] = 10
        g.items['empress'] = 2
        g.items['fool'] = 3
        chess.eval_default(set_debug_value = True)

    def f_get_return_stack_info():
        result = []
        for label in renpy.get_return_stack():
            try:
                node = renpy.game.script.namemap.get(label)
                if node:
                    result.append((label, node.filename, node.linenumber))
                else:
                    result.append((label, None, None))
            except Exception:
                result.append((label, None, None))
        return result

    def f_open_in_vscode(filename, linenumber):
        try:
            subprocess.Popen(['code', '--goto', '{}:{}'.format(filename, linenumber)])
        except Exception as e:
            renpy.notify(str(e))

screen s_debug(offset=(0,0)):
    # sensitive True

    # default show_debug_menu = True
    if config.developer:
        key 'K_2' action Function(f_debug_menu)
    if show_debug_menu:
        frame:
            xalign 1.0 yalign 0.0
            background "#0008"
            padding (8, 8)
            vbox:
                spacing 2
                text "return stack:" size 18 color "#0FF"
                for label, filename, linenumber in f_get_return_stack_info():
                    if filename:
                        textbutton label:
                            text_size 16
                            text_color "#8FF"
                            text_hover_color "#FFF"
                            background None
                            action Function(f_open_in_vscode, filename, linenumber)
                    else:
                        text label size 16 color "#888"

        drag:
            pos offset
            vbox: # debug # release
                spacing -10
                style_prefix "style_debug"
                pos(180,0)

                text "[STAGE_SCENE]"

                text "renpy.get_mode(): [renpy.get_mode()]"

                hbox:
                    text "chess.side:" size 25
                    text str(chess.side)
                    text "engine.side:" size 25
                    text str(engine.side)
                hbox:
                    text "tooltip:" size 25
                    text str(GetTooltip())
                    text "g.state:" size 25
                    text str(' '.join(g.state))
                    text "chess:" size 25
                    text str(chess.state)
                hbox: 
                    text "moves:" size 25
                    for move in chess.ui["moves"]:
                        text str(move)
                # hbox: 
                #     text "arrows:" size 25
                #     for move in chess.ui["arrows"]:
                #         text str(move) 
                #         text ";" 
                
                hbox:
                    spacing 20
                    text str(chess.ui['selected'])
                    text str(chess.ui['inspected'])
                # hbox:
                #     text "positionCount:" size 25
                #     text str(ai.positionCount)

                text "[chess_camera]"

                if 'battle' in g.state:
                    button at t_interactive:
                        text "USE AI" size 80:
                            if not chess.use_engine:
                                color "#828282"
                        action ToggleField(chess, 'use_engine')
                
                    button at t_interactive:
                        align (0.8, 0.0)
                        text chess.fen style 'style_purple_text' color COLOR_HIGHLIGHT() size 15
                        action CopyToClipboard('"' + chess.fen + '"')
                
                # text "EVAL: [chess.eval()]" size 40
                # if renpy.get_screen('say'):
                #     text "get_screen(say): [renpy.get_screen('say')]"

                if 'battle' in g.state:
                    vbox:
                        text "history:" size 25
                        for index, h_move in enumerate(chess.history):
                            if index + 5 > len(chess.history):
                                text str(index) + ":" + str(h_move.move) size 25
                        spacing -10

init python:
    def load_callback():
        global chess, engine
        # so __repr__ of Move can display correctly:
        if 'chess' in globals():
            Move.engine = chess
            Simple_Piece.engine = engine
        # for i, pilot in enumerate(TEAM):
        # for pilot in Pilot.LIST:
        #     globals()[pilot] = pilot
        set_char_on_battlefield()
        init_pilots()
        relink_pilots()
        print("load_callback")
        if persistent.sacrifice_skill:
            for pilot in TEAM:
                if pilot.name == 'generic' and 'sacrifice' not in pilot.skills['can_learn']:
                    pilot.skills['can_learn'].append('sacrifice')
                    print("added sac")
        
        _console.console.history = []

    # sometimes because of rollback bs idk, the position becomes unsync    
    def set_char_on_battlefield():
        # chess.setup_board()
        for piece in chess.get_pieces():
            # chess.board[piece.pos] = piece
            #on reload, often they lose the char_on_battlefield field
            if piece.pilot:
                for pilot in piece._pilot:
                    if pilot.id in character.__dict__:
                        character.__dict__[pilot.id].char_on_battlefield = piece

    # upon reloading, link the global pilot var to the one in the save
    def relink_pilots(): 
        for pilot in TEAM:
            globals()[pilot.id] = pilot
        for pilot in DEAD_OR_DESERT:
            globals()[pilot.id] = pilot
        for robot in chess.get_pieces():
            for pilot in robot._pilot:
                if pilot is not None:
                    globals()[pilot.id] = pilot

define config.after_load_callbacks = [load_callback]
define config.reload_modules = ['fairylion']