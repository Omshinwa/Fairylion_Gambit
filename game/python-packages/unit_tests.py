#
#   This is a list of flags to run after doing some changes in the code:
#

COLOR_GREEN = "\033[1;32;42m"
COLOR_RESET = "\033[0m"

# print(COLOR_GREEN + "TEST OK" + COLOR_RESET)

import timeit
from fairylion import *
from fairylion.mcts_debug import save_mcts_tree_json

# # # 3/8/2025 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # TEST 1: test a fairly simple position
# # # EXPECTED: This should be ran in 3 seconds at most, and find a rook move
# # # b2c2 or b2b8 or e2e8
# # # This bugged when i commented out the last else: in make_move
# import timeit
# engine.set_fen('1r2r1/2k3/6/6/6/6/PR1KRP/3N2 w KQkq - 0 1')
# engine.promotions = [['q'],['q']]
# time_eval = timeit.timeit("globals()['move'] = engine.think(10000)", globals=globals(), number=1)
# if time_eval > 5:
#     raise Exception(f"Too slow: {time_eval} seconds")
# if move.piece.fen != 'r':
#     raise Exception("Not a rook that moved, which should be the best move.")
# print(COLOR_GREEN + "TEST OK" + COLOR_RESET)
# # # # # ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # 1/9/2025
# # # TEST 2: perft test speed, move generation speed
# # # time move var passed: perftest(5): 28.259246792062186
# # # time move var passed: perftest(4): 1.1651818749960512
# import timeit
# from fairylion import *
# engine = Engine()
# engine.set_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
# time_eval = timeit.timeit("engine.perftest(4)", globals=globals(), number=1)
# print(f"time move var passed: {time_eval}")
# if time_eval > 3:
#     raise Exception("might be kinda slow. did you change anything drastically?")
# print(COLOR_GREEN + "TEST OK" + COLOR_RESET)
# # # # # ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# # # # # ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # 1/9/2025
# # # TEST 3: perft test. Testing PROMOTIONS
# engine.set_fen("8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1 ")
# engine.promotions = [['q,r,b,n'],['q,r,b,n']]
# # engine.perftest(5)
# time_eval = timeit.timeit("engine.perftest(5)", globals=globals(), number=1)
# # if engine.positionCount != 43238: # for depth 4
# #     raise Exception("something wrong with promotions?")
# if engine.positionCount != 674624: # for depth 5
#     raise Exception("something wrong with promotions?")
# print(COLOR_GREEN + "TEST OK" + COLOR_RESET)
# # # # # ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # 10/10/2025
# # TEST 4: basic search, didnt work before
# engine.set_fen('r1bqkbnr/pppp1ppp/2n5/3N4/4p3/5N2/PPPPPPPP/R1BQKB1R w KQkq - 0 1')
# move = engine.monte_carlo_search(iterations=2000)
# if move.piece.fen != 'n':
#     raise Exception("Not a knight move, which should be the best move (its gonna be taken).")
# print(COLOR_GREEN + "TEST OK" + COLOR_RESET)
# # # # # ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # TEST 5: Should not be able to castle while in check
# engine.set_fen("r3k2r/pp1b1ppp/8/2bQ4/8/8/PPP1PqPP/R3KB1R w KQkq - 0 11")
# if len(engine.gen_legal_moves())>2:
#     print(engine.gen_legal_moves())
#     raise Exception("Castling while in check")
# print(COLOR_GREEN + "TEST OK" + COLOR_RESET)
# # # # # ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# TEST 6: should be able to castle here
engine.set_fen("r3k2r/pp1b1ppp/8/2bQ4/8/8/PPP1PqPP/R2K1B1R b kq - 1 11")
if len(get('k').moves()) != 5:
    print(get('k').moves())
    raise Exception("should be able to castle here both ways, theres 5 moves")
print(COLOR_GREEN + "TEST OK" + COLOR_RESET)
# # # # ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    