from fairylion import *
from fairylion.mcts_debug import save_mcts_tree_json # so while debugging you can enter save_mcts_tree(root)

# e = engine


# engine.set_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") # starting pos

# best_move = engine.think(time_limit=5)
# save_mcts_tree_json(engine, 21698)

eng = Engine()
eng.set_fen("8/8/8/8/8/8/8/8 w - - 0 1")

# White
_king_w  = eng.drop('k', 'e1', 0)
infnt_w  = eng.drop('i', 'g3', 0)
eng.CRITICAL[0].append(infnt_w)   # infantry is also critical

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