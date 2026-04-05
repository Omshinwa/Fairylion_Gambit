# this match tests needs to have two different search algorithm in the same class.

import fairylion

engine = fairylion.Engine()
engine.set_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

# PLAYING THE GAME
while engine.gen_legal_moves():
    best_move = engine.think(time_limit=4.0)
    engine.make_move(best_move)
    print(engine)
    if not engine.gen_legal_moves():
        break
    best_move = engine.think_minimax()
    engine.make_move(best_move)
    print(engine)
print(engine.to_pgn())
print('game over')