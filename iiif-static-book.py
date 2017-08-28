#!/usr/bin/env python
"""Create static file IIIF instance for a book."""

import argparse
import glob
import logging
import os
import sys

from iiif import IIIFStatic
from iiif_prezi.factory import ManifestFactory

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
        for page in sorted(glob.glob(os.path.join(src, args.pattern))):
            logging.warn("Page %s..." % (page))
            sg.generate(page)
            pages.append(page)
    # Write manifest
    fac = ManifestFactory()
    fac.set_debug("error")
    fac.set_base_image_uri(args.base_image_uri)
    fac.set_base_image_dir(image_dir)
    fac.set_iiif_image_info()
    fac.set_base_prezi_uri(args.base_prezi_uri)
    fac.set_base_prezi_dir(prezi_dir)
    mflbl = os.path.split(image_dir)[1].replace("_", " ").title()
    mfst = fac.manifest(label=mflbl)
    seq = mfst.sequence()
    for page in pages:
        ident = os.path.splitext(page)[0]
        title = ident.replace("_", " ").title()
        cvs = seq.canvas(ident=ident, label=title)
        cvs.add_image_annotation(ident, True)
    mfst.toFile(compact=False)

if __name__ == '__main__':
    main()

