# 0002: Animate attacks with CSS classes chosen by the server

- Status: accepted
- Date: 2026-11-14
- Round: 3 (requirement R7, with R5 and R6)

## Y-statement

In the context of **showing short attack and damage animations on the battle screen (R7)**,
facing **a game that has no JavaScript, where every answer is a form submit followed by a
redirect and a brand-new page, and the rule that the program is written only in Python**,
we decided for **having the game remember the last attack (`Game.last_turn`) and letting
`web.py` turn it into CSS classes (`attack`, `hurt`, `ko`, `enter`) plus a damage number,
so the browser plays CSS keyframe animations once when the new page loads**
and neglected **adding JavaScript to animate without reloading, animating the SVG
sprites themselves with SVG `<animate>` tags, and showing a separate "attack" page before
the result page**,
to achieve **animations that make it obvious who attacked and who was hit, while keeping
the game Python-only, keeping every page testable with plain string checks, and changing
nothing about how answers are sent to the server**,
accepting that **refreshing the page replays the last animation, that a knocked-out
opponent is not redrawn when a new one arrives (only a damage number and "K.O.!" mark
where it stood), and that the animation cannot react to anything after the page loads**.

## Alternatives considered

| Option | Why not chosen |
|---|---|
| JavaScript that sends the answer in the background and animates the result | Smoother, with no page reload, but it would be the first non-Python code with logic in it, and the tests could no longer check the result by reading the HTML. |
| SVG `<animate>` tags inside each sprite | Still no JavaScript, but each sprite would need its own animation markup, the lunge has to move the whole fighter (not shapes inside it), and reduced-motion settings are harder to respect. |
| An extra "attack" page that redirects to the result after a second | Needs a new route and a timed redirect, and it doubles the number of page loads per answer. |

## Consequences

- `game.Turn` records the attacker, damage, crit and knockout, plus the opponent that was
  hit. It is `None` until the first answer, so a new battle starts with no animation.
- `web.turn_effects(game)` is the one place that decides which fighter gets which class.
- The older test `test_R4_battle_sprite_changes_with_the_opponent` requires that a
  defeated opponent's sprite is gone once the next one appears. That is why a mid-game
  knockout shows the new opponent sliding in instead of the old one falling.
- People whose system asks for reduced motion get no movement, but still see the red
  flash and the damage number.
