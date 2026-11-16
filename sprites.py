"""Pictures (sprites) for the heroes and monsters of Math Quest.

Each sprite is drawn as SVG: text that describes shapes (circles, rectangles, ...)
which the browser turns into a picture. Keeping them as Python strings means the game
still needs no image files. Every sprite is drawn on a 64 x 64 grid.

Round 5 redrew every sprite in more detail (R11) and marked the parts that move
(R12); see the comment above HEROES.
"""

from dataclasses import dataclass
from html import escape


@dataclass(frozen=True)
class Sprite:
    name: str   # shown to the player, and read out by screen readers
    svg: str    # the shapes inside the <svg> element
    faces: str = "right"   # which way the drawing looks: "left" or "right" (R6)
    given_name: str = ""   # a hero's personal name, shown to the player (R13)


# Round 5 (R11, R12): detailed sprites. Every sprite has:
#   sp-shadow  a soft shadow on the ground (does not move)
#   sp-body    everything else; it "breathes" (squashes a little from the feet)
#   sp-eye     the eyes; they blink, wince when hit, and close on a knockout
#   sp-sway    loose parts (cape, plume, beard, ears, wings) that swing gently
#   sp-glow    glowing things (orb, fire) that flicker and burst on an attack
#   sp-weapon  the weapon; it swings on an attack. Its style sets the pivot (the hand).
#              Weapons on sprites drawn facing left also get sp-left (swing the other way).
# Animated parts never have a transform= attribute: the CSS animation would replace it.
# The page's CSS for these classes lives in web.py.
OUTLINE = "stroke='#1a1626' stroke-width='1' stroke-linejoin='round'"
SHADOW = "<ellipse class='sp-shadow' cx='{0}' cy='61' rx='{1}' ry='2.6' fill='#000' opacity='0.35'/>"

HEROES = {
    "knight": Sprite("Knight", given_name="Sir Aldric", svg=SHADOW.format(32, 17) + f"""
        <g class='sp-body' {OUTLINE}>
        <g class='sp-sway'>
          <path d='M23 30 Q13 42 14 58 L29 55 L29 31 Z' fill='#9d0208'/>
          <path d='M20 38 Q17 48 18 57' fill='none' stroke='#6a040f' stroke-width='1.5'/></g>
        <path d='M24 47 h6 v9 h-6 Z' fill='#8d99a6'/>
        <path d='M34 47 h6 v9 h-6 Z' fill='#8d99a6'/>
        <path d='M24 50.5 h6 M34 50.5 h6' stroke='#5c5f66'/>
        <path d='M22 56 h9 v4 h-10 Q21 57 22 56 Z' fill='#5c5f66'/>
        <path d='M33 56 h9 Q44 58 43 60 h-10 Z' fill='#5c5f66'/>
        <path d='M22 32 Q32 28 42 32 L40 48 Q32 50 24 48 Z' fill='#b8c2cc'/>
        <path d='M34 29.6 Q38.5 30.3 41.8 32 L39.8 47.8 Q37 48.8 34 49 Z' fill='#9aa5b1' stroke='none'/>
        <path d='M27 33 Q26 40 28 46' fill='none' stroke='#eef2f5' stroke-width='1.5'/>
        <path d='M30.5 34 h3 v3 h3 v3 h-3 v4 h-3 v-4 h-3 v-3 h3 Z' fill='#e63946' stroke-width='0.6'/>
        <rect x='23' y='45' width='18' height='3' fill='#6d4c41'/>
        <rect x='30.5' y='44.5' width='4' height='4' fill='#ffd166'/>
        <circle cx='22' cy='32' r='4.5' fill='#c0c8d0'/>
        <path d='M8 31 h14 v10 q0 9 -7 12 q-7 -3 -7 -12 Z' fill='#457b9d'/>
        <path d='M10 33 h10 v8 q0 6.5 -5 9 q-5 -2.5 -5 -9 Z' fill='none' stroke='#ffd166' stroke-width='1.2'/>
        <path d='M11.5 38 l3.5 4 l3.5 -4' fill='none' stroke='#ffd166' stroke-width='1.6'/>
        <path d='M42 33 L46.5 42' stroke='#8d99a6' stroke-width='4.5' stroke-linecap='round'/>
        <circle cx='42' cy='32' r='4.5' fill='#c0c8d0'/>
        <path class='sp-sway' d='M32 10 Q31 5 28 4 Q20 2 14 8 Q21 7 25 11 Q20 12 18 16 Q26 11 32 12 Z' fill='#e63946'/>
        <path d='M22 23 Q22 9 32 9 Q42 9 42 23 L41 28 Q32 31 23 28 Z' fill='#c0c8d0'/>
        <path d='M36 10 Q42 12 42 23 L41 28 Q38.5 29 36 29.3 Z' fill='#9aa5b1' stroke='none'/>
        <path d='M26 12 Q24 16 24 22' fill='none' stroke='#eef2f5' stroke-width='1.3'/>
        <rect x='28' y='17.5' width='14' height='4' rx='1.5' fill='#1a1626'/>
        <g class='sp-eye'><circle cx='34' cy='19.5' r='1.1' fill='#ffd166' stroke='none'/>
          <circle cx='39' cy='19.5' r='1.1' fill='#ffd166' stroke='none'/></g>
        <path d='M35 24 v3 M38 24 v3' stroke='#5c5f66'/>
        <g class='sp-weapon' style='transform-origin:47px 43.5px'>
          <path d='M45.5 40 L45.5 11 L47.5 7 L49.5 11 L49.5 40 Z' fill='#e9ecef'/>
          <path d='M47.5 11 V39' stroke='#adb5bd' stroke-width='0.8'/>
          <rect x='41.5' y='39' width='12' height='3' rx='1' fill='#ffd166'/>
          <rect x='46.5' y='42' width='2' height='6' fill='#6d4c41'/>
          <circle cx='47.5' cy='49' r='1.6' fill='#ffd166'/>
          <circle cx='47' cy='43.5' r='2.6' fill='#8d99a6'/></g>
        </g>"""),
    "wizard": Sprite("Wizard", given_name="Zoltan", svg=SHADOW.format(33, 16) + f"""
        <g class='sp-body' {OUTLINE}>
        <path d='M19 60 L25 30 L39 30 L46 60 Z' fill='#5e3c99'/>
        <path d='M34 30 L39 30 L46 60 L37 60 Z' fill='#4a2f7a' stroke='none'/>
        <path d='M19.6 57 L45.4 57 L46 60 L19 60 Z' fill='#ffd166'/>
        <path d='M27 45 l1 2 l2.2 .3 l-1.6 1.5 l.4 2.2 l-2 -1 l-2 1 l.4 -2.2 l-1.6 -1.5 l2.2 -.3 Z' fill='#ffd166' stroke='none'/>
        <path d='M38 47 a3 3 0 1 0 2.5 5 a2.4 2.4 0 1 1 -2.5 -5 Z' fill='#ffd166' stroke='none'/>
        <circle cx='31' cy='53' r='0.8' fill='#ffd166' stroke='none'/>
        <circle cx='24' cy='51' r='0.8' fill='#ffd166' stroke='none'/>
        <path d='M25 39 Q32 42 39 39' fill='none' stroke='#ffd166' stroke-width='1.5'/>
        <path d='M33 41 l-1 6 M34 41 l1 6' stroke='#ffd166'/>
        <path d='M37 32 Q45 33 49 37 L47 41 Q41 38 36 38 Z' fill='#5e3c99'/>
        <circle cx='33' cy='24' r='7' fill='#f1c27d'/>
        <g class='sp-sway'>
          <path d='M26.5 25 Q33 30 39.5 25 Q39 37 33.5 43 Q28 36 26.5 25 Z' fill='#eeeeee'/>
          <path d='M31 31 Q32 36 33 40 M35 30 Q35.5 35 34.5 39' fill='none' stroke='#c9c9c9' stroke-width='0.8'/></g>
        <path d='M30 27.5 Q33.5 25.5 38 27.5 Q34 28.8 30 27.5 Z' fill='#dddddd'/>
        <path d='M38.5 23 Q41.5 24.5 39 26' fill='#e0a96d'/>
        <g class='sp-eye'><circle cx='33.5' cy='22.5' r='1.1' fill='#222' stroke='none'/>
          <circle cx='37.5' cy='22.5' r='1.1' fill='#222' stroke='none'/></g>
        <path d='M31.5 20.3 h3.5 M36 20.3 h3' stroke='#eeeeee' stroke-width='1.4'/>
        <path d='M23 18 Q27 10 30 4 Q26 2 21 5 Q26 -1 33 2 Q37 9 41.5 18 Z' fill='#5e3c99'/>
        <path d='M34 3.5 Q37.5 9.5 41.5 18 L37 18 Q35 10 34 3.5 Z' fill='#4a2f7a' stroke='none'/>
        <ellipse cx='32' cy='18' rx='14' ry='3' fill='#4a2f7a'/>
        <path d='M25.8 12.5 L38 12.5 L39 14.8 L24.8 14.8 Z' fill='#ffd166'/>
        <path d='M31 6 l.8 1.6 l1.7 .2 l-1.3 1.2 l.3 1.7 l-1.5 -.8 l-1.5 .8 l.3 -1.7 l-1.3 -1.2 l1.7 -.2 Z' fill='#ffd166' stroke='none'/>
        <g class='sp-weapon' style='transform-origin:48.6px 38.5px'>
          <rect x='47.3' y='14' width='2.6' height='46' rx='1.2' fill='#8d6e63'/>
          <path d='M47.3 26 h2.6 M47.3 50 h2.6' stroke='#5d4037'/>
          <path d='M44.5 15 Q48.6 6 52.7 15' fill='none' stroke='#6d4c41' stroke-width='2'/>
          <circle class='sp-glow' cx='48.6' cy='10' r='4.5' fill='#4cc9f0'/>
          <circle cx='47.2' cy='8.6' r='1.4' fill='#e0fbfc' stroke='none'/>
          <path class='sp-glow' d='M56 4 l1 2 l2 1 l-2 1 l-1 2 l-1 -2 l-2 -1 l2 -1 Z' fill='#e0fbfc' stroke='none'/>
          <circle cx='48.6' cy='38.5' r='2.4' fill='#f1c27d'/></g>
        </g>"""),
    "archer": Sprite("Archer", given_name="Wren", svg=SHADOW.format(32, 16) + f"""
        <g class='sp-body' {OUTLINE}>
        <g class='sp-sway'>
          <path d='M23 26 Q14 40 16 52 L25 48 L27 30 Z' fill='#40916c'/>
          <path d='M20 36 Q18 44 18.5 50' fill='none' stroke='#2d6a4f' stroke-width='1.2'/></g>
        <path d='M18 26 L15 19 M20 25.5 L18 18 M21.5 25 L21 18' stroke='#d4a373' stroke-width='1.2'/>
        <path d='M15 19 l-2 -3 l3 1 Z M18 18 l-1.5 -3.2 l2.8 1.4 Z M21 18 l-0.5 -3.5 l2 2.2 Z' fill='#e63946' stroke-width='0.6'/>
        <path d='M17 27 L22 25 L27 43 L22 45 Z' fill='#7f5539'/>
        <path d='M18.5 30 L23.5 28' stroke='#5c4033'/>
        <path d='M25 49 h5 v8 h-5 Z' fill='#5c4033'/>
        <path d='M34 49 h5 v8 h-5 Z' fill='#5c4033'/>
        <path d='M24 56 h7 v4 h-8 Z' fill='#3e2723'/>
        <path d='M33 56 h7 Q43 58 42 60 h-9 Z' fill='#3e2723'/>
        <path d='M23 31 Q32 28 41 31 L42 50 L39 48 L36 51 L32 48 L28 51 L25 48 L22 50 Z' fill='#2d6a4f'/>
        <path d='M35 29.8 Q38.5 30 40.9 31 L41.9 49.8 L39 48 L36 50.8 Z' fill='#1b4332' stroke='none'/>
        <rect x='23' y='42' width='18.5' height='3' fill='#6d4c41'/>
        <rect x='31' y='41.5' width='3.5' height='4' fill='#ffd166'/>
        <path d='M24 31 L36 42' stroke='#5c4033' stroke-width='1.4'/>
        <path d='M38 32 L51 34' stroke='#2d6a4f' stroke-width='4' stroke-linecap='round'/>
        <path d='M22 25 Q22 8 33 9 Q44 10 43 23 L40 30 L25 31 Z' fill='#40916c'/>
        <circle cx='34' cy='21' r='7' fill='#e0ac69'/>
        <path d='M27 18 Q33 11 41 16 Q35 15 33 18 Q30 16 27 20 Z' fill='#9c4a1a'/>
        <path d='M27.5 22 Q25.5 28 27 33' fill='none' stroke='#9c4a1a' stroke-width='2'/>
        <g class='sp-eye'><ellipse cx='34.5' cy='21' rx='1' ry='1.3' fill='#222' stroke='none'/>
          <ellipse cx='38.7' cy='21' rx='1' ry='1.3' fill='#222' stroke='none'/></g>
        <path d='M35 25.5 Q37 26.8 39 25.3' fill='none' stroke='#7a3e1d' stroke-width='0.9'/>
        <circle cx='32.5' cy='23.5' r='0.5' fill='#b5651d' stroke='none'/>
        <circle cx='40' cy='23.3' r='0.5' fill='#b5651d' stroke='none'/>
        <g class='sp-weapon' style='transform-origin:53px 34px'>
          <path d='M46 12 Q60 34 46 56' fill='none' stroke='#8d6e63' stroke-width='3'/>
          <path d='M46 12 L46 56' stroke='#eeeeee' stroke-width='0.7'/>
          <path d='M37 34 L58 34' stroke='#d4a373' stroke-width='1.5'/>
          <path d='M58 32 L62 34 L58 36 Z' fill='#ced4da'/>
          <path d='M37 34 l-3 -2.5 h3 l2 2.5 l-2 2.5 h-3 Z' fill='#e63946' stroke-width='0.6'/>
          <rect x='51.5' y='31' width='3' height='6' rx='1' fill='#3e2723' stroke='none'/>
          <circle cx='53' cy='34' r='2.2' fill='#e0ac69'/></g>
        </g>"""),
    "ninja": Sprite("Ninja", given_name="Kaito", svg=SHADOW.format(32, 16) + f"""
        <g class='sp-body' {OUTLINE}>
        <g class='sp-sway'>
          <path d='M22 13 Q14 9 5 13 Q11 14.5 9 19 Q15 14.5 22 17 Z' fill='#e63946'/>
          <path d='M21 15 Q13 15 7 22 Q13 20 21 17.5 Z' fill='#c1121f'/></g>
        <path d='M24 47 h6 v10 h-6 Z' fill='#3d405b'/>
        <path d='M34 47 h6 v10 h-6 Z' fill='#3d405b'/>
        <path d='M24 51 h6 M24 54 h6 M34 51 h6 M34 54 h6' stroke='#8d99ae' stroke-width='0.8'/>
        <path d='M23 57 h8 v3 h-9 Z' fill='#2b2d42'/>
        <path d='M33 57 h8 Q43 58.5 42 60 h-9 Z' fill='#2b2d42'/>
        <path d='M22 31 Q32 27 42 31 L41 48 L23 48 Z' fill='#3d405b'/>
        <path d='M34 29.5 Q39 30 41.9 31 L41 47.9 L35 47.9 Z' fill='#2b2d42' stroke='none'/>
        <path d='M26 31 L32 40 L38 31' fill='none' stroke='#2b2d42' stroke-width='1.3'/>
        <rect x='22.5' y='41' width='19' height='3.5' fill='#e63946'/>
        <path d='M25 44.5 l-2 6 l3 -1 Z M27 44.5 l1 6 l-3 -1.5 Z' fill='#c1121f' stroke-width='0.7'/>
        <path d='M37 39.5 L38 41.5 L40 42.5 L38 43.5 L37 45.5 L36 43.5 L34 42.5 L36 41.5 Z' fill='#adb5bd' stroke-width='0.6'/>
        <path d='M40 32 L45 40' stroke='#3d405b' stroke-width='4.5' stroke-linecap='round'/>
        <circle cx='32' cy='20' r='11' fill='#3d405b'/>
        <path d='M38 11 Q43 14 43 20 Q43 26.5 38.5 29.5 Q41 21 38 11 Z' fill='#2b2d42' stroke='none'/>
        <rect x='25' y='16.5' width='17' height='6' rx='3' fill='#f1c27d'/>
        <path d='M29.5 17.6 L33 18.7 M36 18.7 L39.5 17.6' stroke='#1a1626'/>
        <g class='sp-eye'><ellipse cx='31.5' cy='20' rx='1.2' ry='1.4' fill='#222' stroke='none'/>
          <ellipse cx='37.5' cy='20' rx='1.2' ry='1.4' fill='#222' stroke='none'/>
          <circle cx='31.9' cy='19.5' r='0.4' fill='#fff' stroke='none'/>
          <circle cx='37.9' cy='19.5' r='0.4' fill='#fff' stroke='none'/></g>
        <rect x='21' y='11.5' width='22' height='3.2' fill='#e63946'/>
        <rect x='29.5' y='11' width='8' height='4.2' rx='0.8' fill='#adb5bd'/>
        <path d='M31.5 13 h4' stroke='#6c757d' stroke-width='0.8'/>
        <path d='M34 26 Q36 25.5 38 26' fill='none' stroke='#2b2d42'/>
        <g class='sp-weapon' style='transform-origin:45px 41px'>
          <path d='M45.5 38 L55 10 Q57.5 9 57 11.5 L48 39 Z' fill='#e9ecef'/>
          <path d='M47 38 L55.6 12' stroke='#adb5bd' stroke-width='0.6'/>
          <rect x='43' y='37.2' width='8' height='2.4' rx='1' fill='#ffd166'/>
          <path d='M45.5 40 L43.5 46' stroke='#e63946' stroke-width='2.4' stroke-linecap='round'/>
          <circle cx='45' cy='41' r='2.3' fill='#2b2d42'/></g>
        </g>"""),
}

DEFAULT_HERO = "knight"

# Keyed by the first word of each opponent's name in game.OPPONENTS.
MONSTERS = {
    "slime": Sprite("Slime", svg="""
        <ellipse class='sp-shadow' cx='32' cy='59' rx='26' ry='3' fill='#000' opacity='0.35'/>
        <g class='sp-body sp-squish' stroke='#1a1626' stroke-width='1.2' stroke-linejoin='round'>
        <path d='M6 56 Q4 40 14 30 Q22 17 32 17 Q42 17 50 30 Q60 40 58 56 Q32 60 6 56 Z' fill='#80ed99'/>
        <path d='M8.5 51 Q32 57 55.5 51 Q57.5 54 58 56 Q32 60 6 56 Q6.5 53 8.5 51 Z' fill='#57cc99' stroke='none'/>
        <path d='M46 30 Q56 40 56 52 Q51 50 50 42 Q49 35 46 30 Z' fill='#57cc99' stroke='none'/>
        <g class='sp-sway' style='transform-origin:50% 100%'>
          <path d='M29 18 Q30 8 37 10 Q33 12 35 17.5 Z' fill='#80ed99'/>
          <circle cx='32' cy='12' r='0.9' fill='#e9fff0' stroke='none'/></g>
        <path d='M47 55 Q48.5 62 50 55' fill='#57cc99'/>
        <path d='M12 55 Q13 59.5 14.5 55' fill='#57cc99'/>
        <ellipse cx='20' cy='27' rx='5' ry='2.6' fill='#e9fff0' stroke='none'/>
        <circle cx='14.5' cy='33' r='1.4' fill='#e9fff0' stroke='none'/>
        <path d='M27 22 l.6 1.4 l1.4 .6 l-1.4 .6 l-.6 1.4 l-.6 -1.4 l-1.4 -.6 l1.4 -.6 Z' fill='#fff' stroke='none'/>
        <circle cx='44' cy='45' r='2.2' fill='#c7f9cc' stroke='#57cc99' stroke-width='0.6' opacity='0.8'/>
        <circle cx='49' cy='38' r='1.4' fill='#c7f9cc' stroke='#57cc99' stroke-width='0.6' opacity='0.8'/>
        <circle cx='40' cy='52' r='1' fill='#c7f9cc' stroke='none'/>
        <circle cx='52' cy='47' r='0.8' fill='#c7f9cc' stroke='none'/>
        <circle cx='45' cy='25' r='1.1' fill='#c7f9cc' stroke='none'/>
        <path d='M39 31 h4 M41 29 v4' stroke='#2d6a4f' stroke-width='1.3' opacity='0.6'/>
        <g class='sp-eye'>
          <ellipse cx='21' cy='38' rx='4.2' ry='5' fill='#ffffff'/>
          <ellipse cx='34' cy='38' rx='4.2' ry='5' fill='#ffffff'/>
          <circle cx='19.6' cy='39' r='2.4' fill='#222' stroke='none'/>
          <circle cx='32.6' cy='39' r='2.4' fill='#222' stroke='none'/>
          <circle cx='18.8' cy='38' r='0.8' fill='#fff' stroke='none'/>
          <circle cx='31.8' cy='38' r='0.8' fill='#fff' stroke='none'/></g>
        <ellipse cx='14.5' cy='45' rx='3' ry='1.6' fill='#ff8fab' opacity='0.5' stroke='none'/>
        <ellipse cx='39.5' cy='45' rx='3' ry='1.6' fill='#ff8fab' opacity='0.5' stroke='none'/>
        <path d='M20 46 Q26.5 53 33 46 Z' fill='#1b4332'/>
        <path d='M23 49 Q26.5 52 30 49.2 Q26.5 47.8 23 49 Z' fill='#ff6b8a' stroke='none'/>
        </g>""", faces="left"),
    "goblin": Sprite("Goblin", svg=SHADOW.format(32, 15) + f"""
        <g class='sp-body' {OUTLINE}>
        <path d='M26 50 h4 v7 h-4 Z' fill='#6a994e'/>
        <path d='M34 50 h4 v7 h-4 Z' fill='#6a994e'/>
        <path d='M20 57 Q22 55 30 56 v3.5 h-10 Z' fill='#7f5539'/>
        <path d='M33 56 h7 v3.5 h-8 Z' fill='#7f5539'/>
        <path d='M41 37 Q45 42 43 47' fill='none' stroke='#6a994e' stroke-width='3.5' stroke-linecap='round'/>
        <path d='M23 36 Q32 33 41 36 L40 50 L24 50 Z' fill='#6a994e'/>
        <path d='M30 39 Q32 40 34 39 M30 42 Q32 43 34 42' fill='none' stroke='#386641' stroke-width='0.8'/>
        <path d='M23 36 Q26 35 29 34.5 L28 47 L23.5 47 Z' fill='#7f5539'/>
        <path d='M41 36 Q38 35 35 34.5 L36 47 L40.5 47 Z' fill='#7f5539'/>
        <path d='M23 46 L41 46 L40 53 L37 51 L34 54 L31 51 L28 54 L25 51 L24 53 Z' fill='#9c6644'/>
        <rect x='23' y='45' width='18' height='2.5' fill='#582f0e'/>
        <path d='M30.5 46.2 h3' stroke='#ffd166' stroke-width='1.2'/>
        <path d='M24 37 Q19 39 17 41' fill='none' stroke='#6a994e' stroke-width='3.5' stroke-linecap='round'/>
        <g class='sp-sway' style='transform-origin:100% 50%'>
          <path d='M21 24 L2 15 L20 31 Z' fill='#6a994e'/>
          <path d='M18 24.5 L7 18 L18 28 Z' fill='#bc6c25' stroke='none'/></g>
        <g class='sp-sway' style='transform-origin:0% 50%'>
          <path d='M43 24 L62 15 L44 31 Z' fill='#6a994e'/>
          <path d='M46 24.5 L57 18 L46 28 Z' fill='#bc6c25' stroke='none'/></g>
        <circle cx='32' cy='26' r='12' fill='#6a994e'/>
        <path d='M37 15.5 Q44 19 44 26 Q43.5 33 38 37 Q41.5 27 37 15.5 Z' fill='#588157' stroke='none'/>
        <path d='M26 15 Q27 11 29 14 M32 14 Q33 10 35 14' fill='none' stroke='#1a1626' stroke-width='0.9'/>
        <g class='sp-eye'>
          <ellipse cx='26' cy='23' rx='3' ry='2.6' fill='#ffd60a'/>
          <ellipse cx='35' cy='23' rx='3' ry='2.6' fill='#ffd60a'/>
          <ellipse cx='25' cy='23' rx='0.9' ry='2' fill='#222' stroke='none'/>
          <ellipse cx='34' cy='23' rx='0.9' ry='2' fill='#222' stroke='none'/></g>
        <path d='M22 19 L29 21 M31.5 21 L38 19' stroke='#1a1626' stroke-width='1.4' stroke-linecap='round'/>
        <path d='M27 26 Q18 29 22 31.5 Q25 31 29 29 Z' fill='#588157'/>
        <circle cx='38' cy='29' r='1' fill='#386641' stroke='none'/>
        <path d='M24 33 Q31 38 38 33 Q31 35.5 24 33 Z' fill='#1a1626'/>
        <path d='M26 33.6 l1 1.6 l1 -1.2 Z M33 34.4 l1 1.4 l1 -1.6 Z' fill='#fff' stroke='none'/>
        <g class='sp-weapon sp-left' style='transform-origin:17.8px 41px'>
          <path d='M16 39.5 L8 27 Q7.5 25.5 9 26 L18.5 38.5 Z' fill='#ced4da'/>
          <path d='M16.8 39 L9 27' stroke='#868e96' stroke-width='0.6'/>
          <path d='M13.5 40.5 L19.5 36.5' stroke='#582f0e' stroke-width='2' stroke-linecap='round'/>
          <path d='M17.5 40 L19.5 43.5' stroke='#7f5539' stroke-width='2.2' stroke-linecap='round'/>
          <circle cx='17.8' cy='41' r='2.2' fill='#6a994e'/></g>
        </g>""", faces="left"),
    "orc": Sprite("Orc", svg=SHADOW.format(32, 20) + f"""
        <g class='sp-body' {OUTLINE}>
        <path d='M20 50 h9 v8 h-9 Z' fill='#5c4033'/>
        <path d='M35 50 h9 v8 h-9 Z' fill='#5c4033'/>
        <path d='M18 57 h12 v3 h-12 Z' fill='#3e2723'/>
        <path d='M34 57 h12 Q48 58.5 47 60 h-13 Z' fill='#3e2723'/>
        <path d='M14 34 Q32 26 50 34 L47 52 L17 52 Z' fill='#4f772d'/>
        <path d='M38 29.8 Q46 31 49.9 34 L46.9 51.9 L40 51.9 Z' fill='#31572c' stroke='none'/>
        <path d='M24 38 Q28 41 31 38 M33 38 Q36 41 40 38' fill='none' stroke='#31572c' stroke-width='1.2'/>
        <path d='M28 39.5 L36 45 M36 39.5 L28 45' stroke='#d00000' stroke-width='1.8' stroke-linecap='round'/>
        <path d='M16 48 L48 48 L47 55 L43 53 L39 56 L35 53 L31 56 L27 53 L23 56 L19 53 L17 55 Z' fill='#8d6e63'/>
        <rect x='16' y='46.5' width='32' height='3.5' fill='#3e2723'/>
        <circle cx='32' cy='48.2' r='2.6' fill='#e9ecef'/>
        <circle cx='31' cy='47.8' r='0.6' fill='#1a1626' stroke='none'/>
        <circle cx='33' cy='47.8' r='0.6' fill='#1a1626' stroke='none'/>
        <path d='M10 32 Q16 26 22 31 L20 37 Q14 37 10 32 Z' fill='#6c757d'/>
        <path d='M12 30 L11 25 L14.5 28.5 Z M17 28 L17 22 L20 27 Z' fill='#ced4da'/>
        <path d='M46 34 Q52 38 52 44' fill='none' stroke='#4f772d' stroke-width='6' stroke-linecap='round'/>
        <path d='M49.5 39.5 h5' stroke='#5c4033' stroke-width='2.5'/>
        <path d='M19 18 L13 15 L19 25 Z' fill='#4f772d'/>
        <g class='sp-sway' style='transform-origin:50% 100%'>
          <path d='M30 10 Q28 2 33 1 Q31 5 36 4 Q33 7 34 10 Z' fill='#1a1626'/></g>
        <rect x='19' y='9' width='26' height='25' rx='8' fill='#4f772d'/>
        <path d='M38 9.2 Q44.8 10.5 44.8 18 L44.8 28 Q44 33.5 38 33.8 Z' fill='#31572c' stroke='none'/>
        <path d='M22 18 L30 20.5 M34 20.5 L42 18' stroke='#1a1626' stroke-width='2.4' stroke-linecap='round'/>
        <g class='sp-eye'><circle cx='27.5' cy='22.5' r='2' fill='#d00000'/>
          <circle cx='37.5' cy='22.5' r='2' fill='#d00000'/>
          <circle cx='28' cy='22' r='0.6' fill='#ffd166' stroke='none'/>
          <circle cx='38' cy='22' r='0.6' fill='#ffd166' stroke='none'/></g>
        <path d='M30.5 25 Q32.5 27.5 34.5 25' fill='#31572c'/>
        <path d='M24 30 Q32 27 40 30 L39 33 Q32 31 25 33 Z' fill='#1a1626'/>
        <path d='M25.5 31 L26.5 25 L28.8 31 Z' fill='#fffbe6'/>
        <path d='M35.2 31 L37.5 25 L38.5 31 Z' fill='#fffbe6'/>
        <path d='M21 27 L24 24' stroke='#d00000' stroke-width='1.2'/>
        <g class='sp-weapon' style='transform-origin:52.2px 45px'>
          <rect x='50.5' y='16' width='3.4' height='42' rx='1.4' fill='#8d6e63'/>
          <path d='M50.5 26 h3.4 M50.5 30 h3.4' stroke='#5d4037'/>
          <path d='M54 17 Q63 18 63 26 Q63 33 54 33 Z' fill='#adb5bd'/>
          <path d='M50.5 19 Q45 21 45.5 25 Q45.5 29 50.5 31 Z' fill='#adb5bd'/>
          <path d='M56 19 Q61 21 61 26 Q61 31 56 32' fill='none' stroke='#e9ecef' stroke-width='1.2'/>
          <path d='M52.2 16 L52.2 11' stroke='#adb5bd' stroke-width='2'/>
          <circle cx='52.2' cy='45' r='3.2' fill='#4f772d'/></g>
        </g>"""),
    "troll": Sprite("Troll", svg=SHADOW.format(34, 22) + f"""
        <g class='sp-body' {OUTLINE}>
        <path d='M52 36 Q58 44 54 50' fill='none' stroke='#6b7a6c' stroke-width='6' stroke-linecap='round'/>
        <path d='M21 50 h9 v8 h-9 Z' fill='#7d8a7e'/>
        <path d='M36 50 h9 v8 h-9 Z' fill='#7d8a7e'/>
        <path d='M17 56 Q19 54 30 55 v5 h-13 Z' fill='#7d8a7e'/>
        <path d='M36 55 h11 Q49 58 48 60 h-12 Z' fill='#7d8a7e'/>
        <path d='M18.5 60 v-2 M21.5 60 v-2 M24.5 60 v-2' stroke='#4a524b' stroke-width='0.9'/>
        <path d='M12 42 Q12 24 34 24 Q56 24 56 44 Q56 54 44 54 L22 54 Q12 54 12 42 Z' fill='#8a9a8b'/>
        <path d='M44 25.5 Q55.8 30 55.8 44 Q55.8 53.8 44 53.8 Q50 44 44 25.5 Z' fill='#6b7a6c' stroke='none'/>
        <ellipse cx='32' cy='44' rx='11' ry='8' fill='#b5c2a8'/>
        <path d='M27 42 Q32 44 37 42' fill='none' stroke='#8a9a8b' stroke-width='0.9'/>
        <circle cx='32' cy='46.5' r='0.8' fill='#6b7a6c' stroke='none'/>
        <path d='M40 27 Q45 25 49 29 Q45 30 40 27 Z' fill='#588157' stroke='none'/>
        <path d='M15 38 Q17 34 20 36 Q18 39 15 38 Z' fill='#588157' stroke='none'/>
        <path d='M20 50 L46 50 L45 56 L40 54 L35 57 L30 54 L25 57 L21 55 Z' fill='#7f5539'/>
        <rect x='19.5' y='48.5' width='27' height='3' fill='#582f0e'/>
        <path d='M36 18 L40 14 L37.5 22 Z' fill='#8a9a8b'/>
        <circle cx='26' cy='22' r='11' fill='#8a9a8b'/>
        <path class='sp-sway' style='transform-origin:50% 100%' d='M16 18 Q18 9 24 11 M28 11 Q32 6 35 12' fill='none' stroke='#4a524b' stroke-width='1.6'/>
        <path d='M17 21 L24 23 M28 23 L34 21' stroke='#1a1626' stroke-width='1.6' stroke-linecap='round'/>
        <g class='sp-eye'><circle cx='20.5' cy='24.5' r='1.6' fill='#ffd166'/>
          <circle cx='30.5' cy='24.5' r='1.6' fill='#ffd166'/>
          <circle cx='20' cy='24.5' r='0.8' fill='#222' stroke='none'/>
          <circle cx='30' cy='24.5' r='0.8' fill='#222' stroke='none'/></g>
        <ellipse cx='23' cy='28.5' rx='5' ry='3.8' fill='#6b7a6c'/>
        <circle cx='21' cy='29.5' r='0.7' fill='#1a1626' stroke='none'/>
        <circle cx='25' cy='29.5' r='0.7' fill='#1a1626' stroke='none'/>
        <path d='M17 32 Q26 36 33 31' fill='none' stroke='#1a1626' stroke-width='1.4'/>
        <path d='M20 33.4 l1 -3 l1.4 3.3 Z M29 33 l1.4 -3 l0.6 2.8 Z' fill='#fffbe6' stroke-width='0.6'/>
        <path d='M18 36 Q12 40 11 45' fill='none' stroke='#8a9a8b' stroke-width='6' stroke-linecap='round'/>
        <g class='sp-weapon sp-left' style='transform-origin:10px 46px'>
          <path d='M8 58 L7 34 Q6 22 10 20 Q15 22 14 34 L12 58 Z' fill='#7f5539'/>
          <path d='M9 30 Q10 34 9.5 38 M12 40 Q11.5 46 12 50' fill='none' stroke='#582f0e'/>
          <path d='M7.5 27 L4 26 M13.5 31 L17 30 M7.5 36 L4 37' stroke='#adb5bd' stroke-width='1.2' stroke-linecap='round'/>
          <path d='M9 25 h3' stroke='#ffd166' stroke-width='1' stroke-linecap='round'/>
          <circle cx='10.5' cy='23.4' r='0.6' fill='#ffd166' stroke='none'/>
          <circle cx='10.5' cy='26.6' r='0.6' fill='#ffd166' stroke='none'/>
          <circle cx='10' cy='46' r='3.6' fill='#8a9a8b'/></g>
        </g>""", faces="left"),
    "dragon": Sprite("Dragon", svg=SHADOW.format(34, 20) + f"""
        <g class='sp-body' {OUTLINE}>
        <g class='sp-sway' style='transform-origin:100% 100%'>
          <path d='M28 32 L6 6 Q8 16 4 20 Q11 21 10 28 Q16 27 20 36 Z' fill='#9d0208'/>
          <path d='M26 31 L9 10 M24 33 L8 21 M22 34 L12 28' stroke='#6a040f' stroke-width='0.9'/></g>
        <g class='sp-sway' style='transform-origin:0% 100%'>
          <path d='M40 32 L60 4 Q58 14 62 18 Q55 20 57 27 Q50 26 46 36 Z' fill='#9d0208'/>
          <path d='M42 31 L57 8 M44 33 L59 18 M46 34 L55 26' stroke='#6a040f' stroke-width='0.9'/></g>
        <path d='M46 52 Q58 54 60 46 Q61 40 56 40 Q59 44 55 47 Q50 49 45 46 Z' fill='#d00000'/>
        <path d='M56 40 L61 36 L59 42 Z' fill='#ffba08'/>
        <path d='M22 50 h8 v8 h-8 Z' fill='#9d0208'/>
        <path d='M36 50 h8 v8 h-8 Z' fill='#9d0208'/>
        <path d='M21 58 l1 -2 l1 2 l1 -2 l1 2 l1 -2 l1 2 Z M35 58 l1 -2 l1 2 l1 -2 l1 2 l1 -2 l1 2 Z' fill='#fffbe6' stroke-width='0.6'/>
        <ellipse cx='33' cy='44' rx='16' ry='13' fill='#d00000'/>
        <path d='M40 33 Q48.8 38 48.8 45 Q48 54 40 56 Q45 46 40 33 Z' fill='#9d0208' stroke='none'/>
        <ellipse cx='31' cy='46' rx='9' ry='10' fill='#ffba08'/>
        <path d='M23 42 Q31 44 39 42 M22.5 47 Q31 49 39.5 47 M24 52 Q31 54 38 52' fill='none' stroke='#e85d04' stroke-width='0.9'/>
        <path d='M44 34 l3 -4 l0 5 Z M47 39 l4 -3 l-1 5 Z M48.5 45 l4 -2 l-2 4.5 Z' fill='#ffba08' stroke-width='0.7'/>
        <path d='M26 36 Q22 30 24 24 L34 22 Q36 30 34 36 Z' fill='#d00000'/>
        <path d='M33 13 L40 3 L37 14 Z' fill='#ffba08'/>
        <path d='M28 12.5 L30 3 L31.5 12.5 Z' fill='#ffba08'/>
        <path d='M30 12 Q40 12 40 20 Q40 28 32 28 L20 28 Q12 28 12 23 Q12 19 18 18 Q22 12 30 12 Z' fill='#d00000'/>
        <path d='M30 16 Q34 14 37 17 M31 20 Q35 19 38 21' fill='none' stroke='#9d0208'/>
        <path d='M13 24.5 Q20 26 27 25' fill='none' stroke='#6a040f'/>
        <circle cx='15' cy='21' r='0.9' fill='#370617' stroke='none'/>
        <path d='M18 25.3 l1 2.4 l1 -2.3 Z M23 25.6 l1 2.4 l1 -2.3 Z' fill='#fff' stroke='none'/>
        <g class='sp-eye'><ellipse cx='26' cy='18.5' rx='2.4' ry='2' fill='#ffd60a'/>
          <ellipse cx='25.5' cy='18.5' rx='0.7' ry='1.7' fill='#370617' stroke='none'/></g>
        <path d='M22 15.5 L29 17' stroke='#1a1626' stroke-width='1.4' stroke-linecap='round'/>
        <g class='sp-glow' style='transform-origin:100% 50%'>
          <path d='M12 25 Q6 22 3 25 Q6 27 2 30 Q8 30 12 26.5 Z' fill='#ff8800' stroke-width='0.6'/>
          <path d='M11 25.5 Q7 24.5 5 26 Q8 27 6 28.5 Q9 28 11 26.3 Z' fill='#ffd60a' stroke='none'/></g>
        </g>""", faces="left"),
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


def hero_name(key):
    """The personal name of a hero, such as "Kaito" (R13). Unknown keys get the
    default hero's name."""
    return HEROES[hero_or_default(key)].given_name


def render_hero(key, size=96, facing=None):
    """The <svg> element for a hero. Unknown keys get the default hero."""
    sprite = HEROES[hero_or_default(key)]
    return _svg(sprite, sprite.name, size, facing)


def render_monster(opponent, size=96, facing=None):
    """The <svg> element for an opponent, labelled with the opponent's full name."""
    sprite = MONSTERS.get(getattr(opponent, "sprite", ""), UNKNOWN_MONSTER)
    return _svg(sprite, opponent.name, size, facing)
