"""Builds manual.html (the in-game manual on the site) from the mod's own texts and pictures.

Usage: python build_manual.py [path to the mod folder, default ../ModernWAR]
The chapters and their texts are the mod's Languages/<lang>/Keyed/MDW_Manual.xml (English, Ukrainian, Russian, Chinese);
the pictures are its Textures/MDW/Manual/<chapter>.jpg, copied to media/manual.
"""
import html
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MOD = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / 'ModernWAR'
CHAPTERS = ['Start', 'Link', 'EW', 'Drones', 'Warheads', 'Crews', 'Defence', 'Enemy', 'LongRange', 'Ground', 'DLC', 'Settings']
LANGS = [('en', 'English', 'English'), ('es', 'Español', 'Spanish (Español(Castellano))'), ('uk', 'Українська', 'Ukrainian (Українська)'),
         ('ru', 'Русский', 'Russian (Русский)'), ('zh', '简体中文', 'ChineseSimplified (简体中文)')]
UI = {
    'en': dict(back='← Mod page', contents='Contents', note='The same manual is in the game: the Drones tab and the mod settings.'),
    'es': dict(back='← Página del mod', contents='Contenido', note='El mismo manual está en el juego: la pestaña «Drones» y los ajustes del mod.'),
    'uk': dict(back='← Сторінка мода', contents='Зміст', note='Той самий посібник є в грі: вкладка «Дрони» і налаштування мода.'),
    'ru': dict(back='← Страница мода', contents='Содержание', note='То же руководство есть в игре: вкладка «Дроны» и настройки мода.'),
    'zh': dict(back='← 模组主页', contents='目录', note='游戏内也有同样的手册：在“无人机”标签页和模组设置中。'),
}


def keyed(folder):
    text = (MOD / 'Languages' / folder / 'Keyed' / 'MDW_Manual.xml').read_text(encoding='utf-8')
    return {k: html.unescape(v) for k, v in re.findall(r'<(MDW_Manual_[A-Za-z]+_(?:Title|Text))>(.*?)</\1>', text, re.S)}


def render(text):
    """Paragraphs from the manual's \\n breaks; lines starting with '- ' become a list."""
    e = html.escape
    out, items = [], []
    for line in text.replace('\\n', '\n').split('\n'):
        line = line.strip()
        if line.startswith('- '):
            items.append(f'<li>{e(line[2:])}</li>')
            continue
        if items:
            out.append('<ul>' + ''.join(items) + '</ul>')
            items = []
        if line:
            out.append(f'<p>{e(line)}</p>')
    if items:
        out.append('<ul>' + ''.join(items) + '</ul>')
    return ''.join(out)


def main():
    pictures = ROOT / 'media' / 'manual'
    pictures.mkdir(parents=True, exist_ok=True)
    have = set()
    for chapter in CHAPTERS:
        src = MOD / 'Textures' / 'MDW' / 'Manual' / (chapter + '.jpg')
        if src.exists():
            shutil.copyfile(src, pictures / src.name)
            have.add(chapter)
    e = html.escape
    blocks = []
    for code, name, folder in LANGS:
        texts = keyed(folder)
        toc = ''.join(f'<li><a href="#{code}-{c}">{e(texts.get(f"MDW_Manual_{c}_Title", c))}</a></li>' for c in CHAPTERS)
        chapters = []
        for c in CHAPTERS:
            full = f'media/manual/full/{c}.jpg' if (pictures / 'full' / f'{c}.jpg').exists() else f'media/manual/{c}.jpg'
            title = e(texts.get(f"MDW_Manual_{c}_Title", c))
            pic = f'<img src="media/manual/{c}.jpg" alt="{title}" data-full="{full}" loading="lazy">' if c in have else ''
            chapters.append(f'<section id="{code}-{c}"><h2>{e(texts.get(f"MDW_Manual_{c}_Title", c))}</h2>{pic}'
                            f'{render(texts.get(f"MDW_Manual_{c}_Text", ""))}</section>')
        blocks.append(f'''<div class="lang" data-lang="{code}" lang="{code}" hidden>
<a class="back" href="index.html">{e(UI[code]["back"])}</a>
<h1>{e(texts.get("MDW_Manual_Title", "Modern Drone Warfare"))}</h1>
<p class="note">{e(UI[code]["note"])}</p>
<div class="layout"><nav class="toc"><h3>{e(UI[code]["contents"])}</h3><ol>{toc}</ol></nav><div class="chapters">{"".join(chapters)}</div></div>
</div>''')
    switch = ''.join(f'<button data-set="{code}">{e(name)}</button>' for code, name, _ in LANGS)
    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Modern Drone Warfare — manual</title>
<meta name="description" content="The manual of Modern Drone Warfare, a RimWorld mod about how drones really fight.">
<link rel="icon" href="media/icon.png">
<style>
:root {{ --bg:#14171a; --panel:#1d2125; --text:#e7e4dc; --muted:#9aa19a; --accent:#c9a227; --line:#2d3237; }}
@media (prefers-color-scheme: light) {{ :root {{ --bg:#f3f1ea; --panel:#ffffff; --text:#1d2125; --muted:#5d6560; --accent:#8a6d0b; --line:#ddd8cc; }} }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--text); font:16px/1.6 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }}
main {{ max-width:1100px; margin:0 auto; padding:24px 16px 48px; }}
.switch {{ display:flex; gap:8px; justify-content:flex-end; flex-wrap:wrap; margin-bottom:8px; }}
.switch button {{ background:none; border:1px solid var(--line); color:var(--muted); border-radius:6px; padding:4px 10px; cursor:pointer; font:inherit; }}
.switch button.on {{ color:var(--text); border-color:var(--accent); }}
.back {{ color:var(--muted); text-decoration:none; }}
h1 {{ margin:12px 0 4px; font-size:1.7rem; }}
.note {{ color:var(--muted); margin:0 0 20px; }}
.layout {{ display:grid; grid-template-columns:260px 1fr; gap:28px; align-items:start; }}
.toc {{ position:sticky; top:16px; background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:12px 16px; }}
.toc h3 {{ margin:0 0 6px; font-size:.95rem; color:var(--muted); }}
.toc ol {{ margin:0; padding-left:20px; }}
.toc a {{ color:var(--text); text-decoration:none; }}
.toc a:hover {{ color:var(--accent); }}
section {{ background:var(--panel); border:1px solid var(--line); border-radius:12px; padding:6px 22px 14px; margin-bottom:18px; }}
section h2 {{ font-size:1.25rem; }}
section img {{ width:100%; border-radius:8px; display:block; margin:4px 0 10px; }}
li {{ margin:4px 0; }}
@media (max-width:760px) {{ .layout {{ grid-template-columns:1fr; }} .toc {{ position:static; }} }}
</style>
</head>
<body>
<main>
<nav class="switch">{switch}</nav>
{"".join(blocks)}
</main>
<script src="lightbox.js"></script>
<script>
(function () {{
  var langs = document.querySelectorAll('.lang'), buttons = document.querySelectorAll('[data-set]');
  function show(code) {{
    langs.forEach(function (el) {{ el.hidden = el.dataset.lang !== code; }});
    buttons.forEach(function (b) {{ b.classList.toggle('on', b.dataset.set === code); }});
    document.documentElement.lang = code;
    try {{ localStorage.setItem('mdw-lang', code); }} catch (e) {{}}
  }}
  var saved = null;
  try {{ saved = localStorage.getItem('mdw-lang'); }} catch (e) {{}}
  var nav = (navigator.language || 'en').slice(0, 2);
  show(saved || (nav === 'uk' || nav === 'ru' || nav === 'zh' || nav === 'es' ? nav : 'en'));
  buttons.forEach(function (b) {{ b.addEventListener('click', function () {{ show(b.dataset.set); }}); }});
}})();
</script>
</body>
</html>
'''
    (ROOT / 'manual.html').write_text(page, encoding='utf-8')
    print('manual.html:', len(CHAPTERS), 'chapters,', len(have), 'pictures,', len(LANGS), 'languages')


main()
