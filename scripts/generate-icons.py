#!/usr/bin/env python3
"""FocusToma 앱 아이콘 생성 (플랫 토마토 + 시계)."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
ICONS_DIR = ROOT / "icons"

# 브랜드 색
BG = "#0B0B0F"
TOMATO = "#E63946"
TOMATO_LIGHT = "#FF5C68"
TOMATO_DARK = "#C42F3A"
STEM = "#2D6A4F"
RING_TRACK = "#2A2A36"
HANDS = "#FAFAFA"
CENTER_DOT = "#E8E8EC"

# 홈 화면 · PWA · iOS · Android · 스토어
ICON_SIZES = [
    16,
    32,
    48,
    72,
    96,
    128,
    144,
    152,
    167,
    180,
    192,
    256,
    384,
    512,
    1024,
]


def rounded_rect(draw: ImageDraw.ImageDraw, box, radius, fill):
    x0, y0, x1, y1 = box
    r = radius
    draw.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=fill)


def polar(cx: float, cy: float, length: float, deg_from_up: float) -> tuple[float, float]:
    rad = math.radians(deg_from_up)
    return cx + length * math.sin(rad), cy - length * math.cos(rad)


def draw_icon(size: int, *, maskable: bool = False) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    scale = 0.72 if maskable else 1.0
    margin = int(size * (1 - scale) / 2)
    s = size - margin * 2
    ox, oy = margin, margin

    corner = int(s * 0.22)
    rounded_rect(draw, (ox, oy, ox + s - 1, oy + s - 1), corner, BG)

    cx = ox + s / 2
    cy = oy + s / 2 + s * 0.04
    ring_r = s * 0.38
    tomato_r = s * 0.26

    ring_w = max(2, int(s * 0.055))

    # 시계 트랙
    draw.ellipse(
        [cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r],
        outline=RING_TRACK,
        width=ring_w,
    )

    # 토마토 몸통
    ty = cy + s * 0.02
    draw.ellipse(
        [cx - tomato_r, ty - tomato_r, cx + tomato_r, ty + tomato_r],
        fill=TOMATO,
    )
    hl_r = tomato_r * 0.35
    draw.ellipse(
        [cx - tomato_r * 0.55, ty - tomato_r * 0.95, cx - tomato_r * 0.55 + hl_r, ty - tomato_r * 0.95 + hl_r],
        fill=TOMATO_LIGHT,
    )
    draw.ellipse(
        [cx - tomato_r * 0.15, ty + tomato_r * 0.55, cx + tomato_r * 0.55, ty + tomato_r * 0.95],
        fill=TOMATO_DARK,
    )

    # 줄기
    stem_w = max(2, int(s * 0.07))
    stem_h = int(s * 0.09)
    draw.rounded_rectangle(
        [cx - stem_w, ty - tomato_r - stem_h + 2, cx + stem_w, ty - tomato_r + 4],
        radius=stem_w,
        fill=STEM,
    )
    leaf_w = int(s * 0.06)
    draw.ellipse(
        [cx + stem_w - 2, ty - tomato_r - stem_h, cx + stem_w + leaf_w, ty - tomato_r - stem_h // 2],
        fill=STEM,
    )

    # 진행 호 (집중 링)
    bbox = [cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r]
    draw.arc(bbox, start=200, end=340, fill=TOMATO, width=ring_w)

    # 시침·분침 (10:10 — 아이콘에 잘 어울리는 대칭)
    hand_w = max(2, int(s * 0.045))
    hour_len = ring_r * 0.42
    minute_len = ring_r * 0.58
    hx, hy = polar(cx, cy, hour_len, -52)
    mx, my = polar(cx, cy, minute_len, 52)
    draw.line([(cx, cy), (hx, hy)], fill=HANDS, width=hand_w)
    draw.line([(cx, cy), (mx, my)], fill=HANDS, width=hand_w)

    dot_r = max(2, int(s * 0.028))
    draw.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r], fill=CENTER_DOT)

    return img


def main():
    ICONS_DIR.mkdir(parents=True, exist_ok=True)

    for size in ICON_SIZES:
        path = ICONS_DIR / f"icon-{size}.png"
        draw_icon(size).convert("RGB").save(path, "PNG", optimize=True)
        print(f"  {path.name}")

    mask_path = ICONS_DIR / "icon-512-maskable.png"
    draw_icon(512, maskable=True).convert("RGB").save(mask_path, "PNG", optimize=True)
    print(f"  {mask_path.name}")

    # 스토어·iOS 관용 별칭
    aliases = {
        "apple-touch-icon.png": 180,
        "favicon-32.png": 32,
        "favicon-16.png": 16,
        "play-store-icon.png": 512,
        "app-store-icon.png": 1024,
    }
    for name, size in aliases.items():
        src = ICONS_DIR / f"icon-{size}.png"
        dst = ICONS_DIR / name
        if src.exists():
            dst.write_bytes(src.read_bytes())
            print(f"  {name} (from icon-{size}.png)")

    print("Done.")


if __name__ == "__main__":
    main()
