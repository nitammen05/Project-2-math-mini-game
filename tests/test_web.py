"""Tests that start a real server on a free port and talk to it like a browser."""
import http.client
import threading
import unittest
from urllib.parse import urlencode

import main
from game import Game
from problems import Problem
from sprites import DEFAULT_HERO, HEROES, MONSTERS
from web import make_server, render_game, render_title

PROBLEMS = {"addition": [Problem("addition", "1 + 1", 2)],
            "multiplication": [Problem("multiplication", "<b>3 x 3</b>", 9)]}


class TestRendering(unittest.TestCase):
    def test_title_has_start_button(self):
        self.assertIn("action='/start'", render_title())

    def test_game_page_shows_question_and_hp(self):
        html = render_game(Game(PROBLEMS))
        self.assertIn("1 + 1 = ?", html)
        self.assertIn("HP 10/10", html)
        self.assertIn("Slime of Sums", html)

    def test_question_text_is_escaped(self):
        g = Game(PROBLEMS)
        while g.stage == 0:
            g.answer(str(g.current_problem.answer))
        html = render_game(g)
        self.assertIn("&lt;b&gt;3 x 3&lt;/b&gt;", html)
        self.assertNotIn("<b>3 x 3</b>", html)

    def test_end_screens(self):
        g = Game(PROBLEMS)
        while g.status == "playing":
            g.answer("wrong")
        self.assertIn("Game over", render_game(g))
        g = Game(PROBLEMS)
        while g.status == "playing":
            g.answer(str(g.current_problem.answer))
        self.assertIn("Victory", render_game(g))


class TestSpriteRendering(unittest.TestCase):
    """Round 2: sprites on the page (R2, R3, R4)."""

    def test_R3_title_offers_every_hero(self):
        html = render_title()
        for key, hero in HEROES.items():
            self.assertIn(f"name='hero' value='{key}'", html)
            self.assertIn(f"aria-label='{hero.name}'", html)

    def test_R3_default_hero_is_preselected_on_title(self):
        html = render_title()
        self.assertIn(f"value='{DEFAULT_HERO}' checked", html)
        self.assertEqual(html.count(" checked"), 1)

    def test_R2_battle_shows_hero_and_opponent_sprites(self):
        html = render_game(Game(PROBLEMS, hero="archer"))
        self.assertIn("aria-label='Archer'", html)
        self.assertIn("aria-label='Slime of Sums'", html)
        self.assertEqual(html.count("<svg"), 2)

    def test_R4_battle_sprite_changes_with_the_opponent(self):
        g = Game(PROBLEMS)
        self.assertIn(MONSTERS["slime"].svg, render_game(g))
        while g.stage == 0:
            g.answer(str(g.current_problem.answer))
        html = render_game(g)   # PROBLEMS skips to the Orc of Times
        self.assertIn(MONSTERS["orc"].svg, html)
        self.assertNotIn(MONSTERS["slime"].svg, html)

    def test_R3_end_screens_let_player_choose_again_with_current_hero_selected(self):
        g = Game(PROBLEMS, hero="ninja")
        while g.status == "playing":
            g.answer("wrong")
        html = render_game(g)
        self.assertIn("Try again", html)
        for key in HEROES:
            self.assertIn(f"name='hero' value='{key}'", html)
        self.assertIn("value='ninja' checked", html)


class TestServer(unittest.TestCase):
    def setUp(self):
        self.server = make_server(PROBLEMS, port=0)  # port 0 = pick any free port
        self.port = self.server.server_address[1]
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)

    def request(self, method, path, body=None, cookie=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.port)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        if cookie:
            headers["Cookie"] = cookie
        conn.request(method, path, body=urlencode(body or {}), headers=headers)
        resp = conn.getresponse()
        text = resp.read().decode()
        conn.close()
        return resp, text

    def test_home_without_cookie_shows_title(self):
        resp, text = self.request("GET", "/")
        self.assertEqual(resp.status, 200)
        self.assertIn("Begin your quest", text)

    def test_unknown_page_is_404(self):
        self.assertEqual(self.request("GET", "/nope")[0].status, 404)

    def test_full_flow(self):
        resp, _ = self.request("POST", "/start")
        self.assertEqual(resp.status, 303)
        cookie = resp.getheader("Set-Cookie").split(";")[0]
        _, text = self.request("GET", "/", cookie=cookie)
        self.assertIn("1 + 1 = ?", text)
        resp, _ = self.request("POST", "/answer", {"answer": "2"}, cookie=cookie)
        self.assertEqual(resp.status, 303)
        _, text = self.request("GET", "/", cookie=cookie)
        self.assertIn("Correct!", text)
        self.assertIn("HP 2/3", text)

    def test_two_players_have_separate_games(self):
        c1 = self.request("POST", "/start")[0].getheader("Set-Cookie").split(";")[0]
        c2 = self.request("POST", "/start")[0].getheader("Set-Cookie").split(";")[0]
        self.assertNotEqual(c1, c2)
        self.request("POST", "/answer", {"answer": "wrong"}, cookie=c1)
        self.assertIn("HP 9/10", self.request("GET", "/", cookie=c1)[1])
        self.assertIn("HP 10/10", self.request("GET", "/", cookie=c2)[1])

    def test_answer_without_game_just_redirects(self):
        self.assertEqual(self.request("POST", "/answer", {"answer": "2"})[0].status, 303)

    def test_R3_start_with_chosen_hero_shows_it(self):
        resp, _ = self.request("POST", "/start", {"hero": "wizard"})
        cookie = resp.getheader("Set-Cookie").split(";")[0]
        _, text = self.request("GET", "/", cookie=cookie)
        self.assertIn("aria-label='Wizard'", text)

    def test_R3_start_with_bad_hero_uses_default(self):
        resp, _ = self.request("POST", "/start", {"hero": "dragon"})
        cookie = resp.getheader("Set-Cookie").split(";")[0]
        _, text = self.request("GET", "/", cookie=cookie)
        self.assertIn(f"aria-label='{HEROES[DEFAULT_HERO].name}'", text)

    def test_R3_play_again_can_change_hero(self):
        resp, _ = self.request("POST", "/start", {"hero": "wizard"})
        cookie = resp.getheader("Set-Cookie").split(";")[0]
        self.request("POST", "/start", {"hero": "archer"}, cookie=cookie)
        _, text = self.request("GET", "/", cookie=cookie)
        self.assertIn("aria-label='Archer'", text)
        self.assertNotIn("aria-label='Wizard'", text)

class TestMain(unittest.TestCase):
    def test_parse_args_defaults(self):
        args = main.parse_args([])
        self.assertEqual(args.port, 8000)
        self.assertTrue(args.problems.endswith("problems.txt"))

    def test_missing_problems_file_returns_error(self):
        self.assertEqual(main.main(["--problems", "does-not-exist.txt", "--no-browser"]), 1)


if __name__ == "__main__":
    unittest.main()
