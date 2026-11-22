"""Procedural horror foley + ambience beds (48 kHz mono float)."""
import numpy as np
from scipy.signal import fftconvolve
import audio

SR = 48000


def _box(x, k):
    c = np.cumsum(np.concatenate([[0.0], x])); n = len(x); i = np.arange(n)
    lo = np.clip(i - k // 2, 0, n); hi = np.clip(i - k // 2 + k, 0, n)
    return (c[hi] - c[lo]) / np.maximum(hi - lo, 1)


def _r(seed):
    return np.random.default_rng(seed)


def reverb(x, secs=1.2, wet=0.45, seed=0):
    n = int(secs * SR)
    ir = _r(seed).standard_normal(n) * np.exp(-np.arange(n) / SR * (6.9 / secs))
    ir = audio.lp(ir, 5000)
    y = fftconvolve(x, ir)[:len(x) + n]
    y = y / (np.max(np.abs(y)) + 1e-9) * np.max(np.abs(x))
    out = np.zeros(len(y)); out[:len(x)] += x * (1 - wet)
    return out + y * wet


# ---------------- beds (length n)
def crickets(n, seed=1):
    r = _r(seed); t = np.arange(n) / SR; out = np.zeros(n)
    for k in range(3):  # three insects at different pitches/rates
        f = 4200 + 900 * k; rate = 2.2 + 0.7 * k
        car = np.sin(2 * np.pi * f * t)
        trill = (np.sin(2 * np.pi * 32 * t) > 0.2).astype(float)
        gate = (np.sin(2 * np.pi * rate * t + r.random() * 6) > 0.35).astype(float)
        gate = np.convolve(gate, np.ones(240) / 240, mode="same") if len(gate) < 10 * SR else _box(gate, 240)
        out += car * trill * gate * (0.6 + 0.4 * r.random())
    return audio.hp(out, 2500) * 0.3


def forest_wind(n, seed=2):
    r = _r(seed); t = np.arange(n) / SR
    x = audio.bp(r.standard_normal(n), 150, 1200)
    hiss = audio.bp(r.standard_normal(n), 2500, 7000) * 0.25
    g = 0.3 + 0.7 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.09 * t)) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.23 * t + 2))
    return (x + hiss * g) * g * 0.6


def storm(n, seed=3):
    r = _r(seed); t = np.arange(n) / SR
    x = audio.bp(r.standard_normal(n), 100, 2500)
    howl = np.zeros(n)
    f = 300 + 180 * np.sin(2 * np.pi * 0.17 * t) + 90 * np.sin(2 * np.pi * 0.41 * t)
    ph = np.cumsum(f) / SR
    howl = np.sin(2 * np.pi * ph) * 0.15 * audio.bp(r.standard_normal(n), 200, 900) * 4
    g = 0.55 + 0.45 * np.abs(np.sin(2 * np.pi * 0.13 * t)) ** 2
    return (x * 1.2 + howl) * g


def room_tone(n, seed=4):
    return audio.lp(_r(seed).standard_normal(n), 400) * 0.08


def car_hum(n, seed=12):
    """inside a moving car at night: low engine drone + tyre/road rumble, slowly breathing"""
    r = _r(seed); t = np.arange(n) / SR
    eng = sum(np.sin(2 * np.pi * f * t + r.random() * 6) * a for f, a in ((31, 1.0), (62, 0.5), (93, 0.25)))
    eng *= 0.85 + 0.15 * np.sin(2 * np.pi * 0.07 * t)
    road = audio.lp(r.standard_normal(n), 260) * 1.0 + audio.bp(r.standard_normal(n), 300, 1800) * 0.9  # tyre/road hiss: audible on phones
    return (eng * 0.35 + road) * (0.9 + 0.1 * np.sin(2 * np.pi * 0.031 * t + 1))


def city_night(n, seed=13):
    """distant city at 1 AM: far traffic wash + faint hum"""
    r = _r(seed); t = np.arange(n) / SR
    wash = audio.bp(r.standard_normal(n), 250, 2500) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.05 * t) ** 2)
    hum = np.sin(2 * np.pi * 100 * t) * 0.03
    return wash * 0.5 + hum


BEDS = {"crickets": crickets, "wind": forest_wind, "storm": storm, "room": room_tone, "car": car_hum, "city": city_night}


# ---------------- one-shots
def footsteps(steps=6, interval=0.58, seed=5):
    r = _r(seed); L = int((steps * interval + 0.5) * SR); out = np.zeros(L)
    for k in range(steps):
        i = max(0, int((k * interval + r.normal(0, 0.03)) * SR))
        n = int(0.16 * SR); tt = np.arange(n) / SR
        thud = audio.lp(r.standard_normal(n), 700) * np.exp(-tt * 40) * 1.2
        crunch = audio.bp(r.standard_normal(n), 1800, 6000) * (r.random(n) > 0.82) * np.exp(-tt * 22)
        s = (thud + crunch * 0.9) * (0.75 + 0.5 * r.random())
        out[i:i + n] += s[:max(0, min(n, L - i))]
    return out


def owl(seed=6):
    tt = np.arange(int(0.45 * SR)) / SR
    def hoot(f0):
        f = f0 * (1 + 0.04 * np.sin(2 * np.pi * 7 * tt)) * (1 - 0.06 * tt)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / tt[-1]) ** 2
    gap = np.zeros(int(0.18 * SR))
    x = np.concatenate([hoot(390) * 0.6, gap, hoot(370), np.zeros(int(0.1 * SR)), hoot(360) * 0.8])
    return reverb(audio.lp(x, 1500), 1.8, 0.6, seed) * 0.6


def rustle(dur=1.4, seed=7):
    r = _r(seed); n = int(dur * SR); tt = np.arange(n) / SR
    x = audio.bp(r.standard_normal(n), 1200, 7000)
    env = np.convolve((r.random(n) > 0.9993).astype(float), np.exp(-np.arange(2400) / 300), mode="same")
    env = env / (env.max() + 1e-9) * np.sin(np.pi * tt / dur)
    return x * (0.25 + env)


def whisper(dur=1.8, seed=8):
    r = _r(seed); n = int(dur * SR); tt = np.arange(n) / SR
    x = audio.bp(r.standard_normal(n), 1500, 6000) + 0.5 * audio.bp(r.standard_normal(n), 400, 1200)
    syl = np.clip(np.sin(2 * np.pi * 5.5 * tt + 2 * np.sin(2 * np.pi * 1.3 * tt)), 0, 1) ** 1.5
    x = x * syl * np.sin(np.pi * tt / dur)
    return reverb(x, 2.2, 0.55, seed)


def crack(seed=9):
    r = _r(seed); n = int(0.6 * SR); tt = np.arange(n) / SR
    snap = audio.hp(r.standard_normal(n), 1500) * np.exp(-tt * 60)
    splinter = audio.bp(r.standard_normal(n), 800, 4000) * (r.random(n) > 0.95) * np.exp(-tt * 10)
    return reverb(snap * 1.4 + splinter, 1.0, 0.35, seed)


def gust(seed=10):
    r = _r(seed); n = int(2.5 * SR); tt = np.arange(n) / SR
    x = audio.bp(r.standard_normal(n), 200, 3000)
    env = np.sin(np.pi * np.clip(tt / 2.5, 0, 1)) ** 1.5
    return x * env * 1.4


def silence_drop():
    """a deep reverse swell that ends abruptly (use right before a line lands)"""
    r = _r(11); n = int(1.6 * SR); tt = np.arange(n) / SR
    x = reverb(audio.lp(r.standard_normal(n), 900) * np.exp(-tt * 3), 1.4, 0.7)[:n][::-1]
    return x


def car_door(seed=14):
    """car door closing: latch click + body thump"""
    r = _r(seed); n = int(0.7 * SR); t = np.arange(n) / SR
    thump = audio.lp(r.standard_normal(n), 180) * np.exp(-t * 14) * 3
    body = np.sin(2 * np.pi * 70 * t) * np.exp(-t * 18)
    click = audio.hp(r.standard_normal(n), 2500) * np.exp(-t * 90) * 0.6
    x = reverb(thump + body + click, 0.3, 0.15)[:n]
    return x / (np.abs(x).max() + 1e-9) * 0.9


def vibrate(times=3, seed=15):
    """phone vibrating (buzz bursts on a hard surface)"""
    on, off = 0.42, 0.38; L = int(times * (on + off) * SR); t = np.arange(L) / SR
    gate = ((t % (on + off)) < on).astype(float); gate = _box(gate, 300)
    buzz = np.sign(np.sin(2 * np.pi * 168 * t)) * 0.5 + np.sin(2 * np.pi * 336 * t) * 0.3
    return audio.lp(buzz, 1800) * gate * 0.5


def ringback(rings=2):
    """outgoing-call ringback tone (425 Hz, 1 s on / 2 s off), phone-speaker band-limited"""
    L = int(rings * 3.0 * SR); t = np.arange(L) / SR
    gate = _box(((t % 3.0) < 1.0).astype(float), 400)
    return audio.bp(np.sin(2 * np.pi * 425 * t), 300, 3400) * gate * 0.35


ONESHOTS = {"car_door": car_door, "vibrate": vibrate, "ringback": ringback, "footsteps": footsteps, "owl": owl, "rustle": rustle, "whisper": whisper,
            "crack": crack, "gust": gust, "reverse": silence_drop}
