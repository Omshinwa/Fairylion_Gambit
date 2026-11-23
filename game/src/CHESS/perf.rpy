# # you can remove this file for builds

# 9/9/2024 perf(4) takes 26 seconds
# 16 seconds
# changes set() into _set(): 9.5 - 10s
# if you change all RevertableList into list, 4.2s or 46000 nps
# after converting to python only
# 2.5
# idk what happened but im at 5s now
# 3/2026, 2.8s

# blueford  3742776
# chess.js  2703116
# chess.py  700000 nps in rpy, 747309 in vscode...
# 
# fairylion 40000 nps

# search progress
# time_eval = timeit.timeit("engine_move(4)", globals=globals(), number=1)

# LESSONS 1
#   instruction[0] == 'line'
#       is faster than
#   instruction[0] == "LINE"     ///  "LINE" = 2
#   comparing string is actually very fast, as fast as comparing ints

# LESSON 2, SAME SPEED passing the arg or not
# get_move_of_instruction(self, moves, instruction, offset)
# OR
# moves += get_move_of_instruction(self, instruction, offset)
#

init 50 python:
    import timeit # this is used for setting the optimal strength

    def do_perft(engine, depth = 4):
        engine.set_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        # time_eval = timeit.timeit("engine.copy(chess); engine.perftest(4)", globals=globals(), number=1)
        time_eval = timeit.timeit("engine.perftest(4)", globals=globals(), number=1)
        print(f"time move var passed: {time_eval}")

    def do_mcts(engine, depth = 4000):
        engine.set_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        # time_eval = timeit.timeit("engine.copy(chess); engine.perftest(4)", globals=globals(), number=1)
        time_eval = timeit.timeit("engine.think("+str(depth)+")", globals=globals(), number=1)
        print(f"time move var passed: {time_eval}")

#     # renpy.profile_screen('s_chessboard_bg', update=True, time=True) #time=True, update=True, debug=True, const=True

    # #####
    # ##### basic test of move gen speed, currently around 5s for engine.perftest(4) or 40000 nps
    # ##### engine.perftest(5) takes 122 seconds for 4.8 millions nodes or or 40000 nps
    # #####
    # engine = Engine()
    # engine.set_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    # # time_eval = timeit.timeit("engine.copy(chess); engine.perftest(4)", globals=globals(), number=1)
    # time_eval = timeit.timeit("engine.perftest(4)", globals=globals(), number=1)
    # print(f"time move var passed: {time_eval}")


#     # #
#     # # test AI speed
#     # #
#     # engine = Engine()
#     # engine.set_fen("rnbqkbnr/2pp3p/1p2ppp1/6N1/p1BPP1Q1/8/PPP2PPP/RNB1K2R w KQkq - 0 1")
#     # time_eval = timeit.timeit("engine.think(2000)", globals=globals(), number=1)
#     # print(f"time move var passed: {time_eval}")


# init 50 python:  # DOING SOME PROFILING LOL
#     import profile
#     import pstats

#     ###
#     ### change section below
#     ###
#     chess = Engine()
#     chess.set_fen('1r2r1/2k3/6/6/6/6/PR1KRP/2N3 w KQkq - 0 1')
#     chess.promotions = [['q'],['q']]

#     # Get the writable directory from Ren'Py
#     writable_dir = renpy.config.basedir
#     # Run cProfile and save the profiling data to a binary output file

#     profile.runctx('chess.think(300)', globals(), locals(), writable_dir + '/NameOfBinaryOutputFile.prof')

#     # Open the human-readable output file for writing
#     stream = open(writable_dir + '/NameOfHumanReadableTextOutputFile.txt', 'w')
#     # Load the profiling stats and configure the sorting of the output
#     stats = pstats.Stats(writable_dir + '/NameOfBinaryOutputFile.prof', stream=stream)
#     stats.sort_stats('ncalls', 'tottime')

#     # Print the statistics to the text file
#     stats.print_stats()

#     # Close the stream
#     stream.close()
#     os.remove(writable_dir + '/NameOfBinaryOutputFile.prof') # didnt test yet