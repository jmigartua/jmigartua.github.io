#!/usr/bin/env python3
"""Generate the publications pages (en, es, eu) and the home-page includes
from _data/publications.yml.

The data file is the thermomat-site publication registry (OpenAlex-synchronised,
curated by hand there). Only items whose `members` include `igartua-josu` are
used. Re-copy the file from the thermomat repository to refresh.
"""
from __future__ import annotations
import html, re
from collections import Counter, defaultdict
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "_data" / "publications.yml"
ME = "igartua-josu"

STRINGS = {
    "en": dict(title="Publications", kinds=[
            ("research", "Research articles", "Peer-reviewed journal articles, book chapters, books and reports."),
            ("proceedings", "Conference papers", "Contributions published in conference proceedings."),
            ("teaching", "Physics education", "Research on teaching and learning physics."),
            ("outreach", "Outreach", "Science communication, mostly in Basque."),
            ("software", "Software and data", "Released code and datasets, with DOIs.")],
        all="All", items="items", item="item", citations="citations",
        lede="{n} indexed works from {y0} to {y1}, {c} citations counted by OpenAlex. The list is the Thermomat group registry filtered to my authorship, synchronised with OpenAlex and curated by hand; earlier work under the Applied Physics II department is included. Journal articles first; use the tabs for proceedings, physics-education papers, outreach and released software.",
        stats=("research articles", "indexed works", "OpenAlex citations", "years publishing"), crumb="publications"),
    "es": dict(title="Publicaciones", kinds=[
            ("research", "Artículos de investigación", "Artículos revisados por pares, capítulos de libro, libros e informes."),
            ("proceedings", "Congresos", "Contribuciones publicadas en actas de congresos."),
            ("teaching", "Didáctica de la física", "Investigación sobre la enseñanza y el aprendizaje de la física."),
            ("outreach", "Divulgación", "Comunicación científica, sobre todo en euskera."),
            ("software", "Software y datos", "Código y conjuntos de datos publicados, con DOI.")],
        all="Todo", items="ítems", item="ítem", citations="citas",
        lede="{n} trabajos indexados entre {y0} y {y1}, {c} citas contadas por OpenAlex. La lista es el registro del grupo Thermomat filtrado por mi autoría, sincronizado con OpenAlex y revisado a mano; incluye el trabajo anterior en el departamento de Física Aplicada II. Primero los artículos; las pestañas dan acceso a congresos, didáctica, divulgación y software.",
        stats=("artículos de investigación", "trabajos indexados", "citas en OpenAlex", "años publicando"), crumb="publicaciones"),
    "eu": dict(title="Argitalpenak", kinds=[
            ("research", "Ikerketa-artikuluak", "Parekideek berrikusitako artikuluak, liburu-kapituluak, liburuak eta txostenak."),
            ("proceedings", "Kongresuak", "Kongresu-aktetan argitaratutako ekarpenak."),
            ("teaching", "Fisikaren didaktika", "Fisikaren irakaskuntzari eta ikaskuntzari buruzko ikerketa."),
            ("outreach", "Dibulgazioa", "Zientzia-komunikazioa, batez ere euskaraz."),
            ("software", "Softwarea eta datuak", "Argitaratutako kodea eta datu-multzoak, DOIarekin.")],
        all="Guztiak", items="item", item="item", citations="aipu",
        lede="{n} lan indexatu {y0}tik {y1}ra, OpenAlexek zenbatutako {c} aipu. Zerrenda Thermomat taldearen erregistroa da, nire egiletzara iragazia, OpenAlexekin sinkronizatua eta eskuz berrikusia; Fisika Aplikatua II sailean egindako aurreko lana ere sartzen da. Lehenik artikuluak; fitxek kongresuak, didaktika, dibulgazioa eta softwarea ematen dituzte.",
        stats=("ikerketa-artikulu", "lan indexatu", "aipu OpenAlexen", "urte argitaratzen"), crumb="argitalpenak"),
}

def esc(s): return html.escape(str(s or ""), quote=False)

def bold_me(ref: str) -> str:
    return re.sub(r"(Josu M(?:irena|\.)? Igartua(?: Aldamiz)?|J\. M\. Igartua|Igartua,? J\.? ?M\.?|J\. Igartua)", r"<strong>\1</strong>", ref)

def item_html(p: dict, S: dict) -> str:
    title = esc(p.get("title"))
    ref = p.get("reference_html") or esc(p.get("reference") or "")
    ref = re.split(r",?\s*doi:\s*<a", ref)[0] if "doi:" in ref else ref
    ref = bold_me(ref)
    meta = []
    if p.get("doi"): meta.append(f'<a href="https://doi.org/{esc(p["doi"])}">doi:{esc(p["doi"])}</a>')
    if p.get("citations"): meta.append(f'{p["citations"]} {S["citations"]}')
    links = "".join(f' <span class="sep">&middot;</span> <a href="{esc(l["url"])}">{esc(l["name"])}</a>' for l in (p.get("links") or []) if l.get("url") and "doi.org" not in l["url"])
    kw = "".join(f'<span class="pub-tag kw">{esc(k)}</span>' for k in (p.get("keywords") or [])[:5])
    return (f'<div class="pub-item"><div class="t">{title}</div><div class="ref">{ref}</div>'
            + (f'<div class="m">{" · ".join(meta)}{links}</div>' if meta or links else "")
            + (f'<div class="m">{kw}</div>' if kw else "") + "</div>")

SCRIPT = """<script>
function showSection(f){var t=document.querySelector('.pub-section[data-f="'+f+'"]');if(!t)return false;
document.querySelectorAll('.pub-section').forEach(function(s){s.style.display='none'});
document.querySelectorAll('.pf').forEach(function(x){x.classList.remove('current')});
t.style.display='';var b=document.querySelector('.pf[data-f="'+f+'"]');if(b)b.classList.add('current');return true}
document.querySelectorAll('.pf').forEach(function(b){b.addEventListener('click',function(e){e.preventDefault();showSection(b.dataset.f);history.replaceState(null,'','#'+b.dataset.f)})});
(function(){var h=location.hash.replace('#','');if(h)showSection(h)})();
</script>"""

def page_for(lang: str, mine: list, S: dict) -> str:
    by_kind = defaultdict(list)
    for p in mine: by_kind[p.get("kind") or "research"].append(p)
    years = [int(p["year"]) for p in mine if p.get("year")]
    total_cites = sum(int(p.get("citations") or 0) for p in mine)
    tabs, sections = [], []
    for key, label, note in S["kinds"]:
        ps = by_kind.get(key, [])
        if not ps: continue
        tabs.append(f'<a href="#{key}" class="pf{" current" if not tabs else ""}" data-f="{key}">{label} <span class="pf-n">{len(ps)}</span></a>')
        by_year = defaultdict(list)
        for p in ps: by_year[int(p.get("year") or 0)].append(p)
        blocks = [f'<div class="pub-year">{y}<span class="n">{len(by_year[y])} {S["items"] if len(by_year[y]) != 1 else S["item"]}</span></div>' + "".join(item_html(p, S) for p in by_year[y]) for y in sorted(by_year, reverse=True)]
        yrs = [int(p["year"]) for p in ps if p.get("year")]
        sections.append(f'<section class="pub-section" id="sec-{key}" data-f="{key}"{"" if not sections else " style=\"display:none\""}>'
                        f'<p class="sec-count"><strong>{len(ps)}</strong> {S["items"]} · {min(yrs)}–{max(yrs)}</p><p class="sec-note">{note}</p>' + "".join(blocks) + "</section>")
    tabs.append(f'<a href="#all" class="pf" data-f="all">{S["all"]} <span class="pf-n">{len(mine)}</span></a>')
    by_all = defaultdict(list)
    for p in mine: by_all[int(p.get("year") or 0)].append(p)
    sections.append('<section class="pub-section" id="sec-all" data-f="all" style="display:none">'
                    + "".join(f'<div class="pub-year">{y}<span class="n">{len(by_all[y])}</span></div>' + "".join(item_html(p, S) for p in by_all[y]) for y in sorted(by_all, reverse=True)) + "</section>")
    home = "../index.html" if lang == "en" else "index.html"
    crumb_home = "../index.html" if lang == "en" else "../index.html"
    lede = S["lede"].format(n=len(mine), y0=min(years), y1=max(years), c=total_cites)
    return f"""---
title: "{S['title']}"
title-block-style: none
page-layout: full
toc: false
---

<!-- GENERATED by tools/generate_publications.py from _data/publications.yml. Do not edit by hand. -->

```{{=html}}
<div class="crumbs crumbs-wide"><a href="{crumb_home}">igartua</a> / {S['crumb']}</div>
<div class="page-wide">
<h1>{S['title']}</h1>
<p class="lede">{lede}</p>
<div class="pub-filter">{'<span class="sep">·</span>'.join(tabs)}</div>
{''.join(sections)}
{SCRIPT}
</div>
```
"""

def main() -> None:
    items = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    items = items if isinstance(items, list) else items.get("publications", [])
    mine = [p for p in items if ME in (p.get("members") or [])]
    mine.sort(key=lambda p: (str(p.get("date") or p.get("year") or ""), p.get("title") or ""), reverse=True)
    years = [int(p["year"]) for p in mine if p.get("year")]
    total_cites = sum(int(p.get("citations") or 0) for p in mine)
    counts = Counter(p.get("kind") or "research" for p in mine)
    (ROOT / "_gen").mkdir(exist_ok=True)
    for lang, S in STRINGS.items():
        out = ROOT / ("publications" if lang == "en" else f"{lang}/publications") / "index.qmd"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page_for(lang, mine, S), encoding="utf-8")
        recent = [p for p in mine if (p.get("kind") or "research") == "research"][:5]
        (ROOT / "_gen" / f"recent-pubs.{lang}.qmd").write_text("```{=html}\n<div class=\"pub-block\">\n" + "\n".join(item_html(p, S) for p in recent) + "\n</div>\n```\n", encoding="utf-8")
        k = S["stats"]
        (ROOT / "_gen" / f"pub-stats.{lang}.qmd").write_text(
            "```{=html}\n<div class=\"net-stats\">"
            f"<div class=\"net-stat\"><div class=\"v\">{counts.get('research',0)}</div><div class=\"k\">{k[0]}</div></div>"
            f"<div class=\"net-stat\"><div class=\"v\">{len(mine)}</div><div class=\"k\">{k[1]}</div></div>"
            f"<div class=\"net-stat\"><div class=\"v\">{total_cites}</div><div class=\"k\">{k[2]}</div></div>"
            f"<div class=\"net-stat\"><div class=\"v\">{min(years)}–{max(years)}</div><div class=\"k\">{k[3]}</div></div>"
            "</div>\n```\n", encoding="utf-8")
    print(f"publications: {len(mine)} items, {dict(counts)}, {total_cites} citations; pages for en, es, eu")

if __name__ == "__main__":
    main()
