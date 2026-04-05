# :::                            ::::::::  :::            :::      ::::::::   ::::::::  
#  :+:                          :+:    :+: :+:          :+: :+:   :+:    :+: :+:    :+: 
#   +:+                         +:+        +:+         +:+   +:+  +:+        +:+        
#    +#+                        +#+        +#+        +#++:++#++: +#++:++#++ +#++:++#++ 
#     +#+                       +#+        +#+        +#+     +#+        +#+        +#+ 
#      #+#                      #+#    #+# #+#        #+#     #+# #+#    #+# #+#    #+# 
#       ###                      ########  ########## ###     ###  ########   ########  

default PILOTLIST = set()

init -2 python:

    # The Pilots.csv will automatically set up new fields
    class Pilot(Pilot_lines):
        sort_method = 'default'

        def __init__(self, id, max_health=3, health=None, xp=0, trust=5, **kwargs):
            self.id = id
            if health == None:
                self.health = max_health
            else:
                self.health = health
            self.max_health = max_health
            self.xp = xp
            self.xp_all = 0
            self.trust = trust
            self.desc = ''
            self.price = 0
            self.color = 0

            if getattr(character, id, None):
                self.name = getattr(character, id).name
                PILOTLIST.add(self.id) # if it's a character, add it to the list
            else:
                self.name = 'generic'
        
            self.skills = {
                'can_learn':[],
                # below are learned skills types
     
                'setup':[],     # ex: castle, pacifist
                'move':[],      # NOT USED YET? ex: , movement modifier       trigger: on every movement generation      arg: piece
                'card':[],
                'once':[],      # ex: +1 stamina; can drive L            trigger: when they learn it, usable once
            }
            self.can_drive = {}

            # UI STUFF
            self.deployed = False
            self.default_sort = 999

            for key,value in kwargs.items():
                setattr(self, key, value)

            renpy.pure(self.img_side)
                
        def die(self):
            self.health = 0
            renpy.call_in_new_context('l_pilot_death', self, _clear_layers=False)

        def isHere(self):
            return not self in DEAD_OR_DESERT

        def __call__(self):
            return self.name
        def __repr__(self):
            return self.id
        def __hash__(self):
            return self.default_sort
        
        def increase_xp(self, value):
            self.xp += value
            self.xp_all += value

        def _heart_display(self):
            # return an array representing the health to display
            # '*' = gray/empty
            # 0, 1, 2 or 3 etc = color
            # if it's negatif, it's a small heard
            # if it's positif, it's a big heart.
            heart_list = []
            for heart in range(self.max_health):
                if heart >= self.health:
                    heart_list.append('*')
                else:
                    if heart == 0 and TRUST_TO_LOYALTY(self.trust)<2:
                        heart_list.append(- TRUST_TO_LOYALTY(self.trust))
                    else:
                        heart_list.append(TRUST_TO_LOYALTY(self.trust))

            return reversed(heart_list)

        def rest(self):
            """
            return True if health was changed, False otherwise
            """
            original = self.health
            self.health = min(self.health+1, self.max_health)
            if 'rest' in pilot.skills['once']:
                self.health = min(self.health+1, self.max_health)
            if original != self.health:
                return True
            return False
        
        def learn(self, name:str):
            if not name in self.skills['can_learn']:
                renpy.say('', f"NO SKILL {name}, {pilot} can learn")
                return
            renpy.play("sound/board/select.wav")
            skill = SKILLLIST[name]
            self.skills['can_learn'].remove(name)
            self.skills[skill.type].append(name)

            if skill.type == 'once':  # Activate ONCE skills
                skill.effect(pilot, *skill.args)

            for piece in chess.get_pieces():
                if pilot in piece._pilot:
                    piece.setup_piece()
                    if type(chess.ui['selected'])==int and chess.board[chess.ui['selected']] == piece:
                        squares = piece.get_range()
                        for i in squares:
                            chess.ui["moves"][i] = None 

        def img_side(self):
            if hasattr(self, 'img_side_xy'):
                return Crop((self.img_side_xy[0],self.img_side_xy[1],500,500), self.id)
            else:
                print(f"{self} has no .img_side_xy")
                return Crop((220,220,500,500), self.id)

        def img_side_eyes(self):
            return Transform(self.img_side(), crop=(0,130,450,150), fit='cover')

        @staticmethod
        def sort(TEAM, mode=None):
            if mode is None:
                CycleVariable('Pilot.sort_method', [_("default"), _("STA"), _("EXP"), _("valuable")])()
            else:
                Pilot.sort_method = mode
            if Pilot.sort_method == 'default':
                TEAM.sort(key=lambda element: element.default_sort)
            elif Pilot.sort_method == 'STA':
                TEAM.sort(key=lambda element: (         # False (0) for non-generic, True (1) for generic
                    element.health != element.max_health,     # False (0) for max health, True (1) otherwise
                    -element.health,                           # Sort by health in descending order
                    element.id == 'generic',         
                ))
            elif Pilot.sort_method == 'EXP':
                TEAM.sort(key=lambda element: (
                    len(element.skills['can_learn'])==0,
                    -element.xp                           # Sort by health in descending order
                ))
            elif Pilot.sort_method == 'valuable':
                TEAM.sort(key=lambda element: (             # False (0) for non-generic, True (1) for generic
                    -element.price_euristic()                          # Sort by health in descending order
                ))
            
        @staticmethod
        def get_rogue_recruits():
            available_pilots = [lelouch, nunnally, kallen, cc, suzaku, stanley, china, kaguya, abel, jagen, kaworu, penny, oghi]
            available_pilots = [char for char in available_pilots if char not in TEAM and char.health>0]
            i = []
            while len(i)<2 and len(available_pilots)>0:
                i.append(available_pilots.pop(renpy.random.randint(0,len(available_pilots)-1)))
            
            if rogue.round > 0:
                i.append(GenericPilot())
            return i

        def price_euristic(pilot, precise=False):
            if pilot.name == 'generic':
                return 0

            price = pilot.max_health
            if pilot.max_health > 1:
                price+=1
            if pilot.max_health > 2:
                price+=0.5
            # price += pilot.xp/2

            for category in pilot.skills:
                for skill in pilot.skills[category]:
                    if category == 'can_learn':
                        price += SKILLLIST[skill].cost/3
                    else:
                        price += SKILLLIST[skill].cost/1.5
            if precise:
                return price

            price -= 3
            return int(max(1, price))

# :::::::::  :::::::::  :::::::::: :::::::::  :::::::::: :::::::::: 
# :+:    :+: :+:    :+: :+:        :+:    :+: :+:        :+:        
# +:+    +:+ +:+    +:+ +:+        +:+    +:+ +:+        +:+        
# +#++:++#+  +#++:++#:  +#++:++#   +#+    +:+ +#++:++#   :#::+::#   
# +#+        +#+    +#+ +#+        +#+    +#+ +#+        +#+        
# #+#        #+#    #+# #+#        #+#    #+# #+#        #+#        
# ###        ###    ### ########## #########  ########## ###        
    
    class GenericPilot(Pilot):
        def __init__(self, **args):
            super().__init__(id="generic", max_health=2, **args)
            self.img_side_xy = (250,220)
            self.health = 2
            self.skills['can_learn'].append('2-step')
            self.skills['can_learn'].append('stamina')
            self.skills['once'].append('promote_q')
            self.skills['once'].append('drive_p')
            self.can_drive = {'^':'p'}
            if persistent.sacrifice_skill:
                self.skills['can_learn'].append('sacrifice')

    def l(*possible_speakers:Character):
        """
        Give a list of characters that can say a msg, if the character is dead/has deserted the message isnt displayed
        """
        for char in possible_speakers:
            if char.isHere():
                return getattr(character, char.id)
            else:
                continue
        return Character(condition="False")