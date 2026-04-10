import fairylion.CONSTANT as c
from fairylion.simple_piece import Simple_Piece
import math

class Engine_eval():

    def __init__(self):
        self.piece_to_table = {'n':['center_bias_develop', 10], 'b':['center_bias_develop', 3], 'r':['center_bias', 1], 'q':['center_bias', 2]}
        # no_bias isnt a table, it just always return a int
        self.tables = {}
        # those are piece sq tables
        self.tables['center_bias'] = []
        self.tables['center_bias_develop'] = [] # one for white POV, one for black
        self.tables['pawn'] = []

        self.eval = self.eval_default
        self._goal = None # This is the goal condition that changes the evaluation function and win/loss conditions.
        # by default None: this is checkmate
        # 'kill' : eliminate all enemy units
        # 'survive' : survive a number of turns, stalemate = 999999
        # 'defend' 'escape'

        # stalemate flag is either:
        # 0 always draw (regular rules),
        # 1 always win (for defense/survive), return MAX
        # -1 always lose (for must wins), return -MAX
        # 2 the one who gets stalemated loses
        self.stalemate_flag = 0

    @property
    def goal(self):
        return self._goal

    @goal.setter
    def goal(self, cond):
        self._goal = cond
        if cond == None:
            self.stalemate_flag = 0
            self.eval = self.eval_default
        elif cond == 'kill':
            self.eval = self.eval_default
            self.stalemate_flag = -1
        elif cond == 'survive':
            # dont forget to set a turn_limit if theres any, 0 means theres no limit
            self.turn_limit = 0
            self.eval = self.eval_default
            self.stalemate_flag = 1
        else:
            self.eval = cond

    def eval_default(self, *args, set_debug_value=False):
        return self.eval_loop_piecelist(self.eval_single_piece, set_debug_value=set_debug_value)

    # piece value + table base + king safety
    def eval_single_piece(self, piece):
        piece_value = 0
        if piece.fen == 'p':
            if piece.color == 0:
                piece_value = piece.value + self.tables['pawn'][piece.pos]
            else:
                piece_value = piece.value + self.tables['pawn'][len(self.board)-1-piece.pos]
        elif piece.fen == 'i':
            piece_value = piece.value
        elif piece.fen == 'k':
            #checkmate
            #survive
            piece_value = self.eval_king_default(piece)
        else:
            if piece.fen in self.piece_to_table:
                table_2_look = self.piece_to_table[piece.fen][0]
                coefficient = self.piece_to_table[piece.fen][1]
                # piece_value = piece.value + self.tables[table_2_look][piece.pos] * coefficient
                if piece.color == 0:
                    piece_value = piece.value + self.tables[table_2_look][piece.pos] * coefficient
                else:
                    piece_value = piece.value + self.tables[table_2_look][len(self.board)-1-piece.pos] * coefficient
            else:
                piece_value = piece.value
        piece_value *= c.INDEX_TO_SIGN[piece.color]
        return piece_value
        
    def eval_loop_piecelist(self, eval_single_piece:callable, *, set_debug_value = False):
        self.positionCount += 1
        value = 0
        # total_value = 1
        for color in self.PIECELIST:
            if color >=2:
                break
            for piece in self.get_pieces(color):
                piece_value = eval_single_piece(piece)
                # total_value += piece_value
                if set_debug_value:
                    piece.debug_value = piece_value
                value += piece_value
        return value#/total_value

    def eval_king_default(self, king):
        piece_value = 0
        if any(element.value >= 800 for element in self.PIECELIST[1-king.color]['M']): # middle game, calculate king safety
            piece_value = self.eval_king_safety(king)
        else: #else, calculate activity?
            if self.goal is None:
                if king.color == 0: # count only once for both kings, we give a bonus if we trapped the opposing king
                    piece_value = self.corner_king_bonus(king) - self.distance_between_kings()
            else:
                piece_value = 300
        return piece_value
        
    def eval_king_safety(self, king):
        if king.color: # for the black king, look at its 3 squares below it
            direction = self.down
        else:
            direction = self.up
        piece_value = 0
        for j in [1, -1, 0]:
            i = 1
            while self.board[king.pos + (direction+j) * i] is c.EMPTY:
                piece_value -= 5 # king_safety_personnality
                i += 1
        return piece_value
    
    def distance_between_kings(self):
        white_king = self.PIECELIST[0]['K'][0]
        black_king = self.PIECELIST[1]['K'][0]
        where = [self.POS_TO_XY[white_king.pos], self.POS_TO_XY[black_king.pos]]
        return abs(where[0][0] - where[1][0]) + abs(where[0][1] - where[1][1])

    def center_king_bonus(self, king):
        return self.tables['center_bias'][king.pos] * 2

    def corner_king_bonus(self, king):
        enemy_king_pos = self.PIECELIST[1-king.color]['K'][0].pos
        return self.tables['center_bias'][enemy_king_pos] * -2

    def is_checkmated(self, color):
        return len(self.CRITICAL[color]) == 0 or ( self.is_in_check(color) and len(self.gen_legal_moves(color))==0 )

    def is_stalemated(self, color):
        return self.side == color and not self.is_in_check(color) and len(self.gen_legal_moves(color))==0

    # return { (bool) has_terminated, (int) who_won}
    # if who_won == 0: white
    # if who_won == 1: black
    # if who_won == 2: draw
    def is_over(self, color):
        if len(self.gen_legal_moves(self.side))==0: # termination
            if self.is_in_check(self.side): # checkmate
                if color == 1 - self.side:
                    return True,0
                return True,1
            else: # stalemate
                if self.stalemate_flag == 0:
                    return True,2
                elif self.stalemate_flag == 1:
                    return True,0
                elif self.stalemate_flag == -1:
                    return True,1
                elif self.stalemate_flag == 2:
                    return True,1-self.side
        else:
            position_score = self.eval(self)
            if abs(position_score) >= c.MAX_SCORE - 99:
                return True,position_score//abs(position_score) # get the sign
        return False,None

    def calc_piece_sq_tables(self):
        """
        given a specific size, setup the piece sq tables
        """
        if len(self.board) == len(self.tables['center_bias']):
            return
        
        for i in ['center_bias', 'pawn', 'center_bias_develop']:
            self.tables[i] = []
            for sq in self.board:
                if sq is c.OFFBOARD:
                    self.tables[i].append(c.OFFBOARD)
                else:
                    self.tables[i].append(0)

        # setup center table sq
        for i, _ in enumerate(self.tables['center_bias']): 
            if self.board[i] is c.OFFBOARD:
                continue
            coord = self.POS_TO_XY[i] # (x,y)
            xcenter = (self.size[0]-1) / 2
            ycenter = (self.size[1]-1) / 2
            average = int(xcenter/2 + ycenter/2)
            value = average - int(abs(xcenter - coord[0])) - int(abs(ycenter - coord[1]))
            self.tables['center_bias'][i] = value

            self.tables['center_bias_develop'][i] = value
            if coord[1] == 0:
                self.tables['center_bias_develop'][i] -= 1

        # setup center table sq
        for i, _ in enumerate(self.tables['pawn']): 
            if self.board[i] is c.OFFBOARD:
                continue
            if self.POS_TO_XY[i][1] <= 1:
                # starting square
                self.tables['pawn'][i] = -1
                continue
            if self.POS_TO_XY[i][1] >= self.size[1]-2: #almost promotion
                self.tables['pawn'][i] = 100
                continue

            xcenter = (self.size[0]-1) / 2
            x = abs(xcenter - self.POS_TO_XY[i][0])
            y = self.POS_TO_XY[i][1]
            yend_value = 40
            value = yend_value/(self.size[1]-4) * (y-1) - x*6 + 13
            self.tables['pawn'][i] = int(value)


    # usage: print_table('center_bias_develop')
    def print_table(self, which):
        print( self.print_board(self.tables[which], self.repr_print_table) )
    
    @staticmethod
    def repr_print_table(target):
        if target>=0:
            return str(target) + " "
        else:
            return str(target)


    # piece sq tables:
    # pawns better in the middle and to the top