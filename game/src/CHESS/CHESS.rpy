init python:
    from fairylion.move import Move, HistoryNode
    from fairylion.engine_ import Engine
    from fairylion.evaluation import Engine_eval

    class Chess_control(Engine, Engine_eval, Chess_ui):

        PieceClass = Robot_Piece

        def __init__(self, size=(8,8), use_engine=True, **kwargs):
    
            global engine # engine only contains the minimum info for AI, it uses the basic Engine object

            self.use_engine = use_engine
            if use_engine: # and not 'engine' in globals()
                engine = Engine(size)
                Simple_Piece.engine = engine

            Move.engine = self

            Engine_eval.__init__(self)
            self.player = 0
            self.side = 'move_first'
            self.positionCount = 0

            self.move_first = set() # list of pieces the player can move first
            
            # ui stuff
            self.state = "idle" # selecting #dragging # drawing (while right click is held)

            # UI stuff
            self.terrain = renpy.random.randint(0,8000000000)
            self.bg = 'gradient'
            self.bg_board = None
            self.img_board = None

            self.wait_for_enemy = False # is it the enemy turn? ( they are actively thinking )

            for key,value in kwargs.items():
                setattr(self, key, value)

            self.setup_chess(size)
            Chess_ui.__init__(self)

        def reset_piecelist(self):
            super().reset_piecelist()
            # self.PIECELIST = dict(self.PIECELIST) # create revertable
            self.PIECELIST = {
                0: {'p': [], 'm': [], 'M': [], 'K': []},  # white pieces
                1: {'p': [], 'm': [], 'M': [], 'K': []},  # black pieces
                2: {'misc': []}
                }

        def setup_board(self, *args, **kwargs):
            super().setup_board(*args, **kwargs)
            self.board = list(self.board) # create revertable list
            self.create_board_img()

        def setup_chess(self,size:[]):
            super().setup_chess(size)
            if self.use_engine:
                engine.setup_chess(size)

        def start(self):
            # only do this when the game starts, otherwise promotions is fucked up, side is f up
            self.history = []
            global game
            game.undoable_move = -1
            self.perms = set()
            self.promotions = [[], []]
            self.move_first = set()

            self.state = 'start'
            for piece in self.get_pieces():
                piece.setup_piece()
                if piece.color == 2:
                    continue
                else:
                    if not piece.fen in {'p','i','k'}:
                        if not piece.fen in self.promotions[piece.color]:
                            self.promotions[piece.color].append(piece.fen)
            
            if self.side == 'move_first':
                if len(self.move_first) == 0:
                    self.side = 1 - self.player
                else:
                    self.side = self.player

            self.promotions = [sorted(sublist, key=lambda x: c.FEN_TO_VALUE[x], reverse=True) for sublist in self.promotions]

            if self.use_engine:
                engine.copy(self)
            self.state = 'idle'

        def drop(self, piece, pos=None, color=None) -> Robot_Piece:
            """
            @piece: Robot_Piece, string or Pilot (this creates a foot soldier)
            @pos: mandatory if piece is Pilot or str
            @color: mandatory if piece is Pilot or str
            """
            global game

            try:
                game.undoable_move = len(chess.history)
            except:
                pass

            pos = self.TO_POS(pos) if pos is not None else piece.pos
            if color is None:
                color = int(piece.islower()) if type(piece) == str else piece.color

            if self.use_engine: # update Engine
                if isinstance(piece, Pilot):
                    engine.drop('i', pos, color)
                elif type(piece) == Robot_Piece:
                    engine.drop(piece.fen, pos, color)
                elif type(piece) == str:
                    engine.drop(piece, pos, color)

            if isinstance(piece, Pilot):
                # create an INFANTRY
                new_piece = Robot_Piece('i', color=color, pos=pos, pilot=piece, id=id, engine=self)
                new_piece.pos = pos
                self.board[pos] = new_piece
                self._append_piece(new_piece)
                new_piece.pilot = piece
                new_piece.setup_piece()
            else:
                new_piece = super().drop(piece, pos, color)
            
            new_piece.deployed = True
            return new_piece

        def drop_with(self, piece, pos=None, color=None):
            """
            Similar to drop, except it also plays an anim if it's from the edge of the board.
            """
            piece = self.drop(piece, pos, color)
            fr = self.POS_TO_SXY(piece.pos, 0.5)
            # we move it one square from the edge
            if piece.x == 0:
                fr = (fr[0]-SQUARESIZE * c.INDEX_TO_SIGN[self.player], fr[1])
            elif piece.x == self.size[0] - 1:
                fr = (fr[0]+SQUARESIZE * c.INDEX_TO_SIGN[self.player], fr[1])
            elif piece.y == 0:
                fr = (fr[0], fr[1]+SQUARESIZE * c.INDEX_TO_SIGN[self.player])
            elif piece.y == self.size[1] - 1:
                fr = (fr[0], fr[1]-SQUARESIZE * c.INDEX_TO_SIGN[self.player])
            renpy.transition(dissolve, 'master')
            f_create_animation_move(piece, fr, chess.POS_TO_SXY(piece.pos, 0.5), 0.2)

    #
    #       INFANTERY STUFF
    #
        def make_move(self, move:Move, check_legality=None):
            # THIS IS TO MAKE RESCUE MOVES
            if 'rescue' in move.flag:
                for p in move.data['r'].pilot:
                    if p is not None:
                        move.piece.pilot[move.piece.pilot.index(None)] = p
                        break
            
            if check_legality is None:
                check_legality = self.use_engine

            return super().make_move(move, check_legality=check_legality)
        
        def undo(self):
            # THIS IS TO UNDO RESCUE MOVES
            move = self.history[-1].move
            if 'rescue' in move.flag:
                for p in move.data['r'].pilot:
                    if p is not None and p in move.piece.pilot:
                        move.piece.pilot[move.piece.pilot.index(p)] = None
                        break
            super().undo()

        def undo_item(self): # why not just undo(); because it's used to check legal moves etc
            # restore player health
            i = self.history[-1].move.capture
            if i:
                for pilot in i.pilot:
                    if pilot is None:
                        continue
                    if pilot.health == 0:
                        TEAM.append(pilot)
                    pilot.health += 1
                    
            super().undo()
            if self.use_engine:
                engine.copy(self)
            self.wait_for_enemy = False
            
            game.is_over = False
            
        def set_fen(self, fen, starting_new_game=None):
            if self.use_engine:
                engine.set_fen(fen)
            super().set_fen(fen)
            if starting_new_game: #or len(self.history)==0
                self.start() # be careful of removing castle perms
            if self.use_engine:
                engine.copy(self)

            self.clean_arrows()

        def get_advantage(self):
            value = 0
            for color in self.PIECELIST:
                if color >=2:
                    break
                for piece in self.get_pieces(color):
                    if piece.fen == 'k':
                        continue
                    value += piece.value * (c.INDEX_TO_SIGN[color])
                    # 0 -> 1
                    # 1 -> -1
            return value

label l_chess_undo_start:
    python:
        chess.history = []
        game.undoable_move = -1
        chess.perms = set()
        chess.promotions = [[], []]
        chess.move_first = set()

        chess.side = 'move_first'
        g.state = {'preparation'}
        chess.state = 'idle'
        chess.ui['selected'] = None
    jump l_preparation
    return