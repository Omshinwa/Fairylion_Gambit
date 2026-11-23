label l_slink_lelouch_kallen:
    # scene bg barracks
    show kallen at left
    show lelouch at right
    kallen "[lelouch.name], are we just pawns in you eyes?"


    show lelouch at left
    show nunnally at left
    $ MOVE_SPEAK_CHAR_FORWRD[0] = False
    lelouch "hi"
    show suzaku at right
    nunnally "hi"
    $ chess.remove_piece(get(kallen))
    $ chess.drop(suzaku, 47)
    $ chess.drop(lelouch, 46)
    $ chess.drop(nunnally, 36)
    suzaku "So that's where you two have been."
    lelouch "no" # Lelouch should not be brought to the front layer.