# Move CDS Documentation

## Overview
The `move` statement is a Creator-Defined Statement (CDS) for Ren'Py that allows you to easily move chess pieces on the board in your story sequences.

## Syntax
```
move {who} {where}
```

## Parameters

### `{who}` - The piece to move
Can be any of:
- **String literal**: `"kallen"` - references a pilot or piece name (uses `chess.get()`)
- **Variable**: `my_robot` - references a robot_piece variable
- **Pilot reference**: Direct pilot object reference

Examples:
```renpy
move "kallen" 1 toward lelouch
move lelouch a8
move my_piece 2 right
```

### `{where}` - The destination

#### Square Notation
Specify the target square directly using chess notation (column + row):
```renpy
move kallen a8
move lelouch d3
```

#### Directional Movement
Move relative to current position using direction keywords:

**Basic Directions**: `left`, `right`, `up`, `down`
```renpy
move kallen 2 right         # Move 2 squares to the right
move lelouch 1 left         # Move 1 square to the left
move kallen 3 up            # Move 3 squares up
move lelouch 1 down         # Move 1 square down
```

**Relative to Target**: `toward`, `away`
```renpy
move kallen 1 toward lelouch    # Move 1 square toward lelouch
move kallen 2 away lelouch      # Move 2 squares away from lelouch
```

## Behavior

1. **Piece Resolution**: The `{who}` parameter is resolved using `chess.get()`:
   - Searches for pilots by name
   - Searches for pieces by FEN notation
   - Direct piece references are converted to string and looked up

2. **Destination Calculation**:
   - Square notation uses direct conversion via `chess.A8_TO_POS()`
   - Directional movement clamps to board boundaries
   - "toward"/"away" calculate the unit vector direction from source to target

3. **Move Validation**:
   - Searches valid generated moves (`chess.gen_moves()`)
   - Only executes if a valid move exists to the destination
   - Prints error if no valid move found

4. **Animation**:
   - Uses `renpy.call('l_move_piece', move)` to execute
   - Automatically creates animation and updates board state

## Error Handling

The move statement will print error messages for:
- `ERROR: ({who} not found)` - Piece couldn't be found
- `ERROR: No valid move for {piece} to {square}` - Destination is invalid for this piece
- `ERROR: Invalid amount '{value}'` - Amount parameter isn't an integer
- `ERROR: Direction required` - Got amount but no direction
- `ERROR: '{direction}' requires a target` - 'toward'/'away' used without target piece
- `ERROR: Invalid direction '{direction}'` - Unknown direction keyword
- `ERROR: Destination ({x}, {y}) out of bounds` - Calculated position off the board

## Implementation Details

The CDS works by:
1. Registering a custom parser with `renpy.register_statement("move", ...)`
2. Creating a `MoveStatement` class that extends `renpy.ast.Node`
3. Parsing arguments as simple expressions via the Ren'Py lexer
4. Computing the destination position based on parameters
5. Finding valid moves using `chess.gen_moves()`
6. Executing via `l_move_piece` which handles animation and board updates

## Examples

### Simple movement
```renpy
move kallen a8
```

### Directional movement
```renpy
move lelouch 2 left
move kallen 3 up
```

### Movement toward another piece
```renpy
move kallen 1 toward lelouch
pause 1.0
move lelouch 1 away kallen
```

### Complex battle sequence
```renpy
label chess_scene():
    move kallen 2 toward lelouch
    pause 0.5
    move lelouch 1 right
    pause 0.5
    move kallen 1 toward lelouch
    pause 0.5
    move lelouch 2 away kallen
    return
```

## Notes

- The statement automatically handles board visualization if you have `f_create_animation_move()` set up
- Movement must be valid according to piece movement rules (handled by `chess.gen_moves()`)
- The board boundaries are automatically respected (clamping is applied)
- If pieces are already adjacent and trying to move toward them, it will fail validation (as expected from your use case)
