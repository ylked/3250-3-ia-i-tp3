ALL=report.pdf

.phony: all
all: $(ALL)

%.pdf: %.md
	pandoc $^ \
		--standalone \
		--from markdown+smart \
		--to latex \
		--pdf-engine xelatex \
		--lua-filter english.lua \
		--filter pandoc-crossref \
		--citeproc \
		--variable documentclass=article \
		--variable mainfont="Linux Libertine O" \
		--variable sansfont="Linux Biolinum O" \
		--variable monofont="Inconsolata" \
		--output $@

%-cros.pdf: %.md
	pandoc $^ \
		--standalone \
		--from markdown+smart \
		--to latex \
		--pdf-engine xelatex \
		--lua-filter english.lua \
		--filter pandoc-crossref \
		--citeproc \
		--variable documentclass=scrreprt \
		--variable mainfont="Carlito" \
		--variable sansfont="Tinos" \
		--variable monofont="Cousine" \
		--output $@

.PHONY: clean
clean:
	rm -f $(ALL)
