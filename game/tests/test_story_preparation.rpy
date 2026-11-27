# Tests for the story-mode deployment phase: no lone pilot (INFANTRY), and the PAWN robots
# of ROBOTS are counted (src/story_battles.rpy).
#
# Board layout used (6×5):
#
#   ┌────────────────────┐
#   │  . . . K . .   ← rank 5 (enemy)
#   │  . . . . . .   ← rank 4
#   │  . . . . . .   ← rank 3
#   │  . . . . . .   ← rank 2 (pawn rank — white)
#   │  . . . . . .   ← rank 1 (innermost — white)
#   └────────────────────┘
#     a b c d e f
#
#   TEAM = [gp] (GenericPilot, can drive '^')
#   ROBOTS = [pawn_1, pawn_2] (story pawns, not on the board)

testsuite story_preparation:
    setup:
        $ done_flag["oncePerRun"].add('tuto_basic')
        $ done_flag["oncePerRun"].add('tuto_preparation')
        $ done_flag["oncePerRun"].add('tuto_loyalty')
        $ rogue = False

    before testcase:
        $ rogue = False
        $ chess = Chess_control((6, 5))
        $ gp = GenericPilot()
        $ TEAM = [gp]
        $ pawn_1 = Robot_Piece('p', color=0)
        $ pawn_2 = Robot_Piece('p', color=0)
        $ ROBOTS = [pawn_1, pawn_2]
        $ chess.drop(Robot_Piece('k', color=1), chess.TO_POS('d5'))
        $ game = Game('l_map_rogue')
        run Jump('l_preparation')
        pause until screen 's_battlefield'

    testcase pilot_cannot_drop_on_empty_back_row:
        description "A pilot can't be dropped alone on an empty back-row square (no infantry)"

        $ f_select(gp)
        $ renpy.restart_interaction()
        assert eval (chess.ui['moves'].get(chess.TO_POS('e1')) is None) timeout 1.0
        assert eval (chess.ui['moves'].get(chess.TO_POS('e2')) is not None) timeout 1.0

        # even if called directly, nothing is deployed
        $ f_prep_drop_piece(gp, chess.TO_POS('e1'))
        assert eval (chess.board[chess.TO_POS('e1')] is c.EMPTY) timeout 1.0
        assert eval (not gp.deployed) timeout 1.0
        $ f_dismiss()

    testcase pawn_cannot_move_to_back_row:
        description "A deployed pawn can't be moved to the back row"

        $ f_prep_drop_piece(gp, chess.TO_POS('e2'))
        assert eval (chess.board[chess.TO_POS('e2')] is pawn_1) timeout 1.0
        assert eval (len(story_pawns()) == 1) timeout 1.0

        $ f_select(pawn_1)
        $ renpy.restart_interaction()
        assert eval (chess.ui['moves'].get(chess.TO_POS('e1')) is None) timeout 1.0
        assert eval (chess.ui['moves'].get(chess.TO_POS('d2')) is not None) timeout 1.0
        $ f_dismiss()

    testcase pawn_move_along_pawn_row_keeps_its_robot:
        description "Moving a deployed pawn e2 -> d2 keeps the same PAWN robot (no pawn used up)"

        $ f_prep_drop_piece(gp, chess.TO_POS('e2'))
        assert eval (len(story_pawns()) == 1) timeout 1.0

        $ f_select(pawn_1)
        $ renpy.restart_interaction()
        pause 0.3
        $ f_click_on_move_sq(get_drags('battle', child=chess.TO_POS('d2')))
        pause 0.3

        assert eval (chess.board[chess.TO_POS('d2')] is pawn_1) timeout 1.0
        assert eval (chess.board[chess.TO_POS('e2')] is c.EMPTY) timeout 1.0
        assert eval (pawn_1.pilot is gp) timeout 1.0
        assert eval (pawn_1.deployed and gp.deployed) timeout 1.0
        assert eval (len(story_pawns()) == 1) timeout 1.0

        # undeploying it gives the pawn back
        $ f_unprepare(pawn_1)
        assert eval (len(story_pawns()) == 2) timeout 1.0
        assert eval (not gp.deployed) timeout 1.0

    # A deployed KNIGHT dragged onto a deployed QUEEN swaps them. The board was right, but the QUEEN
    # was drawn on top of the KNIGHT: its drag (same loop index, same square) kept the drop position.
    testcase drag_swap_draws_both_pieces_on_their_squares:
        description "Drag KNIGHT b1 onto QUEEN a1: they swap on the board AND on screen"

        $ knight = Robot_Piece('n', color=0)
        $ queen = Robot_Piece('q', color=0)
        $ chess.drop(knight, chess.TO_POS('b1'))
        $ chess.drop(queen, chess.TO_POS('a1'))
        $ renpy.restart_interaction()
        pause 0.3

        drag id "piece_b1" to id "piece_a1"
        pause 0.5

        assert eval (chess.board[chess.TO_POS('a1')] is knight and chess.board[chess.TO_POS('b1')] is queen) timeout 1.0
        assert eval (drag_xy(knight) == square_xy('a1')) timeout 1.0
        assert eval (drag_xy(queen) == square_xy('b1')) timeout 1.0

    testcase click_swap_draws_both_pieces_on_their_squares:
        description "Click KNIGHT b1 then QUEEN a1: same result as the drag"

        $ knight = Robot_Piece('n', color=0)
        $ queen = Robot_Piece('q', color=0)
        $ chess.drop(knight, chess.TO_POS('b1'))
        $ chess.drop(queen, chess.TO_POS('a1'))
        $ renpy.restart_interaction()
        pause 0.3

        click id "piece_b1"
        pause 0.3
        click until id "move_a1"
        click id "move_a1" # the move square is drawn over the QUEEN
        pause 0.5

        assert eval (chess.board[chess.TO_POS('a1')] is knight and chess.board[chess.TO_POS('b1')] is queen) timeout 1.0
        assert eval (drag_xy(knight) == square_xy('a1')) timeout 1.0
        assert eval (drag_xy(queen) == square_xy('b1')) timeout 1.0
