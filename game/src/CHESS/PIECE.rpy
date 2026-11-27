init -1 python:
    # # i import this way because just doing
    # from fairylion import *
    # # breaks pickling when saving or reloading

    # id = max (units on the board) + 1 + len(chess.history)

    import fairylion.CONSTANT as c
    from fairylion.simple_piece import Simple_Piece

    class Robot_Piece(Simple_Piece, object): #(object,)
        def __init__(self, piece:str, color=None, pilot=None, pos=None, *, movement=None, pid=None, engine=None, **kwargs):
            global chess
            if color is None:
                if piece.isupper():
                    color = 0
                else:
                    color = 1
            piece = piece.lower()
            self.engine = engine or chess
            super().__init__(piece, color, pos, movement=movement, pid=pid, engine=self.engine)
            self.type = c.FEN_TO_TYPE[self.fen]
            self._pilot = [None]
            if self.type == '*' and not globals().get('rogue'): # story mode: room for two co-drivers (src/queen_co_drive.rpy)
                self._pilot = [None, None]
            self.pilot = pilot # Robot_Piece has a ._pilot property; capacity = len(_pilot), empty slot = None

            self.range = Robot_Piece.get_range_of(self.fen, self.engine, self.color)

            self.value = c.FEN_TO_VALUE[self.fen]
            self.debug_value = None

            self.killable = True
            if self.fen == "g":
                self.killable = False
            
            # id should always be define if it's out of a battle.
            self.pid = pid or len(chess.get_pieces()) + len(ROBOTS) + len(chess.history)
            # self.eatAllies = False
            # self.passThrough = False

            self.unmovable = False # if True, cannot be moved during preparation
            self.deployed = False
        
            for kwarg in kwargs:
                setattr(self,kwarg,kwargs[kwarg])
            self.setup_piece(True)

        # def __hash__(self) -> int:
        #     return self.id

        # def __eq__(self, other):
        #     if type(other) == Robot_Piece:
        #         return self.id == other.id
        #     else:
        #         return False

        def has_pilot_room(self):
            return None in self._pilot

        @classmethod
        def create_promotion(cls, engine, piece, fen, pos):
            return cls(piece=fen, color=piece.color, pilot=piece._pilot, pos=pos, movement=fen, engine=engine)

        def is_pawn_or_foot(self):
            return self.type == 'i' or self.type == '^'

        @property
        def pilot(self): # the driver: seat 0 (for a Queen, its first co-driver). Everyone inside: .pilots
            return self._pilot[0] if self._pilot else None

        @pilot.setter
        def pilot(self, pilot):
            if pilot is None:
                self._pilot = [None for _ in self._pilot]
            elif isinstance(pilot, Pilot): #if we only give 1 pilot, bracket it
                self._pilot[0] = pilot
                if pilot.id in character.__dict__:
                    character.__dict__[pilot.id].char_on_battlefield = self
            elif isinstance(pilot, _list): # else, like we give it directly a list
                for i in range(min(len(self._pilot), len(pilot))):
                    self._pilot[i] = pilot[i]
                    if pilot[i] and pilot[i].id in character.__dict__:
                        character.__dict__[pilot[i].id].char_on_battlefield = self

        @property
        def drivers(self): # the pilots whose skills count for the robot: seat 0, or every pilot of a Queen (src/queen_co_drive.rpy)
            if self.type == '*':
                return self.pilots
            return [self.pilot] if self.pilot else [] # passengers don't affect the robot

        # idk if it's useful
        # would replaces len(self._pilot), check_for_pilot would also turn the piece neutral
        # if theres a pilot inside but that is dead.
        def has_alive_pilot(self):
            if len(self._pilot) >= 1 and self._pilot[0].health > 0:
                return self._pilot[0]
            if len(self._pilot) == 2 and self._pilot[1].health > 0:
                return self._pilot[1]
            return None

        def setup_piece(self, is_promotion_or_new_piece=False):
            """
            1. Change piece model to pilot's
            2. Activate setup skills
            3. Remove double-move for player
            4. Set movement and killable
            """
            # change the type based on the main pilot's candrive skills
            if self.fen != 'i' and self.type != '^' and self._pilot[0] is not None:
                driven_fen = self.driven_fen()
                if driven_fen:
                    # in the promotion case, we must NOT remove piece:
                    if not is_promotion_or_new_piece:
                        chess._remove_piece(self)
                    self.fen = driven_fen
                    self.color = self._pilot[0].color
                    if not is_promotion_or_new_piece:
                        chess._append_piece(self)

            self.range = Robot_Piece.get_range_of(self.fen, self.engine, self.color)
            for pilot in self.drivers: # passengers' skills don't count
                for skill in pilot.skills['setup']:
                    SKILLLIST[skill].effect(pilot, self)

            # remove 2-step by default for player
            if self.fen == 'p' and self.color == chess.player:
                if 'double move' in self.range and self.drivers and not any('2-step' in p.skills['setup'] for p in self.drivers):
                    del self.range['double move']
            
            if Robot_Piece.get_range_of(self.fen, self.engine, self.color) == self.range: # if its a default piece
                self.movement = self.fen

            else:
                self.movement = None

            if self.fen == "g":
                self.killable = False
            else:
                self.killable = True

        def driven_fen(self):
            """The piece this robot becomes with its pilots, or None if they can't drive it: the first pilot
            drives it, or two pilots co-drive a Queen (story mode, see src/queen_co_drive.rpy)."""
            first = self._pilot[0]
            if first is None:
                return None
            if self.type in first.can_drive:
                return first.can_drive[self.type]
            if self.type == '*' and len(self.pilots) >= 2 and queen_co_drivers(self.pilots[0], self.pilots[1]):
                return 'q'
            return None

        def check_for_pilot(self):
            """
            if theres no pilot, or is dead, turn the piece neutral, doesnt work on opponent
            else turn into a 0 or 1 color
            """
            # only seat 0 drives: a passenger alone stays inside, but the robot can't move.
            # a Queen with only half of its co-drivers can't move either
            no_driver = self.pilot is None or (self.type == '*' and not self.driven_fen())
            if no_driver and self.color == chess.player:
                chess._remove_piece(self)
                self.color = 2
                chess._append_piece(self)
            elif self.color == 2 and len(self.pilots) and self.driven_fen():
                chess._remove_piece(self)
                self.color = chess.player
                chess._append_piece(self)

        def get_range(self): # used for UI, return a dict { square: Move }
            squares = {}
            for move in self.moves(self.engine):
                if move.to in squares:
                    squares[move.to].append(move)
                else:
                    squares[move.to] = [move]

            return squares

        def alignement(self):
            if prefs.style.pieces == 'robot' and self.fen != 'i':
                return (0.5, 1.0)
            return (0.5, 0.5)
            
        def get_range_set(self): # returns a set {move, move}
            squares = set()
            for move in self.moves(self.engine):
                squares.add(move.to)
            return squares

        @staticmethod  
        def get_range_of(piece, engine, color=0):
            range = Simple_Piece.get_range_of(piece, engine, color)
            range = dict(range)
            return range


init python:
    class Obstacle():
        pass


# Live2D() raises at init if Live2D isn't available (e.g. a web build without the
# Cubism SDK for Web), which stops the whole game from loading. Fall back to Null();
# img_piece() then shows a static piece instead of the rig.
image img_rig_piece = Live2D("images/robot/rook_rig", loop=True) if renpy.has_live2d() else Null()