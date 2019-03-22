"""
    test_inlineparser_std
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from docutils import nodes
from utils import publish, assert_node

from pycmark_gfm import addnodes


def test_example_272():
    text = ("- [ ] foo\n"
            "- [x] bar\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, ([nodes.list_item, (addnodes.checkbox,
                                                                                " foo")],
                                                             [nodes.list_item, (addnodes.checkbox,
                                                                                " bar")])])
    assert_node(result[0][0][0], addnodes.checkbox, checked=False)
    assert_node(result[0][1][0], addnodes.checkbox, checked=True)


def test_example_273():
    text = ("- [x] foo\n"
            "  - [ ] bar\n"
            "  - [x] baz\n"
            "- [ ] bim\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.bullet_list, ([nodes.list_item, (addnodes.checkbox,
                                                                                " foo",
                                                                                nodes.bullet_list)],
                                                             [nodes.list_item, (addnodes.checkbox,
                                                                                " bim")])])
    assert_node(result[0][0][2], [nodes.bullet_list, ([nodes.list_item, (addnodes.checkbox,
                                                                         " bar")],
                                                      [nodes.list_item, (addnodes.checkbox,
                                                                         " baz")])])
    assert_node(result[0][0][0], addnodes.checkbox, checked=True)
    assert_node(result[0][0][2][0][0], addnodes.checkbox, checked=False)
    assert_node(result[0][0][2][1][0], addnodes.checkbox, checked=True)
    assert_node(result[0][1][0], addnodes.checkbox, checked=False)


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
