# Playtesting Fairylion Gambit with an AI agent (RenForge)

Notes for an AI agent that drives the game through the RenForge MCP. Tested 2026-11-24 with RenForge 0.7.6 and Ren'Py 8.6.1 on a Retina Mac.

## Launch

`renforge_launch(project_path=<this folder>, version="8.6.1", savedir="temporary")`, then poll `renforge_launch_status`.

- `savedir="temporary"` keeps the real saves (`game/saves`, `~/Library/RenPy/...`) untouched.
- The first launch downloads the 8.6.1 SDK (about 1 min). The main menu is ready about 2 min after launch.
- `renforge_jump(target="l_map_0_0", version="8.6.1", savedir="temporary")` restarts the game process at a label in about 6 s. All state is reset: `g.progress` is 0 and `g.items['undo']` is 0, because the map screen's +3 is skipped.
- Finish with `renforge_stop`, which removes the files RenForge injected into `game/`.

## Input that works

- **Pieces and moves:** `renforge_click_element(element_id="piece_e7")`, then `element_id="move_e3"`.
- **Buttons** (menu, map flag, say screen): mouse clicks don't work, because they land in the wrong place on a Retina screen and still return ok. Use `renforge_hover_element(element_id=...)` with ids from `renforge_list_ui_elements`, then `renforge_eval("renpy.queue_event('button_select')")`.
- **Dialogue:** `renforge_advance` works before a battle starts. After you click a piece, keyboard focus stays on that piece, so `advance` does nothing on in-battle dialogue. Hover the `say` screen's button first, then use `renforge_eval("renpy.queue_event(['dismiss','button_select'])")`.
- **Console:** `renforge_send_input` can't send Shift+O, letters or modifier keys. You rarely need the console because `renforge_eval` does the same job. If you do: open it with `renpy.queue_event('console')` and close it with `renpy.queue_event('console_exit')`. Don't use `send_input(key="esc")`, which opens the Save menu.
- **Debug overlay ("2" key):** `renpy.queue_event('K_2')`. Note that toggling it resets `g.items['undo']` to 3.

## Reading and setting state

- Read dotted names with eval, for example `repr((g.progress, g.money, g.items, g.state, chess.side))`. `renforge_get_var` rejects dotted names.
- Set nested values with eval: `g.items.__setitem__('undo', 9)`, then `renpy.restart_interaction()` to redraw the HUD. `renforge_set_var("g.items['undo']", 9)` returns ok but creates a junk variable with that literal name.
- `renforge_eval` takes expressions only. It fails on `list(`, and a top-level list comprehension fails with `__renpy__list__` not defined. The same comprehension wrapped in `repr((...))` worked, and a tuple of calls always works.
- Change the position: `(chess.set_fen("..."), engine.copy(chess))`, then `renpy.restart_interaction()` to redraw the board.
- Board readout (worked as written): `repr(([(p.fen, chess.POS_TO_A8(p.pos)) for p in chess.get_pieces(0)], [str(m) for m in chess.history[-2:]], game.is_over))`. Use `get_pieces(1)` for Black.
- Wait for the AI's reply: `renforge_wait_until(expr="chess.side == 1 and not chess.wait_for_enemy and 'battle' in g.state and chess.state == 'idle'")`.

## Don't

- `renforge_control(action="reload_script")` (and Shift+R) works since 2026-11-24, when Cubism SDK for Native R5 (Core 06.00.0001) was installed into the user's SDK and into `~/.cache/renforge/sdks/8.6.1/lib/py3-mac-universal/`. Without a Cubism Core 5.3+ library next to the executable, the game segfaults on reload: the first Live2D load fails, but `renpy.gl2.live2dmodel.load()` returns True on later calls, so the rook rig calls a missing Cubism function. If RenForge's SDK cache is wiped, copy `libLive2DCubismCore.dylib` back from the user's SDK `lib/py3-mac-universal/`.
- Don't post raw pygame events through eval unless needed. A KEYUP without `repeat=False` crashes the game (Ren'Py reads `ev.repeat`).
- Don't flag "winning 0-0 goes to Mission 0-2" as a bug. Mission 0-1 was cut on purpose.

## Why not computer use

Tested the same day, it doesn't fit agent debugging of this game:
- A game started with `renpy.sh` can't be granted at all. Started with `renpy.app/Contents/MacOS/renpy <project>` it can.
- In background mode, screenshots work, but key presses never reach the game and clicks land in the wrong place.
- Full-screen control works (Shift+O and the console included), but it takes over the user's screen.
- A manual launch writes into the real `game/saves` even with `RENPY_PATH_TO_SAVES` set.
