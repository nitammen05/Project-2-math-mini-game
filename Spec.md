I want a website where the user can play a fun game to practice math. The game should be a turn-based rpg-type of game where the user must answer questions in succession to defeat harder and harder opponents. The difficulty of opponent should be decided by the level of math problem. For instance, an opponent that prompts the user to answer basic addition problems should be considered a lesser opponent to one that prompts the user for multiplication problems. The program should read contents of a file containing the math problems and show them to the user across the course of their game play. 

## Round 2: Sprites

Requirement IDs used by the tests (R1 is the Round 1 requirement in Problem.md):

- **R1** The game is fun and helps the user practise math. (Round 1; unchanged.)
- **R2** The player and the current opponent are each shown as a sprite, a small
  picture of the character, on the battle screen.
- **R3** Before a game starts, the player chooses their sprite from a set of heroes on
  the title screen. The chosen hero is shown for the whole game. If no valid choice is
  sent, a default hero is used. "Play again" and "Try again" let the player choose again.
- **R4** Each opponent's sprite matches its name: the Slime of Sums is a slime, the
  Goblin of Minus is a goblin, the Orc of Times is an orc, the Troll of Division is a
  troll, and the Dragon of Powers is a dragon. Every opponent has its own sprite.

Constraints carried over from Round 1: Python only, standard library only, started from
the terminal with `python3 main.py`, and all earlier tests keep passing.

## Round 3: Fighting-game screen

New requirement IDs continue from Round 2 (R1–R4 are unchanged):

- **R5** The battle screen uses a classic fighting-game layout. A row of health bars
  runs across the top of the screen: the player's bar on the left and the opponent's
  bar on the right, each with the fighter's name and `HP x/y`. Below the health bars
  is a stage where both fighters stand on a shared floor, the player on the left and
  the opponent on the right. The question and answer box come below the stage.
- **R6** The two fighters face each other: the player's sprite faces right and the
  opponent's sprite faces left. Each sprite records which way it was drawn facing, and
  it is mirrored on screen when that is the wrong way.
- **R7** After each answer, a short animation shows who attacked and who took damage.
  The attacker (the player after a correct answer, the opponent after a wrong one)
  lunges toward the other fighter. The fighter that is hit shakes, flashes red, and
  shows the damage taken (for example `-2`, marked as a critical hit when it is one).
  A fighter whose HP reaches 0 falls over, and when a new opponent follows, it slides
  in after the old one falls. When a battle starts, before any answer, no one attacks.
  If the player's system asks for reduced motion, the movement is left out but the
  red flash and damage number still show who was hit.

Constraints carried over: Python only, standard library only, started from the
terminal with `python3 main.py`, and all earlier tests keep passing.

## Round 4: Themed backgrounds, moving on, and defeat

New requirement IDs continue from Round 3 (R1–R7 are unchanged):

- **R8** Each opponent fights in its own background scene that fits its name. The
  monster half of the name sets the place, and the math half adds a small detail:
  - Slime of Sums: **Slime Swamp**, a murky swamp with glowing `+` fireflies.
  - Goblin of Minus: **Goblin Cave**, a cave with stalactites, torches and `−` marks
    scratched in the wall.
  - Orc of Times: **Orc War Camp**, a camp at sunset with a spiked wooden wall and
    `×` banners.
  - Troll of Division: **Troll Bridge**, a stone bridge over a river with a `÷` sign.
  - Dragon of Powers: **Dragon's Volcano**, an erupting volcano with lava and a gold
    hoard.
  Each scene has its own sky (behind the fighters) and its own ground (the floor
  they stand on). Every opponent has its own scene. An opponent with no scene gets a
  plain one instead of breaking the page. The backgrounds are decoration only: they
  are not read out by screen readers and are not fighters, so the battle page still
  has exactly two sprite pictures.
- **R9** After the player defeats an opponent and another one follows, the player's
  sprite walks forward (to the right) off the old scene. The old scene then slides
  away to the left, revealing the new opponent's scene, and the new opponent slides
  in with it. The player's sprite then walks back in from the left to its place. This
  happens once, on the page shown right after the knockout. Defeating the *last*
  opponent does not move the player, because there is no next scene. With reduced
  motion, the new scene simply appears with no walking or sliding.
- **R10** When the player's HP reaches 0, the player's sprite falls over (as in R7)
  and then sinks down into the ground until it is gone. The opponent's scene fades
  away, and behind it is **Dirt and Bones**: an underground scene of dirt layers,
  bones and skulls. The game-over screen keeps this scene. With reduced motion, the
  scene changes at once and the defeated sprite is shown faded instead of sinking.

Constraints carried over: Python only, standard library only, started from the
terminal with `python3 main.py`, and all earlier tests keep passing. Every single
animation still lasts under 1.5 seconds (R7). The walk-and-scroll in R9 is a chain of
short animations, each started after a delay, so the whole change of scene takes
about 2 seconds.

## Round 5: Detailed sprites, idle animations, hero names, and a cleaner defeat

New requirement IDs continue from Round 4 (R1–R10 are unchanged):

- **R11** Every hero and opponent sprite is drawn in much more detail than in Round 2:
  outlines, shading and highlights, and parts such as armour, clothing, faces, hair,
  weapons and props (at least 25 shapes per sprite). Each still matches its name (R4),
  faces the way it records (R6), and is drawn on the same 64 × 64 grid.
- **R12** Sprites are animated in more detail:
  - *Idle:* while nothing else is happening, every fighter (and every hero on the
    picker) breathes, blinks, and gently moves a loose part such as a cape, plume,
    beard, ears or wings. Glowing things (the wizard's orb, the dragon's fire) flicker.
  - *Attack:* the attacker swings its weapon (or the dragon breathes a burst of fire)
    while it lunges (R7).
  - *Hurt:* the fighter that is hit squeezes its eyes shut while it shakes (R7).
  - *Knocked out:* a knocked-out fighter stops its idle movement and its eyes stay shut.
  Each loop of an idle animation lasts under 1.5 seconds, as R7 requires of every
  animation; longer-looking cycles come from playing a loop forwards then backwards.
  With reduced motion, sprites do not move at all (no idle movement either).
- **R13** Each hero has a personal name, shown instead of its class word: Sir Aldric
  (the knight), Zoltan (the wizard), Wren (the archer) and Kaito (the ninja). The name
  is shown under the hero on the picker and on the player's health bar in battle
  (instead of "You"). The picture itself is still described to screen readers by its
  class ("Knight", "Wizard", ...), as in Round 2.
- **R14** On the defeat (game-over) screen, after the hero has fallen, the opponent's
  sprite vanishes and the health bars fade away, leaving the sinking hero in the Dirt
  and Bones scene (R10). They stay in the page (so the final HP is still there for
  screen readers) but are no longer visible. With reduced motion they are hidden at
  once. Winning does not hide anything.

Constraints carried over: Python only, standard library only, started from the
terminal with `python3 main.py`, and all earlier tests keep passing.

## Round 6: Sound

New requirement IDs continue from Round 5 (R1–R14 are unchanged). The student chose
(when asked) that heroes "speak" in made-up character babble rather than real words,
and that the game stays Python + HTML only, with no JavaScript.

- **R15** The game has sound. Every sound (music, voices and effects) is made by the
  Python program itself, with the standard library only, as a WAV file. No sound
  files are downloaded or stored in the project. The server sends them at
  `/sound/<name>.wav`; any other sound name is "404 Not Found". Pages play them with
  plain HTML `<audio>` tags, and no page contains JavaScript. The battle music has a
  small visible player, so the player can pause it, change the volume, or start it if
  the browser blocked it from starting on its own.
- **R16** Each opponent has its own music, which loops for as long as the player
  fights that opponent and fits its name:
  - Slime of Sums: **Swamp Bounce**, a slow, bouncy, happy tune.
  - Goblin of Minus: **Sneaky Cave**, a quick, tiptoeing minor tune.
  - Orc of Times: **War Drums**, a marching tune with heavy drums.
  - Troll of Division: **Bridge Stomp**, a slow, low, heavy tune.
  - Dragon of Powers: **Volcano Fury**, a fast, fiery tune.
  Every opponent's music is different. An opponent with no music gets a plain default
  tune instead of breaking the page. Because every answer loads a new page, the music
  picks up about where it was on the previous page, and starts from the beginning
  when a new opponent appears. When the game ends, the music stops and a short tune
  plays once instead: a fanfare for a victory, a sad tune for a defeat.
- **R17** Each hero has a voice line: a short burst of babble (under 1.5 seconds)
  with its own pitch, sound and rhythm, so each hero sounds different. Because the
  game has no JavaScript, it plays when the player starts a game with the hero they
  selected (the first battle page, before any answer), not on the click itself. It
  doesn't play again after an answer.
- **R18** Every attack and every hit has a sound. After each answer, the attacker's
  attack sound plays as it lunges (R7). Each fighter has its own: a sword swish
  (Sir Aldric), a magic zap (Zoltan), a bow twang (Wren), a shuriken whoosh (Kaito), a
  splat (slime), a dagger stab (goblin), a club thump (orc), a heavy smash (troll) and
  a roar of fire (dragon). As the hit lands, a damage sound plays for the fighter that
  was hit: one for the hero and one for an opponent. A critical hit and a knockout
  each add a sound of their own. Each of these sounds lasts under 1.5 seconds. No
  attack or damage sound plays when a battle starts, before any answer.

Constraints carried over: Python only, standard library only, started from the
terminal with `python3 main.py`, and all earlier tests keep passing.
