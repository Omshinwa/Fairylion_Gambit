# BATTLE REWARDS
# The rewards screen (s_result_screen in src/roguelike_events.rpy):
# +1 EXP for every pilot who fought, rest for the others (pilot.rest()), +2 EXP for the checkmate.
# The EXP and the rest are given in l_battle_rewards below. In story mode, the day's affinity too
# (affinity_day_won in src/affinity.rpy).
#
#   roguelite:  after each won battle, l_result_screen (src/roguelike.rpy) calls l_battle_rewards.
#   story mode: from map 1-0 on (not the tutorial maps 0-x), once per day, right before the new day:
#               l_new_day (src/day.rpy) calls l_story_day_rewards. A day can have several battles
#               (map 1-0 has two): who fought in any of them gets the EXP, the last one's checkmate gets the +2.
#
# Who fought is pilot.deployed: set by the preparation in roguelite. In story mode, it's every pilot on the
# player's side when a battle starts (rewards_battle_start) or is won (rewards_battle_won).

default rewards_checkmate = [] # pilots of the last won battle's checkmate (in story mode the board is gone by the rewards)
default rewards_pending = False # story mode: a battle was won today, l_new_day shows the rewards
default rewards_seats = set() # story mode: pairs of pilots who sat in the same CHESSMAN today (+3 affinity)

init python:
    def story_rewards_battle():
        """True for a story battle that gets the rewards screen: maps 1-0 and later."""
        if rogue or not game.level.startswith('l_map_'):
            return False
        chapter = game.level[len('l_map_'):].split('_')[0] # 'l_map_1_0_bis' -> '1'
        return chapter.isdigit() and int(chapter) >= 1

    def rewards_mark_fighters():
        """Story mode: every pilot on the player's side fought today (pilot.deployed, reset by the day's rewards)."""
        for piece in chess.get_pieces(chess.player):
            for pilot in piece.pilots:
                pilot.deployed = True

    def rewards_battle_start():
        """Called when a battle starts (l_start_battle)."""
        if story_rewards_battle():
            rewards_mark_fighters()

    def rewards_checkmate_pilots():
        """Pilots of the piece that made the winning move, if it's the player's: they get +2 EXP."""
        if not chess.history:
            return []
        piece = chess.history[-1].move.piece
        if piece.color != chess.player:
            return []
        return list(piece.pilots)

    def rewards_battle_won():
        """Called when a battle is won (l_after_successful_mission), while the board is still there."""
        global rewards_checkmate, rewards_pending
        rewards_checkmate = rewards_checkmate_pilots()
        if story_rewards_battle():
            rewards_mark_fighters() # pilots who joined during the battle also fought (like lelouch's KING in map 1-0)
            # pilots sharing a CHESSMAN: story mode has no ROBOTS list yet, its robots are the player's pieces
            rewards_seats.update(affinity_seat_pairs()) # see src/affinity.rpy
            rewards_pending = True

# Shared by roguelite and story mode. s_result_screen must be showing; each step waits for a click.
label l_battle_rewards:
    pause
    $ renpy.set_screen_variable('state', 1, screen='s_result_screen')

    python: ### EXP for who fought, rest for the others
        for pilot in TEAM:
            # ignore the dead
            if pilot.health <= 0:
                continue

            if pilot.deployed:
                pilot.increase_xp(1)
                renpy.play('sound/misc/xp.wav', channel='sound')
                if renpy.get_screen_variable('state', screen='s_result_screen') == 1:
                    renpy.pause(0.3, modal=False)

        for pilot in TEAM:
            # ignore the dead
            if pilot.health <= 0:
                continue

            # if we didnt use a pilot, rest it:
            if not pilot.deployed:
                if pilot.rest():
                    renpy.play('sound/misc/xp.wav', channel='sound')
                    if renpy.get_screen_variable('state', screen='s_result_screen') == 1:
                        renpy.pause(0.3, modal=False)

    $ renpy.set_screen_variable('state', 2, screen='s_result_screen')
    pause
    $ renpy.set_screen_variable('state', 3, screen='s_result_screen')

    python: ### give XP to the checkmating piece
        if len(rewards_checkmate) == 1:
            rewards_checkmate[0].increase_xp(2)
        elif len(rewards_checkmate) >= 2:
            rewards_checkmate[0].increase_xp(2)
            rewards_checkmate[1].increase_xp(2)
        renpy.play('sound/misc/boost.wav')

    if renpy.get_screen_variable('state', screen='s_result_screen')<4:
        pause
        $ renpy.set_screen_variable('state', 4, screen='s_result_screen')
    return

# Story mode: the rewards of the day's battles, on the map (called by l_new_day).
label l_story_day_rewards:
    if not renpy.get_screen('s_result_screen'): # l_map_select usually shows it already, with the map
        show screen s_result_screen
        with dissolve
    call l_battle_rewards
    hide screen s_result_screen
    with dissolve
    python:
        affinity_day_won([pilot for pilot in TEAM if pilot.deployed], rewards_seats) # see src/affinity.rpy
        for pilot in TEAM:
            pilot.deployed = False
        rewards_seats.clear()
    $ rewards_pending = False
    return
