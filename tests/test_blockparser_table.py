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
    assert_node(result[0][0][2], [nodes.thead, nodes.row, ([nodes.entry, "foo"],
                                                           [nodes.entry, "bar"])])
    assert_node(result[0][0][3], [nodes.tbody, nodes.row, ([nodes.entry, "baz"],
                                                           [nodes.entry, "bim"])])


def test_example_192():
    text = ("| abc | defghi |\n"
            ":-: | -----------:\n"
            "bar | baz\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.table, nodes.tgroup, (nodes.colspec,
                                                                     nodes.colspec,
                                                                     nodes.thead,
                                                                     nodes.tbody)])
    assert_node(result[0][0][2], [nodes.thead, nodes.row, ([nodes.entry, "abc"],
                                                           [nodes.entry, "defghi"])])
    assert_node(result[0][0][3], [nodes.tbody, nodes.row, ([nodes.entry, "bar"],
                                                           [nodes.entry, "baz"])])
    assert_node(result[0][0][2][0][0], align="center")
    assert_node(result[0][0][2][0][1], align="right")
    assert_node(result[0][0][3][0][0], align="center")
    assert_node(result[0][0][3][0][1], align="right")