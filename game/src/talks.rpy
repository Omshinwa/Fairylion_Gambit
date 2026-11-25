# TALKS
# Social discussions, like Fire Emblem supports. When two pilots of TEAM reach an affinity rank
# (TALK_RANKS, see src/affinity.rpy), they get a talk:
#   - a TALK button lights up on the world map, under PILOTS (s_map_select in maps/s_map_select.rpy),
#   - it opens the RELATIONSHIPS tab of the PILOTS list (src/pilot_list.rpy), where their cell shows TALK,
#   - clicking it plays the talk, once.
# With lelouch, the affinity is the pilot's Trust.
#
# Write a talk as the label l_talk_<id>_<id>_<number>, with the two ids in alphabetical order,
# for example l_talk_kallen_kaworu_1 (first talk) or l_talk_kallen_lelouch_2.
# A talk that isn't written yet plays a placeholder.

define TALK_RANKS = [10, 15, 20] # affinity for the 1st, 2nd and 3rd talk of a pair

default TALKS_DONE = {} # (id_a, id_b) sorted -> how many talks the pair had

init python:
    def talk_available(a, b):
        """The number of the talk a and b can have now (1, 2, 3...), or 0."""
        if rogue or a is b or not (affinity_counts(a) and affinity_counts(b)):
            return 0
        done = TALKS_DONE.get(_affinity_key(a, b), 0)
        if done < len(TALK_RANKS) and get_affinity(a, b) >= TALK_RANKS[done]:
            return done + 1
        return 0

    def talks_available():
        """True if two pilots of TEAM can talk (the TALK button of the world map)."""
        members = affinity_table_members(None)
        return any(talk_available(a, b) for i, a in enumerate(members) for b in members[i + 1:])

    def talk_label(a, b, number):
        return "l_talk_{}_{}_{}".format(*sorted((a.id, b.id)), number)

label l_talk(a, b):
    $ talk_number = talk_available(a, b)
    $ TALKS_DONE[_affinity_key(a, b)] = talk_number
    $ talk_name = talk_label(a, b, talk_number)
    if renpy.has_label(talk_name):
        call expression talk_name
    else: # placeholder until the talk is written
        $ talker_a = getattr(character, a.id)
        $ talker_b = getattr(character, b.id)
        talker_a "[b.name], do you have a minute?"
        talker_b "Sure. What is it?"
        "(Talk [talk_number] between [a.name] and [b.name] isn't written yet: label [talk_name].)"
    return

transform t_talk_pulse: # what lights up for a talk
    alpha 1.0
    linear 0.6 alpha 0.4
    linear 0.6 alpha 1.0
    repeat
