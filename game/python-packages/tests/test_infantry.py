"""
Infantry tests run against the pure Engine (Simple_Piece), not Chess_control.

Key difference from Chess_control:
- Simple_Piece.pilot is a plain list of IDs (or None slots), not a property.
- engine.get('r') finds WHITE pieces with uppercase, black with lowercase.
  Easier: just save the return value of drop().
- enter_ally capacity check (None in pilot) is only enforced for RESCUE
  in the base engine (via has_pilot_room). enter_ally itself always fires
  for same-color; the capacity gate lives in Chess_control.can_infant_on.
"""

import pytest
import fairylion.CONSTANT as c
from fairylion import Engine


@pytest.fixture
def e():
    eng = Engine()
    eng.set_fen("8/8/8/8/8/8/8/8 w - - 0 1")
    return eng


# ─── BASICS ───────────────────────────────────────────────────────────────────

def test_drop_infantry_fen_and_color(e):
    infantry = e.drop('i', 'e4', 0)
    assert infantry.fen == 'i'
    assert infantry.color == 0

def test_infantry_starts_with_empty_pilot_list(e):
    infantry = e.drop('i', 'e4', 0)
    assert infantry.pilot == []

def test_infantry_pilot_list_set_correctly(e):
    infantry = e.drop('i', 'e4', 0)
    infantry.pilot = ['lelouch']
    assert infantry.pilot == ['lelouch']

def test_infantry_in_piecelist(e):
    infantry = e.drop('i', 'e4', 0)
    assert infantry in e.get_pieces(0)

def test_infantry_moves_on_empty_board(e):
    infantry = e.drop('i', 'e4', 0)
    moves = infantry.moves(e)
    # e4 has 4 empty neighbours: d4, f4, e3, e5
    assert len(moves) == 4


# ─── ENTER ALLY ───────────────────────────────────────────────────────────────

def test_enter_ally_generates_move(e):
    rook = e.drop('r', 'e4', 0)
    infantry = e.drop('i', 'e5', 0)
    moves = infantry.moves(e)
    assert any('enter_ally' in m.flag for m in moves)

def test_enter_ally_transfers_pilot_id(e):
    rook = e.drop('r', 'e4', 0)
    infantry = e.drop('i', 'e5', 0)
    infantry.pilot = ['lelouch']
    rook.pilot = [None, None]

    move = next(m for m in infantry.moves(e) if 'enter_ally' in m.flag)
    e.make_move(move, check_legality=False)

    assert 'lelouch' in rook.pilot

def test_enter_ally_infantry_removed_from_board(e):
    rook = e.drop('r', 'e4', 0)
    infantry = e.drop('i', 'e5', 0)

    move = next(m for m in infantry.moves(e) if 'enter_ally' in m.flag)
    e.make_move(move, check_legality=False)

    assert e.board[e.A8_TO_POS('e5')] == c.EMPTY
    assert infantry not in e.get_pieces(0)

def test_enter_ally_undo_restores_infantry(e):
    rook = e.drop('r', 'e4', 0)
    infantry = e.drop('i', 'e5', 0)
    infantry.pilot = ['lelouch']
    rook.pilot = [None, None]

    move = next(m for m in infantry.moves(e) if 'enter_ally' in m.flag)
    e.make_move(move, check_legality=False)
    e.undo()

    assert e.board[e.A8_TO_POS('e5')] is infantry
    assert infantry in e.get_pieces(0)

def test_enter_ally_undo_removes_pilot_from_rook(e):
    rook = e.drop('r', 'e4', 0)
    infantry = e.drop('i', 'e5', 0)
    infantry.pilot = ['lelouch']
    rook.pilot = [None, None]

    move = next(m for m in infantry.moves(e) if 'enter_ally' in m.flag)
    e.make_move(move, check_legality=False)
    e.undo()

    assert 'lelouch' not in rook.pilot


# ─── ENTER EMPTY (neutral piece, color=2) ─────────────────────────────────────

def test_enter_empty_generates_move(e):
    neutral = e.drop('r', 'e4', 2)
    infantry = e.drop('i', 'e5', 0)
    moves = infantry.moves(e)
    assert any('enter_empty' in m.flag for m in moves)

def test_enter_empty_transfers_pilot_id(e):
    neutral = e.drop('r', 'e4', 2)
    infantry = e.drop('i', 'e5', 0)
    infantry.pilot = ['lelouch']

    move = next(m for m in infantry.moves(e) if 'enter_empty' in m.flag)
    e.make_move(move, check_legality=False)

    piece_at_e4 = e.board[e.A8_TO_POS('e4')]
    assert 'lelouch' in piece_at_e4.pilot

def test_enter_empty_undo_clears_pilot(e):
    neutral = e.drop('r', 'e4', 2)
    infantry = e.drop('i', 'e5', 0)
    infantry.pilot = ['lelouch']

    move = next(m for m in infantry.moves(e) if 'enter_empty' in m.flag)
    e.make_move(move, check_legality=False)
    e.undo()

    piece_at_e4 = e.board[e.A8_TO_POS('e4')]
    assert piece_at_e4.pilot == []


# ─── RESCUE (rook moves onto infantry square) ─────────────────────────────────

def test_rescue_generates_move(e):
    rook = e.drop('r', 'e4', 0)
    infantry = e.drop('i', 'e5', 0)
    rook.pilot = [None, None]   # rook must have a free slot
    moves = rook.moves(e)
    assert any('rescue' in m.flag for m in moves)

def test_rescue_transfers_pilot_to_rook(e):
    rook = e.drop('r', 'e4', 0)
    infantry = e.drop('i', 'e5', 0)
    rook.pilot = [None, None]
    infantry.pilot = ['lelouch']

    move = next(m for m in rook.moves(e) if 'rescue' in m.flag)
    e.make_move(move, check_legality=False)

    assert 'lelouch' in rook.pilot

def test_rescue_removes_infantry(e):
    rook = e.drop('r', 'e4', 0)
    infantry = e.drop('i', 'e5', 0)
    rook.pilot = [None, None]
    infantry.pilot = ['lelouch']

    move = next(m for m in rook.moves(e) if 'rescue' in m.flag)
    e.make_move(move, check_legality=False)

    assert infantry not in e.get_pieces(0)

def test_rescue_undo_restores_infantry(e):
    rook = e.drop('r', 'e4', 0)
    infantry = e.drop('i', 'e5', 0)
    rook.pilot = [None, None]
    infantry.pilot = ['lelouch']

    move = next(m for m in rook.moves(e) if 'rescue' in m.flag)
    e.make_move(move, check_legality=False)
    e.undo()

    assert infantry in e.get_pieces(0)
    assert 'lelouch' not in rook.pilot

def test_rescue_requires_empty_slot(e):
    # rook has no free pilot slots — rescue should not be generated
    rook = e.drop('r', 'e4', 0)
    infantry = e.drop('i', 'e5', 0)
    rook.pilot = ['lelouch', 'kallen']  # full

    moves = rook.moves(e)
    assert not any('rescue' in m.flag for m in moves)
