.DEFAULT_GOAL := render
.NOTPARALLEL:

USE_DOCKER ?= 0
PORT ?= 4200

.PHONY: preview html pdf render check check-source arxiv clean sync-macros

ifeq ($(USE_DOCKER),1)
DOCKER_COMPOSE ?= docker compose
export LOCAL_UID := $(shell id -u)
export LOCAL_GID := $(shell id -g)
export PORT
preview:
	$(DOCKER_COMPOSE) up --build tools
html pdf render check check-source arxiv clean sync-macros:
	$(DOCKER_COMPOSE) run --build --rm -T tools make $@
else
QUARTO ?= quarto
PYTHON ?= python3
PREVIEW_HOST ?= 127.0.0.1
PREVIEW_FLAGS ?=
export XDG_CACHE_HOME ?= $(CURDIR)/.quarto/cache
export TEXMFVAR ?= _output/tex-var
export TEXMFCACHE ?= _output/tex-cache

preview: sync-macros
	$(PYTHON) scripts/preview.py --quarto "$(QUARTO)" --host $(PREVIEW_HOST) --port $(PORT) $(PREVIEW_FLAGS)
html: sync-macros
	$(QUARTO) render index.qmd --to html
pdf: sync-macros
	$(QUARTO) render index.qmd --to pdf
render: sync-macros
	$(QUARTO) render index.qmd --to html
	$(QUARTO) render index.qmd --to pdf
sync-macros:
	$(PYTHON) scripts/sync-macros.py
check-source:
	$(PYTHON) scripts/sync-macros.py --check
	$(PYTHON) scripts/check-source.py
	$(PYTHON) -m unittest discover -s tests -v
check: check-source
	$(MAKE) render
	$(PYTHON) scripts/check-render.py
arxiv: sync-macros
	$(QUARTO) render index.qmd --to pdf --profile arxiv
	$(PYTHON) scripts/pack-arxiv.py
clean:
	$(PYTHON) scripts/clean.py
endif
