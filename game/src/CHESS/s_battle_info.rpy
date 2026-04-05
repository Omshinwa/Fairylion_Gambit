define INFOBOX_WIDTH = 450
define INFOBOX_HEIGHT = 210

screen s_infobox():
    if not renpy.get_screen('s_character_info'):
        fixed: #   Right Side
            if prefs.layout == "portrait":
                xysize (1.0, 300)
            else:
                xysize (INFOBOX_WIDTH, 1.0)

            if prefs.battlefield_layout_left:
                if prefs.layout == "portrait":
                    align (0.0, 0.0)
                else:
                    align (1.0, 0.5)
            else:
                if prefs.layout == "portrait":
                    align (0.0, 0.0)
                else:
                    align (0.0, 0.5)

            frame:
                style "empty"
                if prefs.layout == "portrait":
                    align (0.0, 0.0)
                $ piece = chess.ui['selected'] or chess.ui['inspected']
                if piece:
                    frame:
                        style "empty"
                        if prefs.layout == "portrait":
                            yalign 0.0
                        xysize (1.0, 1.0)
                        if prefs.layout == "landscape":

                            $ piece = chess.ui['inspected'] or chess.ui['selected']

                            if type(piece) is int: # we selected the board in prep phase
                                $ piece = chess.board[piece]
                            if type(piece) is Robot_Piece:
                                if piece.pilot:
                                    for index, pilot in enumerate(piece._pilot):
                                        if pilot is not None:
                                            vbox:
                                                use s_battlefield_pilot(pilot, index, robot=piece)
                                # elif piece.color == 1-chess.player and type(piece) == Robot_Piece:
                                #     use s_battlefield_nopilot("")
                                # else:
                                #     use s_battlefield_nopilot(_("e m p t y"))

                            
                                if piece.fen == 'i':
                                    pass
                                    # use s_battlefield_nopilot("-")
                                else:
                                    vbox:
                                        ypos 720
                                        use s_battlefield_robot(piece)
                                    
                            elif isinstance(piece, Pilot):
                                vbox:
                                    use s_battlefield_pilot(piece, 0)

screen s_info_field_layout(scale):
    frame:
        style "empty"
        at transform:
            zoom scale
        xysize (INFOBOX_WIDTH, INFOBOX_HEIGHT)
        transclude

screen s_battlefield_nopilot(text_var, scale=1):
    use s_info_field_layout(scale):
        add Solid("#3337")
        text text_var font "fonts/Venus+Carrare.otf" color "#777" size 50 outlines [ (4, "#000000", 0, 3) ] align(0.5,0.5)

screen s_battlefield_pilot(pilot, index, scale=1, robot=None):
    button:
        xsize INFOBOX_WIDTH
        ypos 200
        xpos -15
        vbox: # NAME ETC
            xfill True
            spacing 0
            hbox: # SKILLS
                ysize 64
                xalign 1.0
                spacing 5
                $ i = 0
                
                if 'preparation' in g.state:
                    for skill in pilot.can_drive:
                        if pilot.can_drive[skill] == 'p' and 'promote_q' in pilot.skills['once']:
                            add 'skill promote_q' xysize(64,64) nearest True
                        else:
                            add 'skill drive_[pilot.can_drive[skill]]' xysize(64,64) nearest True

                if 'battle' in g.state and robot and robot.fen == 'p':
                    if 'promote_q' in pilot.skills['once']:
                        add 'skill promote_q' xysize(64,64) nearest True
                    else:
                        add 'skill drive_p' xysize(64,64) nearest True


                if pilot.skills['setup']:
                    for skill in pilot.skills['setup']:
                        if len(SKILLLIST[skill].args) == 0 or robot is None or robot.fen in SKILLLIST[skill].args:
                            $ i += 1
                            if renpy.can_show('skill '+skill):
                                add 'skill [skill]' xysize(64,64) nearest True
                            else:
                                add "#0f0" xysize(64,64)
                        
            hbox: # HP EXP
                ysize 80
                xpos 70
                text _("sta") style "style_info_field"
                fixed:
                    ypos 5
                    xysize(140,70)
                    add "heart big" matrixcolor ColorizeMatrix(LOYALTY_COLORS[TRUST_TO_LOYALTY(pilot.trust)][1],LOYALTY_COLORS[TRUST_TO_LOYALTY(pilot.trust)][0]) xpos 70 ypos -7
                    text "[pilot.health]{size=-20}/[pilot.max_health]" style 'style_3d_big_txt' yalign 0.5:
                        if pilot.health == 1:
                            color "#f77"  outlines [ (3, "#f00", 0, 3) ] # '#d30000' outlines [ (3, "#f00", 0, 3) ]
                fixed:
                    xsize 20
                text _("exp") style "style_info_field"
                if not pilot.skills['can_learn']:
                    text _("MAX") style 'style_3d_txt' kerning -10 xpos -5 yalign 0.5 size 45
                else:
                    grid 4 min(2, math.ceil(pilot.xp/3)):
                        yalign 0.5
                        transpose True
                        for i in range(pilot.xp):
                            if i < 8:
                                fixed:
                                    xysize(30,30)
                                    text '*' style 'style_3d_big_txt' size 80
                    if pilot.xp == 0:
                        fixed:
                            xysize(30,30) xpos 30
                            text '-' style 'style_3d_big_txt' size 80

    #################
    ##
    ##      details on pilot
    ##
    if 'preparation' in g.state:
        frame:
            ysize 1.0
            ypos -20
            xpos -20
            style "empty"
            xsize INFOBOX_WIDTH
            vbox:
                yalign 1.0
                xsize INFOBOX_WIDTH
                spacing 10
                for skill in pilot.skills['setup']:
                    frame:
                        style "empty"
                        background "#fff7"
                        hbox:
                            xfill True
                            if len(SKILLLIST[skill].args) == 0 or robot is None or robot.fen in SKILLLIST[skill].args:
                                if renpy.can_show('skill '+ skill):
                                    add 'skill [skill]' xysize 112,112 nearest True
                                else:
                                    add 'skill none' xysize 112,112 nearest True
                                text "{size=-5}[SKILLLIST[skill].desc!i]" yalign 0.5 font 'FONT_normal' size 35:
                                    if len(SKILLLIST[skill].desc)>80:
                                        size 35

screen s_battlefield_robot(piece, scale=1):
    use s_info_field_layout(scale):
    
        button:
            xysize (1.0,1.0)
            xpos -15
            background Frame('gui/bubble_frame.webp', 55, 55, 40, 40)
            if chess.state == 'selecting':
                action Function(renpy.call_in_new_context,'l_tutorial_piece', piece)
                at t_interactive
            vbox:
                hbox: # NAME
                    xpos INFOBOX_WIDTH//10
                    ypos 8
                    text "MODEL:" yalign 0.5 size 25 font "fonts/DRAMEDYXY.ttf" color "#fff"
                    $ kerning = (8 - len(c.FEN_TO_PIECE[piece.fen]))*4
                    text "{k=[kerning]}[c.FEN_TO_PIECE[piece.fen].capitalize()]" style 'style_purple_text' color COLOR_HIGHLIGHT()
                    add 'info_button' yalign 0.5
                add Solid("#0005") xysize(0.5, 3) ypos 5 xpos INFOBOX_WIDTH//4
                hbox:
                    spacing 0
                    fixed: # SPRITE OF THE PIECE
                        # add "#0f0"
                        xysize (180,180) ypos -10
                        if renpy.can_show(f"icon {piece.fen}"):
                            add f"icon {piece.fen}" nearest True xysize (1.0,1.0)
                        else:
                            if piece.color != 2:
                                add f"[c.INDEX_TO_COLOR[piece.color]] {c.FEN_TO_PIECE[piece.fen]} merida" xysize (1.0,1.0)
                            else:
                                add f"white {c.FEN_TO_PIECE[piece.fen]} merida" xysize (1.0,1.0)

                    grid 2 2:
                        yspacing 5
                        pos (-5, 5)
                        text _("class") style "style_info_field"
                        add f"battle_ui/icon type {piece.type} outline.webp".replace("*", "star").replace("#", "hash") xysize(60,60)
                        text _("value") style "style_info_field"
                        if piece.value > 10000:
                            $ text_value = 99
                        else:
                            $ text_value = f" {int(piece.value/100)}"
                        text "{k=-10}[text_value]" style 'style_3d_big_txt' ypos 5
                
                    vbox:
                        pos (-20, 13)
                        text _("mov") font "fonts/Venus+Plomb.otf" style "style_info_field" 
                        add f"icon movement {piece.fen}" pos (1,-5) xysize (95,95)

            if show_debug_menu:
                text str(piece.pos) size 40