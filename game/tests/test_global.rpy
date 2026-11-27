
testsuite global:
    teardown:
        exit

# where a piece is drawn on the board, to check drag and drop (test_story_preparation.rpy, test_map_1_0.rpy)
init python:
    def drag_xy(piece):
        """Where the board drag of this piece is drawn (tests)."""
        drag = get_drags('battle', child=piece)
        return (int(drag.x), int(drag.y))

    def square_xy(a8):
        """Where a piece on this square should be drawn (tests)."""
        return tuple(int(v) for v in chess.POS_TO_SXY(chess.TO_POS(a8)))
