"""Every sound in Math Quest, made by Python itself (R15-R18).

No sound files are stored: each sound is built from simple waveforms (square,
triangle, sawtooth, sine and random noise) and turned into WAV bytes with the
standard library's `wave` module. The web server sends them at /sound/<name>.wav.

Sound names:
    music-<key>       looping music for an opponent (R16), see MUSIC
    jingle-victory    a short fanfare when the player wins (R16)
    jingle-defeat     a short sad tune when the player loses (R16)
    voice-<hero>      the hero's babble voice line (R17), see VOICES
    attack-<sprite>   a fighter's attack sound (R18), see ATTACK_SOUNDS
    attack-foe        the attack sound for an opponent without its own
    hurt-hero         the hero takes damage (R18)
    hurt-foe          an opponent takes damage (R18)
    crit              a critical hit (R18)
    knockout          a fighter is knocked out (R18)
"""

from dataclasses import dataclass
from functools import lru_cache
import io
import math
import random
import wave

SAMPLE_RATE = 22050   # samples per second; plenty for chiptune-style sound
PEAK = 0.8            # loudest point of every sound, as a fraction of the maximum
HIT_DELAY = 0.2       # seconds from the start of a lunge until the hit lands (R7)
KO_DELAY = 0.8        # seconds until a knocked-out fighter starts to fall (R7)
JINGLE_DELAY = 1.2    # let the last blow and the fall play before the end tune


# ---------------------------------------------------------------------------
# Building blocks. A sound is a plain list of floats between -1 and 1.
# ---------------------------------------------------------------------------

def silence(seconds):
    return [0.0] * int(seconds * SAMPLE_RATE)


def _wave_value(shape, phase, duty=0.5):
    """One point of a waveform; `phase` counts cycles (0.25 = a quarter cycle)."""
    p = phase % 1.0
    if shape == "square":
        return 1.0 if p < duty else -1.0
    if shape == "triangle":
        return 4 * p - 1 if p < 0.5 else 3 - 4 * p
    if shape == "saw":
        return 2 * p - 1
    return math.sin(2 * math.pi * p)   # "sine"


def tone(shape, freq, seconds, volume=1.0, end_freq=None, duty=0.5,
         vibrato=0.0, vibrato_rate=6.0, attack=0.005, decay=None):
    """A note that may slide from `freq` to `end_freq` (a sweep).

    `decay` makes the note fade out like a plucked string (bigger = faster);
    without it, the note holds and then fades over its last few milliseconds.
    """
    n = int(seconds * SAMPLE_RATE)
    end_freq = end_freq or freq
    out, phase = [], 0.0
    release = min(n // 4, int(0.02 * SAMPLE_RATE))
    attack_n = max(1, int(attack * SAMPLE_RATE))
    for i in range(n):
        t = i / SAMPLE_RATE
        f = freq * (end_freq / freq) ** (i / n)          # smooth (exponential) slide
        if vibrato:
            f *= 1 + vibrato * math.sin(2 * math.pi * vibrato_rate * t)
        phase += f / SAMPLE_RATE
        level = min(1.0, i / attack_n)
        if decay:
            level *= math.exp(-decay * t)
        elif i > n - release:
            level *= (n - i) / release
        out.append(volume * level * _wave_value(shape, phase, duty))
    return out


def noise(seconds, volume=1.0, brightness=0.5, end_brightness=None, decay=8.0,
          seed=1, tremolo=0.0, attack=0.002):
    """Random hiss, smoothed by a simple filter.

    `brightness` (0-1) sets how hissy it is: low values give a dull thump, high
    values a sharp crash. It may change over the sound (a "whoosh"). The fixed
    `seed` makes the same sound every time, so tests can compare sounds.
    """
    rng = random.Random(seed)
    n = int(seconds * SAMPLE_RATE)
    end_brightness = brightness if end_brightness is None else end_brightness
    out, smooth = [], 0.0
    attack_n = max(1, int(attack * SAMPLE_RATE))
    for i in range(n):
        t = i / SAMPLE_RATE
        b = brightness + (end_brightness - brightness) * i / n
        smooth += (b * b) * (rng.uniform(-1, 1) - smooth)  # one-pole low-pass filter
        level = min(1.0, i / attack_n) * math.exp(-decay * t)
        if tremolo:
            level *= 0.5 + 0.5 * math.sin(2 * math.pi * tremolo * t)
        out.append(volume * level * smooth * (1.5 / max(b, 0.15)))
    return out


def mix(*parts):
    """Play several sounds at the same time. Each part is (start_seconds, samples)."""
    length = max(int(start * SAMPLE_RATE) + len(s) for start, s in parts)
    out = [0.0] * length
    for start, samples in parts:
        offset = int(start * SAMPLE_RATE)
        for i, v in enumerate(samples):
            out[offset + i] += v
    return out


def then(*sounds):
    """Play sounds one after another."""
    out = []
    for s in sounds:
        out.extend(s)
    return out


def to_wav(samples):
    """Scale a sound so its loudest point is PEAK, and pack it as 16-bit mono WAV."""
    loudest = max((abs(v) for v in samples), default=0.0)
    scale = PEAK * 32767 / loudest if loudest else 0.0
    frames = bytearray()
    for v in samples:
        frames += int(round(v * scale)).to_bytes(2, "little", signed=True)
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(bytes(frames))
    return buffer.getvalue()


NOTE_NAMES = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7,
              "G#": 8, "A": 9, "A#": 10, "B": 11}


def note_freq(note):
    """'A4' -> 440.0 Hz. Each step up the 12-note scale multiplies by 2 ** (1/12)."""
    name, octave = note[:-1], int(note[-1])
    midi = 12 * (octave + 1) + NOTE_NAMES[name]
    return 440.0 * 2 ** ((midi - 69) / 12)


# ---------------------------------------------------------------------------
# Music (R16). Written like an old "tracker": one token per eighth note.
#   a note such as C5 or F#3 starts a note, "-" holds the note before it longer,
#   "." is a rest. Drums: k = kick, s = snare, h = hi-hat, "." = nothing.
#   The "|" bar lines are only there to make the tunes easier to read.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Theme:
    title: str       # shown next to the music player
    tempo: int       # beats per minute; each token is half a beat
    wave: str        # the melody's waveform: square, triangle, saw or sine
    melody: str
    bass: str
    drums: str
    bass_wave: str = "triangle"
    staccato: float = 0.9   # how much of each step a note fills (short = bouncy)


MUSIC = {
    # Slime Swamp: slow, bouncy and happy (C major, short notes).
    "swamp-bounce": Theme(
        "Swamp Bounce", 100, "triangle",
        melody="C5 . E5 G5 . E5 D5 . | C5 . A4 G4 . . . . | A4 . C5 D5 . E5 D5 C5 | D5 - - - . . G4 .",
        bass="C3 . G2 . C3 . G2 . | F2 . C3 . F2 . C3 . | A2 . E3 . A2 . E3 . | G2 . D3 . G2 . B2 .",
        drums="k . . h k . . h | k . . h k . . h | k . . h k . . h | k . s . k . s h",
        staccato=0.5),
    # Goblin Cave: quick tiptoeing minor tune with sneaky half-steps.
    "sneaky-cave": Theme(
        "Sneaky Cave", 132, "square",
        melody="A4 . C5 . D#5 E5 . . | A4 . C5 . B4 . G#4 . | A4 . C5 . D#5 E5 . . | F5 . E5 . D#5 . E5 .",
        bass="A2 . . . E2 . . . | A2 . . . E2 . . . | A2 . . . E2 . . . | B2 . . . E2 . . .",
        drums="h . . h . . h . | h . . h . . h . | h . . h . . h . | h . h . h . s .",
        staccato=0.35),
    # Orc War Camp: a march over pounding drums.
    "war-drums": Theme(
        "War Drums", 112, "saw",
        melody="D4 - - . D4 . F4 . | G4 - - . F4 . E4 . | D4 - - . D4 . A4 . | G4 - F4 - E4 - C4 -",
        bass="D2 . D2 . D2 . D2 . | G2 . G2 . G2 . G2 . | D2 . D2 . D2 . D2 . | A1 . A1 . C2 . C2 .",
        drums="k . k s k . k s | k . k s k k k s | k . k s k . k s | k k s k k s s s",
        bass_wave="square"),
    # Troll Bridge: slow, low and heavy, every beat a stomp.
    "bridge-stomp": Theme(
        "Bridge Stomp", 76, "square",
        melody="E3 - - - G3 - - . | F#3 - E3 - D3 - - . | E3 - - - B3 - - . | A3 - G3 - F#3 - E3 .",
        bass="E2 - . . E2 - . . | D2 - . . D2 - . . | E2 - . . E2 - . . | B1 - . . B1 - . .",
        drums="k . . . s . . . | k . . . s . . . | k . . . s . . . | k . k . s . s ."),
    # Dragon's Volcano: fast, fiery arpeggios (harmonic minor).
    "volcano-fury": Theme(
        "Volcano Fury", 152, "saw",
        melody="C5 D#5 G5 C6 G5 D#5 C5 D#5 | G#4 C5 D#5 G#5 D#5 C5 G#4 C5 | "
               "G4 B4 D5 G5 D5 B4 G4 B4 | C5 D#5 G5 C6 B5 G5 D5 B4",
        bass="C2 C2 C3 C2 C2 C2 C3 C2 | G#1 G#1 G#2 G#1 G#1 G#1 G#2 G#1 | "
             "G1 G1 G2 G1 G1 G1 G2 G1 | C2 C2 C3 C2 G1 G1 G2 G1",
        drums="k h s h k k s h | k h s h k k s h | k h s h k k s h | k s k s k s s s",
        bass_wave="saw", staccato=0.8),
    # For an opponent with no music of its own: a plain, calm tune.
    "default": Theme(
        "Battle", 120, "sine",
        melody="C5 . E5 . G5 . E5 . | F5 . A5 . G5 - - . | E5 . G5 . D5 . F5 . | C5 - - - . . . .",
        bass="C3 . . . C3 . . . | F2 . . . G2 . . . | C3 . . . G2 . . . | C3 . . . . . . .",
        drums="k . . . s . . . | k . . . s . . . | k . . . s . . . | k . . . s . . ."),
}

# Each place has its own music, so the music follows the opponent's scene (R8).
MUSIC_FOR_SCENE = {"swamp": "swamp-bounce", "cave": "sneaky-cave", "camp": "war-drums",
                   "bridge": "bridge-stomp", "volcano": "volcano-fury"}


def music_key(opponent):
    """The key in MUSIC for an opponent, or "default" if it has none (R16)."""
    return MUSIC_FOR_SCENE.get(opponent.scene, "default")


def _tokens(track):
    return [t for t in track.split() if t != "|"]


def _step_seconds(theme):
    return 60 / theme.tempo / 2   # one eighth note


def music_length(key):
    """How many seconds one loop of the music lasts."""
    theme = MUSIC[key]
    return len(_tokens(theme.melody)) * _step_seconds(theme)


def _notes(track, step, shape, volume, staccato):
    """Turn one tracker line into (start_seconds, samples) parts."""
    tokens = _tokens(track)
    parts = []
    for i, token in enumerate(tokens):
        if token in ".-":
            continue
        held = 1
        while i + held < len(tokens) and tokens[i + held] == "-":
            held += 1
        length = step * (held - 1 + staccato)
        parts.append((i * step, tone(shape, note_freq(token), length, volume, duty=0.25)))
    return parts


def _drum(kind):
    if kind == "k":   # kick: a deep thump that drops in pitch
        return tone("sine", 140, 0.18, 0.9, end_freq=45, decay=14)
    if kind == "s":   # snare: a short crack of noise
        return noise(0.14, 0.45, brightness=0.7, decay=22, seed=7)
    return noise(0.04, 0.15, brightness=1.0, decay=60, seed=3)   # h: hi-hat tick


def make_music(key):
    theme = MUSIC[key]
    step = _step_seconds(theme)
    total = music_length(key)
    parts = [(0, silence(total))]
    parts += _notes(theme.melody, step, theme.wave, 0.35, theme.staccato)
    parts += _notes(theme.bass, step, theme.bass_wave, 0.4, 0.9)
    parts += [(i * step, _drum(t)) for i, t in enumerate(_tokens(theme.drums)) if t in "ksh"]
    loop = mix(*parts)
    # Anything that rings past the end wraps round to the start, so the loop is seamless.
    n = int(total * SAMPLE_RATE)
    for i, v in enumerate(loop[n:]):
        loop[i % n] += v
    return loop[:n]


def _jingle(notes, shape, step, drop_last=1.0):
    """A short tune played once, after the final blow has landed (R16)."""
    parts = [(0, silence(JINGLE_DELAY))]
    for i, note in enumerate(notes):
        last = i == len(notes) - 1
        length = step * (4 if last else 0.9)
        end = note_freq(note) * (drop_last if last else 1.0)
        parts.append((JINGLE_DELAY + i * step,
                      tone(shape, note_freq(note), length, 0.5, end_freq=end, duty=0.25)))
    return mix(*parts)


def victory_jingle():
    return _jingle(["C5", "E5", "G5", "C6", "G5", "C6"], "square", 0.13)


def defeat_jingle():
    return _jingle(["G4", "F#4", "F4", "E4"], "triangle", 0.35, drop_last=0.7)


# ---------------------------------------------------------------------------
# Hero voices (R17): babble, like the made-up "talking" in many games.
# Each syllable is a short buzzy note that slides a little, so it sounds like
# speech without any real words.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Voice:
    pitch: float      # the voice's basic pitch in Hz (low = deep voice)
    wave: str         # its "throat": square = buzzy, saw = raspy, triangle = soft
    syllables: tuple  # (semitones above the pitch, seconds, slide) for each syllable
    vibrato: float = 0.0   # wobble, for an old or mysterious voice


VOICES = {
    # Sir Aldric: deep and steady, a bold "Hup-ha-HAA!"
    "knight": Voice(110, "square",
                    ((0, 0.12, 1.0), (3, 0.12, 1.0), (7, 0.32, 0.85))),
    # Zoltan: an old, wavering mutter that rises like a spell.
    "wizard": Voice(150, "saw",
                    ((0, 0.14, 1.1), (5, 0.1, 1.0), (2, 0.14, 1.1), (9, 0.3, 1.25)),
                    vibrato=0.03),
    # Wren: high, quick and chirpy.
    "archer": Voice(280, "triangle",
                    ((0, 0.08, 1.15), (4, 0.08, 1.1), (7, 0.08, 1.1), (12, 0.18, 1.2))),
    # Kaito: short, clipped syllables, then a sharp "Hai!"
    "ninja": Voice(200, "square",
                   ((0, 0.06, 1.0), (0, 0.06, 1.0), (5, 0.06, 1.0), (10, 0.2, 0.75))),
}


def make_voice(voice):
    parts, t = [], 0.0
    for semitones, seconds, slide in voice.syllables:
        f = voice.pitch * 2 ** (semitones / 12)
        syllable = tone(voice.wave, f, seconds, 0.6, end_freq=f * slide,
                        duty=0.3, vibrato=voice.vibrato, attack=0.015)
        breath = noise(0.03, 0.15, brightness=0.8, decay=30, seed=int(f))  # the consonant
        parts += [(t, breath), (t + 0.01, syllable)]
        t += seconds + 0.04
    return mix(*parts)


# ---------------------------------------------------------------------------
# Fight sounds (R18). Attack sounds start at once (with the lunge); damage
# sounds wait HIT_DELAY seconds, until the hit lands.
# ---------------------------------------------------------------------------

def _sword_swish():
    swish = noise(0.25, 0.8, brightness=0.3, end_brightness=0.9, decay=6, seed=11)
    shing = mix((0, tone("sine", 2200, 0.35, 0.25, decay=10)),
                (0, tone("sine", 3300, 0.35, 0.15, decay=12)))
    return mix((0, swish), (0.15, shing))


def _magic_zap():
    return mix((0, tone("square", 1400, 0.4, 0.4, end_freq=180, duty=0.5,
                        vibrato=0.08, vibrato_rate=30)),
               (0, tone("sine", 2000, 0.3, 0.3, end_freq=900, decay=6)))


def _bow_twang():
    twang = tone("triangle", 240, 0.35, 0.8, end_freq=180, decay=9)
    whoosh = noise(0.2, 0.4, brightness=0.6, end_brightness=0.9, decay=10, seed=13)
    return mix((0, twang), (0.05, whoosh))


def _shuriken_whoosh():
    return mix((0, noise(0.35, 0.8, brightness=0.8, end_brightness=0.5, decay=4,
                         seed=17, tremolo=28)),
               (0, tone("sine", 1800, 0.3, 0.15, end_freq=1200, decay=8)))


def _slime_splat():
    return mix((0, noise(0.25, 0.9, brightness=0.25, decay=14, seed=19)),
               (0, tone("sine", 180, 0.3, 0.7, end_freq=60, decay=10)))


def _dagger_stab():
    return mix((0, noise(0.08, 0.6, brightness=1.0, decay=40, seed=23)),
               (0.02, tone("square", 700, 0.15, 0.3, end_freq=350, duty=0.25, decay=18)))


def _club_thump():
    return mix((0, tone("sine", 100, 0.35, 1.0, end_freq=40, decay=9)),
               (0, noise(0.2, 0.5, brightness=0.2, decay=15, seed=29)))


def _troll_smash():
    return mix((0, tone("sine", 70, 0.6, 1.0, end_freq=30, decay=5)),
               (0, noise(0.5, 0.7, brightness=0.35, end_brightness=0.15, decay=6, seed=31)),
               (0.05, tone("square", 90, 0.3, 0.2, end_freq=50, decay=10)))


def _dragon_roar():
    return mix((0, tone("saw", 95, 0.9, 0.6, end_freq=70, vibrato=0.06,
                        vibrato_rate=11, attack=0.05, decay=2.5)),
               (0, noise(0.9, 0.6, brightness=0.5, end_brightness=0.3, decay=2.5,
                         seed=37, attack=0.08)))


def _foe_attack():
    return tone("square", 320, 0.22, 0.6, end_freq=160, duty=0.5, decay=8)


# One attack sound per fighter, keyed like sprites.HEROES and sprites.MONSTERS.
ATTACK_SOUNDS = {
    "knight": _sword_swish, "wizard": _magic_zap, "archer": _bow_twang,
    "ninja": _shuriken_whoosh, "slime": _slime_splat, "goblin": _dagger_stab,
    "orc": _club_thump, "troll": _troll_smash, "dragon": _dragon_roar,
}


def hero_hurt():
    """The hero cries out: a falling 'oof'."""
    oof = tone("square", 420, 0.25, 0.5, end_freq=200, duty=0.3, decay=6)
    smack = noise(0.08, 0.5, brightness=0.6, decay=35, seed=41)
    return then(silence(HIT_DELAY), mix((0, smack), (0.01, oof)))


def foe_hurt():
    """A monster is struck: a solid smack and a low grunt."""
    smack = noise(0.12, 0.8, brightness=0.75, decay=25, seed=43)
    grunt = tone("saw", 160, 0.25, 0.4, end_freq=90, decay=8)
    return then(silence(HIT_DELAY), mix((0, smack), (0.02, grunt)))


def crit():
    """A bright, rising ding for a critical hit."""
    parts = [(i * 0.06, tone("square", note_freq(n), 0.18, 0.3, duty=0.25, decay=10))
             for i, n in enumerate(["C6", "E6", "G6", "C7"])]
    return then(silence(HIT_DELAY), mix(*parts))


def knockout():
    """A long falling whistle and a thud as the fighter hits the ground."""
    fall = tone("triangle", 700, 0.45, 0.5, end_freq=90)
    thud = mix((0, tone("sine", 90, 0.2, 0.8, end_freq=40, decay=15)),
               (0, noise(0.15, 0.4, brightness=0.25, decay=20, seed=47)))
    return then(silence(KO_DELAY - 0.1), fall, thud)


# ---------------------------------------------------------------------------
# The list of every sound, by name.
# ---------------------------------------------------------------------------

def _builders():
    builders = {f"music-{k}": (lambda k=k: make_music(k)) for k in MUSIC}
    builders.update({f"voice-{k}": (lambda v=v: make_voice(v)) for k, v in VOICES.items()})
    builders.update({f"attack-{k}": f for k, f in ATTACK_SOUNDS.items()})
    builders.update({"attack-foe": _foe_attack, "hurt-hero": hero_hurt, "hurt-foe": foe_hurt,
                     "crit": crit, "knockout": knockout,
                     "jingle-victory": victory_jingle, "jingle-defeat": defeat_jingle})
    return builders


BUILDERS = _builders()


def sound_names():
    """Every sound the server can send."""
    return set(BUILDERS)


@lru_cache(maxsize=None)
def make_sound(name):
    """The WAV bytes for a sound, or None if there is no sound with that name.

    Each sound is built the first time it is asked for, then kept (cached).
    """
    builder = BUILDERS.get(name)
    return to_wav(builder()) if builder else None
