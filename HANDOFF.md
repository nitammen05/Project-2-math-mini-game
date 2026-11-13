# Handoff: Math Quest (Project 2)

Last updated: 2026-11-13

## Status
The game is built, working, and committed. All 33 tests pass. How to run it and how
to run the tests are in `README.md`, which the student wrote.

## What the project is
A turn-based math RPG played in the browser (from `Spec.md`). The player answers
problems to defeat five opponents in order. Each opponent is tougher than the last:
addition, subtraction, multiplication, division, then exponents. Problems are read
from `problems.txt`.

## Rules to keep following (from this folder's `CLAUDE.md`)
- Write the program only in Python. Never edit or delete the original files
  (`CLAUDE.md`, `Problem.md`, `Spec.md`).
- Write tests during and after each new function.
- Don't ask the student how to implement things; make reasonable decisions.
- The course-wide `../CLAUDE.md` still applies: teach as you go, explain terms,
  check understanding, and commit after changes.

## Decisions already made (don't revisit them)
- **"Website" vs. "Python only, run from the terminal":** `main.py` starts a local
  web server built with the standard library (`http.server`). The HTML is generated
  inside `web.py`, so there are no separate HTML or JS files.
- **Tests:** `unittest`, because pytest isn't installed. Nothing needs to be installed.
- **Game state:** kept in memory and looked up by a session cookie, so restarting the
  server resets every game.

## Code map
| File | Job |
|---|---|
| `problems.txt` | `category \| question \| answer` per line; `#` starts a comment |
| `problems.py` | `parse_line`, `load_problems`, `check_answer`, `pick_problem` |
| `game.py` | `Opponent`, `OPPONENTS`, and the `Game` class with the battle rules (balance constants are at the top) |
| `web.py` | Page rendering, the `make_handler` routes (`GET /`, `POST /start`, `POST /answer`), and `make_server` |
| `main.py` | Command-line entry point (`--port`, `--problems`, `--no-browser`) |
| `tests/` | One test file per module; `test_web.py` starts a real server on port 0 |

Game rules: a correct answer deals 1 damage, and every 3rd correct answer in a row
deals 2 (a critical hit). A wrong answer lets the opponent hit back. The player has
10 HP and heals 3 after each win. Problems don't repeat until all problems in that
category have been used.

## Learning threads to pick up
These questions were asked but never answered, so ask them again:
1. Why are the battle rules in `game.py` kept separate from `web.py`? (Answer: it lets
   the rules be tested without a server, and it separates concerns.)
2. Which test catches a wrong answer in `problems.txt`? (Answer:
   `test_real_problems_file_has_every_answer_correct`.) Check that the student
   restored the file if they tried this.
3. What happens when the page is refreshed after Ctrl+C? (Answer: the browser can't
   connect because the server has stopped.)

## Possible next steps (only if the student wants them)
- Save high scores to a file.
- Let the player choose a difficulty or start at a given opponent.
- Add more categories (fractions, order of operations). Each new category needs a new
  `Opponent` entry and problems in `problems.txt`.
- Answers must be whole numbers, so problems with decimal answers would need changes
  to `check_answer`.
