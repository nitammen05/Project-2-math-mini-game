"""The turn-based battle rules for Math Quest.

No web code lives here, so the rules can be tested on their own.
"""

from dataclasses import dataclass
import random

from problems import check_answer


@dataclass(frozen=True)
class Opponent:
    name: str
    category: str   # which kind of math problem this opponent asks
    max_hp: int     # how many hits it takes to defeat
    attack: int     # damage dealt to the player on a wrong answer


# Ordered from weakest to strongest: harder math = tougher opponent.
OPPONENTS = [
    Opponent("Slime of Sums", "addition", max_hp=3, attack=1),
    Opponent("Goblin of Minus", "subtraction", max_hp=4, attack=2),
    Opponent("Orc of Times", "multiplication", max_hp=5, attack=2),
    Opponent("Troll of Division", "division", max_hp=6, attack=3),
    Opponent("Dragon of Powers", "exponents", max_hp=7, attack=4),
]

PLAYER_MAX_HP = 10
NORMAL_DAMAGE = 1
CRIT_DAMAGE = 2
CRIT_STREAK = 3        # every 3rd correct answer in a row is a critical hit
HEAL_ON_VICTORY = 3
POINTS_PER_HIT = 10


class Game:
    def __init__(self, problems_by_category, rng=None, opponents=OPPONENTS):
        self.rng = rng or random.Random()
        self.problems = problems_by_category
        # Skip any opponent whose category has no problems in the file.
        self.opponents = [o for o in opponents if self.problems.get(o.category)]
        if not self.opponents:
            raise ValueError("No problems found for any opponent.")
        self.player_hp = PLAYER_MAX_HP
        self.score = 0
        self.streak = 0
        self.stage = 0
        self.opponent_hp = self.opponent.max_hp
        self.status = "playing"          # "playing", "won", or "lost"
        self.message = f"A wild {self.opponent.name} appears!"
        self._unused = {}                # problems not yet shown, per category
        self.current_problem = self._next_problem()

    @property
    def opponent(self):
        return self.opponents[self.stage]

    def _next_problem(self):
        """Pick a problem for the current opponent, not repeating until all are used."""
        category = self.opponent.category
        if not self._unused.get(category):
            pool = list(self.problems[category])
            self.rng.shuffle(pool)
            self._unused[category] = pool
        return self._unused[category].pop()

    def answer(self, user_input):
        """Play one turn. Returns True if the answer was correct."""
        if self.status != "playing":
            return False
        problem = self.current_problem
        correct = check_answer(problem, user_input)
        if correct:
            self._player_hits()
        else:
            self._opponent_hits(problem)
        if self.status == "playing":
            self.current_problem = self._next_problem()
        return correct

    def _player_hits(self):
        self.streak += 1
        crit = self.streak % CRIT_STREAK == 0
        damage = CRIT_DAMAGE if crit else NORMAL_DAMAGE
        self.opponent_hp = max(0, self.opponent_hp - damage)
        self.score += POINTS_PER_HIT * damage
        self.message = ("CRITICAL HIT! " if crit else "Correct! ") + \
            f"You deal {damage} damage to the {self.opponent.name}."
        if self.opponent_hp == 0:
            self._opponent_defeated()

    def _opponent_hits(self, problem):
        self.streak = 0
        self.player_hp = max(0, self.player_hp - self.opponent.attack)
        self.message = (f"Wrong! {problem.question} = {problem.answer}. "
                        f"The {self.opponent.name} hits you for {self.opponent.attack} damage.")
        if self.player_hp == 0:
            self.status = "lost"
            self.message += " You have been defeated..."

    def _opponent_defeated(self):
        defeated = self.opponent.name
        self.score += 50 * (self.stage + 1)
        if self.stage == len(self.opponents) - 1:
            self.status = "won"
            self.message += f" You defeated the {defeated} and conquered every foe!"
            return
        self.stage += 1
        self.opponent_hp = self.opponent.max_hp
        self.player_hp = min(PLAYER_MAX_HP, self.player_hp + HEAL_ON_VICTORY)
        self.message += (f" You defeated the {defeated}! You rest and recover {HEAL_ON_VICTORY} HP. "
                         f"A {self.opponent.name} appears!")
