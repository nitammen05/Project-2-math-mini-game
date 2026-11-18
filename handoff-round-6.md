# Handoff: Math Quest, after Round 6

Written 2026-11-17 for a fresh session that will do Round 7. Read this together with
`CLAUDE.md`, `Problem.md`, `Spec.md`, `docs/decisions/` (0001–0006), and
`handoff-round-5.md`. The older handoffs (`HANDOFF.md`, `handoff-round-2.md` to
`handoff-round-4.md`) and `decisions.md` are still accurate, except where later rounds
changed things.

## Current state

- Round 6 is done and committed. The last commit is `b0df8a3`. The working tree was
  clean before this file and the CLAUDE.md edit (rules 17 and 18) were written. Neither
  one is committed yet; the student reviews them first.
- **All 205 tests pass**: 10 problems, 23 game, 17 sprites, 35 web (Rounds 1–3),
  11 scenes, 24 web Round 4, 34 Round 5, and 51 Round 6 tests (`tests/test_round6.py`).
  No earlier test was changed.
- Requirements, as numbered in `Spec.md`:
  - **R1** (Round 1): the game is fun and helps the user learn math.
  - **R2–R4** (Round 2): sprites, a hero picker, and opponent sprites that match their
    names.
  - **R5–R7** (Round 3): fighting-game layout, fighters facing each other, and attack
    animations.
  - **R8–R10** (Round 4): themed scenes, walking on to the next scene, and sinking into
    Dirt and Bones on defeat.
  - **R11–R14** (Round 5): detailed sprites, idle animations, hero names, and the foe
    and health bars vanishing on defeat.
  - **R15** (Round 6): every sound is made by Python (standard library) as WAV, served
    at `/sound/<name>.wav`, and played with `<audio>` tags. There's no JavaScript. The
    music has a visible player.
  - **R16** (Round 6): each opponent has its own looping music, which picks up where it
    was after each answer. There's a default tune for an opponent without music, and a
    victory or defeat jingle at the end.
  - **R17** (Round 6): each hero has a babble voice line (under 1.5 s). It plays on the
    first battle page of a game.
  - **R18** (Round 6): every fighter has its own attack sound. There are damage sounds
    for the hero and the foe, plus a crit sound and a knockout sound. Each effect lasts
    under 1.5 s.

## The student's answers this round

The student was asked two questions before any code was written (Round 6 is the first
round where questions were asked):

1. **Voice line:** made-up character babble, not real spoken words.
2. **JavaScript:** none. Python + HTML only. As a result, the voice line plays when a
   game starts, not the instant a hero is clicked. This is now standing rule 17 in
   CLAUDE.md.

## How to run it

From the project folder (`~/csc299-main/Project-2-math-mini-game`):

```bash
python3 main.py                        # starts the server on port 8000 and opens the browser
python3 main.py --port 8080 --no-browser
python3 -m unittest discover -s tests -t .   # run every test
python3 -m unittest tests.test_round6        # run one test file
```

Stop the server with Ctrl+C. Only the standard library is used. pytest isn't
installed, so the tests use `unittest`.

**Listening to one sound:** while the server runs, open
`http://127.0.0.1:8000/sound/music-war-drums.wav` (or any name from
`sounds.sound_names()`) in the browser.

**Screenshots:** see `handoff-round-5.md`. In Round 6 a battle page was saved with
`render_game(game, 2.5)`, with `'/sound/` replaced by
`'http://127.0.0.1:8765/sound/` and a server running on port 8765. A screenshot with
`--autoplay-policy=no-user-gesture-required` then showed the music player playing at
`0:02 / 0:09`. That proves the music loads and the `#t=` jump works. It doesn't prove
how it sounds.

## What Round 6 added

| File | Change |
|---|---|
| `sounds.py` (new) | All sound. It has building blocks (`tone`, `noise`, `mix`, `then`, `silence`, `to_wav`, `note_freq`) and these tables: `MUSIC` (a `Theme` per key, written as tracker strings), `MUSIC_FOR_SCENE`, `VOICES` (a `Voice` per hero) and `ATTACK_SOUNDS` (a builder per sprite key). It also has `hero_hurt`, `foe_hurt`, `crit`, `knockout` and the jingles, plus `music_key(opponent)`, `music_length(key)`, `sound_names()` and `make_sound(name)` (cached with `lru_cache`, returns `None` for an unknown name). |
| `web.py` | `sound_html(game, music_at)` builds `<div class='sound'>…</div>`, which goes at the very end of the battle page. `render_game(game, music_at=0.0)` now takes the music's elapsed time. `make_handler`/`make_server` take an optional `clock`. A new `music_clock` dict maps session → (stage, start time); it is reset on `/start`. A new GET route `/sound/<name>.wav` (regex `SOUND_PATH`) handles `Range` requests (206/416) in `_send_sound`. There are two new CSS rules, `.sound` and `.sound audio`. |
| `tests/test_round6.py` (new) | Helpers: `read_wav(name)` gives (seconds, samples). `sound_part(html)` is the `<div class='sound'>` part. `played(html)` lists the sound names a page plays. `right(g)` and `wrong(g)` answer one question. It reuses `PROBLEMS` and `between` from `test_web.py`, and `lose` and `win_first_battle` from `test_web_round4.py`. |
| `docs/decisions/0005-…`, `0006-…` | The Round 6 decision records. |
| `Spec.md` | A `## Round 6` section was appended. Earlier text is unchanged. |

### Which sounds a battle page plays (`sound_html`)

- **Playing:** the opponent's music, with `autoplay loop controls` and `#t=<seconds>`
  when the time isn't 0.
- **Won or lost:** `jingle-victory` or `jingle-defeat` once, with no music. Each starts
  with 1.2 s of silence so the final blow plays first.
- **No answer yet** (`last_turn is None`): `voice-<hero>`.
- **After an answer:** `attack-<attacker>` and then `hurt-hero` or `hurt-foe`. `crit`
  is added if it was a critical hit, and `knockout` if it was a knockout. The attacker
  is `game.hero`, or `turn.foe.sprite` (or `foe` if that sprite has no sound).

### Timing built into the WAV files

The attack sound starts at 0 s (the lunge). `hurt-*` and `crit` start after 0.2 s of
silence (`HIT_DELAY`, when the shake starts in R7). `knockout` starts at 0.7 s, just
before the fall (0.8 s). The jingles start at 1.2 s (`JINGLE_DELAY`). Without
JavaScript, these silences are the only way to time a sound.

## Decisions made this round, and why

1. **Every sound is made by Python from waveforms** (ADR 0005). No files are stored,
   nothing is installed, and tests can read the WAV bytes. The cost is a simple
   chiptune sound.
2. **Sounds play through `<audio autoplay>` tags chosen by the server**, the same idea
   as ADR 0002's CSS classes. No JavaScript, as the student chose.
3. **The music resumes with a server clock and a `#t=` media fragment** (ADR 0006).
   The time lives in `web.py`, not `game.py`, so the rules stay free of web code. A
   refresh resumes the music rather than restarting it.
4. **The server answers Range requests.** Chrome needs them before it can loop or jump
   into a WAV. Without them, `#t=` and `loop` can quietly fail.
5. **Music follows the scene** (`MUSIC_FOR_SCENE`), so `Opponent` got no new field.
6. **Claude chose the names and styles of the tunes, the voices and the attack
   sounds.** The student didn't choose them. Troll is slowest (76 bpm), Dragon fastest
   (152).
7. **Extras the requirements didn't ask for:** crit and knockout sounds, the
   victory/defeat jingles, a default tune, a plain `attack-foe`, and a visible music
   player (so a blocked autoplay can be started by hand).
8. **The voice line plays on the first battle page**, and again on a refresh before
   the first answer, the same way a refresh replays animations (ADR 0002). The title
   screen is silent.
9. **Everything is scaled to the same loudness** (`PEAK = 0.8`). There is no volume
   setting other than the music player's.
10. **Noise uses a fixed seed** (`random.Random(seed)`), so every build of a sound is
    identical. Tests compare sounds by their bytes.

## Unresolved

- **No one has listened to the sounds yet.** Ask the student:
  - Does each tune fit its opponent?
  - Do the four voices sound different, and like "talking"?
  - Does the damage sound line up with the shake?
  - Is anything too loud next to the music?
- **Browser autoplay rules:** Chrome usually allows sound after a click on the site,
  and every page here follows a form submit. Safari and Firefox may block it. Then the
  effects stay silent, and the music needs a press on its player. This hasn't been
  checked in those browsers.
- **The short skip in the music at each answer** (while the page reloads) can't be
  removed without JavaScript or frames (see ADR 0006).
- **Unanswered understanding check from Round 6:** "After a wrong answer, which two
  sounds play, and why does `hurt-hero.wav` start with 0.2 s of silence?" (Answer: the
  opponent's attack sound and `hurt-hero`. The silence makes the sound wait until the
  hit lands, because without JavaScript the page can't delay it.)
- Round 5's open items (the student hasn't watched the idle animations or the defeat
  order in a browser, and the "K.O.!" banner stays on the game-over screen) are still
  open.

## Warnings for the next session

- **Requirement IDs:** R1–R18 are taken, so continue from **R19**. The next decision
  record is `docs/decisions/0007-...md`.
- **`<div class='sound'>` must not contain another `<div>`.** The tests' `sound_part`
  stops at the first `</div>`. The music label uses a `<p>`.
- **The sound block must stay at the end of the body.** Round 3 tests require
  `<body><div class='hud'>` at the start.
- **Adding an opponent** now also needs an entry in `ATTACK_SOUNDS`, keyed by its
  sprite. Otherwise `test_R18_every_fighter_has_its_own_attack_sound` fails. If its
  scene has no entry in `MUSIC_FOR_SCENE`, it gets the default tune. **Adding a hero**
  needs a `Voice` in `VOICES` (with its own `pitch`) and an attack sound.
- **Every effect and voice must last under 1.5 s.** Music loops must last at least
  6 s. Every token line in a `Theme` (melody, bass, drums) should have the same number
  of steps. The loop length comes from the melody.
- **A hurt sound must begin with exact zeros** (a test checks the first 0.15 s). Don't
  add anything (fade-ins, dither) that would put tiny values there.
- **`make_sound` is cached.** If you change a builder while experimenting in one Python
  session, call `make_sound.cache_clear()`.
- **The `clock` argument** of `make_server` is for tests. `main.py` doesn't pass one,
  so the real clock (`time.monotonic`) is used.
- **Generating sound is pure Python,** but it's quick: every sound together takes about
  0.7 s, built once on first request. Music WAVs are 280–560 KB each and are sent with
  `Cache-Control: max-age=3600`.
- **Prefer the Edit tool (or a small Python script) to `sed -i`,** which works
  differently on macOS.
