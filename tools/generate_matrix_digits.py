#!/usr/bin/env python3
"""Generate Huge Digital resources and WFF v4. Requires Pillow and DejaVu Sans."""
from pathlib import Path
import argparse
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter

THEMES = [("White", "FFFFFF"), ("Lime", "B2FF59"), ("Green", "00E676"),
          ("Cyan", "00E5FF"), ("Blue", "448AFF"), ("Violet", "B388FF"),
          ("Pink", "FF80AB"), ("Red", "FF5252"), ("Orange", "FFAB40"),
          ("Yellow", "FFFF00")]
SLOTS = [(35, 18, 190, 205), (225, 18, 190, 205),
         (35, 227, 190, 205), (225, 227, 190, 205)]
SECONDS = [(307, 312, 25, 40), (334, 312, 25, 40)]
TINT = "[CONFIGURATION.mainColor]"

def write_xml(root, path, node):
    path = root / path
    path.parent.mkdir(parents=True, exist_ok=True)
    ET.indent(node)
    ET.ElementTree(node).write(path, encoding="utf-8", xml_declaration=True)

def generate(root, font_path):
    out = root / "app/src/main/res/drawable-nodpi"
    out.mkdir(parents=True, exist_ok=True)
    font = ImageFont.truetype(font_path, 256)
    circle = Image.new("L", (450, 450))
    ImageDraw.Draw(circle).ellipse((6, 6, 443, 443), fill=255)
    assets = {}
    def glyph(d, w, h):
        b = font.getbbox(str(d))
        mask = Image.new("L", (b[2]-b[0], b[3]-b[1]))
        ImageDraw.Draw(mask).text((-b[0], -b[1]), str(d), font=font, fill=255)
        result = Image.new("L", (w, h))
        result.paste(mask.resize((w-8, h-6), Image.Resampling.LANCZOS), (4, 3))
        return result
    def save(name, mask):
        image = Image.new("RGBA", mask.size, "white")
        image.putalpha(mask)
        image.save(out / (name + ".png"), optimize=True)
        assets[name] = mask
    for slot, (x, y, w, h) in enumerate(SLOTS):
        for digit in range(10):
            mask = ImageChops.multiply(glyph(digit, w, h), circle.crop((x, y, x+w, y+h)))
            save(f"huge_{slot}_{digit}_active", mask)
            save(f"huge_{slot}_{digit}_ambient", ImageChops.subtract(mask, mask.filter(ImageFilter.MinFilter(5))))
    for digit in range(10):
        save(f"seconds_{digit}", glyph(digit, 25, 40))

    face = ET.Element("WatchFace", width="450", height="450")
    settings = ET.SubElement(face, "UserConfigurations")
    colors = ET.SubElement(settings, "ColorConfiguration", id="mainColor",
                           displayName="color_selector", defaultValue="0")
    strings = ET.Element("resources")
    ET.SubElement(strings, "string", name="color_selector").text = "Main color"
    for index, (name, color) in enumerate(THEMES):
        ET.SubElement(colors, "ColorOption", id=str(index),
                      displayName=f"theme_{index}", colors="#FF" + color)
        ET.SubElement(strings, "string", name=f"theme_{index}").text = name
    write_xml(root, "app/src/main/res/values/color_themes.xml", strings)
    scene = ET.SubElement(face, "Scene", backgroundColor="#FF000000")
    def choices(name, box, expressions, resource, ambient=False, seconds=False):
        cond = ET.SubElement(scene, "Condition")
        exprs = ET.SubElement(cond, "Expressions")
        for d, expression in enumerate(expressions):
            ET.SubElement(exprs, "Expression", name=f"d{d}").text = expression
        for d in range(len(expressions)):
            compare = ET.SubElement(cond, "Compare", expression=f"d{d}")
            x, y, w, h = box
            attrs = dict(name=f"{name}_{d}", x=str(x), y=str(y), width=str(w), height=str(h),
                         tintColor="#FF646464" if ambient else TINT,
                         alpha="0" if ambient else "255")
            if seconds:
                attrs["blendMode"] = "DIFFERENCE"
            part = ET.SubElement(compare, "PartImage", **attrs)
            ET.SubElement(part, "Image", resource=resource(d))
            ET.SubElement(part, "Variant", mode="AMBIENT", target="alpha",
                          value="255" if ambient else "0")
    for slot, box in enumerate(SLOTS):
        source = "[HOUR_0_23]" if slot < 2 else "[MINUTE]"
        if slot % 2 == 0:
            expressions = [f"{source} >= {d*10} && {source} < {(d+1)*10}"
                           for d in range(3 if slot == 0 else 6)]
        else:
            expressions = [f"({source} % 10) == {d}" for d in range(10)]
        for mode in ("active", "ambient"):
            choices(f"slot_{slot}_{mode}", box, expressions,
                    lambda d, s=slot, m=mode: f"huge_{s}_{d}_{m}", ambient=mode == "ambient")
    for slot, box in enumerate(SECONDS):
        source = "SECOND_TENS_DIGIT" if slot == 0 else "SECOND_UNITS_DIGIT"
        choices(f"seconds_{slot}", box,
                [f"[{source}] == {d}" for d in range(6 if slot == 0 else 10)],
                lambda d: f"seconds_{d}", seconds=True)
    write_xml(root, "app/src/main/res/raw/watchface.xml", face)

    def preview(hours, minutes, seconds, color, ambient=False):
        color = tuple(bytes.fromhex(color)) if not ambient else (100, 100, 100)
        canvas = Image.new("RGB", (450, 450))
        for slot, d in enumerate(f"{hours:02d}{minutes:02d}"):
            x, y, w, h = SLOTS[slot]
            canvas.paste(Image.new("RGB", (w, h), color), (x, y),
                         assets[f"huge_{slot}_{d}_{'ambient' if ambient else 'active'}"])
        if not ambient:
            for slot, d in enumerate(f"{seconds:02d}"):
                x, y, w, h = SECONDS[slot]
                region = canvas.crop((x, y, x+w, y+h))
                inverse = ImageChops.difference(region, Image.new("RGB", region.size, color))
                canvas.paste(Image.composite(inverse, region, assets[f"seconds_{d}"]), (x, y))
        return canvas
    design = root / "design"
    design.mkdir(exist_ok=True)
    for name, color in THEMES:
        preview(8, 58, 37, color).save(design / (name.lower() + ".png"))
    for h, m, s in [(0, 0, 0), (11, 11, 11), (23, 59, 59)]:
        preview(h, m, s, "FFFFFF").save(design / f"time-{h:02d}{m:02d}{s:02d}.png")
    preview(8, 58, 37, "FFFFFF", True).save(design / "ambient.png")
    drawable = root / "app/src/main/res/drawable"
    drawable.mkdir(parents=True, exist_ok=True)
    preview(8, 58, 37, "FFFFFF").save(drawable / "preview.png")
    return face, assets

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--font", default="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    args = parser.parse_args()
    generate(args.root, args.font)
