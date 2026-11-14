"""Pictures (sprites) for the heroes and monsters of Math Quest.

Each sprite is drawn as SVG: text that describes shapes (circles, rectangles, ...)
which the browser turns into a picture. Keeping them as Python strings means the game
still needs no image files. Every sprite is drawn on a 64 x 64 grid.
"""

from dataclasses import dataclass
from html import escape


@dataclass(frozen=True)
class Sprite:
    name: str   # shown to the player, and read out by screen readers
    svg: str    # the shapes inside the <svg> element
    faces: str = "right"   # which way the drawing looks: "left" or "right" (R6)


HEROES = {
    "knight": Sprite("Knight", """
        <rect x='22' y='30' width='20' height='22' rx='3' fill='#9aa5b1'/>
        <circle cx='32' cy='20' r='11' fill='#c0c8d0'/>
        <rect x='24' y='18' width='16' height='4' fill='#33363d'/>
        <path d='M32 6 L36 10 L28 10 Z' fill='#e63946'/>
        <rect x='44' y='14' width='4' height='30' fill='#e0e0e0'/>
        <rect x='40' y='38' width='12' height='4' fill='#8d6e63'/>
        <path d='M10 30 h12 v14 l-6 6 l-6 -6 Z' fill='#457b9d'/>
        <rect x='24' y='52' width='6' height='8' fill='#5c5f66'/>
        <rect x='34' y='52' width='6' height='8' fill='#5c5f66'/>"""),
    "wizard": Sprite("Wizard", """
        <path d='M18 58 L32 26 L46 58 Z' fill='#5e3c99'/>
        <circle cx='32' cy='24' r='8' fill='#f1c27d'/>
        <path d='M32 26 L26 40 L38 40 Z' fill='#eeeeee'/>
        <path d='M20 20 L32 2 L44 20 Z' fill='#5e3c99'/>
        <circle cx='32' cy='10' r='2' fill='#ffd166'/>
        <rect x='48' y='16' width='3' height='42' fill='#8d6e63'/>
        <circle cx='49.5' cy='14' r='4' fill='#4cc9f0'/>
        <circle cx='29' cy='23' r='1.3' fill='#222'/>
        <circle cx='35' cy='23' r='1.3' fill='#222'/>"""),
    "archer": Sprite("Archer", """
        <rect x='24' y='30' width='16' height='20' rx='3' fill='#2d6a4f'/>
        <circle cx='32' cy='20' r='9' fill='#e0ac69'/>
        <path d='M22 18 Q32 4 42 18 L42 22 L22 22 Z' fill='#40916c'/>
        <circle cx='29' cy='21' r='1.3' fill='#222'/>
        <circle cx='35' cy='21' r='1.3' fill='#222'/>
        <path d='M48 12 Q60 34 48 56' stroke='#8d6e63' stroke-width='3' fill='none'/>
        <line x1='48' y1='12' x2='48' y2='56' stroke='#ddd' stroke-width='1'/>
        <line x1='36' y1='34' x2='58' y2='34' stroke='#6d4c41' stroke-width='2'/>
        <rect x='25' y='50' width='5' height='10' fill='#6d4c41'/>
        <rect x='34' y='50' width='5' height='10' fill='#6d4c41'/>"""),
    "ninja": Sprite("Ninja", """
        <rect x='22' y='30' width='20' height='22' rx='4' fill='#4a4e69'/>
        <circle cx='32' cy='20' r='11' fill='#4a4e69'/>
        <rect x='23' y='17' width='18' height='6' rx='3' fill='#f1c27d'/>
        <circle cx='28' cy='20' r='1.5' fill='#222'/>
        <circle cx='36' cy='20' r='1.5' fill='#222'/>
        <rect x='21' y='12' width='22' height='3' fill='#e63946'/>
        <path d='M43 13 L52 9 L50 15 Z' fill='#e63946'/>
        <path d='M50 30 l3 -6 l3 6 l-3 6 Z' fill='#adb5bd'/>
        <rect x='24' y='52' width='6' height='8' fill='#4a4e69'/>
        <rect x='34' y='52' width='6' height='8' fill='#4a4e69'/>"""),
}

DEFAULT_HERO = "knight"

# Keyed by the first word of each opponent's name in game.OPPONENTS.
MONSTERS = {
    "slime": Sprite("Slime", """
        <path d='M8 54 Q8 20 32 18 Q56 20 56 54 Z' fill='#80ed99'/>
        <ellipse cx='24' cy='30' rx='5' ry='3' fill='#c7f9cc'/>
        <circle cx='25' cy='40' r='4' fill='#fff'/><circle cx='23.5' cy='41' r='2' fill='#222'/>
        <circle cx='39' cy='40' r='4' fill='#fff'/><circle cx='37.5' cy='41' r='2' fill='#222'/>
        <path d='M27 48 Q32 52 37 48' stroke='#222' stroke-width='2' fill='none'/>""",
        faces="left"),
    "goblin": Sprite("Goblin", """
        <rect x='22' y='36' width='20' height='18' rx='3' fill='#7f5539'/>
        <circle cx='32' cy='26' r='12' fill='#6a994e'/>
        <path d='M20 24 L4 16 L20 30 Z' fill='#6a994e'/>
        <path d='M44 24 L60 16 L44 30 Z' fill='#6a994e'/>
        <circle cx='27' cy='24' r='2.5' fill='#ffd60a'/>
        <circle cx='37' cy='24' r='2.5' fill='#ffd60a'/>
        <circle cx='26' cy='24' r='1.2' fill='#222'/>
        <circle cx='36' cy='24' r='1.2' fill='#222'/>
        <path d='M26 32 L29 30 L32 32 L35 30 L38 32' stroke='#222' stroke-width='1.5' fill='none'/>
        <rect x='24' y='54' width='5' height='6' fill='#6a994e'/>
        <rect x='35' y='54' width='5' height='6' fill='#6a994e'/>""",
        faces="left"),
    "orc": Sprite("Orc", """
        <rect x='14' y='32' width='36' height='24' rx='6' fill='#5c4033'/>
        <rect x='18' y='10' width='28' height='26' rx='8' fill='#4f772d'/>
        <rect x='22' y='18' width='20' height='3' fill='#31572c'/>
        <circle cx='27' cy='23' r='2' fill='#d00000'/>
        <circle cx='37' cy='23' r='2' fill='#d00000'/>
        <path d='M25 34 L26 28 L28 34 Z' fill='#fff'/>
        <path d='M36 34 L38 28 L39 34 Z' fill='#fff'/>
        <rect x='50' y='22' width='4' height='34' fill='#8d6e63'/>
        <path d='M54 22 h8 v12 h-8 Z' fill='#adb5bd'/>"""),
    "troll": Sprite("Troll", """
        <ellipse cx='32' cy='44' rx='22' ry='16' fill='#6c757d'/>
        <circle cx='32' cy='22' r='14' fill='#8a9a8b'/>
        <ellipse cx='32' cy='26' rx='5' ry='4' fill='#6b7a6c'/>
        <circle cx='26' cy='18' r='2' fill='#222'/>
        <circle cx='38' cy='18' r='2' fill='#222'/>
        <path d='M24 32 Q32 28 40 32' stroke='#222' stroke-width='2' fill='none'/>
        <rect x='4' y='30' width='8' height='28' rx='4' fill='#7f5539'/>
        <circle cx='8' cy='28' r='6' fill='#7f5539'/>""",
        faces="left"),
    "dragon": Sprite("Dragon", """
        <path d='M20 30 L2 10 L10 34 Z' fill='#9d0208'/>
        <path d='M44 30 L62 10 L54 34 Z' fill='#9d0208'/>
        <ellipse cx='32' cy='44' rx='16' ry='14' fill='#d00000'/>
        <ellipse cx='32' cy='46' rx='9' ry='10' fill='#ffba08'/>
        <circle cx='32' cy='22' r='11' fill='#d00000'/>
        <path d='M24 14 L22 4 L28 12 Z' fill='#ffba08'/>
        <path d='M40 14 L42 4 L36 12 Z' fill='#ffba08'/>
        <circle cx='28' cy='20' r='2' fill='#ffd60a'/>
        <circle cx='36' cy='20' r='2' fill='#ffd60a'/>
        <circle cx='27' cy='20' r='1' fill='#370617'/>
        <circle cx='35' cy='20' r='1' fill='#370617'/>
        <path d='M28 28 Q32 31 36 28' stroke='#370617' stroke-width='2' fill='none'/>
        <path d='M30 32 Q32 38 34 32' fill='#ff8800'/>""",
        faces="left"),
}

# Shown if an opponent has no sprite of its own (e.g. a future, unfinished one).
UNKNOWN_MONSTER = Sprite("Unknown monster", """
    <circle cx='32' cy='32' r='22' fill='#6c757d'/>
    <text x='32' y='42' font-size='28' text-anchor='middle' fill='#fff'>?</text>""",
    faces="left")


def hero_or_default(key):
    """Return key if it names a hero, otherwise the default hero's key."""
    return key if key in HEROES else DEFAULT_HERO


# Flips a drawing left-to-right on the 64 x 64 grid: x becomes 64 - x.
MIRROR = "transform='matrix(-1 0 0 1 64 0)'"


def _svg(sprite, label, size, facing=None):
    """Build the <svg> element. If `facing` ("left"/"right") differs from the way the
    sprite was drawn, the shapes are mirrored so it looks the other way (R6)."""
    if facing not in (None, "left", "right"):
        raise ValueError(f"facing must be 'left' or 'right', not {facing!r}")
    shapes = sprite.svg
    if facing and facing != sprite.faces:
        shapes = f"<g {MIRROR}>{shapes}</g>"
    return (f"<svg class='sprite' role='img' aria-label='{escape(label, quote=True)}' "
            f"viewBox='0 0 64 64' width='{size}' height='{size}'>"
            f"<title>{escape(label)}</title>{shapes}</svg>")


def render_hero(key, size=96, facing=None):
    """The <svg> element for a hero. Unknown keys get the default hero."""
    sprite = HEROES[hero_or_default(key)]
    return _svg(sprite, sprite.name, size, facing)


def render_monster(opponent, size=96, facing=None):
    """The <svg> element for an opponent, labelled with the opponent's full name."""
    sprite = MONSTERS.get(getattr(opponent, "sprite", ""), UNKNOWN_MONSTER)
    return _svg(sprite, opponent.name, size, facing)
