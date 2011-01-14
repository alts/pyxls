#!/usr/bin/env python
# encoding: utf-8
"""
nodes.py

Created by Stephen Altamirano on 2010-08-23.
"""
from __future__ import with_statement

_ns_map = {
    "Name": "ss:",
    "Type": "ss:",
    "Formula": "ss:"
}

class NodeSpawner(object):
    def __getattr__(self, name):
        def inner(attrs = None):
            return self.make_node(name, attrs)
        return inner

    def make_node(self, name, attrs = None):
        if attrs is None:
            attrs = {}

        return BaseNode(name.capitalize(), self.writer, attrs)

    def table(self, attrs = None):
        return TableNode(self.writer, attrs)

    def data(self, contents, attrs = None):
        return DataNode(contents, self.writer, attrs)

    def formula(self, formula_text):
        return FormulaCellNode(formula_text, self.writer)

class BaseNode(NodeSpawner):
    def __init__(self, name, writer, attrs = None):
        self.name = name
        self.writer = writer
        self.attrs = attrs or {}

    def __enter__(self):
        self.writer.write("<%s%s>" % (self.name, self.print_attrs()))
        return self

    def __exit__(self, t, value, traceback):
        self.writer.write("</%s>\n" % self.name)

    def print_attrs(self):
        result = []
        for key, value in self.attrs.iteritems():
            result.extend(" %s=\"%s\"" % (_ns_map.get(key, "") + key, value))

        return "".join(result)


class TableNode(BaseNode):
    def __init__(self, writer, attrs = None):
        super(TableNode, self).__init__("Table", writer, attrs)
        self.row_counter = 0

    def row(self):
        self.row_counter += 1
        return RowNode(self.row_counter, self.writer, {})

    def write(self, *args):
        for arg in args:
            with self.row() as r:
                for i, item in enumerate(arg):
                    if isinstance(item, PseudoNode):
                        item.inform({
                            "coords": (r.index, i+1)
                        })
                        with item:
                            self.writer.write(item.content())
                    else:
                        if isinstance(item, BaseNode):
                            inner_data = item
                        elif isinstance(item, (int, str, float, unicode)):
                            inner_data = self.data(item)
                        elif item is None:
                            inner_data = None
                        else:
                            raise Exception(u"Bad item sent to Table: %s" % str(item))

                        with self.cell():
                            if inner_data:
                                with inner_data:
                                    self.writer.write(
                                        (u'%s' % inner_data.content()).encode('ascii', 'xmlcharrefreplace')
                                    )


class RowNode(BaseNode):
    def __init__(self, index, writer, attrs = None):
        self.index = index
        super(RowNode, self).__init__("Row", writer, attrs)


class DataNode(BaseNode):
    def __init__(self, contents, writer, attrs = None):
        attrs = attrs or {}

        self.contents = contents
        if isinstance(contents, (str, unicode)):
            attrs["Type"] = "String"
            attrs["xmlns"] = "http://www.w3.org/TR/REC-html40"
        elif isinstance(contents, int) or isinstance(contents, float):
            attrs["Type"] = "Number"
        else:
            raise Exception("Unacceptable content type for ")


        super(DataNode, self).__init__("ss:Data", writer, attrs)

    def content(self):
        return self.contents

class PseudoNode(BaseNode):
    def __init__(self, *args, **kwargs):
        self.info = {}
        super(PseudoNode, self).__init__(*args, **kwargs)

    def inform(self, info):
        self.info = info

    def content(self):
        return ""


class FormulaCellNode(PseudoNode):
    def __init__(self, formula, writer):
        super(FormulaCellNode, self).__init__("Cell", writer, {
            "Formula": formula
        })

    def __enter__(self):
        if "coords" in self.info:
            fsub = FormulaSubstituter(
                self.attrs["Formula"], self.info["coords"]
            )
            self.attrs["Formula"] = fsub.result()

        return super(FormulaCellNode, self).__enter__()

class FormulaSubstituter(object):
	def __init__(self, string, coords):
	    import re
	    self.string = string
	    self.groups = re.findall(r"(\{[^}]+\})", string)
	    self.coords = coords

	def result(self):
	    r, c = self.coords
	    for pattern in self.groups:
	        self.string = self.string.replace(pattern, str(eval(pattern[1:-1])))
	    return self.string
