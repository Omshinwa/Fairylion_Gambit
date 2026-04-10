import fairylion.CONSTANT as c
from fairylion.move import *
from fairylion.simple_pilot import Simple_Pilot

class Simple_Piece():
    # __slots__ = ("fen", "color", "pos", "range", "movement", "value", "killable", "starting_sq")
    engine = None
    def __init__(self, piece:str, color:int=0, pos:int=0, *, range=None, movement=None, pid=None, engine=None, pilot=None):

        self.fen = piece
        self.color = color;

        self.pos = pos
        self.range = range or Simple_Piece.get_range_of(self, engine)
        self.movement = movement
        self.value = c.FEN_TO_VALUE[self.fen]

        if piece == 'g':
            self.killable = False
        else:
            self.killable = True
        if engine is None:
            self.pid = -1
        else:
            self.pid = pid or len(engine.get_pieces())
        # self.eatAllies = False
        # self.passThrough = False
        if isinstance(pilot, Simple_Pilot):
            self._pilot = [pilot]
        elif isinstance(pilot, list):
            self._pilot = pilot
        else:
            self._pilot = [None]

    def __repr__(self):
        if self.color == 0:
            txt = c.FEN_TO_PIECE[self.fen].upper()
        elif self.color == 1:
            txt = c.FEN_TO_PIECE[self.fen]
        else:
            txt = c.FEN_TO_PIECE[self.fen]
        if self.engine and self.pos is not None:
            return f"{txt} {self.engine.POS_TO_A8(self.pos)}"
        else:
            return f"{txt} {self.pos}"
        
    # def __hash__(self):
    #     return self.id
    # def __eq__(self, other):
    #     if type(other) == Simple_Piece:
    #         return self.id == other.id
    #     else:
    #         return False
    
    @property
    def pilot(self):
        if len(self._pilot) == 0:
            return None
        elif len(self._pilot) == 1:
            return self._pilot[0]
        else:
            return self._pilot

    @property
    def pilots(self): # _pilot without the None
        return [p for p in self._pilot if p is not None]
    
    # @pilot.setter
    # def pilots(self, pilot):
    #     if pilot is None:
    #         self._pilot = [None for _ in self._pilot]
    #     elif isinstance(pilot, list):
    #         for i in range(min(len(self._pilot), len(pilot))):
    #             self._pilot[i] = pilot[i]
    #     else: #if we only give 1 pilot, bracket it
    #         self._pilot[0] = pilot

    @pilot.setter
    def pilot(self, pilot):
        if pilot is None:
            self._pilot = [None for _ in self._pilot]
        elif isinstance(pilot, list):
            for i in range(min(len(self._pilot), len(pilot))):
                self._pilot[i] = pilot[i]
        else: #if we only give 1 pilot, bracket it
            self._pilot[0] = pilot

    @property
    def x(self) -> int:
        return self.engine.POS_TO_XY[self.pos][0]
    @x.setter
    def x(self, x:int):
        self.engine.board[self.pos] = c.EMPTY
        y = self.engine.POS_TO_XY[self.pos][1]
        self.pos = self.engine.XY_TO_POS[x][y]
        self.engine.board[self.pos] = self
    @property
    def y(self) -> int:
        return self.engine.POS_TO_XY[self.pos][1]
    @y.setter
    def y(self, y:int):
        self.engine.board[self.pos] = c.EMPTY
        x = self.engine.POS_TO_XY[self.pos][0]
        self.pos = self.engine.XY_TO_POS[x][y]
        self.engine.board[self.pos] = self
    @property
    def pos_a8(self) -> str:
        return self.engine.POS_TO_A8(self.pos)
    @pos_a8.setter
    def pos_a8(self, a8:str):
        self.engine.board[self.pos] = c.EMPTY
        self.pos = self.engine.A8_TO_POS(a8)
        self.engine.board[self.pos] = self
        
    def get_move_of_instruction(self, moves, instruction, offset, engine):
        MOVE_TO_FUNCTION[instruction](self, moves, offset, self.pos, engine)
        return 

    def get_atk_sq_of_instruction(self, engine, squares, instruction, offset):
        # dont care about colors (so we could use that to count protection?)
        # only return squares attacked (not Moves)
        board = engine.board
        if instruction in ATK_TO_FUNCTION:
            ATK_TO_FUNCTION[instruction](squares, offset, self.pos, board)
        return squares

    def moves(self, engine = None, moves = None): # used for AI/logic, return a list [Move, Move]
        engine = engine or self.engine
        if moves is None:
            moves = []
        range = self.range
        for instruction in range:
            if instruction == 'castling' and engine.is_sq_atk(self.pos, 1-engine.side):
                continue
            MOVE_TO_FUNCTION[instruction](self, moves, range[instruction], self.pos, engine)
        return moves
            
    def atk_sq(self, engine, squares = None):
        range = self.range
        if squares is None:
            squares = set()

        for instruction in range:
            self.get_atk_sq_of_instruction(engine, squares, instruction, range[instruction])

        return squares

    def add_pilot(self, *pilot_list):
        for pilot in pilot_list:
            if pilot is not None:
                for i in range(len(self._pilot)):
                    if self._pilot[i] is None:
                        self._pilot[i] = pilot
                        break

    @classmethod
    def create_promotion(cls, engine, piece, fen, pos):
        return cls(fen, piece.color, pos, movement=fen, engine=engine, pilot=piece._pilot)

    def has_pilot_room(self):
        return None in self._pilot

    def is_ally(self, target):
        if self.color == target.color:
            return True
        return False

    def is_enemy(self, target):
        if self.color == 1 - target.color:
            return True
        return False

    def is_different(self, target):
        if self.color != target.color:
            return True
        return False

    @staticmethod            
    def get_range_of(piece, engine, color=0):
        """
        piece: str or Piece
        """
        if isinstance(piece, Simple_Piece):
            color = piece.color
            piece = piece.fen
        range = {}
        if piece == 'p':
            if color:
                direction = -1
            else:
                direction = 1
            range['JUMP_cap_only'] = {1+engine.up*direction, -1+engine.up*direction}
            range['JUMP_no_cap'] = {engine.up*direction}
            if engine.size[1]>=7:
                range['en passant'] = engine.up*direction
                range['double move'] = engine.up*2*direction

        elif piece == 'n':
            range['JUMP'] = {engine.down*2+engine.left, engine.up*2+engine.right, engine.down*2+engine.right, engine.up*2+engine.left, engine.down+engine.left*2, engine.up+engine.right*2, engine.down+engine.right*2, engine.up+engine.left*2}
        elif piece == 'b':
            range['LINE'] = {engine.down+engine.left, engine.up+engine.right, engine.down+engine.right, engine.up+engine.left}
        elif piece == 'r':
            range['LINE'] = {engine.down, engine.up, engine.left, engine.right}
        elif piece == 'q':
            range.update(Simple_Piece.get_range_of('r', engine))
            range['LINE'].update(Simple_Piece.get_range_of('b', engine)['LINE'])
        elif piece == 'k':
            range['JUMP'] = {engine.down, engine.up, engine.left, engine.right, engine.down+engine.left, engine.up+engine.right, engine.down+engine.right, engine.up+engine.left}
        elif piece == 'g':
            range['WARP'] = {'no_capture'}
        elif piece == 'c':
            range['LINE_no_cap'] = {engine.down, engine.up, engine.left, engine.right}
            range['LINE_jump'] = {engine.down, engine.up, engine.left, engine.right}
        elif piece == 'i':
            range['FOOT'] = {engine.down, engine.up, engine.left, engine.right}
        return range
