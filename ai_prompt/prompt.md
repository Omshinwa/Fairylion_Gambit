# TODO

What's left to do. `SPECS.md` (in this folder) has the full design of the game: read it first.

## Story

- Code the next 2 maps, each with a scripted fight (see Story in `SPECS.md`):
  1. The two of them encounter kaworu, a friend of kallen. Then they fight some enemies, and kaworu takes part in a Pawn.
  2. lelouch tells them they need to go to rendezvous point A to retrieve someone before they can go to the Prince (it's on the way anyway). He doesn't tell kallen who: it's nunnally, a scientist and a mercenary. After meeting them, they fight.
- Write all the scenes for those maps. Design the maps and win conditions, and tweak or change the AI if needed.
- After those 2 maps, the ship becomes available and the random battles start: move `STORY_RANDOM_FROM` (`src/story_battles.rpy`).

## Characters

- Add the scientist and the mercenary: new characters to invent. A quick draft is enough.
- Write a dummy social dialogue for every pair of characters the player has after those 2 maps (lelouch, kallen, kaworu, nunnally, the scientist and the mercenary).
- suzaku's talk with lelouch. It must set the flag: `$ done_flag['oncePerRun'].add('suzaku_trusts_lelouch')`.
- nunnally's scripted mission, to learn to drive a Ghost with cc, or a Cannon with china:
  1. A conversation where she convinces lelouch.
  2. Put nunnally in the classroom with cc or china. This works even if the teacher hasn't learned all their skills.
  3. Put nunnally in a robot with an extra seat, with the same teacher, to finalize it. She learns the skill, and a scripted dialogue plays.
- Give each character their own lines when they leave the group (`l_pilot_desert` in `src/MSG/SCRIPT/pilot_lines.rpy`). For now everyone uses the same placeholder lines.

## World map and deployment

- The PREPARATION menu on the world map, similar to the pilot and robot stats screen: the player builds their tactic card deck (see Tactic cards) and their team presets: many slots, each a 2x8 (or 2x6) grid where they place robots and pilots.
- In the deployment, the player can quick-load a team preset if it has the same width as the board, then adjust it by hand for that board.

## The ship

- Some rare days have no battle, so everyone gets a chance to rest and use the ship's facilities.
- The ship's UI: a big hollow ship with empty spaces where the player builds and extends rooms. For now it's a placeholder grid (`SHIP_HULL_SPACES` in `src/ship.rpy`).
- The hangar: it stores the robots, and it must be upgraded to hold more robots.
- The radar room: the player can preview the enemy composition of the next fight from the world map. It works by itself once built, with no pilot needed. It needs the next battle to be made in advance.

## Tactic cards

- In game, call them TACTIC CARDS so it's explicit that they change the battle.
- For now, a pilot unlocks their tarot skill when they have learned all their skills (in the final game it should be tied to the story).
- The limited deck: in the PREPARATION menu, the player chooses which tactic cards they can use in a battle (for example, only 3 different cards).

## Robots

- The Millenium Dynasty's shop (Cannons).
- A robot destroyed in battle must be repaired with money before it can fight again.
- New upgrades:
  - Auto repair: doesn't need to be repaired after being destroyed in battle.
  - Bitcoin miner: when this robot doesn't fight, +2 money.
  - Extra seat: the robot holds 2 pilots. Every robot can get it (see Seats).
- Show the upgrades in the robot's info panel during battles. For now they only show in the CHESSMEN tab of the PILOTS list.
- Allow repainting the robot.
- Seats: only the first seat drives, except in a Queen, where both pilots are drivers. A passenger's skills don't affect the robot, and a passenger alone can't move it (already in the code). There's no way to seat a passenger yet, and the number of seats isn't displayed: each robot needs to show its seats in the UI (how many, who sits where, driver or passenger), and the preparation needs a way to put a second pilot in a robot that has a free seat.
