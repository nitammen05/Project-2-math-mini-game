# Handoff: Math Quest, after Round 5

Written 2026-11-16 for a fresh session that will do Round 6. Read this together with
`CLAUDE.md`, `Problem.md`, `Spec.md`, `docs/decisions/` (0001–0004), and
`handoff-round-4.md`. The older handoffs (`HANDOFF.md`, `handoff-round-2.md`,
`handoff-round-3.md`) and `decisions.md` are still accurate, except where later rounds
changed things.

## Current state

- Round 5 is done and committed. The last commit is `ed49b36`. The working tree was
  clean before this file and the CLAUDE.md edit were written. Neither one is committed
  yet; the student reviews them first.
- **All 154 tests pass**: 10 problems, 23 game, 17 sprites, 35 web (Rounds 1–3),
  11 scenes, 24 web Round 4, and 34 Round 5 tests (`tests/test_round5.py`). No earlier
  test was changed.
- Requirements, as numbered in `Spec.md`:
  - **R1** (Round 1): the game is fun and helps the user learn math.
  - **R2–R4** (Round 2): sprites, a hero picker, and opponent sprites that match their
    names.
  - **R5–R7** (Round 3): fighting-game layout, fighters facing each other, and attack
    animations.
  - **R8–R10** (Round 4): themed scenes, walking on to the next scene, and sinking into
    Dirt and Bones on defeat.
  - **R11** (Round 5): every sprite is drawn in detail (outlines, shading, a ground
    shadow, props, at least 25 shapes each).
  - **R12** (Round 5): idle animations (breathe, blink, sway, flicker, weapon at the
    ready), plus a weapon swing or fire burst on an attack, a wince when hit, and a
    still pose with shut eyes on a knockout.
  - **R13** (Round 5): heroes have personal names: Sir Aldric (knight), Zoltan
    (wizard), Wren (archer), Kaito (ninja).
  - **R14** (Round 5): on the defeat screen, the opponent vanishes and the health bars
    fade out after the hero has fallen.

## How to run it

From the project folder (`~/csc299-main/Project-2-math-mini-game`):

```bash
python3 main.py                        # starts the server on port 8000 and opens the browser
python3 main.py --port 8080 --no-browser
python3 -m unittest discover -s tests -t .   # run every test
python3 -m unittest tests.test_round5        # run one test file
```

Stop the server with Ctrl+C. Only the standard library is used. pytest isn't installed,
so the tests use `unittest`.

**Screenshots without a person:** Google Chrome is installed. Save `render_game(game)`
(or any HTML) to a file in the scratchpad, then run:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
  --disable-gpu --hide-scrollbars --window-size=680,620 --screenshot=OUT.png \
  file:///path/to/page.html
```

Use a window at least 620 px tall. At 330 px the page scrolls to the focused answer box
and the health bars are cut off.

To see one exact moment, freeze the elements you care about by adding a rule just
before `</style>`, for example
`.attack .sp-weapon{animation-play-state:paused!important;animation-delay:-0.3s!important}`.
To get a real game with real problems, use `load_problems("problems.txt")` from
`problems.py`. Pass `opponents=[OPPONENTS[3]]` to `Game` to jump straight to one
opponent.

## What Round 5 added

| File | Change |
|---|---|
| `sprites.py` | `Sprite` has a new field `given_name` (default `""`), set for the four heroes. There is a new function `hero_name(key)`. All nine sprites (4 heroes, 5 monsters) were redrawn. A comment above `HEROES` explains the part classes. `OUTLINE` and `SHADOW` are small string helpers. `UNKNOWN_MONSTER` was **not** redrawn. |
| `web.py` | The picker shows `hero.given_name` under each picture, and the hero's health bar shows `hero_name(game.hero)` instead of "You". `.sprite` now has `overflow: visible`. New keyframes: `breathe`, `squish`, `blink`, `sway`, `flicker`, `weapon-ready`, `swing`, `swing-left`, `fire-burst`, `wince` (R12), and `vanish` (R14). New rules for `.sprite .sp-*`, `.attack .sp-weapon`, `.attack .sp-glow`, `.hurt .sp-eye`, `.ko .sprite *`, `.ko .sp-eye`, `.perish .fighter.foe`, `body:has(.perish) .hud` and `.perish .dmg`. The reduced-motion block now also stops `.sprite *` and hides `.perish .foe` and the HUD. |
| `tests/test_round5.py` (new) | Round 5 tests. Helpers: `rule(selector)` returns a CSS rule's declarations from `STYLE`, `tags_with_class(svg, cls)`, `lose(g)`, `seconds(text)`. Reuses `PROBLEMS` and `between` from `tests/test_web.py`. |
| `docs/decisions/0004-animate-sprite-parts-with-css-classes.md` | The Round 5 decision record. |
| `Spec.md` | A `## Round 5` section was appended. Earlier text is unchanged. |

### Sprite part classes (R12)

Every sprite is `<ellipse class='sp-shadow' .../>` followed by one
`<g class='sp-body' ...>` that holds everything else. Inside it:

- `sp-eye`: the eyes (they blink, wince, and stay shut on a knockout).
- `sp-sway`: loose parts such as a cape, plume, beard, ears, wings or hair. The pivot
  is the top of the part unless the element's `style` sets `transform-origin`.
- `sp-glow`: the wizard's orb and sparkle, and the dragon's fire (flicker, and a burst
  on an attack).
- `sp-weapon`: one per armed sprite (all heroes, goblin, orc, troll). The CSS uses
  `transform-box: view-box`, so the pivot is written in grid units in the group's
  `style`, for example `style='transform-origin:47px 43.5px'` (the hand).
- `sp-left`: added to the weapon of a sprite drawn facing left, so it swings the other
  way. The orc is drawn facing right and mirrored, so it doesn't need `sp-left`.
- `sp-squish`: on the slime's body, which squashes more than it breathes.

### Animation timeline on defeat (seconds after the page loads)

The foe lunges (0–0.5). The hero shakes and flashes (0.2–0.9), falls (0.8–1.4), then
sinks (1.4–2.6). The old scene fades (1.4–2.4). **New:** the foe vanishes (1.4–2.2),
and the health bars and the damage number fade out (1.4–2.2 and 1.4–1.7).

## Decisions made this round, and why

1. **Parts are animated with CSS classes on SVG groups** (see ADR 0004). It needs no
   JavaScript, it reacts to the same `attack`, `hurt` and `ko` classes as Round 3, and
   one reduced-motion rule stops it all.
2. **Idle loops use `alternate`** (forwards, then backwards). The R7 test requires every
   number in an `animation:` line to be under 1.5 s, so a blink plays over 1.4 s and
   then in reverse. The eyes close for a moment about every 2.8 s.
3. **Each hero has a separate `given_name`; the picture's label stays its class word**
   (`aria-label='Archer'`), because Round 2 tests look for that exact text. Screen
   readers hear "Archer" for the picture and "Wren" in the text.
4. **The names were made up by Claude:** Sir Aldric, Zoltan, Wren and Kaito. The
   student didn't choose them.
5. **The hero's name replaces "You" on the health bar**, not just on the picker.
6. **On defeat, the foe and the health bars are hidden by CSS, not removed from the
   HTML.** Round 3 tests require `<body><div class='hud'>`, `HP 0/10` and
   `class='fighter foe attack'` on the game-over page.
7. **The damage number fades on defeat too,** so no stray "-2" is left on screen.
8. **Picker heroes animate too.** They use the same `.sprite .sp-*` rules.
9. **Sprites may draw outside their 64 × 64 box** (`overflow: visible`), so swings and
   the fire burst aren't cut off.
10. **`UNKNOWN_MONSTER` was left simple.** R11's tests cover `HEROES` and `MONSTERS`
    only.
11. **No clarifying questions were asked** (CLAUDE.md rule 5). The course instructions
    were not re-fetched, because the student said to use only the repository.

## Unresolved

- **The student hasn't tried Round 5 in a browser yet.** Ask about these:
  - Do the idle animations look calm, or too busy?
  - Do the weapon swings read clearly?
  - On defeat, do the foe and health bars vanish *after* the hero falls?
- **The defeat timing has only been checked as end states.** The freeze trick replaces
  every delay in a rule with one value, so it shows where each animation finishes, not
  the order. The end state (only Dirt and Bones plus "K.O.!") was confirmed in a
  screenshot.
- **The "K.O.!" banner stays on the game-over screen.** No one asked whether it should
  vanish along with the foe.
- **Unanswered understanding check from Round 5:** "Which CSS rule makes the knight's
  sword swing, and why does the goblin's dagger need `sp-left`?" (Answer:
  `.attack .sp-weapon { animation: swing ... }`, because the fighter box gets `attack`.
  The goblin is drawn facing left, so a forward swing turns the other way, using
  `swing-left`.)
- The Round 4 open items (the new foe's slide-in timing, and whether the ~2 s walk-on
  feels right) and the older handoffs' checks are still open.

## Warnings for the next session

- **Requirement IDs:** R1–R14 are taken, so continue from **R15**. The next decision
  record is `docs/decisions/0005-...md`.
- **Exact strings earlier tests depend on** (all still in place):
  `<body><div class='hud'>`; `class='stage'`; `class='floor'`; `class='fighter hero'`,
  `'fighter hero attack'`, `'fighter foe enter'`, `'fighter hero hurt ko'`;
  `<div class='world scene-K[ advance| perish]'>`; the backdrop markup in
  `handoff-round-4.md`; `aria-label='Knight'`, `'Wizard'`, `'Archer'`, `'Ninja'`
  (keep `Sprite.name` as the class word); `<b>Kaito</b>` in the HUD.
- **An animated sprite part must not have a `transform=` attribute.** The CSS animation
  would replace it and move the part. Put the transform on a wrapper instead. A test
  checks this.
- **Every class inside a sprite must start with `sp-`.** Otherwise it could pick up page
  styles such as `.hero`, `.foe`, `.sky` or `.fill`. A test checks this.
- **The order of the rules in `STYLE` matters.** The `.attack`, `.hurt` and `.ko` part
  rules have the same specificity as the idle `.sprite .sp-*` rules, so they work only
  because they come later. `.ko .sprite *` must stay after `.hurt .sp-eye` (a test
  checks this). `.perish .fighter.foe` uses three classes so it beats `.foe.attack`.
- **Two animations on the same property:** `vanish` uses `forwards`, not `both`.
  `both` would also apply its first frame during the 1.4 s delay and cancel the lunge.
  Do the same for any new animation that follows another on the same element.
- **`--virtual-time-budget` screenshots can show no animation at all.** In Round 5 a
  3.5 s budget showed the very first frame. Use the freeze trick for end states, and
  ask the student to watch the timing.
- **Adding a hero** now needs a `given_name`, the part classes, and an `sp-weapon` with
  its pivot. Also update `EXPECTED` in `test_R13_every_hero_has_its_personal_name`.
  Adding a monster needs the part classes too (`sp-left` on its weapon if it's drawn
  facing left), plus a scene (see `handoff-round-4.md`).
- **`STYLE` is now about 41 KB,** and `sprites.py` is about 29 KB. Every battle page
  repeats the whole style block and two detailed sprites, and end screens add four more
  sprites. That's fine locally. Serving the CSS from its own route would be the next
  step if size ever matters.
- **`:has()` is now used for the HUD fade** (`body:has(.perish) .hud`) as well as the
  picker. A very old browser would keep the health bars visible on defeat. Nothing
  breaks.
- **Prefer the Edit tool (or a small Python script) to `sed -i`,** which works
  differently on macOS.
