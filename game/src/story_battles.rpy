# STORY MODE'S RANDOM BATTLES. See The ship and Robots in ai_prompt/prompt.md.
#   - From g.progress STORY_RANDOM_FROM on (after map 1-0 for now: maps/map_1_1.rpy is still a draft), the world map's
#     flag starts a random battle, made by the roguelite's generator (Roguelike in src/roguelike.rpy). Move
#     STORY_RANDOM_FROM when the next maps are written. The ship unlocks then (src/ship.rpy), and the player gets
#     their first robots: a KING, a ROOK and a PAWN.
#   - A random battle is a normal story day: deployment (with the SHIP button), battle, rewards on the map, new day.
#     It doesn't move g.progress.
#   - Losing reloads the checkpoint saved when the flag was clicked, like the story maps (l_after_failed_mission).
#   - Robots: ROBOTS is the player's robots and keeps them all, destroyed ones too (repairing them comes later).
#     The generator gives no free robots in story mode: more robots will be bought from the United Nations.
#     The KING is the one the generator puts in the middle of the back row. PAWNS are limited to the PAWN robots
#     of ROBOTS (the roguelite has unlimited pawns): a pilot dropped on the pawn row takes one.

default story_battles = None # the generator of the random battles, a Roguelike (src/roguelike.rpy)
define STORY_START_ROBOTS = ['k', 'r', 'p'] # the robots the player gets when the random battles start
define STORY_BATTLE_LABEL = 'l_story_battle'
define STORY_RANDOM_FROM = 101 # g.progress of the first random battle: the written maps end there

init python:
    def story_map_label(chapter=None, mission=None):
        """The label of the story map for g.progress (or for that chapter and mission)."""
        if chapter is None:
            chapter, mission = g.progress // 100, g.progress % 100
        return 'l_map_{}_{}'.format(chapter, mission)

    def story_random_part(progress=None):
        """True once the written maps are over (g.progress, or the given progress, reached STORY_RANDOM_FROM)."""
        return (g.progress if progress is None else progress) >= STORY_RANDOM_FROM

    def story_next_battle(chapter, mission):
        """The label the world map's flag jumps to: the story map, or a random battle after the written ones."""
        if story_random_part(int(chapter) * 100 + int(mission)):
            return STORY_BATTLE_LABEL
        return story_map_label(chapter, mission)

    def story_new_robot(fen):
        """A robot of the player, made for the current board. The KING has no pilot yet and stays where the generator puts it."""
        if fen == 'k':
            return Robot_Piece('k', color=2, unmovable=True)
        return Robot_Piece(fen, color=0)

    def story_random_start():
        """The written maps are over: the random battles start, with the ship and the first robots."""
        global story_battles, ROBOTS, ship_unlocked
        ship_unlocked = True
        ROBOTS = [story_new_robot(fen) for fen in STORY_START_ROBOTS]
        story_battles = Roguelike()
        story_battles.round = 1

    def story_robots_refresh():
        """The same robots, made again for the new board: a robot computes its moves on the board it was made for,
        and the world map makes a new board after every battle (reset_board in maps/s_map_select.rpy)."""
        global ROBOTS
        ROBOTS = [story_new_robot(DEFAULT_ROBOT[robot.type]) for robot in ROBOTS]

    def story_king():
        """Story mode: the player's KING robot, for the generator to put on the board (None: the generator makes one)."""
        if rogue:
            return None
        for robot in ROBOTS:
            if robot.type == '#' and not robot.deployed:
                robot.deployed = True
                return robot
        return None

    def story_pawns():
        """Story mode: the PAWN robots of ROBOTS that aren't on the board yet."""
        return [robot for robot in ROBOTS if robot.type == '^' and not robot.deployed]

    def story_pawn_free(pos):
        """Can a pilot be put on this square of the pawn row? The roguelite has unlimited pawns;
        story mode needs a PAWN robot left, or a pawn already on the square (the pilot takes its place)."""
        target = chess.board[pos]
        return bool(rogue) or bool(story_pawns()) or (isinstance(target, Robot_Piece) and target.type == '^')

    def story_battle_setup():
        global game, story_battles
        if story_battles is None: # a save from before the random battles
            story_battles = Roguelike()
            story_battles.round = 1
        story_robots_refresh()
        for pilot in TEAM:
            pilot.deployed = False
        story_battles.setup_rogue() # board and enemies; the KING comes from ROBOTS (story_king)
        Pilot.sort(TEAM, 'default')
        ROBOTS.sort(key=lambda element: (-element.value, element.fen == 'n'))
        game = Game(STORY_BATTLE_LABEL, random_battle=True) # random_battle: rewards, and no g.progress (src/game_manager.rpy)

label l_story_battle:
    scene
    scene onlayer screens
    $ story_battle_setup()
    jump l_preparation

label l_story_battle_start:
    if not 'q' in chess.promotions[1-chess.player]: # enemy pawns can promote, like in the roguelite (l_map_rogue_start)
        $ chess.promotions[1].append('q')
    return

label l_story_battle_Win:
    $ story_battles.won() # the next one is harder
    return
