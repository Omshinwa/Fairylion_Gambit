# g is the campaign variable
default -2 TEAM = [] # pilots currently recruited
default -2 ROBOTS = [] # mechs currently 
default -2 DEAD_OR_DESERT = [] # when pilots die / desert, they go there.
default -2 g.progress = 0  # 304 would be chapter 3, mission 4
default -2 g.state = {'cutscene'}
default -2 g.items = {
    'undo':0,
    # tarot items
    'empress':0,
}
default -2 g.money = 0
default g.difficulty = 'normal'
default done_flag = {'oncePerFight':set(), 'oncePerRun':set(), 'onceEveryFight':set(), 'buttons':set()}

#              ███   █████████    █████████   ██████   ██████ ██████████
#            ███░   ███░░░░░███  ███░░░░░███ ░░██████ ██████ ░░███░░░░░█
#          ███░    ███     ░░░  ░███    ░███  ░███░█████░███  ░███  █ ░ 
#        ███░     ░███          ░███████████  ░███░░███ ░███  ░██████   
#      ███░       ░███    █████ ░███░░░░░███  ░███ ░░░  ░███  ░███░░█   
#    ███░         ░░███  ░░███  ░███    ░███  ░███      ░███  ░███ ░   █
#  ███░            ░░█████████  █████   █████ █████     █████ ██████████
# ░░░               ░░░░░░░░░  ░░░░░   ░░░░░ ░░░░░     ░░░░░ ░░░░░░░░░░ 
init python:
    class Game():
        # handles event stuff for a single battle.
        def __init__(self, level=None, **kwargs):
            global chess
            if "needOnlyOneWin" in kwargs:
                self.needOnlyOneWin = kwargs["needOnlyOneWin"]
            else:
                self.needOnlyOneWin = True
            # self.player = chess.player # by default we play from White's perspective
            self.level = level or ("l_map_" + str(g.progress//100) + "_" + str(g.progress%100))
            self.win_con = None # checkmate / survive / else
            self.lose_con = None # Game has additional possible loss conditions, win conditions are on the chess
            self.max_turn = 0
            self.is_over = False

            self.puzzle = False
            self.endTurn = self.level + "_endTurn"

            self.move_callback = None # eg: remove tarots one turn effects

            self.win_label = 'l_after_successful_mission'
            self.lost_label = 'l_after_failed_mission'

            self.undoable_move = -1

            self.custom_objective = None # text display for the start battle screen

            for key,value in kwargs.items():
                setattr(self, key, value)

        def isWin(self):
            global chess
            if self.win_con:
                return eval(self.win_con)
            else:
                result = chess.result()
                return (result[0] is True and result[1] == chess.player)

        def isLost(self):
            if self.lose_con:
                return eval(self.lose_con)
            else:
                result = chess.result()
                return (result[0] is True and result[1] != chess.player)

        @property
        def turnLeft(self):
            return self.max_turn - self.turn

    class DotDict:
        # convert dict to set them as attribute, usage example:
        # self.ui['animation_move'] = DotDict(piece=None, fr=None, to=None, time=None)
        # Usage: self.ui['animation_move'].piece
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

label l_after_successful_mission:
    $ g.progress += 1
    if renpy.has_label (game.level + "_Win"):
        call expression game.level + "_Win"
    show black onlayer screens with transition_bars
    jump l_map_select

label l_after_failed_mission:
    if renpy.has_label (game.level + "_Lost"):
        call expression game.level + "_Lost"
    if game.is_over == 'loss': # we can change the value of game.is_over to avoid loss
        show black onlayer screens with transition_bars
        if renpy.can_load(LOCAL_CHECKPOINT_SLOT):
            $ renpy.load(LOCAL_CHECKPOINT_SLOT)
    "failed to load the checkpoint"
    return

label l_animation_win:
    scene onlayer screens
    $ chess_camera.reset_dezoom_view()
    play audio "sound/misc/cheers.wav"
    show victory onlayer screens zorder 2 with pointillisme
    play audio "sound/misc/MISSION COMPLETE.wav"
    pause 0.8
    scene onlayer screens
    return

label l_animation_lost:
    scene onlayer screens
    $ chess_camera.reset_dezoom_view()
    play audio "sound/misc/YUHELI_00.wav"
    if chess.is_stalemated(1-chess.player):
        show draw onlayer screens zorder 2 with pointillisme
    else:
        show lost onlayer screens zorder 2 with pointillisme
    call screen s_pauseScreen(False)
    scene onlayer screens
    if g.items['undo'] and (len(chess.history)>1 or rogue):
        menu:
            "You still have Undos. Use one?"
            "Yes":
                call l_use_item('undo')
            "No":
                return