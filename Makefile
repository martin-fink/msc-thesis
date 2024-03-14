FILE := main
OUT  := build

.PHONY: pdf
pdf: git_ref
	+latexmk -interaction=nonstopmode -outdir="$(OUT)" -pdf -halt-on-error -jobname="$(jobname)" $(FILE)

.PHONY: watch
watch: git_ref
	+latexmk -interaction=nonstopmode -outdir="$(OUT)" -pdf -pvc -halt-on-error -jobname="$(jobname)" $(FILE)

.PHONY: _fachschaft-print
_fachschaft-print:
	@if grep -sq '^TUM-Dev LaTeX-Thesis-Template: twoside$$' $(OUT)/$(FILE).log; then \
		if [ "$(OUT)/fachschaft_print.pdf" -nt "$(OUT)/$(FILE).pdf" ]; then \
			echo "fachschaft_print.pdf is up to date"; \
		else \
			echo "Building fachschaft_print.pdf..."; \
			if ! command -v pdfjam >/dev/null; then \
				echo "PDFJAM not installed. Can not build fachschaft_print.pdf."; \
				rm -f "$(OUT)/_fachschaft_print.pdf"; \
			else \
				pdfjam --twoside --a4paper -o "$(OUT)/fachschaft_print.pdf" "$(OUT)/$(FILE).pdf" 1,3-; \
			fi \
		fi \
	else \
		cp "$(OUT)/$(FILE).pdf" "$(OUT)/fachschaft_print.pdf"; \
	fi;

.PHONY: clean
clean:
	rm -rf $(filter-out $(wildcard $(OUT)/*.pdf), $(wildcard $(OUT)/*))

.PHONY: mrproper
mrproper:
	rm -rf $(OUT) $(wildcard figures/build/*.pdf)

.PHONY: git_ref
git_ref:
	./scripts/get_ref_name.sh > git_ref.tex

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
	DRAWIO := $(shell /usr/bin/env drawio)
endif
ifeq ($(UNAME_S),Darwin)
	DRAWIO := /Applications/draw.io.app/Contents/MacOS/draw.io
endif

FIGURES = $(wildcard figures/sources/*.drawio)
FIGURES_PDFs = $(FIGURES:figures/sources/%.drawio=figures/build/%.pdf)

figures: $(FIGURES_PDFs)

figures/build/%.pdf: figures/sources/%.drawio
	$(DRAWIO) --crop -x -o $@ $<

