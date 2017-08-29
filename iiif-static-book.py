#!/usr/bin/env python
"""Create static file IIIF instance for a book."""

import argparse
import glob
import logging
import os
import sys

from iiif import IIIFStatic
from iiif_prezi.factory import ManifestFactory


class Page(object):

    def __init__(self, image_file=None, identifier=None):
        self.image_file = image_file
        self.identifier = identifier

    @property
    def info_json(self):
        return(self.identifier + '/info.json')


def main():
    """Parse arguments, do it..."""
    if (sys.version_info < (3, 4)):
        sys.exit("This program requires python version 3.4 or later")

    p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument('--pattern', default="*.jpg",
                   help='Glob pattern to look for page images in src')
    p.add_argument('--dst', default='tmp',
                   help='Destination directory')
    p.add_argument('--base-image-uri', default='http://localhost:9876')
    p.add_argument('--base-image-dir', default='')
    p.add_argument('--base-prezi-uri', default='http://localhost:9876')
    p.add_argument('--base-prezi-dir', default='')
    p.add_argument('--manifest_uri', default='http://localhost:9876/book/manifest.json')
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

    # Set up output
    os.makedirs(args.dst, exist_ok=True)
    image_dir = os.path.join(args.dst, args.base_image_dir)
    os.makedirs(image_dir, exist_ok=True)
    prezi_dir = os.path.join(args.dst, args.base_prezi_dir)
    os.makedirs(prezi_dir, exist_ok=True)

    # Get and convert pages
    pages = []
    sg = IIIFStatic(dst=image_dir, tilesize=args.tilesize,
                    api_version=args.api_version,
                    prefix=args.base_image_uri, osd_version='2.0.0')
    for src in args.src:
        logging.warning("Looking at %s..." % (src))
        for image_file in sorted(glob.glob(os.path.join(src, args.pattern))):
            identifier = os.path.split(os.path.splitext(image_file)[0])[1]
            logging.warn("Page %s..." % (image_file))
            if (not args.skip_tiles):
                sg.generate(image_file)   
            pages.append(Page(image_file=image_file,
                              identifier=identifier))
    # Write manifest
    fac = ManifestFactory()
    fac.set_debug("error")
    fac.set_base_image_uri("file:" + image_dir)  # use local image file info.json
    fac.set_base_image_dir(image_dir)
    fac.set_iiif_image_info()
    fac.set_base_prezi_uri(args.base_prezi_uri)
    fac.set_base_prezi_dir(prezi_dir)
    mflbl = "Book " + os.path.split(image_dir)[1].replace("_", " ")
    mfst = fac.manifest(label=mflbl)
    seq = mfst.sequence()
    for page in pages:
        ident = page.identifier
        title = ident.replace("_", " ")
        print("Title=" + title)
        canvas = seq.canvas(ident=ident, label=title)
        canvas.set_image_annotation(ident, True)
    mfst.toFile(compact=False)

if __name__ == '__main__':
    main()

