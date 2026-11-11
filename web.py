"""The website for Math Quest, using only Python's standard library.

Pages:
    GET  /         show the title screen or the current battle
    POST /start    begin a new game
    POST /answer   submit an answer to the current problem
"""

from html import escape
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs
import secrets

from game import Game, PLAYER_MAX_HP

STYLE = """
body { font-family: system-ui, sans-serif; background: #1d1b2f; color: #f2f0ff;
       max-width: 640px; margin: 0 auto; padding: 16px; }
h1 { text-align: center; color: #ffd166; }
.card { background: #2b2945; border-radius: 12px; padding: 16px; margin: 12px 0; }
.bar { background: #444; border-radius: 6px; height: 18px; overflow: hidden; }
.fill { height: 100%; }
.hero .fill { background: #06d6a0; }
.foe .fill { background: #ef476f; }
.question { font-size: 2.4em; text-align: center; margin: 12px 0; }
.message { font-style: italic; color: #ffd166; }
input[type=text] { font-size: 1.4em; width: 8em; padding: 6px; }
button { font-size: 1.2em; padding: 8px 18px; border: 0; border-radius: 8px;
         background: #ffd166; color: #1d1b2f; cursor: pointer; }
form { text-align: center; }
"""


def page(body):
    return ("<!doctype html><html><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width, initial-scale=1'>"
            f"<title>Math Quest</title><style>{STYLE}</style></head>"
            f"<body><h1>Math Quest</h1>{body}</body></html>")


def hp_bar(label, hp, max_hp, css_class):
    percent = round(100 * hp / max_hp)
    return (f"<div class='card {css_class}'><b>{escape(label)}</b> — HP {hp}/{max_hp}"
            f"<div class='bar'><div class='fill' style='width:{percent}%'></div></div></div>")


def start_button(text):
    return f"<form method='post' action='/start'><button>{text}</button></form>"


def render_title():
    return page("<div class='card'><p>Defeat five monsters by answering math problems. "
                "Each monster is tougher than the last: Addition, Subtraction, "
                "Multiplication, Division, and finally Exponents.</p>"
                "<p>Correct answers hit the monster. Wrong answers let it hit you. "
                "Three right in a row lands a critical hit!</p></div>"
                + start_button("Begin your quest"))


def render_game(game):
    opp = game.opponent
    parts = [
        f"<p>Battle {game.stage + 1} of {len(game.opponents)} · Score {game.score}"
        f" · Streak {game.streak}</p>",
        hp_bar(opp.name, game.opponent_hp, opp.max_hp, "foe"),
        hp_bar("You", game.player_hp, PLAYER_MAX_HP, "hero"),
        f"<p class='message'>{escape(game.message)}</p>",
    ]
    if game.status == "playing":
        parts.append(
            f"<div class='card'><div class='question'>{escape(game.current_problem.question)} = ?</div>"
            "<form method='post' action='/answer'>"
            "<input type='text' name='answer' inputmode='numeric' autocomplete='off' autofocus> "
            "<button>Attack!</button></form></div>")
    elif game.status == "won":
        parts.append(f"<div class='card'><h2>Victory! Final score: {game.score}</h2></div>"
                     + start_button("Play again"))
    else:
        parts.append(f"<div class='card'><h2>Game over. Final score: {game.score}</h2></div>"
                     + start_button("Try again"))
    return page("".join(parts))


def make_handler(problems_by_category):
    """Build a request-handler class that shares one set of problems and games."""
    games = {}  # session id -> Game

    class Handler(BaseHTTPRequestHandler):
        def _session_id(self):
            cookie = SimpleCookie(self.headers.get("Cookie", ""))
            return cookie["session"].value if "session" in cookie else None

        def _send_html(self, html):
            data = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _redirect_home(self, session_id=None):
            # Redirect after a POST so refreshing the page doesn't resubmit an answer.
            self.send_response(303)
            self.send_header("Location", "/")
            if session_id:
                self.send_header("Set-Cookie", f"session={session_id}; Path=/; HttpOnly")
            self.end_headers()

        def do_GET(self):
            if self.path != "/":
                self.send_error(404)
                return
            game = games.get(self._session_id())
            self._send_html(render_game(game) if game else render_title())

        def do_POST(self):
            length = int(self.headers.get("Content-Length", 0))
            form = parse_qs(self.rfile.read(length).decode("utf-8"))
            if self.path == "/start":
                session_id = self._session_id() or secrets.token_hex(16)
                games[session_id] = Game(problems_by_category)
                self._redirect_home(session_id)
            elif self.path == "/answer":
                game = games.get(self._session_id())
                if game:
                    game.answer(form.get("answer", [""])[0])
                self._redirect_home()
            else:
                self.send_error(404)

        def log_message(self, format, *args):
            pass  # keep the terminal quiet

    Handler.games = games
    return Handler


def make_server(problems_by_category, host="127.0.0.1", port=8000):
    return ThreadingHTTPServer((host, port), make_handler(problems_by_category))
