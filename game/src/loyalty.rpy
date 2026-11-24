# LOYALTY
# Trust is a pilot's affinity with lelouch. It sets their loyalty level:
#
#   Trust        Level   Effect
#   20 or more   Red     +2 STAMINA per rest. Trust gains are doubled.
#   10 to 19     Blue    Normal.
#   0 to 9       Green   Default. Won't fight if they could die: 1 small heart.
#   -10 to -1    Yellow  Only fights with full STAMINA: every heart is small except the last one.
#   below -10    Grey    Same as Yellow. 50% chance to leave each day (not implemented yet, needs the day system).
#
# Small hearts are STAMINA the pilot won't risk: they can only be deployed with more STAMINA than that.
# A 1-STAMINA pilot at Green has no big heart, so they can't be deployed.
# Roguelite: every pilot is locked at Blue.

define LOYALTY_GREY = 0
define LOYALTY_YELLOW = 1
define LOYALTY_GREEN = 2
define LOYALTY_BLUE = 3
define LOYALTY_RED = 4

# (light, dark) per level, indexed by loyalty_of() / TRUST_TO_LOYALTY()
define LOYALTY_COLORS = [("#9fb39c","#789070"), ("#e2da89","#e5b24a"), ("#a0e79e","#47a878"),  ("#9ee0e7","#7584c2"), ("#ff93c5","#d55170")]
define LOYALTY_TO_NAME = [_('Worst'),_('Bad'),_('Average'),_('Good'),_('Best')]

init python:
    def TRUST_TO_LOYALTY(trust):
        if trust < -10:
            return LOYALTY_GREY
        elif trust < 0:
            return LOYALTY_YELLOW
        elif trust < 10:
            return LOYALTY_GREEN
        elif trust < 20:
            return LOYALTY_BLUE
        else:
            return LOYALTY_RED

    def loyalty_of(pilot):
        """A pilot's loyalty level. Use this rather than TRUST_TO_LOYALTY(pilot.trust)."""
        if rogue: # roguelite: everyone is locked at Blue
            return LOYALTY_BLUE
        return TRUST_TO_LOYALTY(pilot.trust)

    def loyalty_color(pilot):
        return LOYALTY_COLORS[loyalty_of(pilot)]

    def loyalty_reserved_stamina(pilot):
        """How many hearts are small: STAMINA the pilot won't risk in a battle."""
        level = loyalty_of(pilot)
        if level <= LOYALTY_YELLOW:
            reserved = max(1, pilot.max_health - 1)
        elif level == LOYALTY_GREEN:
            reserved = 1
        else:
            reserved = 0
        # pilot.max_health - 1, guarantees that 1 HP pilots can still pilot
        # return max(0, min(reserved, pilot.max_health - 1))
        return reserved

    def loyalty_rest_bonus(pilot):
        """Extra STAMINA a pilot gets each time they rest (Red: +2 instead of +1)."""
        if loyalty_of(pilot) == LOYALTY_RED:
            return 1
        return 0

    def loyalty_can_deploy(pilot):
        """A pilot can be deployed only with more STAMINA than they keep in reserve."""
        return pilot.health > loyalty_reserved_stamina(pilot)

    def loyalty_passive_desc(pilot):
        """Text for the loyalty passive in the pilot stats screen. None at Blue (no effect)."""
        level = loyalty_of(pilot)
        if level == LOYALTY_RED:
            return _("+2 STAMINA when resting. TRUST gains x2.")
        if level == LOYALTY_GREEN and loyalty_reserved_stamina(pilot):
            return _("Won't fight if they could die.")
        if level == LOYALTY_YELLOW:
            return _("Only fights with full STAMINA.")
        if level == LOYALTY_GREY:
            return _("Only fights with full STAMINA. May leave the group.")
        return None

    def loyalty_refuse_notify(pilot):
        """Tell the player why a pilot can't be deployed."""
        renpy.play("sound/board/cancel.wav", channel='audio')
        if loyalty_of(pilot) <= LOYALTY_YELLOW:
            message = __("{name} only fights with full STAMINA: LOYALTY too low.").format(name=pilot.name)
        else:
            message = __("{name} won't fight while they could die.").format(name=pilot.name)
        renpy.show_screen('s_loyalty_refuse', message=message, color=loyalty_color(pilot))
        renpy.restart_interaction() # called from click callbacks: make sure it gets drawn

    def gain_trust(pilot, amount):
        """Change a pilot's Trust. Gains are doubled at Red. Returns the change actually applied."""
        if amount > 0 and loyalty_of(pilot) == LOYALTY_RED:
            amount *= 2
        pilot.trust += amount
        return amount

# Short message shown over the board when a pilot refuses to be deployed
screen s_loyalty_refuse(message, color):
    zorder 100
    frame at notify_appear:
        style 'empty'
        xalign 0.5
        ypos 20
        padding (30, 12)
        background Solid("#000c")
        hbox:
            spacing 15
            add "heart big" matrixcolor ColorizeMatrix(color[1], color[0]) xysize (50,50) fit "contain" yalign 0.5
            text message font "FONT_bold" size 38 color "#fff" yalign 0.5
    timer 3.25 action Hide('s_loyalty_refuse')
