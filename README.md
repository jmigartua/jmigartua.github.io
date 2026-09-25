# igartua — personal academic site

Source of the personal website of Josu M. Igartua (Physics, UPV/EHU). Fourth
member of the site family that shares one design system: emissivity.org,
thermomat, igartua / gral-tfg. `theme: none`, one stylesheet
(`assets/styles/theme.css`, graphite ink, amber links, slate kickers), header
and footer partials under `assets/includes/`.

## Build

```sh
python3 tools/generate_publications.py   # publications/index.qmd + _gen/ from _data/publications.yml
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

## Not yet decided

- Hosting: the natural home is the GitHub user site `jmigartua.github.io`
  (which does not exist yet); a custom domain is also possible.
- Languages: English only in this version; Basque and Spanish can follow the
  pattern used on igartua / gral-tfg.
- Post-2020 facts to confirm before publishing: sexenios and quinquenios
  after 2020, the status of the doctoral thesis in progress in 2020, current
  CUED and EAU roles, and the exact date of the 2020 appointment.
