#!/usr/bin/python
import json
import os.path
import subprocess
import unittest


class Book1TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        subprocess.call(["python", "iiif-static-book.py", "testdata/book1"])

    def test01_manifes(self):
        manifest_file = "tmp/book1/manifest.json"
        self.assertTrue(os.path.isfile(manifest_file))
        manifest = json.load(open(manifest_file, 'r'))
        self.assertEqual(manifest['label'], "Book book1")
        self.assertEqual(manifest['@id'], "http://localhost:9876/book1/manifest.json")
        self.assertEqual(manifest['@type'], "sc:Manifest")

    def test02_peges(self):
        for n in range(1, 11):
            page_dir = "tmp/book1/%08d" % n
            self.assertTrue(os.path.isdir(page_dir))


if __name__ == '__main__':
    unittest.main()
