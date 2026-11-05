# Matrix Digital — Wear OS / Galaxy Watch 8 Classic

A resource-only Watch Face Format project for Wear OS 6.

## Design

- Huge Matrix-inspired green digits, arranged vertically as HH / MM / SS.
- 24-hour time for hours; minutes and seconds update live.
- Black background with no labels or decorative text.
- Matrix-rain bitmap glyphs are generated during CI from `tools/generate_matrix_digits.py`.
- Dimmed bitmap font variants are provided for ambient mode.

## Build and validation

GitHub Actions runs Google's official Watch Face Format XML validator (schema version 4) before building the debug APK. It then packages the generated digit assets and uploads the APK as the `Matrix-Digital-WearOS-debug` artifact.

Open the repository's Actions tab, select the latest successful run, and download that artifact.

## Important testing note

A successful schema validation and APK build confirm the XML/resource package, but do not prove exact typography sizing or rendering on a physical Galaxy Watch 8 Classic. Install the APK and check active and ambient modes on the watch; adjust the three font sizes if the renderer scales bitmap glyphs differently than expected.
