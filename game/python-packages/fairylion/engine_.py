import fairylion.CONSTANT as c
from fairylion.simple_piece import Simple_Piece
from fairylion.move import Move, HistoryNode
from fairylion.evaluation import Engine_eval
from fairylion.mcts import MonteCarloSearchMixin
from fairylion.engine_utils import EngineUtils
from fairylion.minimax import MinimaxSearchMixin

"""
Only contains the base logic and make_move / undo

Engine vs Chess_control
Chess_control has pilots and skills
Engine isnt aware of them
"""
class Engine(Engine_eval, MonteCarloSearchMixin, EngineUtils, MinimaxSearchMixin):

    PieceClass = Simple_Piece

    def __init__(self, size=(8,8), level=0, personnality = None):
        Engine_eval.__init__(self)

        Move.engine = self
        Simple_Piece.engine = self

        self.level = level
        self.personnality = personnality
        self.positionCount = 0

        self.board = []
        self.side = 0
        
        self.setup_chess(size)
        
    def setup_chess(self, size):
        """
        reset promotions, history, and castling perms
        """
        self.perms = set()
        self.promotions = [[], []] # list of starting pieces that you can promote to.
        self.history = []
        self.reset_piecelist()
        self.setup_board(size)

    def reset_piecelist(self):
        self.PIECELIST = {
        # { 'p': pawns, 'm': minor pieces 'M': major pieces 'K': kings}
            0: {'p': [], 'm': [], 'M': [], 'K': []},  # white pieces
            1: {'p': [], 'm': [], 'M': [], 'K': []},  # black pieces
            2: {'misc': []}
            }
        self.CRITICAL = {0: [], 1: []}

    def append_piece(self, piece):
        self._append_piece(piece)
        if isinstance(self.board[piece.pos], self.PieceClass):
            self.remove_piece(self.board[piece.pos])
        self.board[piece.pos] = piece

    def _append_piece(self, piece):
        # dont forget to change board[] also
        if piece.color == 2:
            self.PIECELIST[2]['misc'].append(piece)
        else:
            self.PIECELIST[piece.color][c.FEN_TO_CLASS[piece.fen]].append(piece)
            # by default, all the kings are critical pieces
            if piece.fen == 'k':
                self.CRITICAL[piece.color].append(piece)

    def remove_piece(self, piece):
        self._remove_piece(piece)
        self.board[piece.pos] = c.EMPTY

    def _remove_piece(self, piece):
        # dont forget to change board[] also
        # self.PIECELIST[piece.color].remove(piece)
        if piece.color == 2:
            self.PIECELIST[2]['misc'].remove(piece)
        else:
            try:
                self.PIECELIST[piece.color][c.FEN_TO_CLASS[piece.fen]].remove(piece)
            except:
                print(f"!!!! cant remove {piece} !!!!")
                print(f"piecelist before remove: {self.PIECELIST[piece.color]}")
                print(f"\nboard before remove: {self}")
                self.PIECELIST[piece.color][c.FEN_TO_CLASS[piece.fen]].remove(piece)
            # removing critical pieces from CRITICAL should never happen?
            # if piece in self.CRITICAL[piece.color]:
            #     print(f"REMOVING {piece}")
            #     self.CRITICAL[piece.color].remove(piece)

    def setup_board(self, size=None):
        """
        we dont reset the piecelist, dont tell me why i forgot
        setup self. size, board[], left/right/up/down, ui, PIECELIST
        also setup self.XY_TO_POS[][], self.POS_TO_XY[]
        """

        if size is None:
            size = self.size
        else:
            self.size = size

        self.board = []
        self.XY_TO_POS = []
        self.POS_TO_XY = {}

        for i in range(size[0]):
            self.XY_TO_POS.append([])
            for j in range(size[1]):
                self.XY_TO_POS[i].append(0)

        for i in range(size[0]+2):
            self.board.append(c.OFFBOARD)
            self.board.append(c.OFFBOARD)

        for j in range(size[1]):
            self.board.append(c.OFFBOARD)
            for i in range(size[0]):
                self.board.append(c.EMPTY) # the actual squares
                self.XY_TO_POS[i][j] = len(self.board)-1 # add it to xy representation
                self.POS_TO_XY[self.XY_TO_POS[i][j]] = (i, j)
            self.board.append(c.OFFBOARD)

        for i in range(size[0]+2):
            self.board.append(c.OFFBOARD)
            self.board.append(c.OFFBOARD)
        
        self.left = -1
        self.right = 1
        self.up = self.XY_TO_POS[0][1] - self.XY_TO_POS[0][0]
        self.down = self.up * -1
    
        self.calc_piece_sq_tables()
                

    #         # ::::    ::::   ::::::::  :::     ::: :::::::::: ::::::::  :::::::::: ::::    ::: 
    #         # +:+:+: :+:+:+ :+:    :+: :+:     :+: :+:       :+:    :+: :+:        :+:+:   :+: 
    #         # +:+ +:+:+ +:+ +:+    +:+ +:+     +:+ +:+       +:+        +:+        :+:+:+  +:+ 
    #         # +#+  +:+  +#+ +#+    +:+ +#+     +:+ +#++:++#  :#:        +#++:++#   +#+ +:+ +#+ 
    #         # +#+       +#+ +#+    +#+  +#+   +#+  +#+       +#+   +#+# +#+        +#+  +#+#+# 
    #         # #+#       #+# #+#    #+#   #+#+#+#   #+#       #+#    #+# #+#        #+#   #+#+# 
    #         # ###       ###  ########      ###     ########## ########  ########## ###    #### 

    @staticmethod
    def can_land_on(piece, target):
        '''
        help in move generation. tells it if its legal or what kind of flag it has
        only for standard pieces, not for infantry
        return
        False: offboard or uncapturable
        m : move
        c : capture
        '''
        if target is c.OFFBOARD: # OFFBOARD
            return False
        if target == c.EMPTY: # EMPTY
            return 'm'
        
        if isinstance(target, Simple_Piece): # we eating a piece?
            if piece.color != target.color:
                if target.killable:
                    return 'c'
            elif target.fen == 'i' and None in piece._pilot:
                return 'r' # rescue
        return False
    
    #
    #       INFANTERY STUFF
    #

    @staticmethod
    def can_infant_on(piece, target):
        '''
        can_land_on but for infantry
        '''
        if target is c.OFFBOARD: # OFFBOARD
            return False
        if target == c.EMPTY: # EMPTY
            return 'm'
        
        if isinstance(target, Simple_Piece) and None in target._pilot: # moving to a piece
            if target.color == piece.color:
                return 'enter_ally'
            elif target.color == 2:
                return 'enter_empty'
        return False
    
    def move_enter(self, move, piece, board):
        target = board[move.to]
        self._remove_piece(piece)

        target.add_pilot(piece._pilot[0])
        if target.color == 2: # ENTER EMPTY
            self.color = piece.color
        else:  # ENTER ALLY
            pass
        if piece in self.CRITICAL[piece.color]: # update CRITICAL
            self.CRITICAL[piece.color].remove(piece)
            self.history[-1].critical_remove = True
            if target not in self.CRITICAL[piece.color]:
                self.CRITICAL[piece.color].append(target)
                self.history[-1].critical_add = True

    def move_rescue(self, move, piece):
        infantry = move.data['r']
        # Transfer infantry pilot IDs to the rescuing piece
        piece.add_pilot(infantry._pilot[0])
        self._remove_piece(infantry)
        if infantry in self.CRITICAL[move.piece.color]: # update CRITICAL
            self.CRITICAL[move.piece.color].remove(infantry)
            self.history[-1].critical_remove = True
            if piece not in self.CRITICAL[piece.color]:
                self.CRITICAL[piece.color].append(piece)
                self.history[-1].critical_add = True

    def undo_enter_empty(self, move, piece, board, last_state):
        piece.pos = move.fr
        self._append_piece(piece)
        target = board[move.to]
        target.color = 2
        target._pilot.remove(piece._pilot[0])
        if last_state.critical_remove:
            self.CRITICAL[piece.color].append(piece)
        if last_state.critical_add:
            self.CRITICAL[piece.color].remove(target)

    def undo_enter_ally(self, move, piece, board, last_state):
        piece.pos = move.fr
        self._append_piece(piece)
        target = board[move.to]
        for p in piece.pilots:
            if p in target._pilot:
                target._pilot[target._pilot.index(p)] = None
                break
        if last_state.critical_remove:
            self.CRITICAL[piece.color].append(piece)
        if last_state.critical_add:
            self.CRITICAL[piece.color].remove(target)
    #
    #       INFANTERY STUFF
    #

    def make_move(self, move:Move, check_legality=True): # MAKEMOVE

        board = self.board
        self.history.append(HistoryNode(move))
        piece = move.piece
        # piece = board[move.fr] # surefire case?

        piece.pos = move.to
        
        if piece.fen != 'i': # 
            board[move.to] = piece
        elif not move.flag: # if no flag: infantry moves to an empty spot
            board[move.to] = piece
            
        board[move.fr] = c.EMPTY
        
        if move.fr in self.perms:
            self.perms.remove(move.fr)
            self.history[-1].remove_perms.append(move.fr)

        capture = move.capture
        data = move.data

        if len(move.flag) == 0: # normal move
            if capture:
                self._remove_piece(capture)
        elif 'en passant' in move.flag:
            self._remove_piece(capture)
            board[capture.pos] = c.EMPTY
        elif 'promotion' in move.flag:
            if capture:
                self._remove_piece(capture)
            new_piece = move.data['p']
            board[piece.pos] = new_piece
            self._remove_piece(piece)
            self._append_piece(new_piece)
        elif 'castleK' in move.flag:
            for castlePerm in piece.range['castling']:
                self.perms.discard(castlePerm)
            if self.board[data.pos] == data:
                self.board[data.pos] = c.EMPTY
            data.pos = move.to - 1
            self.board[data.pos] = data
        elif 'castleQ' in move.flag:
            for castlePerm in piece.range['castling']:
                self.perms.discard(castlePerm)
            if self.board[data.pos] == data:
                self.board[data.pos] = c.EMPTY
            data.pos = move.to + 1
            self.board[data.pos] = data

        elif 'enter_ally' in move.flag or 'enter_empty' in move.flag:
            self.move_enter(move, piece, board)
        elif 'rescue' in move.flag:
            self.move_rescue(move, piece)

        else: # for which case does this apply? IT APPLIES FOR CHECK
            if capture:
                self._remove_piece(capture)

        self.side = 1-self.side

        if check_legality and self.is_in_check(move.color):
            # KING IS IN DANGER, illegal
            self.undo();
            return False;
        return True

    def undo(self):
        last_state = self.history.pop()

        for i in last_state.remove_perms: # restore the permissions like the previous move
            self.perms.add(i)

        move = last_state.move
        capture = move.capture
        board = self.board
        piece = move.piece
        # piece = board[move.to] # surefire case?
        data = move.data

        # move back the piece that moved
        piece.pos = move.fr
        board[move.fr] = piece

        if len(move.flag) == 0: # normal move
            if move.capture:
                board[move.to] = capture
                self._append_piece(capture)
            else:
                board[move.to] = c.EMPTY
        elif 'en passant' in move.flag:
            board[move.to] = c.EMPTY
            board[capture.pos] = capture
            self._append_piece(capture)
        elif 'promotion' in move.flag:
            # self.piece_count -= 1
            self._remove_piece(board[move.to])
            self._append_piece(piece)
            if move.capture:
                board[move.to] = capture
                self._append_piece(capture)
            else:
                board[move.to] = c.EMPTY
        
        elif 'castleK' in move.flag:
            board[move.to] = c.EMPTY
            if self.board[data.pos] == data:
                self.board[data.pos] = c.EMPTY
            if piece.color == 0:
                data.pos = self.XY_TO_POS[self.size[0]-1][0]
            else:
                data.pos = self.XY_TO_POS[self.size[0]-1][self.size[1]-1]
            self.board[data.pos] = data

            for castlePerm in piece.range['castling']:
                self.perms.add(castlePerm)

        elif 'castleQ' in move.flag:
            board[move.to] = c.EMPTY
            if self.board[data.pos] == data:
                self.board[data.pos] = c.EMPTY
            if piece.color == 0:
                data.pos = self.XY_TO_POS[0][0]
            else:
                data.pos = self.XY_TO_POS[0][self.size[1]-1]
            self.board[data.pos] = data
            
            for castlePerm in piece.range['castling']:
                self.perms.add(castlePerm)

        elif 'enter_empty' in move.flag:
            self.undo_enter_empty(move, piece, board, last_state)
        elif 'enter_ally' in move.flag:
            self.undo_enter_ally(move, piece, board, last_state)
        elif 'rescue' in move.flag:
            infantry = move.data['r']
            self.board[move.to] = infantry
            self._append_piece(infantry)
            # Remove transferred pilot from the rescuing piece
            piece._pilot.remove(infantry._pilot[0])
            if last_state.critical_add:
                self.CRITICAL[piece.color].remove(piece)
            if last_state.critical_remove:
                self.CRITICAL[piece.color].append(infantry)

        else: # for what case? # for the double_move case
            if move.capture:
                board[move.to] = capture
                self._append_piece(capture)
            else:
                board[move.to] = c.EMPTY

        self.side = 1-self.side

    def gen_moves(self, side: int = None) -> list:
        """
        Generate all pseudo-legal moves for the given side.
        """
        if side is None:
            side = self.side
        moves = []
        for piece in self.get_pieces(side):
            moves = piece.moves(self, moves)
        return moves

    def gen_legal_moves(self, side=None):
        if side is None:
            side = self.side
        moves = []
        legals = []
        for piece in self.get_pieces(side):
            moves = piece.moves(self, moves)
        for move in moves:
            if self.make_move(move):
                legals.append(move)
                if self.is_in_check(1-move.color):
                    move.flag.add('check')
                self.undo()
        return legals

    def is_in_check(self, color):
        kings = self.CRITICAL[color]
        for king in kings:
            if self.is_sq_atk(king.pos, 1-color):
                return True
        return False
    
    def is_sq_atk(self, sq: int, side: int = None) -> bool:
        """
        Returns True if the square is attacked by the given side.
        """
        if side is None:
            side = self.side
        attacked_squares = set()
        
        for piece in self.get_pieces(side):
            if piece.movement == 'p':
                direction = self.down if side else self.up
                pos = piece.pos
                if sq == pos+1+direction or sq == pos-1+direction:
                    return True
            else:
                piece.atk_sq(self, attacked_squares)

        # print(f"attacked_squares : {attacked_squares}")
        return sq in attacked_squares

    def print_atk(self,side=None):
        if side is None:
            side = self.side
        repr = ""
        for sq, target in enumerate(self.board):
            if sq % (self.size[0]+2) == 0:
                repr += "\n"
            if target is c.OFFBOARD:
                repr += " _"
            elif self.is_sq_atk(sq, side):
                repr += ' X'
            else:
                repr += " ."
        repr = '\n'.join(repr.split("\n")[::-1])
        print(repr)