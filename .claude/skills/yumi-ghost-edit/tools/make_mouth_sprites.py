#!/usr/bin/env python3
"""Build lip-sync sprites (v_closed/half/open/wide/o/frown/blink.png) from a 3x2 expression sheet.

usage: python3 -I make_mouth_sprites.py sheet.png out_dir [--cell 512]

The sheet must be RGBA (real transparency), 3 columns x 2 rows, same pose in every cell:
  1 smile/closed  2 open  3 laughing (eyes closed)
  4 small "o"     5 wink  6 frown
Cells are registered to cell 1 (affine ECC), then only the mouth / eyes are lifted from each cell
and pasted onto a clean copy of cell 1 (original features in-painted with skin), so the body never jumps.
Tune MOUTH / EYES ellipses (cx, cy, rx, ry in cell pixels) if a new character's face sits elsewhere.
"""
import sys
import numpy as np, cv2
from PIL import Image

MOUTH = [(256, 322, 62, 44)]
EYES = [(190, 232, 52, 58), (336, 242, 52, 58)]


def main():
    sheet, out = sys.argv[1], sys.argv[2]
    cs = int(sys.argv[sys.argv.index("--cell") + 1]) if "--cell" in sys.argv else 512
    a = np.array(Image.open(sheet).convert("RGBA"))
    cells = [a[r * cs:(r + 1) * cs, c * cs:(c + 1) * cs] for r in range(2) for c in range(3)]
    g = [cv2.cvtColor(np.ascontiguousarray(c[..., :3]), cv2.COLOR_RGB2GRAY).astype(np.float32) / 255 for c in cells]
    W = [cells[0].astype(np.float32)]
    for i in range(1, 6):
        M = np.eye(2, 3, dtype=np.float32)
        _, M = cv2.findTransformECC(g[0], g[i], M, cv2.MOTION_AFFINE,
                                    (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6), None, 5)
        W.append(cv2.warpAffine(cells[i], M, (cs, cs), flags=cv2.INTER_CUBIC + cv2.WARP_INVERSE_MAP).astype(np.float32))
    base = W[0]
    skin = base[int(cs * 0.556), cs // 2, :3].copy()

    def region(shapes):
        m = np.zeros((cs, cs), np.uint8)
        for cx, cy, ax, ay in shapes:
            cv2.ellipse(m, (cx, cy), (ax, ay), 0, 0, 360, 255, -1)
        return m

    def feat(img, reg):
        d = np.linalg.norm(img[..., :3] - skin, axis=2)
        al = cv2.dilate(np.clip((d - 18) / 40, 0, 1) * (reg > 0), np.ones((3, 3)))
        return cv2.GaussianBlur(al, (0, 0), 1.0)[..., None]

    def clean(img, reg):
        m = cv2.dilate(((feat(img, reg)[..., 0] > 0.05) * 255).astype(np.uint8), np.ones((7, 7)))
        out_ = img.copy()
        out_[..., :3] = cv2.inpaint(np.clip(img[..., :3], 0, 255).astype(np.uint8), m, 7, cv2.INPAINT_TELEA)
        return out_

    def put(dst, src, reg, sy=1.0, ay=0):
        al, s = feat(src, reg), src
        if sy != 1.0:
            M = np.float32([[1, 0, 0], [0, sy, ay * (1 - sy)]])
            s = cv2.warpAffine(src, M, (cs, cs), flags=cv2.INTER_CUBIC)
            al = cv2.warpAffine(al[..., 0], M, (cs, cs))[..., None]
        o = dst.copy(); o[..., :3] = dst[..., :3] * (1 - al) + s[..., :3] * al
        return o

    mr, er = region(MOUTH), region(EYES)
    bm, be = clean(base, mr), clean(base, er)
    v = {"closed": base, "half": put(bm, W[1], mr, 0.55, MOUTH[0][1] - 22), "open": put(bm, W[1], mr),
         "wide": put(bm, W[2], mr), "o": put(bm, W[3], mr), "frown": put(bm, W[5], mr), "blink": put(be, W[2], er)}
    import os
    os.makedirs(out, exist_ok=True)
    for k, x in v.items():
        Image.fromarray(np.clip(x, 0, 255).astype(np.uint8)).save(os.path.join(out, f"v_{k}.png"))
    print("wrote", ", ".join(f"v_{k}.png" for k in v))


if __name__ == "__main__":
    main()
