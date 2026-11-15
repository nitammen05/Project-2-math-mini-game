"""Round 4 tests for the battle page: scenes (R8), moving on (R9), defeat (R10)."""
import http.client
import re
import threading
import unittest

from game import Game, OPPONENTS
from scenes import scene_css
from web import STYLE, make_server, render_game
from tests.test_web import PROBLEMS, between


def win_first_battle(g):
    """Answer correctly until the first opponent is defeated."""
    while g.stage == 0:
        g.answer(str(g.current_problem.answer))
    return g


def lose(g):
    while g.status == "playing":
        g.answer("wrong")
    return g


def reduced_motion_css():
    return STYLE[STYLE.index("prefers-reduced-motion"):]


class TestSceneOnThePage(unittest.TestCase):
    """R8: the battle is fought in front of the opponent's scene."""

    def test_R8_stage_and_floor_sit_inside_the_opponents_scene(self):
        html = render_game(Game(PROBLEMS))
        world = between(html, "<div class='world", "class='question'")
        self.assertIn("<div class='world scene-swamp'>", html)
        self.assertIn("class='stage'", world)
        self.assertIn("class='floor'", world)

    def test_R8_scene_comes_after_the_health_bars(self):
        html = render_game(Game(PROBLEMS))
        self.assertLess(html.index("class='hud'"), html.index("class='world"))

    def test_R8_scene_changes_with_the_opponent(self):
        g = win_first_battle(Game(PROBLEMS))
        g.answer("wrong")    # a plain turn against the new opponent
        html = render_game(g)
        self.assertIn("<div class='world scene-camp'>", html)   # PROBLEMS skips to the Orc
        self.assertNotIn("scene-swamp'", html)

    def test_R8_every_opponent_scene_is_shown_in_its_battle(self):
        problems = {o.category: [p] for o, p in zip(
            OPPONENTS, [__import__("problems").Problem(o.category, "1 + 1", 2)
                        for o in OPPONENTS])}
        g = Game(problems)
        seen = []
        while g.status == "playing":
            seen.append(re.search(r"class='world scene-(\w+)", render_game(g)).group(1))
            g.answer("2")
        self.assertEqual(sorted(set(seen)), sorted(o.scene for o in OPPONENTS))

    def test_R8_page_style_paints_every_scene(self):
        self.assertIn(scene_css(), STYLE)

    def test_R8_scenery_is_not_a_picture_element(self):
        # Only the two fighters are <svg> elements in the scene; scenes live in the CSS.
        # (Look only inside the world: the game-over page also has a hero picker.)
        for g in (Game(PROBLEMS), win_first_battle(Game(PROBLEMS)), lose(Game(PROBLEMS))):
            world = between(render_game(g), "<div class='world", "class='info'")
            self.assertEqual(world.count("<svg"), 2)


class TestMovingOn(unittest.TestCase):
    """R9: after a knockout, the hero walks into the next opponent's scene."""

    def test_R9_knockout_moves_the_hero_into_the_new_scene(self):
        html = render_game(win_first_battle(Game(PROBLEMS)))
        self.assertIn("<div class='world scene-camp advance'>", html)
        # The old scene is drawn on top, ready to slide away.
        self.assertIn("<div class='backdrop scene-swamp' aria-hidden='true'>"
                      "<div class='sky'></div><div class='ground'></div></div>", html)

    def test_R9_old_scene_is_behind_the_fighters_in_the_page(self):
        html = render_game(win_first_battle(Game(PROBLEMS)))
        self.assertLess(html.index("class='backdrop"), html.index("class='stage'"))

    def test_R9_round_3_animation_classes_are_unchanged(self):
        html = render_game(win_first_battle(Game(PROBLEMS)))
        self.assertIn("class='fighter hero attack'", html)
        self.assertIn("class='fighter foe enter'", html)

    def test_R9_no_move_before_any_answer_or_on_an_ordinary_hit(self):
        # Check the world's class, not the whole page: the <style> mentions `advance`.
        g = Game(PROBLEMS)
        self.assertIn("<div class='world scene-swamp'>", render_game(g))
        g.answer("2")
        html = render_game(g)
        self.assertIn("<div class='world scene-swamp'>", html)
        self.assertNotIn("class='backdrop", html)

    def test_R9_move_happens_only_once(self):
        g = win_first_battle(Game(PROBLEMS))
        g.answer("9")    # the next turn, against the Orc
        html = render_game(g)
        self.assertIn("<div class='world scene-camp'>", html)
        self.assertNotIn("class='backdrop", html)

    def test_R9_no_move_after_the_last_opponent(self):
        g = Game(PROBLEMS)
        while g.status == "playing":
            g.answer(str(g.current_problem.answer))
        html = render_game(g)
        self.assertIn("<div class='world scene-camp'>", html)
        self.assertNotIn("class='backdrop", html)

    def test_R9_style_walks_the_hero_out_and_back_in(self):
        for name in ("walk-out", "walk-in", "pan-away"):
            self.assertIn(f"@keyframes {name} ", STYLE, name)
        self.assertRegex(STYLE, r"\.advance \.hero > \.sprite \{ animation: walk-out [^;]*"
                                r"walk-in [^;]*;")
        self.assertRegex(STYLE, r"\.advance > \.backdrop \{ animation: pan-away ")

    def test_R9_walk_starts_after_the_hit_and_ends_after_the_old_scene_leaves(self):
        walk = re.search(r"walk-out ([\d.]+)s ([\d.]+)s[^,]*, walk-in ([\d.]+)s ([\d.]+)s",
                         STYLE).groups()
        out_len, out_delay, in_len, in_delay = map(float, walk)
        pan_len, pan_delay = map(float, re.search(r"pan-away ([\d.]+)s ([\d.]+)s",
                                                  STYLE).groups())
        self.assertGreaterEqual(out_delay, 0.5)                      # the lunge is over
        self.assertGreaterEqual(in_delay, out_delay + out_len - 0.1)  # left before re-entering
        self.assertGreaterEqual(in_delay + in_len, pan_delay + pan_len)

    def test_R9_reduced_motion_just_shows_the_new_scene(self):
        self.assertIn(".backdrop { display: none", reduced_motion_css())


class TestDefeat(unittest.TestCase):
    """R10: at 0 HP the hero sinks into the ground and the scene becomes dirt and bones."""

    def test_R10_defeat_shows_dirt_and_bones_and_the_old_scene_fading(self):
        html = render_game(lose(Game(PROBLEMS)))
        self.assertIn("<div class='world scene-graveyard perish'>", html)
        self.assertIn("<div class='backdrop scene-swamp' aria-hidden='true'>", html)

    def test_R10_defeat_after_moving_on_fades_the_current_opponents_scene(self):
        g = lose(win_first_battle(Game(PROBLEMS)))
        self.assertIn("<div class='backdrop scene-camp'", render_game(g))

    def test_R10_round_3_knockout_classes_are_unchanged(self):
        html = render_game(lose(Game(PROBLEMS)))
        self.assertIn("class='fighter hero hurt ko'", html)
        self.assertIn("class='fighter foe attack'", html)

    def test_R10_hero_falls_then_sinks(self):
        self.assertIn("@keyframes sink ", STYLE)
        rule = re.search(r"\.hero\.hurt\.ko \{ animation: ([^;]+);", STYLE).group(1)
        self.assertIn("fall-left", rule)
        self.assertIn("sink", rule)
        self.assertLess(rule.index("fall-left"), rule.index("sink"))

    def test_R10_sinking_hero_is_hidden_by_the_ground(self):
        stage = re.search(r"\.stage \{([^}]*)\}", STYLE).group(1)
        self.assertIn("overflow: hidden", stage)

    def test_R10_old_scene_fades_into_dirt_and_bones(self):
        self.assertIn("@keyframes fade-away ", STYLE)
        self.assertRegex(STYLE, r"\.perish > \.backdrop \{ animation: fade-away ")

    def test_R10_reduced_motion_shows_the_defeated_hero_faded(self):
        self.assertRegex(reduced_motion_css(), r"\.perish \.hero \{ opacity: 0\.\d+")

    def test_R10_winning_never_shows_the_graveyard(self):
        g = Game(PROBLEMS)
        while g.status == "playing":
            g.answer(str(g.current_problem.answer))
        self.assertNotIn("class='world scene-graveyard", render_game(g))


class TestRound4Server(unittest.TestCase):
    def test_R10_losing_over_the_server_shows_dirt_and_bones(self):
        server = make_server(PROBLEMS, port=0)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        conn = http.client.HTTPConnection("127.0.0.1", server.server_address[1])
        conn.request("POST", "/start", body="")
        resp = conn.getresponse(); resp.read()
        cookie = resp.getheader("Set-Cookie").split(";")[0]
        headers = {"Cookie": cookie, "Content-Type": "application/x-www-form-urlencoded"}
        for _ in range(10):
            conn.request("POST", "/answer", body="answer=wrong", headers=headers)
            conn.getresponse().read()
        conn.request("GET", "/", headers={"Cookie": cookie})
        text = conn.getresponse().read().decode()
        conn.close()
        self.assertIn("Game over", text)
        self.assertIn("scene-graveyard perish", text)


if __name__ == "__main__":
    unittest.main()
