import subprocess
import sys
import fairylion

def run_engine_move(engine_path, fen):
    result = subprocess.run([
        sys.executable, '-c', f'''
import sys
sys.path.insert(0, "{engine_path}")
import fairylion
engine = fairylion.Engine()
engine.set_fen("{fen}")
move = engine.think(2000, makemove=True)
print("RESULT:", move.UCI())
'''
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None
    
    # Extract just the line with RESULT:
    for line in result.stdout.split('\n'):
        if line.startswith("RESULT:"):
            return line.replace("RESULT:", "").strip()
    
    return None

engine = fairylion.Engine()
engine.set_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
# Usage
CURRENT_PATH = "/Users/omshinwa/Documents/GAMEDEV/FAIRYLION/Fairylion_Gambit/game/python-packages/"
OLD_ENGINE_PATH = "/Users/omshinwa/Documents/GAMEDEV/FAIRYLION/#old_version_engine_match_testing/python-packages/"

# PLAYING THE GAME
while engine.gen_legal_moves():
    white, black = CURRENT_PATH, OLD_ENGINE_PATH
    best_move = run_engine_move(white, engine.fen)
    engine.move(best_move)
    print(engine)
    best_move = run_engine_move(black, engine.fen)
    engine.move(best_move)
    print(engine)
print('game over')