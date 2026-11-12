# Quarto mathematical research-note template

A reusable writing system adapted from the workflow of [markov-controlled-sa](https://github.com/jsimbadev/markov-controlled-sa). It provides modular Quarto authoring, HTML and LuaLaTeX PDF output, native or Docker preview, bibliography and macro management, numbered mathematical results, source checks, and GitHub Actions.

## Quick start

Requirements: Quarto >=1.6, Python >=3.10, GNU Make, LuaLaTeX (or Docker Compose).

```sh
make check-source         # includes, citations, references, tests; no Quarto required
make preview              # auto-reloading HTML at http://127.0.0.1:4200
make html                 # _output/index.html
make pdf                  # _output/index.pdf using LuaLaTeX
make check                # source tests + both renders + HTML/PDF validation
make arxiv                # XeLaTeX render and _output/arxiv-source.zip
make USE_DOCKER=1 preview # same environment without native Quarto/TeX
```

Preview automatically watches included manuscript sections, appendices, figures, macros, and the bibliography. Set `PORT=4300` to change the preview port.

## Authoring

- `index.qmd` owns metadata, section includes and bibliography.
- `sections/*.qmd` and `appendices/*.qmd` hold the paper's mathematics.
- Use labels such as `{#eq-poisson}`, `{#lem-poisson}`, and references such as `@eq-poisson`; do not hardcode result numbers.
- Use Quarto theorem environments (`::: {#thm-main}` followed by a `##` heading) and proof blocks (`::: {.proof}`).
- The Lua filter maps `asm-` labels to numbered Assumption environments in both formats.
- `references.bib` is the one bibliography file. Zotero Better BibTeX can auto-export directly to it.
- `macros.tex` is the canonical LaTeX vocabulary. `make sync-macros` updates HTML MathJax macros.
- Track work in `notes/proof-obligations.md`; the internal notes are not part of the paper.

The build uses an A4, 11-point article PDF, semantic cross-references, linked citations, and a restrained HTML theme.

## arXiv packaging

`make arxiv` uses `_quarto-arxiv.yml` to render with XeLaTeX and builds a *candidate* source archive. You must extract `_output/arxiv-source.zip`, compile the extracted `index.tex` independently, inspect any external assets and references, and follow current arXiv rules. This target is not a submission guarantee.

## CI

Pushing to `main` triggers `.github/workflows/render-html.yml`, which runs checks, builds HTML + PDF, and commits rendered outputs back to the same branch. This preserves the existing research-note workflow. The build job uses Quarto's setup action and TinyTeX.

## Start a new paper

In GitHub, mark this repository as a **Template repository** under Settings > General, and choose **Use this template**. Replace `index.qmd`, the `sections/` files, and proof obligations while retaining the tooling and source checks.

This repository deliberately contains only example mathematical text, not a real theorem or paper.
