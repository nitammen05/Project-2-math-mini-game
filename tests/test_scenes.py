"""Tests for the background scenes (Round 4: R8, R10)."""
import unittest

from game import OPPONENTS, Opponent
from scenes import (GRAVEYARD, PLAIN, SCENES, scene_css, scene_key, sky_url)


class TestOpponentScenes(unittest.TestCase):
    """R8: every opponent has its own scene that fits its name."""

    def test_R8_every_opponent_has_a_scene(self):
        for o in OPPONENTS:
            self.assertIn(o.scene, SCENES, o.name)

    def test_R8_every_opponent_has_a_different_scene(self):
        keys = [o.scene for o in OPPONENTS]
        self.assertEqual(len(keys), len(set(keys)))

    def test_R8_scene_name_matches_the_monster_in_the_opponent_name(self):
        expected = {"Slime of Sums": "Slime Swamp", "Goblin of Minus": "Goblin Cave",
                    "Orc of Times": "Orc War Camp", "Troll of Division": "Troll Bridge",
                    "Dragon of Powers": "Dragon's Volcano"}
        for o in OPPONENTS:
            self.assertEqual(SCENES[o.scene].name, expected[o.name])

    def test_R8_scene_shows_the_math_in_the_opponent_name(self):
        signs = {"Slime of Sums": "+", "Goblin of Minus": "−",
                 "Orc of Times": "×", "Troll of Division": "÷"}
        for o in OPPONENTS:
            if o.name in signs:
                self.assertIn(f">{signs[o.name]}<", SCENES[o.scene].svg, o.name)

    def test_R8_opponent_without_a_scene_gets_the_plain_one(self):
        self.assertEqual(scene_key(Opponent("Blob of Mystery", "addition", 1, 1)), PLAIN)
        self.assertEqual(scene_key(Opponent("Blob", "addition", 1, 1, scene="nope")), PLAIN)
        self.assertIn(PLAIN, SCENES)

    def test_R8_known_scene_key_is_kept(self):
        self.assertEqual(scene_key(OPPONENTS[0]), OPPONENTS[0].scene)


class TestSceneDrawing(unittest.TestCase):
    """R8: scenes are pictures put in the page's CSS, not extra <svg> elements."""

    def test_R8_sky_is_an_encoded_svg_data_url(self):
        for key, scene in SCENES.items():
            url = sky_url(scene)
            self.assertTrue(url.startswith('url("data:image/svg+xml,%3Csvg'), key)
            # Raw <, ", ' or # would end the url or confuse the HTML/CSS around it.
            for char in "<>\"'#":
                self.assertNotIn(char, url[len('url("'):-2], key)

    def test_R8_each_scene_has_a_sky_and_a_ground_rule(self):
        css = scene_css()
        for key in SCENES:
            self.assertIn(f".scene-{key} > .stage", css)
            self.assertIn(f".scene-{key} > .floor", css)
            # The leftover old scene during a scene change (R9, R10) uses the same picture.
            self.assertIn(f".scene-{key} > .sky", css)
            self.assertIn(f".scene-{key} > .ground", css)

    def test_R8_every_scene_draws_a_full_picture(self):
        for key, scene in SCENES.items():
            self.assertIn("<rect width='300' height='100'", scene.svg, key)


class TestGraveyard(unittest.TestCase):
    """R10: losing shows a scene of dirt and bones."""

    def test_R10_graveyard_is_dirt_and_bones(self):
        self.assertEqual(SCENES[GRAVEYARD].name, "Dirt and Bones")
        self.assertGreaterEqual(SCENES[GRAVEYARD].svg.count("class='bone'"), 5)
        self.assertGreaterEqual(SCENES[GRAVEYARD].svg.count("class='skull'"), 1)

    def test_R10_graveyard_is_not_an_opponent_scene(self):
        self.assertNotIn(GRAVEYARD, [o.scene for o in OPPONENTS])


if __name__ == "__main__":
    unittest.main()
