# Handoff: Math Quest, after Round 3

Written 2026-11-14 for a fresh session that will do Round 4. Read this together with
`CLAUDE.md`, `Problem.md`, `Spec.md`, `docs/decisions/`, and `handoff-round-2.md`.
`HANDOFF.md` and `decisions.md` (Round 1) are still accurate, except where Rounds 2 and 3
changed things. The main change is that the battle screen layout in `decisions.md` #24 has
been replaced (see below).

## Current state

- Round 3 is done and committed. The last commit is `887852d`, and the working tree was
  clean before this file was written.
- **All 85 tests pass** (10 problems, 23 game, 17 sprites, 35 web). 29 of them are new
  in Round 3.
- Requirements, as numbered in `Spec.md`:
  - **R1** (Round 1): the game is fun and helps the user learn math.
  - **R2–R4** (Round 2): sprites, a hero picker, and opponent sprites that match their
    names.
  - **R5** (Round 3): fighting-game layout. Health bars run across the top, with the
    player on the left and the opponent on the right. Below them both fighters stand on
    a shared stage floor.
  - **R6** (Round 3): the fighters face each other. The hero faces right and the
    opponent faces left.
  - **R7** (Round 3): short animations show who attacked and who took damage.

## How to run it

From the project folder (`~/csc299-main/Project-2-math-mini-game`):

```bash
python3 main.py                        # starts the server on port 8000 and opens the browser
python3 main.py --port 8080 --no-browser
python3 -m unittest discover -s tests -t .   # run every test
```

Stop the server with Ctrl+C. Only the standard library is used, and pytest isn't
installed, so the tests use `unittest`.

**Seeing the screen without a person:** Google Chrome is installed, so the page can be
screenshotted in headless mode (Chrome running with no window). Save `render_game(game)`
to an HTML file in the scratchpad, then run:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
  --disable-gpu --hide-scrollbars --window-size=680,620 \
  --screenshot=OUT.png file:///path/to/page.html
```

To freeze an animation partway through, add
`*{animation-play-state:paused!important;animation-delay:-0.3s!important}` just before
`</style>`. Two things to know:
- Use a window at least 620 px tall. At 260 px tall, the page came out blank.
- A screenshot without a pause is taken at time 0. Anything with a delay, like the new
  opponent's slide-in, won't have happened yet.

## What Round 3 added

| File | Change |
|---|---|
| `game.py` | A new frozen dataclass `Turn(attacker, damage, crit, knockout, foe)`. `Game.last_turn` is `None` until the first answer, then holds the last `Turn`. `attacker` is `"hero"` or `"foe"`. `foe` is the opponent that was hit, so after a knockout it is the *defeated* one, not `game.opponent`. |
| `sprites.py` | `Sprite.faces` (`"left"` or `"right"`, default `"right"`). `MIRROR` is the SVG transform that flips a 64×64 drawing. `render_hero` and `render_monster` take `facing=` and wrap the shapes in `<g MIRROR>` when it differs from `faces`. A bad `facing` raises `ValueError`. The pupils of the Slime, Goblin and Dragon now look left. |
| `web.py` | `FIGHTER_SIZE = 120`. `page(body, heading=True)` hides the `<h1>` on the battle screen. The battle screen is `.hud` (bars + "VS"), then `.stage` with `.fighter.hero` and `.fighter.foe`, then `.floor`. `turn_effects(game)` turns `last_turn` into the classes `attack`, `hurt`, `ko` and `enter`, a `.dmg` number (`at-hero`/`at-foe`, `crit`) and a `.ko-banner`. The `STYLE` string gained keyframes and a `prefers-reduced-motion` block. The old `.arena` layout is gone. |
| `tests/` | `TestLastTurn` (game), `TestFacing` (sprites), and `TestFightingLayout`, `TestAttackAnimations` and one server test (web) |
| `docs/decisions/0002-animate-attacks-with-server-chosen-css-classes.md` | The Round 3 decision record |
| `Spec.md` | A `## Round 3: Fighting-game screen` section was appended. Earlier text is unchanged. |

## Decisions made this round, and why

1. **The animations are CSS, chosen by the server** (see ADR 0002). The game has no
   JavaScript, and every answer reloads the page. So the server adds classes, and the
   browser plays the CSS animations once on load. This keeps the game Python-only and
   testable with string checks.
2. **No clarifying questions were asked,** because CLAUDE.md rule 5 forbids asking about
   implementation. How each requirement was read is written into `Spec.md` instead.
3. **The heading is hidden on the battle screen,** so the health bars really are at the
   top (R5). The title and end screens still have it.
4. **The bars drain toward the outer edges,** as in classic fighting games. The info line
   (stage, score, streak) moved below the stage.
5. **Facing is recorded per sprite, not assumed.** The Orc holds its axe on the right, so
   it is mirrored. The Troll was already facing left. The Slime, Goblin and Dragon faced
   straight ahead, so their pupils were shifted to look left (and the Goblin and Dragon
   got pupils).
6. **A mid-game knockout shows the new opponent sliding in,** not the old one falling.
   The Round 2 test `test_R4_battle_sprite_changes_with_the_opponent` requires that the
   defeated sprite is gone. A "-N" and "K.O.!" show where it stood. A *final* knockout
   (win or loss) does show the loser falling over.
7. **A new battle has no animation** (`last_turn is None`).
8. **The damage number stays on screen** after the animation ends instead of fading, so
   a player who looks late still sees it.
9. **Refreshing the page replays the last animation.** That was accepted to avoid
   changing game state on a GET request.
10. **People whose system asks for reduced motion** get no movement, but keep the red
    flash and the damage number.
11. **Timings:** the lunge takes 0.5 s, the hit runs from 0.2 to 0.9 s, the fall starts
    at 0.8 s, and the new opponent arrives at about 1.8 s. A test keeps each single
    animation duration under 1.5 s.

## Unresolved

- **The student hasn't confirmed what they saw in a real browser.** They asked how to
  run the game, and were told. Ask whether it is always obvious who hit whom, and
  whether the timings feel right. The new opponent arriving about 1.8 s after a
  knockout may feel slow.
- **Unanswered understanding checks.** Ask again:
  1. After a wrong answer, which fighter gets `attack` and which gets `hurt`?
     (Answer: the foe gets `attack` and the hero gets `hurt`.)
  2. Why does the page need `game.last_turn` instead of working out the animation from
     the HP? (Answer: HP alone doesn't say who just attacked, whether it was a crit, or
     which opponent was knocked out before the next one arrived.)
  3. What do you see if you refresh after pressing Ctrl+C? This is still open from
     Rounds 1 and 2. (Answer: the browser can't connect, because the server has stopped.)
- The two Round 2 checks in `handoff-round-2.md` and the Round 1 learning threads in
  `HANDOFF.md` are still open.

## Warnings for the next session

- **Requirement IDs:** R1–R7 are taken, so continue from **R8**. The next decision
  record is `docs/decisions/0003-...md`.
- **Don't assert that CSS class names are absent from the whole page.** `STYLE` is
  inside every page, so a name like `at-foe` is always present in the `<style>` block.
  Look for `class='dmg at-foe` instead. Two Round 3 tests failed this way. The fix was to
  the tests, not the code.
- **With the test problem set `PROBLEMS`** (one addition problem, a Slime with 3 HP), the
  finishing blow is a critical hit (`CRIT -2`), because it is the 3rd correct answer in a
  row.
- **Transform clash in CSS:** one element can only run one `transform` animation at a
  time. The lunge, shake and fall all use `transform`. They work together only because
  each runs on its own element or at a different time. The facing flip lives *inside*
  the SVG (`<g transform>`), so it never clashes with them. Keep it that way.
- **`turn_effects` decides "a new opponent arrived" by checking** `knockout`, a target of
  `"foe"`, and `status == "playing"`. If a new mode (for example, endless) changes when
  the status stays `"playing"`, revisit this.
- **Adding a new sprite now needs a `faces=` value** if it was drawn facing left, or
  `test_R6_...` may expect the wrong mirroring. Opponents still need the four things
  listed in `handoff-round-2.md`.
- **`hp_bar` output must keep containing `HP x/y` and the opponent's name,** and the
  battle screen must keep starting with `<body><div class='hud'>`. Tests check both.
- **Prefer the Edit tool to `sed -i`,** which works differently on macOS.
