# SHIP (story mode), part 1. See The ship in ai_prompt/prompt.md.
#   - The SHIP button of the world map opens it, once ship_unlocked is True.
#   - Rooms are researched, built, then built again to extend them to 2 pilots, with TECH points.
#     A room can't be used on the day it's extended.
#   - Pilots put in a room don't fight: they're left out of the deployment (s_preparation in
#     src/CHESS/s_preparation.rpy) and out of the rewards' rest (src/battle_rewards.rpy).
#     They stay in their room from day to day until the player moves them. Lelouch leads the army: no room for him.
#   - At the new day (l_new_day in src/day.rpy), each room's effect applies, roommates get +3 affinity,
#     and every robot that didn't fight gives 1 TECH.
# Not done yet: the hangar, the healing tank, radar room and classroom, days without a battle.

default ship_unlocked = False
default TECH = 0
default SHIP_RESEARCHED = set()
default SHIP_ROOMS = {} # kind -> ShipRoom

define SHIP_ROOM_KINDS = ['training', 'rest', 'gravity'] # research order
define SHIP_ROOM_NAME = {'training': _("TRAINING ROOM"), 'rest': _("REST ROOM"), 'gravity': _("HEAVY GRAVITY ROOM")}
define SHIP_ROOM_DESC = {
    'training': _("+1 EXP, and they rest."),
    'rest': _("They rest, +1 more STAMINA."),
    'gravity': _("+2 EXP, but they don't rest."),
}
define SHIP_RESEARCH_COST = 2
define SHIP_BUILD_COST = 2 # also the cost to extend a room
define SHIP_ROOM_MAX_SIZE = 2
define SHIP_HULL_SPACES = 6 # empty spaces of the ship, where rooms are built
define AFFINITY_ROOM = 3

init python:
    class ShipRoom(object):
        def __init__(self, kind):
            self.kind = kind
            self.size = 1 # how many pilots it holds
            self.pilots = []
            self.extended_today = False

        def has_room(self):
            return not self.extended_today and len(self.pilots) < self.size

    def ship_room_of(pilot):
        """The room the pilot is in, or None."""
        for room in SHIP_ROOMS.values():
            if pilot in room.pilots:
                return room
        return None

    def ship_can_enter(pilot):
        return pilot.id != 'lelouch'

    def ship_research(kind):
        global TECH
        if TECH >= SHIP_RESEARCH_COST and kind not in SHIP_RESEARCHED:
            TECH -= SHIP_RESEARCH_COST
            SHIP_RESEARCHED.add(kind)

    def ship_build(kind):
        """Build a researched room, or build it again to extend it (closed for the rest of the day)."""
        global TECH
        if TECH < SHIP_BUILD_COST or kind not in SHIP_RESEARCHED:
            return
        room = SHIP_ROOMS.get(kind)
        if room is None:
            if len(SHIP_ROOMS) >= SHIP_HULL_SPACES:
                return
            SHIP_ROOMS[kind] = ShipRoom(kind)
        elif room.size < SHIP_ROOM_MAX_SIZE:
            room.size += 1
            room.extended_today = True
            del room.pilots[:] # back to the rest space
        else:
            return
        TECH -= SHIP_BUILD_COST

    def ship_assign(pilot, room):
        if not ship_can_enter(pilot) or not room.has_room():
            return
        ship_unassign(pilot)
        room.pilots.append(pilot)

    def ship_unassign(pilot):
        room = ship_room_of(pilot)
        if room is not None:
            room.pilots.remove(pilot)

    def ship_new_day():
        """A new day (l_new_day): room effects, roommates' affinity, TECH. Returns the report's lines."""
        global TECH
        report = []
        for room in SHIP_ROOMS.values():
            room.pilots = [pilot for pilot in room.pilots if pilot in TEAM] # the dead and departed leave
            for pilot in room.pilots:
                xp, health = pilot.xp, pilot.health
                if room.kind == 'training':
                    pilot.increase_xp(1)
                    pilot.rest()
                elif room.kind == 'rest':
                    pilot.health = min(pilot.max_health, pilot.health + pilot.rest_gain() + 1)
                elif room.kind == 'gravity':
                    pilot.increase_xp(2)
                gains = []
                if pilot.xp != xp:
                    gains.append(__("+{} EXP").format(pilot.xp - xp))
                if pilot.health != health:
                    gains.append(__("+{} STAMINA").format(pilot.health - health))
                report.append("{}: {}  {}".format(__(SHIP_ROOM_NAME[room.kind]), pilot.name, ", ".join(gains) or "-"))
            for i in range(len(room.pilots)):
                for j in range(i + 1, len(room.pilots)):
                    add_affinity(room.pilots[i], room.pilots[j], AFFINITY_ROOM) # see src/affinity.rpy
                    report.append(__("{} and {} shared a room: +{} affinity").format(room.pilots[i].name, room.pilots[j].name, AFFINITY_ROOM))
            room.extended_today = False
        idle_robots = len([robot for robot in ROBOTS if not robot.deployed])
        TECH += idle_robots
        report.append(__("+{} TECH: robots that didn't fight. TECH: {}").format(idle_robots, TECH))
        for robot in ROBOTS:
            robot.deployed = False
        return report

label l_ship:
    play sound 'sound/misc/plop.wav'
    $ renpy.layer_at_list([t_blur], layer="master")
    $ renpy.retain_after_load() # a save made while the ship is open keeps what was built in it
    call screen s_ship with Dissolve(0.2)
    $ remove_blur_master()
    with Dissolve(0.2)
    return

# called by l_new_day
label l_ship_day:
    $ ship_report = ship_new_day()
    call screen s_ship_report(ship_report) with Dissolve(0.2)
    return

screen s_ship_report(lines):
    modal True
    zorder 1
    add "#000b"
    frame:
        style 'empty'
        background Solid("#0a1830")
        padding (60, 40)
        align (0.5, 0.5)
        vbox:
            spacing 12
            text _("SHIP") style 'style_purple_text' font "Venus+Plomb.otf" kerning 25 xalign 0.5
            for line in lines:
                text line style 'style_big_white_text' size 34 textalign 0.0
    button: # click anywhere to continue
        action Return()

# THE SHIP: rooms built in the hull's empty spaces, research, and the rest space (pilots not in a room).
# Pick a pilot in the rest space, then a free seat. Click a pilot in a room to send them back.
screen s_ship():
    modal True
    zorder 1
    default selected = None # pilot picked in the rest space
    add Solid("#0a1830f0")

    text _("SHIP") style 'style_purple_text' font "Venus+Plomb.otf" kerning 25 xalign 0.5 ypos 15
    text _("TECH: [TECH]") style 'style_3d_big_txt' pos (40, 25)

    $ rooms = [SHIP_ROOMS[kind] for kind in SHIP_ROOMS]
    grid 3 2: # the hull
        xalign 0.5
        ypos 110
        spacing 20
        for i in range(SHIP_HULL_SPACES):
            if i < len(rooms):
                use s_ship_room(rooms[i], selected)
            else:
                use s_ship_empty_space(i == len(rooms)) # only the first empty space can be built on

    hbox: # research
        xalign 0.5
        ypos 700
        spacing 20
        $ to_research = [kind for kind in SHIP_ROOM_KINDS if kind not in SHIP_RESEARCHED]
        if to_research:
            text _("RESEARCH:") style 'style_3d_big_txt' size 40 yalign 0.5
            for kind in to_research:
                textbutton _("{} ({} TECH)").format(__(SHIP_ROOM_NAME[kind]), SHIP_RESEARCH_COST) at t_interactive:
                    text_style 'style_big_white_text'
                    text_size 32
                    sensitive TECH >= SHIP_RESEARCH_COST
                    action Function(ship_research, kind)

    vbox: # rest space
        xalign 0.5
        ypos 790
        spacing 10
        text _("REST SPACE: pick a pilot, then a free seat. Pilots in a room don't fight.") style 'style_big_white_text' size 30 xalign 0.5
        hbox:
            xalign 0.5
            spacing 10
            for pilot in TEAM:
                if ship_room_of(pilot) is None:
                    button at t_interactive:
                        style 'empty'
                        xysize (120, 120)
                        background Solid(COLOR_HIGHLIGHT() if selected is pilot else "#fff2")
                        sensitive ship_can_enter(pilot)
                        action SetScreenVariable('selected', None if selected is pilot else pilot)
                        add pilot.img_side() xysize (110, 110) fit 'cover' align (0.5, 0.5)

    button at t_interactive:
        align (1.0, 0.0)
        xysize 100,100
        action Return()
        text 'X' style 'style_3d_big_txt' size 60 align 0.5,0.5

screen s_ship_room(room, selected):
    frame:
        style 'empty'
        xysize (520, 270)
        background Solid("#1d3a66")
        padding (15, 10)
        vbox:
            spacing 6
            text __(SHIP_ROOM_NAME[room.kind]) style 'style_big_white_text' size 34
            text __(SHIP_ROOM_DESC[room.kind]) style 'style_big_white_text' size 26 color "#cde"
            hbox:
                spacing 10
                for seat in range(room.size):
                    if seat < len(room.pilots):
                        button at t_interactive: # back to the rest space
                            style 'empty'
                            xysize (110, 110)
                            background Solid("#fff3")
                            action Function(ship_unassign, room.pilots[seat])
                            add room.pilots[seat].img_side() xysize (100, 100) fit 'cover' align (0.5, 0.5)
                    else:
                        button at t_interactive: # a free seat
                            style 'empty'
                            xysize (110, 110)
                            background Solid("#fff1")
                            sensitive selected is not None and room.has_room()
                            action Function(ship_assign, selected, room), SetScreenVariable('selected', None)
                            text ("+" if room.has_room() else "") style 'style_3d_big_txt' size 60 align (0.5, 0.5)
            if room.extended_today:
                text _("Extended: closed until tomorrow.") style 'style_big_white_text' size 24 color "#ffa"
            elif room.size < SHIP_ROOM_MAX_SIZE:
                textbutton _("EXTEND ({} TECH)").format(SHIP_BUILD_COST) at t_interactive:
                    text_style 'style_big_white_text'
                    text_size 26
                    sensitive TECH >= SHIP_BUILD_COST
                    action Function(ship_build, room.kind)

screen s_ship_empty_space(buildable):
    frame:
        style 'empty'
        xysize (520, 270)
        background Solid("#ffffff0c")
        padding (15, 10)
        vbox:
            spacing 8
            text _("EMPTY SPACE") style 'style_big_white_text' size 30 color "#fff8"
            if buildable:
                for kind in SHIP_ROOM_KINDS:
                    if kind in SHIP_RESEARCHED and kind not in SHIP_ROOMS:
                        textbutton _("BUILD {} ({} TECH)").format(__(SHIP_ROOM_NAME[kind]), SHIP_BUILD_COST) at t_interactive:
                            text_style 'style_big_white_text'
                            text_size 26
                            sensitive TECH >= SHIP_BUILD_COST
                            action Function(ship_build, kind)
