#!/usr/bin/env python
"""Test HTTP Server with CORS.

See: https://stackoverflow.com/questions/21956683/python-enable-access-control-on-simple-http-server
"""
import os
try:  # Python 3
    from http.server import HTTPServer, SimpleHTTPRequestHandler, test as test_orig
    import sys

    def test(*args):
        """Take port from first argument to match python2 BaseHTTPServer.test."""
        test_orig(*args, port=int(sys.argv[1]) if len(sys.argv) > 1 else 8000)

except ImportError:  # Python 2
    from BaseHTTPServer import HTTPServer, test
    from SimpleHTTPServer import SimpleHTTPRequestHandler


class CORSRequestHandler(SimpleHTTPRequestHandler):
    """Class adding CORS headers to SimpleHTTPRequestHandler."""

    def end_headers(self):
        """Add CORS header."""
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)


if __name__ == '__main__':
    dir = 'tmp'
    print("Starting server from %s directory" % (dir))
    os.chdir(dir)
    test(CORSRequestHandler, HTTPServer)
