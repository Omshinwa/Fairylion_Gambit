OFFBOARD = False
EMPTY = 1

INDEX_TO_SIGN = {0:1, 1:-1, 2:0}
SIGN_TO_INDEX = {1:0, -1:1}

MAX_SCORE = 999999

INDEX_TO_COLOR = {0:'white', 1:'black', 2:'grey'}

FEN_TO_VALUE = {'p':100, 'n':300, 'b':300, 'r':500, 'q':900, 'k':9900, 'g':300, 'c':300, 'i':20}
PIECE_TO_FEN = { 'pawn':'p', 'knight':'n', 'bishop':'b',
'rook':'r', 'queen':'q', 'king':'k', 'infantry':'i', 'ghost':'g', 'cannon':'c', 'mann':'m', 'fairylion':'f', 'jester':'j', 'dragon':'d', 'sentinel':'s'}
FEN_TO_PIECE = { value:key for key, value in PIECE_TO_FEN.items() }
FEN_TO_TYPE = {'p':'^', 'n':'L', 'b':'x', 'r':'+', 'q':'*', 'k':'#', 'g':'L', 'c':'x', 'i':'i'}

FEN_TO_CLASS = {'p':'p', 'n':'m', 'b':'m', 'r':'M', 'q':'M', 'k':'K', 'g':'m', 'c':'m', 'i':'m'}

FEN_TO_UNICODE = {0:{'k':'♔','q':'♕', 'r':'♖', 'b':'♗', 'n':'♘', 'p':'♙'}, 1:{'k':'♚','q':'♛', 'r':'♜', 'b':'♝', 'n':'♞', 'p':'♟'}, 2:{}}

INDEX_TO_LETTER = ['a','b','c','d','e','f','g','h','i','j','k']


# class PieceEnum:
#     def __init__(self, pieces):
#         for i, char in enumerate(pieces):
#             setattr(self, char, i)
#         self._pieces = pieces
#         self._int_to_char = {i: char for i, char in enumerate(pieces)}
    
#     def from_int(self, value):
#         return self._int_to_char[value]

# piece_chars = ['EMPTY',
#                'OBSTACLE'
#                'wP', # white pawn
#                'bP', # black pawn
#                'gP', # gray pawn
#                'wP_d', # pawn double move
#                'bP_d',
#                'wN', # KNIGHT
#                'bN',
#                'gN', # this is also grey ghost
#                'wB', # BISHOP
#                'bB',
#                'gB',
#                'wR',
#                'bR',
#                'gR', 
#                'wQ', 
#                'bQ', 
#                'gQ', 
#                'wK', # NO CASTLE
#                'bK', 
#                'wKc', # CASTLE
#                'bKc', 
#                'wKi', # INDIAN CASTLE
#                'bKi', 
#                'wKh', # KING OF THE HILL
#                'bKh', 
#                'wG',
#                'bG',
#                'wI',
#                'bI',
#                'gI',
#                ]
# PIECE = PieceEnum(piece_chars)