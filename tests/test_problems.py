import os
import random
import tempfile
import unittest

from problems import Problem, check_answer, load_problems, parse_line, pick_problem

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestParseLine(unittest.TestCase):
    def test_valid_line(self):
        self.assertEqual(parse_line("addition | 2 + 3 | 5"), Problem("addition", "2 + 3", 5))

    def test_category_is_lowercased_and_spaces_trimmed(self):
        self.assertEqual(parse_line("  Division|10 / 2|  5  \n"), Problem("division", "10 / 2", 5))

    def test_blank_and_comment_lines_are_skipped(self):
        self.assertIsNone(parse_line(""))
        self.assertIsNone(parse_line("   \n"))
        self.assertIsNone(parse_line("# a comment"))

    def test_malformed_lines_raise(self):
        for bad in ["addition | 2 + 3", "addition | 2 + 3 | five", "a | b | 1 | 2", " | 1 + 1 | 2"]:
            with self.assertRaises(ValueError, msg=bad):
                parse_line(bad)


class TestLoadProblems(unittest.TestCase):
    def write_temp(self, text):
        f = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False)
        f.write(text)
        f.close()
        self.addCleanup(os.remove, f.name)
        return f.name

    def test_groups_by_category(self):
        path = self.write_temp("# header\naddition | 1 + 1 | 2\n\nmultiplication | 2 x 3 | 6\naddition | 2 + 2 | 4\n")
        result = load_problems(path)
        self.assertEqual(len(result["addition"]), 2)
        self.assertEqual(result["multiplication"], [Problem("multiplication", "2 x 3", 6)])

    def test_error_reports_line_number(self):
        path = self.write_temp("addition | 1 + 1 | 2\nbroken line\n")
        with self.assertRaisesRegex(ValueError, "line 2"):
            load_problems(path)

    def test_real_problems_file_has_every_answer_correct(self):
        """Double-check the shipped file: evaluate each question and compare."""
        problems = load_problems(os.path.join(PROJECT_DIR, "problems.txt"))
        self.assertEqual(set(problems), {"addition", "subtraction", "multiplication", "division", "exponents"})
        for plist in problems.values():
            for p in plist:
                expr = p.question.replace("x", "*").replace("^", "**").replace("/", "//")
                self.assertEqual(eval(expr), p.answer, p)


class TestCheckAnswer(unittest.TestCase):
    problem = Problem("addition", "2 + 3", 5)

    def test_correct(self):
        self.assertTrue(check_answer(self.problem, "5"))
        self.assertTrue(check_answer(self.problem, "  5 "))

    def test_wrong_or_garbage(self):
        for guess in ["6", "", "five", "5.5"]:
            self.assertFalse(check_answer(self.problem, guess), guess)


class TestPickProblem(unittest.TestCase):
    def test_picks_from_list(self):
        plist = [Problem("a", "1 + 1", 2), Problem("a", "1 + 2", 3)]
        self.assertIn(pick_problem(plist, random.Random(1)), plist)


if __name__ == "__main__":
    unittest.main()
