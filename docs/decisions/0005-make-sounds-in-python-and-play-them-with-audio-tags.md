# 0005: Make every sound in Python and play it with HTML `<audio>` tags

- Status: accepted
- Date: 2026-11-17
- Round: 6 (requirements R15, R16, R17, R18)

## Y-statement

In the context of **adding music, hero voice lines, and attack and damage sounds to
Math Quest (R15–R18)**,
facing **the rules that the program is Python-only and standard-library-only, the
student's choice of no JavaScript, and a game where every answer loads a brand-new
page**,
we decided for **building every sound from simple waveforms in a new `sounds.py`,
turning it into WAV bytes with the `wave` module, serving it at `/sound/<name>.wav`,
and letting each page play the sounds it needs with `<audio autoplay>` tags chosen by
the server (the same way ADR 0002 chooses CSS classes)**
and neglected **recorded sound files (WAV/MP3) kept in the project, the browser's Web
Audio API driven by JavaScript, and playing no sound until the player presses a play
button**,
to achieve **sounds that need nothing downloaded or installed, that tests can check by
reading the page and the WAV bytes, and that match each character (its own music,
voice and attack)**,
accepting that **the sounds are simple chiptune-style tones rather than real
instruments or real speech; that a damage sound can't wait for the hit by itself, so
the wait (0.2 s) is built into the start of the file; that the voice line plays when
the game starts, not the instant a hero is clicked; and that some browsers block sound
that starts on its own, which is why the music has a visible player**.

## Alternatives considered

| Option | Why not chosen |
|---|---|
| Recorded sound files in a `sounds/` folder | Not Python, someone would have to make or license them, and the tests couldn't tell what they contain. |
| Web Audio API with JavaScript | Could play a voice the moment a hero is clicked and keep music perfectly smooth, but the student chose no JavaScript, and tests can't run it. |
| Only a "play" button for each sound | Works in every browser, but nobody would press a button for every sword swish, so attacks would be silent. |

## Consequences

- `sounds.py` has the only sound code. Each sound is built the first time it is asked
  for, then cached. All of them together take under a second to build.
- `web.py` has a new route that also answers **range requests**, in which the browser
  asks for only part of a file. Chrome needs these before it can loop music or jump
  into the middle of it.
- A test checks that `sounds.py` imports only standard-library modules, and another
  checks that no sound files are stored in the project.
