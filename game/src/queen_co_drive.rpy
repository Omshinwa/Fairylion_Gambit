# QUEEN CO-DRIVING (story mode)
# A pilot with drive_q drives a QUEEN alone. Otherwise, two pilots with an affinity of 10 or more (Good)
# can drive it together: one who can drive the ROOK and one who can drive a minor piece (KNIGHT or BISHOP).
# In story mode, Queens have a second seat for this (Robot_Piece.__init__ in src/CHESS/PIECE.rpy).
# Roguelite has no affinity: there, only drive_q drives a Queen.
#
# Used by Robot_Piece.setup_piece / check_for_pilot (src/CHESS/PIECE.rpy) and the preparation
# (prep_can_drop_here in src/CHESS/CHESS_ui.rpy, f_prep_drop_piece in src/CHESS/s_preparation.rpy).

define QUEEN_CO_DRIVE_AFFINITY = 10

init python:
    def can_drive_rook(pilot):
        return '+' in pilot.can_drive

    def can_drive_minor(pilot):
        return 'L' in pilot.can_drive or 'x' in pilot.can_drive

    def queen_co_drivers(a, b):
        """a and b can drive a Queen together."""
        if rogue or a is b or get_affinity(a, b) < QUEEN_CO_DRIVE_AFFINITY:
            return False
        return (can_drive_rook(a) and can_drive_minor(b)) or (can_drive_rook(b) and can_drive_minor(a))

    def pilot_fits_robot(pilot, robot_type):
        """Preparation: the pilot can sit in this robot, to drive it or to co-drive a Queen."""
        if robot_type in pilot.can_drive:
            return True
        return robot_type == '*' and not rogue and (can_drive_rook(pilot) or can_drive_minor(pilot))
