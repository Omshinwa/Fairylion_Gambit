init -2 python:

    class Skill():
        def __init__(self, name, cost=0, desc='', type=None, effect='no_eff', args=[], **kwargs):
            self.name = name
            self.cost = cost

            self.type = type
            # different types, check PILOT

            self.effect = eval('Skill.'+effect)
            self.args = args
            self.desc = desc

            self._can_learn = 'True' # additional condition to learn the skill

            self.present = {'story', 'rogue'} # defines if it is present in story mode or roguemode only

            for kwarg in kwargs:
                setattr(self,kwarg,kwargs[kwarg])


        def __repr__(self):
            return self.name

        def can_learn(self):
            return eval(self._can_learn)

        @staticmethod
        def no_eff(*args):
            return


        #       :::       ::::::::  ::::    :::  ::::::::  :::::::::: 
        #      :+:       :+:    :+: :+:+:   :+: :+:    :+: :+:        
        #     +:+        +:+    +:+ :+:+:+  +:+ +:+        +:+        
        #    +#+         +#+    +:+ +#+ +:+ +#+ +#+        +#++:++#   
        #   +#+          +#+    +#+ +#+  +#+#+# +#+        +#+        
        #  #+#           #+#    #+# #+#   #+#+# #+#    #+# #+#        
        # ###             ########  ###    ####  ########  ########## 

        @staticmethod
        def drive(pilot, *args):
            global rogue
            pilot.can_drive[args[0]] = args[1]
            if args == ('^','p'): # when learning to pilot pawns, add two optional skills
                if '2-step' not in pilot.skills['setup']:
                    pilot.skills['can_learn'].append('2-step')
                if 'promote_q' not in pilot.skills['once'] and 'promote_q' not in pilot.skills['can_learn']:
                    # if rogue:
                    pilot.skills['once'].append('promote_q')
                    # else:
                        # pilot.skills['can_learn'].append('promote_q')

        @staticmethod
        def unlearn(pilot, *skills):
            for skill in skills:
                print(f'unlearning {skill}')
                for category in pilot.skills:
                    if skill in pilot.skills[category]:
                        print(f'found {skill}')
                        pilot.skills[category].remove(skill)
                        break

        
        @staticmethod
        def sacrifice(pilot, *args):
            pilot.die()
            i = 0
            change = {}
            TEAM.sort(key=lambda element:element.xp)
            while pilot.xp > 0:
                new_pilot = TEAM[i%len(TEAM)]
                new_pilot.increase_xp(1)
                if new_pilot in change:
                    change[new_pilot] += 1
                else:
                    change[new_pilot] = 1
                pilot.xp -= 1
                i += 1
            text = ""
            for new_pilot in change:
                text += new_pilot.name + " " + str(new_pilot.xp-change[new_pilot]) + "->" + str(new_pilot.xp) + " " + __("EXP")
                text += "   "
            if len(text) == 0:
                text = " "
            renpy.play('sound/misc/xp.wav', channel='sound')
            renpy.say('[pilot] died', text)

        @staticmethod
        def mercenary_minor(pilot, *args):
            if 'mercenary_major' in pilot.skills['once']:
                pilot.skills['setup'].remove('mercenary')
                pilot.skills['once'].remove('mercenary_minor')
                pilot.skills['once'].remove('mercenary_major')

        @staticmethod
        def mercenary_major(pilot, *args):
            if 'mercenary_minor' in pilot.skills['once']:
                pilot.skills['setup'].remove('mercenary')
                pilot.skills['once'].remove('mercenary_minor')
                pilot.skills['once'].remove('mercenary_major')

        @staticmethod
        def stamina(pilot, *args):
            pilot.max_health += 1
            pilot.health += 1

        @staticmethod
        def veteran(pilot, *args):
            pilot.exp -= 3
            pilot.health += 1


        #       :::       ::::::::  :::::::::: ::::::::::: :::    ::: :::::::::  
        #      :+:       :+:    :+: :+:            :+:     :+:    :+: :+:    :+: 
        #     +:+        +:+        +:+            +:+     +:+    +:+ +:+    +:+ 
        #    +#+         +#++:++#++ +#++:++#       +#+     +#+    +:+ +#++:++#+  
        #   +#+                 +#+ +#+            +#+     +#+    +#+ +#+        
        #  #+#           #+#    #+# #+#            #+#     #+#    #+# #+#        
        # ###             ########  ##########     ###      ########  ###        

        @staticmethod
        def castle(pilot, piece): #setup # TODO probably still dont work correctly (can we castle during checks?)
            if piece.type == '#':
                if piece.color == 0:
                    castle_left = chess.XY_TO_POS[0][0]
                    castle_right = chess.XY_TO_POS[chess.size[0]-1][0]
                    chess.perms.add(piece.pos)
                    chess.perms.add(castle_left)
                    chess.perms.add(castle_right)
                else:
                    castle_left = chess.XY_TO_POS[0][chess.size[1]-1]
                    castle_right = chess.XY_TO_POS[chess.size[0]-1][chess.size[1]-1]
                    chess.perms.add(piece.pos)
                    chess.perms.add(castle_left)
                    chess.perms.add(castle_right)

                piece.range['castling'] = {castle_left, castle_right}
                return True
            return False

        @staticmethod
        def old_castle(pilot, piece): #setup # TODO debug test implement etc
            if piece.type == '#':
                chess.perms.add(piece.pos)
                piece.range['old_castling'] = {piece.pos}
                return True
            return False

        @staticmethod
        def pacifist(pilot, piece):
            if sum(1 for p in piece._pilot if p is not None) > 1:
                return False
            new_range = {}
            for index, instruction in enumerate(piece.range):
                if instruction == "JUMP":
                    new_range["JUMP_no_cap"] = piece.range["JUMP"]

                elif instruction == "LINE":
                    new_range["LINE_no_cap"] = piece.range["LINE"]

                elif instruction == "JUMP_cap_only":
                    pass
                elif instruction == "en passant":
                    pass
                else:
                    new_range[instruction] = piece.range[instruction]
            
            piece.range = new_range
            return True

        @staticmethod #setup
        def initiative(pilot, piece, *args):
            if chess.state == 'start' and chess.side == 'move_first':
                chess.move_first.add(piece)

        @staticmethod #setup
        def mercenary(pilot, piece, *args):
            if chess.state == 'start':
                f_inspect(piece)
                # f_select(piece)
                if 'mercenary_minor' in pilot.skills['once'] and piece.type in {'^','L','x'}:
                    return
                if 'mercenary_major' in pilot.skills['once'] and piece.type in {'+','*'}:
                    return
                renpy.say(getattr(character,pilot.id),_("I'll take some money. (-2 coins)"))
                renpy.sound.play('sound/misc/coin.mp3')
                g.money = max(0, g.money-2)
                renpy.with_statement(dissolve)
        
        @staticmethod #setup
        def fatigue(element, piece, *args):
            global pilot
            if chess.state == 'start':
                pilot = element
                f_inspect(piece)
                renpy.say(getattr(character,pilot.id),_("{i}[pilot.name] Loses 1 Heart."))

                pilot.health -= 1
                renpy.sound.play('sound/misc/menu_back.ogg')
                if pilot.health <= 0:
                    pilot.die()
                renpy.with_statement(dissolve)

        @staticmethod
        def f_call_tarot(tarot):
            renpy.call('l_use_tarot', tarot)

    class Tarot_skill(Skill):
        def __init__(self, tarot, desc, type='trigger', **kwargs):
            super().__init__(tarot, type=type, desc=desc, effect ='f_call_tarot', args=[tarot], **kwargs)
# desc=desc.replace(' \n ', '')
define -1 SKILLLIST = {
    ##driving skills
    'drive_p':  Skill(_("Pawn"),   effect='drive', type='once', args=['^','p'], cost=1,
                desc=_("Can pilot PAWNs."), ),
    'drive_k':  Skill(_("King"),   effect='drive', type='once', args=['#','k'], cost=2,
                desc=_("Can pilot KINGs."), ),
    'drive_r':  Skill(_("Rook"),   effect='drive', type='once', args=['+','r'], cost=3,
                desc=_("Can pilot ROOKs."), ),
    'drive_n':  Skill(_("Knight"), effect='drive', type='once', args=['L','n'], cost=2,
                desc=_("Can pilot KNIGHTs."), ),
    'drive_g':  Skill(_("Ghost"),  effect='drive', type='once', args=['L','g'], cost=2,
                desc=_("Can pilot KNIGHTs as GHOSTs."), ),
    'drive_b':  Skill(_("Bishop"), effect='drive', type='once', args=['x','b'], cost=2,
                desc=_("Can pilot BISHOPs."), ),
    'drive_c':  Skill(_("Cannon"), effect='drive', type='once', args=['x','c'], cost=2,
                desc=_("Can pilot BISHOPs as CANNONs."), ),
    'drive_q':  Skill(_("Queen"),  effect='drive', type='once', args=['*','q'], cost=4,
                desc=_("Can pilot QUEENs."), ),

    'stamina': Skill(_("Stamina Up"), effect ='stamina', type='once', cost=2,
                desc='Increases Max Stamina by 1.',),
    'rest': Skill(_("Rest Up"), effect ='no_eff', type='once', cost=2,
                desc='When Resting, restore 1 extra Stamina.', ),

    'promote_q': Skill(_("Queen Promotion"),   effect='no_eff', type='once', cost=1,
                desc=_("When promoting: [pilot.name] can promote to a QUEEN.")),
    # args in SETUP type just tells the UI what it affects
    '2-step':   Skill(_("Double-Step"), effect ='no_eff', type='setup', cost=1, args=['p'],
                desc=_('When piloting a PAWN: can do a two-step move on its first move (if the board has at least 7 rows).'), ),
    'castle':   Skill(_("Castle"), effect ='castle', type='setup', cost=3, args=['k'],
                desc=_('When piloting a KING, [pilot.name] can perform a Castle.'), ),
    'old_castle':   Skill('Ancient Castle', effect ='castle',  type='setup', cost=2, args=['k'],
                desc=_('When piloting a KING, the piece can Ancient Castle.'),),
    'pacifist': Skill(_("Pacifist"), effect ='pacifist', type='setup', cost=-14,
                desc=_('Cannot attack enemies.'),),
    'resolve': Skill(_("Resolve"),  effect='unlearn', type='once', args=['pacifist','resolve'], cost=6,
                desc=_("Can attack enemies."), ),

    'initiative': Skill(_("Initiative"), effect ='initiative', type='setup', cost=3,
                desc=_("You have the initiative, but [pilot.name] has to move first."), ),

    'sacrifice': Skill(_("Sacrifice"), effect ='sacrifice', type='once', cost=0,
                desc=_("Sacrifice [pilot.name]. Their EXPs is shared to the remaining pilots."), ),

    'fatigue': Skill(_("Fatigue"), effect ='fatigue', type='setup', cost=-4,
                desc=_("[pilot.name] loses 1 Stamina when deployed."), ),

    'mercenary': Skill(_("Mercenary"), effect ='mercenary', type='setup', cost=-10,
                desc=_("Lose 2 coins everytime [pilot.name] is deployed."), ),

    'mercenary_minor': Skill(_("Discount Minor Pieces"), effect ='mercenary_minor', type='once', cost=4,
                desc=_("Don't pay when driving a PAWN, KNIGHT or BISHOP."), ),
    'mercenary_major': Skill(_("Discount Major Pieces"), effect ='mercenary_major', type='once', cost=4,
                desc=_("Don't pay when driving a ROOK or QUEEN."), ),

    # TODO
    'veteran': Skill(_("Veteran"), effect ='veteran', type='once', cost=3, condition="pilot.exp>=3",
                desc=_("Trade 3 EXP to restore 1 Stamina."), ),

    'rook' : Skill(_("Rook+"), effect ='initiative', type='setup', cost=0, condition="len(pilot.skills['can_learn'])==0",
                desc=_("When deployed on foot, produce a new Rook."), ),
    'adrenaline': Skill(_("Adrenaline"), effect ='initiative', type='once', cost=0,
                desc=_("If [pilot.name] is deployed with 1 Stamina and survive, at the end of the battle: restore 1 Stamina."), ),

    'rookie': Skill(_("Fast-Learner"), effect ='no_eff', type='once', cost=2,
                desc=_("Gains 1 extra EXP on deployments"), ),

    'undo': Skill(_("Undo"), effect ='no_eff', type='once', cost=2,
                desc=_("Undo."), ),

    ### TAROT
    
    'fool' : Tarot_skill('fool', _("Pass \n your turn.")),
    'magicien' : Tarot_skill('magicien', _("Go back \n one turn.")),
    'high priestess' : Tarot_skill('high priestess', _("Get a move suggestion")),
    'empress' : Tarot_skill('empress', _("Move the Queen to any empty square.")),
}


label l_try_to_learn(pilot, skill):
    if pilot.xp < SKILLLIST[skill].cost:
        "Not enough EXP. [pilot.name] has [pilot.xp] EXP, the skill [SKILLLIST[skill].name.upper()] requires [SKILLLIST[skill].cost] EXP."
        return
    
    menu:
        "Learn [SKILLLIST[skill].name.upper()] for [SKILLLIST[skill].cost] EXP?"
        "Yes":
            $ pilot.xp -= SKILLLIST[skill].cost
            $ pilot.learn(skill)
        "No":
            return




#       ::: ::::::::      :::     :::        :::        :::::::::: :::::::::  :::   ::: 
#      :+: :+:    :+:   :+: :+:   :+:        :+:        :+:        :+:    :+: :+:   :+: 
#     +:+  +:+         +:+   +:+  +:+        +:+        +:+        +:+    +:+  +:+ +:+  
#    +#+   :#:        +#++:++#++: +#+        +#+        +#++:++#   +#++:++#:    +#++:   
#   +#+    +#+   +#+# +#+     +#+ +#+        +#+        +#+        +#+    +#+    +#+    
#  #+#     #+#    #+# #+#     #+# #+#        #+#        #+#        #+#    #+#    #+#    
# ###       ########  ###     ### ########## ########## ########## ###    ###    ###    

screen s_all_pilots():
    modal True
    add "black"

    textbutton _("< BACK") action With(Dissolve(.25)),Hide() text_style 'style_3d_big_txt':
        at t_interactive

    vpgrid:
        cols 5
        align 0.5,0.5
        for pilot in sorted(PILOTLIST, key=lambda element: globals()[element].default_sort):
            $ pilot = globals()[pilot]
            button at t_interactive:
                xysize 200,200
                action Call('l_character_info', pilot)
                add pilot.img_side() xysize 200,200:
                    if not pilot.xp_all and not show_debug_menu:
                        at transform:
                            on insensitive:
                                matrixcolor ColorizeMatrix("#eee", "#fff")
                sensitive pilot.xp_all or show_debug_menu

    button at t_interactive:
        align (0.0, 1.0)
        action Call('l_tutorial', 's_pilot')
        add 'info_button'

