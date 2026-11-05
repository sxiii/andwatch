# NIXIE-01 Dynamic — Wear OS / Galaxy Watch 8 Classic

This repository includes a GitHub Actions workflow that builds the Android APK on GitHub-hosted Ubuntu runners.

## GitHub Actions build

1. Create a GitHub repository and push this project to it.
2. Open the repository's **Actions** tab.
3. The **Build NIXIE-01** workflow runs on every push and pull request. You can also start it manually with **Run workflow**.
4. Open a successful workflow run and download the `NIXIE-01-Dynamic-debug` artifact.
5. Extract the artifact ZIP to get the APK.

No local Android SDK or Android Studio is required for CI.

## Local build (optional)

Requires JDK 17, Android SDK 36 and Gradle 8.13:

```bash
gradle --no-daemon :app:assembleDebug
```

## Current prototype status

- WFF resource-only Android project structure
- Nixie-inspired background and digit assets
- Animated flicker overlay asset
- GitHub Actions CI build and APK artifact upload

**Important:** CI packaging success does not by itself prove that the watch face XML passes the official Watch Face Format validator or that every visual element renders as intended on a physical Galaxy Watch 8 Classic. The WFF XML still needs schema validation and on-device testing. This is an early development prototype, not a Play Store-ready release.
