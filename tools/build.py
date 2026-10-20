#!/usr/bin/env python3
"""Builds the static site: <lang>/{index,privacy,support}.html for thirteen languages, the language
pickers at the root, the stylesheet and the images. Texts live in tools/content_*.py, the landing page's
feature list in tools/features_short.py and its short UI strings in tools/ui.py.

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
from content_cs_sk import CS, SK  # noqa: E402
from content_pt import PT  # noqa: E402
from content_sv_no import NO, SV  # noqa: E402
from features_short import FEATURES  # noqa: E402
from ui import UI  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
LANGS = [PL, EN, DE, FR, ES, IT, JA, ZH, SV, NO, CS, SK, PT]
MAIL = "kontakt@ideaapps.io"
APP_STORE = "https://apps.apple.com/app/id6814474214"
# framed store screenshot folder (kajet-ios/fastlane/screenshots) per site folder
SHOT_FOLDERS = {"pl": "pl", "en": "en-US", "de": "de-DE", "fr": "fr-FR", "es": "es-ES", "it": "it", "ja": "ja",
                "zh": "zh-Hans", "sv": "sv", "no": "no", "cs": "cs", "sk": "sk", "pt": "pt-PT"}
# the store posters the page shows, cropped to 4:5 (headline and the top of the phone): hero pair, then a row of three
HERO_SHOTS = ("01_dashboard", "06_plan")
ROW_SHOTS = ("07_subjects", "02_study", "03_stats")
SHOT_W, SHOT_H = 640, 800
GROUP_COLORS = ["#0EA5E9", "#DB2777", "#16A34A", "#7C3AED"]
ICONS = [  # one per feature, in the order of features_short.py
    '<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    '<path d="M7 7h12l-3-3M17 17H5l3 3"/>',
    '<circle cx="12" cy="7" r="3"/><path d="M6 21v-3a6 6 0 0112 0v3"/>',
    '<rect x="3" y="3" width="8" height="8" rx="2"/><rect x="13" y="3" width="8" height="8" rx="2"/><rect x="3" y="13" width="8" height="8" rx="2"/><circle cx="17" cy="17" r="4"/>',
    '<path d="M4 20v-7M10 20V5M16 20v-10M22 20H2"/>',
    '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
    '<path d="M2 9l10-5 10 5-10 5L2 9z"/><path d="M6 11.5V16c0 1.5 3 3 6 3s6-1.5 6-3v-4.5"/>',
    '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/>',
    '<rect x="4" y="3" width="16" height="18" rx="3"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    '<path d="M6 16V11a6 6 0 0112 0v5l2 2H4l2-2z"/><path d="M10 21h4"/>',
    '<circle cx="12" cy="13" r="8"/><path d="M12 9v4l3 2M9 2h6"/>',
    '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8L12 3z"/>',
    '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0014 0M12 18v3"/>',
    '<path d="M12 3l9 5-9 5-9-5 9-5z"/><path d="M3 13l9 5 9-5"/>',
    '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
]

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
.home .wrap{max-width:1080px}
.home{--shadow:0 24px 50px -22px rgba(36,31,115,.38)}
.hero{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center;padding:8px 0 64px}
.hero>*{min-width:0}
.hero h1{font-size:clamp(34px,4.8vw,54px);line-height:1.07;letter-spacing:-.02em;margin:0 0 18px}
.hero .lead{font-size:19px;max-width:30em;margin:0 0 28px}
.hero .btns{margin-bottom:22px}
.hero .btn{padding:14px 26px}
.facts{display:flex;gap:6px 18px;flex-wrap:wrap;color:var(--soft);font-size:14px;font-weight:600;margin:0;padding:0;list-style:none}
.facts li{margin:0}.facts li::before{content:"✓ ";color:var(--accent);font-weight:800}
.posters{position:relative;aspect-ratio:1/1;max-width:100%}
.posters img{position:absolute;width:62%;height:auto;border-radius:26px;box-shadow:var(--shadow)}
.posters .p1{left:0;top:10%;transform:rotate(-3deg);z-index:2}
.posters .p2{right:0;top:0;transform:rotate(4deg)}
.sec-title{font-size:clamp(26px,3.6vw,38px);line-height:1.15;font-weight:800;letter-spacing:-.015em;margin:0 0 30px;text-wrap:balance}
.band{padding-top:72px}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;margin:0}
.grp{background:var(--card);border:1px solid var(--border);border-radius:24px;padding:26px 26px 12px}
.grp h3{margin:0 0 18px;font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--c);font-weight:800}
.grp ul{list-style:none;margin:0;padding:0}
.grp li{display:flex;gap:14px;padding:13px 0;margin:0;border-top:1px solid var(--border)}
.grp li:first-child{border-top:0;padding-top:0}
.ico{flex:none;width:40px;height:40px;border-radius:12px;display:grid;place-items:center;background:var(--tint);background:color-mix(in srgb,var(--c) 14%,transparent)}
.ico svg{width:21px;height:21px;fill:none;stroke:var(--c);stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round}
.grp b{display:block;font-size:16px;line-height:1.3}
.grp p{margin:2px 0 0;color:var(--soft);font-size:14.5px;line-height:1.45}
.trio{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.trio img{width:100%;height:auto;border-radius:24px;box-shadow:var(--shadow);display:block}
.langs-sec p{color:var(--soft);margin:-14px 0 24px;max-width:36em}
.pills{display:flex;flex-wrap:wrap;gap:8px;margin:0;padding:0;list-style:none}
.pills li{margin:0}
.pills a{display:block;padding:8px 16px;border-radius:999px;background:var(--card);border:1px solid var(--border);color:var(--ink);text-decoration:none;font-weight:700;font-size:14.5px}
.pills a:hover,.pills a[aria-current]{border-color:var(--accent);color:var(--accent);background:var(--tint)}
.cta{margin:72px 0 28px;border-radius:30px;padding:clamp(32px,6vw,56px);background:linear-gradient(135deg,#4F46E5,#6D3FD8);color:#fff;display:flex;gap:24px;align-items:center;justify-content:space-between;flex-wrap:wrap}
.cta h2{margin:0 0 4px;color:#fff;font-size:clamp(24px,3.4vw,34px);line-height:1.15;font-weight:800;letter-spacing:-.015em}
.cta p{margin:0;color:rgba(255,255,255,.86)}
.cta .btn{background:#fff;color:#2A2380}
@media (max-width:820px){
  .hero{grid-template-columns:1fr;gap:28px}.posters{max-width:420px;margin:0 auto;width:100%}
  .grid{grid-template-columns:1fr}.trio{grid-template-columns:1fr;max-width:420px;margin-inline:auto}
}
"""

ROOT_SCRIPT = """\
<script>
(function(){
  var map={pl:'pl',en:'en',de:'de',fr:'fr',es:'es',it:'it',ja:'ja',zh:'zh',sv:'sv',nb:'no',nn:'no',no:'no',cs:'cs',sk:'sk',pt:'pt'};
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


def head(lang: dict, page: str, title: str, description: str, depth: str = "../", body: str = "") -> str:
    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{l["code"]}" href="../{l["folder"]}/{page}">' for l in LANGS)
    return f"""<!doctype html>
<html lang="{lang['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#4F46E5">
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
<body{f' class="{body}"' if body else ''}>
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


def poster(lang: dict, shot: str, alt: str, cls: str = "", lazy: bool = True) -> str:
    loading = ' loading="lazy"' if lazy else ""
    return (f'<img{f" class={chr(34)}{cls}{chr(34)}" if cls else ""} src="../assets/shots/{lang["folder"]}-{shot}.jpg"'
            f' alt="{html.escape(alt)}" width="{SHOT_W}" height="{SHOT_H}"{loading}>')


def index_page(lang: dict) -> str:
    c = lang["index"]
    ui = UI[lang["folder"]]
    feats = FEATURES[lang["folder"]]
    chips = "".join(f"<li>{esc(t)}</li>" for t in ui["chips"])
    groups = []
    for g, title in enumerate(feats["groups"]):
        items = "".join(
            f'<li><span class="ico"><svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[g * 4 + i]}</svg></span>'
            f"<div><b>{esc(t)}</b><p>{esc(d)}</p></div></li>"
            for i, (t, d) in enumerate(feats["items"][g * 4:g * 4 + 4]))
        groups.append(f'<section class="grp" style="--c:{GROUP_COLORS[g]}"><h3>{esc(title)}</h3><ul>{items}</ul></section>')
    trio = "".join(poster(lang, shot, f"Kajet {i + 1}") for i, shot in enumerate(ROW_SHOTS))
    pills = "".join(
        f'<li><a href="../{l["folder"]}/index.html" hreflang="{l["code"]}" lang="{l["html_lang"]}"'
        f'{" aria-current=page" if l is lang else ""}>{esc(l["label"])}</a></li>' for l in LANGS)
    return (head(lang, "index.html", c["title"], c["description"], body="home") + nav(lang, "index.html") +
            f'<header class="hero"><div><h1>{esc(c["h1"])}</h1><p class="lead">{esc(c["lead"])}</p>\n'
            f'<div class="btns"><a class="btn" href="{APP_STORE}">{esc(c["download"])}</a>'
            f'<a class="btn ghost" href="#features">{esc(feats["see"])}</a></div>'
            f'<ul class="facts">{chips}</ul></div>'
            f'<div class="posters">{poster(lang, HERO_SHOTS[0], "Kajet", "p1", lazy=False)}{poster(lang, HERO_SHOTS[1], "Kajet", "p2", lazy=False)}</div></header>\n'
            f'<section id="features" class="band" style="padding-top:8px"><h2 class="sec-title">{esc(ui["features_title"])}</h2><div class="grid">' + "".join(groups) + "</div></section>\n"
            f'<section class="band"><h2 class="sec-title">{esc(ui["screens_title"])}</h2><div class="trio">{trio}</div></section>\n'
            f'<section class="band langs-sec"><h2 class="sec-title">{esc(ui["langs_title"])}</h2><p>{esc(ui["langs_text"])}</p><ul class="pills">{pills}</ul></section>\n'
            f'<div class="cta"><div><h2>{esc(ui["cta_title"])}</h2><p>{esc(ui["cta_text"])}</p></div>'
            f'<a class="btn" href="{APP_STORE}">{esc(c["download"])}</a></div>\n'
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
<p class="lead">{" · ".join(l["label"] for l in LANGS)}</p>
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
        for shot in HERO_SHOTS + ROW_SHOTS:
            path = shots_dir / source / f"{shot}.png"
            if not path.exists():
                print("missing", path)
                continue
            im = Image.open(path).convert("RGB")
            im = im.crop((0, 0, im.width, round(im.width * SHOT_H / SHOT_W)))
            im.resize((SHOT_W, SHOT_H), Image.LANCZOS).save(
                out / f"{folder}-{shot}.jpg", "JPEG", quality=84, optimize=True, progressive=True)


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
