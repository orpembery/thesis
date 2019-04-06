# Things in this Makefile have been taken from http://matt.might.net/articles/intro-to-make/

.SUFFIXES: .tex .pdf

all: thesis.pdf 
	evince thesis.pdf &
	touch thesis.tex # This is a hack, as I can't work out how to get make to depend on all the tex files

.tex.pdf:
	pdflatex $<
	bibtex thesis.aux # This is a hack
	pdflatex $<
	pdflatex $<
	#evince thesis.pdf # As is this
	#touch $<

clean:
	rm *pdf *log *bbl *blg *dvi *out *aux

supervisor:
# Based on https://tex.stackexchange.com/a/1495
	pdflatex  "\def\supervisorversion{1} \input{thesis.tex}" 
	bibtex thesis.aux
	pdflatex  "\def\supervisorversion{1} \input{thesis.tex}"
	pdflatex  "\def\supervisorversion{1} \input{thesis.tex}" 

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
