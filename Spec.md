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
