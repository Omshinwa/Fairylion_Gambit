"""
Profile the engine + MCTS on several chess positions.

Run from the python-packages directory:
    python -m fairylion.profile_engine
or from this directory:
    python profile_engine.py

Writes results to profile_engine.log next to this file.
"""
import cProfile
import pstats
import io
import os
import time

from fairylion.engine_ import Engine

POSITIONS = {
    "opening (start position)":
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "midgame (Ruy Lopez, ~move 10, lots of pieces, tactical)":
        "r1bq1rk1/2p1bppp/p1np1n2/1p2p3/4P3/1BP2N1P/PP1P1PP1/RNBQR1K1 w - - 0 8",
    "midgame (Sicilian, complex, many sliders active)":
        "r2qk2r/pp1n1ppp/2p1pn2/3p4/3P1B2/2NBPN2/PPPQ1PPP/2KR3R w kq - 0 9",
    "endgame (K+R+P vs K+R, sparse, long rays)":
        "8/5pk1/6p1/7p/8/1R6/5PKP/3r4 w - - 0 1",
    "endgame (K+Q vs K+R, very sparse)":
        "8/8/4k3/8/8/3K4/3Q4/4r3 w - - 0 1",
}

MCTS_ITERATIONS = 1500
MOVEGEN_REPS    = 1500
CHECK_REPS      = 15000

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profile_engine.log")


def build_engine(fen):
    engine = Engine(size=(8, 8), level=2)
    engine.set_fen(fen)
    return engine


def run_workload(label, fn, top, out):
    pr = cProfile.Profile()
    t0 = time.time()
    pr.enable()
    fn()
    pr.disable()
    elapsed = time.time() - t0

    out.write(f"\n{'='*72}\n  {label}  -- wall time: {elapsed:.3f}s\n{'='*72}\n")

    buf = io.StringIO()
    pstats.Stats(pr, stream=buf).sort_stats('tottime').print_stats(top)
    out.write("---- by tottime (self time) ----\n")
    out.write(buf.getvalue())

    buf = io.StringIO()
    pstats.Stats(pr, stream=buf).sort_stats('cumulative').print_stats(top)
    out.write("---- by cumulative ----\n")
    out.write(buf.getvalue())

    return elapsed


def profile_position(name, fen, out):
    out.write(f"\n\n{'#'*72}\n# POSITION: {name}\n# FEN: {fen}\n{'#'*72}\n")
    print(f"  {name} ...", end="", flush=True)

    summary = []

    engine = build_engine(fen)
    n_moves = len(engine.gen_legal_moves())
    out.write(f"legal moves at root: {n_moves}\n")

    engine = build_engine(fen)
    t = run_workload(f"MCTS x{MCTS_ITERATIONS}", lambda: engine.monte_carlo_search(iterations=MCTS_ITERATIONS), 20, out)
    summary.append(("MCTS", t))

    engine = build_engine(fen)
    t = run_workload(f"gen_legal_moves x{MOVEGEN_REPS}",
                     lambda: [engine.gen_legal_moves() for _ in range(MOVEGEN_REPS)], 20, out)
    summary.append(("movegen", t))

    engine = build_engine(fen)
    t = run_workload(f"is_in_check x{CHECK_REPS}",
                     lambda: [engine.is_in_check(engine.side) for _ in range(CHECK_REPS)], 15, out)
    summary.append(("is_in_check", t))

    print(" done")
    return summary


def main():
    with open(LOG_PATH, "w") as out:
        out.write(f"engine profile run at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        out.write(f"MCTS_ITERATIONS={MCTS_ITERATIONS}  MOVEGEN_REPS={MOVEGEN_REPS}  CHECK_REPS={CHECK_REPS}\n")

        all_summaries = {}
        for name, fen in POSITIONS.items():
            all_summaries[name] = profile_position(name, fen, out)

        out.write("\n\n" + "="*72 + "\n  SUMMARY (wall time, seconds)\n" + "="*72 + "\n")
        out.write(f"{'position':<55}{'MCTS':>8}{'movegen':>10}{'inCheck':>10}\n")
        for name, rows in all_summaries.items():
            d = dict(rows)
            out.write(f"{name[:54]:<55}{d.get('MCTS',0):>8.3f}{d.get('movegen',0):>10.3f}{d.get('is_in_check',0):>10.3f}\n")

    print(f"\nwrote {LOG_PATH}")


if __name__ == "__main__":
    main()
