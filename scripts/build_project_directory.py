"""Publish the intentionally curated public project directory, never a filesystem scan."""
import html
import json
from pathlib import Path
from build_discovery import head_metadata, ROOT

projects = json.loads((ROOT / 'seo/projects.json').read_text(encoding='utf-8'))
e = lambda value: html.escape(value, quote=True)
cards = ''.join(f'<article><p class="topic">{e(p["topic"])}</p><h2><a href="{p["url"]}">{e(p["name"])}</a></h2><p>{e(p["description"])}</p><nav><a href="{p["url"]}">Apri il sito ↗</a><a href="{p["data"]}">Dati</a><a href="{p["methods"]}">Metodo e fonti</a><a href="{p["repo"]}">Codice</a></nav></article>' for p in projects)
source = f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Progetti</title><meta name="description" content="Progetti di ricerca"><link rel="icon" href="../favicon.svg"><style>*{{box-sizing:border-box}}body{{margin:0;background:#f2eee5;color:#171b1b;font:17px/1.7 system-ui,sans-serif}}main,header,footer{{max-width:1060px;margin:auto;padding:24px}}header,footer{{border-bottom:1px solid #c9c4ba}}a{{color:#215b55;text-underline-offset:4px}}h1{{font:400 clamp(2.5rem,6vw,4rem)/1.1 Georgia,serif}}h2{{font-size:1.7rem;line-height:1.3}}article{{padding:30px 0;border-top:1px solid #c9c4ba}}article p{{max-width:78ch}}.topic{{color:#5a6262;font-size:.85rem;text-transform:uppercase;letter-spacing:.06em}}nav{{display:flex;flex-wrap:wrap;gap:20px}}nav a{{min-height:44px;display:inline-flex;align-items:center}}:focus-visible{{outline:3px solid #9b4f37;outline-offset:4px}}</style></head><body><header><a href="../">Simone Ghezzi Colombo</a> · <a href="../index-en.html">English profile</a></header><main><h1>Progetti di ricerca e dataset pubblici</h1><p>Una guida ai miei progetti su elezioni, mobilità, scuola e ricerca sociale. Ogni collegamento porta al sito del progetto, ai dati disponibili e alle fonti necessarie per interpretarli.</p>{cards}</main><footer><p>Ricerca indipendente e trasparenza del metodo. Le analisi non sono siti istituzionali e le proposte non equivalgono a servizi pubblici in esercizio.</p><a href="../feed.xml">Feed RSS</a> · <a href="../llms.txt">Indice testuale dei contenuti</a></footer></body></html>'''
source = head_metadata(source, {'url':'progetti/', 'title':'Progetti di ricerca e dataset pubblici | Simone Ghezzi Colombo', 'description':'Electio Italia, S8 Milano-Lecco, indice delle scuole superiori, polarizzazione Gen Z e Nodo8: siti, dati, codice e fonti.', 'type':'CollectionPage'})
items = {'@context':'https://schema.org','@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'name':p['name'],'url':p['url']} for i,p in enumerate(projects)]}
source = source.replace('</head>', '<script type="application/ld+json">' + json.dumps(items,ensure_ascii=False) + '</script></head>')
target = ROOT / 'progetti/index.html'
target.parent.mkdir(exist_ok=True)
target.write_text(source,encoding='utf-8')
print(f'Published {len(projects)} curated public projects.')
