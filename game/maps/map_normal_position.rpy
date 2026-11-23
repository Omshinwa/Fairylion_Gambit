label load_standard_pos():
    scene onlayer screens
    scene
    $ game = Game('l_osef')
    $ chess = Chess_control()
    $ chess.set_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") # starting pos
    $ chess.perms = python_set({21,28,25,95,91,98}) # starting pos castle_rights
    $ get('K').range['castling'] = python_set({21,28})
    $ get('k').range['castling'] = python_set({91,98})
    show screen s_battlefield(chess)
    with dissolve
    jump l_gameLoop
    return