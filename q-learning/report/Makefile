.PHONY: clean all
FILE=mathiabo_project_5

all: $(FILE).pdf

$(FILE).pdf: $(FILE).tex
	pdflatex $(FILE).tex
	bibtex $(FILE).aux
	pdflatex $(FILE).tex
	pdflatex $(FILE).tex

clean:
	rm -rf *.aux *.bbl *.blg *dvi *.log *.out *.synctex.gz *.toc *.lot *.lof
