testsuite map_0_4_tests:

    testcase map_0_4_jagen_death_and_undo:
        description "Play rook f1->d2 (bad move), enemy takes rook, jagen dies, then undo removes him from DEAD_OR_DESERT"

        run Jump("l_map_0_4")
        skip until screen "s_start_battle"
        assert "Draw against the enemy"
        click until eval ('battle' in g.state)

        # Bad move: rook f1 -> d2, leaves the rook exposed
        click until id "piece_f1"
        click id "piece_f1"
        pause until id "move_d2"
        click id "move_d2"

        # Enemy should capture the rook, killing jagen
        pause until eval (not chess.wait_for_enemy) timeout 10.0

        # Jagen's death line must appear
        assert "My Lord... I've fufilled my duty..."

        # Jagen should now be in DEAD_OR_DESERT
        assert eval (jagen in DEAD_OR_DESERT) timeout 2.0

        # Undo the capture; jagen should be revived (removed from DEAD_OR_DESERT)
        $ chess.undo_item()
        assert eval (jagen not in DEAD_OR_DESERT) timeout 2.0
