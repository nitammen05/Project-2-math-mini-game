"""Round 6 tests: sound made by Python (R15), music for each opponent (R16),
hero voice lines (R17), and attack and damage sounds (R18)."""
import ast
import http.client
import io
import re
import sys
import threading
import unittest
import wave

import sounds
from game import Game, Opponent, OPPONENTS
from sounds import (ATTACK_SOUNDS, MUSIC, SAMPLE_RATE, VOICES, make_sound,
                    music_key, music_length, sound_names)
from sprites import HEROES, MONSTERS
from web import make_server, render_game, render_title
from tests.test_web import PROBLEMS, between
from tests.test_web_round4 import lose, win_first_battle

MAX_EFFECT_SECONDS = 1.5


def read_wav(name):
    """(seconds, samples) of a sound, read back with Python's own wave module."""
    with wave.open(io.BytesIO(make_sound(name))) as w:
        frames = w.readframes(w.getnframes())
        samples = [int.from_bytes(frames[i:i + 2], "little", signed=True)
                   for i in range(0, len(frames), 2)]
        return w.getnframes() / w.getframerate(), samples


def sound_part(html):
    """The part of a page that holds the sounds (rule 15: look in the right place)."""
    return between(html, "<div class='sound'>", "</div>")


def played(html):
    """The names of the sounds a page plays, in order."""
    return re.findall(r"src='/sound/([\w-]+)\.wav", sound_part(html))


def right(g):
    g.answer(str(g.current_problem.answer))
    return g


def wrong(g):
    g.answer("wrong")
    return g


class TestSoundFiles(unittest.TestCase):
    """R15: every sound is a WAV file made by Python's standard library."""

    def test_R15_every_sound_is_a_valid_wav_file(self):
        for name in sound_names():
            with wave.open(io.BytesIO(make_sound(name))) as w:
                self.assertEqual(w.getnchannels(), 1, name)
                self.assertEqual(w.getsampwidth(), 2, name)
                self.assertEqual(w.getframerate(), SAMPLE_RATE, name)
                self.assertGreater(w.getnframes(), 0, name)

    def test_R15_no_sound_is_silent(self):
        for name in sound_names():
            _, samples = read_wav(name)
            self.assertGreater(max(map(abs, samples)), 1000, name)

    def test_R15_sounds_do_not_clip(self):
        for name in sound_names():
            _, samples = read_wav(name)
            self.assertLessEqual(max(map(abs, samples)), 32767, name)

    def test_R15_unknown_sound_name_gives_nothing(self):
        for name in ["nope", "music-nope", "voice-dragon", "../web", ""]:
            self.assertIsNone(make_sound(name), name)

    def test_R15_sounds_use_only_the_standard_library(self):
        with open(sounds.__file__, encoding="utf-8") as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module]
            else:
                continue
            for name in names:
                self.assertIn(name.split(".")[0], sys.stdlib_module_names, name)

    def test_R15_no_sound_files_are_stored_in_the_project(self):
        import os
        here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        for root, _, files in os.walk(here):
            if ".git" in root:
                continue
            for f in files:
                self.assertFalse(f.endswith((".wav", ".mp3", ".ogg")), f)


class TestSoundOnPages(unittest.TestCase):
    """R15: pages play sounds with plain HTML <audio> tags and no JavaScript."""

    def pages(self):
        return {"title": render_title(),
                "battle": render_game(Game(PROBLEMS)),
                "after hit": render_game(right(Game(PROBLEMS))),
                "won": render_game(right(right(win_first_battle(Game(PROBLEMS))))),
                "lost": render_game(lose(Game(PROBLEMS)))}

    def test_R15_no_page_has_javascript(self):
        for label, html in self.pages().items():
            self.assertNotIn("<script", html, label)
            self.assertIsNone(re.search(r"\son\w+=", html), label)
            self.assertNotIn("javascript:", html, label)

    def test_R15_every_sound_a_page_plays_exists(self):
        for label, html in self.pages().items():
            if label == "title":
                continue
            for name in played(html):
                self.assertIn(name, sound_names(), label)

    def test_R15_sounds_are_audio_tags_that_start_themselves(self):
        tags = re.findall(r"<audio[^>]*>", sound_part(render_game(right(Game(PROBLEMS)))))
        self.assertGreater(len(tags), 1)
        for tag in tags:
            self.assertIn(" autoplay", tag)

    def test_R15_battle_music_has_a_visible_player(self):
        music = re.findall(r"<audio[^>]*music-[^>]*>", sound_part(render_game(Game(PROBLEMS))))
        self.assertEqual(len(music), 1)
        self.assertIn(" controls", music[0])

    def test_R15_effects_have_no_visible_player(self):
        sound = sound_part(render_game(right(Game(PROBLEMS))))
        for tag in re.findall(r"<audio[^>]*>", sound):
            if "music-" not in tag:
                self.assertNotIn("controls", tag)

    def test_R15_sounds_come_after_the_battle_so_layout_is_kept(self):
        html = render_game(Game(PROBLEMS))
        self.assertIn("<body><div class='hud'>", html)   # Round 3 layout kept
        self.assertGreater(html.index("<div class='sound'>"), html.index("class='floor'"))


class TestSoundServer(unittest.TestCase):
    """R15 (served at /sound/<name>.wav) and R16 (music picks up where it was)."""

    def start(self, clock=None):
        self.server = make_server(PROBLEMS, port=0, clock=clock)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.conn = http.client.HTTPConnection("127.0.0.1", self.server.server_address[1])
        self.addCleanup(self.conn.close)

    def get(self, path, cookie=None):
        self.conn.request("GET", path, headers={"Cookie": cookie} if cookie else {})
        resp = self.conn.getresponse()
        return resp, resp.read()

    def post(self, path, body="", cookie=None):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        if cookie:
            headers["Cookie"] = cookie
        self.conn.request("POST", path, body=body, headers=headers)
        resp = self.conn.getresponse()
        resp.read()
        return resp

    def test_R15_server_sends_a_sound_as_wav(self):
        self.start()
        resp, data = self.get("/sound/hurt-hero.wav")
        self.assertEqual(resp.status, 200)
        self.assertEqual(resp.getheader("Content-Type"), "audio/wav")
        self.assertEqual(data, make_sound("hurt-hero"))

    def test_R15_server_says_404_for_an_unknown_sound(self):
        self.start()
        for path in ["/sound/nope.wav", "/sound/hurt-hero", "/sound/../web.py",
                     "/sound/hurt-hero.wav/x"]:
            self.assertEqual(self.get(path)[0].status, 404, path)

    def test_R16_server_can_send_part_of_a_sound_so_music_can_skip_ahead(self):
        # Browsers ask for a "range" of bytes to jump into the middle of music or loop it.
        self.start()
        self.conn.request("GET", "/sound/music-war-drums.wav", headers={"Range": "bytes=100-199"})
        resp = self.conn.getresponse()
        data = resp.read()
        whole = make_sound("music-war-drums")
        self.assertEqual(resp.status, 206)
        self.assertEqual(resp.getheader("Content-Range"), f"bytes 100-199/{len(whole)}")
        self.assertEqual(data, whole[100:200])

    def test_R16_open_ended_range_runs_to_the_end_and_bad_range_is_refused(self):
        self.start()
        whole = make_sound("crit")
        self.conn.request("GET", "/sound/crit.wav", headers={"Range": "bytes=40-"})
        resp = self.conn.getresponse()
        self.assertEqual((resp.status, resp.read()), (206, whole[40:]))
        self.conn.request("GET", "/sound/crit.wav", headers={"Range": f"bytes={len(whole)}-"})
        resp = self.conn.getresponse()
        resp.read()
        self.assertEqual(resp.status, 416)

    def test_R16_music_picks_up_where_it_was_across_pages(self):
        now = [100.0]
        self.start(clock=lambda: now[0])
        cookie = self.post("/start", "hero=knight").getheader("Set-Cookie").split(";")[0]
        first = self.get("/", cookie)[1].decode()
        self.assertIn("music-swamp-bounce.wav'", first)       # starts at the beginning
        now[0] += 4.25
        self.post("/answer", "answer=wrong", cookie)
        later = self.get("/", cookie)[1].decode()
        self.assertIn("music-swamp-bounce.wav#t=4.25'", later)

    def test_R16_a_new_game_starts_the_music_again(self):
        now = [100.0]
        self.start(clock=lambda: now[0])
        cookie = self.post("/start").getheader("Set-Cookie").split(";")[0]
        self.get("/", cookie)
        now[0] += 3
        self.post("/start", "", cookie)
        self.assertIn("music-swamp-bounce.wav'", self.get("/", cookie)[1].decode())


class TestOpponentMusic(unittest.TestCase):
    """R16: each opponent has its own looping music that fits its name."""

    TITLES = {"Slime of Sums": "Swamp Bounce", "Goblin of Minus": "Sneaky Cave",
              "Orc of Times": "War Drums", "Troll of Division": "Bridge Stomp",
              "Dragon of Powers": "Volcano Fury"}

    def test_R16_every_opponent_has_the_music_named_in_the_spec(self):
        self.assertEqual({o.name: MUSIC[music_key(o)].title for o in OPPONENTS}, self.TITLES)

    def test_R16_every_opponent_has_different_music(self):
        tunes = {make_sound(f"music-{music_key(o)}") for o in OPPONENTS}
        self.assertEqual(len(tunes), len(OPPONENTS))

    def test_R16_themes_differ_in_speed_or_sound(self):
        styles = {(MUSIC[music_key(o)].tempo, MUSIC[music_key(o)].wave) for o in OPPONENTS}
        self.assertEqual(len(styles), len(OPPONENTS))

    def test_R16_dragon_is_faster_than_slime_and_troll_is_slowest(self):
        tempo = {o.sprite: MUSIC[music_key(o)].tempo for o in OPPONENTS}
        self.assertGreater(tempo["dragon"], tempo["slime"])
        self.assertEqual(min(tempo, key=tempo.get), "troll")

    def test_R16_music_is_long_enough_to_loop_nicely(self):
        for key in MUSIC:
            seconds, _ = read_wav(f"music-{key}")
            self.assertGreaterEqual(seconds, 6, key)
            self.assertAlmostEqual(seconds, music_length(key), places=2)

    def test_R16_opponent_without_music_gets_the_default_tune(self):
        odd = Opponent("Mystery of Maths", "addition", 3, 1)
        self.assertEqual(music_key(odd), "default")
        html = render_game(Game(PROBLEMS, opponents=[odd]))
        self.assertIn("music-default.wav", sound_part(html))

    def test_R16_battle_page_loops_the_opponents_music(self):
        sound = sound_part(render_game(Game(PROBLEMS)))
        tag = re.search(r"<audio[^>]*music-[^>]*>", sound).group(0)
        self.assertIn("/sound/music-swamp-bounce.wav", tag)
        self.assertIn(" loop", tag)
        self.assertIn("Swamp Bounce", sound)

    def test_R16_music_continues_from_the_time_given(self):
        html = render_game(Game(PROBLEMS), music_at=3.5)
        self.assertIn("music-swamp-bounce.wav#t=3.50'", sound_part(html))

    def test_R16_music_time_wraps_around_the_loop(self):
        length = music_length("swamp-bounce")
        html = render_game(Game(PROBLEMS), music_at=length + 1)
        self.assertIn("music-swamp-bounce.wav#t=1.00'", sound_part(html))

    def test_R16_a_new_opponent_brings_its_own_music(self):
        g = win_first_battle(Game(PROBLEMS))
        self.assertEqual(g.opponent.name, "Orc of Times")
        sound = sound_part(render_game(g, music_at=0))
        self.assertIn("music-war-drums.wav'", sound)
        self.assertNotIn("swamp-bounce", sound)

    def test_R16_victory_plays_a_fanfare_once_instead_of_music(self):
        g = right(right(right(win_first_battle(Game(PROBLEMS)))))
        while g.status == "playing":
            right(g)
        names = played(render_game(g))
        self.assertIn("jingle-victory", names)
        self.assertFalse(any(n.startswith("music-") for n in names))
        self.assertNotIn(" loop", sound_part(render_game(g)))

    def test_R16_defeat_plays_a_sad_tune_once_instead_of_music(self):
        names = played(render_game(lose(Game(PROBLEMS))))
        self.assertIn("jingle-defeat", names)
        self.assertNotIn("jingle-victory", names)
        self.assertFalse(any(n.startswith("music-") for n in names))

    def test_R16_jingles_are_different(self):
        self.assertNotEqual(make_sound("jingle-victory"), make_sound("jingle-defeat"))


class TestHeroVoices(unittest.TestCase):
    """R17: each hero has its own short babble voice line."""

    def test_R17_every_hero_has_a_voice(self):
        self.assertEqual(set(VOICES), set(HEROES))

    def test_R17_every_voice_sounds_different(self):
        voices = {make_sound(f"voice-{k}") for k in HEROES}
        self.assertEqual(len(voices), len(HEROES))
        self.assertEqual(len({v.pitch for v in VOICES.values()}), len(HEROES))

    def test_R17_voice_lines_are_short(self):
        for key in HEROES:
            seconds, _ = read_wav(f"voice-{key}")
            self.assertLess(seconds, MAX_EFFECT_SECONDS, key)

    def test_R17_voice_is_babble_of_several_syllables(self):
        for key, voice in VOICES.items():
            self.assertGreaterEqual(len(voice.syllables), 3, key)

    def test_R17_starting_a_game_plays_the_chosen_heros_voice(self):
        for key in HEROES:
            self.assertIn(f"voice-{key}", played(render_game(Game(PROBLEMS, hero=key))), key)

    def test_R17_only_the_chosen_hero_speaks(self):
        names = played(render_game(Game(PROBLEMS, hero="wizard")))
        self.assertEqual([n for n in names if n.startswith("voice-")], ["voice-wizard"])

    def test_R17_voice_does_not_play_again_after_an_answer(self):
        for g in [right(Game(PROBLEMS)), wrong(Game(PROBLEMS))]:
            self.assertFalse(any(n.startswith("voice-") for n in played(render_game(g))))

    def test_R17_title_screen_plays_no_sound(self):
        self.assertNotIn("<audio", render_title())


class TestFightSounds(unittest.TestCase):
    """R18: every attack and every hit has a sound."""

    def test_R18_every_fighter_has_its_own_attack_sound(self):
        self.assertEqual(set(ATTACK_SOUNDS), set(HEROES) | set(MONSTERS))
        sounds_made = {make_sound(f"attack-{k}") for k in ATTACK_SOUNDS}
        self.assertEqual(len(sounds_made), len(ATTACK_SOUNDS))

    def test_R18_effects_are_short(self):
        names = [n for n in sound_names()
                 if n.split("-")[0] in ("attack", "hurt", "crit", "knockout")]
        self.assertGreaterEqual(len(names), len(ATTACK_SOUNDS) + 4)
        for name in names:
            seconds, _ = read_wav(name)
            self.assertLess(seconds, MAX_EFFECT_SECONDS, name)

    def test_R18_attack_sound_starts_at_once(self):
        _, samples = read_wav("attack-knight")
        self.assertGreater(max(map(abs, samples[:SAMPLE_RATE // 20])), 1000)

    def test_R18_damage_sound_waits_for_the_hit_to_land(self):
        # The hit lands 0.2 s after the lunge starts (R7), so the damage sound is quiet before.
        for name in ["hurt-hero", "hurt-foe"]:
            _, samples = read_wav(name)
            self.assertEqual(max(map(abs, samples[:int(SAMPLE_RATE * 0.15)])), 0, name)
            self.assertGreater(max(map(abs, samples)), 1000, name)

    def test_R18_hero_and_foe_damage_sounds_differ(self):
        self.assertNotEqual(make_sound("hurt-hero"), make_sound("hurt-foe"))

    def test_R18_right_answer_plays_hero_attack_and_foe_damage(self):
        names = played(render_game(right(Game(PROBLEMS, hero="archer"))))
        self.assertIn("attack-archer", names)
        self.assertIn("hurt-foe", names)
        self.assertNotIn("hurt-hero", names)
        self.assertNotIn("attack-slime", names)

    def test_R18_wrong_answer_plays_foe_attack_and_hero_damage(self):
        names = played(render_game(wrong(Game(PROBLEMS, hero="archer"))))
        self.assertIn("attack-slime", names)
        self.assertIn("hurt-hero", names)
        self.assertNotIn("hurt-foe", names)
        self.assertNotIn("attack-archer", names)

    def test_R18_each_opponent_attacks_with_its_own_sound(self):
        for opp in OPPONENTS:
            g = wrong(Game({opp.category: PROBLEMS["addition"]}, opponents=[opp]))
            self.assertIn(f"attack-{opp.sprite}", played(render_game(g)), opp.name)

    def test_R18_unknown_monster_gets_a_plain_attack_sound(self):
        odd = Opponent("Mystery of Maths", "addition", 3, 1, sprite="ghost")
        names = played(render_game(wrong(Game(PROBLEMS, opponents=[odd]))))
        self.assertIn("attack-foe", names)

    def test_R18_critical_hit_adds_its_sound(self):
        g = Game(PROBLEMS, opponents=[Opponent("Big Slime", "addition", 9, 1, "slime")])
        self.assertNotIn("crit", played(render_game(right(g))))
        right(right(g))
        self.assertTrue(g.last_turn.crit)
        self.assertIn("crit", played(render_game(g)))

    def test_R18_knockout_adds_its_sound(self):
        g = Game(PROBLEMS)
        self.assertNotIn("knockout", played(render_game(right(g))))
        win_first_battle(g)
        self.assertIn("knockout", played(render_game(g)))
        self.assertIn("knockout", played(render_game(lose(Game(PROBLEMS)))))

    def test_R18_no_fight_sounds_before_any_answer(self):
        names = played(render_game(Game(PROBLEMS)))
        self.assertFalse([n for n in names if n.split("-")[0]
                          in ("attack", "hurt", "crit", "knockout")])


if __name__ == "__main__":
    unittest.main()
