default persistent.best_run = 0

screen main_menu():
    
    use navigation
    add Solid("#edf5f9")

    text _("{i}BEST RUN: [persistent.best_run] rounds") xalign 0.5 ypos 50 style 'style_purple_text' color COLOR_HIGHLIGHT() font 'Venus+Cormier.otf' size 100

    vbox:
        align 0.5,1.0
        hbox:
            button at t_interactive:
                # ysize 400
                text _("{i}STORY\nMODE") color "#10cafb" size 80
                style_prefix 'sty_btn'
                action With(Dissolve(.25)),Jump('l_intro')

            button at t_interactive:
                # ysize 400
                text _("{i}ROGUE\nMODE") color "#10cafb" size 80
                style_prefix 'sty_btn'
                action With(Dissolve(.25)),Jump('l_map_rogue')
                    
            vbox:
                button at t_interactive:
                    # ysize 400
                    text _("{i}SHOP") size 80
                    style_prefix 'sty_btn'
                    action With(Dissolve(.25)),Jump('l_shop_persistent')

                button at t_interactive:
                    # ysize 400
                    text _("{i}PILOTS") size 80
                    style_prefix 'sty_btn'
                    action With(Dissolve(.25)),Show('s_all_pilots')

            vbox:
                button at t_interactive:
                    text _("play normal pos") size 40
                    style_prefix 'sty_btn'
                    action Jump('load_standard_pos')

                # button at t_interactive:
                #     text _("check mcts tree") size 40
                #     style_prefix 'sty_btn'
                #     action Jump('l_mcts_visualizer') # check the other renpy project instead

        hbox:

            button at t_interactive:
                text _("How to Checkmate?") size 35
                style_prefix 'sty_btn'
                action With(Dissolve(.25)),Show('s_how_to_checkmate')

            button at t_interactive:
                text _("Customize") size 35
                style_prefix 'sty_btn'
                action With(Dissolve(.25)),Show('s_rename'),Return()

        button at t_interactive:
            text  _("Delete Save") size 35
            style_prefix 'sty_btn'
            action Confirm(prompt=_("Are you sure?"),yes=[Function(delete_save)])

        hbox:
            button at t_interactive:
                style_prefix 'sty_btn'
                if g.difficulty == 'normal':
                    text _("> Difficulty: Normal")  size 35
                    action Call('l_switch_difficulty')
                else:
                    text _("> Difficulty: Easy")  size 35
                    action Call('l_switch_difficulty')

        fixed:
            xalign 0.8
            xysize (900,200)
            vbox:
                text _("CPU thinking time: [persistent.cpu_strength]") size 45 xalign 0.5
                hbox:
                    bar value FieldValue(persistent, 'cpu_strength', min=100, max=8000, step=100, force_step=True) style 'bar_slider' xsize 300 yalign 0.5
                    vbox:
                        button at t_interactive:
                            style_prefix 'sty_btn'
                            text _("> AUTO") size 35
                            action Call('l_estimate_cpu_str')

    vbox:
        align (1.0, 1.0)
        hbox:
            xalign 1.0
            button at t_interactive style 'sty_btn_button':
                add "gui/main_menu/icon_itch.png" xysize(100,100)
                action OpenURL("https://omshinwa.itch.io/fairylion")
            button at t_interactive style 'sty_btn_button':
                add "gui/main_menu/icon_twitter.jpg"  xysize(100,100)
                action OpenURL("https://x.com/Omshinwa")
            button at t_interactive style 'sty_btn_button':
                add "gui/main_menu/icon_bluesky.svg"  xysize(100,100)
                action OpenURL("https://bsky.app/profile/omshinwa.itch.io")
            button at t_interactive style 'sty_btn_button':
                add "gui/main_menu/icon_discord.jpg"  xysize(100,100)
                action OpenURL("https://discord.com/invite/gU8bxGC87Z")
        
        text 'VER. [config.version]' xalign 1.0

label l_switch_difficulty:
    if g.difficulty == 'easy':
        $ g.difficulty = 'normal'
    else:
        $ g.difficulty = 'easy'
        "In Easy mode, you start with more undos, more pilots, get more money, but the game won't remember your best run."
    return

label l_estimate_cpu_str():
    "Setting the optimal CPU strength based on your computer, click and wait."
    $ estimate_cpu_str()
    return

init python:
    def estimate_cpu_str(time_in_seconds=0.5):
        """
        must be called outside of a game (ie in the main menu)
        set the cpu so it takes _ amount of seconds
        """
        chess = Chess_control((8,8))
        chess.set_fen('1Q4/2pC2/1kP3/6/1q2PP/4K1 b KQkq - 0 1')
        engine.set_fen('1Q4/2pC2/1kP3/6/1q2PP/4K1 b KQkq - 0 1')
        engine.promotions = [['q'],['q']]
        time_eval = timeit.timeit("engine.think(1000)", globals=globals(), number=1)
        persistent.cpu_strength = int( (time_in_seconds / time_eval) * 10 ) * 100

init python:
    def delete_save():
        renpy.unlink_save('current_run')
        renpy.unlink_save('current_checkpoint')
        renpy.unlink_save('current_run_checkpoint')
        persistent._clear()
        # init_pilots()
        renpy.full_restart()

screen s_how_to_checkmate():
    add "black"
    modal True
    vbox:
        align 0.2,0.5

        textbutton _("< BACK") action With(Dissolve(.25)),Hide() text_style 'style_3d_big_txt':
            at t_interactive

        textbutton _("  > Two Queens") action With(dissolve),Jump('l_tutorial_checkmate_2Q') text_style 'style_3d_big_txt':
            at t_interactive
            if not persistent.tutorial_2Q:
                text_color "#8f8fa7"
        textbutton _("  > Two Rooks") action With(dissolve),Jump('l_tutorial_checkmate_2R') text_style 'style_3d_big_txt':
            at t_interactive
            if not persistent.tutorial_2R:
                text_color "#8f8fa7"
        textbutton _("  > One Rook") action With(dissolve),Jump('l_tutorial_checkmate_1R') text_style 'style_3d_big_txt':
            at t_interactive
            if not persistent.tutorial_1R:
                text_color "#8f8fa7"
        textbutton _("  > More") action With(dissolve),Jump('l_tutorial_checkmate_more') text_style 'style_3d_big_txt':
            at t_interactive
            sensitive (bool) (persistent.tutorial_2Q and persistent.tutorial_2R and persistent.tutorial_1R)

label l_shop_persistent:
    $ engine = Engine()
    $ chess = Chess_control()
    $ chess.set_fen('rnbqk/ppppp/5/PPPPP/RNBQK w kq - 0 1')
    $ chess.ui['arrows'] = {(23,38),(32,32)}
    show screen s_shop_persistent with dissolve
    label .loop:
    call screen s_pauseScreen(hard_stop=True)
    jump .loop

# # TYPE # Data
# WHITE PIECE | WHITE SQ | BLACK SQ | BLACK PIECE
define 2 run_rewards = [
        ['color', ["#fff","#e9d7b4", "#b18967", "#000"]],
        ['color', ["#eefbf9","#dfe3e6", "#90a1ac", "#020e2b"]],
        ['color', ["#fff","#f1edbd", "#ca3521", "#002311"]],
        ['color', ["#fff","#e8eced", "#41684e", "#1e0000"]],
        ['other', 'skill sacrifice','sacrifice_skill', _("Generic units can learn the skill SACRIFICE.")],
        ['color', ["#e6ffe3","#ffdded", "#daa4dd", "#c500d7"]],
        # ['other', 'side kallen', 'start_with_kallen', _(f"{kallen.name} and {china.name} can be recruited on the first round.")],
        ['color', ["#fff","#eee5b8", "#d3ddb6", "#1f3926"]],
        ['other', 'undo icon', 'free_undo', _(f"Get +1 Undo after each round.")],
        ['color', ["#fff","#c8fff8", "#5ab3fc", "#0e2a42"]],
        ['color', ["#fff","#f4eeaa", "#d29b75", "#000"]],
        # ['other', 'side oghi','all_pilots', _("Unlock remaining pilots.")],
        ['color', ["#fff","#f6f6e9", "#333", "#00258b"]],
        ['color', ["#fff","#555", "#555", "#fff"]],
        
        ]

screen s_shop_persistent():
    
    use s_chess_dismiss()
    add "#0004"
    use s_chessboard_viewport(chess, xinit=0.8)

    dismiss:
        action NullAction()

    textbutton _("< BACK") action Jump('start') text_style 'style_3d_big_txt':
        at t_interactive
        
    vpgrid:
        cols 1
        xalign 0.8
        style_prefix "s_shop"
        for index,reward in enumerate(run_rewards):

            button at t_interactive:
                style 'empty'
                xysize (1000,100)
                sensitive persistent.best_run >= index #int(index + math.exp(index*0.1)-1)

                if reward[0] == 'color':
                    if persistent.style_colors == reward[1]:
                        add "#1797d3"
                    action SetField(persistent,'style_colors', reward[1]), Function(chess.create_board_img)
                else:
                    action ToggleField(persistent,reward[2])
                    if getattr(persistent,reward[2]):
                        add "#1797d3"

                hbox:
                    frame:
                        yalign 0.5
                        xsize 270
                        style 'empty'
                        text _("ROUND [index]\nreward") yalign 0.5

                    if reward[0] == 'color':
                        grid 2 2:
                            add Solid(reward[1][0]) xysize(50,50)
                            add Solid(reward[1][1])  xysize(50,50)
                            add Solid(reward[1][2])  xysize(50,50)
                            add Solid(reward[1][3]) xysize(50,50)
                        frame:
                            style 'empty'
                            xfill True yfill True
                            text _('board color') size 35 align 0.5,0.5

                    else:
                        add reward[1] xysize(100,100) nearest True
                        frame:
                            style 'empty'
                            xfill True yfill True
                            text reward[3] size 35 align 0.5,0.5
        

style s_shop_text:
    color "#fff"
