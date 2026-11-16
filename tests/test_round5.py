"""Round 5 tests: detailed sprites (R11), detailed and idle animations (R12),
hero names (R13), and the defeat screen (R14)."""
import unittest

from game import Game
from sprites import HEROES, render_hero
from web import render_game, render_title
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


if __name__ == "__main__":
    unittest.main()
