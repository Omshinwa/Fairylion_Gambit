# this file has functions for easy way to make movements for cutscenes

# move kallen 1 toward lelouch

# f_move(
#   kallen,
#   1
#   right, left, up, down, toward, away
#   lelouch
    # used in l_move_piece when calling an impossible move during cutscene
    # allow for fantasy moves in cutscenes, only for l_move_piece(A8H8) format

label l_black_scene_change:
    show black onlayer screens
    with transition_bars
    scene onlayer screens
    scene
    return