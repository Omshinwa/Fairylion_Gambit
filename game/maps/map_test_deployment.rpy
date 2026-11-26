# TEST MAP, not part of the story yet: a story-mode deployment, like the fights after kaworu joins
# will have (they use the roguelite battle generator, see ai_prompt/prompt.md).
# Start it from the console with:  jump l_test_story_deployment
#
# kallen (ROOK) and kaworu (KNIGHT) have an affinity of 10: put them both in the QUEEN to co-drive it
# (src/queen_co_drive.rpy). The ship is unlocked with 8 TECH: after the win, try the SHIP button.

label l_test_story_deployment:
    scene
    scene onlayer screens
    $ rogue = False # story mode
    $ g.progress = 101 # after map 1-0
    $ TEAM = [lelouch, kallen, kaworu, nunnally]
    $ affinity_reset()
    $ AFFINITY[('kallen', 'kaworu')] = QUEEN_CO_DRIVE_AFFINITY
    $ ship_unlocked = True # the SHIP button of the world map (src/ship.rpy)
    $ TECH = 8
    python:
        for pilot in TEAM:
            pilot.health = pilot.max_health
            pilot.deployed = False
        ROBOTS = [Robot_Piece('q', color=0), Robot_Piece('r', color=0), Robot_Piece('n', color=0), Robot_Piece('p', color=0)]
        story_battles = Roguelike() # the story's random battles (src/story_battles.rpy): the flag goes on after a win
        story_battles.round = 2
        story_battles.setup_rogue()
        Pilot.sort(TEAM, 'default')
        ROBOTS.sort(key=lambda element: (-element.value, element.fen == 'n'))
    $ game = Game('l_map_1_test') # a chapter 1 battle: the rewards screen shows after the win
    jump l_preparation

# TEST: the rewards screen of a won day, with pilots in every room of the ship (src/ship.rpy):
# kaworu in the training room, cc and china in the (extended) rest room (half the time they share a coffee),
# nunnally in the heavy gravity room, oghi in the healing tank, stanley (who learned every skill) teaches abel
# in the classroom, suzaku rests normally. lelouch and kallen fought, kallen made the checkmate.
# Start it from the console with:  jump l_test_ship_rewards
label l_test_ship_rewards:
    scene
    scene onlayer screens
    $ rogue = False # story mode
    $ g.progress = 101 # after map 1-0
    $ TEAM = [lelouch, kallen, kaworu, nunnally, cc, china, oghi, stanley, abel, suzaku]
    $ affinity_reset()
    $ ship_unlocked = True
    python:
        for pilot in TEAM:
            pilot.deployed = False
        lelouch.deployed = True
        kallen.deployed = True
        rewards_checkmate = [kallen]
        rewards_seats = set()
        rewards_pending = True # l_map_select shows the day's rewards
        kallen.health = 2
        for pilot in (kaworu, nunnally, cc, china, oghi, stanley, abel, suzaku): # stamina to recover, to see each room's rest
            pilot.health = 1
        stanley.xp = 5 # the classroom's teacher gives them to abel
        stanley.skills['can_learn'] = [] # MAX: nothing left to learn (a test shortcut: the skills aren't really learned)
        SHIP_RESEARCHED = set(SHIP_ROOM_KINDS)
        SHIP_ROOMS = {}
        for kind in SHIP_ROOM_KINDS:
            SHIP_ROOMS[kind] = ShipRoom(kind)
        SHIP_ROOMS['rest'].size = 2
        ship_assign(kaworu, SHIP_ROOMS['training'])
        ship_assign(cc, SHIP_ROOMS['rest'])
        ship_assign(china, SHIP_ROOMS['rest'])
        ship_assign(nunnally, SHIP_ROOMS['gravity'])
        ship_assign(oghi, SHIP_ROOMS['healing'])
        ship_assign(stanley, SHIP_ROOMS['classroom'])
        ship_assign(abel, SHIP_ROOMS['classroom'])
        TECH = 4
        story_battles = Roguelike() # the story's random battles and robots (src/story_battles.rpy)
        story_battles.round = 1
        ROBOTS = [story_new_robot(fen) for fen in STORY_START_ROBOTS]
        for robot in ROBOTS: # lelouch drove the KING, kallen the ROOK: the PAWN didn't fight, +1 TECH
            robot.deployed = robot.type != '^'
    $ game = Game('l_map_1_test')
    "TEST: a won day. Next, the rewards screen: the RESERVE column shows who rested, and in which room of the ship."
    jump l_map_select
