init -1 python:

    class NoInertiaAdjustment(renpy.display.behavior.Adjustment, object):
        """A tiny wrapper around Adjustment that disables inertia."""
    
        def inertia(self, amplitude, time_constant, st):
            self.player_changed = True
            self.end_animation()
        
        def recenter(self, time=0.5):
            amp = self._range/2 - self.value
            if not amp: amp = 0.0001
            # we do a small offset because animate(0) would cancel any previous animation()
            # doing
            # ```animate(10) 
            #    animate(0). ```
            # used to not do anything
            self.animate(amp, time, self.inertia_warper)

#    █████████    █████████   ██████   ██████ ██████████ ███████████     █████████  
#   ███░░░░░███  ███░░░░░███ ░░██████ ██████ ░░███░░░░░█░░███░░░░░███   ███░░░░░███ 
#  ███     ░░░  ░███    ░███  ░███░█████░███  ░███  █ ░  ░███    ░███  ░███    ░███ 
# ░███          ░███████████  ░███░░███ ░███  ░██████    ░██████████   ░███████████ 
# ░███          ░███░░░░░███  ░███ ░░░  ░███  ░███░░█    ░███░░░░░███  ░███░░░░░███ 
# ░░███     ███ ░███    ░███  ░███      ░███  ░███ ░   █ ░███    ░███  ░███    ░███ 
#  ░░█████████  █████   █████ █████     █████ ██████████ █████   █████ █████   █████
#   ░░░░░░░░░  ░░░░░   ░░░░░ ░░░░░     ░░░░░ ░░░░░░░░░░ ░░░░░   ░░░░░ ░░░░░   ░░░░░ 
    
    class Chess_camera(): #(NoRollback)
        # handles zoom/camera movement/pan etc
        # example usage:
        # chess_camera.zoom = 1.1
        # chess_camera.center_on('a8')
        def __init__(self, chess, **kwargs):
            global chess_camera
            if chess.use_engine:
                chess_camera = self

            self.player_changed = False # used to check if the player moved/zoomed the board
            self.possible_zooms = [0.07,0.10,0.15,0.22,0.31,0.39,0.5,0.61,0.75,0.85,0.95,1,1.05,1.15,1.25,1.5,1.75,2,2.5,3,3.5,4]
            self.xadj = NoInertiaAdjustment(range=1920, value=1920/2)
            self.yadj = NoInertiaAdjustment(range=1080, value=1080/2)
            self._zoom = 18 - max(chess.size[1], chess.size[0]) # max size
            if 'preparation' in g.state:
                self._zoom -= 2
            if prefs.layout == 'portrait':
                self._zoom += 2
            
            self.chess = chess # keep a reference to the original Chess
        
        def __repr__(self):
            return f"zoom: {self.zoom} x: {self.xadj.value} y: {self.yadj.value}"

        @property
        def zoom(self):
            return self.possible_zooms[self._zoom]
        @zoom.setter
        def zoom(self, new_zoom):
            if new_zoom > self.zoom:
                while new_zoom > self.zoom:
                    self.viewport_zoom_in()
            elif new_zoom < self.zoom:
                while new_zoom < self.zoom:
                    self.viewport_zoom_out()
            self.player_changed = False

        @property
        def x(self):
            # This is the relative position where
            # x == 0 means its centered
            return int(self.xadj.value)
        @x.setter
        def x(self, value):
            self.xadj.value = value

        @property
        def y(self):
            # This is the relative position where
            # y == 0 means its centered
            return int(self.yadj.value)
        @y.setter
        def y(self, value):
            self.yadj.value = value

        def viewport_zoom_in(self):
            self.player_changed = True
            self._zoom = min(len(self.possible_zooms)-1, self._zoom+1)
            
        def viewport_zoom_out(self):
            self.player_changed = True
            self._zoom = max(0, self._zoom-1)

        def move(self, x, y, time=0.5):
            amp_x = -x if x else 0.0001
            amp_y = -y if y else 0.0001
            self.xadj.animate(amp_x, time, self.xadj.inertia_warper)
            self.yadj.animate(amp_y, time, self.yadj.inertia_warper)

        def move_abs(self, x, y, time=0.5):
            # set the position
            amp_x = -x - self.xadj.value + self.xadj._range/2
            amp_y = -y - self.yadj.value + self.yadj._range/2
            
            if not amp_x: amp_x = 0.0001
            if not amp_y: amp_y = 0.0001
            
            self.xadj.animate(amp_x, time, self.xadj.inertia_warper)
            self.yadj.animate(amp_y, time, self.yadj.inertia_warper)

        def center_on(self, pos=None, time=0.5):
            # TODO? make it so when it center on a square at the edge of the board
            # it doesnt completely move (otherwise a lot of the board is off view?)
            global AUTO_CENTER_ON_SPEAK_CHAR_BATTLEFIELD
            if pos is None:
                self.xadj.recenter(time)
                self.yadj.recenter(time)
                self.player_changed = False
                AUTO_CENTER_ON_SPEAK_CHAR_BATTLEFIELD = False
                return
            pos = self.chess.TO_POS(pos)
            sq = self.chess.POS_TO_SXY(pos)
            a8 = self.chess.POS_TO_SXY((0,self.chess.size[1]-1))
            h1 = self.chess.POS_TO_SXY((self.chess.size[0]-1,0))
            if a8[0] == 0: # find the corner with the max size of the board
                corner = h1
            else:
                corner = a8

            move_x = (sq[0] - corner[0]/2)
            move_y = (sq[1] - corner[1]/2) / 2 # doing /2 because idk how to make it scale
            # so it doesnt do too much if it's in the edge

            target = [-move_x*self.zoom, -move_y*self.zoom]

            self.move_abs(target[0], target[1], time)

        def reset_dezoom_view(self, time=0.5):
            "dezoom slightly so we can see the board and text"
            self._zoom = 18 - max(chess.size[1], chess.size[0]) # max size
            self.center_on()

        def center_if_changed(self):
            if not AUTO_CENTER_ON_SPEAK_CHAR_BATTLEFIELD and chess.ui['camera'].player_changed:
                print("trigerred center_if_changed ")
                self.reset_dezoom_view()

        def board_offset(self):
            """
            output the offset of the chessboard from top left
            """
            x = 1920-self.x - self.chess.size[0]/2*SQUARESIZE
            y = 1080-self.y - self.chess.size[1]/2*SQUARESIZE
            return (absolute(x),absolute(y))

        def board_offset_center(self):
            """
            output the offset of the chessboard's center
            """
            x = 1920-self.x*2
            y = 1080-self.y*2
            return (absolute(x/2),absolute(y/2))

        def pos_to_trans(self, pos):
            """
            return the xy coords (relative to the full screen) of a sq
            """
            x, y = self.board_offset_center()
            x += 1920/2
            y += 1080/2
            x2, y2 = self.chess.POS_TO_SXY(pos, .5)
            x2 -= (SQUARESIZE * chess.size[0])/2
            y2 -= (SQUARESIZE * chess.size[1])/2
            x += x2 * self.zoom
            y += y2 * self.zoom
            return Transform(pos=(position(x), position(y)), anchor=(.5,.5), zoom=self.zoom)

#           █████                                  █████  ██             ███   ██ █████
#          ░░███                                  ░███░  ███            ░░░   ███░░░███
#   ██████  ░███████    ██████   █████   █████    ░███  ░░░  █████ ████ ████ ░░░   ░███
#  ███░░███ ░███░░███  ███░░███ ███░░   ███░░     ░███      ░░███ ░███ ░░███       ░███
# ░███ ░░░  ░███ ░███ ░███████ ░░█████ ░░█████    ░███       ░███ ░███  ░███       ░███
# ░███  ███ ░███ ░███ ░███░░░   ░░░░███ ░░░░███   ░███       ░███ ░███  ░███       ░███
# ░░██████  ████ █████░░██████  ██████  ██████  ██░█████     ░░████████ █████     █████
#  ░░░░░░  ░░░░ ░░░░░  ░░░░░░  ░░░░░░  ░░░░░░  ░░ ░░░░░       ░░░░░░░░ ░░░░░     ░░░░░ 
                                                                                     
    class Chess_ui():
        def __init__(self, **kwargs):
            self.ui = {"moves":{}, "arrows":set(), 'drawing':None, 'inspected':None, 'selected':None}
            self.ui['camera'] = Chess_camera(self)
            self.ui['animation_move'] = None # move for the animation

            self.bg_board_pixel_coord = (0,0)

        def clean_moves(self):
            self.ui["moves"] = {}

        def clean_arrows(self):
            self.ui["arrows"] = set()

        def create_board_img(self):
            x = self.size[0]
            y = self.size[1]
            sq_list = []
            white_or_black = 0
            for i in range(x*y):
                # if prefs.style.board is None and self.bg and white_or_black: # si on a un BG, on ignore les cases noires
                #     if x%2==0 and i%x==x-1:
                #         continue
                #     white_or_black = 1 - white_or_black
                #     continue
                sq_list.append(((i%x)*SQUARESIZE, int(i/x)*SQUARESIZE))
                if white_or_black:
                    sq_list.append(f"skin/square/square {prefs.style.board} black.webp")
                else:
                    sq_list.append(f"skin/square/square {prefs.style.board} white.webp")
                if x%2==0 and i%x==x-1:
                    continue
                white_or_black = 1 - white_or_black
            img = Composite( (SQUARESIZE*x, SQUARESIZE*y), *sq_list, subpixel=True)
            img = Transform(img)
            self.img_board = img
            return img

        def is_move_legal_ui(self, move:Move):
            if move is None: # it's possible the UI sends NONE moves, those are illegal moves but still shown on board
                return False
            if self.use_engine and len(self.history) == 0 and chess.side == chess.player:
                if not self.move_first or move.piece in self.move_first:
                    # if self.move_first is empty (player is starting) or it's not empty and player has to move a piece w initiative skill
                    return self.make_move(move, check_legality=self.use_engine)
                else:
                    return False
            else:
                return self.make_move(move, check_legality=self.use_engine)
            
        def t_layer(self, pos:str):
            # return a transform to put a displayable at the POS square (inside the frame of s_chessboard_main)
            sq = self.POS_TO_SXY(pos)
            h1 = self.POS_TO_SXY((self.size[0]-1,0))
            move_x = sq[0] - h1[0]/2
            move_y = sq[1] - h1[1]/2
            return Transform(pos=(position(move_x,.5), position(move_y,.5)), anchor=(.5,.5), zoom=self.ui['camera'].zoom)

        # Return coordinates with the TOP LEFT BOARD as origin
        def POS_TO_SXY(self, pos, offset=0):
            if type(offset) is float or type(offset) is int:
                offset = (offset, offset)
            pos = self.TO_POS(pos)
            return (absolute((self.POS_TO_XY_POV(pos)[0]+offset[0])*SQUARESIZE), absolute((self.size[1]-1-self.POS_TO_XY_POV(pos)[1]+offset[1])*SQUARESIZE))
        
        # bug? its counting from bottom up for Y?
        def POS_TO_XY_POV(self, pos):
            # return x y based on the perspective of the player
            x = self.POS_TO_XY[pos][0]
            y = self.POS_TO_XY[pos][1]
            if self.player == 0:
                return (x,y)
            else:
                return (self.size[0] - x - 1,self.size[1] - y - 1)

        def real_dist_between_two_pos(self, pos1, pos2):
            return math.sqrt((self.POS_TO_XY[pos1][0]-self.POS_TO_XY[pos2][0])**2 + (self.POS_TO_XY[pos1][1]-self.POS_TO_XY[pos2][1])**2)

        def prep_can_drop_here(self, element, pos, req_true = False):
            target = self.board[pos]

            if element == target:
                return True
            if element == c.EMPTY:
                return True

            if isinstance(element, Pilot):
                if chess.POS_TO_XY_POV(pos)[1] > 1:
                    return False

                if chess.POS_TO_XY_POV(pos)[1] == 1 and '^' in element.can_drive: # and also still have pawns in reserve
                    return True
                if chess.POS_TO_XY_POV(pos)[1] == 0:
                    if target is c.EMPTY:
                        return True
                    if type(target) is Robot_Piece:
                        if target.fen == 'i':
                            return True
                        if target.type in element.can_drive:
                            return True
                    return False
                
            # select unmovable piece, only possible if Pilot can drive it
            if (isinstance(element, Robot_Piece) and element.unmovable) or (isinstance(target, Robot_Piece) and target.unmovable):
                return False

            if isinstance(element, Robot_Piece):
                # if it's an infantry, can go anywhere
                if element.fen == 'i':
                    # only if it cannot drive a pawn, cannot go to rank 1
                    if '^' not in element._pilot[0].can_drive and self.POS_TO_XY_POV(pos)[1] == 1:
                        return False
                    if req_true:
                        return True
                    return self.prep_can_drop_here(target, element.pos, True)
                # if it's a pawn, cannot go if there's already a normal robot):
                if element.type == '^':
                    if req_true:
                        return True
                    return self.prep_can_drop_here(target, element.pos, True)
                # if its a normal robot, cant be above the bottom row
                if self.POS_TO_XY_POV(pos)[1] == 1:
                    return False
                else:
                    if isinstance(target, Robot_Piece) and target.fen == 'i':
                        if element.type in target.pilot.can_drive:
                            return True
                        else:
                            return False
                    else:
                        return True

        def get_drag_list(self):
            # return get_pieces() sorted by IDs
            # issue was, when you select an infantry that has Enter_empty moves, the make_move and undo would change
            # the order of get_pieces(), which would make the dragging pieces change
            return sorted(self.get_pieces(), key=lambda piece: -piece.y)
            # return sorted(self.get_pieces(), key=lambda piece: piece.pid)

        # used in l_move_piece when calling an impossible move during cutscene
        # allow for fantasy moves in cutscenes, only for l_move_piece(A8H8) format
        def create_move_cutscene(self, a8h8:str) -> Move:
            fr = self.TO_POS(a8h8[:2])
            to = self.TO_POS(a8h8[2:])
            board = self.board
            piece = board[fr]
            target = board[to]

            move = Move(piece, fr, to)

            if piece.fen == 'i':
                moves = [];
                piece.get_move_of_instruction(moves, 'FOOT', [to-fr], self)
                move = moves[0]

            return move;

        def drop_with(self, piece, pos=None, color=None, direction=None):
            """
            Similar to drop, except it also plays an anim if it's from the edge of the board.
            """
            piece = self.drop(piece, pos, color)
            fr = self.POS_TO_SXY(piece.pos, PIECE_ALIGNMENT())
            # we move it one square from the edge
            if direction == 'right' or piece.x == 0:
                fr = (fr[0]-SQUARESIZE * c.COLOR_TO_SIGN[self.player], fr[1])
            elif direction == 'left' or piece.x == self.size[0] - 1:
                fr = (fr[0]+SQUARESIZE * c.COLOR_TO_SIGN[self.player], fr[1])
            elif direction == 'down' or piece.y == 0:
                fr = (fr[0], fr[1]+SQUARESIZE * c.COLOR_TO_SIGN[self.player])
            elif direction == 'up' or piece.y == self.size[1] - 1:
                fr = (fr[0], fr[1]-SQUARESIZE * c.COLOR_TO_SIGN[self.player])
            renpy.transition(dissolve, 'master')
            f_create_animation_move(piece, fr, chess.POS_TO_SXY(piece.pos, PIECE_ALIGNMENT()), 0.2)
        
        def remove_with(self, piece, direction=None, time=0.2):
            piece = get(piece)
            to = self.POS_TO_SXY(piece.pos, PIECE_ALIGNMENT())
            if direction == 'left' or piece.x == 0:
                to = (to[0]-SQUARESIZE * c.COLOR_TO_SIGN[self.player], to[1])
            elif direction == 'right' or piece.x == self.size[0] - 1:
                to = (to[0]+SQUARESIZE * c.COLOR_TO_SIGN[self.player], to[1])
            elif direction == 'up' or piece.y == 0:
                to = (to[0], to[1]+SQUARESIZE * c.COLOR_TO_SIGN[self.player])
            elif direction == 'down' or piece.y == self.size[1] - 1:
                to = (to[0], to[1]-SQUARESIZE * c.COLOR_TO_SIGN[self.player])
            f_create_animation_move(piece, chess.POS_TO_SXY(piece.pos, PIECE_ALIGNMENT()), to, time)
            self.remove_piece(piece)
            renpy.transition(dissolve, 'master')
