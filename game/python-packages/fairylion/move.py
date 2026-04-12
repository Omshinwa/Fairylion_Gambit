import fairylion.CONSTANT as c

def move_jump(piece, moves, offset, pos, engine):
    board = engine.board
    for x in offset:
        sq = pos + x
        target = board[sq]
        flag = engine.can_land_on(piece, target)
        if flag:
            if flag == 'm':
                moves.append(Move(piece, pos, sq))
            elif flag == 'c':
                moves.append(Move(piece, pos, sq, capture=target))
            elif flag == 'r':
                moves.append(Move(piece, pos, sq, data={'r':target}, flag='rescue'))

def move_line(piece, moves, offset, pos, engine):
    board = engine.board
    for x in offset:
        sq = pos + x
        target = board[sq]
        i = 1
        flag = engine.can_land_on(piece, target)
        while flag == 'm' or flag == 'r':# and i<99:
            if flag == 'r':
                moves.append(Move(piece, pos, sq, data={'r':target}, flag='rescue'))
            else:
                moves.append(Move(piece, pos, sq))
            i+=1
            sq = pos + x*i
            target = board[sq]
            flag = engine.can_land_on(piece, target)
        if flag:
            moves.append(Move(piece, pos, sq, capture=target))


            # if move.data['p'].fen == 'q' and not 'q' in chess.promotions[chess.player]:
            #     return False

def move_jump_no_cap(piece, moves, offset, pos, engine):
    board = engine.board
    for x in offset:
        sq = pos + x
        target = board[sq]
        flag = engine.can_land_on(piece, target)
        if flag:
            if flag == 'm':
                # promotion?
                if piece.fen == 'p' and engine.POS_TO_XY[sq][1] == (1-piece.color) * (engine.size[1]-1):
                    for possible_promotion in engine.promotions[piece.color]:
                        moves.append(Move(piece, pos, sq, data={'p':return_piece_promotion(engine,piece,possible_promotion,sq)}, flag='promotion'))
                    if should_add_queen_to_promotions(engine, piece):
                        moves.append(Move(piece, pos, sq, data={'p':return_piece_promotion(engine,piece,'q',sq)}, flag='promotion'))
                    elif len(engine.promotions[piece.color]) == 0:
                            moves.append(Move(piece, pos, sq, data={'p':return_piece_promotion(engine,piece,'p',sq)}, flag='promotion'))
                else:
                    moves.append(Move(piece, pos, sq))
            elif flag == 'r':
                moves.append(Move(piece, pos, sq, data={'r':target}, flag='rescue'))

# handling special cases like 'promote_q' or no promotion at all:

# we only add it in the case where 'promote_q' is in the skills
def should_add_queen_to_promotions(engine, piece):
    if piece.pilot and 'promote_q' in piece._pilot[0].skills['once']:
        return True
    return False

def return_piece_promotion(engine, piece, possible_promotion, pos):
    # Q: why do we create a new piece in the move, instead of creating it when doing the move?
    # A: The reason we create a piece on Move creation, is so that when we undo it,
    # when we redo it, we still have the reference to the piece. If we only created it on
    # make_move and don't save the reference, it would lose it on undo.
    return engine.PieceClass.create_promotion(engine, piece, possible_promotion, pos)

def move_jump_cap_only(piece, moves, offset, pos, engine):
    board = engine.board
    for x in offset:
        sq = pos + x
        target = board[sq]
        flag = engine.can_land_on(piece, target)
        if flag == 'c':
            if piece.fen == 'p' and engine.POS_TO_XY[sq][1] == (1-piece.color) * (engine.size[1]-1): # promotion?
                for possible_promotion in engine.promotions[piece.color]:
                    moves.append(Move(piece, pos, sq, capture=target, data={'p':return_piece_promotion(engine,piece,possible_promotion,sq)}, flag='promotion'))
                if should_add_queen_to_promotions(engine, piece):
                    moves.append(Move(piece, pos, sq, capture=target, data={'p':return_piece_promotion(engine,piece,'q',sq)}, flag='promotion'))
                elif len(engine.promotions[piece.color]) == 0:
                    moves.append(Move(piece, pos, sq, capture=target, data={'p':return_piece_promotion(engine,piece,'p',sq)}, flag='promotion'))
            else:
                moves.append(Move(piece, pos, sq, capture=target))

def move_warp(piece, moves, offset, pos, engine):
    board = engine.board

    for sq in range(engine.XY_TO_POS[0][0], engine.XY_TO_POS[-1][-1]+1, 1):
        if board[sq] is c.EMPTY:
            moves.append(Move(piece, pos, sq))

def move_line_no_cap(piece, moves, offset, pos, engine):
    board = engine.board
    for x in offset:
        sq = pos + x
        target = board[sq]
        i = 1
        while target is c.EMPTY:# and i<99:
            moves.append(Move(piece, pos, sq))
            i+=1
            sq = pos + x*i
            target = board[sq]

        flag = engine.can_land_on(piece, target)
        if flag == 'r':
            moves.append(Move(piece, pos, sq, data={'r':target}, flag='rescue'))

def move_line_jump(piece, moves, offset, pos, engine):
    board = engine.board
    for x in offset:
        between = False
        i = 0
        while i<99:
            i+=1
            sq = pos + x*i
            target = board[pos + x*i]
            if target is c.OFFBOARD:
                break
            elif target == c.EMPTY:
                continue
            elif between == False:
                between = True
            else:
                if engine.can_land_on(piece, target) == 'c':
                    moves.append(Move(piece, pos, sq, capture=board[sq]))
                break

def move_double_move(piece, moves, offset, pos, engine):
    board = engine.board
    
    color = c.COLOR_TO_SIGN[piece.color]     
    # pawn double move
    if (engine.POS_TO_XY[pos][1] <= 1) if color == 1 else (engine.POS_TO_XY[pos][1] >= engine.size[1] - 2):
        sq1 = pos+engine.up*color
        sq = pos+engine.up*2*color
        if board[sq1] is c.EMPTY or (hasattr(board[sq1], 'fen') and board[sq1].fen == 'i'):
            if board[sq] is c.EMPTY :
                moves.append(Move(piece, pos, sq, flag='double move'))
            elif hasattr(board[sq], 'fen') and board[sq].fen == 'i':
                moves.append(Move(piece, pos, sq, data={'r':board[sq]}, flag={'rescue','double move'}))

def move_en_passant(piece, moves, offset, pos, engine):
    board = engine.board
    if len(engine.history)==0:
        return moves
    lastmove = engine.history[-1].move
    if 'double move' in lastmove.flag and piece.is_different(lastmove.piece):
        target_square = lastmove.to
        sq = False
        if target_square == pos + 1: # check if the previous turn, the pawn landed next to our current piece
            sq = pos + offset + 1    
        elif target_square == pos - 1:
            sq = pos + offset - 1
        if sq and board[sq] is c.EMPTY:
            target = board[target_square]
            moves.append(Move(piece, pos, sq, capture=target, flag='en passant'))

def move_castling(piece, moves, offset, pos, engine):
    # you can castle when in check or passing through attacked squares. #TODO do the legality check in make_move
    board = engine.board
    if not pos in engine.perms:
        return
    for variable in offset: #{15, 19}
        if variable in engine.perms: #19 in {15, 18, 19}
            if variable>pos: # pos = 18
                i = 1
                sign = 1
            else:
                i = -1
                sign = -1
            while board[pos+i] == c.EMPTY:
                i+=sign
                if engine.is_sq_atk(pos+i, 1-piece.color): # is the sq attacked?
                    return
            target = board[variable]
            if pos+i == variable and piece.is_ally(target):

                sq = pos+2*sign #move by two?
                # allow 1 square castling
                if board[sq] is c.OFFBOARD:
                    sq = pos+sign

                if sign == 1:
                    moves.append(Move(piece, pos, sq, data=target, flag='castleK'))
                else:
                    moves.append(Move(piece, pos, sq, data=target, flag='castleQ'))

def move_foot(piece, moves, offset, pos, engine):
    board = engine.board
    for x in offset:
        sq = pos + x
        target = board[sq]
        flag = engine.can_infant_on(piece, target)
        if flag:
            if flag == 'm':
                moves.append(Move(piece, pos, sq))
            else:
                moves.append(Move(piece, pos, sq, flag=flag))
                # note, move.data is added in Chess move_enter

def atk_jump(squares, offset, pos, board):
    for x in offset:
        if not board[pos+x] is c.OFFBOARD:
            squares.add(pos+x)
    
def atk_line(squares, offset, pos, board):
    for direction in offset:
        sq = pos + direction
        while board[sq] is c.EMPTY:
            squares.add(sq)
            sq += direction
        if board[sq]: # add the blocking target to squares if it has a non false value
            squares.add(sq)

def atk_line_jump(squares, offset, pos, board):
    for direction in offset:
        between = False
        i = 0
        while i<99:
            i+=1
            sq = pos + direction*i
            target = board[pos + direction*i]
            if target is c.OFFBOARD:
                break
            elif target == c.EMPTY:
                continue
            elif between == False:
                between = True
            else:
                squares.add(sq)
                break

MOVE_TO_FUNCTION = {
    'JUMP' : move_jump,
    'LINE' : move_line,
    'JUMP_no_cap' : move_jump_no_cap,
    'JUMP_cap_only' : move_jump_cap_only,
    'WARP' : move_warp,
    'LINE_no_cap' : move_line_no_cap,
    'LINE_jump' : move_line_jump,
    'double move' : move_double_move,
    'en passant' : move_en_passant,
    'castling' : move_castling,
    'FOOT' : move_foot,
}

ATK_TO_FUNCTION = {
    'JUMP' : atk_jump,
    'JUMP_cap_only' : atk_jump,
    'LINE' : atk_line,
    'LINE_jump' : atk_line_jump,
}

class Move():
    __slots__ = ("piece", "color", "fr", "to", "capture", "data", "flag")
    
    engine = None

    def __init__(self, piece, fr, to, capture=None, flag=None, color=None, data=None): #undo=None): #, sflag=None):
        self.piece = piece
        self.color = (piece.color if color is None else color)
        self.fr = fr
        self.to = to
        self.capture = capture
        self.data = data
        
        # flag ('promotion', 'en passant', 'castling', 'double move', 'enter', 'rescue')
        if flag is None:
            self.flag = set()
        elif type(flag) is str:
            self.flag = {flag}
        else:
            self.flag = flag

    def __repr__(self):
        txt = c.FEN_TO_PIECE[self.piece.fen]
        if self.color == 0:
            txt = txt.upper()
        if self.engine:
            txt += f" {self.engine.POS_TO_A8(self.fr)}{self.engine.POS_TO_A8(self.to)}"
        else:
            return f" {self.fr}{self.to}"
        return txt
        
    def __eq__(self, other):
        if self.fr != other.fr or self.to != other.to:
            return False
        
        if 'promotion' in self.flag: # promotion
            if not 'promotion' in other.flag:
                return False
            if self.data['p'].fen != other.data['p'].fen:
                return False
        
        return True

    #Long Algebraic Notation and Standard Algebraic Notation
    def PGN(self, simplified=False):
        """ return complete notation for PGN """
        if 'castling' in self.flag:
            # Assuming king moves two squares for castling
            if self.to - self.fr == 2:
                return "O-O"
            elif self.fr - self.to == 2:
                return "O-O-O"
        
        txt = ""

        if self.piece.fen != 'p':
            txt += self.piece.fen.upper()
            
        if simplified:
            if self.capture:
                if self.piece.fen == 'p':
                    txt += self.engine.POS_TO_A8(self.fr)[0]
                txt += 'x'
            txt += self.engine.POS_TO_A8(self.to)
            return txt

            
        if self.capture:
            txt += f"{self.engine.POS_TO_A8(self.fr)}x{self.engine.POS_TO_A8(self.to)}"
        else:
            txt += f"{self.engine.POS_TO_A8(self.fr)}{self.engine.POS_TO_A8(self.to)}"
        
        if 'promotion' in self.flag and self.data and 'p' in self.data:
            txt += "=" + self.data['p'].fen.upper()
        if 'checkmate' in self.flag:
            txt += "#"
        elif 'check' in self.flag:
            txt += "+"
            
        return txt
    
    def UCI(self):
        if 'promotion' in self.flag:
            return f"{self.engine.POS_TO_A8(self.fr)}{self.engine.POS_TO_A8(self.to)}{self.data['p'].fen}"
        else:
            return f"{self.engine.POS_TO_A8(self.fr)}{self.engine.POS_TO_A8(self.to)}"
    
# TODO, add a field 'can_undo', so that you can add 'fake moves' to the history
# which cannot be undone
# add a method that only counts real moves.
class HistoryNode():
    def __init__(self, move):
        self.move = move
        self.add_perms = []
        self.remove_perms = []
        # maybe refactor to have a
        # .critical_changes = [set(ADD), set(REMOVE)] with one set to add and another to remove?
        self.critical_add = False # if True, a critical piece was added onto the list, usually on ENTER/RESCUE moves
        self.critical_remove = False # if True, a critical piece was removed, usually on ENTER/RESCUE moves and the piece is an infantry
        self.tarot = False

    def __eq__(self, other):
        return self.move == other.move
        
    def __repr__(self):
        self = self.move
        if self.engine:
            return f"{self.piece} {self.engine.POS_TO_A8(self.fr)}{self.engine.POS_TO_A8(self.to)}" # {self.flag}"
        else:
            return f"{self.piece} {self.fr}{self.to}" # {self.flag}"
