This is the Ren'Py folder of a chess game I'm making: a story-based RPG with fights very similar to chess.
Think of a Fire Emblem campaign, but with chess gameplay.
The pieces are huge robots called CHESSMEN. The characters pilot those robots, which move like chess pieces.

I only wrote a few maps. Based on them, I want you to build:
- the world map, the deployment and the affinity tab (see Gameplay),
- the ship and its rooms (see The ship),
- the next 2 maps, each with a scripted fight: one after meeting kaworu, and one after meeting nunnally, the scientist and the mercenary (see Story).

After those 2 maps, the ship becomes available, and all the following fights are randomized, endlessly, with the same generator as the roguelike mode (`setup_rogue()` in `src/roguelike.rpy`).

Put the code for each system in its own .rpy files so it can easily be black-boxed.

Write all the scenes for those maps. Use my scripting system to make the characters appear on screen and talk. Design the maps and win conditions, and tweak or change the AI if needed. Write a dummy social dialogue for every pair of characters the player has after those 2 maps (lelouch, kallen, kaworu, nunnally, the scientist and the mercenary). Render images yourself if you need to.

Ask me questions if you're unsure about some designs. Fill in 'prompt.md' whenever I answer your questions.

The names I use for the characters are their ids. `PILOTS.csv` lists most of the characters with their id, their name, and how I worked out their skills.

# Countries

The game is about a conflict. The names of the countries are kept vague in game, and the player can change them (see custom_names.rpy).

THE HOLY EMPIRE: the bad guys. Similar to Russia and China.
THE MIDDLE KINGDOM: in the past, they and the Holy Empire were a single country. It became independent after the country collapsed into the Holy Empire. They are similar to Taiwan or Ukraine. They are the protagonist faction.
THE UNITED NATIONS: a faraway ally of the Middle Kingdom. They are similar to the US and Europe: they help the Middle Kingdom indirectly, but never interfere directly for fear of a nuclear war with the Holy Empire. They could have dark skin.
THE MILLENIUM DYNASTY: a country with a rich history. They help the Middle Kingdom more directly, and they have the Cannon piece (from xiangqi, Chinese chess). In general they are very Asian-coded.

`world_map.webp` (in this folder) gives an idea of the world map. The big red country is the Holy Empire. The small white country is the Middle Kingdom.

# Story

The story progresses through maps with objectives that the player must complete.

The main hero, lelouch, is the prince of the Holy Empire. But the Holy Empire is very cruel: it follows an extreme Darwinism where everyone is forced to fight. Lelouch had to fight his sister (nunnally) in some cruel training. They faked their deaths and fled to the Middle Kingdom, and have been hiding there ever since. When the story truly starts, Lelouch is 25. He spent the last 10 years financing his project: because he knew how belligerent THE HOLY EMPIRE is, he prepared funds to buy his own CHESSMEN and defend against an eventual invasion.

The first tutorial maps are a flashback to 3 years ago. We play the Prince of THE MIDDLE KINGDOM, who escapes the country. His servant, jagen, dies for it. We are also introduced to stanley, a commander of the HOLY EMPIRE, and abel, someone working for jagen. Eventually the Prince (`young_suzaku`) and abel escape. 3 years later, the Prince is `suzaku`, a separate character in `PILOTS.csv`: when we meet them again, it's abel and suzaku.

We then play kallen, a soldier of the MIDDLE KINGDOM. Her superior oghi just betrayed the MIDDLE KINGDOM and is trying to capture her. A mysterious KING appears and helps kallen. It's lelouch. He keeps his identity hidden for now.

The two of them collaborate, because lelouch knows the whereabouts of the Prince. He also provides the ROOK CHESSMAN to kallen.

These are the two maps I want you to code, each with a scripted fight:

1. The two of them encounter kaworu, a friend of kallen. Then they fight some enemies, and kaworu takes part in a Pawn.
2. lelouch tells them they need to go to rendezvous point A to retrieve someone before they can go to the Prince (it's on the way anyway). He doesn't tell kallen who: it's nunnally, a scientist and a mercenary. The scientist and the mercenary aren't in the game yet, so add them. After meeting them, they fight.

# Characters

Each character has a story that can change their gameplay: unique rules that affect their relationships (especially Trust), which discussions and character development can unlock or change.

- `lelouch`: the hero, a prince of the Holy Empire (see Story). He hides his identity as the mysterious KING. Cold and calculating, like Lelouch in the anime Code Geass. His tarot card is the Magician: he makes his plans reality.
- `nunnally`: lelouch's sister. She uses a wheelchair. A mix of Rollo and Nunnally from Code Geass: she wants to be useful. She doesn't fight until she convinces lelouch to let her pilot a robot. Then she must learn to drive a Ghost with cc, or a Cannon with china. It's a scripted mission:
  1. A conversation where she convinces lelouch.
  2. Put nunnally in the classroom with cc or china. This works even if the teacher hasn't learned all their skills.
  3. Put nunnally in a robot with an extra seat, with the same teacher, to finalize it. She learns the skill, and a scripted dialogue plays.
- `kallen`: a Middle Kingdom soldier, known as "the Lion of the battlefield". Blunt and proud, like Kallen in Code Geass. She starts with some affinities already set: -2 with stanley, china and cc, and +2 with kaworu (`AFFINITY_START` in `src/affinity.rpy`, applied when a new story starts).
- `suzaku`: the Prince of the Middle Kingdom (`young_suzaku` in the flashback). He loses 2 Trust every time you deploy him, and gains 2 Trust every time he isn't deployed. After talking with lelouch, he stops losing Trust when deployed. Implemented in `src/character_rules.rpy` (counted when a battle starts). The talk with lelouch must set the flag: `$ done_flag['oncePerRun'].add('suzaku_trusts_lelouch')`.
- `kaworu`: kallen's friend. Personality and gender not decided yet.
- `oghi`: kallen's superior, who betrays the Middle Kingdom.
- `jagen`: the Prince's servant. He dies in the flashback.
- `abel`: works for jagen, and escapes with the Prince.
- `stanley`: a commander of the Holy Empire.
- `cc`: can teach nunnally to drive the Ghost.
- `china`: can teach nunnally to drive the Cannon.
- The scientist and the mercenary: new characters for you to invent. A quick draft is enough; I'll probably change them later.


# Gameplay

## World map

Between fights there is a world map where the player can see the stamina of each character and every CHESSMAN they possess. They click on the next dot for the next scripted fight. Social discussions and the affinity tab are also on the world map (see Trust and affinity). The full world map unlocks after `map_1_1`, my last written map.

Done so far: a PILOTS button on the map opens a list with two tabs. PILOTS: one row per pilot in TEAM (stamina hearts in loyalty colors, EXP, "can learn a skill", loyalty emoji); clicking a row opens their profile, where they can learn skills. RELATIONSHIPS: the affinity table of the whole TEAM (`s_relationships_table` in `src/affinity.rpy`). CHESSMEN (story mode): one row per robot the player owns (`ROBOTS`), with its class and upgrades. See `src/pilot_list.rpy`. Once the random battles start, the United Nations' country on the map opens their shop (see Robots), with the player's money under it.

The world map also has a PREPARATION menu, similar to the pilot and robot stats screen. There, the player builds their tactic card deck (if they have any cards) and their team presets: many slots, each a 2x8 (or 2x6) grid where they place robots and pilots, so they don't have to place every piece by hand before each battle.

## Deployment

Deployment is the step right before a battle starts, where the player makes their last adjustments. Once the world map is unlocked, the player can arrange their army. They prepare the 16 squares available to them, choosing where the robots are placed and who pilots them. They can quick-load a team preset if it has the same width as the board, then adjust it by hand for that board. The king must start in the middle of the back row (e1 for White on an 8x8 board). The Middle Kingdom is always white.

Pawns: the roguelite has unlimited pawns (a pilot dropped on the pawn row makes one, "♙ = ∞" in the reserve). In story mode they're limited to the PAWN robots the player owns: a pilot dropped on the pawn row takes one, and the reserve shows how many are left (`story_pawns()` in `src/story_battles.rpy`).

### Random battles

Done so far (`src/story_battles.rpy`): from `g.progress` `STORY_RANDOM_FROM` (101, right after map 1-0, since `maps/map_1_1.rpy` is still a draft without a battle) the world map shows RANDOM BATTLE and its flag starts a battle made by the roguelite's generator (`Roguelike` in `src/roguelike.rpy`, kept in `story_battles`; each win makes the next one harder). Move `STORY_RANDOM_FROM` when the next maps are written. A random battle is a normal story day: deployment (with the SHIP button), battle, the rewards on the map, the new day. It doesn't change `g.progress`. Losing reloads the checkpoint saved when the flag was clicked, like the story maps. At that point the ship unlocks and the player gets their first robots (see Robots).

## The ship

Like in XCOM, there are micro and macro plays: the micro plays are the fights, the macro is improving your technology tree, getting passive buffs, etc.

In the final game, after the player rescues suzaku, they negotiate with the UN and the Millenium Dynasty, who provide a huge ship that acts as a hangar for the CHESSMEN. For this debug build, make the ship available earlier: right after the 2 new maps.

One battle = one day: it's the basic unit of time. Some rare days have no battle, so everyone gets a chance to rest and use the ship's facilities. A new day starts in `l_new_day` (`src/day.rpy`), called by `l_map_select` when a won battle goes back to the map.

Each day, the player chooses how to develop the ship, such as building new rooms. This works like a technology tree that costs tech points: most rooms must be researched before they can be built. For example: research training rooms (2 tech points), then build a training room (2 tech points), then build another one (2 tech points), which extends the room so it holds 2 pilots. A room can't be used on the day it is extended.

Robots with the RESEARCH LAB upgrade generate tech points on the days they don't fight (see Robots). Keep the macro play pleasant: planning each day shouldn't be tedious.

The ship's UI is a big hollow ship with empty spaces where the player builds and extends rooms. The rest of the ship is the basic rest space, where all 16 pilots can slot in. There's also a hangar that stores the robots, and it must be upgraded to hold more robots.

### Rooms

Rooms are places in the ship where the player puts pilots to spend a day. Pilots in a room can't take part in fights that day. Each room has a specific effect, and most rooms must be built first.

- Heavy gravity room: +2 XP, but they don't rest.
- Training room: +1 XP, and they also rest.
- Rest room: +2 stamina instead of +1. If it's big enough for 2 pilots and 2 pilots are in it, they take a break together (sometimes show a small dialogue of the two sharing a coffee).
- Healing tank: restores all stamina, but costs a lot to build.
- Radar room: the player can preview the enemy composition of the next fight from the world map. It works by itself once built, with no pilot needed.
- Classroom: must be 2 pilots. One pilot must have learned all their skills: they become the teacher and transfer all their XP to the second pilot, the student for that day.

Done so far (parts 1 and 2, `src/ship.rpy`): a SHIP button on the world map, and one under START in the story-mode deployment, shown when `ship_unlocked` is True (set when the random battles start, see Random battles). The deployment picks who fights; the ship, opened from there, shows only the pilots who don't fight and lets the player put them in rooms. The ship screen is a placeholder: 6 empty spaces in a grid (`SHIP_HULL_SPACES`), a RESEARCH row and the rest space with every pilot who isn't in a room and doesn't fight today. Five rooms: training, rest, heavy gravity, healing tank and classroom. Each one is researched (2 TECH), then built (2 TECH), then extended once to 2 seats (2 TECH, `SHIP_ROOM_MAX_SIZE`). The healing tank costs more: 4 to research, 6 to build or extend (`SHIP_ROOM_COST`). The classroom is built with its 2 seats (`SHIP_ROOM_START_SIZE`). An extended room is closed until the next day and its pilots go back to the rest space. Pilots are moved like in the deployment: drag one onto a room (or back onto the rest space), or click it, then click the room; the rooms it can go to light up. Anyone can go in a room, Lelouch too (then he doesn't fight that day). The pilots in the ship use the same icon as the deployment's reserve (`s_pilot_icon` in `src/PILOT_screen.rpy`). Pilots stay in their room from day to day until moved, and they're left out of the deployment.
- The rewards screen (see below) shows the pilots in a room in its RESERVE column, with the room's name: their room's effect replaces their rest (`ship_room_rest`). Training: +1 EXP and a normal rest; rest room: the pilot's usual rest +1 STAMINA; heavy gravity: +2 EXP, no rest; healing tank: all their STAMINA back; classroom: both rest, and if one of them learned every skill (MAX) and the other didn't, the MAX one gives all their EXP to the other (`ship_classroom_teacher`). Nunnally's scripted lesson (a teacher who isn't MAX) isn't done yet.
- Then at each new day (`l_ship_day`, called by `l_new_day` when the ship is unlocked), a report shows +3 affinity between pilots of the same room (`AFFINITY_ROOM`) and the TECH: 10 every day (`SHIP_TECH_PER_DAY`), +2 per robot with a RESEARCH LAB that didn't fight (`ROBOT_UPGRADE_TECH`). Half the time (`SHIP_COFFEE_CHANCE`), two pilots in the rest room share a coffee: the report says so, then the label `l_coffee_<id>_<id>` plays if it's written (ids in alphabetical order).
- Not done yet: the radar room (it needs the next battle to be made in advance), the hangar, days without a battle.
- Test labels in `maps/map_test_deployment.rpy`: `l_test_story_deployment` (a deployment with the ship unlocked) and `l_test_ship_rewards` (the rewards screen with a pilot in every room, then the world map with the random battles).

# Pilots

Each character can pilot certain robots.
Each has a STAMINA (`health` in the code, `max_health` in `PILOTS.csv`). It decreases by 1 every time they are captured in battle. Every pilot who doesn't fight rests by default and gets +1 stamina, like in roguelike mode (`pilot.rest()` in `src/roguelike.rpy`). Pilots in the heavy gravity room are the exception.

After each won battle, the rewards screen (the roguelite one, `s_result_screen`) gives +1 EXP to every pilot who fought, rests the others (or gives their ship room's effect), and gives +2 EXP to the pilot(s) of the piece that made the checkmate (the winning move). In story mode it starts at map 1-0 (not during the tutorial maps 0-x) and shows once per day, on the world map right before the new day (`l_new_day`): a day can have several battles (map 1-0 has two), everyone who fought in one of them gets the +1 EXP, and the last battle's checkmate gets the +2. See `src/battle_rewards.rpy`.

## Pilot screen

The pilot screen (`s_character_info` in `src/PILOT_screen.rpy`) has three tabs:

- STATS (`s_pilot_tab_stats`): stamina, experience, value, LOYALTY (for example "5 (Average)", only the name in roguelite), the loyalty passive, the robot row, and the icons of the other learned skills.
- SKILLS (`s_pilot_tab_skills`): the learned skills with what each one does, and the skills to learn.
- RELATIONSHIPS (`s_pilot_relationships` in `src/affinity.rpy`, story mode only): the pilot's row of the affinity table, their affinity with every other pilot in TEAM, colored like the loyalty levels. With Lelouch it's Trust. The whole table is in the PILOTS list of the world map.

## Permadeath

Characters can die if they lose all their stamina. Then, when they should talk, the Ren'Py engine skips them (I set up a special condition in the Character arguments).

- `DEAD_OR_DESERT` (in `src/game_manager.rpy`): the list of characters who died or left the group. A character in this list doesn't talk anymore: their Character condition `canTalk()` returns False.
- `IN_FLASHBACK` (in `src/CONSTANTS.rpy`): set it to True during flashbacks. Then `canTalk()` ignores `DEAD_OR_DESERT`, so dead or departed characters still talk.

## Trust and affinity

Each character has an affinity with every other character. Lelouch's affinity with a character is their Trust: how much the character trusts Lelouch and their faction. Otherwise, affinity is a number that increases:

- +1 with each other for all pilots who fought on a won day (given with the day's EXP, from map 1-0 on).
- +3 more for two pilots who sat in the same CHESSMAN (a robot with an extra seat).
- +3 with each other for all pilots in the same room of the ship.
- Story mode only: roguelite mode has no affinity. Implemented in `src/affinity.rpy` (fights and seats) and `src/ship.rpy` (rooms, `AFFINITY_ROOM`).

- When 2 characters have high enough affinity, a social discussion is triggered, like in Fire Emblem or Persona. Implemented in `src/talks.rpy`: at affinity 10, 15 and 20 (`TALK_RANKS`) a pair gets a talk. A TALK button lights up under PILOTS on the world map, the pair's cell shows TALK in the RELATIONSHIPS table, and clicking it plays the label `l_talk_<id>_<id>_<number>` (ids in alphabetical order, e.g. `l_talk_kallen_kaworu_1`), or a placeholder if it isn't written yet.
- Queen: a pilot with `drive_q` can drive a Queen alone. Otherwise, 2 pilots with high affinity can drive a Queen together: one who can drive the Rook and one who can drive a minor piece. Keep `drive_q` working, since roguelike mode uses it. I may later remove it from story mode only. Implemented in `src/queen_co_drive.rpy`: affinity 10 or more (`QUEEN_CO_DRIVE_AFFINITY`), story mode only. In story mode Queens have a second seat; dropping a second pilot onto a Queen in the preparation seats them next to the first. A Queen with only half of its crew stays neutral. Test it with `jump l_test_story_deployment` (`maps/map_test_deployment.rpy`), a story-mode deployment with kallen (ROOK) and kaworu (KNIGHT) at affinity 10.
- A tab displays every character and their current affinity with the others.

Since Trust is lelouch's affinity, it follows the same rules: it goes up when a pilot fights alongside lelouch or shares a room with him. Some characters also have unique Trust rules (see Characters).

### Loyalty

Trust sets a loyalty level, and each level has its own color and effect. Implemented in `src/loyalty.rpy` (`TRUST_TO_LOYALTY`, `loyalty_of()`).

Small hearts show the stamina a pilot won't risk: they can only be deployed with more stamina than that. Pilots with 1 max stamina can't be deployed if their Trust is too low. Show each level's effect in the pilot stats menu as a passive, so the player remembers it. The STATS tab also shows an emoji after LOYALTY, from Grey to Red: 💀 🤢 😐 🙂 😄 (`LOYALTY_EMOJI` in `src/loyalty.rpy`).

| Trust | Color | Effect |
|---|---|---|
| 20 or more | Red | +2 stamina per rest instead of +1. |
| 10 to 19 | Blue | Normal. |
| 0 to 9 | Green | Default. Won't fight if they could die: 1 small heart, so they need 2 stamina to be deployed. |
| -10 to -1 | Yellow | Only fights with full stamina: every heart is small except the last one. |
| below -10 | Grey | Same as Yellow, and 50% chance to leave the group at the start of each day. |

In roguelite mode, every pilot is locked at Blue (for now `loyalty_of()` returns Blue whenever a roguelite run is active).

Lelouch has no loyalty: Trust is how much the others trust him. `loyalty_of()` returns Blue (no effect) for him, and his STATS tab has no LOYALTY row.

A character who leaves goes into `DEAD_OR_DESERT`. Before they leave, a short conversation plays (2 or 3 lines) where the pilot tells lelouch why they're leaving. Implemented: `l_new_day` (`src/day.rpy`) rolls the 50% for each Grey pilot (`loyalty_deserters()` in `src/loyalty.rpy`, never lelouch or generic pilots), and `l_pilot_desert` (`src/MSG/SCRIPT/pilot_lines.rpy`) plays the talk. For now everyone uses the same placeholder lines.

## Skills

Each pilot has skills (see `PILOTS.csv` and `src/PILOT_SKILLS.rpy`): driving skills (which robots they can pilot), setup skills like Castle or Initiative, and one-time skills like Stamina Up.

### Tactic cards

Tactic cards are themed on tarot cards. In game, call them TACTIC CARDS so it's explicit that they change the battle.

When a character progresses in the story, they gain a tarot skill that unlocks their tarot card. For example, lelouch is the Magician: he makes his plans reality. In the final game this should be tied to the story, but for now a pilot unlocks their tarot skill when they have learned all their skills.

During a battle, the player can play tactic cards. Each card has an effect that totally changes the rules of chess for 1 move. For example, the Fool: skip your turn.

The player has a limited deck: in the PREPARATION menu, they choose which tactic cards they can use in a battle (for example, only 3 different cards).

A few cards already exist in `src/TAROT.rpy` and `src/PILOT_SKILLS.rpy` (`Tarot_skill`): the Fool, the Magician (`magicien`) and the Empress.

## Robots

In story mode, the player starts with 1 KING, 1 ROOK and 1 PAWN (`STORY_START_ROBOTS` in `src/story_battles.rpy`, given when the random battles start). `ROBOTS` keeps every robot the player owns; robots destroyed in battle stay in it. The KING is the one placed in the middle of the back row; Lelouch usually drives it, but any pilot who can drive a King can take his place. The generator gives no free robots in story mode (only in the roguelite). To get more, the player buys them from the United Nations.

Done so far (`src/un_shop.rpy`): once the random battles start, the United Nations' country on the world map shows their name and the player's money (`g.money`); clicking it opens their shop, which looks like the roguelite's. CHESSMEN cost their chess value (PAWN 1, KNIGHT and BISHOP 3, ROOK 5, QUEEN 9, `UN_ROBOT_PRICE`) and join `ROBOTS`. Upgrades: the RESEARCH LAB costs 6 (`UN_UPGRADE_PRICE`), given to one of the player's robots (not the KING, which always fights). Money: each won random battle gives 7 (`STORY_MONEY_PER_WIN`, with the roguelite's flying coins). The Millenium Dynasty's shop (Cannons) isn't done.

Notes for later:
- A robot destroyed in battle must be repaired with money before it can fight again.
- A robot upgrade, "Auto repair": doesn't need to be repaired after being destroyed in battle.

On the world map, the player clicks the UN or the Dynasty country to buy more robots and robot upgrades with money. The upgrades mostly reward keeping robots out of battle when you can.

- Bitcoin miner: when this robot doesn't fight, +2 money.
- Research lab: when this robot doesn't fight, +2 TECH at the new day. Done in `src/robot_upgrades.rpy` (upgrade id `'tech'`): a robot's upgrades are `robot.upgrades`, kept when the robots are made again for each battle. The United Nations sell it; the test label `l_test_ship_rewards` gives one to the PAWN. Upgrades show in the CHESSMEN tab of the PILOTS list, not yet in the robot's info panel during battles.
- Allow repainting the robot.
- Extra seat: the robot holds 2 pilots. Usually only the first pilot drives it (except for Queens, see Trust and affinity), so the second pilot's main use is gaining affinity with the first. A robot with a free seat can also RESCUE a stray pilot by moving onto them; this is already in the code (move flag `rescue`, see `tests/test_rescue.rpy`).

## ignore

those are notes i scrambled for now, dont take that section into account

VV: "The Fairies were always going to be inevitably massacred at some point because they're genetically deficient. Or so people like to say."

### team preview or not?


team preview
* there's skills that allows knights and pawns to move first
* player has to spend time manually deploying each robot
* could have variety of board sizes
* (white by default play second)
fog of war
* there's skills that allows knights and pawns to do one extra move at the beginning?
* player doesnt have to manually construct the formation everytime, they could have presaved them
* board sizes fixed to 6 or 8 horizontally

### Difficulty

At the beginning of a run, the player can choose difficulty modifiers, like Kaycee's Mod in Inscryption. For example:
- The AI is stronger.
- The player has a 10-minute timer for each game.
- The player has a 5-minute timer for each game.
- The player gains less money per battle.
- The tarot deck is smaller.
- The enemy army can include non-standard chess units (cannon, ghost).

Each modifier adds to a score. For flavor, the score sets the world's population: in a very easy game the Middle Kingdom has only 1,000 people, and in the hardest it has 65 million. The ending then says something like "You saved 1,000 people!" It's only flavor, a way to show the difficulty multiplier.