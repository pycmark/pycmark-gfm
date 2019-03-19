"""
    test_blockparser_table
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from docutils import nodes
from utils import publish, assert_node


def test_example_191():
    text = ("| foo | bar |\n"
            "| --- | --- |\n"
            "| baz | bim |\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.table, nodes.tgroup, (nodes.colspec,
                                                                     nodes.colspec,
                                                                     nodes.thead,
                                                                     nodes.tbody)])
    assert_node(result[0][0][2], [nodes.thead, nodes.row, ([nodes.entry, nodes.paragraph, "foo"],
                                                           [nodes.entry, nodes.paragraph, "bar"])])
    assert_node(result[0][0][3], [nodes.tbody, nodes.row, ([nodes.entry, nodes.paragraph, "baz"],
                                                           [nodes.entry, nodes.paragraph, "bim"])])


def test_example_192():
    text = ("| abc | defghi |\n"
            ":-: | -----------:\n"
            "bar | baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.table, nodes.tgroup, (nodes.colspec,
                                                                     nodes.colspec,
                                                                     nodes.thead,
                                                                     nodes.tbody)])
    assert_node(result[0][0][2], [nodes.thead, nodes.row, ([nodes.entry, nodes.paragraph, "abc"],
                                                           [nodes.entry, nodes.paragraph, "defghi"])])
    assert_node(result[0][0][3], [nodes.tbody, nodes.row, ([nodes.entry, nodes.paragraph, "bar"],
                                                           [nodes.entry, nodes.paragraph, "baz"])])
    assert_node(result[0][0][2][0][0], align="center")
    assert_node(result[0][0][2][0][1], align="right")
    assert_node(result[0][0][3][0][0], align="center")
    assert_node(result[0][0][3][0][1], align="right")


def test_example_193():
    text = ("| f\\|oo  |\n"
            "| ------ |\n"
            "| b `\\|` az |\n"
            "| b **\\|** im |\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.table, nodes.tgroup, (nodes.colspec,
                                                                     nodes.thead,
                                                                     nodes.tbody)])
    assert_node(result[0][0][1], [nodes.thead, nodes.row, nodes.entry, nodes.paragraph, "f|oo"])
    assert_node(result[0][0][2], [nodes.tbody, ([nodes.row, nodes.entry, nodes.paragraph, ("b ",
                                                                                           [nodes.literal, "|"],
                                                                                           " az")],
                                                [nodes.row, nodes.entry, nodes.paragraph, ("b ",
                                                                                           [nodes.strong, "|"],
                                                                                           " im")])])


def test_example_194():
    text = ("| abc | def |\n"
            "| --- | --- |\n"
            "| bar | baz |\n"
            "> bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.table, nodes.tgroup, (nodes.colspec,
                                                                       nodes.colspec,
                                                                       nodes.thead,
                                                                       nodes.tbody)],
                                          [nodes.block_quote, nodes.paragraph, "bar"])])
    assert_node(result[0][0][2], [nodes.thead, nodes.row, ([nodes.entry, nodes.paragraph, "abc"],
                                                           [nodes.entry, nodes.paragraph, "def"])])
    assert_node(result[0][0][3], [nodes.tbody, nodes.row, ([nodes.entry, nodes.paragraph, "bar"],
                                                           [nodes.entry, nodes.paragraph, "baz"])])


def test_example_195():
    text = ("| abc | def |\n"
            "| --- | --- |\n"
            "| bar | baz |\n"
            "bar\n"
            "\n"
            "bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.table, nodes.tgroup, (nodes.colspec,
                                                                       nodes.colspec,
                                                                       nodes.thead,
                                                                       nodes.tbody)],
                                          [nodes.paragraph, "bar"])])
    assert_node(result[0][0][2], [nodes.thead, nodes.row, ([nodes.entry, nodes.paragraph, "abc"],
                                                           [nodes.entry, nodes.paragraph, "def"])])
    assert_node(result[0][0][3], [nodes.tbody, ([nodes.row, ([nodes.entry, nodes.paragraph, "bar"],
                                                             [nodes.entry, nodes.paragraph, "baz"])],
                                                [nodes.row, ([nodes.entry, nodes.paragraph, "bar"],
                                                             nodes.entry)])])


def test_example_196():
    text = ("| abc | def |\n"
            "| --- |\n"
            "| bar |\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, text.strip()])


def test_example_197():
    text = ("| abc | def |\n"
            "| --- | --- |\n"
            "| bar |\n"
            "| bar | baz | boo |\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.table, nodes.tgroup, (nodes.colspec,
                                                                     nodes.colspec,
                                                                     nodes.thead,
                                                                     nodes.tbody)])
    assert_node(result[0][0][2], [nodes.thead, nodes.row, ([nodes.entry, nodes.paragraph, "abc"],
                                                           [nodes.entry, nodes.paragraph, "def"])])
    assert_node(result[0][0][3], [nodes.tbody, ([nodes.row, ([nodes.entry, nodes.paragraph, "bar"],
                                                             nodes.entry)],
                                                [nodes.row, ([nodes.entry, nodes.paragraph, "bar"],
                                                             [nodes.entry, nodes.paragraph, "baz"])])])


def test_example_198():
    text = ("| abc | def |\n"
            "| --- | --- |\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.table, nodes.tgroup, (nodes.colspec,
                                                                     nodes.colspec,
                                                                     nodes.thead)])
    assert_node(result[0][0][2], [nodes.thead, nodes.row, ([nodes.entry, nodes.paragraph, "abc"],
                                                           [nodes.entry, nodes.paragraph, "def"])])
