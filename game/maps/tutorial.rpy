# The second argument allow the player to skip with TAB, it also allows they to
# interact with what's behind the tutorial potentially
label l_tutorial(which, unskippable=True):
    # whenever we click on the '?' icon
    play audio "sound/tutorial.wav"
    show screen s_tutorialPause(which, unskippable) with dissolve
    pause
    hide screen s_tutorialPause
    if renpy.can_show(f"tutorial {which}2"):
        call l_tutorial(which+'2', unskippable) from _call_l_tutorial_1
    if renpy.can_show(f"tutorial {which}3"):
        call l_tutorial(which+'3', unskippable) from _call_l_tutorial_2
    return

screen s_tutorialPause(which, unskippable=True):
    zorder 2
    on 'show' action Function(renpy.layer_at_list, [t_blur], layer='master')
    on 'hide' action Function(remove_blur_master), With(dissolve)

    # DRAWBACK : will prevent skipping:
    # modal True
    if unskippable:
        dismiss:
            action Return()
    
    add "tutorial " + which xysize(1.0, 1.0)

#
#
#

label l_tutorial_checkmate_2Q:
    scene onlayer screens
    $ chess = Chess_control((8,8))
    $ game = Game('tutorial_checkmate_2Q')
    $ chess.set_fen('8/8/8/8/8/3k4/8/3K2QQ w - - 0 1')
    show screen s_battlefield(chess) with dissolve
    play audio "sound/tutorial.wav"
    show stanley at right
    stanley "It's pointless to play chess if you don't know the basics checkmates."
    stanley "You paying attention, prince [lelouch()]?"
    show young_lelouch at left
    young_lelouch "Yes!"
    pause 0.5
    stanley "Let's go over the fundamentals."
    $ chess.ui["arrows"] = {(44,44), (44,94)}
    stanley "First, we will drive the Black King to the edge and corner it."
    $ chess.ui["arrows"] = {(27,27),(28,28)}
    stanley "With two Queens against a lone King, this is straightforward."
    stanley "Don't forget, you can promote Pawns into Queens."
    $ chess.ui["arrows"] = {(27,27),(27,21),(27,97),(27,81),(27,28)}
    stanley "The Queen is the strongest Chess piece; it can move vertically, horizontally, and diagonally across any number of squares."
    $ chess.ui["arrows"] = {(44,44),(44,45),(44,43),(44,33),(44,34),(44,35),(44,53),(44,54),(44,55)}
    stanley "Meanwhile, the King is much weaker, it can move in all eight directions, but only one square."
    $ chess.ui["arrows"] = {(27,37)}
    stanley "Move the Queen up to restrict the King's movement."
    call l_move_piece('g1g2') from _call_l_move_piece_2
    $ chess.ui["arrows"] = {(37,31), (44,34), (34,34)}
    stanley "Here, the King cannot go down, because our Queen would just take it."
    call l_move_piece('d3e3') from _call_l_move_piece_3
    $ chess.ui["arrows"] = {(28,48)}
    stanley "Next, we use the other Queen."
    call l_move_piece('h1h3') from _call_l_move_piece_4
    stanley "Can you visualize where the King can go?"
    young_lelouch "Mhh... I think the King is forced to go up?"
    stanley "You are correct."
    $ chess.ui["arrows"] = {(37,31)}
    stanley "The King cannot move down due to the Queen on g2."
    $ chess.ui["arrows"] = {(37,31), (48,41)}
    stanley "And it can't move left or right because of the Queen on h3."
    stanley "The King can only move 1 square at a time. So the King is forced up."
    call l_move_piece('e3d4') from _call_l_move_piece_5
    $ chess.ui["arrows"] = {(37,57)}
    stanley "We will force the King to move up again with the Queen at the bottom."
    call l_move_piece('g2g4') from _call_l_move_piece_6
    $ chess.ui["arrows"] = {(57,51), (48,41)}
    stanley "We just need to move it two squares up."
    call l_move_piece('d4c5') from _call_l_move_piece_7
    $ chess.ui["arrows"] = {(57,77), (48,68), (68,88), (77,97)}
    stanley "Repeat this laddering process, alternating the Queens."
    call l_move_piece('h3h5') from _call_l_move_piece_8
    $ chess.ui["arrows"] = {(57,77), (68,88), (77,97)}
    pause
    call l_move_piece('c5c6') from _call_l_move_piece_9
    $ chess.ui["arrows"] = {(57,77), (68,88), (77,97)}
    pause
    call l_move_piece('g4g6') from _call_l_move_piece_10
    $ chess.ui["arrows"] = {(68,88), (77,97)}
    pause
    call l_move_piece('c6b7') from _call_l_move_piece_11
    $ chess.ui["arrows"] = {(68,88), (77,97)}
    pause
    call l_move_piece('h5h7') from _call_l_move_piece_12
    $ chess.ui["arrows"] = {(77,97)}
    pause
    call l_move_piece('b7c8') from _call_l_move_piece_13
    pause
    call l_move_piece('g6g8') from _call_l_move_piece_14
    stanley "The King is under attack, but has nowhere to go. This is checkmate."
    young_lelouch "I see..."
    stanley "Be careful, though—if the King has no legal moves but isn't in check, {color=#f00}it's a draw under Chess rules.{/color}"
    stanley "Let's undo to demonstrate."
    $ chess.undo()
    with dissolve
    call l_move_piece('g6b6') from _call_l_move_piece_15
    stanley "This is stalemate."
    $ chess.ui["arrows"] = {(88,81),(72,92), (72,94)}
    stanley "The Queens cover all squares around the King, but the King isn't in check."
    stanley "This results in a draw."
    stanley "Understood?"
    young_lelouch "Yes!"
    $ chess.set_fen('8/8/8/8/8/3k4/8/3K2QQ w - - 0 1')
    with dissolve
    stanley "Time for practice!"
    $ chess.side = 0
    $ game.win_label = 'l_map_tutorial_checkmate_Win'
    $ game.lost_label = 'l_map_tutorial_checkmate_Lose'
    jump l_start_battle

label l_map_tutorial_checkmate_Win:
    if game.level == 'tutorial_checkmate_2Q':
        $ persistent.tutorial_2Q = True
    elif game.level == 'tutorial_checkmate_2R':
        $ persistent.tutorial_2R = True
        call l_tutorial_checkmate_2R_Win
    elif game.level == 'tutorial_checkmate_1R':
        $ persistent.tutorial_1R = True
    show black onlayer screens with transition_bars
    jump start

label l_tutorial_checkmate_2R_Win:
    pause
    show black onlayer screens
    with transition_bars_fast
    $ chess.set_fen('8/8/8/8/4k3/6R1/7R/K7 b - - 0 1')
    hide black onlayer screens
    with transition_bars_fast
    
    "There are faster ways than linking your Rooks."
    call l_move_piece('e4f4') from _call_l_move_piece_16
    $ chess.ui["arrows"] = {(38,48), (38,38)}
    "Instead of moving your h2 Rook up to protect the other Rook..."
    call l_move_piece('g3a3') from _call_l_move_piece_17
    "You could move the Rook to the opposite side."
    $ chess.ui["arrows"] = {(41,48)}
    "The Rook still prevents the King from moving down."
    call l_move_piece('f4e4') from _call_l_move_piece_18
    "While the King cannot catch up."
    call l_move_piece('h2h4') from _call_l_move_piece_19
    "Then, continue the ladder technique from both sides."
    call l_move_piece('e4f5') from _call_l_move_piece_20
    call l_move_piece('a3a5') from _call_l_move_piece_21
    pause
    call l_move_piece('f5g6') from _call_l_move_piece_22
    $ chess.ui["arrows"] = {(58,78)}
    "We can't move up, so we either link both Rooks or..."
    call l_move_piece('h4b4') from _call_l_move_piece_23
    "Move it to the opposite side."
    call l_move_piece('g6f6') from _call_l_move_piece_24
    call l_move_piece('b4b6') from _call_l_move_piece_25
    pause
    call l_move_piece('f6e7') from _call_l_move_piece_26
    call l_move_piece('a5a7') from _call_l_move_piece_27
    pause
    call l_move_piece('e7d8') from _call_l_move_piece_28
    call l_move_piece('b6b8') from _call_l_move_piece_29
    "And this is checkmate."
    "This method is quicker but doesn't work on smaller boards."
    return

label l_map_tutorial_checkmate_Lose:
    if len(chess.gen_legal_moves()) == 0: #no moves left = stalemate
        "This is a stalemate—a draw, as the black King can't move and is not in check."
        "When you make a move, ensure it doesn't lead to stalemate."
        "Let's undo this."
        call l_use_item('undo', True)
    else:
        show black onlayer screens with transition_bars
        jump start
    return

label l_tutorial_checkmate_2R:
    scene onlayer screens
    $ chess = Chess_control((8,8))
    $ chess.set_fen('5/5/5/5/5/1k3/4R/K2R1 w - - 0 1')
    show screen s_battlefield(chess) with dissolve
    play audio "sound/tutorial.wav"
    show stanley at right
    show young_lelouch at left
    stanley "Checkmating with two Rooks is also simple."
    call l_move_piece('d1d3') from _call_l_move_piece_30
    stanley "Force the King to move upward."
    $ chess.ui["arrows"] = {(26,22)}
    stanley "The King can't move down due to the Rook on e2."
    $ chess.ui["arrows"] = {(26,22), (32,29)}
    stanley "The King cannot move left or right due to the Rook on d3."
    $ chess.ui["arrows"] = {}
    call l_move_piece('b3c4') from _call_l_move_piece_31
    stanley "Now what should we do here?"
    young_lelouch "We move the other rook up and force the King to the edge?"
    stanley "Actually, if we kept doing the ladder technique..."
    call l_move_piece('e2e4') from _call_l_move_piece_32
    pause 0.5
    call l_move_piece('c4d3') from _call_l_move_piece_33
    stanley "The King would just take a Rook. That's a mistake, let's undo."
    $ chess.undo()
    with dissolve
    $ chess.undo()
    with dissolve
    $ chess.ui["arrows"] = {(38,32),(32,32)}
    stanley "In this position, the King threatens our Rook. Always be careful of that."
    young_lelouch "I see..."
    # $ chess.ui["arrows"] = {(56, 56), (56, 57), (56, 55), (56, 45), (56, 46), (56, 47), (56, 65), (56, 66), (56, 67)}
    # "The King's range is only 1, so we can just move our Rooks far away first."
    $ chess.ui["arrows"] = {(26,33)}
    stanley "Let's move our Rook one square."
    call l_move_piece('e2e3') from _call_l_move_piece_34
    $ chess.ui["arrows"] = {(32,33),(33,32)}
    stanley "Now the Rooks protect each other."
    stanley "The King must make an idle move."
    call l_move_piece('c4b4') from _call_l_move_piece_35
    stanley "Now that the King is far enough, continue with the ladder."
    call l_move_piece('e3e4') from _call_l_move_piece_36
    call l_move_piece('b4c5') from _call_l_move_piece_37
    stanley "Again, we face the same problem."
    $ chess.ui["arrows"] = {(32,46),(45,46)}
    stanley "Moving the Rook to d5 would result in capture. Instead, link both Rooks again."
    call l_move_piece('d3d4') from _call_l_move_piece_38
    call l_move_piece('c5b5') from _call_l_move_piece_39
    $ chess.ui["arrows"] = {(39,40),(40,39)}
    pause
    call l_move_piece('e4e5') from _call_l_move_piece_40
    call l_move_piece('b5c6') from _call_l_move_piece_41
    pause
    call l_move_piece('d4d5') from _call_l_move_piece_42
    call l_move_piece('c6b6') from _call_l_move_piece_43
    pause
    call l_move_piece('e5e6') from _call_l_move_piece_44
    call l_move_piece('b6a7') from _call_l_move_piece_45
    pause
    call l_move_piece('d5d6') from _call_l_move_piece_46
    call l_move_piece('a7b7') from _call_l_move_piece_47
    pause
    call l_move_piece('e6e7') from _call_l_move_piece_48
    call l_move_piece('b7c8') from _call_l_move_piece_49
    pause
    call l_move_piece('d6d7') from _call_l_move_piece_50
    call l_move_piece('c8b8') from _call_l_move_piece_51
    pause
    call l_move_piece('e7e8') from _call_l_move_piece_52
    stanley "This is checkmate."
    stanley "Let's check some caveats."

    show black onlayer screens
    with transition_bars_fast
    $ chess.set_fen('5/5/5/1k3/3RR/5/5/K4 b KQkq - 0 1')
    hide black onlayer screens
    with transition_bars_fast

    #CAVEATS
    "IDLE MOVES"
    call l_move_piece('b5c5') from _call_l_move_piece_53

    $ chess.ui["arrows"] = {(45,39)}
    stanley "This is your turn. But Black King is too close for your Rooks to ladder, and your Rooks are already linked."

    call l_move_piece('d4c4') from _call_l_move_piece_54
    pause 0.5
    call l_move_piece('c5b5') from _call_l_move_piece_55
    pause 0.5
    call l_move_piece('c4d4') from _call_l_move_piece_56
    pause 0.5
    call l_move_piece('b5c5') from _call_l_move_piece_57
    stanley "If we could just skip our turn, Black would be forced to move away."
    $ chess.ui["arrows"] = {(15,23)}
    stanley "You can just move your own King to waste a tempo."
    call l_move_piece('a1b2') from _call_l_move_piece_58
    call l_move_piece('c5b5') from _call_l_move_piece_59
    pause
    call l_move_piece('e4e5') from _call_l_move_piece_60
    call l_move_piece('b5b6') from _call_l_move_piece_61
    pause
    call l_move_piece('d4d5') from _call_l_move_piece_62
    call l_move_piece('b6c6') from _call_l_move_piece_63
    pause
    call l_move_piece('b2c3') from _call_l_move_piece_64
    call l_move_piece('c6c7') from _call_l_move_piece_65
    pause
    call l_move_piece('e5e6') from _call_l_move_piece_66

    stanley "Understood?"

    $ chess.set_fen('5/5/5/5/5/1k3/4R/K2R1 w - - 0 1')
    with dissolve
    stanley "Time for practice!"
    $ chess.side = 0
    $ game = Game('tutorial_checkmate_2R')
    $ game.win_label = 'l_map_tutorial_checkmate_Win'
    $ game.lost_label = 'l_map_tutorial_checkmate_Lose'
    jump l_start_battle


label l_tutorial_checkmate_1R:
    scene onlayer screens
    $ chess = Chess_control((8,8))
    $ chess.set_fen('8/8/8/8/8/3k4/8/4K2R w - - 0 1')
    show screen s_battlefield(chess) with dissolve
    play audio "sound/tutorial.wav"
    show stanley at right
    show young_lelouch at left
    stanley "Good Morning [lelouch()]."
    stanley "Today, I will teach you the most important checkmate."
    young_lelouch "What is it?"
    stanley "A KING + ROOK vs a lone KING."
    stanley "You can't call yourself a chess player if you don't know how to do that."
    stanley "This checkmate requires teamwork. You'll need to use both your pieces."
    stanley "First restrict the Black King's movement with your Rook."
    call l_move_piece('h1h2') from _call_l_move_piece_67
    $ chess.ui["arrows"] = {(38,31)}
    stanley "The Black King can never cross this imaginary barrier."
    $ chess.ui["arrows"] = {(38,31),(31,91),(91,98),(98,38),}
    stanley "This imaginary box represents the area the Black King is restricted to."
    stanley "We will use both Rook and King to shrink this box."
    call l_move_piece('d3e3') from _call_l_move_piece_68
    stanley "If the Black King ever comes face to face with your King, move your Rook up."
    $ chess.ui["arrows"] = {(25,45)}
    call l_move_piece('h2h3') from _call_l_move_piece_69
    stanley "Now, can you tell me where can the Black King go?"
    young_lelouch "Mhh..."
    $ chess.ui["arrows"] = {(25,34),(25,35),(25,36),(45,34),(45,35),(45,36)}
    young_lelouch "The Black King cannot move down as it's boxed out by our King."
    $ chess.ui["arrows"] = {(48,41)}
    young_lelouch "It also cannot move left or right because of our Rook, so it has to move up."
    stanley "Correct."
    call l_move_piece('e3d4') from _call_l_move_piece_70

    $ chess.ui["arrows"] = {(48,41),(41,91),(91,98),(98,48),}
    stanley "The box has shrinked."

    $ chess.ui["arrows"].update({(54,54), (54,94)})
    stanley "Our goal is to drive the King to the edge, where we will checkmate it."
    $ chess.ui["arrows"] = {}
    stanley "Get your King closer so they can face each others again."
    call l_move_piece('e1e2') from _call_l_move_piece_71
    pause 0.5
    call l_move_piece('d4e4') from _call_l_move_piece_72
    stanley "Here the Black King just came right at us, so bring your Rook."
    call l_move_piece('h3h4') from _call_l_move_piece_73
    $ chess.ui["arrows"] = {(35,44),(35,45),(35,46),(55,44),(55,45),(55,46),(58,51)}
    stanley "The Black King can only move up."

    call l_move_piece('e4d5')
    call l_move_piece('e2e3')
    young_lelouch "I see. But what if the King runs away from us?"
    stanley "Good question, let's illustrate that."
    call l_move_piece('c5') from _call_l_move_piece_76
    call l_move_piece('d3') from _call_l_move_piece_77
    stanley "Here we just keep chasing him."
    call l_move_piece('b5') from _call_l_move_piece_78
    call l_move_piece('c3') from _call_l_move_piece_79
    pause 0.5
    call l_move_piece('a5') from _call_l_move_piece_80
    $ chess.ui["arrows"] = {(43,53), (58,53)}
    stanley "Never cross the Rook's line of sight; it would allow the black King to escape."
    call l_move_piece('c3c4') from _call_l_move_piece_81
    pause 0.5
    call l_move_piece('a4') from _call_l_move_piece_82
    $ chess.ui["arrows"] = {(51,41)}
    stanley "Like this."
    $ chess.undo()
    with dissolve
    $ chess.undo()
    with dissolve
    $ chess.ui["arrows"] = {(58,51),(51,91),(91,98),(98,58),}
    stanley "Remember to not let the Black King out of this box."
    
    call l_move_piece('b3') from _call_l_move_piece_83
    $ chess.ui["arrows"] = {(61,62),(61,71),(61,72)}
    stanley "Here, the black King has to either move up or come toward you."
    call l_move_piece('b5') from _call_l_move_piece_84
    call l_move_piece('h5') from _call_l_move_piece_85
    stanley "If the Kings are facing each others, just bring the Rook."
    $ chess.undo()
    with dissolve
    $ chess.undo()
    with dissolve
    pause 0.5
    call l_move_piece('b6') from _call_l_move_piece_86
    call l_move_piece('h5') from _call_l_move_piece_87
    $ chess.ui["arrows"] = {(68,61),(61,91),(91,98),(98,68),}
    stanley "If they move up, take the space with the Rook anyway."
    young_lelouch "The box got smaller again, the King is near the edge..."
    young_lelouch "Are there any tricky cases?"
    stanley "Well, sometimes Black can avoid facing you."
    call l_move_piece('b4') from _call_l_move_piece_88
    pause 0.3
    call l_move_piece('c6') from _call_l_move_piece_89
    pause 0.3
    call l_move_piece('c4')
    pause 0.3
    call l_move_piece('b6') from _call_l_move_piece_90
    pause 0.3
    call l_move_piece('b4')
    pause 0.3
    call l_move_piece('c6')
    pause 0.5
    call l_move_piece('c4')
    call l_move_piece('b6')
    pause 0.5
    call l_move_piece('b4') from _call_l_move_piece_94
    call l_move_piece('c6') from _call_l_move_piece_95
    stanley "Whenever you move in, they move out."
    pause 0.3
    call l_move_piece('c4')
    pause 0.3
    call l_move_piece('b6')
    pause 0.3
    stanley "It seems like it's impossible to make any progress."
    young_lelouch "If only we could force them to move..."
    stanley "You have the right intuition, you can ''skip'' a turn by doing an ''useless'' move with your Rook."
    call l_move_piece('g5') from _call_l_move_piece_96
    $ chess.ui["arrows"] = {(72,71),(72,73)}
    stanley"Now, either the black King faces you, or it tries to escape. But eventually, it will be forced to face you."
    call l_move_piece('a6')
    pause 0.3
    call l_move_piece('b4')
    $ chess.ui["arrows"] = {(71,72),(71,81),(71,82)}
    stanley "Now like earlier, the black King either comes face you, or it has to move up."
    young_lelouch "I see... This is a bit tricky."
    stanley "Yes. You should remember this technique of wasting a move with your Rook."
    stanley "It is fundamental for checkmating a smart King."
    stanley "Now, let's resume."
    call l_move_piece('b6')
    call l_move_piece('g6')
    stanley "Black is forced to move up."
    call l_move_piece('c7')
    call l_move_piece('b5')
    pause 0.5
    call l_move_piece('d7') from _call_l_move_piece_115
    call l_move_piece('c5') from _call_l_move_piece_116
    pause 0.5
    call l_move_piece('e7') from _call_l_move_piece_117
    call l_move_piece('d5') from _call_l_move_piece_118
    pause 0.5
    call l_move_piece('f7') from _call_l_move_piece_119
    call l_move_piece('e5') from _call_l_move_piece_120
    pause 0.5
    stanley "If your Rook is under threat, move it to the other side."
    call l_move_piece('a6') from _call_l_move_piece_100
    $ chess.ui["arrows"] = {(71, 78)}
    stanley "Here, it still prevents the King from crossing."
    pause 0.5
    call l_move_piece('e7') from _call_l_move_piece_123
    stanley "Face to face, you should be used to it now."
    call l_move_piece('a7') from _call_l_move_piece_124
    call l_move_piece('d8') from _call_l_move_piece_125
    pause 0.5
    young_lelouch "Now it's stuck at the edge!"
    stanley "Correct, we are close to checkmate."
    call l_move_piece('d6') from _call_l_move_piece_126
    call l_move_piece('e8') from _call_l_move_piece_127
    pause 0.5
    call l_move_piece('e6')
    call l_move_piece('d8')
    stanley "Remember, in those infinite loop situation, waste a tempo with your Rook."
    call l_move_piece('h7') from _call_l_move_piece_106
    pause 0.3
    call l_move_piece('c8') from _call_l_move_piece_107
    pause 0.5
    call l_move_piece('d6') from _call_l_move_piece_110
    call l_move_piece('b8') 
    pause 0.5
    call l_move_piece('c6') from _call_l_move_piece_112
    call l_move_piece('a8') from _call_l_move_piece_111
    pause 0.5
    call l_move_piece('b6')
    call l_move_piece('b8') 
    pause 0.5
    call l_move_piece('h8') 
    stanley "The King cannot run up anymore. This is checkmate."
    stanley "Understood?"
    young_lelouch "I'll try."

    $ chess.set_fen('8/8/8/8/8/3k4/8/4K2R w - - 0 1')
    with dissolve
    stanley "This is the last essential checkmate to learn. Good luck!"
    $ chess.side = 0
    $ game = Game('tutorial_checkmate_1R')
    $ game.win_label = 'l_map_tutorial_checkmate_Win'
    $ game.lost_label = 'l_map_tutorial_checkmate_Lose'
    jump l_start_battle



label l_tutorial_checkmate_more:
    "You have learned the basic checkmates."
    "There's other checkmates (like two Bishops vs King), but they're not recommended for beginners."
    "If you're curious, you can learn them on specialized websites like chess.com or lichess."
    "There's also faster ways to checkmate, I've only shown you the simplest way."
    "The sky's the limit in chess!"
    return


#       :::      ::::::::::: ::::    ::: :::::::::: ::::::::  
#      :+:           :+:     :+:+:   :+: :+:       :+:    :+: 
#     +:+            +:+     :+:+:+  +:+ +:+       +:+    +:+ 
#    +#+             +#+     +#+ +:+ +#+ :#::+::#  +#+    +:+ 
#   +#+              +#+     +#+  +#+#+# +#+       +#+    +#+ 
#  #+#               #+#     #+#   #+#+# #+#       #+#    #+# 
# ###            ########### ###    #### ###        ########  


label l_tutorial_piece(piece):
    label .replay:
    python:
        if type(piece) == str:
            piece = Robot_Piece(piece, color=0)
        newboard = Chess_control((6,6), False)
        newboard.ui['camera'].zoom = 0.8
        Move.engine = newboard
        if piece.fen == 'n':
            newboard.set_fen('3p1/p3p/1PN2/1P2p/1p3 w - - 0 1')
            newboard.ui["arrows"] = {(31,17), (17,18), (18,18)}
        elif piece.fen == 'b':
            newboard.set_fen('p4/4p/2B2/1p1P1/4p w - - 0 1')
            newboard.ui["arrows"] = {(31,47)}
        elif piece.fen == 'r':
            newboard.set_fen('2p2/8/1pR1P3/8/2p5 w - - 0 1')
            newboard.ui["arrows"] = {(31,45)}
        elif piece.fen == 'k':
            newboard.set_fen('5/2p2/2K2/3P1/5 w - - 0 1')
            newboard.ui["arrows"] = {(23,23),(24,24),(25,25),(30,30),(32,32), (37,37),(38,38),(39,39)}
        elif piece.fen == 'g':
            newboard.set_fen('5/2p2/2G2/3P1/5 w - - 0 1')
        elif piece.fen == 'c':
            newboard.set_fen('p3p/4P/C1p1p/8/8 w - - 0 1')
            newboard.ui["arrows"] = {(29,31),(33,33)}
        elif piece.fen == 'q':
            newboard.set_fen('p1p1p/5/p1Q1p3/8/p1p1p3 w - - 0 1')
            newboard.ui["arrows"] = {(31,45),(31,47),(31,33)}
        elif piece.fen == 'p':
            newboard.set_fen('5/5/1pp5/8/8/2P5 w - - 0 1')
            newboard.ui["arrows"] = {(17,24), (31,37)}

    python: # show the movement dots
        newboard.state = "selecting"
        piece = get(piece.fen.upper(), board=newboard)
        newboard.clean_moves()
        squares = piece.get_range()
        for sq in squares:
            newboard.ui["moves"][sq] = squares[sq]

    show screen s_tutorial_piece(piece, g.state) with Dissolve(0.2)

    pause 0.5

    if piece.fen in {'n', 'b', 'r', 'k', 'g', 'q'}:
        python:
            renpy.pause(1, modal=False)
            moves = [move for move in newboard.gen_moves(0) if move.fr == 31]
            while len(moves) > 0:
                newboard.make_move(moves.pop(0))
                renpy.pause(1, modal=False)
                newboard.make_move([move for move in newboard.gen_moves(0) if move.to == 31][0])
                newboard.clean_moves()
                squares = piece.get_range()
                for sq in squares:
                    newboard.ui["moves"][sq] = squares[sq]
                renpy.pause(1, modal=False)
    else:
        python:
            if piece.fen == 'c':
                moves = ['a3a4', 'a4a3', 'a3a2', 'a2a1', 'a1a3', 'a3b3', 'b3a3', 'a3e3', 'e3d3', 'd3e3', 'e3e2', 'e2e1', 'e1e5']
            elif piece.fen == 'p':
                moves = ['c1c2', 'c2c3', 'c3b4', 'b4b5', 'b5b6']
                newboard.promotions[0] = ['q']
                
            renpy.pause(1, modal=False)
            while len(moves) > 0:
                newboard.move(moves.pop(0))
                newboard.clean_moves()
                squares = piece.get_range()
                for sq in squares:
                    newboard.ui["moves"][sq] = squares[sq]
                renpy.pause(1, modal=False)
    
    jump .replay
    return

transform t_blur:
    blur 25

screen s_tutorial_piece(piece, previous_state):
    zorder 2
    
    use s_popup_blurry_screen()

    hbox:
        xalign 0.5
        fixed:
            use s_chess_main(newboard, demo=True)
            xysize(0.5,1.0)

        frame:
            style "empty"
            xysize(0.8,1.0)
            yalign 0.5
            xpos -100
            if piece.fen == 'n':
                text _("The Knight jumps to squares in a L-shape.\n\nIt cannot be blocked.") style 'style_info_field'  text_align 0.5 size 50
            elif piece.fen == 'b':
                text _("The Bishop slides along diagonals. \n\nIt always stays on the same color.") style 'style_info_field' text_align 0.5 size 50
            elif piece.fen == 'r':
                text _("The Rook slides horizontally and vertically. \nIts simple movement makes it one of the deadliest pieces.") style 'style_info_field' text_align 0.5 size 50
            elif piece.fen == 'q':
                text _("The Queen slides horizontally, vertically and diagonally. \n\nIt's the most powerful classical piece.") style 'style_info_field' text_align 0.5 size 50
            elif piece.fen == 'k':
                text _("The King can move to any neighbor square. \n\nYou must protect it at all cost.") style 'style_info_field' text_align 0.5 size 50
            elif piece.fen == 'g':
                text _("The Ghost can {color=[g.colors['bluesky']]}jump{/color} to any square. \n\nIt cannot take or be taken.") style 'style_info_field' text_align 0.5 size 50
            elif piece.fen == 'c':
                text _("The Cannon {color=[g.colors['bluesky']]}slides{/color} horizontally and vertically, stopping at the first obstacle. \n\nIt can {color=[g.colors['magenta']]}capture{/color} by hoping over an obstacle.") style 'style_info_field' text_align 0.5 size 50
            elif piece.fen == 'p':
                text _("The Pawn {color=[g.colors['bluesky']]}moves{/color} up one square at a time. \n\nIt can only {color=[g.colors['magenta']]}capture{/color} diagonally forward. \n\nIt promotes into one of your starting pieces when it reaches the last rank.") style 'style_info_field' text_align 0.5 size 50
        
    key "mousedown_3" action NullAction()
    button:
        action Hide(None, Dissolve(.2)),Jump('l_close_pop_up')
        # action Jump('l_close_pop_up')
    