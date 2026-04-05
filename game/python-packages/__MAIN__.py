from fairylion import *
from fairylion.mcts_debug import save_mcts_tree_json # so while debugging you can enter save_mcts_tree(root)

# engine.set_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") # starting pos

engine.set_fen("r3k2r/pp1b1ppp/8/2bQ4/8/8/PPP1PqPP/R2K1B1R b kq - 1 11")
print(engine.gen_legal_moves())
# best_move = engine.think(time_limit=5)
# save_mcts_tree_json(engine, 21698)