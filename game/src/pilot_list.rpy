# PILOTS LIST
# The PILOTS button of the world map (s_map_select in maps/s_map_select.rpy) opens this list:
# PILOTS tab: one row per pilot in TEAM with a summary (stamina, EXP, loyalty). Click a row to open their
# profile (s_character_info in src/PILOT_screen.rpy); closing the profile brings the list back.
# RELATIONSHIPS tab: the affinity table of the whole TEAM (s_relationships_table in src/affinity.rpy).
# The pairs who can talk show TALK in the table: click it to play the talk (src/talks.rpy).
# CHESSMEN tab (story mode): one row per robot the player owns (ROBOTS, src/story_battles.rpy) with its upgrades
# (src/robot_upgrades.rpy). More are bought from the United Nations (src/un_shop.rpy).

label l_pilot_list(start_tab='pilots'):
    play sound 'sound/misc/plop.wav'
    label .loop:
        # blur the map behind the list (closing a profile removes it, see l_close_pop_up)
        $ renpy.layer_at_list([t_blur], layer="master")
        # returns the pilot clicked, ('talk', pilot, pilot) for a talk, or False to close the list
        call screen s_pilot_list(start_tab) with Dissolve(0.2)
        if isinstance(_return, Pilot):
            call l_character_info(_return) # the list is hidden while the profile is open
            $ start_tab = 'pilots'
            jump .loop
        elif isinstance(_return, tuple) and _return[0] == 'talk':
            call l_talk(_return[1], _return[2]) # see src/talks.rpy
            $ start_tab = 'relationships'
            jump .loop
    $ remove_blur_master()
    with Dissolve(0.2)
    return

init python:
    def pilot_can_learn(pilot):
        """True if the pilot has enough EXP for one of their skills to learn."""
        return any(SKILLLIST[skill].cost <= pilot.xp for skill in pilot.skills['can_learn'])

screen s_pilot_list(start_tab='pilots'):
    zorder 1
    modal True
    default tab = start_tab
    add "#0009"
    button: # click outside the list to close it
        action Return(False) # not None: Return(None) returns True

    frame:
        style 'empty'
        background Solid("#000a")
        xsize 1300
        ysize 0.92
        align (0.5, 0.5)
        vbox:
            xfill True
            spacing 15
            $ tabs = [('pilots', _("PILOTS"))] + ([] if rogue else [('relationships', _("RELATIONSHIPS")), ('chessmen', _("CHESSMEN"))]) # no affinity in roguelite
            use s_tab_bar(tabs) # see src/PILOT_screen.rpy
            if tab == 'relationships' and not rogue:
                use s_relationships_table() # every pilot's affinities, see src/affinity.rpy
            elif tab == 'chessmen' and not rogue:
                viewport:
                    mousewheel True
                    draggable True
                    vbox:
                        spacing 10
                        xalign 0.5
                        for robot in ROBOTS:
                            use s_chessmen_row(robot)
                        if not ROBOTS:
                            text _("No CHESSMEN yet.") style 'style_big_white_text' xalign 0.5
            else:
                viewport:
                    mousewheel True
                    draggable True
                    vbox:
                        spacing 10
                        xalign 0.5
                        for pilot in TEAM:
                            use s_pilot_list_row(pilot)

    button at t_interactive:
        align (1.0, 0.0)
        xysize 100,100
        action Return(False)
        text 'X' style 'style_3d_big_txt' size 60 align 0.5,0.5

screen s_pilot_list_row(pilot):
    $ show_loyalty = not rogue and pilot.id != 'lelouch' # lelouch has no loyalty (src/loyalty.rpy)
    button at t_interactive:
        xsize 1240
        ysize 120
        background Solid("#fff1")
        hover_background Solid("#fff3")
        action Return(pilot) # l_pilot_list opens their profile
        hbox:
            yalign 0.5
            spacing 25
            add pilot.img_side_eyes() xysize (280, 100) yalign 0.5
            fixed: # same width on every row, so the columns line up
                xysize (280, 100)
                yalign 0.5
                text pilot.name.upper() style 'style_big_white_text' yalign 0.5
            fixed: # STAMINA, hearts like the STATS tab
                xysize (250, 100)
                yalign 0.5
                hbox:
                    yalign 0.5
                    for heart in pilot._heart_display():
                        if heart == '*':
                            add "heart grey" zoom 0.7
                        else:
                            $ heart_size, heart_level = heart # 'small' or 'big', see src/loyalty.rpy
                            add "heart [heart_size]" zoom 0.7 matrixcolor ColorizeMatrix(LOYALTY_COLORS[heart_level][1], LOYALTY_COLORS[heart_level][0])
            vbox:
                xsize 260
                yalign 0.5
                text _("EXP: [pilot.xp]") style 'style_big_white_text' textalign 0.0
                if pilot_can_learn(pilot):
                    text _("can learn a skill") style 'style_big_white_text' size 26 color "#ffa" textalign 0.0
            if show_loyalty:
                $ loyalty_level = loyalty_of(pilot)
                text LOYALTY_EMOJI[loyalty_level] size 60 yalign 0.5

# a robot the player owns: its model, class and upgrades
screen s_chessmen_row(robot):
    $ fen = DEFAULT_ROBOT[robot.type]
    frame:
        style 'empty'
        xsize 1240
        ysize 120
        background Solid("#fff1")
        hbox:
            yalign 0.5
            spacing 25
            add f"white {c.FEN_TO_PIECE[fen]} merida" xysize (100, 100) yalign 0.5
            fixed: # same width on every row, so the columns line up
                xysize (280, 100)
                yalign 0.5
                text c.FEN_TO_PIECE[fen].upper() style 'style_big_white_text' yalign 0.5
            add f"battle_ui/icon type {robot.type} outline.webp".replace("*", "star").replace("#", "hash") xysize (60, 60) yalign 0.5
            vbox:
                yalign 0.5
                if robot_upgrades(robot):
                    for upgrade in robot_upgrades(robot):
                        $ upgrade_name, upgrade_desc = ROBOT_UPGRADES[upgrade]
                        text "{}: {}".format(__(upgrade_name), __(upgrade_desc)) style 'style_big_white_text' size 30 textalign 0.0
                else:
                    text _("No upgrade.") style 'style_big_white_text' size 30 color "#fff8"
