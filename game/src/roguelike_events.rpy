label l_shop_rogue:
    show screen s_shop_rogue
    play audio 'sound/rogue/shop.wav'
    # this is so while the screen is displayed, we cant progress in the label until its hidden away
    label .loop:
    if renpy.get_screen('s_shop_rogue'):
        call screen s_pauseScreen(False)
        jump .loop
    return

screen s_shop_rogue():
    zorder 2
    modal True
    default value = {'n':3, 'b':3, 'r':5, 'q':9}

    dismiss:
        action Hide(None)

    fixed:
        at transform:
            on show:
                ypos -1.0
                easein 0.5 ypos 0
            on hide:
                ypos 0
                easeout 0.5 ypos -1.0

        add 'shop_bg' nearest True xysize(1.0, 1.0)
        text _("SHOP")  color "#ff0" font 'Lithops-Regular.otf'  xalign 0.5 ypos 70 size 200
        vbox:
            spacing 30
            xalign 0.5
            ypos 300
            hbox:
                spacing 50
                button at t_interactive:
                    action Call('l_buy_robot', 'undo', 1)
                    sensitive g.money>0
                    vbox:
                        # frame:
                        fixed:
                            xysize (200,200)  
                            add f"undo icon": 
                                blur 10 matrixcolor BrightnessMatrix(-1) alpha 0.5 xysize (170,170) align 0.8,0.8
                            add f"undo icon" xysize (150,150) align 0.5,0.5
                            text "{k=-10}2x" style 'style_3d_big_txt' align -0.3,0.8 size 70

                        # text _("COST {size=+20}1") style 'style_3d_txt' xalign 0.5
                        text _("COST {size=+20}1") style 'style_3d_txt' xalign 0.5

                for piece in ['n', 'b', 'r', 'q']:
                    button at t_interactive:
                        sensitive g.money>=value[piece]
                        action Call('l_buy_robot', piece, value[piece])
                        vbox:
                            # frame:
                            fixed:
                                xysize (200,200)  
                                add f"white {c.FEN_TO_PIECE[piece]} merida":
                                    blur 10 matrixcolor BrightnessMatrix(-1) zoom 1.1 alpha 0.5 align 0.5,0.5
                                add f"white {c.FEN_TO_PIECE[piece]} merida"

                            text _("COST {size=+20}[value[piece]]") style 'style_3d_txt' xalign 0.5
            null
            null
            text _("IN STOCK:") style 'style_3d_txt' xalign 0.5
            vpgrid:
                xalign 0.5
                cols 10
                for piece in ROBOTS:
                    add f"white {c.FEN_TO_PIECE[piece.fen]} merida" matrixcolor BrightnessMatrix(0.2) xysize (80,80)  

        button at t_interactive:
            action Hide(None)
            xysize(520,160)
            align 1.0,1.0
    
label l_buy_robot(piece, price):
    play audio 'sound/rogue/ghost.wav'
    if piece == 'undo':
        $ g.items['undo'] += 2
    else:
        $ ROBOTS.append(Robot_Piece(piece,color=chess.player))
    $ g.money -= price
    return

#       ::: :::::::::  :::::::::: ::::::::::: :::       ::: :::::::::: :::::::::: ::::    ::: 
#      :+:  :+:    :+: :+:            :+:     :+:       :+: :+:        :+:        :+:+:   :+: 
#     +:+   +:+    +:+ +:+            +:+     +:+       +:+ +:+        +:+        :+:+:+  +:+ 
#    +#+    +#++:++#+  +#++:++#       +#+     +#+  +:+  +#+ +#++:++#   +#++:++#   +#+ +:+ +#+ 
#   +#+     +#+    +#+ +#+            +#+     +#+ +#+#+ +#+ +#+        +#+        +#+  +#+#+# 
#  #+#      #+#    #+# #+#            #+#      #+#+# #+#+#  #+#        #+#        #+#   #+#+# 
# ###       #########  ##########     ###       ###   ###   ########## ########## ###    #### 
screen s_in_between_rounds():
    default state = 0
    default original_xp = {pilot:pilot.xp for pilot in TEAM}
    default original_health = {pilot:pilot.health for pilot in TEAM}

    fixed:
        if state >= 4:
            at transform:
                ease 0.5 xpos -600
        else:
            at transform:
                ease 0.5 xpos 0
        use s_in_between_rounds_mini(True, state, original_xp)

    fixed:
        if state >= 4:
            at transform:
                ease 0.5 xpos 600
        else:
            at transform:
                ease 0.5 xpos 0
        use s_in_between_rounds_mini(False, state, original_health)

    use s_shop_coin()

screen s_in_between_rounds_mini(battle=True, state=None, original=None):
    layer 'master'
    default team_length = len(TEAM) # so we dont display any new recruit in this screen
    frame:
        style 'empty'
        if battle:
            background "#311" #g.colors['magenta']
        else:
            background "#113"
        xysize(0.5,1.0)
        if not battle:
            xpos 0.5
        if battle:
            text _("BATTLE") color g.colors['magenta'] font 'Lithops-Regular.otf'  xalign 0.5 ypos 50 size 200
        else:
            text _("RESERVE") color g.colors['bluesky'] font 'Lithops-Regular.otf' xalign 0.5 ypos 50 size 200

        if state < 4:
            button:
                # add "#fff"
                action IncrementScreenVariable('state', 1), Return()
        fixed:
            ysize 0.9
            yalign 1.0

            vpgrid:
                align (0.5, 0.5)
                cols 3
                for i, pilot in enumerate(TEAM):
                    if i >= team_length:
                        break
                    if pilot.deployed!=battle:
                        continue
                    button at t_interactive:
                        sensitive pilot.health
                        if state>=2:
                            action Call('l_character_info', pilot)
                        else:
                            action IncrementScreenVariable('state', 1), Return()
                        xysize 300,240
                        vbox:
                    
                            text pilot.name.upper() style 'style_big_white_text'
                            fixed: # face
                                xysize 280,100
                                add pilot.img_side_eyes():
                                    xysize 280,100
                                    if pilot.health == 1:
                                        at t_low_health
                                hbox:
                                    align 1.0,1.0
                                    for i in pilot._heart_display():
                                        fixed:
                                            xysize 40,30
                                            if i == '*':
                                                text '❤️' size 30
                                                at transform:
                                                    matrixcolor ColorizeMatrix("#aaa","#aaa")
                                            else:
                                                text '❤️' size 30
                                                at transform:
                                                    matrixcolor ColorizeMatrix('#ffa','#ffa')
                                        # fixed:
                                        #     xysize 35,50
                                        #     # if i == '*':
                                        #     #     at transform:
                                        #     #         matrixcolor ColorizeMatrix("#000","#666")
                                        #     #     add "heart small" yalign 0.5
                                        #     # else:
                                        #     #     at transform:
                                        #     #         matrixcolor ColorizeMatrix("#a00","#f00")
                                        #     #     add "heart small" yalign 0.5
                                

                            fixed:
                                # add "#ff02"
                                xalign 0.5
                                xysize(300,140)
                                ypos 5
                                if battle:
                                    vbox:
                                        if pilot in original and original[pilot] == pilot.xp:
                                            text _("EXP: [original[pilot]]") xalign 0.0 style 'style_big_white_text'
                                        else:
                                            text _("EXP: [pilot.xp]") xalign 0.0 style 'style_big_white_text' color '#ffa'

                                            if state>=1:
                                                text _("> deployed:  +1") ypos -10 xalign 0.0 font "fonts/Compagnon-Medium.otf" style 'style_big_white_text' size 30 at t_emphazise_text
                                            if state>=3 and chess.history and pilot in chess.history[-1].move.piece._pilot:
                                                text _("> checkmate: +2") ypos -20  xalign 0.0 font "fonts/Compagnon-Medium.otf" style 'style_big_white_text' size 30 at t_emphazise_text
                                else:
                                    vbox:
                                        if pilot in original and original[pilot] == pilot.health:
                                            text _("HEALTH: [original[pilot]]/[pilot.max_health]") xalign 0.0 style 'style_big_white_text'
                                        else:
                                            text _("HEALTH: [pilot.health]/[pilot.max_health]") xalign 0.0 style 'style_big_white_text' color '#ffa'

                                            if state>=1:
                                                if 'rest' in pilot.skills['once']:
                                                    text _("> xtra rest: +2") ypos -10  xalign 0.0 font "fonts/Compagnon-Medium.otf"  style 'style_big_white_text' size 30 at t_emphazise_text
                                                else:
                                                    text _("> rested:    +1") ypos -10  xalign 0.0 font "fonts/Compagnon-Medium.otf"  style 'style_big_white_text' size 30 at t_emphazise_text
        
        if state >= 4:
            button:
                action SetScreenVariable('state', 3)

transform t_emphazise_text:
    xzoom 1.5
    ease .5  xzoom 1


#       ::: :::::::::  :::::::::: ::::::::  :::::::::  :::    ::: ::::::::::: ::::::::::: 
#      :+:  :+:    :+: :+:       :+:    :+: :+:    :+: :+:    :+:     :+:         :+:     
#     +:+   +:+    +:+ +:+       +:+        +:+    +:+ +:+    +:+     +:+         +:+     
#    +#+    +#++:++#:  +#++:++#  +#+        +#++:++#:  +#+    +:+     +#+         +#+     
#   +#+     +#+    +#+ +#+       +#+        +#+    +#+ +#+    +#+     +#+         +#+     
#  #+#      #+#    #+# #+#       #+#    #+# #+#    #+# #+#    #+#     #+#         #+#     
# ###       ###    ### ########## ########  ###    ###  ########  ###########     ###     

screen s_recruit(recruitable_pilots):

    layer 'master'
    zorder -1

    add "#e2f9dc"
    text _("RECRUIT")  color g.colors['green'] font 'Lithops-Regular.otf'  xalign 0.5 ypos 70 size 200

    hbox:
        align 0.5,0.5
        if len(recruitable_pilots) <= 2:
            spacing 100
        else:
            spacing 60
        for pilot in recruitable_pilots:
            button at t_interactive:
                action Show('s_recruit_character_info', Dissolve(.2), pilot)
                sensitive g.money >= pilot.price and not pilot in TEAM
                vbox:
                    xsize 300
                    button:
                        ysize 240
                        vbox:
                            text pilot.name.upper() style 'style_big_white_text' color g.colors['green']
                            add pilot.img_side_eyes() xysize(300,100)

                            fixed:
                                xalign 0.5
                                ypos 5
                                xysize(300,140)
                                vbox:
                                    text _("HEALTH: [pilot.health]/[pilot.max_health]") xalign 0.0 style 'style_big_white_text' color g.colors['green']
                                    text _("EXP: [pilot.xp]") xalign 0.0 style 'style_big_white_text' color g.colors['green']
                    button:
                        if show_debug_menu:
                            add "#000"
                        xysize 300,120
                        # action Call('l_recruit',pilot)
                        hbox:
                            vbox:
                                spacing -10
                                text _("RECRUIT") style 'style_3d_big_txt' size 45
                                text _("> cost:") style 'style_3d_big_txt'
                            text _("[pilot.price]") style 'style_3d_big_txt' yalign 0.5 size 120:
                                at transform:
                                    rotate 15 transform_anchor True anchor (0.3,0.65)
    
    button at t_interactive:
        action Call('l_close_recruit')
        align(0.5,0.9)
        text _("> SKIP")  style 'style_3d_big_txt' size 80



#       ::: :::::::::  :::::::::: ::::::::  :::::::::  :::    ::: ::::::::::: ::::::::::: 
#      :+:  :+:    :+: :+:       :+:    :+: :+:    :+: :+:    :+:     :+:         :+:     
#     +:+   +:+    +:+ +:+       +:+        +:+    +:+ +:+    +:+     +:+         +:+     
#    +#+    +#++:++#:  +#++:++#  +#+        +#++:++#:  +#+    +:+     +#+         +#+     
#   +#+     +#+    +#+ +#+       +#+        +#+    +#+ +#+    +#+     +#+         +#+     
#  #+#      #+#    #+# #+#       #+#    #+# #+#    #+# #+#    #+#     #+#         #+#     
# ###       ###    ### ########## ########  ###    ###  ########  ###########     ###     

# inspect pilot before deciding recruit or not
screen s_recruit_character_info(pilot):
    use s_character_info(pilot)
    dismiss:
        action Confirm(_("Recruit?"), Call('l_recruit', pilot), [Hide('s_recruit_character_info', Dissolve(.2)),Call('l_close_pop_up')])

label l_recruit(pilot):
    hide screen s_recruit_character_info
    $ remove_blur_master()
    if pilot:
        $ g.money -= pilot.price
        "[pilot.name] joins your team!"
        $ TEAM.append(pilot)
    hide screen s_recruit
    hide screen s_in_between_rounds
    with transition_bars
    return

label l_close_recruit():
    hide screen s_recruit
    return
                            

            

