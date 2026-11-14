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
