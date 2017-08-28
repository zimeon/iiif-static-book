# Test book

Scan of some pages in `pages.pdf`

Extract low-res jpeg images with:

```
gs -dNOPAUSE -sDEVICE=jpeg -dFirstPage=1 -dLastPage=10 -sOutputFile=testdata/book1/%08d.jpg -dJPEGQ=80 -r200 -q testdata/book1/pages.pdf -c quit
```
 