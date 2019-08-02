# Things in this Makefile have been taken from http://matt.might.net/articles/intro-to-make/

all: thesis.pdf 


thesis.pdf: *tex *pgf 
	pdflatex thesis.tex
	bibtex thesis.aux # This is a hack
	pdflatex thesis.tex
	pdflatex thesis.tex
	evince thesis.pdf &

clean:
	rm *~
	rm *aux	
	rm *pdf
	rm *log
	rm *bbl
	rm *blg
	rm *out
	rm *toc
	rm *dvi

supervisor:
	# Based on https://tex.stackexchange.com/a/1495
	pdflatex  "\def\supervisorversion{1}\def\revisionversion{1} \input{thesis.tex}" 
	bibtex thesis.aux
	pdflatex  "\def\supervisorversion{1}\def\revisionversion{1} \input{thesis.tex}"
	pdflatex  "\def\supervisorversion{1}\def\revisionversion{1} \input{thesis.tex}" 

	touch thesis.tex # This means next time I try and make the thesis, make runs

	evince thesis.pdf &

revision:
# Based on https://tex.stackexchange.com/a/1495
	pdflatex  "\def\revisionversion{1} \input{thesis.tex}" 
	bibtex thesis.aux
	pdflatex  "\def\revisionversion{1} \input{thesis.tex}"
	pdflatex  "\def\revisionversion{1} \input{thesis.tex}" 

	touch thesis.tex # This means next time I try and make the thesis, make runs

	evince thesis.pdf &

# Check style:
# From http://matt.might.net/articles/shell-scripts-for-passive-voice-weasel-words-duplicates/
proof:
	echo "weasel words: "
	sh bin/weasel *.tex
	echo
	echo "passive voice: "
	sh bin/passive *.tex
	echo
	echo "duplicates: "
	perl bin/dups *.tex

spell:
	# Next bit of code inspired by syntax in from https://stackoverflow.com/a/1490961 - no idea why this works and what I was trying doesn't
	for file in $(shell ls *tex); do \
	aspell --mode=tex -c $$file ; \
	done

l1-table.tex: l1-plot-and-table.py ~/Documents/running-code/running-nbpc/nbpc-scaling-l1/output/*csv
	python l1-plot-and-table.py

l1*.pgf: l1-plot-and-table.py ~/Documents/running-code/running-nbpc/nbpc-scaling-l1/output/*csv
	python l1-plot-and-table.py

pollution*.pgf: pollution-figure.py
	python pollution-figure.py

interpolation*.pgf: interpolation-figure.py
	python interpolation-figure.py

GMRES.pgf: GMRES.pickle gmres-blow-up-plot.py
	python gmres-blow-up-plot.py
