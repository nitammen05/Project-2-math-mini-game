# 0003: Draw background scenes as SVG pictures inside the CSS

- Status: accepted
- Date: 2026-11-15
- Round: 4 (requirements R8, R9, R10)

## Y-statement

In the context of **giving each opponent a themed background, and changing the
background when the player moves on or is defeated (R8–R10)**,
facing **the rules that the program is Python-only with no image files, that earlier
tests count exactly two `<svg>` elements on a battle page and look for exact class
strings like `class='stage'`, and that scenery is decoration rather than content**,
we decided for **drawing each scene as SVG shapes in Python (`scenes.py`), encoding the
whole picture into a CSS `url("data:image/svg+xml,...")`, and painting it as the
background of a new `.world` wrapper's stage and floor through a class such as
`scene-swamp`**
and neglected **inline `<svg>` elements behind the fighters, pure CSS gradients, PNG
files, and emoji**,
to achieve **detailed scenes (trees, a bridge arch, bones and skulls) drawn the same way
as the sprites, a scene change that is just a class swap, scenery that screen readers
skip, and no change to the markup earlier rounds' tests rely on**,
accepting that **every page now carries all seven scenes in its `<style>` block (about
30 KB), that the pictures can't be checked by reading the HTML (only by looking at
screenshots), and that a scene can't be changed without editing encoded SVG in Python**.

## Alternatives considered

| Option | Why not chosen |
|---|---|
| Inline `<svg>` elements in the stage | The most direct, but screen readers would treat scenery as content, and it would break the Round 2 test that a battle page has exactly two `<svg>` pictures (rule 13: earlier tests are not changed to suit new code). |
| Only CSS gradients (no SVG) | Fine for skies and stripes, but drawing bones, skulls, a bridge or a volcano out of gradients is unreadable code. |
| PNG image files and a route to serve them | Needs non-Python files and someone to draw them (already rejected for sprites in ADR 0001). |
| Emoji (🌋 🦴 💀) | Little code, but emoji look different on every device and there is no swamp or troll-bridge emoji. |

## Consequences

- `Opponent.scene` names a key in `scenes.SCENES`, just as `Opponent.sprite` names a
  sprite. An unknown key gets the plain "Open Field" scene.
- `web.scene_effects(game)` is the one place that picks the scene, plus the old scene
  that is laid on top (`.backdrop`) to slide away (`advance`, R9) or fade away
  (`perish`, R10).
- The walk in R9 animates the hero's `<svg>`, not the fighter box, because the box is
  already lunging (both use `transform`).
- To keep each animation under 1.5 s (R7), the scene change is a chain of short
  animations started one after another, taking about 2 seconds in all.
