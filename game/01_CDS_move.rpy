# Creator-Defined Statement for move command
# Syntax: move {who} {where}
# Example: move kallen 1 toward lelouch
#          move kallen a8
#          move lelouch 2 left

# Move by square notation:
# move kallen a8
# move lelouch "d3"

# Move by directional offset (left, right, up, down):
# move kallen 2 right          # Move kallen 2 squares to the right
# move kallen 1 left           # Move kallen 1 square to the left
# move lelouch 3 up            # Move lelouch 3 squares up
# move lelouch 1 down          # Move lelouch 1 square down

# Move toward/away from another piece:
# move kallen 1 toward lelouch  # Move kallen 1 square toward lelouch
# move kallen 2 away lelouch    # Move kallen 2 squares away from lelouch

python early:

    DIRECTION_OFFSETS = {
        'left': (-1, 0),
        'right': (1, 0),
        'up': (0, 1),
        'down': (0, -1),
    }

    def _move_resolve_dest(who_val, where_tokens):
        """Resolve destination position from parsed tokens. Returns (piece, move_str) or (None, None)."""
        if isinstance(who_val, Robot_Piece):
            piece = who_val
        else:
            piece = chess.get(who_val)
        if piece is None:
            renpy.say(None, f"ERROR: ({who_val} not found)")
            return None, None

        tokens = where_tokens

        if not tokens:
            renpy.say(None, "ERROR: No destination specified")
            return None, None

        # Square notation like 'a8', 'd3'
        if len(tokens) == 1 and len(str(tokens[0])) == 2:
            try:
                dest_pos = chess.A8_TO_POS(str(tokens[0]).lower())
                return piece, chess.POS_TO_A8(piece.pos) + chess.POS_TO_A8(dest_pos)
            except:
                pass

        # Directional: amount + direction [+ target]
        try:
            amount = int(tokens[0])
        except (ValueError, TypeError):
            renpy.say(None, f"ERROR: Invalid amount '{tokens[0]}'")
            return None, None

        if len(tokens) < 2:
            renpy.say(None, "ERROR: Direction required")
            return None, None

        direction = str(tokens[1]).lower()

        if direction in ('toward', 'away'):
            if len(tokens) < 3:
                renpy.say(None, f"ERROR: '{direction}' requires a target")
                return None, None

            target_val = tokens[2]
            target_piece = target_val if isinstance(target_val, Robot_Piece) else chess.get(target_val)

            if target_piece is None:
                renpy.say(None, f"ERROR: ({target_val} not found)")
                return None, None

            from_xy = chess.POS_TO_XY[piece.pos]
            to_xy   = chess.POS_TO_XY[target_piece.pos]
            dx = 0 if from_xy[0] == to_xy[0] else (1 if to_xy[0] > from_xy[0] else -1)
            dy = 0 if from_xy[1] == to_xy[1] else (1 if to_xy[1] > from_xy[1] else -1)
            if direction == 'away':
                dx, dy = -dx, -dy
            new_x = max(0, min(from_xy[0] + dx * amount, chess.size[0] - 1))
            new_y = max(0, min(from_xy[1] + dy * amount, chess.size[1] - 1))

        elif direction in DIRECTION_OFFSETS:
            xy = chess.POS_TO_XY[piece.pos]
            dx, dy = DIRECTION_OFFSETS[direction]
            new_x = max(0, min(xy[0] + dx * amount, chess.size[0] - 1))
            new_y = max(0, min(xy[1] + dy * amount, chess.size[1] - 1))

        else:
            renpy.say(None, f"ERROR: Invalid direction '{direction}'. Use: left, right, up, down, toward, away")
            return None, None

        try:
            dest_pos = chess.XY_TO_POS[new_x][new_y]
        except:
            renpy.say(None, f"ERROR: Destination ({new_x}, {new_y}) out of bounds")
            return None, None

        return piece, chess.POS_TO_A8(piece.pos) + chess.POS_TO_A8(dest_pos)


    def parse_move_statement(l):
        who = l.simple_expression()
        where_tokens = []
        while not l.eol():
            tok = l.simple_expression()
            if tok is not None:
                where_tokens.append(tok)
            else:
                break
        return (who, where_tokens)


    _MOVE_KEYWORDS = frozenset({'left', 'right', 'up', 'down', 'toward', 'away'})

    def execute_move_statement(parsed):
        who_expr, where_tokens = parsed
        who_val = renpy.python.py_eval(who_expr)
        evaled_tokens = [
            t if t in _MOVE_KEYWORDS else renpy.python.py_eval(t)
            for t in where_tokens
        ]
        piece, move = _move_resolve_dest(who_val, evaled_tokens)
        if move is not None:
            renpy.call('l_move_piece', move)


    renpy.register_statement("move",
        parse=parse_move_statement,
        execute=execute_move_statement)
