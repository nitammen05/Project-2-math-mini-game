# Handoff: Math Quest, after Round 2

Written 2026-11-14 for a fresh session that will do Round 3. Read this together with
`CLAUDE.md`, `Problem.md`, `Spec.md`, `docs/decisions/`, and the Round 1 notes in
`HANDOFF.md` and `decisions.md`. Those two Round 1 files are still accurate, except for
what this file says changed.

## Current state

- Round 2 is done and committed. The last commit is `581345b`, and the working tree was
  clean before this file was written.
- **All 56 tests pass** (10 problems, 16 game, 19 web, 11 sprites). 33 of them are from
  Round 1, and 23 are new in Round 2.
- Round 2 requirements, as numbered in `Spec.md`:
  - **R1** (Round 1): the game is fun and helps the user learn math.
  - **R2**: the player and opponents are shown as sprites.
  - **R3**: the player chooses their sprite.
  - **R4**: each opponent's sprite matches its name.

## How to run it

From the project folder (`~/csc299-main/Project-2-math-mini-game`):

```bash
python3 main.py                        # starts the server on port 8000 and opens the browser
python3 main.py --port 8080 --no-browser
python3 -m unittest discover -s tests -t .   # run every test
```

Stop the server with Ctrl+C. Only the standard library is used, so nothing needs to be
installed. pytest is not available, so the tests use `unittest`.

## What Round 2 added

| File | Change |
|---|---|
| `sprites.py` (new) | `Sprite(name, svg)`, `HEROES` (knight, wizard, archer, ninja), `DEFAULT_HERO = "knight"`, `MONSTERS` (slime, goblin, orc, troll, dragon), `UNKNOWN_MONSTER`, `hero_or_default`, `render_hero`, `render_monster` |
| `game.py` | `Opponent.sprite: str = ""`, a key into `MONSTERS`. `Game(..., hero=None)` stores `self.hero` through `hero_or_default`. |
| `web.py` | `start_button` was replaced by `start_form(text, selected)`, which adds a radio-button hero picker. It is used on the title, victory and game-over screens. The battle screen is an `.arena` with the hero and HP bar on the left and the monster and HP bar on the right. `POST /start` reads the form field `hero`. |
| `tests/test_sprites.py` (new) | Tests for the sprites, plus R3 tests added to `test_game.py` and R2–R4 tests added to `test_web.py` |
| `docs/decisions/0001-draw-sprites-as-inline-svg.md` | The first decision record, written as a Y-statement |
| `Spec.md` | A `## Round 2: Sprites` section was appended. The Round 1 text is unchanged. |

## Decisions made this round, and why

1. **Sprites are inline SVG built in Python** (see ADR 0001). This keeps the game
   Python-only, with no image files and no new routes. Emoji were rejected because there
   are no slime, goblin or troll emoji.
2. **R4 is enforced by a naming rule.** `Opponent.sprite` must equal the first word of the
   opponent's name in lowercase, and `test_R4_sprite_matches_opponent_name` checks it.
3. **Bad or missing hero choices quietly become the Knight.** A form value should never be
   able to break the page or reach the HTML unescaped.
4. **"Play again" and "Try again" show the picker again,** with the current hero already
   selected, so players can change heroes between games.
5. **An opponent without a sprite gets a grey "?" placeholder** instead of crashing.
6. **`Opponent.sprite` has a default of `""`,** so existing code and tests that build an
   `Opponent` without it still work.
7. **Smaller choices:** sprites are 96 px in battle and 72 px in the picker. The chosen
   hero gets a gold border (CSS `:has()`), and the radio circles are hidden. Every sprite
   has an `aria-label` for screen readers, and a monster's label is its full name. The
   ninja's colours were lightened because it was nearly invisible on the dark background.
8. **The student's uncommitted `Problem.md` edit (the Round 2 requirements)** was
   committed as its own commit before any other work.

## Unresolved

- **The student hasn't seen the game in the browser this round.** All checks so far were
  automated tests, a scripted request to the real server, and a rendered preview image of
  the sprites. Ask the student whether the sprites look right to them.
- Two understanding checks were asked and not answered yet. Ask them again:
  1. What happens with `Opponent("Ghost of Fractions", "fractions", 8, 4)`, which has no
     `sprite=`? (Answer: the battle shows the grey "?" placeholder. Both
     `test_R4_every_opponent_has_a_sprite` and `test_R4_sprite_matches_opponent_name`
     fail. It would also be skipped completely unless `problems.txt` has `fractions`
     problems.)
  2. What happens if you refresh the page after pressing Ctrl+C? (Answer: the browser
     can't connect, because the server has stopped.) This was also unanswered in Round 1.
- The three Round 1 learning threads in `HANDOFF.md` are still open.

## Warnings for the next session

- **`Spec.md` vs. "do not edit original files":** the student chose to *append* a round
  section to `Spec.md` and never change earlier text. A proposed standing rule for this
  is in `CLAUDE.md`. Check that the student kept it.
- **Requirement IDs:** R1–R4 are taken, so continue from **R5**. Every test name includes
  the requirement ID it checks (`test_R4_...`).
- **Decision records:** the next one is `docs/decisions/0002-...md`. Last round's
  `decisions.md` at the top level is older and not numbered, so leave it as it is.
- **New opponents need four things:** an `Opponent` entry with `sprite=` set to the first
  word of its name, a matching entry in `sprites.MONSTERS`, problems in `problems.txt`,
  and possibly an update to the `eval`-based answer check in `tests/test_problems.py` if
  the new problems use new symbols.
- **SVG text uses single quotes** inside Python triple-quoted strings. Labels go through
  `html.escape(..., quote=True)`. Never put user input into an SVG unescaped.
- **`hp_bar` output must keep containing `HP x/y` and the opponent's name,** because older
  tests check for those strings.
- **Tests may be wrong too.** In Round 2, one new test failed because it looked for
  `<svg` inside `Sprite.svg`, which holds only the inner shapes. The test was fixed, not
  the code. Read a failure before changing code to make it pass.
- `sed -i ''` is the macOS form of the command. The student may be on a different shell
  setup, so prefer the Edit tool.
