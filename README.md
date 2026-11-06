# Huge Digital — Wear OS / Galaxy Watch

A resource-only Watch Face Format v4 watch face. Replaces the Matrix experiment.

## Design

- Solid, large HH above mm, fixed 24-hour clock, black background.
- Four 190 x 205 image cells in a 450 x 450 design coordinate system.
- Glyphs clipped to radius 219: a six-unit screen-edge margin.
- Seconds restored to 25 x 40 each, at (307,312) and (334,312).
- Ten editor-selectable colors: white, lime, green, cyan, blue, violet,
  pink, red, orange and yellow. White is the default.
- Seconds use the SAME selected tint with DIFFERENCE blending: black on
  colored strokes and the selected color on black. No separate rectangle.
- Ambient uses separate dim gray outlines; seconds hidden.
- App ID retained for upgrades; versionCode 2 / versionName 0.3.

## Source and build

The authoritative source is tools/generate_matrix_digits.py. It generates
PNG assets, color-label resources, watchface.xml and previews. The raw XML
remaining from the earlier experiment is overwritten before validation/build;
do not edit that generated file to change the design.

Dependencies: Python 3, Pillow, and fonts-dejavu-core (DejaVuSans-Bold.ttf).
For example on Debian/Ubuntu:

```sh
sudo apt-get install python3-venv fonts-dejavu-core
python3 -m venv .venv
. .venv/bin/activate
python -m pip install Pillow
python tools/generate_matrix_digits.py
```

The existing GitHub Actions workflow already runs this generator before
Google's WFF v4 validator and assembleDebug. Its legacy Matrix-Digital-WearOS-debug
artifact name is retained. A Gradle preBuild dependency also regenerates resources
for local builds, using python3 from PATH. Activate the virtualenv first.

The generator supports --root PATH and --font PATH. Changing the font changes
appearance. The default is /usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf.
Design previews in design/ are Pillow simulations, not Wear OS screenshots.

## Acceptance on hardware

Install the APK from a successful CI run, select Huge Digital and open its
editor to choose Main color. Check all 10 colors, 00:00, 08:58, 11:11 and 23:59,
including outer corners and seconds over both strokes and black holes.
Check ambient, wake-up, minute changes, midnight and battery use.

Local resource and expression checks are not schema validation or a device test.
Physical rendering, burn-in behavior and battery consumption remain unverified.
Legacy Nixie assets are retained; removing them is outside this change.
