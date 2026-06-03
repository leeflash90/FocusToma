#!/usr/bin/env python3
"""Play Store / PWABuilder용 스크린샷 이미지 생성."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "screenshots"

BG = "#0B0B0F"
CARD = "#1A1A24"
LINE = "#2A2A36"
TOMATO = "#E63946"
TEXT = "#FAFAFA"
MUTED = "#A1A1AA"


def try_font(size: int):
    for name in (
        "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ):
        p = Path(name)
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except OSError:
                pass
    return ImageFont.load_default()


def draw_phone_screen(draw: ImageDraw.ImageDraw, w: int, h: int, font_lg, font_md, font_sm):
    draw.rectangle([0, 0, w, h], fill=BG)
    draw.text((48, 72), "FocusToma", fill=TOMATO, font=font_lg)
    draw.rounded_rectangle([48, 140, w - 48, 220], radius=36, fill=CARD, outline=LINE, width=2)
    draw.text((72, 168), "집중  ·  짧은 휴식  ·  긴 휴식", fill=MUTED, font=font_sm)

    cx, cy = w // 2, h // 2 - 40
    r = min(w, h) // 5
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=LINE, width=8)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=TOMATO, width=8)
    draw.text((cx - 95, cy - 35), "25:00", fill=TEXT, font=font_lg)

    bw = 200
    bx = cx - bw // 2
    by = cy + r + 80
    draw.rounded_rectangle([bx, by, bx + bw, by + 56], radius=28, fill=TOMATO)
    draw.text((bx + 62, by + 14), "시작", fill=TEXT, font=font_md)

    draw.text((48, h - 200), "오늘 할 일", fill=TEXT, font=font_md)
    draw.rounded_rectangle([48, h - 150, w - 48, h - 90], radius=16, fill=CARD, outline=LINE, width=2)
    draw.text((72, h - 132), "□  보고서 작성", fill=MUTED, font=font_sm)


def draw_wide_screen(draw: ImageDraw.ImageDraw, w: int, h: int, font_lg, font_md, font_sm):
    draw.rectangle([0, 0, w, h], fill=BG)
    draw.text((40, 36), "FocusToma", fill=TOMATO, font=font_lg)

    lx = 40
    draw.ellipse([lx + 80, 120, lx + 280, 320], outline=LINE, width=6)
    draw.arc([lx + 80, 120, lx + 280, 320], 200, 340, fill=TOMATO, width=6)
    draw.text((lx + 118, 195), "25:00", fill=TEXT, font=font_lg)

    rx = w // 2 + 20
    draw.rounded_rectangle([rx, 100, w - 40, h - 40], radius=20, fill=CARD, outline=LINE, width=2)
    draw.text((rx + 24, 120), "오늘 할 일", fill=TEXT, font=font_md)
    draw.text((rx + 24, 170), "2 / 5 남음", fill=MUTED, font=font_sm)
    for i, t in enumerate(["보고서 작성", "이메일 확인", "운동 30분"]):
        draw.text((rx + 24, 220 + i * 44), f"· {t}", fill=MUTED, font=font_sm)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    font_lg = try_font(56)
    font_md = try_font(32)
    font_sm = try_font(24)

    mobile = Image.new("RGB", (1080, 1920), BG)
    draw_phone_screen(ImageDraw.Draw(mobile), 1080, 1920, try_font(72), try_font(36), try_font(28))
    mobile.save(OUT / "mobile.png", "PNG", optimize=True)

    wide = Image.new("RGB", (1280, 720), BG)
    draw_wide_screen(ImageDraw.Draw(wide), 1280, 720, try_font(48), try_font(28), try_font(22))
    wide.save(OUT / "wide.png", "PNG", optimize=True)

    print("screenshots/mobile.png, screenshots/wide.png")


if __name__ == "__main__":
    main()
