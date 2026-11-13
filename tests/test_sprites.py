"""Tests for sprites.py (Round 2: R2, R3, R4)."""
import unittest

from game import OPPONENTS
from sprites import (DEFAULT_HERO, HEROES, MONSTERS, hero_or_default,
                     render_hero, render_monster)


class TestHeroSprites(unittest.TestCase):
    def test_R3_there_are_several_heroes_to_choose_from(self):
        self.assertGreaterEqual(len(HEROES), 3)
        self.assertIn(DEFAULT_HERO, HEROES)

    def test_R3_every_hero_has_a_name_and_a_distinct_picture(self):
        pictures = [hero.svg for hero in HEROES.values()]
        self.assertEqual(len(set(pictures)), len(pictures))
        for key, hero in HEROES.items():
            self.assertTrue(hero.name)
            self.assertTrue(hero.svg.strip())
            self.assertIn(hero.svg, render_hero(key))

    def test_R3_hero_or_default_keeps_valid_choices(self):
        for key in HEROES:
            self.assertEqual(hero_or_default(key), key)

    def test_R3_hero_or_default_rejects_unknown_or_missing(self):
        for bad in (None, "", "dragon", "<script>", "KNIGHT "):
            self.assertEqual(hero_or_default(bad), DEFAULT_HERO)

    def test_R2_render_hero_is_an_accessible_svg(self):
        html = render_hero(DEFAULT_HERO)
        self.assertTrue(html.startswith("<svg"))
        self.assertIn("role='img'", html)
        self.assertIn(f"aria-label='{HEROES[DEFAULT_HERO].name}'", html)

    def test_R2_render_hero_falls_back_for_unknown_key(self):
        self.assertEqual(render_hero("nobody"), render_hero(DEFAULT_HERO))


class TestMonsterSprites(unittest.TestCase):
    def test_R4_every_opponent_has_a_sprite(self):
        for opponent in OPPONENTS:
            self.assertIn(opponent.sprite, MONSTERS, opponent.name)

    def test_R4_sprite_matches_opponent_name(self):
        # "Slime of Sums" must use the slime sprite, "Dragon of Powers" the dragon, ...
        for opponent in OPPONENTS:
            self.assertEqual(opponent.sprite, opponent.name.split()[0].lower())

    def test_R4_each_opponent_looks_different(self):
        sprites = [o.sprite for o in OPPONENTS]
        self.assertEqual(len(set(sprites)), len(sprites))
        pictures = [MONSTERS[s].svg for s in sprites]
        self.assertEqual(len(set(pictures)), len(pictures))

    def test_R2_R4_render_monster_labels_it_with_the_opponent_name(self):
        html = render_monster(OPPONENTS[0])
        self.assertTrue(html.startswith("<svg"))
        self.assertIn("aria-label='Slime of Sums'", html)

    def test_R2_render_monster_handles_opponent_without_sprite(self):
        from game import Opponent
        html = render_monster(Opponent("Mystery Foe", "addition", 1, 1))
        self.assertTrue(html.startswith("<svg"))
        self.assertIn("aria-label='Mystery Foe'", html)


if __name__ == "__main__":
    unittest.main()
