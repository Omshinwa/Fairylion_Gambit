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


# ─── TEST 2: Move generation speed (perft depth 4) ───────────────────────────

def test_perft_speed(engine):
    engine.set_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    t = timeit.timeit(lambda: engine.perftest(4), number=1)
    assert t <= 3, f"Perft too slow: {t:.1f}s"


# ─── TEST 3: Perft node count with promotions ────────────────────────────────

def test_perft_promotions(engine):
    engine.set_fen("8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1")
    engine.promotions = [['q', 'r', 'b', 'n'], ['q', 'r', 'b', 'n']]
    engine.perftest(5)
    assert engine.positionCount == 674624, f"Wrong node count: {engine.positionCount}"


# ─── TEST 4: No castling while in check ──────────────────────────────────────

def test_no_castling_while_in_check(engine):
    engine.set_fen("r3k2r/pp1b1ppp/8/2bQ4/8/8/PPP1PqPP/R3KB1R w KQkq - 0 11")
    legals = engine.gen_legal_moves()
    assert len(legals) <= 2, f"Should have ≤2 legal moves (no castling in check), got {len(legals)}"


# ─── TEST 5: Castling available when not in check ────────────────────────────

def test_castling_available(engine):
    engine.set_fen("r3k2r/pp1b1ppp/8/2bQ4/8/8/PPP1PqPP/R2K1B1R b kq - 1 11")
    king = engine.get('k')
    moves = king.moves()
    assert len(moves) == 5, f"Expected 5 king moves, got {len(moves)}: {moves}"
