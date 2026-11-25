# DAY
# One battle = one day (see The ship in ai_prompt/prompt.md). A new day starts when a won battle
# goes back to the map: l_map_select calls l_new_day. Story mode only (roguelite doesn't use the map).
# It's a label rather than a python function because it plays dialogue: call l_new_day
#
# Later, the ship's rooms and tech points can be added here.

label l_new_day:
    # first, the rewards of the day's battles: EXP and rest (see src/battle_rewards.rpy)
    if rewards_pending:
        call l_story_day_rewards

    # Grey pilots may leave the group, after a short talk with lelouch (see src/loyalty.rpy)
    $ deserters = loyalty_deserters()
    while deserters:
        call l_pilot_desert(deserters.pop(0)) # see src/MSG/SCRIPT/pilot_lines.rpy
    return
