# iiif-static-book

**WORK IN PROGRESS**

Aim is to create a simple program that will generate a set of static tiles and a manifest for a set of images of a book. Based on:

  * Static tile generation: <https://github.com/zimeon/iiif/blob/master/iiif_static.py>
  * Manifest generation: <https://github.com/iiif-prezi/iiif-prezi/blob/master/examples/build-from-directory.py>

## Use

Generate tiles and manifest (in `tmp` by default, `-h` for help):

```
> ./iiif-static-book.py testdata/book1

Processing testdata/book1 directory, will use book_id 'book1'
Expecting files in tmp/book1 to be hosted as http://localhost:9876/book1
View: http://universalviewer.io/uv.html?manifest=http://localhost:9876/book1/manifest.json
```

Run web server (on port 9876) and load <http://universalviewer.io/uv.html?manifest=http://localhost:9876/book1/manifest.json> in browser:

```
> ./http-server-with-cors.py 9876
Starting server from tmp directory
Serving HTTP on 0.0.0.0 port 9876 ...
127.0.0.1 - - [13/Oct/2017 09:30:37] "GET /book1/manifest.json HTTP/1.1" 200 -
127.0.0.1 - - [13/Oct/2017 09:30:38] "GET /book1/00000001/info.json HTTP/1.1" 200 -
127.0.0.1 - - [13/Oct/2017 09:30:38] "GET /book1/00000001/full/90,/0/default.jpg?t=1507901438209 HTTP/1.1" 200 -
127.0.0.1 - - [13/Oct/2017 09:30:38] "GET /book1/00000002/full/90,/0/default.jpg?t=1507901438209 HTTP/1.1" 200 -
127.0.0.1 - - [13/Oct/2017 09:30:38] "GET /book1/00000003/full/90,/0/default.jpg?t=1507901438210 HTTP/1.1" 200 -
...
```
