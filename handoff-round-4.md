# Handoff: Math Quest, after Round 4

Written 2026-11-15 for a fresh session that will do Round 5. Read this together with
`CLAUDE.md`, `Problem.md`, `Spec.md`, `docs/decisions/` (0001–0003), and
`handoff-round-3.md`. The earlier handoffs (`HANDOFF.md`, `handoff-round-2.md`) and
`decisions.md` are still accurate, except where later rounds changed things.

## Current state

- Round 4 is done and committed. The last commit is `009398f`, and the working tree was
  clean before this file and the CLAUDE.md edit were written.
- **All 120 tests pass**: 10 problems, 23 game, 17 sprites, 35 web (Rounds 1–3), plus
  11 scenes and 24 web Round 4 tests. No earlier test was changed.
- Requirements, as numbered in `Spec.md`:
  - **R1** (Round 1): the game is fun and helps the user learn math.
  - **R2–R4** (Round 2): sprites, a hero picker, and opponent sprites that match their
    names.
  - **R5–R7** (Round 3): fighting-game layout, fighters facing each other, and attack
    animations.
  - **R8** (Round 4): each opponent fights in its own themed scene.
  - **R9** (Round 4): after a knockout that brings in a new opponent, the hero walks
    into the new scene.
  - **R10** (Round 4): at 0 HP the hero falls, then sinks into the ground, and the scene
    becomes dirt and bones.

## How to run it

From the project folder (`~/csc299-main/Project-2-math-mini-game`):

```bash
python3 main.py                        # starts the server on port 8000 and opens the browser
python3 main.py --port 8080 --no-browser
python3 -m unittest discover -s tests -t .   # run every test
python3 -m unittest tests.test_web_round4    # run one test file
```

Stop the server with Ctrl+C. Only the standard library is used. pytest isn't installed,
so the tests use `unittest`.

**Screenshots without a person:** Google Chrome is installed. Save `render_game(game)`
to an HTML file in the scratchpad, then run:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
  --disable-gpu --hide-scrollbars --window-size=680,620 \
  --virtual-time-budget=1500 --screenshot=OUT.png file:///path/to/page.html
```

`--virtual-time-budget=N` lets the page run for about N milliseconds before the shot,
so you can see a chain of animations partway through. It is only approximate (see
Warnings). To check one element at an exact moment, add
`.foe.enter{animation-play-state:paused!important;animation-delay:-1.6s!important}`
just before `</style>`. This freezes that element as if 1.6 s had passed. Don't use it
on `*`: that resets every delay and breaks the chained animations.

## What Round 4 added

| File | Change |
|---|---|
| `scenes.py` (new) | A frozen dataclass `Scene(name, svg, base, ground)`. `SCENES` has `swamp`, `cave`, `camp`, `bridge`, `volcano`, `graveyard` (Dirt and Bones, R10) and `plain` (Open Field, the fallback). Each picture is drawn on a 300×100 grid by helper functions (`_sky`, `_sign`, `_bone`, `_skull`, `_swamp()`…). `scene_key(opponent)` returns the opponent's key, or `plain`. `sky_url(scene)` returns a percent-encoded `url("data:image/svg+xml,...")`. `scene_css()` writes `.scene-K > .stage`, `> .sky`, `> .floor` and `> .ground` rules. `GRAVEYARD` and `PLAIN` are the key names. |
| `game.py` | `Opponent.scene` (default `""`), set for all five opponents. Nothing else changed. |
| `web.py` | `STYLE` ends with `+ scene_css()`. The stage and floor are now wrapped in `<div class='world scene-K[ advance\| perish]'>`. During a change of scene, a `<div class='backdrop scene-OLD' aria-hidden='true'><div class='sky'></div><div class='ground'></div></div>` comes first inside the world. New `moved_on(game)` (shared with `turn_effects`) and `scene_effects(game)` → `(world_classes, backdrop_html)`. New keyframes: `walk-out`, `walk-in`, `pan-away`, `fade-away`, `sink`. `.stage` has `min-height: 180px`. Fighters have `z-index: 2`, the numbers and banner `3`, and the backdrop `1`. The reduced-motion block hides `.backdrop` and fades `.perish .hero`. |
| `tests/test_scenes.py`, `tests/test_web_round4.py` (new) | Round 4 tests. The page tests reuse `PROBLEMS` and `between` from `tests/test_web.py`. |
| `docs/decisions/0003-draw-scenes-as-svg-data-urls-in-css.md` | The Round 4 decision record. |
| `Spec.md` | A `## Round 4` section was appended. Earlier text is unchanged. |

### Animation timeline (seconds after the page loads)

- **Moving on (`advance`):** the hero lunges (0–0.5). The K.O. banner pops in at 0.8.
  The hero's sprite walks out to the right (0.9–1.4). The old scene pans left
  (1.2–2.0) while the new foe slides in (1.2–1.8). The K.O. banner and damage number
  fade out (1.2–1.5). The hero walks back in from the left (1.45–2.05).
- **Defeat (`perish`):** the foe lunges (0–0.5) and the hero shakes and flashes
  (0.2–0.9). The hero falls over (0.8–1.4), then sinks (1.4–2.6). The old scene fades
  away (1.4–2.4).

## Decisions made this round, and why

1. **Scenes are SVG pictures inside the CSS** (see ADR 0003). There are no image files,
   screen readers skip them, and the battle page still has exactly two `<svg>`
   elements, which the Round 2 test requires.
2. **Each scene comes from the name.** The monster word picks the place (Slime Swamp,
   Goblin Cave, Orc War Camp, Troll Bridge, Dragon's Volcano). The math word adds a sign
   (`+ − × ÷`). The dragon's scene has no sign.
3. **A `.world` wrapper was added instead of extra classes on `.stage`.** Round 3 tests
   look for the exact strings `class='stage'` and `class='fighter hero attack'`, so
   neither could gain a class.
4. **The walk animates the hero's `<svg>`, not the fighter box.** The box is already
   lunging, and one element can run only one `transform` animation at a time.
5. **The scene change is a chain of short animations started with delays.** The R7
   test keeps every number in an `animation:` line under 1.5 s, delays included. The
   whole change takes about 2 s.
6. **The new foe arrives together with its scene,** not after the hero walks back in.
   This kept every delay under 1.5 s.
7. **Defeating the last opponent doesn't move the hero.** There is no next scene.
8. **On defeat, the hero falls (as in R7) and then sinks.** The `sink` keyframes include
   `rotate(-90deg)`, so the fallen pose is kept while the hero moves down. The stage's
   `overflow: hidden` hides the part below the ground.
9. **Game over keeps the Dirt and Bones scene,** including after a refresh.
10. **Reduced motion:** the backdrop is hidden, so the new scene simply appears, and a
    defeated hero is shown at `opacity: 0.35`.
11. **Two new Round 4 tests were wrong and were fixed (the tests, not the code).** One
    looked for `advance` in the whole page, which is always in the `<style>`. The other
    counted `<svg>`s on the game-over page, which also has the hero picker's four.
12. **No clarifying questions were asked** (CLAUDE.md rule 5), and the course
    instructions were not re-fetched, because the student said to use only the
    repository.

## Unresolved

- **The new foe's slide-in hasn't been seen in a real browser.** In a headless
  screenshot about 1.8 s into a scene change, the Orc wasn't visible yet. It should
  have been almost in place by then. Frozen at that moment, the Orc's own animation
  *was* almost in place, so the screenshot clock is the likely cause, but this isn't
  proven. Ask the student whether the new opponent slides in smoothly or pops in late.
  Also ask whether the walk-on feels right and whether about 2 s is too slow.
- **The student hasn't tried Round 4 in a browser at all.** Ask what they saw: the five
  scenes, moving on, and losing.
- **Unanswered understanding check from Round 4:** "After a loss, which scene's picture
  is in the `.backdrop` layer, and which one is behind it?" (Answer: the backdrop holds
  the opponent's scene, which fades away. Behind it, on `.world`, is `scene-graveyard`.)
- The Round 3 checks in `handoff-round-3.md` and the older ones in
  `handoff-round-2.md` and `HANDOFF.md` are still open.

## Warnings for the next session

- **Requirement IDs:** R1–R10 are taken, so continue from **R11**. The next decision
  record is `docs/decisions/0004-...md`.
- **Exact strings earlier tests depend on:** `<body><div class='hud'>`;
  `class='stage'` and `class='floor'` (with nothing else in the class);
  `class='fighter hero'`, `'fighter hero attack'`, `'fighter foe enter'`,
  `'fighter hero hurt ko'`; `<div class='world scene-K'>`,
  `<div class='world scene-K advance'>`, `<div class='world scene-K perish'>`; and the
  exact backdrop markup quoted above. Adding a class to any of these breaks a test.
- **A battle page has two fighter `<svg>`s, but end screens have six** (the hero picker
  adds four). Count inside `.world` when you mean "on the stage".
- **The R7 test reads delays as durations.** Anything written in an `animation:`
  shorthand must use numbers under 1.5 s. A longer sequence must be chained, or the
  timing rethought.
- **`virtual-time-budget` is only approximate,** and the frozen `*` trick from Round 3
  breaks chained delays. Freeze one element at a time, as described above.
- **`STYLE` is now about 38 KB,** because every scene is in it. That is fine for now,
  but adding many scenes will make every page bigger. Serving the CSS once from its own
  route would be the next step, if that ever matters.
- **Adding an opponent now needs a scene too.** Add a `scene=` key, add a `Scene` to
  `SCENES`, and update the name mapping in `test_R8_scene_name_matches_...` (Round 4's
  test), or the opponent gets the plain scene and the test fails.
- **Data URLs must stay percent-encoded.** `sky_url` uses `quote()`. A raw `#` or `'`
  inside the url breaks the CSS. A test checks this.
- **`moved_on(game)` assumes** that a hero knockout with `status == "playing"` means a
  new opponent arrived. An endless or replay mode would break that assumption.
- **The z-index layers only work because neither `.world` nor `.stage` sets a z-index.**
  If either one does, it creates its own layering group (a "stacking context"), and the
  backdrop could cover the fighters.
- **Prefer the Edit tool (or a small Python script) to `sed -i`,** which works
  differently on macOS.
