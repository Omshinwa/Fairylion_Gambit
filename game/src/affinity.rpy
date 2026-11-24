# AFFINITY
# Every pair of characters has an affinity. Lelouch's affinity with a pilot is that pilot's
# Trust (pilot.trust, see src/loyalty.rpy), so both go through the same functions here.
# Story mode only: roguelite has no social side.
#
#   +1  for every pair of pilots who win a battle together
#   +3  more if they sat in the same CHESSMAN (two-seat robot)
#
# Not done yet: +3 for sharing a room on the ship, social discussions are triggered at high affinity,
# also allows to drive a Queen


default AFFINITY = {} # (id_a, id_b) sorted -> int, lelouch pairs are stored as Trust instead

# Affinities a new story starts with (the pair's order doesn't matter), applied by affinity_reset()
define AFFINITY_START = {
    # kallen (see Characters in ai_prompt/prompt.md)
    ('kallen', 'stanley'): -2,
    ('kallen', 'china'): -2,
    ('kallen', 'cc'): -2,
    ('kallen', 'kaworu'): 2,
}

define AFFINITY_FIGHT = 1
define AFFINITY_SEAT = 3

init python:
    def affinity_counts(pilot):
        """Only named characters get affinity (generic pilots have no identity)."""
        return isinstance(pilot, Pilot) and pilot.id != 'generic' and pilot.id in character.PILOTLIST

    def _affinity_key(a, b):
        return tuple(sorted((a.id, b.id)))

    def affinity_reset():
        """A new story starts (l_intro): every affinity goes back to AFFINITY_START."""
        AFFINITY.clear()
        for pair, value in AFFINITY_START.items():
            AFFINITY[tuple(sorted(pair))] = value

    def get_affinity(a, b):
        if a is b:
            return 0
        if a.id == 'lelouch':
            return b.trust
        if b.id == 'lelouch':
            return a.trust
        return AFFINITY.get(_affinity_key(a, b), 0)

    def add_affinity(a, b, amount):
        if a is b or not (affinity_counts(a) and affinity_counts(b)):
            return
        if a.id == 'lelouch':
            gain_trust(b, amount)
        elif b.id == 'lelouch':
            gain_trust(a, amount)
        else:
            key = _affinity_key(a, b)
            AFFINITY[key] = AFFINITY.get(key, 0) + amount

    def _affinity_player_crews():
        """(pilots, seat pairs) for the player's side of the current board."""
        pilots = []
        seats = set()
        for piece in chess.get_pieces(chess.player):
            crew = [p for p in piece.pilots if affinity_counts(p)]
            pilots += crew
            for i in range(len(crew)):
                for j in range(i + 1, len(crew)):
                    seats.add(_affinity_key(crew[i], crew[j]))
        return pilots, seats

    def affinity_battle_start():
        """Called when a battle starts (l_start_battle): remember who fights for the player."""
        if rogue:
            return
        game.affinity_pilots, game.affinity_seats = _affinity_player_crews()

    def affinity_battle_won():
        """Called when a battle is won (l_after_successful_mission)."""
        if rogue or not hasattr(game, 'affinity_pilots'):
            return
        team = game.affinity_pilots
        for i in range(len(team)):
            for j in range(i + 1, len(team)):
                add_affinity(team[i], team[j], AFFINITY_FIGHT)
                if _affinity_key(team[i], team[j]) in game.affinity_seats:
                    add_affinity(team[i], team[j], AFFINITY_SEAT)
        del game.affinity_pilots # a battle only counts once
        del game.affinity_seats

    def affinity_report():
        """Console helper: every affinity and Trust that isn't 0, e.g. affinity_report()"""
        report = {}
        for (a, b), value in sorted(AFFINITY.items()):
            if value:
                report[a + " - " + b] = value
        for pid in sorted(character.PILOTLIST):
            pilot = globals().get(pid)
            if isinstance(pilot, Pilot) and pid != 'lelouch':
                report["lelouch - " + pid + " (TRUST)"] = pilot.trust
        return report

    def affinity_table_members(pilot):
        """Who appears in the Relationships table: named pilots in TEAM (Lelouch first), plus the pilot being viewed."""
        members = [p for p in TEAM if affinity_counts(p)]
        if pilot not in members and affinity_counts(pilot):
            members.append(pilot)
        members.sort(key=lambda p: p.id != 'lelouch') # stable: Lelouch first, then TEAM order
        return members

# RELATIONSHIPS tab of the pilot screen (s_character_info in src/PILOT_screen.rpy).
# A table with every pilot as a row and a column: each cell is the affinity between the two,
# colored like loyalty (TRUST_TO_LOYALTY). Lelouch's row and column are Trust.
# The row and column of the pilot being viewed are highlighted.
screen s_pilot_relationships(pilot):
    $ members = affinity_table_members(pilot)
    if len(members) < 2:
        text _("No relationships yet.") style 'style_3d_big_txt' xalign 0.5 ypos 100
    else:
        $ n = len(members)
        $ side = n + 1 # one extra row and column for the heads
        $ cell = max(36, min(100, int(860 / side)))
        $ value_size = max(18, int(cell * 0.45))
        grid side side:
            spacing 3
            xalign 0.5
            ypos 10
            null width cell height cell
            for member in members: # column heads
                fixed:
                    xysize (cell, cell)
                    if member is pilot:
                        add Solid(COLOR_HIGHLIGHT())
                    add member.img_side() xysize (cell - 8, cell - 8) fit 'cover' align (0.5, 0.5)
            for row in members:
                fixed: # row head
                    xysize (cell, cell)
                    if row is pilot:
                        add Solid(COLOR_HIGHLIGHT())
                    add row.img_side() xysize (cell - 8, cell - 8) fit 'cover' align (0.5, 0.5)
                for col in members:
                    if row is col:
                        add Solid("#0006") xysize (cell, cell)
                    else:
                        $ value = get_affinity(row, col)
                        $ color = LOYALTY_COLORS[TRUST_TO_LOYALTY(value)]
                        $ highlighted = row is pilot or col is pilot
                        fixed:
                            xysize (cell, cell)
                            add Solid("#000b") # dark base, so dimmed cells look the same on any background
                            add Solid(color[0]) alpha (1.0 if highlighted else 0.3)
                            text str(value) font "fonts/cmu_b.ttf" size value_size align (0.5, 0.5) color ("#222" if highlighted else color[0])
