#!/usr/bin/env python3
"""Builds the static site: <lang>/{index,privacy,support}.html for eight languages, the language
pickers at the root, the stylesheet and the images. Texts live in tools/content_*.py.

Usage (from the repo root):  python3 tools/build.py [--shots ../kajet-ios/fastlane/screenshots]
Needs Pillow only for the screenshots (`python3 -m pip install Pillow`); without --shots they are kept as they are.
"""
import html
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from content_de_fr import DE, FR  # noqa: E402
from content_en_pl import EN, PL  # noqa: E402
from content_es_it import ES, IT  # noqa: E402
from content_ja_zh import JA, ZH  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
LANGS = [PL, EN, DE, FR, ES, IT, JA, ZH]
MAIL = "kontakt@ideaapps.io"
APP_STORE = "https://apps.apple.com/app/id6814474214"
# fastlane screenshot folder per site folder, and which frames the landing page shows
SHOT_FOLDERS = {"pl": "pl", "en": "en-US", "de": "de-DE", "fr": "fr-FR", "es": "es-ES", "it": "it", "ja": "ja", "zh": "zh-Hans"}
SHOT_FILES = ["01_dashboard", "02_study", "03_stats", "06_plan", "07_subjects", "08_tasks"]

STYLE = """\
@font-face{font-family:"Plus Jakarta Sans";font-weight:400;font-display:swap;src:url(fonts/PlusJakartaSans-Regular.ttf) format("truetype")}
@font-face{font-family:"Plus Jakarta Sans";font-weight:700;font-display:swap;src:url(fonts/PlusJakartaSans-Bold.ttf) format("truetype")}
@font-face{font-family:"Plus Jakarta Sans";font-weight:800;font-display:swap;src:url(fonts/PlusJakartaSans-ExtraBold.ttf) format("truetype")}
:root{color-scheme:light dark;--bg:#F3F2F9;--card:#FFFFFF;--ink:#18162C;--soft:#6C6987;--accent:#4F46E5;--border:#E4E1F1;--on:#FFFFFF;--tint:#ECEAFB}
@media (prefers-color-scheme:dark){:root{--bg:#131223;--card:#1C1B30;--ink:#F5F4FB;--soft:#A6A3BE;--accent:#8B85F5;--border:#2C2A45;--on:#131223;--tint:#26244A}}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Plus Jakarta Sans",-apple-system,BlinkMacSystemFont,"Segoe UI","Hiragino Sans","PingFang SC","Noto Sans CJK SC","Helvetica Neue",Arial,sans-serif;font-size:17px;line-height:1.6}
.wrap{max-width:820px;margin:0 auto;padding:24px 20px 56px}
nav{display:flex;gap:6px 20px;flex-wrap:wrap;align-items:center;margin-bottom:40px;font-weight:700;font-size:16px}
nav a{color:var(--ink);text-decoration:none}nav a:hover,nav a[aria-current]{color:var(--accent)}
nav .brand{margin-right:auto;font-size:21px;font-weight:800;display:flex;align-items:center;gap:10px}
nav .brand img{width:34px;height:34px;border-radius:9px}
.langs{position:relative}
.langs summary{cursor:pointer;list-style:none;color:var(--soft);font-weight:700;font-size:15px;padding:4px 0}
.langs summary::-webkit-details-marker{display:none}
.langs summary::after{content:" ▾"}
.langs ul{position:absolute;right:0;top:100%;z-index:5;margin:6px 0 0;padding:6px;list-style:none;background:var(--card);border:1px solid var(--border);border-radius:14px;min-width:170px;box-shadow:0 10px 30px rgba(24,22,44,.14)}
@media (max-width:560px){.langs{width:100%}.langs ul{position:static;box-shadow:none}}
.langs li a{display:block;padding:7px 12px;border-radius:9px;font-weight:600}
.langs li a:hover,.langs li a[aria-current]{background:var(--tint);color:var(--accent)}
h1{font-size:clamp(30px,6.6vw,46px);line-height:1.12;margin:0 0 14px;font-weight:800;letter-spacing:-.015em;text-wrap:balance}
.hero h1{color:var(--accent)}
h2{font-size:20px;font-weight:800;margin:34px 0 8px}
p,li{color:var(--ink)}p{margin:0 0 14px}ul{padding-left:22px;margin:0 0 14px}li{margin-bottom:6px}
.lead{font-size:19px;color:var(--soft);margin:0 0 26px;max-width:640px}
.updated{font-size:13px;font-weight:700;color:var(--soft);margin:0 0 26px}
.callout,.card,details.q{background:var(--card);border:1px solid var(--border);border-radius:18px}
.callout{padding:18px 20px;margin:0 0 24px}.callout strong{color:var(--accent)}
a{color:var(--accent)}
.btns{display:flex;gap:12px;flex-wrap:wrap;margin:0 0 30px}
.btn{display:inline-block;padding:13px 26px;border-radius:999px;background:var(--accent);color:var(--on);font-weight:700;text-decoration:none}
.btn.ghost{background:var(--card);color:var(--ink);border:1px solid var(--border)}
.shots{display:flex;gap:14px;overflow-x:auto;padding:4px 0 16px;margin:0 -20px 26px;padding-inline:20px;scroll-snap-type:x mandatory}
.shots img{height:440px;width:auto;border-radius:22px;scroll-snap-align:start;flex:none}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));margin:0 0 28px}
.card{padding:18px 20px}.card h3{margin:0 0 6px;font-size:17px;font-weight:800;color:var(--accent)}.card p{margin:0;color:var(--soft);font-size:15px}
.note{font-size:14px;color:var(--soft)}
.faq h3{font-size:16px;font-weight:800;margin:22px 0 6px}.faq p{margin:0 0 10px}
footer{margin-top:46px;color:var(--soft);font-size:13px;display:flex;gap:6px 18px;flex-wrap:wrap}footer a{color:var(--soft)}
.pick{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));margin:24px 0}
.pick a{display:block;padding:16px 18px;border-radius:16px;background:var(--card);border:1px solid var(--border);color:var(--ink);text-decoration:none;font-weight:700}
.pick a:hover{border-color:var(--accent);color:var(--accent)}.pick small{display:block;color:var(--soft);font-weight:600;font-size:13px}
"""

ROOT_SCRIPT = """\
<script>
(function(){
  var map={pl:'pl',en:'en',de:'de',fr:'fr',es:'es',it:'it',ja:'ja',zh:'zh'};
  var list=navigator.languages||[navigator.language||'en'];
  var folder='en';
  for(var i=0;i<list.length;i++){var c=String(list[i]).toLowerCase().split('-')[0];if(map[c]){folder=map[c];break;}}
  location.replace(folder+'/%s');
})();
</script>"""


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def fill(text: str, lang: dict, page: str = "") -> str:
    return text.replace("{mail}", MAIL).replace("{privacy}", "privacy.html").replace("{support}", "support.html")


def head(lang: dict, page: str, title: str, description: str, depth: str = "../") -> str:
    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{l["code"]}" href="../{l["folder"]}/{page}">' for l in LANGS)
    return f"""<!doctype html>
<html lang="{lang['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{html.escape(description)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:image" content="https://haker.dev/kajet-public/assets/icon.png">
<link rel="icon" href="{depth}assets/icon.png">
<link rel="stylesheet" href="{depth}assets/style.css">
{alternates}
<link rel="alternate" hreflang="x-default" href="../en/{page}">
</head>
<body>
<div class="wrap">
"""


def nav(lang: dict, page: str) -> str:
    items = "".join(
        f'<li><a href="../{l["folder"]}/{page}" hreflang="{l["code"]}" lang="{l["html_lang"]}"'
        f'{" aria-current=page" if l is lang else ""}>{esc(l["label"])}</a></li>' for l in LANGS)
    cur = lambda p: ' aria-current="page"' if page == p else ""
    return (f'<nav><a class="brand" href="index.html"><img src="../assets/icon.png" alt="">Kajet</a>'
            f'<a href="privacy.html"{cur("privacy.html")}>{esc(lang["nav_privacy"])}</a>'
            f'<a href="support.html"{cur("support.html")}>{esc(lang["nav_support"])}</a>'
            f'<details class="langs"><summary>{esc(lang["label"])}</summary><ul>{items}</ul></details></nav>\n')


def footer(lang: dict) -> str:
    return (f'<footer><span>{lang["footer_rights"]}</span>'
            f'<a href="privacy.html">{esc(lang["nav_privacy"])}</a><a href="support.html">{esc(lang["nav_support"])}</a></footer>\n'
            "</div>\n</body>\n</html>\n")


def blocks_html(lang: dict, blocks) -> str:
    out = []
    for kind, value in blocks:
        if kind == "callout":
            out.append(f'<div class="callout">{fill(value, lang)}</div>')
        elif kind == "h2":
            out.append(f"<h2>{esc(value)}</h2>")
        elif kind == "p":
            out.append(f"<p>{fill(value, lang)}</p>")
        elif kind == "ul":
            out.append("<ul>" + "".join(f"<li>{fill(v, lang)}</li>" for v in value) + "</ul>")
        elif kind == "faq":
            out.append('<div class="faq">' + "".join(
                f"<h3>{esc(q)}</h3><p>{fill(a, lang)}</p>" for q, a in value) + "</div>")
    return "\n".join(out) + "\n"


def index_page(lang: dict) -> str:
    c = lang["index"]
    shots = "".join(
        f'<img src="../assets/shots/{lang["folder"]}-{i}.jpg" alt="Kajet {i}" loading="lazy" width="440" height="956">'
        for i in range(1, len(SHOT_FILES) + 1))
    cards = "".join(f'<div class="card"><h3>{esc(t)}</h3><p>{esc(p)}</p></div>' for t, p in c["cards"])
    return (head(lang, "index.html", c["title"], c["description"]) + nav(lang, "index.html") +
            f'<div class="hero"><h1>{esc(c["h1"])}</h1><p class="lead">{esc(c["lead"])}</p>\n'
            f'<div class="btns"><a class="btn" href="{APP_STORE}">{esc(c["download"])}</a>'
            f'<a class="btn ghost" href="support.html">{esc(c["support_btn"])}</a>'
            f'<a class="btn ghost" href="privacy.html">{esc(c["privacy_btn"])}</a></div></div>\n'
            f'<div class="shots">{shots}</div>\n<div class="grid">{cards}</div>\n'
            f'<p class="note">{esc(c["note"])}</p>\n' + footer(lang))


def text_page(lang: dict, kind: str) -> str:
    c = lang[kind]
    page = f"{kind}.html"
    return (head(lang, page, f'{c["title"]} · Kajet', c["description"]) + nav(lang, page) +
            f'<h1>{esc(c["h1"])}</h1><p class="updated">{esc(c["updated"])}</p>\n' +
            blocks_html(lang, c["blocks"]) + footer(lang))


def picker(page: str, titles: dict) -> str:
    """A root page: sends the browser to its language, and lists all of them for anyone else."""
    links = "".join(
        f'<a href="{l["folder"]}/{page}" hreflang="{l["code"]}" lang="{l["html_lang"]}">{esc(l["label"])}'
        f'<small>{esc(titles[l["code"]])}</small></a>' for l in LANGS)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kajet</title>
<meta name="description" content="Kajet: a student planner for iPhone. Choose your language.">
<link rel="icon" href="assets/icon.png">
<link rel="stylesheet" href="assets/style.css">
{ROOT_SCRIPT % page}
</head>
<body>
<div class="wrap">
<nav><a class="brand" href="index.html"><img src="assets/icon.png" alt="">Kajet</a></nav>
<h1>Kajet</h1>
<p class="lead">Polski · English · Deutsch · Français · Español · Italiano · 日本語 · 简体中文</p>
<div class="pick">{links}</div>
</div>
</body>
</html>
"""


def build_shots(shots_dir: Path) -> None:
    from PIL import Image
    out = ROOT / "assets" / "shots"
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("*.jpg"):
        old.unlink()
    for folder, source in SHOT_FOLDERS.items():
        for i, name in enumerate(SHOT_FILES, start=1):
            path = shots_dir / source / f"{name}.png"
            if not path.exists():
                print("missing", path)
                continue
            Image.open(path).convert("RGB").resize((440, 956), Image.LANCZOS).save(
                out / f"{folder}-{i}.jpg", "JPEG", quality=82, optimize=True, progressive=True)


def main() -> None:
    assets = ROOT / "assets"
    (assets / "fonts").mkdir(parents=True, exist_ok=True)
    (assets / "style.css").write_text(STYLE, encoding="utf-8")
    if "--shots" in sys.argv:
        build_shots(Path(sys.argv[sys.argv.index("--shots") + 1]).resolve())
    for lang in LANGS:
        folder = ROOT / lang["folder"]
        folder.mkdir(exist_ok=True)
        (folder / "index.html").write_text(index_page(lang), encoding="utf-8")
        (folder / "privacy.html").write_text(text_page(lang, "privacy"), encoding="utf-8")
        (folder / "support.html").write_text(text_page(lang, "support"), encoding="utf-8")
    (ROOT / "index.html").write_text(picker("index.html", {l["code"]: l["nav_home"] for l in LANGS}), encoding="utf-8")
    (ROOT / "privacy.html").write_text(picker("privacy.html", {l["code"]: l["nav_privacy"] for l in LANGS}), encoding="utf-8")
    (ROOT / "support.html").write_text(picker("support.html", {l["code"]: l["nav_support"] for l in LANGS}), encoding="utf-8")
    print("built", len(LANGS), "languages")


if __name__ == "__main__":
    main()
