# Tests for the roguelike preparation screen
#
# Board layout used (6×5):
#
#   ┌────────────────────┐
#   │  . . . K . .   ← rank 5 (enemy)
#   │  . . . . . .   ← rank 4
#   │  . . . . . .   ← rank 3
#   │  . . . . . .   ← rank 2 (pawn rank — white)
#   │  Q Q . . . .   ← rank 1 (innermost — white)
#   └────────────────────┘
#     a b c d e f
#
#   a1 = white queen, NO pilot  (queen_a)
#   b1 = white queen WITH GenericPilot inside  (queen_b / gp)
#   d5 = enemy king
#
#   TEAM = [penny, gp]
#
# Penny has can_drive = {'*': 'q'}  (drive_q skill → queen-type only).
# She CANNOT drive '^' (pawn type), so pawn-rank squares must stay None.
#
# Key behaviours under test:
#   1. Penny's moves on pawn rank (y=1) are all None.
#   2. Penny's moves on innermost rank (y=0) include queen squares.
#   3. Clicking a deployed queen twice undeployies it (penny.deployed → False).
#   4. Two deployed pieces can be swapped by f_prep_click_sq_swap.
#   5. Dropping penny on an empty queen works: queen.pilot == penny.
#   6. Dropping penny on an occupied queen ejects the old pilot.

testsuite roguelite:
    setup:
        $ done_flag["oncePerRun"].add('tuto_basic')
        $ done_flag["oncePerRun"].add('tuto_preparation')
        $ g.money = 10
        $ g.items['undo'] = 3
        $ rogue = Roguelike()

    # Run before every testcase in this suite: rebuild a fresh board,
    # reset penny, and jump into l_preparation. Keeps testcases free of
    # duplicated scaffolding and isolates state between tests.
    before testcase:
        $ chess = Chess_control((6, 5))
        $ reset_pilot('penny')  # re-applies drive_q → penny.can_drive = {'*': 'q'}
        $ gp = GenericPilot()
        $ TEAM = [penny, gp]
        $ ROBOTS = []
        # enemy king at d5
        $ chess.drop(Robot_Piece('k', color=1), chess.TO_POS('d5'))
        # white queen at a1 (empty)
        $ queen_a = Robot_Piece('q', color=0)
        $ chess.drop(queen_a, chess.TO_POS('a1'))
        # white queen at b1 with gp inside
        $ queen_b = Robot_Piece('q', color=0)
        $ chess.drop(queen_b, chess.TO_POS('b1'))
        $ queen_b.pilot = gp
        $ gp.deployed = True
        $ queen_b.check_for_pilot()
        $ queen_b.setup_piece()
        $ game = Game('l_map_rogue')
        run Jump('l_preparation')
        pause until screen 's_battlefield'

    testcase penny_cannot_drop_pawn_rank:
        description "Penny (drive_q only) has no valid moves on the pawn rank"

        # Select penny by clicking her portrait in the reserve
        click until id "penny"
        click id "penny"

        # All six pawn-rank squares must be None (penny has no drive_^)
        assert eval (chess.ui['moves'].get(chess.TO_POS('a2')) is None) timeout 1.0
        assert eval (chess.ui['moves'].get(chess.TO_POS('b2')) is None) timeout 1.0
        assert eval (chess.ui['moves'].get(chess.TO_POS('c2')) is None) timeout 1.0
        assert eval (chess.ui['moves'].get(chess.TO_POS('d2')) is None) timeout 1.0
        assert eval (chess.ui['moves'].get(chess.TO_POS('e2')) is None) timeout 1.0
        assert eval (chess.ui['moves'].get(chess.TO_POS('f2')) is None) timeout 1.0

        $ f_dismiss()

    testcase penny_can_drop_innermost_rank:
        description "Penny can target queen squares on rank 1 (innermost)"

        # Select penny by clicking her portrait in the reserve
        click until id "penny"
        click id "penny"

        # a1 (empty queen) and b1 (queen with gp) are both valid targets
        assert eval (chess.ui['moves'].get(chess.TO_POS('a1')) is not None) timeout 10.0
        assert eval (chess.ui['moves'].get(chess.TO_POS('b1')) is not None) timeout 1.0

        # Empty squares on rank 1 (c1-f1) must not be None — penny can be dropped as infantry
        assert eval (chess.ui['moves'].get(chess.TO_POS('c1'))) timeout 1.0

        $ f_dismiss()


    testcase undeploy_penny_by_clicking:
        description "Clicking a deployed piece twice undeployies it (penny.deployed → False)"

        # Deploy penny into queen_a by click-click:
        #   1. click penny in reserve — selects her, populates chess.ui['moves']
        #   2. click the target queen — f_chessboard_clicked routes through
        #      f_click_on_move_sq → f_prep_drop_piece
        click until id "penny"
        click id "penny"
        click until id "piece_a1"
        click id "piece_a1"

        assert eval (penny.deployed) timeout 1.0
        assert eval (penny in queen_a._pilot) timeout 1.0
        assert eval (chess.ui['selected'] == queen_a) timeout 1.0
        # Now undeploy: click the deployed piece, then click the move indicator
        # that sits on the same square. When selected is deployed, the viewport's
        # move indicator (id "move_a1") is shown and f_click_on_move_sq detects
        # the reclick and calls f_unprepare.
        click until id "move_a1"
        click id "move_a1"

        assert eval (not penny.deployed) timeout 1.0
        assert eval (not queen_a.deployed) timeout 1.0


    testcase swap_two_deployed_pieces:
        description "f_prep_click_sq_swap swaps two pieces on the board"

        $ pos_a1 = chess.TO_POS('a1')
        $ pos_b1 = chess.TO_POS('b1')

        # Verify starting positions
        assert eval (chess.board[pos_a1] == queen_a) timeout 1.0
        assert eval (chess.board[pos_b1] == queen_b) timeout 1.0

        # Drag queen_a onto queen_b triggers a swap in f_chessboard_dragged.
        # We call the swap function directly (drag targets have no widget id).
        $ f_prep_click_sq_swap(pos_a1, pos_b1)
        $ renpy.restart_interaction()

        # After swap, pieces must have exchanged board positions
        assert eval (chess.board[pos_b1] == queen_a) timeout 1.0
        assert eval (chess.board[pos_a1] == queen_b) timeout 1.0
        # Piece objects carry their updated .pos
        assert eval (queen_a.pos == pos_b1) timeout 1.0
        assert eval (queen_b.pos == pos_a1) timeout 1.0


    testcase drop_penny_on_empty_queen:
        description "Dropping penny on a pilotless queen installs her inside"

        # Preconditions
        assert eval (queen_a.pilot is None) timeout 1.0
        assert eval (not penny.deployed) timeout 1.0

        # Deploy penny onto the empty queen by click-click:
        #   1. click penny — selects her, populates moves with queen squares
        #   2. click piece_a1 — target is a valid move, routes through
        #      f_click_on_move_sq → f_prep_drop_piece
        click until id "penny"
        click id "penny"
        click until id "piece_a1"
        click id "piece_a1"

        assert eval (penny.deployed) timeout 1.0
        assert eval (queen_a.pilot == penny) timeout 1.0


    testcase drop_penny_on_occupied_queen:
        description "Dropping penny on an occupied queen ejects the old pilot"

        # Preconditions: gp is inside queen_b, penny is in reserve
        assert eval (queen_b.pilot == gp) timeout 1.0
        assert eval (gp.deployed) timeout 1.0
        assert eval (not penny.deployed) timeout 1.0

        # Drop penny onto the occupied queen by click-click:
        #   1. click penny — selects her from reserve
        #   2. click piece_b1 — f_prep_drop_piece ejects gp and installs penny
        click until id "penny"
        click id "penny"
        click until id "piece_b1"
        click id "piece_b1"

        assert eval (penny.deployed) timeout 1.0
        assert eval (queen_b.pilot == penny) timeout 1.0
        # gp was ejected from the queen, so deployed must be False
        assert eval (not gp.deployed) timeout 1.0
