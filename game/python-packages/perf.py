# time move var passed: perftest(5): 28.259246792062186

import timeit
from fairylion import *

# ##
# ## test generation move speed
# ##
engine = Engine()
engine.set_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
time_eval = timeit.timeit("engine.perftest(5)", globals=globals(), number=1)
print(f"time move var passed: {time_eval}")
# PERFT 5 (base position) = 4865609

##
## test evaluation speed on a specific position
##
# engine = Engine()
# engine.set_fen("rnbqkbnr/2pp3p/1p2ppp1/6N1/p1BPP1Q1/8/PPP2PPP/RNB1K2R w KQkq - 0 1")
# time_eval = timeit.timeit("engine.think(1000)", globals=globals(), number=1)
# print(f"time move var passed: {time_eval}")

##
## test generation move speed with profiling
##
# import cProfile

# engine.set_fen('1r2r1/2k3/6/6/6/6/PR1KRP/2N3 w KQkq - 0 1')
# cProfile.run('engine.think(300, makemove=True)', 'profile_output.prof')

# import pstats
# import os
# # Load the profile data
# p = pstats.Stats('profile_output.prof')
# # Strip the common path from the output
# p.strip_dirs()
# # Sort by total time and output to a file
# with open('profile_report.txt', 'w') as f:
#     p.sort_stats('tottime').print_stats()
#     p.stream = f
#     p.print_stats()

# os.remove('profile_output.prof')