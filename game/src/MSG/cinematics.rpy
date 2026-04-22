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

# transform to have a displayable at POS
# add "square default eatpiece" at t_camera_follow(centered_pilot.pos)
transform t_camera_follow(pos):
    function _t_camera_follow_func(pos)

init python:
    def _t_camera_follow_func(pos):
        def _f(trans, st, at):
            x, y = chess_camera.board_offset_center()
            x += 1920/2.0
            y += 1080/2.0
            x2, y2 = chess.POS_TO_SXY(pos, .5)
            x2 -= (SQUARESIZE * chess.size[0])/2.0
            y2 -= (SQUARESIZE * chess.size[1])/2.0
            x += x2 * chess_camera.zoom
            y += y2 * chess_camera.zoom
            trans.pos = (absolute(x), absolute(y))
            trans.anchor = (.5,.5)
            trans.zoom = chess_camera.zoom
            return 0 if st < 0.6 else None
        return _f