# Test book 2

Source is LaTeX for a 2 page A6 document, compile to PDF with:

```
pdflatex book2.tex
```

Make low-res jpeg images with:

```
gs -dNOPAUSE -sDEVICE=jpeg -dFirstPage=1 -dLastPage=2  -sOutputFile=page%d.jpg -dJPEGQ=80 -r200 -q book2.pdf -c quit
```
