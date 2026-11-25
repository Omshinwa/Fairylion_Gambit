# TEST MAP, not part of the story yet: a story-mode deployment, like the fights after kaworu joins
# will have (they use the roguelite battle generator, see ai_prompt/prompt.md).
# Start it from the console with:  jump l_test_story_deployment
#
# kallen (ROOK) and kaworu (KNIGHT) have an affinity of 10: put them both in the QUEEN to co-drive it
# (src/queen_co_drive.rpy).

label l_test_story_deployment:
    scene
    scene onlayer screens
    $ rogue = False # story mode
    $ g.progress = 101 # after map 1-0
    $ TEAM = [lelouch, kallen, kaworu]
    $ affinity_reset()
    $ AFFINITY[('kallen', 'kaworu')] = QUEEN_CO_DRIVE_AFFINITY
    python:
        for pilot in TEAM:
            pilot.health = pilot.max_health
            pilot.deployed = False
        ROBOTS = [Robot_Piece('q', color=0), Robot_Piece('r', color=0), Robot_Piece('n', color=0)]
        generator = Roguelike() # the roguelite battle generator, without starting a roguelite run
        generator.round = 2
        generator.setup_rogue()
        Pilot.sort(TEAM, 'default')
        ROBOTS.sort(key=lambda element: (-element.value, element.fen == 'n'))
    $ game = Game('l_map_1_test') # a chapter 1 battle: the rewards screen shows after the win
    jump l_preparation
