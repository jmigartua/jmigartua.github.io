#!/usr/bin/env python3
"""Generate teaching/index.qmd (en, es, eu) from _data/teaching.yml.

Produces, per language: headline numbers, an SVG timeline of subjects by
institution and centre (bars by academic year, thickness by credits, colour by
language of instruction, hatched for laboratory, outlined for continuations
attested but not itemised), a hover/focus tooltip, and the subject tables.
"""
from __future__ import annotations
import html
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = yaml.safe_load((ROOT / "_data" / "teaching.yml").read_text())
LANGS = ("en", "es", "eu")

S = {
"en": dict(title="Teaching", crumb="teaching",
  desc="Thirty-five academic years of teaching at four institutions: the subjects, the timeline, the course that defines the chair, textbooks and teaching innovation.",
  sub="Thirty-five academic years at four institutions, some forty subjects and courses in three languages, and since 2010 one course taught the way I would have wanted to be taught.",
  intro="The record below comes from the itemised teaching certificates in the dossier for the chair and from the later abbreviated CV. The timeline reads left to right by academic year; each row is a subject, grouped by institution and centre; the colour is the language of instruction, the thickness the credits taught that year. Hover or focus a bar for its details. The full list follows as tables.",
  stats=("academic years", "subjects and courses", "credits taught", "languages of instruction"),
  h_timeline="Timeline of subjects", h_list="Subjects taught", h_tfe="Termodinamika eta Fisika Estatistikoa",
  h_books="Textbooks and teaching material", h_innov="Teaching research and innovation",
  legend=dict(eu="Basque", es="Spanish", en="English", mixed="several languages", lab="laboratory practicals (hatched)", ext="continuing, not itemised by year (outlined)", thick="bar thickness: credits per year"),
  th=("Years", "Subject", "Degree · centre", "Credits / year", "Language", "Type"),
  kinds=dict(theory="lectures and tutoring", lab="laboratory", master="master's and doctorate", tfg="thesis supervision", course="course", organised="organisation", post="post"),
  langs=dict(eu="Basque", es="Spanish", en="English", mixed="Basque, Spanish, English"),
  tip=dict(years="Years", credits="Credits per year", lang="Language", kind="Type", cont="continuing to"),
  years_word="academic years", cap="Figure: subjects taught by academic year, grouped by institution and centre. The data are in the tables below.",
  toc="On this page"),
"es": dict(title="Docencia", crumb="docencia",
  desc="Treinta y cinco cursos de docencia en cuatro instituciones: las asignaturas, la cronología, la asignatura que da nombre a la cátedra, libros de texto e innovación docente.",
  sub="Treinta y cinco cursos académicos en cuatro instituciones, una cuarentena de asignaturas y cursos en tres lenguas y, desde 2010, una asignatura impartida como me habría gustado que me la impartieran.",
  intro="El registro que sigue procede de los certificados itemizados de docencia del dosier de la cátedra y del currículum abreviado posterior. La cronología se lee de izquierda a derecha por curso académico; cada fila es una asignatura, agrupada por institución y centro; el color es la lengua de impartición y el grosor, los créditos impartidos ese curso. Pase el ratón o el foco por una barra para ver sus detalles. La lista completa sigue en forma de tablas.",
  stats=("cursos académicos", "asignaturas y cursos", "créditos impartidos", "lenguas de impartición"),
  h_timeline="Cronología de las asignaturas", h_list="Asignaturas impartidas", h_tfe="Termodinamika eta Fisika Estatistikoa",
  h_books="Libros de texto y material docente", h_innov="Investigación e innovación docente",
  legend=dict(eu="euskera", es="castellano", en="inglés", mixed="varias lenguas", lab="prácticas de laboratorio (rayado)", ext="continúa, no itemizado por curso (contorno)", thick="grosor de la barra: créditos por curso"),
  th=("Cursos", "Asignatura", "Titulación · centro", "Créditos / curso", "Lengua", "Tipo"),
  kinds=dict(theory="clases y tutorías", lab="laboratorio", master="máster y doctorado", tfg="dirección de trabajos", course="curso", organised="organización", post="cargo"),
  langs=dict(eu="euskera", es="castellano", en="inglés", mixed="euskera, castellano, inglés"),
  tip=dict(years="Cursos", credits="Créditos por curso", lang="Lengua", kind="Tipo", cont="continúa hasta"),
  years_word="cursos", cap="Figura: asignaturas impartidas por curso académico, agrupadas por institución y centro. Los datos están en las tablas siguientes.",
  toc="En esta página"),
"eu": dict(title="Irakaskuntza", crumb="irakaskuntza",
  desc="Hogeita hamabost ikasturte irakasten lau erakundetan: irakasgaiak, kronologia, katedrari izena ematen dion irakasgaia, testuliburuak eta irakaskuntza-berrikuntza.",
  sub="Hogeita hamabost ikasturte lau erakundetan, berrogei bat irakasgai eta ikastaro hiru hizkuntzatan, eta 2010etik irakasgai bakarra, niri irakatsi izana gustatuko litzaidakeen moduan emana.",
  intro="Beheko erregistroa katedrako dosierraren irakaskuntza-ziurtagiri xehatuetatik eta geroagoko curriculum laburtutik dator. Kronologia ezkerretik eskuinera irakurtzen da ikasturteka; errenkada bakoitza irakasgai bat da, erakundeka eta zentroka taldekatuta; kolorea irakaskuntza-hizkuntza da eta lodiera, ikasturte horretan emandako kredituak. Jarri sagua edo fokua barra baten gainean bere xehetasunak ikusteko. Zerrenda osoa taula moduan dator jarraian.",
  stats=("ikasturte", "irakasgai eta ikastaro", "emandako kreditu", "irakaskuntza-hizkuntza"),
  h_timeline="Irakasgaien kronologia", h_list="Emandako irakasgaiak", h_tfe="Termodinamika eta Fisika Estatistikoa",
  h_books="Testuliburuak eta irakas-materiala", h_innov="Irakaskuntza-ikerketa eta -berrikuntza",
  legend=dict(eu="euskara", es="gaztelania", en="ingelesa", mixed="hainbat hizkuntza", lab="laborategiko praktikak (marratua)", ext="jarraitzen du, ikasturteka xehatu gabe (ingerada)", thick="barraren lodiera: kredituak ikasturteko"),
  th=("Ikasturteak", "Irakasgaia", "Titulazioa · zentroa", "Kredituak / ikasturte", "Hizkuntza", "Mota"),
  kinds=dict(theory="eskolak eta tutoretzak", lab="laborategia", master="masterra eta doktoregoa", tfg="lanen zuzendaritza", course="ikastaroa", organised="antolaketa", post="kargua"),
  langs=dict(eu="euskara", es="gaztelania", en="ingelesa", mixed="euskara, gaztelania, ingelesa"),
  tip=dict(years="Ikasturteak", credits="Kredituak ikasturteko", lang="Hizkuntza", kind="Mota", cont="jarraitzen du honaino"),
  years_word="ikasturte", cap="Irudia: emandako irakasgaiak ikasturteka, erakundeka eta zentroka taldekatuta. Datuak beheko tauletan daude.",
  toc="Orri honetan"),
}

# Prose carried over from the previous version of the pages (unchanged).
PROSE = {
"en": dict(
 tfe="""A twelve-credit, full-year course in the third year of the Physics degree and the Double Degree in Physics and Electronic Engineering, taught in Basque to sixty or seventy students a year. It is the course named in my chair and the one I have coordinated since 2010. I introduced thermodynamics and its neighbouring subjects in Basque at this university and prepared the first complete set of materials for them, so the course also carries that history. The way it runs has been stable for a decade and is documented in public:

- **A daily class log** (egunkaria): what was done in every session, published as it happens, so nobody has to guess what the course expects.
- **Short tests** (azterketatxoak) through the year rather than one examination, with a public rubric and worked examples of how answers are marked.
- **Concept maps and reading maps** for both semesters, so the structure of the subject is visible before the details.
- **Jupyter notebooks in Basque** as the working documents: derivations, exercises from Zemansky and the students' own computations in one place.
- **MinervaLab**, the interactive simulation laboratory for first-order phase transitions and the van der Waals fluid, used in class for the part students find hardest.

The course material lives in yearly GitHub repositories. The bachelor's theses that come out of it, the ones in progress and the proposals for the coming year are on [igartua / gral-tfg](https://jmigartua.github.io/tfgs-website/), together with the [preparation manual](https://jmigartua.github.io/tfgs-website/preparing/) I wrote for students starting a thesis.""",
 books="""Twenty entries with ISBN in the dossier: three university-level textbooks and seven books or extended teaching materials for undergraduates as author or translator, and thirteen more as translator, reviser or contributor, mostly in Basque, which made it possible to teach the physics curriculum entirely in that language. Among them the translation and scientific revision of Fishbane, Gasiorowicz and Thornton's *Physics for Scientists and Engineers* (2008; two volumes, 2014), the Elhuyar encyclopaedic dictionary of science and technology (2009), *Mekanika Estatistikoa* and *Forma eta Fluxua* for the Basque Summer University, the *Fisika Praktikak* laboratory manual, the *Fisikaz Blai* booklets, *Iraunkortasuna*, the Lur physics and chemistry dictionary, and the physics and chemistry textbooks for Edebé (2008–2015).""",
 innov="""Eighteen teaching-innovation projects at UPV/EHU, including the one I led on the electronic laboratory notebook with Jupyter (PIE 2018–2019), and physics-education papers at CINTE 2016, CSEDU 2017, GIREP 2018 and the RSEF biennial meeting of 2019. Thirty-eight training courses, eight hundred and twenty hours in all, and the three Terminologia Sareak Ehunduz terminology programmes. Teaching evaluated in the top band of DOCENTIAZ, 82.4 and 95.7 points in 2008–2013 and 2013–2018. Coordinator of the Physics Olympiad, tutor in the tutorial action programme, and a regular at open days, the science week and the summer science campus. Since 2017, coordinator of the design and preparation of the physics examination for university entrance in the Basque Country, which has turned into a data project of its own on how the examination behaves across Spain."""),
"es": dict(
 tfe="""Una asignatura anual de doce créditos en tercer curso del Grado en Física y del Doble Grado en Física e Ingeniería Electrónica, impartida en euskera a sesenta o setenta estudiantes al año. Es la asignatura que da nombre a mi cátedra y la que coordino desde 2010. Introduje la termodinámica y las materias afines en euskera en esta universidad y preparé el primer conjunto completo de materiales para ellas, de modo que la asignatura arrastra también esa historia. Su funcionamiento lleva una década estable y está documentado en público:

- **Un diario de clase** (egunkaria): qué se ha hecho en cada sesión, publicado sobre la marcha, para que nadie tenga que adivinar qué espera la asignatura.
- **Pruebas cortas** (azterketatxoak) a lo largo del año en lugar de un único examen, con una rúbrica pública y ejemplos resueltos de cómo se corrigen las respuestas.
- **Mapas conceptuales y mapas de lectura** de los dos cuatrimestres, para que la estructura de la materia sea visible antes que los detalles.
- **Cuadernos Jupyter en euskera** como documentos de trabajo: deducciones, ejercicios de Zemansky y los cálculos propios de los estudiantes en un mismo lugar.
- **MinervaLab**, el laboratorio interactivo de simulación de transiciones de fase de primer orden y del fluido de van der Waals, usado en clase para la parte que más cuesta a los estudiantes.

El material de la asignatura vive en repositorios anuales de GitHub. Los trabajos de fin de grado que salen de ella, los que están en curso y las propuestas para el próximo año están en [igartua / gral-tfg](https://jmigartua.github.io/tfgs-website/es/), junto con el [manual de preparación](https://jmigartua.github.io/tfgs-website/preparing/) que escribí para quien empieza un trabajo.""",
 books="""Veinte entradas con ISBN en el dosier: tres libros de texto universitarios y siete libros o materiales docentes extensos para estudiantes de grado como autor o traductor, y trece más como traductor, revisor o colaborador, en su mayoría en euskera, que hicieron posible impartir el plan de estudios de física íntegramente en esa lengua. Entre ellos, la traducción y revisión científica del *Física para ciencias e ingeniería* de Fishbane, Gasiorowicz y Thornton (2008; dos volúmenes, 2014), el diccionario enciclopédico de ciencia y tecnología de Elhuyar (2009), *Mekanika Estatistikoa* y *Forma eta Fluxua* para la Universidad Vasca de Verano, el manual de laboratorio *Fisika Praktikak*, los cuadernos *Fisikaz Blai*, *Iraunkortasuna*, el diccionario de física y química de Lur y los libros de texto de física y química para Edebé (2008–2015).""",
 innov="""Dieciocho proyectos de innovación docente en la UPV/EHU, incluido el que dirigí sobre el cuaderno de laboratorio electrónico con Jupyter (PIE 2018–2019), y artículos de didáctica de la física en CINTE 2016, CSEDU 2017, GIREP 2018 y la reunión bienal de la RSEF de 2019. Treinta y ocho cursos de formación, ochocientas veinte horas en total, y los tres programas de terminología Terminologia Sareak Ehunduz. Docencia evaluada en la banda superior de DOCENTIAZ, 82,4 y 95,7 puntos en 2008–2013 y 2013–2018. Coordinador de la Olimpiada de Física, tutor del programa de acción tutorial y presencia habitual en jornadas de puertas abiertas, la semana de la ciencia y el campus científico de verano. Desde 2017, coordinador del diseño y preparación del examen de física de acceso a la universidad en el País Vasco, que se ha convertido en un proyecto de datos propio sobre cómo se comporta el examen en toda España."""),
"eu": dict(
 tfe="""Hamabi kredituko urteko irakasgaia Fisikako Graduko eta Fisikako eta Ingeniaritza Elektronikoko Gradu Bikoitzeko hirugarren mailan, euskaraz emana urtean hirurogei edo hirurogeita hamar ikasleri. Nire katedrari izena ematen dion irakasgaia da eta 2010etik koordinatzen dudana. Termodinamika eta inguruko gaiak euskaraz sartu nituen unibertsitate honetan eta horietarako lehen material-multzo osoa prestatu nuen, beraz irakasgaiak historia hori ere badakar. Bere funtzionamendua hamarkada batez egonkorra izan da eta publikoki dokumentatuta dago:

- **Eguneroko klase-egunkaria**: saio bakoitzean zer egin den, unean bertan argitaratua, inork asmatu behar ez dezan irakasgaiak zer espero duen.
- **Azterketatxoak** urtean zehar azterketa bakarraren ordez, errubrika publiko batekin eta erantzunak nola zuzentzen diren erakusten duten adibide ebatziekin.
- **Kontzeptu-mapak eta irakurketa-mapak** bi lauhilekoetarako, gaiaren egitura xehetasunen aurretik ikusgai egon dadin.
- **Jupyter koadernoak euskaraz** lan-dokumentu gisa: dedukzioak, Zemanskyren ariketak eta ikasleen beren kalkuluak toki berean.
- **MinervaLab**, lehen ordenako fase-trantsizioen eta van der Waals fluidoaren simulazio-laborategi interaktiboa, ikasgelan erabilia ikasleei gehien kostatzen zaien zatirako.

Irakasgaiaren materiala urteroko GitHub biltegietan bizi da. Hortik ateratzen diren gradu amaierako lanak, martxan daudenak eta datorren urterako proposamenak [igartua / gral-tfg](https://jmigartua.github.io/tfgs-website/eu/) webgunean daude, lan bat hasten duenarentzat idatzi nuen [prestaketa eskuliburuarekin](https://jmigartua.github.io/tfgs-website/eu/preparing/) batera.""",
 books="""Hogei sarrera ISBNarekin dosierrean: hiru unibertsitate-mailako testuliburu eta zazpi liburu edo irakas-material zabal graduko ikasleentzat egile edo itzultzaile gisa, eta beste hamahiru itzultzaile, berrikusle edo laguntzaile gisa, gehienak euskaraz, fisikako ikasketa-plana osorik hizkuntza horretan irakastea ahalbidetu zutenak. Horien artean, Fishbane, Gasiorowicz eta Thorntonen *Fisika zientzialari eta ingeniarientzat* liburuaren itzulpena eta berrikuspen zientifikoa (2008; bi liburuki, 2014), Elhuyarren zientzia eta teknologiaren hiztegi entziklopedikoa (2009), *Mekanika Estatistikoa* eta *Forma eta Fluxua* Udako Euskal Unibertsitaterako, *Fisika Praktikak* laborategi-eskuliburua, *Fisikaz Blai* koadernoak, *Iraunkortasuna*, Lur argitaletxearen fisika eta kimika hiztegia eta Edebérentzako fisika eta kimikako testuliburuak (2008–2015).""",
 innov="""Hemezortzi irakaskuntza-berrikuntzako proiektu UPV/EHUn, Jupyterrekin laborategi-koaderno elektronikoari buruz zuzendu nuena barne (PIE 2018–2019), eta fisikaren didaktikako artikuluak CINTE 2016, CSEDU 2017, GIREP 2018 eta RSEFen 2019ko bilera bienalean. Hogeita hemezortzi prestakuntza-ikastaro, zortziehun eta hogei ordu guztira, eta Terminologia Sareak Ehunduz hiru programak. Irakaskuntza DOCENTIAZen goiko mailan ebaluatua, 82,4 eta 95,7 puntu 2008–2013 eta 2013–2018 aldietan. Fisika Olinpiadaren koordinatzailea, tutoretza-ekintzako programaren tutorea eta ohiko presentzia ate irekien jardunaldietan, zientziaren astean eta udako zientzia-campusean. 2017tik, Euskadiko unibertsitatera sartzeko fisikako azterketaren diseinuaren eta prestaketaren koordinatzailea, eta hori azterketak Espainia osoan nola jokatzen duen aztertzen duen datu-proiektu bihurtu da."""),
}

TOC_JS = '''<script>
(function () {
  var main = document.querySelector(".article-grid > .page-article");
  var list = document.getElementById("docs-toc-list");
  if (!main || !list) return;
  var heads = main.querySelectorAll("h2, h3");
  heads.forEach(function (h) {
    if (!h.id) return;
    var li = document.createElement("li"); li.className = h.tagName === "H3" ? "l3" : "l2";
    var a = document.createElement("a"); a.href = "#" + h.id; a.textContent = h.textContent;
    li.appendChild(a); list.appendChild(li);
  });
  if (!list.children.length) { list.parentNode.hidden = true; return; }
  var links = list.querySelectorAll("a");
  var mark = function () {
    var y = window.scrollY + 80, cur = null;
    heads.forEach(function (h) { if (h.id && h.getBoundingClientRect().top + window.scrollY <= y) cur = h.id; });
    links.forEach(function (a) { a.classList.toggle("current", cur !== null && a.getAttribute("href") === "#" + cur); });
  };
  window.addEventListener("scroll", mark, { passive: true }); mark();
})();
</script>'''

TIP_JS = '''<script>
(function () {
  var wrap = document.getElementById("tl-wrap"); if (!wrap) return;
  var tip = document.getElementById("tl-tip");
  function show(el, x, y) {
    tip.innerHTML = el.getAttribute("data-tip");
    tip.hidden = false;
    var r = wrap.getBoundingClientRect(), tw = tip.offsetWidth, th = tip.offsetHeight;
    var left = x - r.left + 14, top = y - r.top + 14;
    if (left + tw > r.width - 8) left = x - r.left - tw - 14;
    if (top + th > wrap.scrollHeight - 8) top = y - r.top - th - 14;
    tip.style.left = Math.max(4, left) + "px"; tip.style.top = Math.max(4, top) + "px";
  }
  wrap.querySelectorAll(".tl-bar").forEach(function (el) {
    el.addEventListener("mousemove", function (e) { show(el, e.clientX, e.clientY); });
    el.addEventListener("mouseleave", function () { tip.hidden = true; });
    el.addEventListener("focus", function () { var b = el.getBoundingClientRect(); show(el, b.left + b.width / 2, b.bottom); });
    el.addEventListener("blur", function () { tip.hidden = true; });
  });
})();
</script>'''

def yr(y):  # 2003 -> "2003/04"
    return f"{y}/{str(y + 1)[-2:]}"

def spans_text(subj):
    parts = []
    for a, b in subj["spans"]:
        parts.append(yr(a) if a == b else f"{yr(a)}–{yr(b)}")
    return ", ".join(parts)

def years_of(subj):
    ys = []
    for a, b in subj["spans"]:
        ys += list(range(a, b + 1))
    return ys

def credits_of(subj, y):
    c = subj.get("credits", 0)
    if isinstance(c, dict):
        return float(c.get(y, 0))
    return float(c)

def credits_text(subj):
    c = subj.get("credits", 0)
    if isinstance(c, dict):
        vals = sorted(set(float(v) for v in c.values() if float(v) > 0))
        if not vals: return "—"
        return f"{vals[0]:g}" if len(vals) == 1 else f"{vals[0]:g}–{vals[-1]:g}"
    return f"{float(c):g}" if float(c) > 0 else "—"

def fmt_int(n):
    return f"{n:,}".replace(",", " ")

# ---------------------------------------------------------------- numbers
def numbers():
    subs = [s for inst in DATA["institutions"] for c in inst["centres"] for s in c["subjects"]]
    years = set()
    credits = 0.0
    n_subjects = 0
    for s in subs:
        for y in years_of(s):
            years.add(y); credits += credits_of(s, y)
        if s["kind"] in ("theory", "lab", "master", "tfg"):
            n_subjects += 1
        elif s["kind"] == "course":
            n_subjects += len(s["degree"]["en"].split("·"))
    y0, y1 = DATA["axis"]["start"], DATA["axis"]["end"]
    return dict(years=y1 - y0 + 1, y0=y0, y1=y1, subjects=n_subjects, credits=int(round(credits)), langs="eu · es · en")

# ---------------------------------------------------------------- timeline
LABEL_W, YEAR_W, LANE_H, INST_H, CEN_H, TOP = 262, 16, 21, 30, 22, 30

def truncate(s, n=42):
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"

def build_svg(lang):
    t = S[lang]
    y0, y1 = DATA["axis"]["start"], DATA["axis"]["end"]
    ny = y1 - y0 + 1
    W = LABEL_W + ny * YEAR_W + 44
    X = lambda y: LABEL_W + (y - y0) * YEAR_W
    rows = []  # (type, payload)
    for inst in DATA["institutions"]:
        rows.append(("inst", inst))
        for c in inst["centres"]:
            rows.append(("cen", c))
            for s in c["subjects"]:
                rows.append(("sub", (inst, c, s)))
    H = TOP + sum(INST_H if r[0] == "inst" else CEN_H if r[0] == "cen" else LANE_H for r in rows) + 28
    out = [f'<svg class="tl" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{html.escape(t["h_timeline"])}">']
    out.append('<defs>' + "".join(
        f'<pattern id="hatch-{k}" patternUnits="userSpaceOnUse" width="6" height="6" patternTransform="rotate(45)"><rect width="6" height="6" fill="var(--tl-{k})" opacity="0.35"/><line x1="0" y1="0" x2="0" y2="6" stroke="var(--tl-{k})" stroke-width="2"/></pattern>'
        for k in ("eu", "es", "en", "mixed")) + '</defs>')
    # gridlines and year labels
    for y in range(y0, y1 + 1):
        x = X(y)
        major = (y % 5 == 0) or y == y0
        out.append(f'<line class="tl-grid{" major" if major else ""}" x1="{x}" y1="{TOP - 6}" x2="{x}" y2="{H - 22}"/>')
        if major:
            out.append(f'<text class="tl-year" x="{x + 2}" y="{TOP - 10}">{y}</text>')
            out.append(f'<text class="tl-year" x="{x + 2}" y="{H - 8}">{y}</text>')
    out.append(f'<line class="tl-grid major" x1="{X(y1 + 1)}" y1="{TOP - 6}" x2="{X(y1 + 1)}" y2="{H - 22}"/>')
    yy = TOP
    for kind, p in rows:
        if kind == "inst":
            out.append(f'<rect class="tl-band" x="0" y="{yy}" width="{W}" height="{INST_H}"/>')
            out.append(f'<text class="tl-inst" x="8" y="{yy + 20}">{html.escape(p["name"][lang])}</text>')
            yy += INST_H
        elif kind == "cen":
            out.append(f'<text class="tl-cen" x="16" y="{yy + 15}">{html.escape(p["name"][lang])}</text>')
            out.append(f'<line class="tl-rule" x1="16" y1="{yy + CEN_H - 1}" x2="{W - 8}" y2="{yy + CEN_H - 1}"/>')
            yy += CEN_H
        else:
            inst, c, s = p
            mid = yy + LANE_H / 2
            out.append(f'<text class="tl-lab" x="{LABEL_W - 10}" y="{mid + 4}" text-anchor="end">{html.escape(truncate(s["name"][lang]))}</text>')
            k = s["lang"]
            tip = (f'<b>{html.escape(s["name"][lang])}</b><br>{html.escape(s["degree"][lang])}<br><span class="m">{html.escape(c["name"][lang])} · {html.escape(inst["name"][lang])}</span>'
                   f'<br>{t["tip"]["years"]}: {spans_text(s)}' + (f' · {t["tip"]["cont"]} {yr(s["extend"])}' if s.get("extend") else "")
                   + (f'<br>{t["tip"]["credits"]}: {credits_text(s)}' if credits_text(s) != "—" else "")
                   + f'<br>{t["tip"]["lang"]}: {t["langs"][k]} · {t["tip"]["kind"]}: {t["kinds"][s["kind"]]}'
                   + (f'<br><span class="m">{html.escape(s["note"][lang])}</span>' if s.get("note") else ""))
            tip_attr = html.escape(tip, quote=True)
            aria = html.escape(f'{s["name"][lang]}, {spans_text(s)}', quote=True)
            for a, b in s["spans"]:
                # one rect per year so thickness follows credits
                for y in range(a, b + 1):
                    cr = credits_of(s, y)
                    h = 6 if cr <= 0 else max(4, min(16, 4 + 12 * cr / 12))
                    fill = f'url(#hatch-{k})' if s["kind"] == "lab" else f'var(--tl-{k})'
                    out.append(f'<rect class="tl-bar" tabindex="0" data-tip="{tip_attr}" aria-label="{aria}" x="{X(y) + 1}" y="{mid - h / 2:.1f}" width="{YEAR_W - 2}" height="{h:.1f}" rx="2" fill="{fill}"/>')
            if s.get("extend"):
                last = s["spans"][-1][1]
                cr = credits_of(s, last); h = 6 if cr <= 0 else max(4, min(16, 4 + 12 * cr / 12))
                out.append(f'<rect class="tl-bar tl-ext" tabindex="0" data-tip="{tip_attr}" aria-label="{aria}" x="{X(last + 1) + 1}" y="{mid - h / 2:.1f}" width="{(s["extend"] - last) * YEAR_W - 2}" height="{h:.1f}" rx="2" fill="none" stroke="var(--tl-{k})"/>')
            yy += LANE_H
    out.append("</svg>")
    L = t["legend"]
    legend = ('<div class="tl-legend">' + "".join(f'<span><i style="background:var(--tl-{k})"></i>{L[k]}</span>' for k in ("eu", "es", "en", "mixed"))
              + f'<span><i class="hatch"></i>{L["lab"]}</span><span><i class="ext"></i>{L["ext"]}</span><span class="note">{L["thick"]}</span></div>')
    return f'<figure class="tl-figure"><div class="tl-wrap" id="tl-wrap">{"".join(out)}<div class="tl-tip" id="tl-tip" hidden></div></div>{legend}<figcaption>{t["cap"]}</figcaption></figure>'

# ---------------------------------------------------------------- tables
def build_tables(lang):
    t = S[lang]; out = []
    for inst in DATA["institutions"]:
        out.append(f'<h3 id="list-{inst["id"]}">{html.escape(inst["name"][lang])}</h3>')
        out.append('<div class="table-wrap"><table><thead><tr>' + "".join(f"<th>{h}</th>" for h in t["th"]) + "</tr></thead><tbody>")
        for c in inst["centres"]:
            for s in c["subjects"]:
                deg = f'{html.escape(s["degree"][lang])}<br><span class="m">{html.escape(c["name"][lang])}</span>'
                note = f'<br><span class="m">{html.escape(s["note"][lang])}</span>' if s.get("note") else ""
                ext = f' · {t["tip"]["cont"]} {yr(s["extend"])}' if s.get("extend") else ""
                out.append(f'<tr><td>{spans_text(s)}{ext}</td><td>{html.escape(s["name"][lang])}{note}</td><td>{deg}</td><td>{credits_text(s)}</td><td>{t["langs"][s["lang"]]}</td><td>{t["kinds"][s["kind"]]}</td></tr>')
        out.append("</tbody></table></div>")
    return "\n".join(out)

# ---------------------------------------------------------------- page
def build(lang):
    t, P, n = S[lang], PROSE[lang], numbers()
    stats = (f'<div class="net-stats"><div class="net-stat"><div class="v">{n["years"]}</div><div class="k">{t["stats"][0]} · {n["y0"]}–{n["y1"] + 1}</div></div>'
             f'<div class="net-stat"><div class="v">{n["subjects"]}</div><div class="k">{t["stats"][1]}</div></div>'
             f'<div class="net-stat"><div class="v">{fmt_int(n["credits"])}</div><div class="k">{t["stats"][2]}</div></div>'
             f'<div class="net-stat"><div class="v">3</div><div class="k">{t["stats"][3]} · {n["langs"]}</div></div></div>')
    return f"""---
title: "{t['title']}"
description: "{t['desc']}"
title-block-style: none
page-layout: full
toc: false
---

```{{=html}}
<div class="crumbs"><a href="../index.html">igartua</a> / {t['crumb']}</div>
<div class="article-grid">
<article class="page-article">
<h1>{t['title']}</h1>
<p class="sub">{t['sub']}</p>
{stats}
```

{t['intro']}

## {t['h_timeline']} {{#timeline}}

```{{=html}}
{build_svg(lang)}
{TIP_JS}
```

## {t['h_tfe']} {{#tfe}}

{P['tfe']}

## {t['h_list']} {{#subjects}}

```{{=html}}
{build_tables(lang)}
```

## {t['h_books']} {{#books}}

{P['books']}

## {t['h_innov']} {{#innovation}}

{P['innov']}

```{{=html}}
</article>
<aside class="docs-toc" aria-label="{t['toc']}"><div class="t">{t['toc']}</div><ol id="docs-toc-list"></ol></aside>
</div>
{TOC_JS}
```
"""

if __name__ == "__main__":
    for lang in LANGS:
        p = ROOT / ("teaching/index.qmd" if lang == "en" else f"{lang}/teaching/index.qmd")
        p.write_text(build(lang))
        print("wrote", p)
    print(numbers())
