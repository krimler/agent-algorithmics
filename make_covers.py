#!/usr/bin/env python3
"""Generate the fractal cover images for *Agent Algorithmics*.

    .venv/bin/python make_covers.py        # writes covers/front.jpg, covers/back.jpg

Front cover: dark.  A deep zoom into the Mandelbrot set's seahorse valley,
coloured from near-black through deep blue to cyan at the boundary.
Back cover: bright.  A Julia set on a warm cream ground, coloured gold to
orange to magenta.

Both are US-letter portrait at 150 dpi (1275 x 1650) and saved as JPEG at
quality 82, which keeps each under about half a megabyte.
"""
import numpy as np
from PIL import Image
from pathlib import Path

W, H = 1275, 1650
OUT = Path(__file__).resolve().parent / "covers"
OUT.mkdir(exist_ok=True)


def escape_time(c, z0=None, max_iter=400, radius=4.0):
    """Smooth escape-time field in [0, 1); NaN where the orbit never escaped."""
    z = np.zeros_like(c) if z0 is None else z0.copy()
    cc = c
    if z0 is not None:            # Julia set: iterate z, c is the constant
        z, cc = c.copy(), z0
    n = np.full(c.shape, np.nan, dtype=np.float64)
    alive = np.ones(c.shape, dtype=bool)
    for i in range(max_iter):
        z[alive] = z[alive] * z[alive] + cc[alive] if np.ndim(cc) else z[alive] * z[alive] + cc
        mag = np.abs(z)
        escaped = alive & (mag > radius)
        # smooth iteration count
        n[escaped] = i + 1 - np.log(np.log(mag[escaped])) / np.log(2)
        alive &= ~escaped
        if not alive.any():
            break
    return n


def grid(cx, cy, half_w, w=W, h=H):
    half_h = half_w * h / w
    xs = np.linspace(cx - half_w, cx + half_w, w)
    ys = np.linspace(cy + half_h, cy - half_h, h)
    X, Y = np.meshgrid(xs, ys)
    return X + 1j * Y


def colorize(n, stops, inside, period=40.0, gamma=1.0):
    """Map the escape field through a cyclic gradient defined by RGB stops."""
    stops = np.array(stops, dtype=np.float64)
    k = len(stops)
    t = np.nan_to_num(n, nan=0.0)
    t = (t / period) ** gamma % 1.0
    pos = t * (k - 1)
    i0 = np.floor(pos).astype(int) % (k - 1)
    frac = (pos - np.floor(pos))[..., None]
    rgb = stops[i0] * (1 - frac) + stops[i0 + 1] * frac
    rgb[np.isnan(n)] = inside
    return np.clip(rgb, 0, 255).astype(np.uint8)


def front():
    # Seahorse valley, deep portrait crop so filaments fill the page
    c = grid(-0.74364, 0.13182, 0.0042)
    n = escape_time(c, max_iter=900)
    stops = [
        (3, 4, 12), (6, 14, 48), (14, 40, 120), (26, 96, 190),
        (90, 190, 240), (210, 240, 255), (40, 110, 200), (8, 20, 64), (3, 4, 12),
    ]
    img = colorize(n, stops, inside=(1, 2, 8), period=70.0, gamma=0.8).astype(np.float64)
    # overall darkening, plus a smooth extra fade over the top 45% so the title reads
    rows = np.arange(H)[:, None, None]
    top = 0.45 * H
    fade = np.where(rows < top, 0.45 + 0.55 * (rows / top) ** 1.5, 1.0)
    img = np.clip(img * 0.82 * fade, 0, 255).astype(np.uint8)
    Image.fromarray(img, "RGB").save(OUT / "front.jpg", quality=74, optimize=True)


def back():
    # Julia set, bright palette on cream
    z0 = grid(0.0, 0.0, 1.55)
    cst = np.complex128(-0.79 + 0.15j)
    n = escape_time(z0, z0=cst, max_iter=300)
    stops = [
        (255, 250, 236), (255, 222, 120), (250, 160, 40), (235, 80, 90),
        (200, 60, 170), (255, 200, 90), (255, 250, 236),
    ]
    img = colorize(n, stops, inside=(255, 246, 225), period=60.0, gamma=0.9)
    Image.fromarray(img, "RGB").save(OUT / "back.jpg", quality=82, optimize=True)


if __name__ == "__main__":
    front()
    back()
    for f in ("front.jpg", "back.jpg"):
        print(f, (OUT / f).stat().st_size // 1024, "KB")
