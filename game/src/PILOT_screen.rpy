#       :::       ::::::::   ::::::::  :::::::::  :::::::::: :::::::::: ::::    ::: 
#      :+:       :+:    :+: :+:    :+: :+:    :+: :+:        :+:        :+:+:   :+: 
#     +:+        +:+        +:+        +:+    +:+ +:+        +:+        :+:+:+  +:+ 
#    +#+         +#++:++#++ +#+        +#++:++#:  +#++:++#   +#++:++#   +#+ +:+ +#+ 
#   +#+                 +#+ +#+        +#+    +#+ +#+        +#+        +#+  +#+#+# 
#  #+#           #+#    #+# #+#    #+# #+#    #+# #+#        #+#        #+#   #+#+# 
# ###             ########   ########  ###    ### ########## ########## ###    #### 

label l_character_info(pilot):
    # this is so while the screen is displayed, we cant progress in the label until its hidden away
    play sound 'sound/misc/plop.wav'
    show screen s_character_info(pilot) with Dissolve(0.2)
    label .gameLoop:
        call screen s_pauseScreen(hard_stop=False)
        if renpy.get_screen('s_character_info'):
            jump .gameLoop
    return

screen s_character_info(pilot):
    zorder 2
    use s_popup_blurry_screen()

    add pilot.id ysize 2000 fit 'contain' pos (-70,-int(pilot.img_side_xy[1]/1.5))

    frame:
        style 'empty'
        xsize 800
        yanchor 1.0
        xpos 0
        ypos 1020
        text pilot.get_desc() style 'style_text_handwritten' outlines [ (4, "#333", 0, 1) ] color "#fff" xalign 0.5 layout "subtitle" line_spacing -30

    frame:

        style 'empty'
        add "#fff2"
        # background Frame('gui/bubble_frame.webp', 55, 55, 40, 40)

        xsize 0.55
        ysize 0.95
        xpos 0.4
        ypos 20
        vbox:
            xpos 30
            text _("- stats -") style 'style_purple_text' color COLOR_HIGHLIGHT() xalign 0.5 kerning 25 font "Venus+Plomb.otf"
            grid 2 3:
                yspacing -20
                xspacing 80
                text _("HEALTH:") style 'style_3d_big_txt' align 1.0,0.5
                hbox: #HEARTS
                    xsize 200
                    for heart in pilot._heart_display():
                        if heart == '*':
                            add "heart grey"
                        else:
                            if heart<0: #small heart
                                add "heart small" matrixcolor ColorizeMatrix(LOYALTY_COLORS[-heart][1],LOYALTY_COLORS[-heart][0])
                            else:
                                add "heart big" matrixcolor ColorizeMatrix(LOYALTY_COLORS[heart][1],LOYALTY_COLORS[heart][0])
                
                text _("EXPERIENCE:") style "style_3d_big_txt" align 1.0,0.5
                text _("[pilot.xp]{size=-20}/[pilot.xp_all]") font "fonts/cmu_b.ttf" size 60 color "#ffffff" outlines [ (4, "#000000", 0, 2) ] yalign 1.0

                text _("VALUE?") style "style_3d_big_txt" align 1.0,0.5
                text _("[pilot.price_euristic()]") font "fonts/cmu_b.ttf" size 60 color "#ffffff" outlines [ (4, "#000000", 0, 2) ]  yalign 1.0

                # text _("LOYALTY:") style "style_3d_big_txt" align 1.0,1.0
                # hbox:
                #     spacing 20 align 0.5,1.0
                #     text LOYALTY_TO_NAME[TRUST_TO_LOYALTY(pilot.trust)] font "fonts/cmu_b.ttf" size 60 color LOYALTY_COLORS[TRUST_TO_LOYALTY(pilot.trust)][0] outlines [ (4, LOYALTY_COLORS[TRUST_TO_LOYALTY(pilot.trust)][1], 0, 2) ] yalign 1.0
                #     text "{{[pilot.trust]}" font "fonts/cmu_b.ttf" size 60 color LOYALTY_COLORS[TRUST_TO_LOYALTY(pilot.trust)][0] outlines [ (4, LOYALTY_COLORS[TRUST_TO_LOYALTY(pilot.trust)][1], 0, 2) ] yalign 1.0
            
            # fixed:
            #     ysize 30
            # text _("- c a n   P i l o t -") style 'style_big_white_text' color "#cb6bff" xalign 0.5
            # fixed:
            #     ysize 20
            hbox:
                xalign 0.5
                spacing 10
                for robot in ['^', 'L','x','+','#', '*']:
                    fixed:
                        xysize(100,100)
                        add Solid("#696969")
                        if robot in pilot.can_drive:
                            button at t_interactive:
                                xysize(100,100)
                                action Hide(None, Dissolve(.2)), Function(renpy.call_in_new_context,'l_tutorial_piece', pilot.can_drive[robot])
                                if pilot.can_drive[robot] == 'p' and 'promote_q' in pilot.skills['once']:
                                    add 'skill promote_q' xysize(100,100) align 0.5,0.5 nearest True
                                else:
                                    add 'skill drive_[pilot.can_drive[robot]]' xysize(100,100) align 0.5,0.5 nearest True
                        else:
                            add "skin/pieces/robot/robot type [DEFAULT_ROBOT[robot]].svg" xysize(100,100) alpha 0.5
                for skill in ['stamina','rest']:
                    if skill in pilot.skills['once']:
                        add 'skill [skill]' xysize 100,100 nearest True

            fixed:
                ysize 20
            text _("- skills -") style 'style_purple_text' color COLOR_HIGHLIGHT() xalign 0.5 kerning 25 font "Venus+Plomb.otf"

            vpgrid:
                cols 2
                for category in ['once', 'setup']:
                    for skill in pilot.skills[category]:
                        # Don't display those skills if learned
                        if category=='once' and skill in {'stamina','rest','promote_q','drive_p', 'drive_k', 'drive_r', 'drive_n', 'drive_b', 'drive_q'}:
                            continue

                        fixed:
                            xysize (500,120)
                            button:
                                if category == 'can_learn':
                                    at t_interactive
                                    action Call('l_try_to_learn', pilot, skill)
                                else:
                                    action NullAction()

                                hbox:
                                    xsize 500
                                    spacing 5
                                    fixed:
                                        xysize 112,112
                                        if renpy.can_show('skill '+ skill):
                                            add 'skill [skill]' xysize 112,112 nearest True:
                                                if category == 'can_learn':
                                                    alpha 0.8 nearest False
                                        else:
                                            add 'skill none' xysize 112,112 nearest True
                                        if category == 'can_learn':
                                            text "[SKILLLIST[skill].cost]" style 'style_purple_text' color COLOR_HIGHLIGHT() align 0.5,0.5 text_align 0.5
                                    fixed:
                                        xysize 380,112
                                        text SKILLLIST[skill].desc font "FONT_bold" size 35 color "#fff" align 0.3,0.5 layout "subtitle":
                                            if category == 'can_learn':
                                                color "#fff9"
                                            if len(SKILLLIST[skill].desc)>80:
                                                size 30

            fixed:
                ysize 10
            text _("- learn -") style 'style_purple_text' color COLOR_HIGHLIGHT() xalign 0.5 kerning 25 font "Venus+Plomb.otf"
            vpgrid:
                cols 2
                for category in ['can_learn']:
                    for skill in pilot.skills[category]:
                        fixed:
                            xysize (500,120)
                            button at t_interactive:
                                action Call('l_try_to_learn', pilot, skill)

                                hbox:
                                    xsize 500
                                    spacing 5
                                    fixed:
                                        xysize 112,112
                                        if renpy.can_show('skill '+ skill):
                                            add 'skill [skill]' xysize 112,112 alpha 0.8 nearest True
                                        else:
                                            add 'skill none' xysize 112,112 nearest True
                                        text "[SKILLLIST[skill].cost]" style 'style_purple_text' color COLOR_HIGHLIGHT() align 0.5,0.5 text_align 0.5
                                    fixed:
                                        xysize 380,112
                                        text SKILLLIST[skill].desc font "FONT_bold" size 35 color "#fff9" align 0.3,0.5 layout "subtitle":
                                            if len(SKILLLIST[skill].desc)>80:
                                                size 30

    vbox:
        xalign 1.0
        button at t_interactive:
            xysize 100,100
            action Hide(None, Dissolve(.2)),Jump('l_close_pop_up')
            text 'X' style 'style_3d_big_txt' size 60 align 0.5,0.5

    text pilot.name style 'style_3d_big_txt' font "fonts/Basteleur-Bold.ttf" size 100 align(0.98,1.0) outlines [ (6, "#000000", 0, 7) ]

    button at t_interactive:
        align (0.0, 1.0)
        action Call('l_tutorial', 'pilot')
        add 'info_button'

    if show_debug_menu:
        add pilot.img_side() align (0,1.0)

        add pilot.img_side_eyes() align (1.0,1.0) xysize (450, 150)

#       :::           ::::::::::: ::::    ::: ::::::::::: ::::::::::: 
#      :+:                :+:     :+:+:   :+:     :+:         :+:     
#     +:+                 +:+     :+:+:+  +:+     +:+         +:+     
#    +#+                  +#+     +#+ +:+ +#+     +#+         +#+     
#   +#+                   +#+     +#+  +#+#+#     +#+         +#+     
#  #+#                    #+#     #+#   #+#+#     #+#         #+#     
# ###                 ########### ###    #### ###########     ###     


###############################################################
#
# Initialize all renpy CHARACTERS
# lelouch (is the Pilot, in store) and character.lelouch
#
###############################################################

init -1 python:
    def init_pilots():
        # reload changes from the csv, then set pilots for everyone
        global PILOTLIST
        PILOTLIST = set()
        character.load_character_csv()
        reset_pilot()

init -1 python in character:
    def load_character_csv():
        """
        create Character for every pilot in .csv, also fill character.PILOTLIST with data
        """
        global PILOTLIST
        file = renpy.open_file("PILOTS.csv", encoding="utf8")
        data = file.read()
        data = data.split("\n")
        # pr int(data)
        
        # Get the headers from the first row (assuming the first line is the header)
        headers = data[0].split(";")
        PILOTLIST = {}
        
        for row in data[1:]:  # Skip the header row
            if row.strip() == "":  # Skip empty lines
                continue
            values = row.split(";")
            key = values[0]  # The first value is the key (e.g., 'lelouch')
            if key == "internal":
                continue
            
            # Create a dictionary for each pilot with headers as keys
            PILOTLIST[key] = {header: value for header, value in zip(headers[1:], values[1:])}
        
        # Create characters using the dictionary values
        for key, value in PILOTLIST.items():
            if key == "internal":
                continue
            if key == "":  # Skip empty lines
                continue

            globals()[key] = renpy.store.Character(value['name'], image=key, show_pilot=key, condition=f'{key} not in DEAD_OR_DESERT')
            # show_pilot??? i think show_ variables are passed to say() screen
            globals()[key].id = key

###############################################################
#
# Initialize Pilots skills, desc etc
#
###############################################################

init -1 python:
    def reset_pilot(single_pilot=None): # single_pilot is str or None
        #
        #   if single_pilot = None, we set pilots for everyone.
        #   else: we only do it on one pilot
        #
        for key, value in character.PILOTLIST.items():
            if single_pilot: # if we give an arg, we only do it on one pilot
                if key != single_pilot:
                    continue
                    
            if key != "internal":
                img_side = eval(value['img_side_xy']) if value['img_side_xy'] else (250,220)
                
                new_pilot = Pilot(key, max_health=int(value['max_health']), img_side_xy=img_side)
                # renpy.image(new_pilot.id + ' side', new_pilot.img_side())
                
                new_pilot.default_sort = len(PILOTLIST)
                
                # PILOTLIST[key] = new_pilot
                
                # If learned skills exist and are not empty
                if 'skills' in value and value['skills']:
                    for skill in value['skills'].strip().split(' '):
                        if skill == '':
                            continue
                        skill_type = SKILLLIST[skill].type
                        new_pilot.skills[skill_type].append(skill)
                        
                        if skill_type == 'once':  # Activate already learned skills
                            skill = new_pilot.skills['once'][-1]
                            skill = SKILLLIST[skill]
                            skill.effect(new_pilot, *skill.args)

                if 'can_learn' in value and value['can_learn']:
                    for skill in value['can_learn'].strip().split(' '):
                        skill_type = SKILLLIST[skill].type
                        new_pilot.skills['can_learn'].append(skill)
        
                # THOSE ARE SKILLS EVERYONE CAN LEARN:
                new_pilot.skills['can_learn'].append('stamina')
                new_pilot.skills['can_learn'].append('rest')
                # if 'drive_p' in new_pilot.skills['once']:
                #     new_pilot.skills['can_learn'].append('2-step')
                #     new_pilot.skills['can_learn'].append('promote_q')

                new_pilot.price = new_pilot.price_euristic()
                globals()[key] = new_pilot

        # del character.PILOTLIST