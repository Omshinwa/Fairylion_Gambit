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
- `kallen`: a Middle Kingdom soldier, known as "the Lion of the battlefield". Blunt and proud, like Kallen in Code Geass. A royalist: she loses 4 Trust every time you recruit a non-royalist.
- `suzaku`: the Prince of the Middle Kingdom (`young_suzaku` in the flashback). He loses 2 Trust every time you deploy him, and gains 2 Trust every time he isn't deployed. After talking with lelouch, he stops losing Trust when deployed.
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

The world map also has a PREPARATION menu, similar to the pilot and robot stats screen. There, the player builds their tactic card deck (if they have any cards) and their team presets: many slots, each a 2x8 (or 2x6) grid where they place robots and pilots, so they don't have to place every piece by hand before each battle.

## Deployment

Deployment is the step right before a battle starts, where the player makes their last adjustments. Once the world map is unlocked, the player can arrange their army. They prepare the 16 squares available to them, choosing where the robots are placed and who pilots them. They can quick-load a team preset if it has the same width as the board, then adjust it by hand for that board. The king must start in the middle of the back row (e1 for White on an 8x8 board). The Middle Kingdom is always white.

## The ship

Like in XCOM, there are micro and macro plays: the micro plays are the fights, the macro is improving your technology tree, getting passive buffs, etc.

In the final game, after the player rescues suzaku, they negotiate with the UN and the Millenium Dynasty, who provide a huge ship that acts as a hangar for the CHESSMEN. For this debug build, make the ship available earlier: right after the 2 new maps.

One battle = one day: it's the basic unit of time. Some rare days have no battle, so everyone gets a chance to rest and use the ship's facilities.

Each day, the player chooses how to develop the ship, such as building new rooms. This works like a technology tree that costs tech points: most rooms must be researched before they can be built. For example: research training rooms (2 tech points), then build a training room (2 tech points), then build another one (2 tech points), which extends the room so it holds 2 pilots. A room can't be used on the day it is extended.

Robots that don't fight generate tech points. Keep the macro play pleasant: planning each day shouldn't be tedious.

The ship's UI is a big hollow ship with empty spaces where the player builds and extends rooms. The rest of the ship is the basic rest space, where all 16 pilots can slot in. There's also a hangar that stores the robots, and it must be upgraded to hold more robots.

### Rooms

Rooms are places in the ship where the player puts pilots to spend a day. Pilots in a room can't take part in fights that day. Each room has a specific effect, and most rooms must be built first.

- Heavy gravity room: +2 XP, but they don't rest.
- Training room: +1 XP, and they also rest.
- Rest room: +2 stamina instead of +1. If it's big enough for 2 pilots and 2 pilots are in it, they take a break together (sometimes show a small dialogue of the two sharing a coffee).
- Healing tank: restores all stamina, but costs a lot to build.
- Radar room: the player can preview the enemy composition of the next fight from the world map. It works by itself once built, with no pilot needed.
- Classroom: must be 2 pilots. One pilot must have learned all their skills: they become the teacher and transfer all their XP to the second pilot, the student for that day.

# Pilots

Each character can pilot certain robots.
Each has a STAMINA (`health` in the code, `max_health` in `PILOTS.csv`). It decreases by 1 every time they are captured in battle. Every pilot who doesn't fight rests by default and gets +1 stamina, like in roguelike mode (`pilot.rest()` in `src/roguelike.rpy`). Pilots in the heavy gravity room are the exception.

## Pilot screen (to do later)

The pilot screen (`s_character_info` in `src/PILOT_screen.rpy`) needs tabs:

- Stats: stamina, experience, the Trust stat shown as LOYALTY (for example "LOYALTY: 5 (Good)"), and the icons of the learned skills.
- Skills: learn new skills and see what each one does (the current "- skills -" and "- learn -" part).
- Relationships: the pilot's affinity with every other character (see Trust and affinity).

## Permadeath

Characters can die if they lose all their stamina. Then, when they should talk, the Ren'Py engine skips them (I set up a special condition in the Character arguments).

- `DEAD_OR_DESERT` (in `src/game_manager.rpy`): the list of characters who died or left the group. A character in this list doesn't talk anymore: their Character condition `canTalk()` returns False.
- `IN_FLASHBACK` (in `src/CONSTANTS.rpy`): set it to True during flashbacks. Then `canTalk()` ignores `DEAD_OR_DESERT`, so dead or departed characters still talk.

## Trust and affinity

Each character has an affinity with every other character. Lelouch's affinity with a character is their Trust: how much the character trusts Lelouch and their faction. Otherwise, affinity is a number that increases:

- +1 with each other for all pilots who take part in the same fight.
- +3 with each other for all pilots in the same room of the ship.

- When 2 characters have high enough affinity, a social discussion is triggered, like in Fire Emblem or Persona.
- Queen: a pilot with `drive_q` can drive a Queen alone. Otherwise, 2 pilots with high affinity can drive a Queen together: one who can drive the Rook and one who can drive a minor piece. Keep `drive_q` working, since roguelike mode uses it. I may later remove it from story mode only.
- A tab displays every character and their current affinity with the others.

Since Trust is lelouch's affinity, it follows the same rules: it goes up when a pilot fights alongside lelouch or shares a room with him. Some characters also have unique Trust rules (see Characters).

### Loyalty

Trust sets a loyalty level, and each level has its own color and effect. Implemented in `src/loyalty.rpy` (`TRUST_TO_LOYALTY`, `loyalty_of()`).

Small hearts show the stamina a pilot won't risk: they can only be deployed with more stamina than that. Pilots with 1 max stamina can't be deployed if their Trust is too low. Show each level's effect in the pilot stats menu as a passive, so the player remembers it.

| Trust | Color | Effect |
|---|---|---|
| 20 or more | Red | Trust gains are doubled. +2 stamina per rest instead of +1. |
| 10 to 19 | Blue | Normal. |
| 0 to 9 | Green | Default. Won't fight if they could die: 1 small heart, so they need 2 stamina to be deployed. |
| -10 to -1 | Yellow | Only fights with full stamina: every heart is small except the last one. |
| below -10 | Grey | Same as Yellow, and 50% chance to leave the group at the start of each day. |

In roguelite mode, every pilot is locked at Blue (for now `loyalty_of()` returns Blue whenever a roguelite run is active).

A character who leaves goes into `DEAD_OR_DESERT`. Before they leave, a short conversation plays (2 or 3 lines) where the pilot tells lelouch why they're leaving.

## Skills

Each pilot has skills (see `PILOTS.csv` and `src/PILOT_SKILLS.rpy`): driving skills (which robots they can pilot), setup skills like Castle or Initiative, and one-time skills like Stamina Up.

### Tactic cards

Tactic cards are themed on tarot cards. In game, call them TACTIC CARDS so it's explicit that they change the battle.

When a character progresses in the story, they gain a tarot skill that unlocks their tarot card. For example, lelouch is the Magician: he makes his plans reality. In the final game this should be tied to the story, but for now a pilot unlocks their tarot skill when they have learned all their skills.

During a battle, the player can play tactic cards. Each card has an effect that totally changes the rules of chess for 1 move. For example, the Fool: skip your turn.

The player has a limited deck: in the PREPARATION menu, they choose which tactic cards they can use in a battle (for example, only 3 different cards).

A few cards already exist in `src/TAROT.rpy` and `src/PILOT_SKILLS.rpy` (`Tarot_skill`): the Fool, the Magician (`magicien`) and the Empress.

## Robots

On the world map, the player clicks the UN or the Dynasty country to buy more robots and robot upgrades with money. The upgrades mostly reward keeping robots out of battle when you can.

- Bitcoin miner: when this robot doesn't fight, +2 money.
- Speed up the development of the ship.
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