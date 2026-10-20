#!/usr/bin/env python3
"""Builds the static site: <lang>/{index,privacy,support}.html for thirteen languages, the language
pickers at the root, the stylesheet and the images. Texts live in tools/content_*.py, the landing page's
feature copy in tools/features_data.py (tools/sync_features.py) and its short UI strings in tools/ui.py.

Usage (from the repo root):  python3 tools/build.py [--shots ../kajet-ios/build/screenshots/raw]
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
from features_data import DATA as FEATURES  # noqa: E402
from ui import UI  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
LANGS = [PL, EN, DE, FR, ES, IT, JA, ZH, SV, NO, CS, SK, PT]
MAIL = "kontakt@ideaapps.io"
APP_STORE = "https://apps.apple.com/app/id6814474214"
# raw capture folder (kajet-ios/build/screenshots/raw) per site folder
SHOT_FOLDERS = {"pl": "pl", "en": "en-US", "de": "de-DE", "fr": "fr-FR", "es": "es-ES", "it": "it", "ja": "ja",
                "zh": "zh-Hans", "sv": "sv", "no": "no", "cs": "cs", "sk": "sk", "pt": "pt-PT"}
SCENES = FEATURES["scenes"]
SHOT_W, SHOT_H = 560, 1217  # the 1320x2868 capture, scaled
# landing page: which screen shows which section of the App Store description (index into FEATURES sections)
SHOWCASE = [("dashboard", 0), ("plan", 1), ("subjects", 2), ("tasks", 4), ("study", 5), ("stats", 6)]
MORE_SCREENS = ["history", "todo", "exams", "quick"]
HERO_SCREENS = ("dashboard", "plan")
ICONS = [
    '<path d="M2 9l10-5 10 5-10 5L2 9z"/><path d="M6 11.5V16c0 1.5 3 3 6 3s6-1.5 6-3v-4.5"/><path d="M22 9v6"/>',
    '<rect x="3" y="3" width="8" height="8" rx="2"/><rect x="13" y="3" width="8" height="8" rx="2"/><rect x="3" y="13" width="8" height="8" rx="2"/><circle cx="17" cy="17" r="4"/>',
    '<rect x="4" y="10" width="16" height="11" rx="3"/><path d="M8 10V7a4 4 0 018 0v3"/>',
]

STYLE = """\
@font-face{font-family:"Plus Jakarta Sans";font-weight:400;font-display:swap;src:url(fonts/PlusJakartaSans-Regular.ttf) format("truetype")}
@font-face{font-family:"Plus Jakarta Sans";font-weight:700;font-display:swap;src:url(fonts/PlusJakartaSans-Bold.ttf) format("truetype")}
@font-face{font-family:"Plus Jakarta Sans";font-weight:800;font-display:swap;src:url(fonts/PlusJakartaSans-ExtraBold.ttf) format("truetype")}
:root{color-scheme:light dark;--bg:#F3F2F9;--card:#FFFFFF;--ink:#18162C;--soft:#6C6987;--accent:#4F46E5;--border:#E4E1F1;--on:#FFFFFF;--tint:#ECEAFB;--glow:rgba(124,58,237,.28)}
@media (prefers-color-scheme:dark){:root{--bg:#131223;--card:#1C1B30;--ink:#F5F4FB;--soft:#A6A3BE;--accent:#8B85F5;--border:#2C2A45;--on:#131223;--tint:#26244A;--glow:rgba(139,133,245,.3)}}
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
.wide .wrap,.wrap.wide{max-width:1120px}
.hero{display:grid;grid-template-columns:1.05fr .95fr;gap:40px;align-items:center;margin:8px 0 56px}
.hero h1{font-size:clamp(32px,4.4vw,52px);line-height:1.08;margin-bottom:18px}
.hero .lead{font-size:20px;max-width:560px}
.hero .btns{margin-bottom:22px;flex-wrap:nowrap}.hero .btn{padding:13px 22px;white-space:nowrap}
.chips{display:flex;gap:8px 10px;flex-wrap:wrap;margin:0;padding:0;list-style:none}
.chips li{margin:0;padding:6px 13px 6px 11px;border-radius:999px;background:var(--tint);color:var(--accent);font-weight:700;font-size:14px;display:flex;align-items:center;gap:7px}
.chips li::before{content:"✓";font-weight:800}
.hero-art{position:relative;height:560px}
.hero-art::before{content:"";position:absolute;inset:6% 4% 4%;border-radius:50%;background:radial-gradient(closest-side,var(--glow),transparent 72%);filter:blur(10px)}
.hero-art .phone{position:absolute;width:262px}
.hero-art .p1{left:3%;bottom:0;transform:rotate(-4deg);z-index:2}
.hero-art .p2{right:2%;top:0;transform:rotate(5deg)}
.phone{position:relative;padding:8px;border-radius:44px;background:linear-gradient(150deg,#34344a,#0b0b12);box-shadow:0 30px 60px -18px rgba(36,31,115,.45),0 0 0 1px rgba(255,255,255,.07) inset}
.phone::before{content:"";position:absolute;z-index:1;top:17px;left:50%;width:28%;height:20px;margin-left:-14%;border-radius:20px;background:#05050a}
.phone img{display:block;width:100%;height:auto;border-radius:36px;background:var(--card)}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:0 0 72px}
.stat{padding:22px 24px;border-radius:22px;background:var(--card);border:1px solid var(--border);text-align:center}
.stat b{display:block;font-size:clamp(34px,5vw,48px);line-height:1.1;font-weight:800;letter-spacing:-.02em;color:var(--accent)}
.stat span{color:var(--soft);font-weight:700;font-size:15px}
.sec-title{font-size:clamp(26px,4vw,38px);line-height:1.15;font-weight:800;letter-spacing:-.015em;text-align:center;margin:0 auto 40px;max-width:760px;text-wrap:balance}
.feat{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center;margin:0 0 72px}
.feat.rev .feat-art{order:2}
.feat-art{position:relative;display:flex;justify-content:center;padding:28px 0}
.feat-art::before{content:"";position:absolute;inset:0 8%;border-radius:36px;background:linear-gradient(160deg,var(--c1),var(--c2));opacity:.16}
.feat-art .phone{width:min(100%,290px)}
.eyebrow{margin:0 0 10px;font-size:13px;font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:var(--c1,var(--accent))}
@media (prefers-color-scheme:dark){.eyebrow{filter:brightness(1.35)}}
.feat h3{font-size:clamp(24px,3.4vw,34px);line-height:1.18;font-weight:800;letter-spacing:-.012em;margin:0 0 18px;text-wrap:balance}
.ticks{list-style:none;padding:0;margin:0}
.ticks li{position:relative;padding-left:32px;margin:0 0 12px;color:var(--soft);font-size:16.5px}
.ticks li::before{content:"✓";position:absolute;left:0;top:2px;width:21px;height:21px;border-radius:50%;background:var(--tint);color:var(--accent);font-size:12px;font-weight:800;display:flex;align-items:center;justify-content:center}
.more{margin:0 0 72px}
.more .grid{grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin:0}
.more .card{padding:26px}
.more .card svg{width:30px;height:30px;stroke:var(--accent);fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;margin-bottom:14px}
.more .card h3{font-size:19px}.more .card p{font-size:16px;line-height:1.55}
.screens{margin:0 0 72px}
.rail{display:flex;gap:22px;overflow-x:auto;padding:6px 20px 26px;margin:0 -20px;scroll-snap-type:x mandatory;justify-content:safe center}
.rail .phone{flex:none;width:230px;scroll-snap-align:center}
.langs-sec{text-align:center;margin:0 0 72px}
.langs-sec p{color:var(--soft);max-width:560px;margin:-18px auto 26px}
.pills{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin:0;padding:0;list-style:none}
.pills li{margin:0}
.pills a{display:block;padding:9px 18px;border-radius:999px;background:var(--card);border:1px solid var(--border);color:var(--ink);text-decoration:none;font-weight:700;font-size:15px}
.pills a:hover,.pills a[aria-current]{border-color:var(--accent);color:var(--accent);background:var(--tint)}
.cta{border-radius:32px;padding:clamp(32px,6vw,64px) 24px;text-align:center;color:#fff;background:linear-gradient(135deg,#4F46E5,#7C3AED 60%,#DB2777);margin:0 0 30px;position:relative;overflow:hidden}
.cta::after{content:"";position:absolute;inset:auto -10% -60% auto;width:60%;aspect-ratio:1;border-radius:50%;background:rgba(255,255,255,.1)}
.cta h2{font-size:clamp(26px,4.4vw,40px);line-height:1.15;margin:0 0 10px;font-weight:800;letter-spacing:-.015em;position:relative}
.cta p{margin:0 0 24px;color:rgba(255,255,255,.88);font-size:18px;position:relative}
.cta .btn{background:#fff;color:#241F73;position:relative}
.js .reveal{opacity:0;transform:translateY(18px);transition:opacity .6s ease,transform .6s ease}
.js .reveal.in{opacity:1;transform:none}
@media (max-width:860px){
  .hero .btns{flex-wrap:wrap}
  .hero{grid-template-columns:1fr;gap:28px}.hero-art{height:470px;max-width:440px;margin:0 auto;width:100%}.hero-art .phone{width:215px}
  .feat,.feat.rev{grid-template-columns:1fr;gap:20px;margin-bottom:56px}.feat.rev .feat-art{order:0}
  .stats{grid-template-columns:1fr}.more .grid{grid-template-columns:1fr}
  .rail{justify-content:flex-start}
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
{HEAD_JS if body == "home" else ""}</head>
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


REVEAL_SCRIPT = """<script>
(function(){if(!document.documentElement.classList.contains('js'))return;
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}})},{rootMargin:'0px 0px -8% 0px'});
document.querySelectorAll('.reveal').forEach(function(e){io.observe(e)});})();
</script>
"""
HEAD_JS = """<script>(function(){if('IntersectionObserver' in window&&!matchMedia('(prefers-reduced-motion: reduce)').matches)document.documentElement.classList.add('js')})()</script>
"""


def footer(lang: dict, script: str = "") -> str:
    return (f'<footer><span>{lang["footer_rights"]}</span>'
            f'<a href="privacy.html">{esc(lang["nav_privacy"])}</a><a href="support.html">{esc(lang["nav_support"])}</a></footer>\n'
            f"</div>\n{script}</body>\n</html>\n")


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


def phone(lang: dict, scene: str, alt: str, lazy: bool = True, cls: str = "") -> str:
    loading = ' loading="lazy"' if lazy else ""
    return (f'<div class="phone{" " + cls if cls else ""}"><img src="../assets/shots/{lang["folder"]}-{scene}.jpg"'
            f' alt="{html.escape(alt)}" width="{SHOT_W}" height="{SHOT_H}"{loading}></div>')


def index_page(lang: dict) -> str:
    c = lang["index"]
    ui = UI[lang["folder"]]
    feats = FEATURES["langs"][lang["folder"]]
    colors = FEATURES["colors"]
    head_html = head(lang, "index.html", c["title"], c["description"], body="home")
    hero_art = (phone(lang, HERO_SCREENS[0], feats["headlines"][0], lazy=False, cls="p1") +
                phone(lang, HERO_SCREENS[1], feats["headlines"][1], lazy=False, cls="p2"))
    chips = "".join(f"<li>{esc(t)}</li>" for t in ui["chips"])
    stats = "".join(f'<div class="stat"><b>{n}</b><span>{esc(t)}</span></div>'
                    for n, t in zip(("13", "0", "100%"), ui["stats"]))
    rows = []
    for i, (scene, sec) in enumerate(SHOWCASE):
        heading, bullets = feats["sections"][sec]
        headline = feats["headlines"][FEATURES["scenes"].index(scene)]
        c1, c2 = colors[scene]
        ticks = "".join(f"<li>{esc(b)}</li>" for b in bullets)
        rows.append(
            f'<article class="feat reveal{" rev" if i % 2 else ""}" style="--c1:{c1};--c2:{c2}">'
            f'<div class="feat-art">{phone(lang, scene, headline)}</div>'
            f'<div class="feat-text"><p class="eyebrow">{esc(heading)}</p><h3>{esc(headline)}</h3><ul class="ticks">{ticks}</ul></div>'
            "</article>")
    cards = c["cards"] if len(c["cards"]) == 3 else [c["cards"][3], c["cards"][6], c["cards"][7]]
    more = "".join(
        f'<div class="card"><svg viewBox="0 0 24 24" aria-hidden="true">{icon}</svg><h3>{esc(t)}</h3><p>{esc(p)}</p></div>'
        for icon, (t, p) in zip(ICONS, cards))
    rail = "".join(phone(lang, sc, feats["headlines"][FEATURES["scenes"].index(sc)]) for sc in MORE_SCREENS)
    pills = "".join(
        f'<li><a href="../{l["folder"]}/index.html" hreflang="{l["code"]}" lang="{l["html_lang"]}"'
        f'{" aria-current=page" if l is lang else ""}>{esc(l["label"])}</a></li>' for l in LANGS)
    return (head_html + nav(lang, "index.html") +
            f'<section class="hero"><div class="hero-text"><h1>{esc(c["h1"])}</h1><p class="lead">{esc(c["lead"])}</p>\n'
            f'<div class="btns"><a class="btn" href="{APP_STORE}">{esc(c["download"])}</a>'
            f'<a class="btn ghost" href="support.html">{esc(c["support_btn"])}</a></div>'
            f'<ul class="chips">{chips}</ul></div><div class="hero-art">{hero_art}</div></section>\n'
            f'<section class="stats">{stats}</section>\n'
            f'<section id="features"><h2 class="sec-title">{esc(ui["features_title"])}</h2>\n' + "\n".join(rows) + "</section>\n"
            f'<section class="more reveal"><h2 class="sec-title">{esc(ui["more_title"])}</h2><div class="grid">{more}</div></section>\n'
            f'<section class="screens reveal"><h2 class="sec-title">{esc(ui["screens_title"])}</h2><div class="rail">{rail}</div></section>\n'
            f'<section class="langs-sec reveal"><h2 class="sec-title">{esc(ui["langs_title"])}</h2><p>{esc(ui["langs_text"])}</p><ul class="pills">{pills}</ul></section>\n'
            f'<section class="cta reveal"><h2>{esc(ui["cta_title"])}</h2><p>{esc(ui["cta_text"])}</p>'
            f'<a class="btn" href="{APP_STORE}">{esc(c["download"])}</a></section>\n'
            f'<p class="note">{esc(c["note"])}</p>\n' + footer(lang, REVEAL_SCRIPT))


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
        for scene in SCENES:
            path = shots_dir / source / f"{scene}.png"
            if not path.exists():
                print("missing", path)
                continue
            Image.open(path).convert("RGB").resize((SHOT_W, SHOT_H), Image.LANCZOS).save(
                out / f"{folder}-{scene}.jpg", "JPEG", quality=80, optimize=True, progressive=True)


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
