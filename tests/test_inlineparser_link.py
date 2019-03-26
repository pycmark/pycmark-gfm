"""
    test_inlineparser_link
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from docutils import nodes
from utils import publish, assert_node


def test_example_162():
    text = ("[Foo bar]:\n"
            "<my url>\n"
            "'title'\n"
            "\n"
            "[Foo bar]\n")
    result = publish(text)
    assert_node(result, [nodes.document, (nodes.target,
                                          [nodes.paragraph, nodes.reference, "Foo bar"])])
    assert_node(result[1][0], refuri="my%20url", reftitle="title")


def test_example_479():
    result = publish("[link](</my uri>)")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "link"])
    assert_node(result[0][0], refuri="/my%20uri")
