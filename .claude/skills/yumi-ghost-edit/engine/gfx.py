"""Graphic components for the explainer style (9:16, 1080x1920).

Every builder returns a Layer: an RGBA numpy array (premultiplied=False) plus its
top-left position on the canvas. The renderer animates layers (pop / slide / fade).
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.environ.get("EDIT_FONT_DIR", os.path.join(HERE, "..", "fonts"))
CN = os.path.join(FONT_DIR, "YouSheBiaoTiHei.ttf")
EN = os.path.join(FONT_DIR, "Montserrat-700.ttf")
EN_B = os.path.join(FONT_DIR, "Montserrat-800.ttf")
# Traditional-Chinese capable faces (YouSheBiaoTiHei lacks many traditional glyphs)
TC_SANS = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc#3"
TC_SERIF = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Black.ttc#3"

# ---- palette (from the reference frames) ----
WHITE = (255, 255, 255)
GOLD_LINE = (232, 213, 140)          # card borders, connector lines
SUB_HL = (255, 215, 0)               # subtitle keyword highlight
ICE = [(0, (246, 251, 255)), (1, (190, 216, 240))]                 # intro title
GOLD_TXT = [(0, (255, 246, 196)), (0.5, (236, 205, 110)), (1, (196, 154, 60))]
ROSE = [(0, (255, 240, 226)), (0.42, (232, 190, 160)), (0.5, (150, 108, 84)),
        (0.62, (214, 168, 138)), (1, (250, 222, 198))]                # metallic 3D
TEAL_BOX = [(0, (64, 116, 138)), (1, (40, 62, 112))]
TAG_GRAD = [(0, (52, 104, 124)), (1, (44, 60, 110))]

_font_cache = {}


def font(path, size):
    k = (path, size)
    if k not in _font_cache:
        if "#" in path:  # "file.ttc#3" selects a face inside a collection
            fp, idx = path.rsplit("#", 1)
            _font_cache[k] = ImageFont.truetype(fp, size, index=int(idx))
        else:
            _font_cache[k] = ImageFont.truetype(path, size)
    return _font_cache[k]


class Layer:
    def __init__(self, rgba, x, y):
        self.rgba = rgba  # HxWx4 uint8
        self.x, self.y = int(x), int(y)

    @property
    def w(self):
        return self.rgba.shape[1]

    @property
    def h(self):
        return self.rgba.shape[0]


# ---------------------------------------------------------------- helpers
def grad_img(size, stops, vertical=True):
    w, h = size
    n = h if vertical else w
    t = np.linspace(0, 1, max(n, 2))
    cols = np.zeros((len(t), 3), np.float32)
    ps = [p for p, _ in stops]
    for c in range(3):
        cols[:, c] = np.interp(t, ps, [col[c] for _, col in stops])
    if vertical:
        arr = np.repeat(cols[:, None, :], w, axis=1)
    else:
        arr = np.repeat(cols[None, :, :], h, axis=0)
    return Image.fromarray(arr.astype(np.uint8), "RGB")


def text_mask(text, fnt, tracking=0, pad=40):
    """Grayscale mask of text with optional letter spacing (px)."""
    chars = list(text)
    widths = [fnt.getbbox(c)[2] - fnt.getbbox(c)[0] if c.strip() else fnt.size * 0.35 for c in chars]
    asc, desc = fnt.getmetrics()
    tw = int(sum(fnt.getlength(c) for c in chars) + tracking * (len(chars) - 1)) + 2 * pad
    th = asc + desc + 2 * pad
    m = Image.new("L", (max(tw, 1), th), 0)
    d = ImageDraw.Draw(m)
    x = pad
    for c in chars:
        d.text((x, pad), c, font=fnt, fill=255)
        x += fnt.getlength(c) + tracking
    bb = m.getbbox() or (0, 0, 1, 1)
    return m.crop((bb[0] - 4, bb[1] - 4, bb[2] + 4, bb[3] + 4))


def skew(img, k):
    """Italic-style shear (k ~ 0.12)."""
    w, h = img.size
    extra = int(abs(k) * h)
    return img.transform((w + extra, h), Image.AFFINE, (1, k, -extra if k > 0 else 0, 0, 1, 0),
                         resample=Image.BICUBIC)


def fill_mask(mask, stops):
    g = grad_img(mask.size, stops)
    out = g.convert("RGBA")
    out.putalpha(mask)
    return out


def solid(mask, color, alpha=255):
    out = Image.new("RGBA", mask.size, color + (0,))
    a = np.array(mask, np.float32) * (alpha / 255.0)
    out.putalpha(Image.fromarray(a.astype(np.uint8)))
    return out


def expand(img, pad):
    out = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0))
    out.alpha_composite(img, (pad, pad))
    return out


def shadowed(img, blur=10, offset=(0, 6), alpha=170, color=(0, 0, 0)):
    pad = blur * 3 + max(abs(offset[0]), abs(offset[1]))
    base = expand(img, pad)
    sh = solid(base.getchannel("A"), color, alpha).filter(ImageFilter.GaussianBlur(blur))
    out = Image.new("RGBA", base.size, (0, 0, 0, 0))
    out.alpha_composite(sh, offset)
    out.alpha_composite(base)
    return out


def glow(img, blur=14, color=(255, 255, 255), alpha=120):
    pad = blur * 3
    base = expand(img, pad)
    g = solid(base.getchannel("A"), color, alpha).filter(ImageFilter.GaussianBlur(blur))
    out = Image.new("RGBA", base.size, (0, 0, 0, 0))
    out.alpha_composite(g)
    out.alpha_composite(base)
    return out


def metallic_text(text, size, tracking=0, depth=7):
    """Rose-gold bevelled 3D text like the reference number cards."""
    m = text_mask(text, font(CN, size), tracking)
    m = skew(m, 0.0)
    face = fill_mask(m, ROSE)
    pad = depth + 30
    W2, H2 = m.width + 2 * pad, m.height + 2 * pad
    out = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
    sh = solid(m, (0, 0, 0), 200)
    shb = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
    shb.alpha_composite(sh, (pad + 4, pad + depth + 10))
    out.alpha_composite(shb.filter(ImageFilter.GaussianBlur(12)))
    for i in range(depth, 0, -1):  # extrusion
        shade = int(70 + 40 * (1 - i / depth))
        out.alpha_composite(solid(m, (shade + 20, shade - 5, shade - 25)), (pad, pad + i))
    # bevel: thin bright rim then face
    rim = solid(m.filter(ImageFilter.MaxFilter(3)), (255, 244, 230), 255)
    out.alpha_composite(rim, (pad, pad - 1))
    out.alpha_composite(face, (pad, pad))
    # inner highlight on upper half
    hl = Image.fromarray((np.array(m, np.float32) *
                          np.linspace(0.45, 0, m.height)[:, None]).astype(np.uint8))
    out.alpha_composite(solid(hl, (255, 255, 255)), (pad, pad))
    return out


def spaced_en(text, size, color, tracking=None, path=EN):
    f = font(path, size)
    tr = size * 0.55 if tracking is None else tracking
    return solid(text_mask(text, f, tr), color)


def rounded_box(size, radius, fill=None, outline=None, width=0, dotted_inset=None):
    w, h = size
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if fill is not None:
        if isinstance(fill, list):
            g = grad_img((w, h), fill).convert("RGBA")
            mk = Image.new("L", (w, h), 0)
            ImageDraw.Draw(mk).rounded_rectangle((0, 0, w - 1, h - 1), radius, fill=255)
            g.putalpha(mk)
            img.alpha_composite(g)
        else:
            d.rounded_rectangle((0, 0, w - 1, h - 1), radius, fill=fill)
    if outline is not None:
        d.rounded_rectangle((width // 2, width // 2, w - 1 - width // 2, h - 1 - width // 2),
                            radius, outline=outline, width=width)
    if dotted_inset:
        ins, col = dotted_inset
        x0, y0, x1, y1 = ins, ins, w - 1 - ins, h - 1 - ins
        for x in range(x0 + 6, x1 - 6, 7):
            d.point([(x, y0), (x, y1)], fill=col)
        for y in range(y0 + 6, y1 - 6, 7):
            d.point([(x0, y), (x1, y)], fill=col)
    return img


def flourish(size=70, color=(220, 232, 240, 255), width=3):
    """Small ornamental corner (L-bracket with a curl), top-left orientation."""
    s = size
    img = Image.new("RGBA", (s * 3, s * 3), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    S = 3
    d.line([(4 * S, 4 * S + s * 1.6 * S / S * 1), (4 * S, 4 * S)], fill=color, width=width * S)
    d.line([(4 * S, 4 * S), (4 * S + s * 1.6, 4 * S)], fill=color, width=width * S)
    d.arc([(14 * S, 14 * S), (14 * S + s * 0.9, 14 * S + s * 0.9)], 180, 450, fill=color, width=width * 2)
    d.arc([(14 * S + s * 0.25, 14 * S + s * 0.25), (14 * S + s * 0.65, 14 * S + s * 0.65)], 0, 270,
          fill=color, width=width * 2)
    img = img.resize((s, s), Image.LANCZOS)
    return img


def corners(box_w, box_h, size=70, color=(220, 232, 240, 255)):
    f = flourish(size, color)
    img = Image.new("RGBA", (box_w, box_h), (0, 0, 0, 0))
    img.alpha_composite(f, (0, 0))
    img.alpha_composite(f.transpose(Image.FLIP_LEFT_RIGHT), (box_w - size, 0))
    img.alpha_composite(f.transpose(Image.FLIP_TOP_BOTTOM), (0, box_h - size))
    img.alpha_composite(f.transpose(Image.ROTATE_180), (box_w - size, box_h - size))
    return img


def to_layer(img, cx, cy):
    arr = np.array(img.convert("RGBA"))
    return Layer(arr, cx - img.width / 2, cy - img.height / 2)


# ---------------------------------------------------------------- components
def intro_card(kicker, title, cy=1000):
    """Ornamental corner frame + small kicker + big icy skewed title."""
    k = glow(fill_mask(skew(text_mask(kicker, font(CN, 84), 6), 0.12), ICE), 10, (170, 210, 255), 90)
    tsize = 190
    while font(CN, tsize).getlength(title) + 10 * len(title) > 820:
        tsize -= 6
    t = glow(fill_mask(skew(text_mask(title, font(CN, tsize), 10), 0.12), ICE), 18, (150, 200, 255), 110)
    t = shadowed(t, 12, (0, 8), 160)
    bw = max(t.width, k.width) + 60
    bh = k.height + t.height + 60
    frame_w, frame_h = min(bw + 40, 900), bh + 120
    img = Image.new("RGBA", (frame_w + 80, frame_h + 80), (0, 0, 0, 0))
    img.alpha_composite(corners(frame_w, frame_h, 100, (214, 226, 236, 230)), (40, 40))
    img.alpha_composite(k, ((img.width - k.width) // 2, 40 + 60))
    img.alpha_composite(t, ((img.width - t.width) // 2, 40 + 50 + k.height - 10))
    return to_layer(img, W / 2, cy)


def topic_tag(cn, en, y=250):
    """Slanted teal->navy tag flush to the left edge (no flag, no timer)."""
    c = solid(text_mask(cn, font(CN, 58), 2), WHITE)
    e = solid(text_mask(en, font(EN, 22), 1), (200, 214, 226))
    h, slant = 116, 34
    w = max(c.width, e.width) + 60 + slant + 30
    img = Image.new("RGBA", (w + 10, h + 10), (0, 0, 0, 0))
    g = grad_img((w, h), TAG_GRAD, vertical=False).convert("RGBA")
    mk = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mk).polygon([(0, 0), (w - slant, 0), (w, h), (0, h)], fill=235)
    g.putalpha(mk)
    img.alpha_composite(g, (0, 0))
    d = ImageDraw.Draw(img)
    d.line([(w - slant, 0), (w, h)], fill=(190, 214, 230, 255), width=3)
    d.line([(0, h - 1), (w, h - 1)], fill=(190, 214, 230, 160), width=2)
    img.alpha_composite(c, (60, 14))
    img.alpha_composite(e, (62, 18 + c.height))
    img = shadowed(img, 8, (0, 4), 140)
    return Layer(np.array(img), -24, y - 24)


def gold_card(sub, main, en, cy=900, w=760):
    """Gold-framed rounded card (reference: 神权共和 card)."""
    s = solid(text_mask(sub, font(CN, 64), 4), WHITE) if sub else None
    m = shadowed(fill_mask(text_mask(main, font(CN, 150), 14), GOLD_TXT), 8, (0, 5), 170)
    e = solid(text_mask(en, font(EN_B, 36), 2), WHITE) if en else None
    inner_h = (s.height + 10 if s else 0) + m.height + (e.height + 14 if e else 0)
    h = inner_h + 130
    box = rounded_box((w, h), 30, fill=(12, 14, 18, 120), outline=(232, 213, 140, 255), width=6)
    box = glow(box, 14, (255, 236, 160), 110)
    pad = (box.width - w) // 2
    d = ImageDraw.Draw(box)
    # top-centre flourish
    cxb = box.width // 2
    d.line([(cxb - 60, pad + 34), (cxb + 60, pad + 34)], fill=(232, 213, 140, 230), width=2)
    d.ellipse([(cxb - 7, pad + 27), (cxb + 7, pad + 41)], outline=(232, 213, 140, 230), width=2)
    fl = flourish(46, (232, 213, 140, 220))
    box.alpha_composite(fl.transpose(Image.FLIP_TOP_BOTTOM), (pad + 22, pad + h - 68))
    box.alpha_composite(fl.transpose(Image.ROTATE_180), (pad + w - 68, pad + h - 68))
    y = pad + 62
    if s:
        box.alpha_composite(s, (cxb - s.width // 2, y)); y += s.height + 10
    box.alpha_composite(m, (cxb - m.width // 2, y - 18)); y += m.height - 30
    if e:
        box.alpha_composite(e, (cxb - e.width // 2, y + 8))
    return to_layer(box, W / 2, cy)


def flow_parts(top_cn, top_en, left, right, cy=820):
    """Org-chart: top glass box -> two teal boxes. Returns (top_layer, children_layer)."""
    tw, th = 600, 170
    top = rounded_box((tw, th), 18, fill=(22, 26, 32, 215), outline=(236, 236, 236, 255), width=4,
                      dotted_inset=(10, (200, 200, 200, 200)))
    tm = shadowed(fill_mask(text_mask(top_cn, font(CN, 112), 40), GOLD_TXT[:2] + [(1, (255, 255, 255))]), 6, (0, 4), 160)
    te = solid(text_mask(top_en, font(EN, 26), 6), (220, 220, 220))
    top.alpha_composite(tm, ((tw - tm.width) // 2, 8))
    top.alpha_composite(te, ((tw - te.width) // 2, th - te.height - 18))
    top = glow(top, 10, (255, 255, 255), 60)
    top_cy = cy - 260
    top_layer = to_layer(top, W / 2, top_cy)

    cw, ch = 340, 210
    kids = Image.new("RGBA", (W, 520), (0, 0, 0, 0))
    d = ImageDraw.Draw(kids)
    y0 = 0
    lx, rx = W / 2 - 250, W / 2 + 250
    col = (232, 213, 140, 255)
    d.line([(W / 2, y0), (W / 2, y0 + 70)], fill=col, width=5)
    d.line([(lx, y0 + 70), (rx, y0 + 70)], fill=col, width=5)
    for x in (lx, rx):
        d.line([(x, y0 + 70), (x, y0 + 150)], fill=col, width=5)
        d.polygon([(x - 16, y0 + 140), (x + 16, y0 + 140), (x, y0 + 168)], fill=col)
    for x, (cn, en) in ((lx, left), (rx, right)):
        b = rounded_box((cw, ch), 14, fill=TEAL_BOX, outline=(220, 232, 240, 255), width=4,
                        dotted_inset=(9, (200, 220, 235, 200)))
        c = shadowed(fill_mask(text_mask(cn, font(CN, 92), 22), GOLD_TXT), 5, (0, 3), 150)
        e = solid(text_mask(en, font(EN_B, 30), 1), WHITE)
        b.alpha_composite(c, ((cw - c.width) // 2, 30))
        b.alpha_composite(e, ((cw - e.width) // 2, ch - e.height - 32))
        b = shadowed(b, 10, (0, 6), 150)
        kids.alpha_composite(b, (int(x - b.width / 2), y0 + 175 - (b.height - ch) // 2))
    kids_layer = Layer(np.array(kids), 0, top_cy + th / 2 + 10)
    return top_layer, kids_layer


def metal_word(kicker, word, en, cy=860):
    k = metallic_text(kicker, 76, tracking=30, depth=4) if kicker else None
    w = metallic_text(word, 300, tracking=30, depth=10)
    e = spaced_en(en, 46, (236, 212, 186)) if en else None
    hh = (k.height if k else 0) + w.height + (e.height if e else 0)
    img = Image.new("RGBA", (max(w.width, (e.width if e else 0)) + 40, hh + 20), (0, 0, 0, 0))
    y = 0
    if k:
        img.alpha_composite(k, ((img.width - k.width) // 2, y)); y += k.height - 16
    img.alpha_composite(w, ((img.width - w.width) // 2, y)); y += w.height - 40
    if e:
        img.alpha_composite(e, ((img.width - e.width) // 2, y))
    return to_layer(img, W / 2, cy)


def pip_ring(d=270):
    """Gold ring + glow drawn around a circular picture-in-picture."""
    S = d + 80
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    dr.ellipse([(40, 40), (40 + d, 40 + d)], outline=(236, 222, 160, 255), width=6)
    img = glow(img, 12, (255, 236, 170), 140)
    return img


def subtitle(text, highlights=(), size=82, y_center=1470, max_w=980, font_path=None):
    """Bold white condensed subtitle with soft dark shadow, optional gold keywords."""
    fp = font_path or CN
    f = font(fp, size)
    # build per-char colour map
    colors = [WHITE] * len(text)
    for hword in highlights:
        i = text.find(hword)
        while i >= 0:
            for j in range(i, i + len(hword)):
                colors[j] = SUB_HL
            i = text.find(hword, i + len(hword))
    tracking = 2
    total = sum(f.getlength(c) for c in text) + tracking * (len(text) - 1)
    if total > max_w:
        f = font(fp, int(size * max_w / total))
        total = sum(f.getlength(c) for c in text) + tracking * (len(text) - 1)
    asc, desc = f.getmetrics()
    pad = 40
    img = Image.new("RGBA", (int(total) + 2 * pad, asc + desc + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = pad
    for c, col in zip(text, colors):
        d.text((x, pad), c, font=f, fill=col + (255,))
        x += f.getlength(c) + tracking
    a = img.getchannel("A")
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sh.putalpha(a.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(5)).point(lambda v: int(v * 0.85)))
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.alpha_composite(sh, (0, 3))
    out.alpha_composite(img)
    return to_layer(out, W / 2, y_center)


# ---------------------------------------------------------------- plate textures
def halftone(shape=(H, W), pitch=7, r=1.6, alpha=0.30):
    """Dot-screen overlay (black dots) used on dimmed plates."""
    yy, xx = np.mgrid[0:shape[0], 0:shape[1]].astype(np.float32)
    dx = (xx % pitch) - pitch / 2
    dy = (yy % pitch) - pitch / 2
    dist = np.sqrt(dx * dx + dy * dy)
    dots = np.clip(r + 0.5 - dist, 0, 1) * alpha
    return dots  # HxW float, multiply-darken amount


def vignette(shape=(H, W), strength=0.55):
    yy, xx = np.mgrid[0:shape[0], 0:shape[1]].astype(np.float32)
    nx = (xx / shape[1] - 0.5) * 2
    ny = (yy / shape[0] - 0.5) * 2
    v = 1 - strength * np.clip((nx ** 2 * 0.9 + ny ** 2 * 0.6) - 0.15, 0, 1)
    return v
