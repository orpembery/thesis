# Things in this Makefile have been taken from http://matt.might.net/articles/intro-to-make/

.SUFFIXES: .tex .pdf

all: thesis.pdf

.tex.pdf:
	pdflatex $<
	bibtex thesis.aux
	pdflatex $<
	pdflatex $<
