# 0004: Animate parts of each sprite with CSS classes on SVG groups

- Status: accepted
- Date: 2026-11-16
- Round: 5 (requirements R11, R12, with R14)

## Y-statement

In the context of **giving every sprite idle animations (breathing, blinking, swaying)
and more detailed attack, hurt and knockout animations (R12)**,
facing **a game with no JavaScript where every answer loads a new page, earlier tests
that require every `animation:` value to be under 1.5 s (R7), mirrored sprites (R6), and
sprite pictures that earlier tests find by their exact SVG text**,
we decided for **marking the moving parts inside each SVG sprite with `sp-*` classes
(`sp-body`, `sp-eye`, `sp-sway`, `sp-glow`, `sp-weapon`) and animating them with CSS
keyframes in the page's shared stylesheet, chosen by the fighter's existing state
classes (`attack`, `hurt`, `ko`)**
and neglected **SVG `<animate>` (SMIL) tags written inside each sprite, a JavaScript
animation loop, and drawing several frames per sprite and flipping between them**,
to achieve **one place (`web.py`) that decides how every part moves, animations that
react to the same server-chosen classes as Round 3's lunges and shakes, one
reduced-motion rule that stops them all, and sprites that stay plain text that tests
can check**,
accepting that **each moving part needs a class and, for weapons, its pivot point
written by hand in its `style`; that parts with a `transform=` attribute cannot be
animated (a test checks for this); and that idle loops must be under 1.5 s each, so
calmer cycles are made by playing a loop forwards then backwards (`alternate`)**.

## Alternatives considered

| Option | Why not chosen |
|---|---|
| SMIL `<animate>` tags inside each sprite | Would put timing into every sprite string, can't easily switch to a swing when the fighter attacks, and reduced-motion settings can't turn it off with CSS. |
| JavaScript animation loop | The first logic not written in Python, and nothing to test by reading the HTML. Already rejected for attacks in ADR 0002. |
| Several frames per sprite (frame-by-frame) | Several times more SVG to draw by hand, and the pages already carry every scene (about 38 KB of CSS). |

## Consequences

- Class names inside sprites all start with `sp-`, so they can't clash with page
  classes such as `hero`, `foe`, `sky` or `fill`. A test checks this.
- Sprites drawn facing left mark their weapon `sp-left` so it swings toward the enemy
  (the other way). Mirrored sprites (the orc) need nothing extra, because the mirror
  flips the swing too.
- The `<svg>` sprites now have `overflow: visible`, so a swinging weapon or a burst of
  fire may reach outside the 64 × 64 box.
- Knockout rules come after the idle and hurt rules in the stylesheet so they win; a
  test checks the order.
