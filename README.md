# kajet-public

The public site of Kajet (served at https://haker.dev/kajet-public/): a landing page, the privacy policy and the support page in 13 languages — `pl/`, `en/`, `de/`, `fr/`, `es/`, `it/`, `ja/`, `zh/`, `sv/`, `no/` (Bokmål), `cs/`, `sk/`, `pt/` (European Portuguese). The pages at the root only send the browser to its language (and list all of them).

Everything is generated; do not edit the HTML by hand.

```bash
python3 -m pip install Pillow            # one-time, only for the screenshots
python3 tools/build.py                   # pages and stylesheet
python3 tools/build.py --shots ../kajet-ios/fastlane/screenshots   # also refresh the store posters on the landing pages
```

- Texts: `tools/content_*.py` (one dict per language, the same structure in all of them — edit all thirteen when the meaning changes, and bump the "updated" date of the privacy policy and the support page).
- Landing page copy: the 16 features in four groups are in `tools/features_short.py`, the short interface strings (chips, headings, language text) in `tools/ui.py`.
- Layout and styles: `tools/build.py`. Fonts and the icon: `assets/`.
- The privacy policy must stay in step with what the app does (Firebase Analytics and Crashlytics, no account, on-device AI) and with the App Privacy answers in App Store Connect.
- The App Store listing links to `<lang>/privacy.html` and `<lang>/support.html` (`fastlane/metadata` in kajet-ios).
