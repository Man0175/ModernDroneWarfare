"""Builds the mod's support page from links.json: README.md (the repository page), index.html (GitHub Pages) and
.github/FUNDING.yml (the Sponsor button). A link left empty is left out everywhere.

Usage: python build.py                 (the real page from links.json)
       python build.py --preview <dir>  (example links, written to <dir> to look at the layout)
"""
import html
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LINKS = json.loads((ROOT / 'links.json').read_text(encoding='utf-8'))
PREVIEW = Path(sys.argv[sys.argv.index('--preview') + 1]) if '--preview' in sys.argv else None
if PREVIEW:
    LINKS.update(kofi='https://ko-fi.com/example', monobank='https://send.monobank.ua/jar/example',
                 funpay='https://funpay.com/users/example/', monobank_card='0000 0000 0000 0000',
                 usdt_bep20='0x0000000000000000000000000000000000000000')

TEXT = {
    'en': dict(
        name='English',
        title='Modern Drone Warfare',
        tagline='A RimWorld mod',
        intro="Drone warfare the way it really works: you don't just build drones, you fly them — with crews of pilots, "
              "observers and technicians, over a radio link that walls, woods, weather and jamming can break.",
        head='What may surprise you',
        points=[
            'Crews fight on their own: on alarm they drop their work, run to the launch point and take off; technicians build, arm and charge the drones.',
            'The link is everything. Five real radio kits, each with its own range and picture, and the enemy retunes its jammers to the ones you fly on most. Fiber-optic FPVs ignore jamming but drag a cable across the map: cut it and the drone goes blind.',
            'The enemy hunts your operators by direction finding; your video receiver shows where its FPV is heading.',
            'Night raids by Shahed / Geran-class drones off launch rails, strikes back on the world map, TB2-class planes rolling down a runway.',
            'What is mounted is what you see: warheads, drops and the satellite modem are drawn on the drone. Real prototype names for your side: Ukrainian, Russian or Western.',
            'Air defense from jammer guns and nets to flak, lasers, microwaves and GPS spoofing — and your own EW can blind your own drones.',
        ],
        workshop='Get it on the Steam Workshop',
        support='Support the author',
        support_intro='The mod is free and stays free. If you enjoy it and want to help it grow, here is how — thank you!',
        west='International', ua='Ukraine', ru='Russia and CIS', crypto='Crypto',
        copy='Copy', copied='Copied', card='Jar card',
        bep20='Only USDT on BNB Smart Chain (BEP20) — other networks or tokens will be lost.',
        footer='This mod is about the mechanics of drone warfare, not about politics.',
    ),
    'uk': dict(
        name='Українська',
        title='Сучасна безпілотна війна',
        tagline='Мод для RimWorld',
        intro="Війна дронів така, якою вона є: дрони мало збудувати, ними треба літати — розрахунками з пілотів, "
              "спостерігачів і техніків, через радіозв'язок, який рвуть стіни, ліс, погода й РЕБ.",
        head='Чим може здивувати',
        points=[
            'Екіпажі воюють самі: за тривогою кидають роботу, біжать на точку й злітають; техніки збирають, споряджають і заряджають дрони.',
            "Зв'язок вирішує все. П'ять реальних радіокомплектів зі своєю дальністю й картинкою, а ворог перебудовує глушилки під ті, на яких ви літаєте найчастіше. Оптоволоконний FPV не боїться РЕБ, але тягне кабель через усю мапу: переріжте — і дрон осліп.",
            'Ворог пеленгує ваших операторів, а ваш відеоприймач показує, куди летить його FPV.',
            'Нічні нальоти «Шахедів» із пускових напрямних, удари у відповідь по мапі світу, літаки класу TB2 з розбігом по злітній смузі.',
            'Що підвішено, те й видно: БЧ, скиди й супутниковий модем намальовані на дроні. Назви реальних прототипів вашої сторони: українські, російські або західні.',
            'ППО від РЕБ-рушниць і сіток до зеніток, лазерів, НВЧ і підміни GPS — а своя РЕБ може осліпити власні дрони.',
        ],
        workshop='Завантажити в Steam Workshop',
        support='Підтримати автора',
        support_intro='Мод безкоштовний і таким залишиться. Якщо він вам подобається і ви хочете допомогти йому рости — ось як. Дякую!',
        west='Міжнародні', ua='Україна', ru='Росія та СНД', crypto='Крипта',
        copy='Копіювати', copied='Скопійовано', card='Картка банки',
        bep20='Лише USDT у мережі BNB Smart Chain (BEP20) — інші мережі чи токени буде втрачено.',
        footer='Мод — про механіку війни дронів, а не про політику.',
    ),
    'ru': dict(
        name='Русский',
        title='Современная беспилотная война',
        tagline='Мод для RimWorld',
        intro="Война дронов такой, какая она есть: дроны мало построить, ими надо летать — расчётами из пилотов, "
              "наблюдателей и техников, по радиосвязи, которую рвут стены, лес, погода и РЭБ.",
        head='Чем может удивить',
        points=[
            'Экипажи воюют сами: по тревоге бросают работу, бегут на точку и взлетают; техники собирают, снаряжают и заряжают дроны.',
            'Связь решает всё. Пять реальных радиокомплектов со своей дальностью и картинкой, а враг перестраивает глушилки под те, на которых вы летаете чаще. Оптоволоконный FPV не боится РЭБ, но тянет кабель через всю карту: перережьте — и дрон ослеп.',
            'Враг пеленгует ваших операторов, а ваш видеоприёмник показывает, куда летит его FPV.',
            'Ночные налёты «Шахедов» с пусковых направляющих, ответные удары по карте мира, самолёты класса TB2 с разбегом по взлётной полосе.',
            'Что подвешено, то и видно: БЧ, сбросы и спутниковый модем нарисованы на дроне. Названия реальных прототипов вашей стороны: украинские, российские или западные.',
            'ПВО от РЭБ-ружей и сетей до зениток, лазеров, СВЧ и подмены GPS — а своя РЭБ может ослепить свои же дроны.',
        ],
        workshop='Скачать в Steam Workshop',
        support='Поддержать автора',
        support_intro='Мод бесплатный и останется таким. Если он вам нравится и хочется помочь ему расти — вот как. Спасибо!',
        west='Международные', ua='Украина', ru='Россия и СНГ', crypto='Крипта',
        copy='Копировать', copied='Скопировано', card='Карта банки',
        bep20='Только USDT в сети BNB Smart Chain (BEP20) — другие сети или токены будут потеряны.',
        footer='Мод — про механику войны дронов, а не про политику.',
    ),
}
ORDER = ['en', 'uk', 'ru']
MEDIA = [('media/strike.gif', 'FPV strike'), ('media/planeflight.jpg', 'Rail launch, runway take-off, landing roll-out'),
         ('media/bigdrones.jpg', 'Big drones by heading'), ('media/drop.gif', 'Drop from a scout'),
         ('media/crew.jpg', 'A drone crew at its launch point'), ('media/lineup.jpg', 'The drones')]


def support_links():
    """(group key, label, url) of every filled-in link."""
    rows = []
    if LINKS.get('kofi'):
        rows.append(('west', 'Ko-fi', LINKS['kofi']))
    if LINKS.get('github_sponsors'):
        rows.append(('west', 'GitHub Sponsors', LINKS['github_sponsors']))
    if LINKS.get('patreon'):
        rows.append(('west', 'Patreon', LINKS['patreon']))
    if LINKS.get('monobank'):
        rows.append(('ua', 'Monobank', LINKS['monobank']))
    if LINKS.get('funpay'):
        rows.append(('ru', 'FunPay', LINKS['funpay']))
    if LINKS.get('boosty'):
        rows.append(('ru', 'Boosty', LINKS['boosty']))
    return rows


def readme():
    t = TEXT['en']
    out = [f'<p align="center"><img src="media/preview.png" alt="{t["title"]}" width="640"></p>', '',
           f'# {t["title"]}', '', f'*{t["tagline"]}* — **[{t["workshop"]}]({LINKS["steam"]})**', '']
    links = support_links()
    if links or LINKS.get('usdt_bep20'):
        out += [f'## {t["support"]}', '', t['support_intro'], '']
        for key in ('west', 'ua', 'ru'):
            group = [f'[{label}]({url})' for k, label, url in links if k == key]
            if key == 'ua' and LINKS.get('monobank_card'):
                group.append(f'{t["card"]} `{LINKS["monobank_card"]}`')
            if group:
                out.append(f'- **{t[key]}:** ' + ' · '.join(group))
        if LINKS.get('usdt_bep20'):
            out.append(f'- **{t["crypto"]} (USDT, BEP20 / BSC):** `{LINKS["usdt_bep20"]}` — {t["bep20"]}')
        out.append('')
    for lang in ORDER:
        t = TEXT[lang]
        body = [f'### {t["head"]}', ''] + [f'- {p}' for p in t['points']] + ['']
        if lang == 'en':
            out += [t['intro'], ''] + body
        else:
            out += [f'<details><summary><b>{t["name"]} — {t["title"]}</b></summary>', '', t['intro'], ''] + body + ['</details>', '']
    out += ['## Screenshots', '']
    for src, alt in MEDIA:
        out.append(f'<img src="{src}" alt="{alt}" width="420">')
    out += ['', f'*{TEXT["en"]["footer"]}*', '']
    return '\n'.join(out)


def funding():
    lines = []
    sponsors = LINKS.get('github_sponsors', '')
    if sponsors:
        lines.append(f'github: [{sponsors.rstrip("/").split("/")[-1]}]')
    if LINKS.get('kofi'):
        lines.append(f'ko_fi: {LINKS["kofi"].rstrip("/").split("/")[-1]}')
    if LINKS.get('patreon'):
        lines.append(f'patreon: {LINKS["patreon"].rstrip("/").split("/")[-1]}')
    custom = [LINKS[k] for k in ('monobank', 'funpay', 'boosty') if LINKS.get(k)]
    if custom:
        lines.append('custom: [' + ', '.join(f'"{u}"' for u in custom[:4]) + ']')
    return '\n'.join(lines) + '\n' if lines else ''


def page():
    e = html.escape
    langs = []
    for lang in ORDER:
        t = TEXT[lang]
        groups = []
        for key in ('west', 'ua', 'ru'):
            buttons = ''.join(f'<a class="btn" href="{e(url)}" target="_blank" rel="noopener">{e(label)}</a>'
                              for k, label, url in support_links() if k == key)
            extra = ''
            if key == 'ua' and LINKS.get('monobank_card'):
                card = LINKS['monobank_card']
                extra = (f'<div class="row wallet"><span class="muted">{e(t["card"])}</span><code>{e(card)}</code>'
                         f'<button class="btn ghost" data-copy="{e(card.replace(" ", ""))}" data-done="{e(t["copied"])}">{e(t["copy"])}</button></div>')
            if buttons or extra:
                groups.append(f'<div class="group"><h3>{e(t[key])}</h3><div class="row">{buttons}</div>{extra}</div>')
        if LINKS.get('usdt_bep20'):
            addr = LINKS['usdt_bep20']
            groups.append(f'<div class="group"><h3>{e(t["crypto"])} · USDT (BEP20 / BSC)</h3><div class="row wallet">'
                          f'<code>{e(addr)}</code><button class="btn ghost" data-copy="{e(addr)}" '
                          f'data-done="{e(t["copied"])}">{e(t["copy"])}</button></div><p class="note">{e(t["bep20"])}</p></div>')
        support = (f'<section class="support"><h2>{e(t["support"])}</h2><p>{e(t["support_intro"])}</p>{"".join(groups)}</section>'
                   if groups else '')
        points = ''.join(f'<li>{e(p)}</li>' for p in t['points'])
        langs.append(f'''<div class="lang" data-lang="{lang}" lang="{lang}" hidden>
<header><img class="icon" src="media/icon.png" alt=""><div><h1>{e(t["title"])}</h1><p class="tag">{e(t["tagline"])}</p></div></header>
<p class="intro">{e(t["intro"])}</p>
<a class="btn primary" href="{e(LINKS["steam"])}" target="_blank" rel="noopener">{e(t["workshop"])}</a>
<h2>{e(t["head"])}</h2><ul class="points">{points}</ul>
{support}
<p class="foot">{e(t["footer"])}</p>
</div>''')
    gallery = ''.join(f'<figure><img src="{src}" alt="{e(alt)}" loading="lazy"></figure>' for src, alt in MEDIA)
    switch = ''.join(f'<button data-set="{lang}">{e(TEXT[lang]["name"])}</button>' for lang in ORDER)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Modern Drone Warfare</title>
<meta name="description" content="Modern Drone Warfare — a RimWorld mod about how drones really fight.">
<link rel="icon" href="media/icon.png">
<style>
:root {{ --bg:#14171a; --panel:#1d2125; --text:#e7e4dc; --muted:#9aa19a; --accent:#c9a227; --line:#2d3237; }}
@media (prefers-color-scheme: light) {{ :root {{ --bg:#f3f1ea; --panel:#ffffff; --text:#1d2125; --muted:#5d6560; --accent:#8a6d0b; --line:#ddd8cc; }} }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--text); font:16px/1.55 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }}
main {{ max-width:960px; margin:0 auto; padding:24px 16px 48px; }}
.switch {{ display:flex; gap:8px; justify-content:flex-end; flex-wrap:wrap; margin-bottom:16px; }}
.switch button {{ background:none; border:1px solid var(--line); color:var(--muted); border-radius:6px; padding:4px 10px; cursor:pointer; font:inherit; }}
.switch button.on {{ color:var(--text); border-color:var(--accent); }}
.hero img {{ width:100%; border-radius:10px; display:block; }}
header {{ display:flex; gap:14px; align-items:center; margin:20px 0 8px; }}
.icon {{ width:56px; height:56px; border-radius:10px; }}
h1 {{ margin:0; font-size:1.7rem; }}
.tag {{ margin:0; color:var(--muted); }}
.intro {{ font-size:1.08rem; }}
h2 {{ margin-top:32px; font-size:1.25rem; }}
h3 {{ margin:0 0 8px; font-size:.95rem; color:var(--muted); font-weight:600; }}
.points li {{ margin:6px 0; }}
.btn {{ display:inline-block; padding:9px 16px; border-radius:8px; border:1px solid var(--line); background:var(--panel); color:var(--text); text-decoration:none; font:inherit; cursor:pointer; }}
.btn:hover {{ border-color:var(--accent); }}
.btn.primary {{ background:var(--accent); border-color:var(--accent); color:#14171a; font-weight:600; }}
.support {{ background:var(--panel); border:1px solid var(--line); border-radius:12px; padding:4px 20px 18px; margin-top:32px; }}
.group {{ margin-top:14px; }}
.row {{ display:flex; gap:10px; flex-wrap:wrap; align-items:center; }}
.wallet {{ margin-top:8px; }}
.wallet code {{ font-size:.85rem; word-break:break-all; }}
.muted, .note {{ color:var(--muted); font-size:.9rem; }}
.note {{ margin:6px 0 0; }}
.gallery {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:12px; margin-top:28px; }}
.gallery figure {{ margin:0; }}
.gallery img {{ width:100%; border-radius:8px; display:block; }}
.foot {{ color:var(--muted); font-size:.9rem; margin-top:28px; }}
</style>
</head>
<body>
<main>
<nav class="switch">{switch}</nav>
<div class="hero"><img src="media/preview.png" alt="Modern Drone Warfare"></div>
{"".join(langs)}
<div class="gallery">{gallery}</div>
</main>
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
  show(saved || (nav === 'uk' || nav === 'ru' ? nav : 'en'));
  buttons.forEach(function (b) {{ b.addEventListener('click', function () {{ show(b.dataset.set); }}); }});
  document.querySelectorAll('[data-copy]').forEach(function (b) {{
    b.addEventListener('click', function () {{
      var label = b.textContent;
      navigator.clipboard.writeText(b.dataset.copy).then(function () {{
        b.textContent = b.dataset.done; setTimeout(function () {{ b.textContent = label; }}, 1500);
      }});
    }});
  }});
}})();
</script>
</body>
</html>
'''


if PREVIEW:
    PREVIEW.mkdir(parents=True, exist_ok=True)
    (PREVIEW / 'index.html').write_text(page(), encoding='utf-8')
    shutil.copytree(ROOT / 'media', PREVIEW / 'media', dirs_exist_ok=True)
    print('preview:', PREVIEW / 'index.html')
    sys.exit(0)
(ROOT / 'README.md').write_text(readme(), encoding='utf-8')
(ROOT / 'index.html').write_text(page(), encoding='utf-8')
fund = funding()
path = ROOT / '.github' / 'FUNDING.yml'
if fund:
    path.parent.mkdir(exist_ok=True)
    path.write_text(fund, encoding='utf-8')
elif path.exists():
    path.unlink()
print('built:', ', '.join(label for _, label, _ in support_links()) or 'no support links yet',
      '+ jar card' if LINKS.get('monobank_card') else '', '+ USDT BEP20' if LINKS.get('usdt_bep20') else '')
