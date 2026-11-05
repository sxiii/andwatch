#!/usr/bin/env python3
"""Generate the Matrix-rain bitmap glyphs used by the WFF BitmapFont."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

OUT = Path("app/src/main/res/drawable-nodpi")
OUT.mkdir(parents=True, exist_ok=True)
W, H = 96, 72
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
mono_path = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

for digit in range(10):
    # Make a bold, squared numeral mask, deliberately wide for a watch display.
    font = ImageFont.truetype(font_path, 120)
    probe = Image.new("L", (1, 1))
    box = ImageDraw.Draw(probe).textbbox((0, 0), str(digit), font=font)
    glyph = Image.new("L", (box[2] - box[0], box[3] - box[1]), 0)
    ImageDraw.Draw(glyph).text((-box[0], -box[1]), str(digit), font=font, fill=255)
    glyph = glyph.resize((W - 8, H - 6), Image.Resampling.LANCZOS)
    mask = Image.new("L", (W, H), 0)
    mask.paste(glyph, ((W - glyph.width) // 2, (H - glyph.height) // 2))

    # Vertical streams of binary glyphs clipped to the numeral silhouette.
    rain = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rain)
    tiny = ImageFont.truetype(mono_path, 9)
    random.seed(900 + digit)
    for x in range(1, W - 2, 9):
        y = random.randrange(-14, 2)
        while y < H:
            rd.text((x, y), random.choice("01"), font=tiny,
                    fill=(75, 255, 105, random.randrange(150, 255)))
            y += random.randrange(9, 15)

    solid = Image.new("RGBA", (W, H), (0, 230, 48, 255))
    solid.putalpha(mask)
    rain = Image.alpha_composite(solid, rain)
    rain.putalpha(mask)

    # Subtle neon halo, then a crisp pale-green highlight.
    halo = mask.filter(ImageFilter.GaussianBlur(5))
    glow = Image.new("RGBA", (W, H), (0, 255, 45, 0))
    glow.putalpha(halo.point(lambda p: p * 3 // 4))
    result = Image.alpha_composite(glow, rain)
    edge = mask.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.GaussianBlur(0.6))
    highlight = Image.new("RGBA", (W, H), (170, 255, 180, 0))
    highlight.putalpha(edge.point(lambda p: min(255, p * 2)))
    result = Image.alpha_composite(result, highlight)
    result.save(OUT / f"matrix_{digit}.png", optimize=True)
