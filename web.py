"""The website for Math Quest, using only Python's standard library.

Pages:
    GET  /         show the title screen or the current battle
    POST /start    begin a new game (form field `hero` picks the player's sprite)
    POST /answer   submit an answer to the current problem
"""

from html import escape
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs
import secrets

from game import Game, PLAYER_MAX_HP
from sprites import DEFAULT_HERO, HEROES, render_hero, render_monster

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
.sprite { display: block; margin: 0 auto; }
/* Round 3: fighting-game screen. Health bars on top (R5)... */
.hud { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.hud .hp { flex: 1; margin: 0; padding: 8px 10px; }
.hud .foe { text-align: right; }
.hud .vs { font-weight: bold; font-size: 1.3em; color: #ffd166; }
.hud .hero .bar { display: flex; justify-content: flex-end; } /* bars drain outward */
/* ...then a stage with both fighters standing on one floor. */
.stage { position: relative; display: flex; justify-content: space-between;
         align-items: flex-end; padding: 24px 28px 0; border-radius: 12px 12px 0 0;
         background: linear-gradient(#3a2f6b, #2b2945 70%); overflow: hidden; }
.floor { height: 14px; border-radius: 0 0 12px 12px;
         background: repeating-linear-gradient(90deg, #7a5c3e 0 24px, #6b4f35 24px 48px); }
.fighter { position: relative; display: grid; }
.fighter > .sprite { grid-area: 1 / 1; }
.info { text-align: center; margin: 8px 0 0; }
.picker { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; margin: 8px 0 14px; }
.picker label { background: #2b2945; border: 3px solid transparent; border-radius: 12px;
                padding: 6px 10px; cursor: pointer; }
.picker label:has(input:checked) { border-color: #ffd166; }
.picker input { position: absolute; opacity: 0; }
.picker input:focus-visible + .sprite { outline: 2px dashed #ffd166; }
"""


FIGHTER_SIZE = 120   # pixels; how big the fighters are drawn on the stage


def page(body, heading=True):
    """A full HTML page. The battle screen leaves out the big heading so the
    health bars can sit at the very top (R5)."""
    title = "<h1>Math Quest</h1>" if heading else ""
    return ("<!doctype html><html><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width, initial-scale=1'>"
            f"<title>Math Quest</title><style>{STYLE}</style></head>"
            f"<body>{title}{body}</body></html>")


def hp_bar(label, hp, max_hp, css_class):
    percent = round(100 * hp / max_hp)
    return (f"<div class='card hp {css_class}'><b>{escape(label)}</b> — HP {hp}/{max_hp}"
            f"<div class='bar'><div class='fill' style='width:{percent}%'></div></div></div>")


def start_form(text, selected=DEFAULT_HERO):
    """The 'start a game' form, with a hero picker (R3). `selected` starts ticked."""
    choices = []
    for key, hero in HEROES.items():
        checked = " checked" if key == selected else ""
        choices.append(f"<label><input type='radio' name='hero' value='{key}'{checked}>"
                       f"{render_hero(key, size=72)}{escape(hero.name)}</label>")
    return ("<form method='post' action='/start'><p>Choose your hero:</p>"
            f"<div class='picker'>{''.join(choices)}</div><button>{text}</button></form>")


def render_title():
    return page("<div class='card'><p>Defeat five monsters by answering math problems. "
                "Each monster is tougher than the last: Addition, Subtraction, "
                "Multiplication, Division, and finally Exponents.</p>"
                "<p>Correct answers hit the monster. Wrong answers let it hit you. "
                "Three right in a row lands a critical hit!</p></div>"
                + start_form("Begin your quest"))


def render_game(game):
    opp = game.opponent
    parts = [
        # Health bars across the top: you on the left, the opponent on the right (R5).
        "<div class='hud'>",
        hp_bar("You", game.player_hp, PLAYER_MAX_HP, "hero"),
        "<div class='vs'>VS</div>",
        hp_bar(opp.name, game.opponent_hp, opp.max_hp, "foe"),
        "</div>",
        # The stage: both fighters on one floor, facing each other (R5, R6).
        "<div class='stage'>",
        f"<div class='fighter hero'>{render_hero(game.hero, FIGHTER_SIZE, 'right')}</div>",
        f"<div class='fighter foe'>{render_monster(opp, FIGHTER_SIZE, 'left')}</div>",
        "</div><div class='floor'></div>",
        f"<p class='info'>Battle {game.stage + 1} of {len(game.opponents)} · Score {game.score}"
        f" · Streak {game.streak}</p>",
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
                     + start_form("Play again", game.hero))
    else:
        parts.append(f"<div class='card'><h2>Game over. Final score: {game.score}</h2></div>"
                     + start_form("Try again", game.hero))
    return page("".join(parts), heading=False)


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
                games[session_id] = Game(problems_by_category, hero=form.get("hero", [None])[0])
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
