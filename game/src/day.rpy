# DAY
# One battle = one day (see The ship in ai_prompt/prompt.md). A new day starts when a won battle
# goes back to the map: l_map_select calls l_new_day. Story mode only (roguelite doesn't use the map).
# It's a label rather than a python function because it plays dialogue: call l_new_day
#
label l_new_day:
    if rewards_pending: # a battle was won today
        # first, the rewards of the day's battles: EXP and rest (see src/battle_rewards.rpy)
        call l_story_day_rewards
        # then the ship: its rooms' effects and TECH (see src/ship.rpy)
        if ship_unlocked:
            call l_ship_day

    # Grey pilots may leave the group, after a short talk with lelouch (see src/loyalty.rpy)
    $ deserters = loyalty_deserters()
    while deserters:
        call l_pilot_desert(deserters.pop(0)) # see src/MSG/SCRIPT/pilot_lines.rpy
    return
