# Example usage of the move CDS statement
# Include this file's statements in your game script to use the move command

# These are example usage patterns:

# Move by square notation:
# move kallen a8
# move lelouch "d3"

# Move by directional offset (left, right, up, down):
# move kallen 2 right          # Move kallen 2 squares to the right
# move kallen 1 left           # Move kallen 1 square to the left
# move lelouch 3 up            # Move lelouch 3 squares up
# move lelouch 1 down          # Move lelouch 1 square down

# Move toward/away from another piece:
# move kallen 1 toward lelouch  # Move kallen 1 square toward lelouch
# move kallen 2 away lelouch    # Move kallen 2 squares away from lelouch

# Move with piece references (if piece is stored in variable):
# move my_robot 1 toward enemy_robot

# Note: The move statement will:
# 1. Find the piece using chess.get() (searches by name/pilot/piece reference)
# 2. Calculate the destination square
# 3. Find a valid move to that square
# 4. Create animation and execute the move via l_move_piece()
# 5. Print errors if piece not found or move is invalid

# Example battle sequence:
label example_battle():
    # These would be used in your story/battle sequences
    move kallen 2 toward lelouch
    pause 1.0
    move lelouch 1 left
    pause 1.0
    move kallen 1 toward lelouch
    return

label pidg_pretty_screenshot:
    $ chess = Chess_control((6,6), bg="castle_gates", bg_board='grass')
    $ chess.set_fen('1bnkq1/2pp2/6/6/1P2PP/G1NK1C')
    $ get('G').pilot = cc
    $ get('C').pilot = china
    $ china.health = 1
    $ get('N').pilot = kaworu
    $ kaworu.xp = 6
    $ AUTO_CENTER_ON_SPEAK_CHAR_BATTLEFIELD = False
    show cc at left
    $ g.state = {'battle'}
    $ f_inspect(get('G'))
    cc "I refuse to kill anyone."
    return

    