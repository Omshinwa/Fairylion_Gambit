init -2 python:
    # return the description of a char
    class Pilot_lines():
        def get_desc(self):
            s = ""
            if self.id == 'lelouch': 
                s = _("Banished prince of [name('the Holy Empire')]. Good leader but poor piloting skills.")
            elif self.id == 'kallen': 
                s = _("The 'Lion of the Battlefield'. A pilot prodigy from [name('the Middle Kingdom')].")
            elif self.id == 'cc': 
                s = _("A girl who was part of the 'Super Soldier' project. She vowed to not harm anymore.")
            elif self.id == 'nunnally': 
                s = _("The little sister of [lelouch.name]. Weak health but still wants to fight.")
            elif self.id == 'suzaku':
                s = _("Prince of [name('the Middle Kingdom')]. Yearn for a bohemian life.")
            elif self.id == 'stanley':
                s = _("A veteran of [name('the Holy Empire')]. She's unsure about the war.")
            elif self.id == 'jagen':
                s = _("Respected captain of the royal guard.")
            elif self.id == 'oghi':
                s = _("He betrays [name('the Middle Kingdom')].")
            elif self.id == 'abel':
                s = _("Retainer of [suzaku.name], kind of a pushover.")
            elif self.id == 'vv':
                s = _("A victim of the 'Super Soldier' project. He only cares about [cc.name].")
            elif self.id == 'china':
                s = _("Confident pilot from [name('the Millenium Dynasty')]. The 'Ace'.")
            elif self.id == 'kaworu':
                s = _("She's a bit freaky, but I can fix her...")
            elif self.id == 'kaguya':
                s = _("Pilot from [name('the Millenium Dynasty')], she and [china.name] are dear childhood friends.")
            elif self.id == 'penny':
                s = _("A girl who was part of the 'Super Soldier' project. She has no humanity left.")
            elif self.id == 'young_suzaku':
                s = _("Prince of [name('the Middle Kingdom')].")
            return s

# CC is good at drawing food from memory (hobby she had as a child because she drew what she wanted to eat.)
# Maybe someday she killed someone and decided to never kill (maybe a dog or something). VV remembers

label l_pilot_death(pilot):
    if pilot == lelouch: 
        lelouch "I can't die here... Not yet..."
    elif pilot.id == 'kallen': 
        kallen "Save [name('The Middle Kingdom')]... [lelouch.name]..."
    elif pilot.id == 'cc': 
        cc "So much blood... But I'm glad... I'm human..."
    elif pilot.id == 'suzaku': 
        suzaku "This is... reality..."
    elif pilot.id == 'nunnally': 
        nunnally "My death... will matter..."
    elif pilot.id == 'stanley': 
        stanley "[jagen.name], you better bring out the whiskey."
    elif pilot.id == 'jagen':
        if game and game.level == 4:
            jagen "Run Prince. Don't look back."
        else:
            jagen "My Lord... I've fufilled my duty..."
    elif pilot.id == 'oghi':
        oghi "Life... is just too unfair..."
    elif pilot.id == 'abel':
        abel "[jagen.name], I did my best..."
    elif pilot.id == 'vv':
        vv "[lelouch.name]... Protect [cc.name] please..."
    elif pilot == china:
        china "So I've met my match..."
    elif pilot == kaworu:
        kaworu "I can't die before meeting my soulmate..."
    elif pilot == kaguya:
        kaguya "The world is so vast."
    elif pilot == penny:
        penny ""
    python:
        if pilot in TEAM: # TODO should do this at the end of the map?
            TEAM.remove(pilot)
            DEAD_OR_DESERT.append(pilot)
        else:
            renpy.say('', _(f"{pilot.name} couldnt be found in TEAM."))
    python:
        # only remove it during the setup phase, we dont want to
        # remove it if it's a capture, the piece is gone anyway, it would be
        # impossible to undo, or add it to the
        if chess.state == 'start' or 'preparation' in g.state:
            for piece in chess.get_pieces():
                if pilot in piece._pilot:
                    piece.pilot[piece.pilot.index(pilot)] = None
                    piece.check_for_pilot()
                    break
        # reset_pilot(self.id) only in roguelike
    play sound "sound/death.wav"
    with dissolve

