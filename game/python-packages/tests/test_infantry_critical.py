"""
Tests for CRITICAL-list rules on rescue / enter_ally / enter_empty moves,
plus a shallow MCTS fork test.

CRITICAL[color] is the list of "must-protect" pieces for that side.
Kings are added automatically; infantry must be added manually in these tests.

Two bugs were fixed in engine_.py alongside this file:
  1. undo() rescue branch: list.add()  →  list.append()
  2. undo_enter_ally(): CRITICAL.remove(piece) when critical_add=True
                        → should remove(target), not remove(piece)
"""

import pytest
import fairylion.CONSTANT as c
from fairylion import Engine


@pytest.fixture
def e():
    eng = Engine()
    eng.set_fen("8/8/8/8/8/8/8/8 w - - 0 1")
    return eng


# ─── RESCUE + CRITICAL ────────────────────────────────────────────────────────

class TestRescueCritical:

    def test_rescue_generates_move_for_critical_infantry(self, e):
        """Rook with a free pilot slot generates a rescue move onto a CRITICAL infantry."""
        rook = e.drop('r', 'e4', 0)
        infantry = e.drop('i', 'e5', 0)
        rook._pilot = [None, None]
        e.CRITICAL[0].append(infantry)

        moves = rook.moves(e)
        assert any('rescue' in m.flag for m in moves)

    def test_rescue_no_move_when_pilot_full_and_infantry_critical(self, e):
        """A full pilot list blocks rescue even when the target infantry is CRITICAL."""
        rook = e.drop('r', 'e4', 0)
        infantry = e.drop('i', 'e5', 0)
        rook._pilot = ['lelouch', 'kallen']   # full — no free slot
        e.CRITICAL[0].append(infantry)

        moves = rook.moves(e)
        assert not any('rescue' in m.flag for m in moves)

    def test_rescue_removes_infantry_from_critical(self, e):
        """After rescue the infantry is no longer in CRITICAL[0]."""
        rook = e.drop('r', 'e4', 0)
        infantry = e.drop('i', 'e5', 0)
        rook._pilot = [None, None]
        e.CRITICAL[0].append(infantry)

        move = next(m for m in rook.moves(e) if 'rescue' in m.flag)
        e.make_move(move, check_legality=False)

        assert infantry not in e.CRITICAL[0]

    def test_rescue_adds_rescuer_to_critical(self, e):
        """After rescue the rook that performed it is added to CRITICAL[0]."""
        rook = e.drop('r', 'e4', 0)
        infantry = e.drop('i', 'e5', 0)
        rook._pilot = [None, None]
        e.CRITICAL[0].append(infantry)

        move = next(m for m in rook.moves(e) if 'rescue' in m.flag)
        e.make_move(move, check_legality=False)

        assert rook in e.CRITICAL[0]

    def test_rescue_history_critical_flags(self, e):
        """HistoryNode has critical_remove=True and critical_add=True after rescue of CRITICAL infantry."""
        rook = e.drop('r', 'e4', 0)
        infantry = e.drop('i', 'e5', 0)
        rook._pilot = [None, None]
        e.CRITICAL[0].append(infantry)

        move = next(m for m in rook.moves(e) if 'rescue' in m.flag)
        e.make_move(move, check_legality=False)

        last = e.history[-1]
        assert last.critical_remove is True
        assert last.critical_add is True

    def test_rescue_undo_restores_critical(self, e):
        """Undo after rescue restores infantry to CRITICAL and removes the rook."""
        rook = e.drop('r', 'e4', 0)
        infantry = e.drop('i', 'e5', 0)
        rook._pilot = [None, None]
        e.CRITICAL[0].append(infantry)

        move = next(m for m in rook.moves(e) if 'rescue' in m.flag)
        e.make_move(move, check_legality=False)
        e.undo()

        assert infantry in e.CRITICAL[0]
        assert rook not in e.CRITICAL[0]

    def test_rescue_critical_add_false_when_rescuer_already_critical(self, e):
        """
        Both infantry and rook in CRITICAL: rescue removes infantry but does NOT
        re-add the rook (it is already there), so critical_add is False.
        """
        rook = e.drop('r', 'e4', 0)
        infantry = e.drop('i', 'e5', 0)
        rook._pilot = [None, None]
        e.CRITICAL[0].append(infantry)
        e.CRITICAL[0].append(rook)

        move = next(m for m in rook.moves(e) if 'rescue' in m.flag)
        e.make_move(move, check_legality=False)

        last = e.history[-1]
        assert last.critical_remove is True
        assert last.critical_add is False   # rook was already critical

    def test_rescue_both_critical_undo_restores(self, e):
        """Undo when both pieces are CRITICAL restores both to their original places."""
        rook = e.drop('r', 'e4', 0)
        infantry = e.drop('i', 'e5', 0)
        rook._pilot = [None, None]
        e.CRITICAL[0].append(infantry)
        e.CRITICAL[0].append(rook)

        move = next(m for m in rook.moves(e) if 'rescue' in m.flag)
        e.make_move(move, check_legality=False)
        e.undo()

        assert infantry in e.CRITICAL[0]
        assert rook in e.CRITICAL[0]

    def test_rescue_no_critical_update_when_infantry_not_critical(self, e):
        """Rescue of a non-CRITICAL infantry leaves CRITICAL completely unchanged."""
        rook = e.drop('r', 'e4', 0)
        infantry = e.drop('i', 'e5', 0)
        rook._pilot = [None, None]
        critical_before = list(e.CRITICAL[0])

        move = next(m for m in rook.moves(e) if 'rescue' in m.flag)
        e.make_move(move, check_legality=False)

        assert e.CRITICAL[0] == critical_before
        last = e.history[-1]
        assert last.critical_remove is False
        assert last.critical_add is False

    def test_rescue_not_critical_undo_critical_unchanged(self, e):
        """Undo of rescue on a non-CRITICAL infantry also leaves CRITICAL unchanged."""
        rook = e.drop('r', 'e4', 0)
        infantry = e.drop('i', 'e5', 0)
        rook._pilot = [None, None]
        critical_before = list(e.CRITICAL[0])

        move = next(m for m in rook.moves(e) if 'rescue' in m.flag)
        e.make_move(move, check_legality=False)
        e.undo()

        assert e.CRITICAL[0] == critical_before


# ─── ENTER_ALLY + CRITICAL ────────────────────────────────────────────────────

class TestEnterAllyCritical:

    def test_enter_ally_no_move_when_target_pilot_full(self, e):
        """Infantry cannot enter a rook whose pilot list has no free slot."""
        rook = e.drop('r', 'e4', 0)
        rook._pilot = ['lelouch', 'kallen']   # full
        infantry = e.drop('i', 'e5', 0)

        moves = infantry.moves(e)
        assert not any('enter_ally' in m.flag for m in moves)

    def test_enter_ally_critical_infantry_updates_critical(self, e):
        """CRITICAL infantry entering a non-CRITICAL rook: infantry removed, rook added."""
        rook = e.drop('r', 'e4', 0)
        rook._pilot = [None, None]
        infantry = e.drop('i', 'e5', 0)
        e.CRITICAL[0].append(infantry)

        move = next(m for m in infantry.moves(e) if 'enter_ally' in m.flag)
        e.make_move(move, check_legality=False)

        assert infantry not in e.CRITICAL[0]
        assert rook in e.CRITICAL[0]

    def test_enter_ally_history_critical_flags(self, e):
        """HistoryNode records critical_remove=True and critical_add=True."""
        rook = e.drop('r', 'e4', 0)
        rook._pilot = [None, None]
        infantry = e.drop('i', 'e5', 0)
        e.CRITICAL[0].append(infantry)

        move = next(m for m in infantry.moves(e) if 'enter_ally' in m.flag)
        e.make_move(move, check_legality=False)

        last = e.history[-1]
        assert last.critical_remove is True
        assert last.critical_add is True

    def test_enter_ally_critical_infantry_undo_restores_critical(self, e):
        """Undo after CRITICAL infantry enters rook restores CRITICAL to original state."""
        rook = e.drop('r', 'e4', 0)
        rook._pilot = [None, None]
        infantry = e.drop('i', 'e5', 0)
        e.CRITICAL[0].append(infantry)

        move = next(m for m in infantry.moves(e) if 'enter_ally' in m.flag)
        e.make_move(move, check_legality=False)
        e.undo()

        assert infantry in e.CRITICAL[0]
        assert rook not in e.CRITICAL[0]

    def test_enter_ally_critical_add_false_when_target_already_critical(self, e):
        """
        CRITICAL infantry enters a CRITICAL rook: infantry removed but rook not
        re-added (already there), so critical_add is False.
        """
        rook = e.drop('r', 'e4', 0)
        rook._pilot = [None, None]
        infantry = e.drop('i', 'e5', 0)
        e.CRITICAL[0].append(infantry)
        e.CRITICAL[0].append(rook)

        move = next(m for m in infantry.moves(e) if 'enter_ally' in m.flag)
        e.make_move(move, check_legality=False)

        last = e.history[-1]
        assert last.critical_remove is True
        assert last.critical_add is False
        assert infantry not in e.CRITICAL[0]
        assert rook in e.CRITICAL[0]

    def test_enter_ally_both_critical_undo_restores(self, e):
        """
        Undo when both are CRITICAL restores both (critical_add=False here, so
        only the infantry re-append path runs — no bug-prone remove(target)).
        """
        rook = e.drop('r', 'e4', 0)
        rook._pilot = [None, None]
        infantry = e.drop('i', 'e5', 0)
        e.CRITICAL[0].append(infantry)
        e.CRITICAL[0].append(rook)

        move = next(m for m in infantry.moves(e) if 'enter_ally' in m.flag)
        e.make_move(move, check_legality=False)
        e.undo()

        assert infantry in e.CRITICAL[0]
        assert rook in e.CRITICAL[0]

    def test_enter_ally_no_critical_change_when_infantry_not_critical(self, e):
        """Non-CRITICAL infantry entering a rook does not touch CRITICAL at all."""
        rook = e.drop('r', 'e4', 0)
        rook._pilot = [None, None]
        infantry = e.drop('i', 'e5', 0)
        critical_before = list(e.CRITICAL[0])

        move = next(m for m in infantry.moves(e) if 'enter_ally' in m.flag)
        e.make_move(move, check_legality=False)

        assert e.CRITICAL[0] == critical_before
        last = e.history[-1]
        assert last.critical_remove is False
        assert last.critical_add is False

    def test_enter_ally_not_critical_undo_critical_unchanged(self, e):
        """Undo of enter_ally by non-CRITICAL infantry leaves CRITICAL unchanged."""
        rook = e.drop('r', 'e4', 0)
        rook._pilot = [None, None]
        infantry = e.drop('i', 'e5', 0)
        critical_before = list(e.CRITICAL[0])

        move = next(m for m in infantry.moves(e) if 'enter_ally' in m.flag)
        e.make_move(move, check_legality=False)
        e.undo()

        assert e.CRITICAL[0] == critical_before

    def test_enter_ally_not_critical_into_critical_no_change(self, e):
        """Non-CRITICAL infantry entering a CRITICAL rook: CRITICAL list unchanged."""
        rook = e.drop('r', 'e4', 0)
        rook._pilot = [None, None]
        infantry = e.drop('i', 'e5', 0)
        e.CRITICAL[0].append(rook)         # rook is critical, infantry is not
        critical_before = list(e.CRITICAL[0])

        move = next(m for m in infantry.moves(e) if 'enter_ally' in m.flag)
        e.make_move(move, check_legality=False)

        assert e.CRITICAL[0] == critical_before
        last = e.history[-1]
        assert last.critical_remove is False
        assert last.critical_add is False

    def test_enter_ally_not_critical_into_critical_undo_no_change(self, e):
        """Undo of enter_ally (non-CRITICAL into CRITICAL rook) leaves CRITICAL unchanged."""
        rook = e.drop('r', 'e4', 0)
        rook._pilot = [None, None]
        infantry = e.drop('i', 'e5', 0)
        e.CRITICAL[0].append(rook)
        critical_before = list(e.CRITICAL[0])

        move = next(m for m in infantry.moves(e) if 'enter_ally' in m.flag)
        e.make_move(move, check_legality=False)
        e.undo()

        assert e.CRITICAL[0] == critical_before


# ─── ENTER_EMPTY + CRITICAL ───────────────────────────────────────────────────

class TestEnterEmptyCritical:

    def test_enter_empty_no_move_when_neutral_pilot_full(self, e):
        """Infantry cannot enter a neutral piece whose pilot slot is already taken."""
        neutral = e.drop('r', 'e4', 2)
        neutral._pilot = ['lelouch']   # single slot, already occupied
        infantry = e.drop('i', 'e5', 0)

        moves = infantry.moves(e)
        assert not any('enter_empty' in m.flag for m in moves)

    def test_enter_empty_critical_infantry_updates_critical(self, e):
        """CRITICAL infantry entering a neutral piece: infantry removed, neutral added."""
        neutral = e.drop('r', 'e4', 2)
        neutral._pilot = [None]
        infantry = e.drop('i', 'e5', 0)
        e.CRITICAL[0].append(infantry)

        move = next(m for m in infantry.moves(e) if 'enter_empty' in m.flag)
        e.make_move(move, check_legality=False)

        assert infantry not in e.CRITICAL[0]
        assert neutral in e.CRITICAL[0]

    def test_enter_empty_history_critical_flags(self, e):
        """HistoryNode has critical_remove=True and critical_add=True."""
        neutral = e.drop('r', 'e4', 2)
        neutral._pilot = [None]
        infantry = e.drop('i', 'e5', 0)
        e.CRITICAL[0].append(infantry)

        move = next(m for m in infantry.moves(e) if 'enter_empty' in m.flag)
        e.make_move(move, check_legality=False)

        last = e.history[-1]
        assert last.critical_remove is True
        assert last.critical_add is True

    def test_enter_empty_critical_infantry_undo_restores_critical(self, e):
        """Undo after CRITICAL infantry enters neutral restores original CRITICAL state."""
        neutral = e.drop('r', 'e4', 2)
        neutral._pilot = [None]
        infantry = e.drop('i', 'e5', 0)
        e.CRITICAL[0].append(infantry)

        move = next(m for m in infantry.moves(e) if 'enter_empty' in m.flag)
        e.make_move(move, check_legality=False)
        e.undo()

        assert infantry in e.CRITICAL[0]
        assert neutral not in e.CRITICAL[0]

    def test_enter_empty_not_critical_no_change(self, e):
        """Non-CRITICAL infantry entering neutral: CRITICAL list untouched."""
        neutral = e.drop('r', 'e4', 2)
        neutral._pilot = [None]
        infantry = e.drop('i', 'e5', 0)
        critical_before = list(e.CRITICAL[0])

        move = next(m for m in infantry.moves(e) if 'enter_empty' in m.flag)
        e.make_move(move, check_legality=False)

        assert e.CRITICAL[0] == critical_before
        last = e.history[-1]
        assert last.critical_remove is False
        assert last.critical_add is False

    def test_enter_empty_not_critical_undo_no_change(self, e):
        """Undo of enter_empty by non-CRITICAL infantry: CRITICAL unchanged."""
        neutral = e.drop('r', 'e4', 2)
        neutral._pilot = [None]
        infantry = e.drop('i', 'e5', 0)
        critical_before = list(e.CRITICAL[0])

        move = next(m for m in infantry.moves(e) if 'enter_empty' in m.flag)
        e.make_move(move, check_legality=False)
        e.undo()

        assert e.CRITICAL[0] == critical_before


# ─── MCTS FORK TEST ───────────────────────────────────────────────────────────

class TestMctsForkCritical:

    def test_mcts_finds_bishop_fork_on_two_critical_pieces(self):
        """
        Position (black to move):
            White King e1  — in CRITICAL[0] (auto)
            White Infantry g3 — manually added to CRITICAL[0]
            Black Bishop c5  — can move to f2 via c5→d4→e3→f2
            Black Rook f8    — defends the entire f-file, making f2 untakeable
            Black King h8    — keeps CRITICAL[1] non-empty

        Bishop c5→f2 simultaneously attacks:
            • King e1  (SW diagonal from f2, one step)
            • Infantry g3 (NE diagonal from f2, one step)

        White king cannot take f2 (rook on f8 defends it).  White must flee
        the check, then Black wins the infantry.

        A shallow MCTS (200 iterations) should select bishop c5→f2 as the
        best move thanks to the 'check' flag priority in expand_initial.
        """
        eng = Engine()
        eng.set_fen("8/8/8/8/8/8/8/8 w - - 0 1")

        # White
        _king_w  = eng.drop('k', 'e1', 0)
        infnt_w  = eng.drop('i', 'g3', 0)
        eng.CRITICAL[0].append(infnt_w)   # infantry is also critical
        eng.CRITICAL[0].append(_king_w)

        # Black
        _bishop_b = eng.drop('b', 'c5', 1)
        _rook_b   = eng.drop('r', 'f8', 1)   # defends f2 so king can't take
        _king_b   = eng.drop('k', 'h8', 1)   # keeps CRITICAL[1] non-empty

        eng.side = 1   # black to move

        best = eng.monte_carlo_search(iterations=200)

        assert best.fr == eng.A8_TO_POS('c5'), (
            f"Expected bishop on c5 to move, got fr={eng.POS_TO_A8(best.fr)}"
        )
        assert best.to == eng.A8_TO_POS('f2'), (
            f"Expected target square f2, got to={eng.POS_TO_A8(best.to)}"
        )
