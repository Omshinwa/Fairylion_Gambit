default prefs.battlefield_layout_left = True #left/right

screen s_battlefield(*args, **kwargs): 
    zorder -2
    layer 'master'

    use s_chess_dismiss()
    use s_chessboard_bg(*args, **kwargs)
    fixed:
        xysize (config.screen_width, config.screen_height)

        if 'preparation' in g.state:
            at blur_masked(sigma=16.0, mask="mask_prepbox")
        elif 'battle' in g.state or 'preparation' in g.state and not 'tutorial' in game.level: # s_chessboard_overlay is shown
            at blur_masked(sigma=16.0, mask="mask_itembar")
        else:
            at blur_masked(sigma=16.0, mask="mask_sides")


        use s_chessboard_viewport(chess)
    if 'preparation' in g.state:
        use s_preparation_overlay()
    showif 'battle' in g.state or 'preparation' in g.state: #or ('cutscene' in g.state and game.is_over == "loss"):
        if not 'tutorial' in game.level:
            use s_chessboard_overlay()

    if renpy.get_mode() == 'pause' or renpy.get_mode() == 'say' or game.is_over:
        button: # DISMISS
            xysize 1.0,1.0
            if config.developer:
                text "RETURN" color "#0f0"
            action Return()

#              ███ ███████████    █████████ 
#            ███░ ░░███░░░░░███  ███░░░░░███
#          ███░    ░███    ░███ ███     ░░░ 
#        ███░      ░██████████ ░███         
#      ███░        ░███░░░░░███░███    █████
#    ███░          ░███    ░███░░███  ░░███ 
#  ███░            ███████████  ░░█████████ 
# ░░░             ░░░░░░░░░░░    ░░░░░░░░░  
                                          
screen s_chess_dismiss():
    if chess.bg:
        $ bg = 'bg ' + chess.bg
        add bg xysize(1.0, 1.0):
            if chess.bg == 'gradient':
                matrixcolor ColorizeMatrix(prefs.style.gradient_color[1],prefs.style.gradient_color[0])

    # objective    
    if hasattr(store, 'game') and game.custom_objective and 'battle' in g.state:
        frame:
            style 'empty'
            align (1.0,0)
            xsize 400
            padding 10,10
            vbox:
                xalign 1.0
                spacing -120
                text 'GOAL :\n' size 50 font "Trattatello.ttf" color "#fff" outlines [(4, "#696969",0,0)] xalign .5
                text _(game.custom_objective) size 50 color "#fff" outlines [(4, "#696969",0,0)] font 'FONT_normal'
   
    button: # DISMISS
        xysize (1.0, 1.0)
        if 'cutscene' in g.state or chess.ui["selected"] or chess.ui["arrows"] or chess.ui['animation_move']: # avoid doing returns for nothing
            if config.developer:
                text "F_DISMISS" color "#0f0" ypos 50
            action Function(f_dismiss), Return()
        else:
            action NullAction()

screen s_chessboard_bg(chess, xinit=None,yinit=None):

    layer 'master'

    # if 'battle' in g.state:
    #     default text_scroll_str = "BATTLEBATTLEBATTLE"
    #     default scrolling_way = 1
    # elif 'preparation' in g.state:
    #     default text_scroll_str = "SETUPSETUPSETUPSETUPSETUPSETUP"
    #     default scrolling_way = -1
    # else:
    #     default text_scroll_str = None
    # if text_scroll_str:
    #     text text_scroll_str xpos 1200 size 600 font "Lithops-Regular.otf" layout "nobreak" vertical True kerning -20 yoffset -1000:
    #         at t_blend_bottom
    #     text text_scroll_str xpos 1200 size 600 font "Lithops-Regular.otf" layout "nobreak" vertical True kerning -20 yoffset 600 :
    #         at t_text_scroll(scrolling_way), t_blend_top
    
    ###############################
    #
    #       PILOT INSPECT
    #
    if 'cutscene' not in g.state and not renpy.get_screen('s_character_info'):
        # hide it when we open the info menu
        $ v_inspect = chess.ui['inspected'] or chess.ui['selected']
        $ pilots = []
        if v_inspect:
            if isinstance(v_inspect, Pilot):
                $ pilots = [v_inspect]
            elif isinstance(v_inspect, Robot_Piece) and v_inspect._pilot:
                $ pilots = v_inspect._pilot

        for index, pilot in enumerate(reversed(pilots)):
            if pilot:
                button:
                    at transform:
                        alpha 0.91
                    # add "#0f0"
                    xysize (1920 - 1250, 1.0)
                    style 'empty'
                    if chess.state == 'selecting':
                        action Call('l_character_info', pilot)
                        at t_interactive
                    if len(pilots) == 2:
                        xpos 1250 + index * 50
                        ypos index * -30
                    else:
                        xpos 1250
                    focus_mask True
                    fixed: #profil
                        if get_board_color():
                            $ light_color = get_board_color().replace_lightness(0.7) 
                        else:
                            $ light_color = (persistent.style_colors[1])
                        ypos 200
                        add pilot.id:
                            at transform:
                                ypos -pilot.img_side_xy[1]
                                matrixcolor ColorizeMatrix("#0e2a42", light_color) * SaturationMatrix(0.5) * BrightnessMatrix(0.4) * ContrastMatrix(0.6)
                            if pilot.health == 1:
                                at t_low_health
                        add AlphaMask(Transform('bg gradient2 ', xysize=(1.0, 1.1), ypos=-200), pilot.id):
                            blend 'multiply' additive 0.4 alpha 0.7 ypos -pilot.img_side_xy[1]

#     ███████    █████   █████ ██████████ ███████████   █████         █████████   █████ █████
#   ███░░░░░███ ░░███   ░░███ ░░███░░░░░█░░███░░░░░███ ░░███         ███░░░░░███ ░░███ ░░███ 
#  ███     ░░███ ░███    ░███  ░███  █ ░  ░███    ░███  ░███        ░███    ░███  ░░███ ███  
# ░███      ░███ ░███    ░███  ░██████    ░██████████   ░███        ░███████████   ░░█████   
# ░███      ░███ ░░███   ███   ░███░░█    ░███░░░░░███  ░███        ░███░░░░░███    ░░███    
# ░░███     ███   ░░░█████░    ░███ ░   █ ░███    ░███  ░███      █ ░███    ░███     ░███    
#  ░░░███████░      ░░███      ██████████ █████   █████ ███████████ █████   █████    █████   
#    ░░░░░░░         ░░░      ░░░░░░░░░░ ░░░░░   ░░░░░ ░░░░░░░░░░░ ░░░░░   ░░░░░    ░░░░░    
                                                                                           
screen s_chessboard_overlay():
    default old_score = chess.get_advantage()

    use s_infobox()

    #############################
    #
    #   EVAL BAR + ITEMS + give up UI, there's the UNDO item that should be available on lose
    #
    fixed at t_dissolve:
        if not 'preparation' in g.state:
            button at t_interactive :
                id 'btn_giveup'
                add "give_up" xysize 200,200
                align 0.11,0.5
                if game.is_over:
                    action NullAction()
                else:
                    action SetVariable('game.lose_con', 'True'), Return()
        if show_debug_menu:
            button at t_interactive :
                xysize 200,100
                add "#f00"
                text "WIN"
                align 0.11,0.3
                action SetVariable('game.win_con', 'True'), Return()

        fixed:
            if prefs.battlefield_layout_left:
                xsize 250 xalign 1.0

        showif chess.wait_for_enemy:
            text "Thinking..." xalign .5:
                at t_dissolve

            # text _("{b}5:29") size 90 font "fonts/Venus+Carrare.otf" color "#000" outlines [(4, "#696969",0,4)]
            # text _("{b}4:22") size 90 font "fonts/Venus+Carrare.otf" color "#fff" outlines [(4, "#696969",0,4)] yalign 1.0
        
        fixed:
            #############################
            #
            #   EVAL BAR + ITEMS
            #
            xysize (170, 1.0)
            if prefs.battlefield_layout_left:
                align (0.0, 0.5)
            else:
                align (1.0, 0.5)

            hbox:
                box_reverse True
                # if not prefs.battlefield_layout_left:

                fixed: # actual bar
                    xysize (50, 1.0)
                    vbox:
                        showif old_score != chess.get_advantage() and not renpy.in_rollback():
                            add Solid("#000") at t_eval_anim(old_score)
                        else:
                            add Solid("#000") xysize (1.0, 0.5 - old_score/2500 )
                        fixed:
                            add Solid("#eee")
                    text "mat.\nadv\ntage" align (0.5,1.0) size 25 font "FONT_normal"
                    vbox:
                        spacing 49
                        xsize 50 yalign 0.475
                        text ". . . ." size 40 font "FONT_normal" xalign 0.5 color "#444"
                        text " " size 40 font "FONT_normal" xalign 0.5 color "#999"
                        text ". . . ." size 40 font "FONT_normal" xalign 0.5 color "#555"
                        text ". . . ." size 40 font "FONT_normal" xalign 0.5 color "#666"
                        text ". . . ." size 40 font "FONT_normal" xalign 0.5 color "#777"
                        text ". . . ." size 40 font "FONT_normal" xalign 0.5 color "#999"
                        text ". . . ." size 40 font "FONT_normal" xalign 0.5 color "#aaa"
                        text ". . . ." size 40 font "FONT_normal" xalign 0.5 color "#bbb"
                        text " " size 40 font "FONT_normal" xalign 0.5 color "#999"
                        text ". . . ." size 40 font "FONT_normal" xalign 0.5 color "#ccc"
                    add Solid("#ffa5a5") align (0.5,0.5) xysize(1.0,10)

                fixed: 
                # grey side
                    xysize (120, 1.0)
                    if chess.bg == 'gradient':
                        add Solid('#fff4') matrixcolor ColorizeMatrix(prefs.style.gradient_color[1], prefs.style.gradient_color[0])
                    else:
                        add Solid('#6668')

                #############################
                #   
                #       ITEMS
                #
                    vbox:
                        xalign 0.5
                        button at t_interactive:
                            xysize(90,90)
                            action Call('l_use_item', 'undo')
                            sensitive False
                            if g.items['undo']>0 and 'battle' in g.state and game.undoable_move < len(chess.history):
                                sensitive True
                            add 'undo icon' xysize(1.0,1.0)
                            text str(g.items['undo']) style 'style_purple_text' color COLOR_HIGHLIGHT() pos 1.0,1.0 anchor 0.5,0.5
                        
                        # text "." align (.5,.5)
                        for tarot, quantity in g.items.items():
                            if quantity > 0 and tarot != 'undo':
                                button at t_interactive:
                                    xysize(120,80)
                                    # add "#00f"
                                    # focus_mask True
                                    action Call('l_use_item', tarot)
                                    hovered Function(show_s_tarot, tarot)
                                    unhovered Function(hide_s_tarot)
                                    for i in range(quantity):
                                        add 'tarot [tarot]' yalign .5 xalign .6 ysize 90 fit 'scale-down' rotate -70 transform_anchor True offset (-i*5, -i*5)

                    $ txt = str(int(chess.get_advantage()/100) * c.COLOR_TO_SIGN[chess.player]) 
                    if chess.get_advantage()>0:
                        $ txt = "+" + txt
                    text "{i}{size=-10}[txt[0]]{/size}[txt[1:]]" xalign 0.5 yalign 0.5 font "FONT_big" size 50 color "#a2eba6" outlines [ (4, "#00a03d", 0, 2) ]


                    # button at t_interactive:
                    #     xysize(90,90)
                    #     align .5,1.0
                    #     action NullAction()
                    #     add 'options icon' xysize(1.0,1.0)
                    
            $ old_score = chess.get_advantage()

