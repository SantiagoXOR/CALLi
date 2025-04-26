# Makefile para generación de documentación

.PHONY: all clean html validate diagrams linkcheck serve

# Variables
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build
PYTHON        = python3

all: validate linkcheck html

html:
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

validate:
	@echo "Validando diagramas..."
	@$(PYTHON) scripts/validate_diagrams.py
	@echo "Validando enlaces internos..."
	@$(PYTHON) scripts/validate_links.py

linkcheck:
	@echo "Verificando enlaces externos..."
	@$(SPHINXBUILD) -b linkcheck "$(SOURCEDIR)" "$(BUILDDIR)/linkcheck"

diagrams:
	@echo "Generando diagramas..."
	@find diagrams -name "*.puml" -exec plantuml {} \;

clean:
	@rm -rf $(BUILDDIR)/*
	@find diagrams -name "*.png" -delete
	@find diagrams -name "*.svg" -delete

serve:
	@echo "Iniciando servidor de documentación..."
	@cd $(BUILDDIR)/html && python -m http.server 8000
