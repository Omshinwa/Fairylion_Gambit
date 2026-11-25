# AFFINITY
# Every pair of characters has an affinity. Lelouch's affinity with a pilot is that pilot's
# Trust (pilot.trust, see src/loyalty.rpy), so both go through the same functions here.
# Story mode only: roguelite has no social side.
#
#   +1  for every pair of pilots who fought on a won day (with the day's EXP, see src/battle_rewards.rpy)
#   +3  more if they sat in the same CHESSMAN (two-seat robot) in one of the day's battles
#
# Talks unlocked by high affinity: src/talks.rpy
# Not done yet: +3 for sharing a room on the ship, also allows to drive a Queen


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
        """A new story starts (l_intro): every affinity goes back to AFFINITY_START, and no talk was had."""
        AFFINITY.clear()
        for pair, value in AFFINITY_START.items():
            AFFINITY[tuple(sorted(pair))] = value
        TALKS_DONE.clear() # see src/talks.rpy

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

    def affinity_seat_pairs():
        """Pairs of named pilots sitting in the same CHESSMAN, on the player's side of the board."""
        seats = set()
        for piece in chess.get_pieces(chess.player):
            crew = [p for p in piece.pilots if affinity_counts(p)]
            for i in range(len(crew)):
                for j in range(i + 1, len(crew)):
                    seats.add(_affinity_key(crew[i], crew[j]))
        return seats

    def affinity_day_won(fought, seats):
        """The day's battles were won (l_story_day_rewards): +1 for every pair who fought, +3 more for seat pairs."""
        team = [p for p in fought if affinity_counts(p)]
        for i in range(len(team)):
            for j in range(i + 1, len(team)):
                add_affinity(team[i], team[j], AFFINITY_FIGHT)
                if _affinity_key(team[i], team[j]) in seats:
                    add_affinity(team[i], team[j], AFFINITY_SEAT)

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

# RELATIONSHIPS: each cell is the affinity between two pilots, colored like loyalty (TRUST_TO_LOYALTY).
# Lelouch's row and column are Trust.
#   s_relationships_table():       every pilot in TEAM as a row and a column
#                                  (RELATIONSHIPS tab of the PILOTS list, src/pilot_list.rpy)
#   s_pilot_relationships(pilot):  only that pilot's row
#                                  (RELATIONSHIPS tab of their profile, s_character_info in src/PILOT_screen.rpy)

screen s_affinity_face(member, cell, highlight=False):
    fixed:
        xysize (cell, cell)
        if highlight:
            add Solid(COLOR_HIGHLIGHT())
        add member.img_side() xysize (cell - 8, cell - 8) fit 'cover' align (0.5, 0.5)

screen s_affinity_value(a, b, cell, talk=False): # talk: show (and play) the talk the pair can have, src/talks.rpy
    $ value = get_affinity(a, b)
    $ color = LOYALTY_COLORS[TRUST_TO_LOYALTY(value)]
    if talk and talk_available(a, b):
        button at t_interactive:
            style 'empty'
            xysize (cell, cell)
            background Solid(color[0])
            action Return(('talk', a, b)) # l_pilot_list plays it
            text str(value) font "fonts/cmu_b.ttf" size max(18, int(cell * 0.35)) xalign 0.5 ypos 0.1 color "#222"
            text _("TALK") style 'style_3d_big_txt' size max(16, int(cell * 0.28)) xalign 0.5 yalign 0.9 at t_talk_pulse
    else:
        fixed:
            xysize (cell, cell)
            add Solid(color[0])
            text str(value) font "fonts/cmu_b.ttf" size max(18, int(cell * 0.45)) align (0.5, 0.5) color "#222"

screen s_relationships_table():
    $ members = affinity_table_members(None)
    if len(members) < 2:
        text _("No relationships yet.") style 'style_3d_big_txt' xalign 0.5 ypos 100
    else:
        $ side = len(members) + 1 # one extra row and column for the faces
        $ cell = max(36, min(100, int(860 / side)))
        grid side side:
            spacing 3
            xalign 0.5
            null width cell height cell
            for member in members: # column heads
                use s_affinity_face(member, cell)
            for row in members:
                use s_affinity_face(row, cell) # row head
                for col in members:
                    if row is col:
                        add Solid("#0006") xysize (cell, cell)
                    else:
                        use s_affinity_value(row, col, cell, talk=True)

screen s_pilot_relationships(pilot):
    $ others = [member for member in affinity_table_members(pilot) if member is not pilot]
    if not others:
        text _("No relationships yet.") style 'style_3d_big_txt' xalign 0.5 ypos 100
    else:
        $ side = len(others) + 1 # one extra column for the pilot's face
        $ cell = max(36, min(110, int(1000 / side)))
        grid side 2:
            spacing 3
            xalign 0.5
            ypos 10
            null width cell height cell
            for member in others: # column heads
                use s_affinity_face(member, cell)
            use s_affinity_face(pilot, cell, highlight=True) # the row
            for member in others:
                use s_affinity_value(pilot, member, cell)
