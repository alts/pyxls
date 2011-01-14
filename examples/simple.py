#!/usr/bin/env python
# encoding: utf-8
"""
simple.py

Created by Stephen Altamirano on 2011-01-13
"""

from __future__ import with_statement
from pyxls.writer import ExcelWriter

with ExcelWriter('simple.xls') as w:
    with w.worksheet({'Name':'My First Spreadsheet'}) as ws:
        with ws.table() as t:
            t.write(
                ('This is the top row!',),
                ['Lists work too!'],
                (),
                ('That empty tuple is a blank row',),
                ('Column 1', 'Column2', 'Column3', 'Column4'),
                (1, 2, 3, 4, 5),
                (u'\u30e6\u30cb\u30b3\u30fc\u30c9', 'Friendly!')
            )