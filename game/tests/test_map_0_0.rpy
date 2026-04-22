# Tests for l_map_0_0 (first tutorial battle)
#
# Key behaviours under test:
#   1. Win:       capturing all white pawns fires the win screen immediately.
#                 win_con = "len(chess.get_pieces(0)) == 0"
#                 isWin() fires BEFORE endTurn, so "White skips their turn." is
#                 never shown — the game ends cleanly.
#
#   2. Stalemate: white still has a pawn but zero legal moves →
#                 l_map_0_0_endTurn detects chess.is_stalemated(0) and narrates
#                 "White skips their turn.", then sets chess.side = 1 so the
#                 player can continue.  The pawn remains on the board.
#
#   3. Lose:      any white pawn reaching y=7 (back rank) fires isLost() via
#                 lose_con = "any(pawn.y == 7 for pawn in chess.PIECELIST[0]['p'])"
#                 The AI (white, maximising eval_map_0_0) advances a pawn at y=6
#                 in one move → lost screen appears.
#
# Board dimensions: 7 cols (a–g) × 8 rows (y=0–7).
#   y=7 = row 8 = back rank (lethal for white pawns).
#   Player = black (side 1).  AI = white (side 0).
#
# All testcases jump to l_map_0_0 so that game / chess / game.win_con /
# game.lose_con / chess.goal (eval_map_0_0) are initialised normally, then
# use set_fen to drop into the minimal position of interest.

# testsuite map_0_0:
#     # setup:
#     teardown:
#         exit

#     testsuite battle_conditions:

#         testcase win_capture_last_pawn:
#             description "Capturing the only white pawn triggers the win screen (no stalemate msg)"

#             run Jump("l_map_0_0")
#             skip until screen "s_start_battle"
#             click until eval ('battle' in g.state)
#             $ not_done('select_rook', 'onceEveryFight')
#             $ not_done('select_king', 'onceEveryFight')

#             # Position: black rook e7, white pawn e3, black king d8.
#             # The rook slides straight to e3, capturing the pawn.
#             # win_con fires before endTurn → "White skips their turn." must NOT appear.
#             $ chess.set_fen("3k3/4r2/7/7/7/4P2/7/7 b - - 0 1")
#             $ engine.copy(chess)

#             assert eval (renpy.get_widget("s_battlefield", "piece_e7") is not None) timeout 1.0
#             assert eval (renpy.get_widget("s_battlefield", "piece_e3") is not None)

#             click until id "piece_e7"
#             click id "piece_e7"
#             pause until id "move_e3"
#             click id "move_e3"

#             # l_animation_win shows the "victory" displayable.
#             pause until eval (renpy.showing("victory", layer="screens")) timeout 10.0

#         testcase stalemate_white_skips_turn:
#             description "White pawn blocked by a rook: skip message shown, battle continues"

#             run Jump("l_map_0_0")
#             skip until screen "s_start_battle"
#             click until eval ('battle' in g.state)
#             $ not_done('select_rook', 'onceEveryFight')
#             $ not_done('select_king', 'onceEveryFight')

#             # Position:
#             #   Black king a8  (safe corner, well away from the action)
#             #   Black rook d7  (directly ahead of white pawn → blocks forward move)
#             #   Black rook f7  (free rook to give black a legal move)
#             #   White pawn d6  (y=5; forward sq blocked, no diagonal captures, y>1 so
#             #                   no double-move → zero legal moves → stalemated)
#             $ chess.set_fen("k6/3r1r1/3P3/7/7/7/7/7 b - - 0 1")
#             $ engine.copy(chess)

#             assert eval (renpy.get_widget("s_battlefield", "piece_d6") is not None) timeout 1.0
#             assert eval (renpy.get_widget("s_battlefield", "piece_d7") is not None)

#             # Black moves the free rook f7 → f6.
#             # Afterwards chess.side == 0 and the pawn is still fully blocked.
#             click until id "piece_f7"
#             click id "piece_f7"
#             pause until id "move_f6"
#             click id "move_f6"

#             # l_map_0_0_endTurn detects is_stalemated(0) and shows this line.
#             assert "White skips their turn." timeout 5.0
#             # Dismiss the dialog; game resets chess.side = 1 and returns to battle.
#             click until eval ('battle' in g.state) timeout 10.0

#             # The pawn must still be there — win_con must not have fired.
#             assert eval (renpy.get_widget("s_battlefield", "piece_d6") is not None)


#         testcase lose_pawn_reaches_back_rank:
#             description "White pawn one step from y=7: AI advances it, lose screen appears"

#             run Jump("l_map_0_0")
#             skip until screen "s_start_battle"
#             click until eval ('battle' in g.state)
#             $ not_done('select_rook', 'onceEveryFight')
#             $ not_done('select_king', 'onceEveryFight')

#             # Position:
#             #   Black king a8  (col 0, y=7 — does not block col 3)
#             #   White pawn d7  (col 3, y=6 — one step from the back rank d8)
#             #   Black rook g2  (col 6, y=1 — only black piece that moves;
#             #                   retreating to g1 leaves the pawn path clear)
#             $ chess.set_fen("k6/3P3/7/7/7/7/6r/7 b - - 0 1")
#             $ engine.copy(chess)

#             assert eval (renpy.get_widget("s_battlefield", "piece_d7") is not None) timeout 1.0
#             assert eval (renpy.get_widget("s_battlefield", "piece_g2") is not None)

#             # Black moves the rook away; d8 remains empty.
#             click until id "piece_g2"
#             click id "piece_g2"
#             pause until id "move_g1"
#             click id "move_g1"

#             # White AI finds d7→d8 at depth 1 (eval_map_0_0 returns MAX_SCORE for
#             # pawn.y == 7). isLost() fires → l_animation_lost shows the "lost" image.
#             pause until eval (renpy.showing("lost", layer="screens")) timeout 15.0
