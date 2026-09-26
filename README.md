# igartua — personal academic site

Source of the personal website of Josu M. Igartua (Physics, UPV/EHU). Fourth
member of the site family that shares one design system: emissivity.org,
thermomat, igartua / gral-tfg. `theme: none`, one stylesheet
(`assets/styles/theme.css`, graphite ink, amber links, slate kickers), header
and footer partials under `assets/includes/`.

## Build

```sh
python3 tools/generate_publications.py   # publications/index.qmd + _gen/ from _data/publications.yml
python3 tools/generate_teaching.py       # teaching/index.qmd ×3 (timeline, tables) from _data/teaching.yml
quarto render                            # → _site/
```

`_data/publications.yml` is a copy of the thermomat-site registry
(`thermomat-site/_data/publications.yml`, OpenAlex-synchronised and curated
there). Re-copy it to refresh; only items whose `members` include
`igartua-josu` are used.

## Sources and provenance

Career, theses, service and teaching facts come from the 2020 accreditation
documentation (private Jupyter Book, frozen October 2020) and were checked
against the thermomat people registry. Counts stated "as of 2020" in the text
are exactly that. Figures in `assets/images/` are the author's own research
figures from that documentation; the portrait is `Josu.png` from the same
source. No certificate, service record, ID number, address or third-party
photograph from the 2020 documentation is included here, by design.

## Languages and facts

English at the root, Spanish under `es/`, Basque under `eu/`; each directory's
`_metadata.yml` sets `lang`, and the shared header and footer partials switch
their navigation by `<html lang>`. Facts up to October 2020 come from the
accreditation dossier; later facts (appointment 2 November 2020, six sexenios
and six quinquenios, two doctoral theses in progress, recent projects and
contracts, continuing CUED and PAU roles) come from the 2026 abbreviated CV
and the author's own confirmation.

## Hosting

Published as the GitHub user site at https://jmigartua.github.io/ by the
workflow in `.github/workflows/pages.yml` (Quarto render on Actions, deployed
with `actions/deploy-pages`). The theses site stays at
https://jmigartua.github.io/tfgs-website/ and is linked from here.
