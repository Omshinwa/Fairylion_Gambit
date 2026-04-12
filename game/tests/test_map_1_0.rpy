# # boilerplate:
# # skip until screen "s_start_battle" # clicks until the show start battle
# # click until eval ('battle' in g.state) # starts the battle
# # now it's waiting for command inputs

testsuite map_1_0:
    setup:
        run Preference("all mute", False)

    teardown:
        exit

    testsuite battle_maps: # 2026 fevrier 16

        testcase map_1_0:
            description "Move g3 to f3 and wait for enemy reply"

            run Jump("l_map_1_0")
            skip until screen "s_start_battle"
            click until eval ('battle' in g.state)
            # check if the button piece_f3 exists
            assert eval (renpy.get_widget("s_battlefield", "piece_f3") is not None)
            click until id "piece_f3"
            click id "piece_f3"
            pause until id "move_f4"
            click id "move_f4"
            pause until eval (not chess.wait_for_enemy) timeout 10.0
    
    
        testcase map_0_4:
            description "Map 0-4 death, see if it's playable"
            # i remember i had an issue with the animation of the piece replaying
            # on death

            $ print(chess)
            run Jump("l_map_0_4")
            skip until screen "s_start_battle"
            assert "Draw against the enemy"
            click until eval ('battle' in g.state)
            click id "piece_h4"
            assert eval (renpy.get_widget("s_battlefield", "move_f5") is not None) 
            pause until id "move_f5"
            click id "move_f5"
            pause until eval (not chess.wait_for_enemy) timeout 10.0