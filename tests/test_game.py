import random
import unittest

import game
from game import Game, Opponent, OPPONENTS, PLAYER_MAX_HP
from problems import Problem


def make_problems():
    """Two problems per category so we can test no-repeat behaviour."""
    return {o.category: [Problem(o.category, f"{o.category} q{i}", i) for i in (1, 2)]
            for o in OPPONENTS}


def right(g):
    return str(g.current_problem.answer)


class TestSetup(unittest.TestCase):
    def test_opponents_get_harder(self):
        hps = [o.max_hp for o in OPPONENTS]
        attacks = [o.attack for o in OPPONENTS]
        self.assertEqual(hps, sorted(hps))
        self.assertEqual(attacks, sorted(attacks))
        self.assertEqual(OPPONENTS[0].category, "addition")
        self.assertEqual(OPPONENTS[2].category, "multiplication")

    def test_new_game_state(self):
        g = Game(make_problems(), random.Random(0))
        self.assertEqual(g.player_hp, PLAYER_MAX_HP)
        self.assertEqual(g.opponent, OPPONENTS[0])
        self.assertEqual(g.opponent_hp, OPPONENTS[0].max_hp)
        self.assertEqual(g.status, "playing")
        self.assertEqual(g.current_problem.category, "addition")

    def test_skips_opponents_without_problems(self):
        problems = make_problems()
        del problems["subtraction"]
        g = Game(problems, random.Random(0))
        self.assertNotIn("subtraction", [o.category for o in g.opponents])

    def test_no_problems_at_all_raises(self):
        with self.assertRaises(ValueError):
            Game({}, random.Random(0))


class TestTurns(unittest.TestCase):
    def setUp(self):
        self.g = Game(make_problems(), random.Random(0))

    def test_correct_answer_damages_opponent(self):
        self.assertTrue(self.g.answer(right(self.g)))
        self.assertEqual(self.g.opponent_hp, OPPONENTS[0].max_hp - 1)
        self.assertEqual(self.g.score, 10)
        self.assertEqual(self.g.player_hp, PLAYER_MAX_HP)

    def test_wrong_answer_damages_player_and_shows_answer(self):
        problem = self.g.current_problem
        self.assertFalse(self.g.answer("-999"))
        self.assertEqual(self.g.player_hp, PLAYER_MAX_HP - OPPONENTS[0].attack)
        self.assertIn(str(problem.answer), self.g.message)
        self.assertEqual(self.g.streak, 0)

    def test_problems_do_not_repeat_until_all_used(self):
        first = self.g.current_problem
        self.g.answer("-999")
        self.assertNotEqual(self.g.current_problem, first)

    def test_third_correct_in_a_row_is_critical(self):
        opp = Opponent("Big", "addition", max_hp=10, attack=1)
        g = Game(make_problems(), random.Random(0), opponents=[opp])
        for _ in range(3):
            g.answer(right(g))
        self.assertEqual(g.opponent_hp, 10 - 1 - 1 - 2)
        self.assertIn("CRITICAL", g.message)

    def test_defeating_opponent_advances_and_heals(self):
        self.g.player_hp = 5
        while self.g.stage == 0:
            self.g.answer(right(self.g))
        self.assertEqual(self.g.opponent, OPPONENTS[1])
        self.assertEqual(self.g.opponent_hp, OPPONENTS[1].max_hp)
        self.assertEqual(self.g.player_hp, 5 + game.HEAL_ON_VICTORY)
        self.assertEqual(self.g.current_problem.category, "subtraction")

    def test_heal_never_exceeds_max(self):
        while self.g.stage == 0:
            self.g.answer(right(self.g))
        self.assertEqual(self.g.player_hp, PLAYER_MAX_HP)

    def test_losing(self):
        while self.g.status == "playing":
            self.g.answer("-999")
        self.assertEqual(self.g.status, "lost")
        self.assertEqual(self.g.player_hp, 0)
        self.assertFalse(self.g.answer(right(self.g)), "no turns after game over")

    def test_winning_whole_game(self):
        turns = 0
        while self.g.status == "playing":
            self.g.answer(right(self.g))
            turns += 1
        self.assertEqual(self.g.status, "won")
        self.assertEqual(self.g.stage, len(OPPONENTS) - 1)
        self.assertLess(turns, 40)


class TestHeroChoice(unittest.TestCase):
    """Round 2: the player's chosen sprite is stored on the game."""

    def test_R3_default_hero_when_none_chosen(self):
        from sprites import DEFAULT_HERO
        self.assertEqual(Game(make_problems(), random.Random(0)).hero, DEFAULT_HERO)

    def test_R3_chosen_hero_is_kept(self):
        g = Game(make_problems(), random.Random(0), hero="wizard")
        self.assertEqual(g.hero, "wizard")

    def test_R3_unknown_hero_falls_back_to_default(self):
        from sprites import DEFAULT_HERO
        g = Game(make_problems(), random.Random(0), hero="<script>")
        self.assertEqual(g.hero, DEFAULT_HERO)

    def test_R3_hero_stays_the_same_across_battles(self):
        g = Game(make_problems(), random.Random(0), hero="ninja")
        while g.status == "playing":
            g.answer(right(g))
        self.assertEqual(g.status, "won")
        self.assertEqual(g.hero, "ninja")


class TestLastTurn(unittest.TestCase):
    """Round 3: the game remembers the last attack so the page can animate it (R7)."""

    def test_R7_no_attack_before_the_first_answer(self):
        self.assertIsNone(Game(make_problems(), random.Random(0)).last_turn)

    def test_R7_correct_answer_is_a_hero_attack(self):
        g = Game(make_problems(), random.Random(0))
        g.answer(right(g))
        t = g.last_turn
        self.assertEqual(t.attacker, "hero")
        self.assertEqual(t.damage, game.NORMAL_DAMAGE)
        self.assertFalse(t.crit)
        self.assertFalse(t.knockout)
        self.assertEqual(t.foe, OPPONENTS[0])

    def test_R7_wrong_answer_is_a_foe_attack(self):
        g = Game(make_problems(), random.Random(0))
        g.answer("wrong")
        t = g.last_turn
        self.assertEqual(t.attacker, "foe")
        self.assertEqual(t.damage, OPPONENTS[0].attack)
        self.assertFalse(t.crit)
        self.assertFalse(t.knockout)

    def test_R7_critical_hit_is_recorded(self):
        strong = [Opponent("Wall", "addition", max_hp=99, attack=1)]
        g = Game(make_problems(), random.Random(0), opponents=strong)
        for _ in range(game.CRIT_STREAK):
            g.answer(right(g))
        self.assertTrue(g.last_turn.crit)
        self.assertEqual(g.last_turn.damage, game.CRIT_DAMAGE)

    def test_R7_knockout_remembers_the_defeated_opponent(self):
        g = Game(make_problems(), random.Random(0))
        while g.stage == 0:
            g.answer(right(g))
        t = g.last_turn
        self.assertTrue(t.knockout)
        self.assertEqual(t.attacker, "hero")
        self.assertEqual(t.foe, OPPONENTS[0])     # the one that fell...
        self.assertEqual(g.opponent, OPPONENTS[1])  # ...not the one that arrives

    def test_R7_player_knockout_when_game_is_lost(self):
        g = Game(make_problems(), random.Random(0))
        while g.status == "playing":
            g.answer("wrong")
        self.assertEqual(g.last_turn.attacker, "foe")
        self.assertTrue(g.last_turn.knockout)

    def test_R7_answers_after_the_game_ends_do_not_change_last_turn(self):
        g = Game(make_problems(), random.Random(0))
        while g.status == "playing":
            g.answer("wrong")
        before = g.last_turn
        g.answer("1")
        self.assertIs(g.last_turn, before)


if __name__ == "__main__":
    unittest.main()
