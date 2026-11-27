# SHIP (story mode), parts 1 and 2. See The ship in ai_prompt/prompt.md.
#   - The SHIP button of the world map opens it, once ship_unlocked is True. So does the SHIP button of the
#     deployment (story mode): the deployment picks who fights, the ship where the others spend the day.
#   - Rooms are researched, built, then built again to extend them to 2 pilots, with TECH points.
#     A room can't be used on the day it's extended.
#   - Pilots are moved like in the deployment: drag them to a room (or back to the rest space),
#     or click them, then click the room.
#   - Pilots put in a room don't fight: they're left out of the deployment (s_preparation in
#     src/CHESS/s_preparation.rpy). They stay in their room from day to day until the player moves them.
#   - Each room's effect replaces the pilot's rest on the rewards screen (its RESERVE column, see ship_room_rest).
#     Then at the new day (l_new_day in src/day.rpy), roommates get +3 affinity, the ship gives 10 TECH,
#     and every robot with a RESEARCH LAB that didn't fight gives 2 more (src/robot_upgrades.rpy).
#   - Rooms: training, rest (two pilots there may share a coffee), heavy gravity, healing tank (costs more)
#     and classroom (2 seats: a pilot who learned every skill gives all their EXP to the other).
# Not done yet: the hangar, the radar room, days without a battle.

default ship_unlocked = False
default TECH = 0
default SHIP_RESEARCHED = set()
default SHIP_ROOMS = {} # kind -> ShipRoom

define SHIP_ROOM_KINDS = ['training', 'rest', 'gravity', 'healing', 'classroom'] # research order
define SHIP_ROOM_NAME = {
    'training': _("TRAINING ROOM"),
    'rest': _("RESTING ROOM"),
    'gravity': _("GRAVITY ROOM"),
    'healing': _("HEALING TANK"),
    'classroom': _("CLASSROOM"),
}
define SHIP_ROOM_DESC = { # one line: about 32 characters at most
    'training': _("+1 EXP, and they rest."),
    'rest': _("They rest, +1 more STAMINA."),
    'gravity': _("+2 EXP, but they don't rest."),
    'healing': _("Restores all their STAMINA."),
    'classroom': _("A MAX pilot teaches the other."), # MAX: learned every skill, like in the deployment's EXP sort
}
define SHIP_RESEARCH_COST = 2
define SHIP_BUILD_COST = 2 # also the cost to extend a room
define SHIP_ROOM_COST = {'healing': (4, 6)} # (research, build or extend) of the rooms that cost more
define SHIP_ROOM_MAX_SIZE = 2
define SHIP_ROOM_START_SIZE = {'classroom': 2} # seats when built (otherwise 1)
define SHIP_COFFEE_CHANCE = 0.5 # two pilots in the rest room share a coffee (the day's report, l_ship_day)
define SHIP_HULL_SPACES = 6 # empty spaces of the ship, where rooms are built
define AFFINITY_ROOM = 3
define SHIP_TECH_PER_DAY = 10 # every new day, once the ship is unlocked

# the ship screen's layout (pixels): the hull's spaces in 3 columns, the rest space under them
define SHIP_SPACE_SIZE = (520, 270)
define SHIP_HULL_POS = (160, 100)
define SHIP_HULL_GAP = 20
define SHIP_REST_RECT = (160, 780, 1600, 280) # x, y, width, height
define SHIP_REST_PER_ROW = 12

default ship_selected = None # the pilot picked in the ship screen, before clicking where they go
default ship_coffee = None # the two pilots of the day's coffee break (ship_new_day)

init python:
    class ShipRoom(object):
        def __init__(self, kind):
            self.kind = kind
            self.size = SHIP_ROOM_START_SIZE.get(kind, 1) # how many pilots it holds
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

    def ship_research_cost(kind):
        return SHIP_ROOM_COST.get(kind, (SHIP_RESEARCH_COST, SHIP_BUILD_COST))[0]

    def ship_build_cost(kind):
        """To build the room, or to extend it."""
        return SHIP_ROOM_COST.get(kind, (SHIP_RESEARCH_COST, SHIP_BUILD_COST))[1]

    def ship_research(kind):
        global TECH
        if TECH >= ship_research_cost(kind) and kind not in SHIP_RESEARCHED:
            TECH -= ship_research_cost(kind)
            SHIP_RESEARCHED.add(kind)

    def ship_build(kind):
        """Build a researched room, or build it again to extend it (closed for the rest of the day)."""
        global TECH
        if TECH < ship_build_cost(kind) or kind not in SHIP_RESEARCHED:
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
        TECH -= ship_build_cost(kind)

    def ship_assign(pilot, room):
        if not room.has_room():
            return
        ship_unassign(pilot)
        room.pilots.append(pilot)

    def ship_unassign(pilot):
        room = ship_room_of(pilot)
        if room is not None:
            room.pilots.remove(pilot)

    ### MOVING PILOTS: drag them, or click them then click the room (like the deployment, src/CHESS/s_preparation.rpy)
    # Targets are drags named ('room', kind) for a room, SHIP_REST_SPACE for the rest space.
    SHIP_REST_SPACE = 'ship_rest_space'

    def ship_rest_pilots():
        """Pilots in the rest space: not in a room and not fighting today (deployed, when it's opened from the deployment)."""
        return [pilot for pilot in TEAM if not pilot.deployed and ship_room_of(pilot) is None]

    def ship_target(drag_name):
        """The ShipRoom a target drag stands for, or None for the rest space."""
        if drag_name == SHIP_REST_SPACE:
            return None
        return SHIP_ROOMS[drag_name[1]]

    def ship_can_move(pilot, room):
        """Can the pilot go to this room (None: the rest space)?"""
        if room is None:
            return ship_room_of(pilot) is not None
        return ship_room_of(pilot) is not room and room.has_room()

    def ship_move(pilot, room):
        """Move the pilot to the room (None: the rest space). True if they moved."""
        if not ship_can_move(pilot, room):
            return False
        if room is None:
            ship_unassign(pilot)
        else:
            ship_assign(pilot, room)
        renpy.play("sound/board/tank.wav", channel='sound')
        return True

    def ship_drop_allowable(drop, drags):
        # only the rooms the dragged pilot can go to light up and take the drop
        return ship_can_move(drags[0].drag_name, ship_target(drop.drag_name))

    def ship_pilot_clicked(drag):
        """Click a pilot to pick them (again to drop them)."""
        global ship_selected
        pilot = drag.drag_name
        if ship_selected is pilot:
            ship_selected = None
            renpy.play("sound/board/cancel.wav", channel='audio')
        else:
            ship_selected = pilot
            renpy.play("sound/board/select.wav", channel='audio')
        renpy.restart_interaction()

    def ship_target_clicked(drag):
        """Click a room (or the rest space) after picking a pilot: they go there."""
        global ship_selected
        if ship_selected is None:
            return
        room = ship_target(drag.drag_name)
        if ship_move(ship_selected, room) or room is None: # a click in the rest space also drops the pick
            ship_selected = None
        renpy.restart_interaction()

    def ship_pilot_dragging(drags):
        global ship_selected
        if ship_selected is not drags[0].drag_name: # picked while dragged: the rooms they can go to light up
            ship_selected = drags[0].drag_name
            renpy.restart_interaction()

    def ship_pilot_dragged(drags, drop):
        global ship_selected
        drag = drags[0]
        moved = drop is not None and ship_move(drag.drag_name, ship_target(drop.drag_name))
        if moved:
            ship_selected = None
        # back to its place: if it moved, the screen places it in its new seat
        drag.snap(int(drag.start_x), int(drag.start_y), delay=0 if moved else 0.1)
        renpy.restart_interaction()

    ### LAYOUT
    def ship_space_pos(i):
        """Top-left corner of the hull's space i."""
        column, row = i % 3, i // 3
        return (SHIP_HULL_POS[0] + column * (SHIP_SPACE_SIZE[0] + SHIP_HULL_GAP),
                SHIP_HULL_POS[1] + row * (SHIP_SPACE_SIZE[1] + SHIP_HULL_GAP))

    def ship_seat_pos(i, seat):
        """Top-left corner of a pilot sitting in seat `seat` of the room in space i (seats are 110 wide, pilots 100)."""
        x, y = ship_space_pos(i)
        return (x + 20 + seat * 120, y + 100)

    def ship_rest_pos(index, count):
        """Top-left corner of the pilot number `index` of the rest space, which holds `count` pilots."""
        row, column = index // SHIP_REST_PER_ROW, index % SHIP_REST_PER_ROW
        in_row = min(SHIP_REST_PER_ROW, count - row * SHIP_REST_PER_ROW)
        x0 = SHIP_REST_RECT[0] + (SHIP_REST_RECT[2] - (in_row * 120 - 20)) // 2
        return (x0 + column * 120, SHIP_REST_RECT[1] + 60 + row * 120)

    def ship_room_child(room, color):
        """A room's background and seats (the room is a drag the pilots are dropped on)."""
        children = [Solid(color)]
        for seat in range(room.size):
            children.append(Solid("#fff1", xysize=(110, 110), pos=(15 + seat * 120, 95)))
            if seat >= len(room.pilots) and room.has_room():
                children.append(Text("+", style='style_3d_big_txt', size=60, pos=(70 + seat * 120, 150), anchor=(0.5, 0.5)))
        return Fixed(*children, xysize=SHIP_SPACE_SIZE)

    def ship_room_rest(pilot):
        """The day's rest of a pilot in a ship room, instead of pilot.rest(): given by the rewards screen
        (l_battle_rewards in src/battle_rewards.rpy), which shows them in its RESERVE column. True if they gained something."""
        room = ship_room_of(pilot)
        xp, health = pilot.xp, pilot.health
        if room.kind == 'training':
            pilot.increase_xp(1)
            pilot.rest()
        elif room.kind == 'rest':
            pilot.health = min(pilot.max_health, pilot.health + pilot.rest_gain() + 1)
        elif room.kind == 'gravity':
            pilot.increase_xp(2)
        elif room.kind == 'healing':
            pilot.health = pilot.max_health
        elif room.kind == 'classroom':
            pilot.rest()
            teacher = ship_classroom_teacher(room)
            if teacher is not None and teacher is not pilot: # the student gets all the teacher's EXP
                pilot.increase_xp(teacher.xp)
                teacher.xp = 0
        return pilot.xp != xp or pilot.health != health

    def ship_classroom_teacher(room):
        """The classroom's teacher: a pilot who learned every skill (MAX), with a student who still has skills to learn."""
        if len(room.pilots) != 2:
            return None
        for teacher, student in (room.pilots, room.pilots[::-1]):
            if not teacher.skills['can_learn'] and student.skills['can_learn'] and teacher.xp:
                return teacher
        return None

    def ship_coffee_label(a, b):
        """Write a label with this name for two pilots' coffee break in the rest room (ids in alphabetical order)."""
        return 'l_coffee_{}_{}'.format(*sorted((a.id, b.id)))

    def ship_new_day():
        """A new day (l_new_day), after the rewards gave the rooms' effects: roommates' affinity, TECH. Returns the report's lines."""
        global TECH, ship_coffee
        report = []
        ship_coffee = None
        for room in SHIP_ROOMS.values():
            room.pilots = [pilot for pilot in room.pilots if pilot in TEAM] # the dead and departed leave
            if room.kind == 'rest' and len(room.pilots) == 2 and renpy.random.random() < SHIP_COFFEE_CHANCE:
                ship_coffee = tuple(room.pilots) # l_ship_day plays their coffee break
                report.append(__("{} and {} shared a coffee in the rest room.").format(room.pilots[0].name, room.pilots[1].name))
            for i in range(len(room.pilots)):
                for j in range(i + 1, len(room.pilots)):
                    add_affinity(room.pilots[i], room.pilots[j], AFFINITY_ROOM) # see src/affinity.rpy
                    report.append(__("{} and {} shared a room: +{} affinity").format(room.pilots[i].name, room.pilots[j].name, AFFINITY_ROOM))
            room.extended_today = False
        # robots with a RESEARCH LAB that didn't fight (src/robot_upgrades.rpy)
        lab_tech = ROBOT_UPGRADE_TECH * len([robot for robot in ROBOTS if not robot.deployed and robot_has_upgrade(robot, 'tech')])
        TECH += SHIP_TECH_PER_DAY + lab_tech
        if lab_tech:
            report.append(__("+{} TECH: {} a day, {} from the RESEARCH LABS of robots that didn't fight. TECH: {}").format(SHIP_TECH_PER_DAY + lab_tech, SHIP_TECH_PER_DAY, lab_tech, TECH))
        else:
            report.append(__("+{} TECH. TECH: {}").format(SHIP_TECH_PER_DAY, TECH))
        for robot in ROBOTS:
            robot.deployed = False
        return report

label l_ship:
    play sound 'sound/misc/plop.wav'
    $ renpy.layer_at_list([t_blur], layer="master")
    $ renpy.retain_after_load() # a save made while the ship is open keeps what was built in it
    $ ship_selected = None
    call screen s_ship with Dissolve(0.2)
    $ ship_selected = None
    $ remove_blur_master()
    with Dissolve(0.2)
    return

# called by l_new_day
label l_ship_day:
    $ ship_report = ship_new_day()
    call screen s_ship_report(ship_report) with Dissolve(0.2)
    if ship_coffee and renpy.has_label(ship_coffee_label(*ship_coffee)): # their talk over a coffee, if it's written
        call expression ship_coffee_label(*ship_coffee)
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

# THE SHIP: rooms built in the hull's empty spaces, research, and the rest space (pilots not in a room, not fighting).
# The pilots are drags, like the deployment's reserve: drag one to a room (or back to the rest space),
# or click it, then click where it goes. The rooms and the rest space are the drop targets.
screen s_ship():
    modal True
    zorder 1
    add Solid("#0a1830f0")
    button: # a click in the void drops the pick
        style 'empty'
        xysize (1.0, 1.0)
        action SetVariable('ship_selected', None)

    text _("SHIP") style 'style_purple_text' font "Venus+Plomb.otf" kerning 25 xalign 0.5 ypos 15
    text _("TECH: [TECH]") style 'style_3d_big_txt' pos (40, 25)

    $ rooms = list(SHIP_ROOMS.values())
    $ rest_pilots = ship_rest_pilots()
    $ picked = ship_selected

    for i in range(len(rooms), SHIP_HULL_SPACES):
        use s_ship_empty_space(i == len(rooms), ship_space_pos(i)) # only the first empty space can be built on

    hbox: # research: up to two lines, between the hull and the rest space
        xalign 0.5
        ypos 668
        xmaximum 1700
        box_wrap True
        spacing 20
        $ to_research = [kind for kind in SHIP_ROOM_KINDS if kind not in SHIP_RESEARCHED]
        if to_research:
            text _("RESEARCH:") style 'style_3d_big_txt' size 34 yalign 0.5
            for kind in to_research:
                textbutton _("{} ({} TECH)").format(__(SHIP_ROOM_NAME[kind]), ship_research_cost(kind)) at t_interactive:
                    text_style 'style_big_white_text'
                    text_size 28
                    sensitive TECH >= ship_research_cost(kind)
                    action Function(ship_research, kind)

    draggroup:
        # the drop targets: rooms (brighter when the picked pilot can go there) and the rest space
        for i, room index room.kind in enumerate(rooms):
            $ room_color = "#16294a" if room.extended_today else "#1d3a66"
            $ can_go = picked is not None and ship_can_move(picked, room)
            drag:
                drag_name ('room', room.kind)
                draggable False
                droppable True
                drop_allowable ship_drop_allowable
                pos ship_space_pos(i)
                clicked ship_target_clicked
                idle_child ship_room_child(room, "#2b5596" if can_go else room_color)
                hover_child ship_room_child(room, "#3a6cb5" if can_go else room_color)
                selected_idle_child ship_room_child(room, COLOR_HIGHLIGHT())
                selected_hover_child ship_room_child(room, COLOR_HIGHLIGHT())

        $ rest_size = (SHIP_REST_RECT[2], SHIP_REST_RECT[3])
        $ can_go = picked is not None and ship_can_move(picked, None)
        drag:
            drag_name SHIP_REST_SPACE
            draggable False
            droppable True
            drop_allowable ship_drop_allowable
            pos (SHIP_REST_RECT[0], SHIP_REST_RECT[1])
            clicked ship_target_clicked
            idle_child Solid("#ffffff1c" if can_go else "#ffffff0c", xysize=rest_size)
            hover_child Solid("#ffffff2a" if can_go else "#ffffff0c", xysize=rest_size)
            selected_idle_child Solid(COLOR_HIGHLIGHT(), xysize=rest_size)
            selected_hover_child Solid(COLOR_HIGHLIGHT(), xysize=rest_size)

        # the pilots
        for i, room index room.kind in enumerate(rooms):
            for seat, pilot index pilot.id in enumerate(room.pilots):
                use s_ship_pilot(pilot, ship_seat_pos(i, seat), picked)
        for k, pilot index pilot.id in enumerate(rest_pilots):
            use s_ship_pilot(pilot, ship_rest_pos(k, len(rest_pilots)), picked)

    # texts and buttons on top of the rooms (they're not drop targets: the room under them is)
    for i, room in enumerate(rooms):
        use s_ship_room_text(room, ship_space_pos(i))
    text _("REST SPACE: drag a pilot to a room, or click them then the room. Pilots in a room don't fight.") style 'style_big_white_text' size 30:
        xalign 0.5
        ypos SHIP_REST_RECT[1] + 12

    button at t_interactive:
        align (1.0, 0.0)
        xysize 100,100
        action Return()
        text 'X' style 'style_3d_big_txt' size 60 align 0.5,0.5

screen s_ship_pilot(pilot, xy, picked):
    drag:
        drag_name pilot
        pos xy
        xysize (100, 100)
        droppable False
        mouse_drop True # dropped on the room under the mouse
        clicked ship_pilot_clicked
        dragging ship_pilot_dragging
        dragged ship_pilot_dragged
        use s_pilot_icon(pilot, picked=(picked is pilot)) # the deployment's icon, see src/PILOT_screen.rpy

screen s_ship_room_text(room, xy):
    vbox:
        pos (xy[0] + 15, xy[1] + 10)
        spacing 6
        text __(SHIP_ROOM_NAME[room.kind]) style 'style_big_white_text' size 34
        text __(SHIP_ROOM_DESC[room.kind]) style 'style_big_white_text' size 26 color "#cde"
    if room.extended_today:
        text _("Extended: closed until tomorrow.") style 'style_big_white_text' size 24 color "#ffa" pos (xy[0] + 15, xy[1] + 222)
    elif room.size < SHIP_ROOM_MAX_SIZE:
        textbutton _("EXTEND ({} TECH)").format(ship_build_cost(room.kind)) at t_interactive:
            pos (xy[0] + 15, xy[1] + 215)
            text_style 'style_big_white_text'
            text_size 26
            sensitive TECH >= ship_build_cost(room.kind)
            action Function(ship_build, room.kind)

screen s_ship_empty_space(buildable, xy):
    frame:
        style 'empty'
        pos xy
        xysize SHIP_SPACE_SIZE
        background Solid("#ffffff0c")
        padding (15, 10)
        vbox:
            spacing 8
            text _("EMPTY SPACE") style 'style_big_white_text' size 30 color "#fff8"
            if buildable:
                for kind in SHIP_ROOM_KINDS:
                    if kind in SHIP_RESEARCHED and kind not in SHIP_ROOMS:
                        textbutton _("BUILD {} ({} TECH)").format(__(SHIP_ROOM_NAME[kind]), ship_build_cost(kind)) at t_interactive:
                            text_style 'style_big_white_text'
                            text_size 26
                            sensitive TECH >= ship_build_cost(kind)
                            action Function(ship_build, kind)

# the RESERVE column of the rewards screen (s_result_screen_mini in src/roguelike_events.rpy), for a pilot in a room
screen s_result_room_gains(pilot, room, state, original_health, original_xp):
    $ xp_gain = pilot.xp - original_xp.get(pilot, pilot.xp)
    $ health_gain = pilot.health - original_health.get(pilot, pilot.health)
    vbox: # compact: the card has 140 pixels for the room, the stat and up to two gains
        spacing -4
        text __(SHIP_ROOM_NAME[room.kind]) style 'style_big_white_text' size 22 color "#8cf"
        if room.kind == 'gravity':
            text _("EXP: [pilot.xp]") xalign 0.0 style 'style_big_white_text' size 34 color ("#ffa" if xp_gain else "#fff")
        else:
            text _("STAMINA: [pilot.health]/[pilot.max_health]") xalign 0.0 style 'style_big_white_text' size 34 color ("#ffa" if health_gain else "#fff")
        if state >= 1 and (xp_gain or health_gain): # one line: a second one would run under the next row
            $ gains = [__("{:+d} EXP").format(xp_gain)] if xp_gain else [] # a teacher of the classroom loses theirs
            $ gains += [__("{:+d} STAMINA").format(health_gain)] if health_gain else []
            text "> " + ", ".join(gains) xalign 0.0 font "fonts/Compagnon-Medium.otf" style 'style_big_white_text' size 24 at t_emphazise_text
