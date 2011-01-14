#!/usr/bin/env python
# encoding: utf-8
"""
writer.py

Created by Stephen Altamirano on 2010-08-10.
"""

import nodes

class ExcelWriter(nodes.NodeSpawner):
    def __init__(self, path, compression=None):
        self.file = None
        self.path = path
        self.workbook = None
        self.writer = self
        self.compression = compression

    def __enter__(self):
        open_func = open
        if self.compression == 'gzip':
            import gzip
            open_func = gzip.open

        self.file = open_func(self.path, 'w')
        self.write("<?xml version=\"1.0\"?>\n")
        self.workbook = self.make_node('workbook', {
            "xmlns": "urn:schemas-microsoft-com:office:spreadsheet",
            "xmlns:o": "urn:schemas-microsoft-com:office:office",
            "xmlns:x": "urn:schemas-microsoft-com:office:office",
            "xmlns:ss": "urn:schemas-microsoft-com:office:spreadsheet",
            "xmlns:html": "http://www.w3.org/TR/REC-html40"
        })
        self.workbook.__enter__()
        return self

    def __exit__(self, t, value, traceback):
        self.workbook.__exit__(t, value, traceback)
        self.file.close()

    def write(self, content):
        self.file.write(content)