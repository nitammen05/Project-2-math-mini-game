"""Background scenes for Math Quest (Round 4: R8, R10).

Each scene is a picture drawn as SVG on a 300 x 100 grid, plus a pattern for the
ground the fighters stand on. Unlike the sprites, a scene is not put into the page as
an <svg> element. It is turned into a "data URL" (the whole picture written inside
the link itself) and used as a CSS background-image. That keeps the scenery out of
the page's content: screen readers skip it, and the page still has exactly two
sprite pictures (see docs/decisions/0003).
"""

from dataclasses import dataclass
from urllib.parse import quote


@dataclass(frozen=True)
class Scene:
    name: str     # what the place is called, e.g. "Slime Swamp"
    svg: str      # the shapes of the background picture, on a 300 x 100 grid
    base: str     # a colour shown while the picture loads, or around its edges
    ground: str   # CSS background for the floor strip the fighters stand on


def _sky(top, bottom):
    """A full-size rectangle shaded from `top` colour to `bottom` colour."""
    return ("<defs><linearGradient id='sky' x1='0' y1='0' x2='0' y2='1'>"
            f"<stop offset='0' stop-color='{top}'/><stop offset='1' stop-color='{bottom}'/>"
            "</linearGradient></defs><rect width='300' height='100' fill='url(#sky)'/>")


def _sign(x, y, char, size, color, opacity=1):
    """A math sign drawn as text, e.g. a glowing '+' firefly."""
    return (f"<text x='{x}' y='{y}' font-size='{size}' font-family='sans-serif' "
            f"font-weight='bold' text-anchor='middle' fill='{color}' "
            f"opacity='{opacity}'>{char}</text>")


def _bone(x, y, angle, length=26):
    """A cartoon bone: a bar with two knobs at each end, turned by `angle` degrees."""
    half = length / 2
    knobs = "".join(f"<circle cx='{cx}' cy='{cy}' r='3.2'/>"
                    for cx in (-half, half) for cy in (-2.4, 2.4))
    return (f"<g class='bone' transform='translate({x} {y}) rotate({angle})'>"
            f"<rect x='{-half}' y='-2' width='{length}' height='4'/>{knobs}</g>")


def _skull(x, y, angle=0):
    """A cartoon skull with dark eye holes."""
    return (f"<g class='skull' transform='translate({x} {y}) rotate({angle})'>"
            "<circle r='9'/><rect x='-5.5' y='4' width='11' height='7' rx='2'/>"
            "<circle class='hole' cx='-3.5' cy='-1' r='2.6'/>"
            "<circle class='hole' cx='3.5' cy='-1' r='2.6'/>"
            "<path class='hole' d='M0 2 L-1.5 5 H1.5 Z'/></g>")


def _swamp():
    trees = "".join(
        f"<path d='M{x} 100 V{top} M{x} {top + 14} L{x + 13} {top + 2} "
        f"M{x} {top + 26} L{x - 11} {top + 16}' stroke='#132619' stroke-width='5' "
        "stroke-linecap='round' fill='none'/>"
        for x, top in ((26, 34), (92, 50), (214, 44), (282, 30)))
    bubbles = "".join(f"<circle cx='{x}' cy='{y}' r='{r}' fill='none' stroke='#a7d48a' "
                      "stroke-width='0.8' opacity='0.7'/>"
                      for x, y, r in ((60, 90, 2.5), (66, 85, 1.5), (170, 92, 2),
                                      (240, 88, 2.8), (246, 82, 1.3)))
    reeds = "".join(f"<path d='M{x} 100 Q{x + 2} 84 {x + 5} 76' stroke='#2f5d2a' "
                    "stroke-width='1.6' fill='none'/>"
                    for x in (6, 10, 14, 128, 133, 196, 292, 296))
    fireflies = "".join(_sign(x, y, "+", 9, "#e4ff7a", 0.9)
                        for x, y in ((48, 40), (120, 26), (158, 52), (196, 22), (252, 58)))
    return (_sky("#0d2419", "#4d7a44")
            + "<circle cx='236' cy='20' r='11' fill='#e9f5c9' opacity='0.75'/>"
            + "<path d='M0 76 Q40 60 80 72 T160 68 T240 66 T300 70 V100 H0 Z' fill='#1c3a27'/>"
            + trees
            + "<path d='M0 88 Q75 82 150 88 T300 86 V100 H0 Z' fill='#4e7d2c'/>"
            + "<ellipse cx='110' cy='93' rx='34' ry='3' fill='#7fb24a' opacity='0.6'/>"
            + bubbles + reeds + fireflies)


def _cave():
    stalactites = "".join(f"<path d='M{x} 0 L{x + w} 0 L{x + w / 2} {h} Z' fill='#2a1f33'/>"
                          for x, w, h in ((0, 22, 26), (30, 14, 16), (62, 26, 34), (110, 16, 20),
                                          (150, 30, 30), (200, 18, 22), (240, 28, 36),
                                          (282, 18, 18)))
    stalagmites = "".join(f"<path d='M{x} 100 L{x + w / 2} {100 - h} L{x + w} 100 Z' "
                          "fill='#3a2c42'/>"
                          for x, w, h in ((8, 20, 22), (130, 14, 14), (268, 24, 26)))

    def torch(x):
        return (f"<circle cx='{x}' cy='44' r='13' fill='#ffb703' opacity='0.1'/>"
                f"<rect x='{x - 1.5}' y='46' width='3' height='16' fill='#6b4226'/>"
                f"<ellipse cx='{x}' cy='42' rx='4' ry='7' fill='#fb8500'/>"
                f"<ellipse cx='{x}' cy='44' rx='2' ry='4' fill='#ffd166'/>")

    crystals = "".join(f"<path d='M{x} 100 L{x + 4} {100 - h} L{x + 8} 100 Z' fill='#9b5de5' "
                       "opacity='0.85'/>"
                       for x, h in ((90, 18), (96, 26), (104, 14), (188, 20), (195, 12)))
    scratches = "".join(_sign(x, y, "−", 12, "#b9a7c9", 0.55)
                        for x, y in ((60, 60), (70, 62), (80, 59), (226, 66), (236, 64)))
    eyes = ("<circle cx='166' cy='58' r='1.6' fill='#ffd60a'/>"
            "<circle cx='172' cy='58' r='1.6' fill='#ffd60a'/>")
    return (_sky("#120c1a", "#3d2b47")
            + "<ellipse cx='150' cy='66' rx='50' ry='30' fill='#0a070e'/>"
            + eyes + stalactites + torch(40) + torch(258) + scratches + stalagmites + crystals)


def _camp():
    palisade = "".join(f"<path d='M{x} 100 V64 L{x + 5} 56 L{x + 10} 64 V100 Z' fill='#5a3a22' "
                       "stroke='#3d2616' stroke-width='1'/>"
                       for x in range(0, 300, 10))

    def tent(x):
        return (f"<path d='M{x} 66 L{x + 22} 34 L{x + 44} 66 Z' fill='#8c5a2b'/>"
                f"<path d='M{x + 18} 66 L{x + 22} 50 L{x + 26} 66 Z' fill='#2b1a0e'/>")

    def banner(x):
        return (f"<rect x='{x}' y='18' width='2' height='46' fill='#3d2616'/>"
                f"<path d='M{x + 2} 20 H{x + 22} V36 L{x + 12} 32 L{x + 2} 36 Z' fill='#9d0208'/>"
                + _sign(x + 12, 31, "×", 13, "#ffd166"))

    return (_sky("#3d1d3a", "#f4a261")
            + "<circle cx='150' cy='60' r='22' fill='#ffd166' opacity='0.9'/>"
            + "<path d='M0 64 Q60 44 120 60 T240 54 T300 58 V100 H0 Z' fill='#4a2c2a'/>"
            + tent(40) + tent(212) + banner(110) + banner(176) + palisade)


def _bridge():
    clouds = "".join(f"<ellipse cx='{x}' cy='{y}' rx='{rx}' ry='6' fill='#fff' opacity='0.8'/>"
                     for x, y, rx in ((50, 16, 20), (64, 12, 14), (210, 22, 24), (228, 17, 14)))
    bricks = "".join(f"<line x1='0' y1='{y}' x2='300' y2='{y}' stroke='#5c5f66' "
                     "stroke-width='0.8'/>" for y in (46, 54))
    posts = "".join(f"<rect x='{x}' y='28' width='4' height='10' fill='#6c6f76'/>"
                    for x in range(6, 300, 24))
    river = "".join(f"<path d='M{x} {y} q6 -2 12 0' stroke='#cfe8ff' stroke-width='1' "
                    "fill='none'/>" for x, y in ((120, 92), (150, 96), (176, 90), (140, 86)))
    return (_sky("#4a6d8c", "#b8d0e6")
            + clouds
            + "<path d='M0 70 Q50 60 100 70 V100 H0 Z M200 70 Q250 60 300 70 V100 H200 Z' "
              "fill='#56794a'/>"
            + "<rect x='0' y='38' width='300' height='22' fill='#8d9199'/>"
            + "<path d='M0 60 H300 V100 H250 A100 44 0 0 0 50 100 H0 Z' fill='#7d8189'/>"
            + bricks + "<rect x='0' y='34' width='300' height='4' fill='#6c6f76'/>" + posts
            + "<path d='M50 100 A100 44 0 0 1 250 100 Z' fill='#2c5d8a'/>" + river
            + "<rect x='143' y='40' width='14' height='14' rx='2' fill='#d9c9a3' "
              "stroke='#6b4f35' stroke-width='1'/>"
            + _sign(150, 51, "÷", 12, "#3d2616"))


def _volcano():
    embers = "".join(f"<circle cx='{x}' cy='{y}' r='{r}' fill='#ffba08' opacity='0.85'/>"
                     for x, y, r in ((120, 10, 1.4), (172, 6, 1.2), (190, 20, 1.6), (104, 26, 1),
                                     (40, 30, 1), (260, 16, 1.3), (230, 40, 0.9)))
    coins = "".join(f"<ellipse cx='{x}' cy='{y}' rx='3' ry='1.6' fill='#ffd60a' "
                    "stroke='#b07d00' stroke-width='0.5'/>"
                    for x, y in ((20, 90), (30, 86), (40, 92), (262, 88), (274, 84), (284, 91)))
    return (_sky("#1a0505", "#9d0208")
            + "<circle cx='150' cy='24' r='34' fill='#ff5400' opacity='0.25'/>"
            + "<path d='M60 100 L132 26 H168 L240 100 Z' fill='#2b1b17'/>"
            + "<path d='M138 26 Q146 50 136 70 Q130 86 142 100 H150 Q140 84 148 66 "
              "Q156 46 150 26 Z' fill='#ff6d00'/>"
            + "<path d='M132 26 Q150 4 168 26 Z' fill='#ffba08' opacity='0.9'/>"
            + "<path d='M0 80 Q60 70 100 84 V100 H0 Z M200 84 Q240 70 300 80 V100 H200 Z' "
              "fill='#140a08'/>"
            + "<path d='M0 96 Q40 92 80 96 T160 95 T240 96 T300 94 V100 H0 Z' fill='#ff5400' "
              "opacity='0.8'/>"
            + "<path d='M8 98 Q30 78 52 98 Z M252 98 Q274 76 296 98 Z' fill='#ffba08'/>"
            + coins + embers)


def _graveyard():
    layers = ("<path d='M0 30 Q75 24 150 32 T300 28 V100 H0 Z' fill='#4a2f1f'/>"
              "<path d='M0 58 Q80 50 160 60 T300 56 V100 H0 Z' fill='#3b2416'/>"
              "<path d='M0 84 Q70 78 150 86 T300 82 V100 H0 Z' fill='#2b1a10'/>")
    roots = "".join(f"<path d='M{x} 0 Q{x + 8} 10 {x + 2} 20 T{x + 6} 34' stroke='#6b4226' "
                    "stroke-width='2' fill='none'/>" for x in (30, 140, 250))
    pebbles = "".join(f"<ellipse cx='{x}' cy='{y}' rx='3' ry='2' fill='#6e5240'/>"
                      for x, y in ((50, 44), (118, 70), (190, 40), (232, 76), (276, 50),
                                   (12, 72), (160, 92)))
    bones = "".join(_bone(x, y, a) for x, y, a in ((40, 56, 20), (96, 40, -30), (150, 70, 70),
                                                   (206, 54, -10), (262, 66, 35), (120, 90, 5),
                                                   (20, 90, -40)))
    skulls = _skull(70, 76, -12) + _skull(240, 36, 15) + _skull(180, 88, 0)
    colours = ("<style>.bone, .skull { fill: #e8dfc4; } .hole { fill: #2b1a10; }</style>")
    return (colours + _sky("#5a3a25", "#2b1a10") + layers + roots + pebbles + bones + skulls)


def _plain():
    return _sky("#3a2f6b", "#2b2945")


# Keyed by the scene names used in game.OPPONENTS (Opponent.scene).
SCENES = {
    "swamp": Scene("Slime Swamp", _swamp(), "#1c3a27",
                   "repeating-linear-gradient(90deg, #4b5d2a 0 18px, #3e4f22 18px 36px)"),
    "cave": Scene("Goblin Cave", _cave(), "#1b1324",
                  "repeating-linear-gradient(90deg, #4a4453 0 30px, #3b3643 30px 60px)"),
    "camp": Scene("Orc War Camp", _camp(), "#4a2c2a",
                  "repeating-linear-gradient(90deg, #7a5c3e 0 24px, #6b4f35 24px 48px)"),
    "bridge": Scene("Troll Bridge", _bridge(), "#4a6d8c",
                    "repeating-linear-gradient(90deg, #8d9199 0 20px, #777b83 20px 40px)"),
    "volcano": Scene("Dragon's Volcano", _volcano(), "#1a0505",
                     "repeating-linear-gradient(90deg, #2a2320 0 40px, #ff6d00 40px 42px)"),
    # Not an opponent's scene: shown when the player is defeated (R10).
    "graveyard": Scene("Dirt and Bones", _graveyard(), "#2b1a10",
                       "repeating-linear-gradient(90deg, #3a2416 0 22px, #2e1c11 22px 44px)"),
    # For an opponent with no scene of its own.
    "plain": Scene("Open Field", _plain(), "#2b2945",
                   "repeating-linear-gradient(90deg, #7a5c3e 0 24px, #6b4f35 24px 48px)"),
}

GRAVEYARD = "graveyard"
PLAIN = "plain"


def scene_key(opponent):
    """The opponent's scene key, or the plain scene if it has none we know."""
    key = getattr(opponent, "scene", "")
    return key if key in SCENES else PLAIN


def sky_url(scene):
    """The scene's picture as a CSS url(...) holding the whole SVG ("data URL").

    quote() percent-encodes characters such as < > # ' that would otherwise break
    the CSS or the HTML around it, e.g. '<' becomes '%3C'.
    """
    svg = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 100' "
           f"preserveAspectRatio='xMidYMax slice'>{scene.svg}</svg>")
    return f'url("data:image/svg+xml,{quote(svg)}")'


def scene_css():
    """CSS rules that paint every scene. A battle page wraps its stage and floor in an
    element with the class `scene-<key>`. The `.sky` and `.ground` versions are for the
    old scene that is shown leaving during a scene change (R9, R10)."""
    rules = []
    for key, scene in SCENES.items():
        rules.append(f".scene-{key} > .stage, .scene-{key} > .sky {{ "
                     f"background: {sky_url(scene)} center bottom / cover no-repeat {scene.base}; }}")
        rules.append(f".scene-{key} > .floor, .scene-{key} > .ground {{ "
                     f"background: {scene.ground}; }}")
    return "\n".join(rules) + "\n"
