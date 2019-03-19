#!/bin/bash

name="thesis"


# latex and bibtex everything
pdflatex $name
bibtex $name
pdflatex $name
pdflatex $name

# tidy up
rm *.aux $name.txt *.bbl *.blg *.log *.synctex.gz *.tex~

# display
evince $name.pdf &
