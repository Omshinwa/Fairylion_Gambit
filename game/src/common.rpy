# credits: Jse

# we have game.is_over that states if the game is over or not
# game.isWin() and game.isLost() returns a bool whetever the game is won or lost
# they evaluate game.win_con and game.lose_con, which contain a string that states the
# win and loss conditions

# l_gameLoop_everyInteraction is called on any interaction
# they call game.lost_label and game.win_label
# the default labels are l_after_successful_mission and l_after_failed_mission
# which will call label_Win and label_Lost

label l_null:
    return

init python:
    def remove_blur_master():
        renpy.layer_at_list([], layer="master")

label l_close_pop_up:
    # used to close pop up windows (like pilot info window)
    $ Move.engine = chess
    $ remove_blur_master()
    call screen s_pauseScreen(hard_stop=True) # so it doesnt move ahead during exp screens
    return

screen s_popup_blurry_screen():
    on "show" action Function(renpy.layer_at_list, [t_blur], layer="master")
    # this blurs everything on the master layer
    add "#0009"
    button:
        action Hide(None, Dissolve(.2)),Jump('l_close_pop_up')

label l_gameLoop():
    $ g.state = {"battle"}
    with dissolve
    $ renpy.restart_interaction()
    call l_enemy_play()
    call screen s_pauseScreen(hard_stop=True)

    label .gameLoop: #only enter on returns
        call l_gameLoop_everyInteraction
        call l_enemy_play()
        call l_gameLoop_everyInteraction
        $ g.state = {"battle"}
        call screen s_pauseScreen(hard_stop=False)
        jump .gameLoop

label l_gameLoop_everyInteraction():
    if chess.wait_for_enemy:
        return
    if game.isWin():
        $ game.is_over = 'win'
        pause 0.2
        $ done_flag["oncePerFight"] = Set()
        $ g.state = {'cutscene'}
        call l_animation_win
        $ renpy.jump(game.win_label)
    elif game.isLost():
        label .give_up:
        $ game.is_over = 'loss'
        pause 0.5
        $ g.state = {'cutscene'}
        call l_animation_lost
        call expression game.lost_label
    if renpy.has_label(game.endTurn): #shouldnt i call this before checking for win/loss?
        $ g.state = {'cutscene'}
        call expression game.endTurn
    return

screen s_pauseScreen(hard_stop): # let player interact with screens. if hardstop is false, do it only once.
    layer 'master'
    zorder -99
    dismiss:
        if not hard_stop:
            action Return()
        else:
            action NullAction()
                    
init python:
    def not_done(flag:str, which=None) -> bool:
        """
        if not_done is tested with several conditions, test it last.

        :which: "oncePerRun" "oncePerFight"
        """
        if which == None:
            which = "oncePerRun"
        if flag not in done_flag[which]:
            done_flag[which].add(flag)
            return True
        else:
            return False
    def has_done(flag:str, which=None) -> bool:
        """
        if not_done is tested with several conditions, test it last.

        :which: "oncePerRun" "oncePerFight"
        """
        if which == None:
            which = "oncePerRun"
        if flag not in done_flag[which]:
            return False
        else:
            return True