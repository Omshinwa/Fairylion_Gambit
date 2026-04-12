import fairylion.CONSTANT as c
from fairylion.simple_piece import Simple_Piece
from fairylion.move import Move

class EngineUtils():
        
    def get_pieces(self, color: int = None) -> list:
        """
        Return all pieces for the given color, or all pieces if color is None.
        """
        pieces = []
        colors = self.PIECELIST.keys() if color is None else [color]
        for c in colors:
            for category in self.PIECELIST[c]:
                pieces.extend(self.PIECELIST[c][category])
        return pieces
    
    @property
    def fen(self):
        return self.get_fen()

    def get_fen(self):
        board_fen = ""
        empty_count = 0
    
        for index, square in enumerate(self.board):

            if index % (self.size[0]+2) == 1: # NEW ROW !
                if empty_count > 0:
                    board_fen += str(empty_count)
                    empty_count = 0
                board_fen += "/"
            
            if square is c.OFFBOARD:
                continue

            if square == c.EMPTY:
                empty_count += 1
            else:
                if empty_count > 0:
                    board_fen += str(empty_count)
                    empty_count = 0
                piece_char = square.fen.lower()
                board_fen += piece_char if square.color else piece_char.upper()

        board_fen = board_fen.split('/')
        board_fen = [item for item in board_fen if item] # remove every empty element, ie when theres // in a row or empty
        board_fen.reverse()
        board_fen = '/'.join(board_fen)

        if self.side:
            turn = "b"
        else:
            turn = "w"

        castling = ""
        if 25 in self.perms and 28 in self.perms:
            castling += "K"
        if 25 in self.perms and 21 in self.perms:
            castling += "Q"
        if 95 in self.perms and 98 in self.perms:
            castling += "k"
        if 95 in self.perms and 91 in self.perms:
            castling += "q"

        if not castling:
            castling = "-"

        en_passant = "-"
        halfmove_clock = "0"
        fullmove_number = "1"

        fen = f"{board_fen} {turn} {castling} {en_passant} {halfmove_clock} {fullmove_number}"
        # rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
        return fen

    def to_pgn(self):
        """
        Returns a clean PGN string of the game history.
        """
        pgn = []
        move_number = 1
        for i, state in enumerate(self.history):
            if i % 2 == 0:
                pgn.append(f"{move_number}. {state.move.PGN()}")
                move_number += 1
            else:
                pgn.append(f"{state.move.PGN()}")
        return " ".join(pgn)

    def set_fen(self, fen):
        parts = fen.split()
        board_fen = parts[0]
        turn = parts[1] if len(parts) > 1 else "b"
        if turn.lower() == "b":
            self.side = 1
        else:
            self.side = 0
        
        rows = board_fen.split('/')

        x_length = 0
        for i in rows[0]:
            if i.isnumeric():
                x_length += int(i)
            else:
                x_length += 1

        self.setup_chess((x_length, len(rows)))

        for row_index, fen_row in enumerate(rows):
            col_index = 0
            for char in fen_row:
                if char.isdigit():
                    col_index += int(char)
                else:
                    color = 0 if char.isupper() else 1
                    piece = self.drop(char.lower(), (col_index, len(rows)-1-row_index), color)
                    col_index += 1

                    if char.lower() == 'k': # by default kings are critical
                        self.CRITICAL[color].append(piece)

        # Set up castling permissions
        castling_rights = parts[2] if len(parts) > 2 else "-"

        if castling_rights != "-":
            if 'K' in castling_rights or 'Q' in castling_rights:
                white_king = self.PIECELIST[0]['K'][0]
                white_king.range['castling'] = set()
            if 'k' in castling_rights or 'q' in castling_rights:
                black_king = self.PIECELIST[1]['K'][0]
                black_king.range['castling'] = set()
            # Set castling permissions based on FEN castling rights
            if 'Q' in castling_rights:
                self.perms.add(white_king.pos)
                white_queenside_corner = self.XY_TO_POS[0][0]
                self.perms.add(white_queenside_corner)
                white_king.range['castling'].add(white_queenside_corner)
            if 'K' in castling_rights:
                self.perms.add(white_king.pos)  # King must be on starting square
                white_kingside_corner = self.XY_TO_POS[self.size[0]-1][0]
                self.perms.add(white_kingside_corner)
                white_king.range['castling'].add(white_kingside_corner)
            if 'q' in castling_rights:
                self.perms.add(black_king.pos)  # King must be on starting square
                black_queenside_corner = self.XY_TO_POS[0][self.size[1]-1]
                self.perms.add(black_queenside_corner)
                black_king.range['castling'].add(black_queenside_corner)
            if 'k' in castling_rights:
                self.perms.add(black_king.pos)  # King must be on starting square
                black_kingside_corner = self.XY_TO_POS[self.size[0]-1][self.size[1]-1]
                self.perms.add(black_kingside_corner)
                black_king.range['castling'].add(black_kingside_corner)
    
    def drop(self, piece, pos=None, color=None, id=None):
        """
        @piece a string or Robot_Piece or Pilot (this creates a foot soldier)
        """
        pos = self.TO_POS(pos) or piece.pos

        if type(piece) == str:
            if color is None:
                if piece.islower(): # p -> black     P-> white
                    color = 1
                else:
                    color = 0
            new_piece = self.PieceClass(piece.lower(), color=color, pos=pos, movement=piece.lower(), engine=self)
        elif type(piece) == self.PieceClass:
            new_piece = piece
            new_piece.pos = pos
            color = piece.color
        else:
            raise Exception(f"type not valid, piece is of type, {type(piece)}")
        
        self.board[pos] = new_piece
        self._append_piece(new_piece)
        # self.piece_count += 1

        if color >= 2:
            return new_piece
        if new_piece.fen != 'p' and new_piece.fen != 'i' and new_piece.fen != 'k':
            if not new_piece.fen in self.promotions[color]:
                self.promotions[color].append(new_piece.fen)
                self.promotions[color] = sorted(self.promotions[color], key=lambda x: c.FEN_TO_VALUE[x], reverse=True)

        return new_piece
    
    #       :::      :::::::::  :::::::::: :::::::::  :::    :::  ::::::::  
    #      :+:       :+:    :+: :+:        :+:    :+: :+:    :+: :+:    :+: 
    #     +:+        +:+    +:+ +:+        +:+    +:+ +:+    +:+ +:+        
    #    +#+         +#+    +:+ +#++:++#   +#++:++#+  +#+    +:+ :#:        
    #   +#+          +#+    +#+ +#+        +#+    +#+ +#+    +#+ +#+   +#+# 
    #  #+#           #+#    #+# #+#        #+#    #+# #+#    #+# #+#    #+# 
    # ###            #########  ########## #########   ########   ########  
        
    def POS_TO_A8(self, pos):
        return c.INDEX_TO_LETTER[self.POS_TO_XY[pos][0]] + str(self.POS_TO_XY[pos][1]+1)
    
    def A8_TO_POS(self, string): # a6 -> 24
        return self.XY_TO_POS[ord(string[0])-97][int(string[1])-1]
    
    def TO_POS(self, pos: tuple|str|int) -> int:
        """ convert A8 or (8,8) coordinate to integer pos """
        if type(pos) == tuple:
            pos = self.XY_TO_POS[pos[0]][pos[1]]
        elif type(pos) == str:
            pos = self.A8_TO_POS(pos)
        return pos
    
    def print_board(self, board, callback):
        repr = ""
        empty_line = True
        for sq, target in enumerate(board):
            if sq % (self.size[0]+2) == 0 and not empty_line:
                repr += "\n"
                empty_line = True
            if target is c.OFFBOARD: #offboard
                continue
            else:
                repr += " " + callback(target)
                empty_line = False
        repr = repr.split("\n")[::-1] #reverse the board
        repr = [i for i in repr if i != '']
        repr = "\n".join(repr)
        return repr

    @staticmethod
    def repr_board(target):

        if target is c.EMPTY:
            return "."
        elif isinstance(target, Simple_Piece):
            if target.fen in c.FEN_TO_UNICODE[target.color]:
                return c.FEN_TO_UNICODE[target.color][target.fen]
            else:
                if target.color:
                    return target.fen
                else:
                    return target.fen.upper()
        else:
            return "?"
        
    def __repr__(self):
        return self.print_board(self.board, self.repr_board)

    def copy(self, chess): # copy the chess.board
        if chess.history:
            self.history = [chess.history[-1]]
        else:
            self.history = []

        self.up = chess.up
        self.down = chess.down
        self.left = chess.left
        self.right = chess.right
        self.side = chess.side
        self.size = chess.size
        self.setup_board((self.size[0], self.size[1])) # also set up piece tables here

        # copy castle permissions
        self.perms = set()
        for perm in chess.perms:
            self.perms.add(perm)
        # copy promotions
        self.promotions =[[], []]
        for i, color in enumerate(chess.promotions):
            for prom in color:
                self.promotions[i].append(prom)

        # copy rules
        self.goal = chess.goal
        self.stalemate_flag = chess.stalemate_flag

        # copy pieces and board
        self.board = []
        self.reset_piecelist()
        for sq in chess.board:
            if type(sq) == int:
                self.board.append(sq)
            else:
                self.board.append(c.OFFBOARD)

        for color in chess.PIECELIST:
            for category in chess.PIECELIST[color]:
                for piece in chess.PIECELIST[color][category]:
                    new_piece = Simple_Piece(piece.fen, piece.color, piece.pos, range=piece.range,
                                             movement=piece.movement, pid=piece.pid, engine=self, pilot=piece._pilot)
                    self.board[piece.pos] = new_piece
                    
                    # Manually append to avoid unwanted side-effects from _append_piece
                    if new_piece.color == 2:
                        self.PIECELIST[2]['misc'].append(new_piece)
                    else:
                        self.PIECELIST[new_piece.color][c.FEN_TO_CLASS[new_piece.fen]].append(new_piece)
                    
                    # copy critical pieces explicitly
                    for color2 in [0, 1]:
                        if piece in chess.CRITICAL[color2] and new_piece not in self.CRITICAL[color2]:
                            self.CRITICAL[color2].append(new_piece)
                            break

    def coord_to_move(self, move:str) -> Move: 
        #   move is in the form of 'b7b8q'
        #   or 'b8' with b8 being the target, q being the promotion
        #   return a Move
        if len(move) == 4 or len(move) == 5:
            for i in self.gen_moves():
                if i.fr == self.A8_TO_POS(move[:2]) and i.to == self.A8_TO_POS(move[2:]):
                    if len(move) == 4 or i.data['p'].fen == move[4]: # checking for promotions
                        return i
            for i in self.gen_moves(1-self.side):
                if i.fr == self.A8_TO_POS(move[:2]) and i.to == self.A8_TO_POS(move[2:]):
                    if len(move) == 4 or i.data['p'].fen == move[4]: # checking for promotions
                        return i
        elif len(move) == 2:
            for i in self.gen_moves():
                if i.to == self.A8_TO_POS(move):
                    return i
            for i in self.gen_moves(1-self.side):
                if i.to == self.A8_TO_POS(move):
                    return i
        return False
        raise Exception("Didnt find any move")
            
    def move(self, move:str): #move is in the form of 'b7b8'
        self.make_move(self.coord_to_move(move))

    def do_moves(self, list):
        # takes a history list as input, reproduce the move from one board to another
        for move in list:
            self.make_move(move.move)

    def eq_board(self, other):
        if self.fen != other.fen:
            return False
        if self.perms != other.perms or self.size != other.size:
            return False
        # check if the critical pieces correspond
        if len(self.CRITICAL[0])!=len(other.CRITICAL[0]):
            return False
        if len(self.CRITICAL[1]) != len(other.CRITICAL[1]):
            return False
        if self.stalemate_flag != other.stalemate_flag:
            return False
        for color in [0,1]:
            for piece_index in range(len(self.CRITICAL[color])):
                if self.CRITICAL[color][piece_index].pid != other.CRITICAL[color][piece_index].pid:
                    return False
        return True
        
    def is_sync(self):
        # check if the number of pieces is the same on PIECELIST and .board
        pieces = 0
        for sq in self.board:
            if isinstance(sq, Simple_Piece):
                pieces += 1
        return len(self.get_pieces()) != pieces
    
    def is_sync_deep(self): # check if the pieces are the same
        for piece in self.get_pieces():
            if self.board[piece.pos] != piece:
                return f"{piece} is misplaced"
        return self.is_sync()

    
    # to find a NEUTRAL piece, write the letter twice ie QQ for a grey queen
    # get('Q 2')
    def get(self, target:str|int):
        if type(target) is int:
            for piece in self.get_pieces():
                if piece.pid == target:
                    return piece
        elif type(target) is str:
            target_fen = target.split(' ')[0]
            target_index = 1
            if len(target.split(' ')) > 1:
                target_index = int(target.split(' ')[1])
            i = 1
            if len(target_fen) == 2 and target_fen[0] == target_fen[1]:
                color = 2
                target_fen = target_fen[0]
            elif target_fen.isupper():
                color = 0
            else:
                color = 1
            for piece in self.get_pieces(color):
                if piece.fen == target_fen.lower():
                    if i == target_index:
                        return piece
                    else:
                        i+=1
        else: # its a pilot?
            for piece in self.get_pieces():
                for pilot in piece._pilot:
                    if pilot and target == pilot:
                        return piece
        return None
    
    def get_pilot(self, pilot_name:str):
        for piece in self.get_pieces():
            if pilot_name in piece._pilot:
                return piece
        return None

    def perftest(engine, depth):

        def perft(engine, depth):
            if depth == 0:
                engine.positionCount += 1
                return

            moves = engine.gen_moves()
            for move in moves:
                if(engine.make_move(move) == False):
                    continue
                perft(engine, depth-1)
                engine.undo()

            return engine.positionCount
    
        print(f"Starting Test To Depth: {depth}")
        engine.positionCount = 0
        moveNum = 0
        moves = engine.gen_moves()
        for move in moves:
            if(engine.make_move(move) == False):
                continue
            moveNum += 1
            cumnodes = engine.positionCount
            perft(engine, depth-1)
            engine.undo()
            oldnodes = engine.positionCount - cumnodes
            print(f"move: {moveNum} {move} {oldnodes}")
        
        print(f"Test Complete : {engine.positionCount} leaf nodes visited")
        return