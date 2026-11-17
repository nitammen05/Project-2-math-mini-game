# 0006: Resume each opponent's music using a clock kept by the server

- Status: accepted
- Date: 2026-11-17
- Round: 6 (requirement R16)

## Y-statement

In the context of **looping each opponent's own music while the player fights it
(R16)**,
facing **a page that is replaced after every answer, so the music player is destroyed
and created again each time, and no JavaScript to remember where it was**,
we decided for **having the web server remember, for each player, when the current
opponent's music started, and writing the elapsed time into the music's address as a
media fragment (`music-war-drums.wav#t=4.25`), which tells the browser to start
playing from that second**
and neglected **restarting the music from the beginning on every page, keeping the
music in an outer page with the game inside an `<iframe>`, and storing the time on the
`Game` object**,
to achieve **music that sounds like it keeps going, apart from a short gap while the
new page loads, and that starts fresh when a new opponent appears or a new game
begins**,
accepting that **there is a small skip at every answer, that the time is measured on
the server (so it drifts slightly if a page loads slowly, or if the player pauses the
music), and that a refresh resumes the music rather than restarting it**.

## Alternatives considered

| Option | Why not chosen |
|---|---|
| Restart the music on every page | Simplest, but the player would hear only the first few seconds of each tune, over and over. |
| Outer page with the music, game in an `<iframe>` | Truly seamless, but the outer page can't find out that the opponent changed without JavaScript, so the music couldn't change with the opponent. |
| Keep the time on `Game` | `game.py` holds only the rules, with no time and no web code, so it can be tested on its own. Timing music belongs to the web side. |

## Consequences

- `make_handler` and `make_server` take an optional `clock`, so tests can pass a fake
  clock and check the exact `#t=` value.
- `render_game(game, music_at=...)` wraps the time round the loop's length, so a long
  fight doesn't ask for a second past the end.
