label l_map_select:
    $ g.items['undo'] += 3
    scene onlayer screens
    scene
    show screen s_map_select 
    with dissolve_fast

    label .loop:
    call screen s_pauseScreen(hard_stop=True)
    jump .loop

label l_set_level:
    $ g.progress = int(renpy.input(prompt='g.progress (in base 100), current: [g.progress]'))
    $ renpy.set_screen_variable('current_chapter', str(g.progress//100), screen='s_map_select', layer='master')
    $ renpy.set_screen_variable('current_mission',  str(g.progress%10), screen='s_map_select', layer='master')
    return

screen s_map_select():
    layer 'master'
    # check team / robots
    add 'map'
    
    default flag_position = [(1040, 730), (1040, 730), (1040, 730)]

    default current_chapter = str(g.progress//100)
    default current_mission = str(g.progress%100)

    button at t_interactive:
        text 'MISSION [current_chapter]-[current_mission]' style 'style_3d_big_txt' pos 20,20
        if config.developer:
            action Call('l_set_level')
        

    button at t_interactive:
        # pos flag_position[g.progress]
        pos (1040, 730)
        xysize 200,200
        anchor 0.5,0.5
        add 'flag':
            align (0.5,0.5)
        # add "#666"
        action Function(update_local_checkpoint_and_autosave), Play('audio', 'sound/UI/enter_142.wav'), Jump('l_map_'+current_chapter+'_'+current_mission)

    add 'i_clouds_loop'


image i_clouds_loop:
    Transform("overworld/cloud.webp", zoom=2)
    blend "add"
    xpan 0.0 ypan 0.0
    linear 60.0 xpan -1080.0 ypan 360.0
    repeat

image flag:
    "flag_1"
    pause 0.15
    "flag_2"
    pause 0.15
    "flag_3"
    pause 0.15
    "flag_4"
    pause 0.15
    repeat