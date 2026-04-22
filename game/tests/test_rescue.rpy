# Tests for rescue on Chess_control (rpy-side), in particular pawn double-move
# rescue: a pawn at its starting rank double-moves onto a friendly infantry
# carrying a pilot. The pilot must transfer, the infantry must be removed, and
# undo() must cleanly restore the prior state.
#
# Scenario under test: default position, a pawn manually given _pilot=[None,None]
# (Robot_Piece.__init__ forces [None], so we write directly), and an infantry
# with a pilot two squares ahead. After the double-move rescue:
#   - pawn is at the infantry's old square
#   - pawn._pilot contains the rescued pilot (NOT empty)
#   - infantry is removed from the piecelist
#   - undo() restores both positions and clears the pawn slot

# testsuite rescue:
#     setup:
#         run Jump('load_standard_pos')
#         $ game = Game('l_osef')
#         run Preference("all mute", True)
#     teardown:
#         exit

#     testsuite pawn_double_move_rescue:

#         testcase pawn_double_move_rescues_pilot_from_infantry:
#             description "Pawn with 2 pilot slots double-moves onto infantry: pilot transfers, undo works"

#             $ chess = Chess_control((8, 8))
#             $ chess.set_fen("8/8/8/8/8/8/8/8 w - - 0 1")
            
#             assert eval ("chess['a1'] == 1") timeout 2.0

#             # Kings (required for is_in_check during make_move)
#             $ white_king = Robot_Piece('k', color=0)
#             $ chess.drop(white_king, chess.TO_POS('a1'))
#             $ black_king = Robot_Piece('k', color=1)
#             $ chess.drop(black_king, chess.TO_POS('h8'))

#             # White pawn at e2 with TWO pilot slots (direct write — the setter
#             # clamps list length to the existing _pilot length).
#             $ pawn = Robot_Piece('p', color=0)
#             $ chess.drop(pawn, chess.TO_POS('e2'))
#             $ pawn._pilot = [None, None]

#             # Friendly infantry at e4 carrying a pilot
#             $ gp = GenericPilot()
#             $ infantry = Robot_Piece('i', color=0, pilot=gp)
#             $ chess.drop(infantry, chess.TO_POS('e4'))

#             $ chess.start()
#             $ engine.copy(chess)

#             # Find the rescue+double-move the pawn should have.
#             # NOTE: `set` inside $-blocks is RevertableSet; move.flag is a plain
#             # Python set, so avoid `isinstance(m.flag, set)` here — it's False.
#             $ rescue_moves = [m for m in pawn.moves(chess) if 'rescue' in m.flag and 'double move' in m.flag]
#             assert eval (len(rescue_moves) == 1) timeout 1.0

#             $ move = rescue_moves[0]
#             $ chess.make_move(move, check_legality=False)

#             # Pawn at e4, infantry removed, pilot transferred to pawn
#             assert eval (chess.board[chess.TO_POS('e4')] is pawn) timeout 1.0
#             assert eval (chess.board[chess.TO_POS('e2')] == c.EMPTY) timeout 1.0
#             assert eval (gp in pawn._pilot) timeout 1.0
#             assert eval (len(pawn._pilot) == 2) timeout 1.0
#             assert eval (infantry not in chess.get_pieces(0)) timeout 1.0

#             # Undo restores everything
#             $ chess.undo()
#             assert eval (chess.board[chess.TO_POS('e2')] is pawn) timeout 1.0
#             assert eval (chess.board[chess.TO_POS('e4')] is infantry) timeout 1.0
#             assert eval (gp not in pawn._pilot) timeout 1.0
#             assert eval (pawn._pilot == [None, None]) timeout 1.0
#             assert eval (infantry in chess.get_pieces(0)) timeout 1.0


#         testcase pawn_full_slots_cannot_double_rescue:
#             description "Pawn with no free pilot slots has no rescue move generated (single or double)"

#             $ chess = Chess_control((8, 8))
#             $ chess.set_fen("8/8/8/8/8/8/8/8 w - - 0 1")

#             $ white_king = Robot_Piece('k', color=0)
#             $ chess.drop(white_king, chess.TO_POS('a1'))
#             $ black_king = Robot_Piece('k', color=1)
#             $ chess.drop(black_king, chess.TO_POS('h8'))

#             # Pawn at e2 with its single slot occupied (no room for another pilot)
#             $ existing = GenericPilot()
#             $ pawn = Robot_Piece('p', color=0, pilot=existing)
#             $ chess.drop(pawn, chess.TO_POS('e2'))

#             # Friendly infantry at e4 with a pilot — rescue would fire if allowed
#             $ gp = GenericPilot()
#             $ infantry_double = Robot_Piece('i', color=0, pilot=gp)
#             $ chess.drop(infantry_double, chess.TO_POS('e4'))

#             $ chess.start()
#             $ engine.copy(chess)

#             $ flags = [m.flag for m in pawn.moves(chess)]
#             assert eval (not any('rescue' in f for f in flags)) timeout 1.0


#         testcase pawn_single_rescue_transfers_pilot:
#             description "Pawn single-step rescue: pilot transfers, undo restores"

#             $ chess = Chess_control((8, 8))
#             $ chess.set_fen("8/8/8/8/8/8/8/8 w - - 0 1")

#             $ white_king = Robot_Piece('k', color=0)
#             $ chess.drop(white_king, chess.TO_POS('a1'))
#             $ black_king = Robot_Piece('k', color=1)
#             $ chess.drop(black_king, chess.TO_POS('h8'))

#             $ pawn = Robot_Piece('p', color=0)
#             $ chess.drop(pawn, chess.TO_POS('e2'))

#             $ gp = GenericPilot()
#             $ infantry = Robot_Piece('i', color=0, pilot=gp)
#             $ chess.drop(infantry, chess.TO_POS('e3'))

#             $ chess.start()
#             $ engine.copy(chess)

#             $ rescue_moves = [m for m in pawn.moves(chess) if 'rescue' in m.flag and 'double move' not in m.flag]
#             assert eval (len(rescue_moves) == 1) timeout 1.0

#             $ move = rescue_moves[0]
#             $ chess.make_move(move, check_legality=False)

#             assert eval (chess.board[chess.TO_POS('e3')] is pawn) timeout 1.0
#             assert eval (gp in pawn._pilot) timeout 1.0
#             assert eval (infantry not in chess.get_pieces(0)) timeout 1.0

#             $ chess.undo()
#             assert eval (chess.board[chess.TO_POS('e2')] is pawn) timeout 1.0
#             assert eval (chess.board[chess.TO_POS('e3')] is infantry) timeout 1.0
#             assert eval (gp not in pawn._pilot) timeout 1.0
