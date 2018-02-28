#!/usr/bin/env python
"""Create static file IIIF instance for a book."""

import argparse
import glob
import logging
import os
import re
import sys

from iiif import IIIFStatic
from iiif_prezi.factory import ManifestFactory


class Page(object):
    """Class for data about a single page (one image)."""

    def __init__(self, image_file=None, identifier=None):
        """Initialize Page object."""
        self.image_file = image_file
        self.identifier = identifier
        self._title = None

    @property
    def info_json(self):
        """Construct info.json path."""
        return(self.identifier + '/info.json')

    @property
    def title(self):
        """Explicit or implicit page title."""
        if (self._title is None):
            t = self.identifier.replace("_", " ")
            if (re.match(r'''^[0-9]+$''', t)):
                t = 'p%d' % int(t)
            return(t)
        else:
            return(self._title)


def uri_join(*args):
    """Join URI path components."""
    return('/'.join(args))


def make_book(src, book_id,
              image_dir, image_uri,
              prezi_dir, prezi_uri,
              args):
    """Make tiles and manifest for one book from src."""
    # Get and convert pages
    logging.info("Looking at %s..." % (src))
    pages = []
    sg = IIIFStatic(dst=image_dir,
                    tilesize=args.tilesize,
                    api_version=args.api_version,
                    prefix=image_uri,
                    osd_version='2.0.0',
                    extras=['/full/90,/0/default.jpg',
                            '/full/200,/0/default.jpg'])  # thumbnail for UV
    for image_file in sorted(glob.glob(os.path.join(src, args.pattern))):
        identifier = os.path.split(os.path.splitext(image_file)[0])[1]
        logging.info("Page %s..." % (image_file))
        if (not args.skip_tiles):
            sg.generate(image_file)
        pages.append(Page(image_file=image_file,
                          identifier=identifier))
    if (len(pages) == 0):
        logging.fatal("No pages found matching glob --pattern '%s'" % (args.pattern))
        exit(1)
    # Write manifest
    fac = ManifestFactory()
    fac.set_debug("error")
    fac.set_base_image_uri(image_uri)
    fac.set_base_image_dir(image_dir)
    fac.set_iiif_image_info()
    fac.set_base_prezi_uri(prezi_uri)
    fac.set_base_prezi_dir(prezi_dir)
    mflbl = "Book " + os.path.split(image_dir)[1].replace("_", " ")
    mfst = fac.manifest(label=mflbl)
    seq = mfst.sequence()
    for page in pages:
        logging.debug("Adding %s as %s" % (page.identifier, page.title))
        canvas = seq.canvas(ident=page.identifier, label=page.title)
        # Make image annotation manually so we use disk info.json but real URI for @id
        anno = canvas.annotation()
        image = anno.image(ident=page.identifier, iiif=True)
        dbiu = fac.default_base_image_uri
        fac.default_base_image_uri = "file:" + image_dir
        image._identifier = page.identifier
        image.set_hw_from_iiif()
        fac.default_base_image_uri = dbiu
        canvas.set_hw(image.height, image.width)
    mfst.toFile(compact=False)
    manifest_uri = uri_join(prezi_uri, 'manifest.json')
    print("Expecting files in %s to be hosted as %s" % (prezi_dir, prezi_uri))
    print("View: http://universalviewer.io/uv.html?manifest=%s" % (manifest_uri))
    print()


def main():
    """Parse arguments, do it..."""
    if (sys.version_info < (3, 4)):
        sys.exit("This program requires python version 3.4 or later")

    p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument('--pattern', default="*.jpg",
                   help='Glob pattern to look for page images in src')
    p.add_argument('--dst', default='tmp',
                   help='Destination directory')
    p.add_argument('--base-uri', default='http://localhost:9876',
                   help='Base URI for images and/or presentation API manifest. Override either '
                        'with --base-image-uri or --base-prezi-uri')
    p.add_argument('--base-image-uri', default='',
                   help='Base URI for images, overrides value from --base-uri')
    p.add_argument('--base-image-dir', default='',
                   help='Base directory under --dst to write image tiles and info.json')
    p.add_argument('--base-prezi-uri', default='',
                   help='Base URI for presentation API manifest, overrides value from --base-uri')
    p.add_argument('--base-prezi-dir', default='',
                   help='Base directory under --dst to write presentation API manifest')
    # Control of static tiles
    p.add_argument('--skip-tiles', action='store_true',
                   help="Skip tile generation (assume has already been done on previous run")
    p.add_argument('--tilesize', action='store', type=int, default=512,
                   help="Tilesize in pixels")
    p.add_argument('--api-version', action='store', default='2.1',
                   help="Image API version")
    # General
    p.add_argument("-v", "--verbosity", action="count", default=0)
    p.add_argument('src', nargs=1, default=[])
    args = p.parse_args()

    # Logging
    logging.basicConfig(level=(logging.WARN if args.verbosity == 0 else (
                               logging.INFO if args.verbosity == 1 else
                               logging.DEBUG)))

    base_image_uri = args.base_image_uri if args.base_image_uri else args.base_uri
    base_prezi_uri = args.base_prezi_uri if args.base_prezi_uri else args.base_uri

    for src in args.src:
        src = src.rstrip('/')  # remove any trailing slash
        book_id = os.path.split(src)[1]
        print()
        print("Processing %s directory, will use book_id '%s'" % (src, book_id))
        # Set up base output dirs
        os.makedirs(args.dst, exist_ok=True)
        image_dir = os.path.join(args.dst, args.base_image_dir, book_id)
        os.makedirs(image_dir, exist_ok=True)
        prezi_dir = os.path.join(args.dst, args.base_prezi_dir, book_id)
        os.makedirs(prezi_dir, exist_ok=True)
        # Do it...
        make_book(src, book_id,
                  image_dir=image_dir, image_uri=uri_join(base_image_uri, book_id),
                  prezi_dir=prezi_dir, prezi_uri=uri_join(base_prezi_uri, book_id),
                  args=args)


if __name__ == '__main__':
    main()
