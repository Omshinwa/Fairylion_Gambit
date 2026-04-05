
import pytest
import timeit
from fairylion import Engine


@pytest.fixture
def engine():
    return Engine()

# ─── TEST 1: AI finds best move in simple position ───────────────────────────
# Expected: a rook move (b2c2, b2b8, or e2e8) within 5 seconds

def test_ai_finds_rook_move(engine):
    engine.set_fen('1r2r1/2k3/6/6/6/6/PR1KRP/3N2 w KQkq - 0 1')
    engine.promotions = [['q'], ['q']]
    move = engine.think_minimax(time_limit=5.0)
    assert move is not None
    assert move.piece.fen == 'r', f"Expected rook move, got {move.piece.fen}"

# --- TEST: basic search, didnt work before
def test_finds_knight_move(engine):
    engine.set_fen('r1bqkbnr/pppp1ppp/2n5/3N4/4p3/5N2/PPPPPPPP/R1BQKB1R w KQkq - 0 1')
    move = engine.monte_carlo_search(iterations=2000)
    assert move.piece.fen == 'n', "Not a knight move, which should be the best move (its gonna be taken)."