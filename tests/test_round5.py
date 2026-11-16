"""Round 5 tests: detailed sprites (R11), detailed and idle animations (R12),
hero names (R13), and the defeat screen (R14)."""
import re
import unittest

from game import Game, OPPONENTS
from sprites import HEROES, MIRROR, MONSTERS, render_hero, render_monster
from web import STYLE, render_game, render_title
from tests.test_web import PROBLEMS, between


class TestHeroNames(unittest.TestCase):
    """R13: each hero has a personal name, shown instead of its class word."""

    EXPECTED = {"knight": "Sir Aldric", "wizard": "Zoltan",
                "archer": "Wren", "ninja": "Kaito"}

    def test_R13_every_hero_has_its_personal_name(self):
        self.assertEqual({k: h.given_name for k, h in HEROES.items()}, self.EXPECTED)

    def test_R13_names_are_all_different_from_the_class_words(self):
        for hero in HEROES.values():
            self.assertNotEqual(hero.given_name, hero.name)

    def test_R13_picker_shows_the_names_not_the_class_words(self):
        picker = between(render_title(), "class='picker'", "</form>")
        for key, hero in HEROES.items():
            label = between(picker, f"value='{key}'", "</label>")
            after_picture = label[label.index("</svg>"):]
            self.assertIn(hero.given_name, after_picture, key)
            self.assertNotIn(hero.name, after_picture, key)

    def test_R13_picture_is_still_described_by_its_class(self):
        # Round 2 behaviour kept: screen readers hear "Ninja" for the picture.
        self.assertIn("aria-label='Ninja'", render_hero("ninja"))

    def test_R13_health_bar_uses_the_heros_name(self):
        hud = between(render_game(Game(PROBLEMS, hero="ninja")), "class='hud'", "class='world")
        self.assertIn("<b>Kaito</b>", hud)
        self.assertNotIn("<b>You</b>", hud)


SHAPES = re.compile(r"<(path|rect|circle|ellipse|line|polygon|polyline)\b")
ALL_SPRITES = {**{f"hero {k}": h for k, h in HEROES.items()},
               **{f"monster {k}": m for k, m in MONSTERS.items()}}


def tags_with_class(svg, cls):
    """Every opening tag in svg whose class list includes cls."""
    return [t for t in re.findall(r"<[a-z]+\b[^>]*>", svg)
            if re.search(rf"class='[^']*\b{cls}\b", t)]


class TestDetailedSprites(unittest.TestCase):
    """R11: sprites are drawn in much more detail."""

    def test_R11_every_sprite_has_at_least_25_shapes(self):
        for label, sprite in ALL_SPRITES.items():
            self.assertGreaterEqual(len(SHAPES.findall(sprite.svg)), 25, label)

    def test_R11_every_sprite_has_outlines(self):
        for label, sprite in ALL_SPRITES.items():
            self.assertIn("stroke='#1a1626'", sprite.svg, label)

    def test_R11_every_sprite_has_a_ground_shadow(self):
        for label, sprite in ALL_SPRITES.items():
            self.assertIn("class='sp-shadow'", sprite.svg, label)

    def test_R11_sprites_stay_on_the_64_grid_and_keep_their_facing(self):
        self.assertIn("viewBox='0 0 64 64'", render_hero("knight"))
        for opponent in OPPONENTS:
            html = render_monster(opponent, facing="left")
            self.assertIn(MONSTERS[opponent.sprite].svg, html)
            self.assertEqual(MIRROR in html, MONSTERS[opponent.sprite].faces == "right")


class TestAnimatedParts(unittest.TestCase):
    """R12: each sprite marks the parts that the page's CSS animates."""

    def test_R12_every_sprite_breathes_and_blinks(self):
        for label, sprite in ALL_SPRITES.items():
            self.assertEqual(len(tags_with_class(sprite.svg, "sp-body")), 1, label)
            self.assertTrue(tags_with_class(sprite.svg, "sp-eye"), label)

    def test_R12_every_sprite_has_something_loose_or_glowing(self):
        for label, sprite in ALL_SPRITES.items():
            moving = (tags_with_class(sprite.svg, "sp-sway")
                      + tags_with_class(sprite.svg, "sp-glow"))
            self.assertTrue(moving, label)

    def test_R12_heroes_and_armed_monsters_have_one_weapon(self):
        armed = [*(f"hero {k}" for k in HEROES), "monster goblin", "monster orc",
                 "monster troll"]
        for label in armed:
            self.assertEqual(len(tags_with_class(ALL_SPRITES[label].svg, "sp-weapon")),
                             1, label)

    def test_R12_dragon_attacks_with_fire(self):
        self.assertTrue(tags_with_class(MONSTERS["dragon"].svg, "sp-glow"))

    def test_R12_weapons_drawn_facing_left_swing_the_other_way(self):
        for label, sprite in ALL_SPRITES.items():
            for tag in tags_with_class(sprite.svg, "sp-weapon"):
                self.assertEqual("sp-left" in tag, sprite.faces == "left", label)

    def test_R12_animated_parts_have_no_transform_attribute(self):
        # A CSS animation on transform would replace the attribute and move the part.
        for label, sprite in ALL_SPRITES.items():
            for tag in re.findall(r"<[a-z]+\b[^>]*class='[^']*sp-[^>]*>", sprite.svg):
                self.assertNotIn("transform=", tag, label)

    def test_R12_part_class_names_do_not_clash_with_the_page(self):
        # Page classes like 'hero', 'foe', 'sky' or 'fill' must not appear inside sprites.
        for label, sprite in ALL_SPRITES.items():
            for classes in re.findall(r"class='([^']*)'", sprite.svg):
                for name in classes.split():
                    self.assertTrue(name.startswith("sp-"), f"{label}: {name}")


def rule(selector):
    """The declarations of the first CSS rule in STYLE with exactly this selector."""
    m = re.search(re.escape(selector) + r" \{([^}]*)\}", STYLE)
    if m is None:
        raise AssertionError(f"no CSS rule for {selector}")
    return m.group(1)


def reduced_motion_css():
    return STYLE[STYLE.index("prefers-reduced-motion"):]


class TestAnimationStyle(unittest.TestCase):
    """R12: the page's CSS moves the marked parts."""

    def test_R12_style_defines_the_new_animations(self):
        for name in ("breathe", "squish", "blink", "sway", "flicker", "weapon-ready",
                     "swing", "swing-left", "fire-burst", "wince"):
            self.assertIn(f"@keyframes {name} ", STYLE, name)

    def test_R12_idle_animations_loop_forever(self):
        for selector, name in ((".sprite .sp-body", "breathe"), (".sprite .sp-eye", "blink"),
                               (".sprite .sp-sway", "sway"), (".sprite .sp-glow", "flicker"),
                               (".sprite .sp-weapon", "weapon-ready")):
            self.assertRegex(rule(selector), rf"animation: {name} [^;]*infinite", selector)

    def test_R12_each_idle_loop_is_under_one_and_a_half_seconds(self):
        for line in re.findall(r"animation: ([^;]*infinite[^;]*);", STYLE):
            seconds = float(re.search(r"(\d*\.?\d+)s", line).group(1))
            self.assertLess(seconds, 1.5, line)

    def test_R12_attacker_swings_its_weapon_or_breathes_fire(self):
        self.assertIn("animation: swing ", rule(".attack .sp-weapon"))
        self.assertIn("swing-left", rule(".attack .sp-weapon.sp-left"))
        self.assertIn("animation: fire-burst ", rule(".attack .sp-glow"))

    def test_R12_hurt_fighter_winces(self):
        self.assertIn("animation: wince ", rule(".hurt .sp-eye"))

    def test_R12_knocked_out_fighter_stops_and_shuts_its_eyes(self):
        self.assertIn("animation: none", rule(".ko .sprite *"))
        self.assertIn("scaleY(", rule(".ko .sp-eye"))
        # The knockout rules come last, so they win over the idle and hurt rules.
        self.assertGreater(STYLE.index(".ko .sprite *"), STYLE.index(".hurt .sp-eye"))

    def test_R12_weapons_and_fire_may_reach_outside_the_sprite_box(self):
        self.assertIn("overflow: visible", rule(".sprite"))

    def test_R12_reduced_motion_stops_all_sprite_movement(self):
        self.assertRegex(reduced_motion_css(), r"\.sprite \*[^{]*\{ animation: none !important")

    def test_R12_battle_page_fighters_carry_the_animated_parts(self):
        world = between(render_game(Game(PROBLEMS)), "<div class='world", "class='info'")
        self.assertEqual(world.count("class='sp-body"), 2)
        self.assertIn("class='sp-eye'", world)

    def test_R12_hero_picker_sprites_are_animated_too(self):
        picker = between(render_title(), "class='picker'", "</form>")
        self.assertEqual(picker.count("class='sp-body"), len(HEROES))


if __name__ == "__main__":
    unittest.main()
