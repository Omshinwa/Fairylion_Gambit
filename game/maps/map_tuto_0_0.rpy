label l_map_tuto_0_0_start:
    # oghi was originally oghi here
    oghi "It should be here."
    penny "I'm Commander [penny()]. Are you the new recruit?"
    oghi "?!"
    oghi "Y-Yes! Sorry Ma'am."
    oghi "(A little girl? She's gonna teach me?!)"
    penny "What is your battle experience?"
    oghi "I've been deployed a few times on the battlefield, but none piloting.. huh..."
    oghi "I never piloted a NEUSUIT before."
    penny "Just call it a NEWSUIT like everyone else. Come with me."
    "(black transition)"
    scene cg_tuto_0
    pause 2
    oghi "Wow..."
    # scene Solid('#fff')
    # show icon movement k at truecenter
    oghi "This is..."
    penny "The NEWSUIT type+: model ROOK."
    oghi "The cream of the cream of NEWSUITs..."
    oghi "A conflict against an enemy should always includes one."
    penny "Indeed, without a ROOK, the best you can hope for is a stalemate."
    $ engine = Engine()
    
    $ chess = Chess_control((6,6), bg="bunker")
    $ chess.drop('r', 'd5')
    $ chess.drop(oghi, 'd3', 1)
    $ chess.drop(penny, 'c3', 1)
    show screen s_battlefield with dissolve
    oghi "Commander [penny()]. Will you show me a demonstration?"
    penny "You get in."
    oghi "?!"
    oghi "Sorry Commander, but out of respect..."
    oghi "Shouldn't I be pilotting PAWNs at first?"
    penny "We're in shortage of soldiers right now."
    penny "So you're one of the lucky ones. Get inside the ROOK [oghi()]."
    oghi "..."
    $ chess.side = 1
    $ engine.copy(chess)
    call l_move_piece(chess.move('d3d4',True) ) from _call_l_move_piece
    oghi "..."

    hide screen s_battlefield 
    scene black
    scene cg_tuto_1
    oghi "Wow... this is better than the simulations..."
    penny "Start the engine."
    scene cg_tuto_2
    oghi "!"
    penny "Good... Seems like your synchronization rate is high enough."
    $ remove(oghi)
    $ remove(penny)
    $ get('r').pilot = oghi
    show screen s_battlefield with dissolve
    penny "Try the controls and move the rook around."
    play audio "sound/tutorial.wav"
    show tutorial onlayer screens:
        align(0.47,0.65)
    "The ROOK is a powerful piece. It moves horizontally and vertically. {b}{color=#4bf}Click on the piece to see its movement.{/color}{/b}"
    hide tutorial onlayer screens
    $ game = Game('tuto_0_0', win='len(chess.history)>4')
    jump l_gameLoop

    $ chess = Chess_control((6,6), bg="bunker")
    scene black
    show screen s_battlefield with dissolve
    oghi "...Wow"
    penny "Come on, get in there. This is a NEWSUIT +."
    $ chess.set_fen("8/2P5/8/8/4r3/2k5 w - - 0 1")
    with dissolve
    $ get("k").pilot = penny
    $ get("P").pilot = victim
    $ victim.health = 1
    $ get("k").pilot.xp = 99
    $ get("r").get_range()
    $ get("r").pilot = oghi
    with dissolve
    oghi "Forgive me if asking this is out of line... em Ma'am..."
    penny "..."
    oghi "I heard [name('the Holy Empire')] will invade [name('the Middle Kingdom')]"
    oghi "Is this correct?"
    penny "You'll find out soon enough. Let's go to the battleground."
    jump l_gameLoop

label l_map_tuto_0_0_Win:
    penny "Seems like you got the handle. Come with me."

label l_map_tuto_0_0_endTurn:
    return

label l_map_insta_story:
    penny "Indeed, without a ROOK, the best you can hope for is a stalemate."

    $ chess = Chess_control((6,6), bg="bunker")
    $ chess.set_fen("6/6/6/6/6/6 w - - 0 1")
    $ chess.drop('black rook', 'e5')
    $ chess.drop('black king', 'b4')
    $ chess.drop('white king', 'a6')
    $ chess.drop('grey queen', 'a1')
    $ get("black king").pilot = penny
    # $ get("white knight").pilot = victim
    $ get("white king").pilot = lelouch
    $ lelouch.health = 1
    $ victim.health = 1
    $ get("black king").pilot.xp = 99
    $ get("black rook").pilot = oghi
    
    oghi "Commander [penny()]. Will you show me a demonstration?"
    scene black
    show screen s_battlefield with dissolve

    # $ get("white king").get_range()
    # with dissolve
    # lelouch "So.., this is the end..."
    # $ chess.drop(kallen, 'b1', 0)
    # with dissolve
    # $ get("white foot").get_range()
    # with dissolve
    # kallen "No! I... I will fight!"

    jump l_gameLoop
    penny "You get in."
    oghi "?!"
    oghi "Sorry Commander, but out of respect..."
    oghi "Shouldn't I be pilotting PAWNs at first?"
    penny "We're in shortage of soldiers right now."
    penny "So you're one of the lucky ones. Get inside the ROOK [oghi()]."
    oghi "..."
    hide screen s_battlefield 
    scene black
    scene cg_tuto_1
    oghi "! This is insane."
    penny "Get in the fucking robot oghi"
    penny "Shut up, you haven't started the engine yet."
    penny "Try the controls, if your synchronization matches..."
    scene cg_tuto_2
    oghi "!"
    penny "Good... Seems like you might be skilled enough."
    penny "Follow me, let's test you."
    $ chess = Chess_control((6,6), bg="bunker")
    scene black
    show screen s_battlefield with dissolve
    oghi "...Wow"
    penny "Come on, get in there. This is a NEWSUIT +."
    $ chess.set_fen("8/2P5/8/8/4r3/2k5 w - - 0 1")
    with dissolve
    $ get("black king").pilot = penny
    $ get("white pawn").pilot = victim
    $ victim.health = 1
    $ get("black king").pilot.xp = 99
    $ get("black rook").get_range()
    $ get("black rook").pilot = oghi
    with dissolve
    oghi "Forgive me if asking this is out of line... em Ma'am..."
    penny "..."
    oghi "I heard [name('Holy Empire')] will invade [name('Middle Kingdom')]"
    oghi "Is this correct?"
    penny "You'll find out soon enough. Let's go to the battleground."
    jump l_gameLoop