"""Reading math problems from a text file and checking answers.

Each non-blank, non-comment line of the file looks like:
    category | question | answer
for example:
    multiplication | 7 x 8 | 56
"""

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class Problem:
    category: str
    question: str
    answer: int


def parse_line(line):
    """Turn one line of the file into a Problem.

    Returns None for blank lines and comments (lines starting with #).
    Raises ValueError if the line is malformed.
    """
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    parts = [part.strip() for part in line.split("|")]
    if len(parts) != 3 or not all(parts):
        raise ValueError(f"Expected 'category | question | answer', got: {line!r}")
    category, question, answer = parts
    return Problem(category.lower(), question, int(answer))


def load_problems(path):
    """Read a problems file and group the problems by category.

    Returns a dict like {"addition": [Problem, ...], ...}.
    """
    by_category = {}
    with open(path, encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            try:
                problem = parse_line(line)
            except ValueError as err:
                raise ValueError(f"{path}, line {line_number}: {err}") from err
            if problem is not None:
                by_category.setdefault(problem.category, []).append(problem)
    return by_category


def check_answer(problem, user_input):
    """Return True if the text the user typed matches the problem's answer."""
    try:
        return int(str(user_input).strip()) == problem.answer
    except ValueError:
        return False


def pick_problem(problems, rng=random):
    """Choose one problem at random from a list."""
    return rng.choice(problems)
