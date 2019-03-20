"""
    test_inlineparser_std
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from docutils import nodes
from utils import publish, assert_node


def test_example_315():
    result = publish("&#35; &#1234; &#992; &#0;")
    assert_node(result, [nodes.document, nodes.paragraph, "# Ӓ Ϡ �"])


def test_example_316():
    result = publish("&#X22; &#XD06; &#xcab;")
    assert_node(result, [nodes.document, nodes.paragraph, '" ആ ಫ'])


def test_example_317():
    text = ("&nbsp &x; &#; &#x;\n"
            "&#987654321;\n"
            "&#abcdef0;\n"
            "&ThisIsNotDefined; &hi?;")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, ("&nbsp &x; &#; &#x;\n"
                                                           "&#987654321;\n"
                                                           "&#abcdef0;\n"
                                                           "&ThisIsNotDefined; &hi?;")])


def test_example_472():
    result = publish("~~Hi~~ Hello, world!")
    assert_node(result, [nodes.document, nodes.paragraph, ([nodes.inline, "Hi"],
                                                           " Hello, world!")])


def test_example_473():
    text = ("This ~~has a\n"
            "\n"
            "new paragraph~~.\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, "This ~~has a"],
                                          [nodes.paragraph, "new paragraph~~."])])
