# BATTLE REWARDS
# After a won battle, the rewards screen (s_in_between_rounds in src/roguelike_events.rpy):
# +1 EXP for every pilot who fought, rest for the others (pilot.rest()), +2 EXP for the checkmate.
#
#   roguelite:  l_result_screen (src/roguelike.rpy) calls l_battle_rewards.
#   story mode: from map 1-0 on (not the tutorial maps 0-x), l_after_successful_mission calls
#               l_story_battle_rewards, before the map's victory dialogue.
#
# Who fought is pilot.deployed: set by the preparation in roguelite. In story mode, it's every pilot on the
# player's side when the battle starts (rewards_battle_start) or ends (l_story_battle_rewards).

init python:
    def story_rewards_battle():
        """True for a story battle that gets the rewards screen: maps 1-0 and later."""
        if rogue or not game.level.startswith('l_map_'):
            return False
        chapter = game.level[len('l_map_'):].split('_')[0] # 'l_map_1_0_bis' -> '1'
        return chapter.isdigit() and int(chapter) >= 1

    def rewards_battle_start():
        """Called when a battle starts (l_start_battle): story mode marks who fights (pilot.deployed)."""
        if not story_rewards_battle():
            return
        fighting = [pilot for piece in chess.get_pieces(chess.player) for pilot in piece.pilots]
        for pilot in TEAM:
            pilot.deployed = pilot in fighting

    def rewards_checkmate_pilots():
        """Pilots of the piece that made the winning move, if it's the player's: they get +2 EXP."""
        if not chess.history:
            return []
        piece = chess.history[-1].move.piece
        if piece.color != chess.player:
            return []
        return list(piece.pilots)

# Shared by roguelite and story mode. s_in_between_rounds must be showing; each step waits for a click.
label l_battle_rewards:
    pause
    $ renpy.set_screen_variable('state', 1, screen='s_in_between_rounds')

    python: ### EXP for who fought, rest for the others
        for pilot in TEAM:
            # ignore the dead
            if pilot.health <= 0:
                continue

            if pilot.deployed:
                pilot.increase_xp(1)
                renpy.play('sound/misc/xp.wav', channel='sound')
                if renpy.get_screen_variable('state', screen='s_in_between_rounds') == 1:
                    renpy.pause(0.3, modal=False)

        for pilot in TEAM:
            # ignore the dead
            if pilot.health <= 0:
                continue

            # if we didnt use a pilot, rest it:
            if not pilot.deployed:
                if pilot.rest():
                    renpy.play('sound/misc/xp.wav', channel='sound')
                    if renpy.get_screen_variable('state', screen='s_in_between_rounds') == 1:
                        renpy.pause(0.3, modal=False)

    $ renpy.set_screen_variable('state', 2, screen='s_in_between_rounds')
    pause
    $ renpy.set_screen_variable('state', 3, screen='s_in_between_rounds')

    python: ### give XP to the checkmating piece
        checkmate_pilots = rewards_checkmate_pilots()
        if len(checkmate_pilots) == 1:
            checkmate_pilots[0].increase_xp(2)
        elif len(checkmate_pilots) >= 2:
            checkmate_pilots[0].increase_xp(1)
            checkmate_pilots[1].increase_xp(1)
        renpy.play('sound/misc/boost.wav')

    if renpy.get_screen_variable('state', screen='s_in_between_rounds')<4:
        pause
        $ renpy.set_screen_variable('state', 4, screen='s_in_between_rounds')
    return

# Story mode: the rewards screen over the board, then back to the map's victory dialogue.
label l_story_battle_rewards:
    python: # pilots who joined during the battle also fought (like lelouch's KING in map 1-0)
        for piece in chess.get_pieces(chess.player):
            for pilot in piece.pilots:
                pilot.deployed = True
    $ g.state = {'result_screen'}
    show screen s_in_between_rounds
    with dissolve
    call l_battle_rewards
    hide screen s_in_between_rounds
    with dissolve
    python:
        for pilot in TEAM:
            pilot.deployed = False
    $ g.state = {'cutscene'}
    return
