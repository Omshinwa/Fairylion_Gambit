# Tests for l_tutorial_checkmate_2Q
#
# Key behaviors under test:
#   1. When the player makes a stalemate move, l_map_tutorial_checkmate_Lose
#      detects it (gen_legal_moves() == 0), shows the stalemate dialogue, and
#      calls l_use_item('undo', True) which *jumps* to l_gameLoop.gameLoop.
#      The label therefore never reaches its own `return`, so the game stays
#      in battle — it does NOT navigate to start/game-over.
#   2. The undo item is applied correctly: the queen that caused stalemate is
#      walked back to its previous square, letting the player correct the move.
#
# Stalemate position used:
#   FEN  2k5/7Q/6Q1/8/8/8/8/3K4 w - - 0 1
#   Pieces: White King d1, Queen g6, Queen h7 / Black King c8
#   Qg6 -> b6  gives stalemate: c8 king has no legal squares (b7/b8/c7/d7/d8
#   all covered by Qb6 or Qh7) and is not in check.

testsuite global:
    setup:
        run Preference("all mute", True)

    teardown:
        exit

    testsuite tutorial_checkmate_2Q:

        testcase stalemate_triggers_undo_not_game_over:
            description "Stalemate: undo item fires and battle continues, no game-over"

            run Jump("l_tutorial_checkmate_2Q")
            skip until screen "s_start_battle"
            click until eval ('battle' in g.state)

            # Skip to the interesting part: set up a pre-stalemate position so
            # the test is independent of the full AI move sequence.
            # White King d1, Queens g6 + h7, Black King c8.
            # Next white move Qg6->b6 is the stalemate move.
            $ chess.set_fen('2k5/7Q/6Q1/8/8/8/8/3K4 w - - 0 1')
            $ engine.copy(chess)
            # Verify the expected pieces are in place before the stalemate move.
            assert eval (renpy.get_widget("s_battlefield", "piece_g6") is not None) timeout 1.0
            assert eval (renpy.get_widget("s_battlefield", "piece_h7") is not None)

            # Make the stalemate move: Queen g6 -> b6.
            click until id "piece_g6"
            click id "piece_g6"
            pause until id "move_b6"
            click id "move_b6"
            # The game should show the stalemate explanation, NOT the game-over screen.
            # "draw" is an image shown via `show draw onlayer screens`, not a screen widget.
            pause until eval (renpy.showing("draw", layer="screens")) timeout 2.0

            # l_use_item('undo') jumps to l_gameLoop.gameLoop, so we must
            # end up back in battle — never at the main menu / jump start.
            click until eval ('battle' in g.state) timeout 5.0

            # Undo was applied: the queen is back on g6, not b6.
            assert eval (renpy.get_widget("s_battlefield", "piece_g6") is not None)
            assert eval (renpy.get_widget("s_battlefield", "piece_b6") is None)


        testcase stalemate_allows_corrective_move:
            description "After stalemate undo, player can make a different (non-stalemate) move"

            $ persistent.tutorial_2Q = False
            run Jump("l_tutorial_checkmate_2Q")
            skip until screen "s_start_battle"
            click until eval ('battle' in g.state)

            $ chess.set_fen('2k5/7Q/6Q1/8/8/8/8/3K4 w - - 0 1')
            $ engine.copy(chess)

            # Trigger stalemate.
            click until id "piece_g6"
            click id "piece_g6"
            pause until id "move_b6"
            click id "move_b6"

            # Wait for undo to resolve and battle to resume.
            pause until eval ('battle' in g.state) timeout 15.0

            # Now play the correct checkmate move: Qg6 -> g8 (delivers checkmate,
            # not stalemate — the king is in check and has no escape).
            click until id "piece_g6"
            click id "piece_g6"
            pause until id "move_g8"
            click id "move_g8"

            # The win label fires: persistent.tutorial_2Q should now be set.
            pause until eval (persistent.tutorial_2Q) timeout 10.0
