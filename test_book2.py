#!/usr/bin/python
import json
import os.path
import subprocess
import unittest


class Book2TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        subprocess.call(["python", "iiif-static-book.py", "testdata/book2"])

    def test01_manifest(self):
        manifest_file = "tmp/book2/manifest.json"
        self.assertTrue(os.path.isfile(manifest_file))
        manifest = json.load(open(manifest_file, 'r'))
        self.assertEqual(manifest['label'], "My Book 2")
        self.assertEqual(manifest['@id'], "http://localhost:9876/book2/manifest.json")
        self.assertEqual(manifest['@type'], "sc:Manifest")
        self.assertEqual(manifest['metadata'][0]['label'], "Author")
        self.assertEqual(manifest['metadata'][0]['value'], "Anne Author")
        # Info from metadata for page1
        canvas0 = manifest['sequences'][0]['canvases'][0]
        self.assertEqual(canvas0['label'], "First Page")
        # Info defaults for page2
        self.assertEqual(manifest['sequences'][0]['canvases'][1]['label'], "page2")

    def test02_pages(self):
        for n in range(1, 2):
            page_dir = "tmp/book2/page%d" % n
            self.assertTrue(os.path.isdir(page_dir))


if __name__ == '__main__':
    unittest.main()
