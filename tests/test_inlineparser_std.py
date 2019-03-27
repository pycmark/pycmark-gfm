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


def test_example_404():
    result = publish("*foo**bar*")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.emphasis, "foo**bar"])


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


def test_example_599():
    result = publish("www.commonmark.org")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "www.commonmark.org"])
    assert_node(result[0][0], refuri="http://www.commonmark.org")


def test_example_600():
    result = publish("Visit www.commonmark.org/help for more information.")
    assert_node(result, [nodes.document, nodes.paragraph, ("Visit ",
                                                           [nodes.reference, "www.commonmark.org/help"],
                                                           " for more information.")])
    assert_node(result[0][1], refuri="http://www.commonmark.org/help")


def test_example_601():
    text = ("Visit www.commonmark.org.\n"
            "\n"
            "Visit www.commonmark.org/a.b.\n")
    result = publish(text)
    assert_node(result, ([nodes.paragraph, ("Visit ",
                                            [nodes.reference, "www.commonmark.org"],
                                            ".")],
                         [nodes.paragraph, ("Visit ",
                                            [nodes.reference, "www.commonmark.org/a.b"],
                                            ".")]))
    assert_node(result[0][1], refuri="http://www.commonmark.org")
    assert_node(result[1][1], refuri="http://www.commonmark.org/a.b")


def test_example_602():
    text = ("www.google.com/search?q=Markup+(business)\n"
            "\n"
            "(www.google.com/search?q=Markup+(business))\n")
    result = publish(text)
    assert_node(result, ([nodes.paragraph, nodes.reference, "www.google.com/search?q=Markup+(business)"],
                         [nodes.paragraph, ("(",
                                            [nodes.reference, "www.google.com/search?q=Markup+(business)"],
                                            ")")]))
    assert_node(result[0][0], refuri="http://www.google.com/search?q=Markup+(business)")
    assert_node(result[1][1], refuri="http://www.google.com/search?q=Markup+(business)")


def test_example_603():
    text = "www.google.com/search?q=(business))+ok"
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, text])
    assert_node(result[0][0], refuri="http://www.google.com/search?q=(business))+ok")


def test_example_604():
    text = ("www.google.com/search?q=commonmark&hl=en\n"
            "\n"
            "www.google.com/search?q=commonmark&hl;\n")
    result = publish(text)
    assert_node(result, ([nodes.paragraph, nodes.reference, "www.google.com/search?q=commonmark&hl=en"],
                         [nodes.paragraph, ([nodes.reference, "www.google.com/search?q=commonmark"],
                                            "&hl;")]))
    assert_node(result[0][0], refuri="http://www.google.com/search?q=commonmark&hl=en")
    assert_node(result[1][0], refuri="http://www.google.com/search?q=commonmark")


def test_example_605():
    result = publish("www.commonmark.org/he<lp")
    assert_node(result, [nodes.document, nodes.paragraph, ([nodes.reference, "www.commonmark.org/he"],
                                                           "<lp")])
    assert_node(result[0][0], refuri="http://www.commonmark.org/he")


def test_example_606():
    text = ("http://commonmark.org\n"
            "\n"
            "(Visit https://encrypted.google.com/search?q=Markup+(business))\n"
            "\n"
            "Anonymous FTP is available at ftp://foo.bar.baz.\n")
    result = publish(text)
    assert_node(result, ([nodes.paragraph, nodes.reference, "http://commonmark.org"],
                         [nodes.paragraph, ("(Visit ",
                                            [nodes.reference,
                                             "https://encrypted.google.com/search?q=Markup+(business)"],
                                            ")")],
                         [nodes.paragraph, ("Anonymous FTP is available at ",
                                            [nodes.reference, "ftp://foo.bar.baz"],
                                            ".")]))
    assert_node(result[0][0], refuri="http://commonmark.org")
    assert_node(result[1][1], refuri="https://encrypted.google.com/search?q=Markup+(business)")
    assert_node(result[2][1], refuri="ftp://foo.bar.baz")


def test_example_607():
    result = publish("foo@bar.baz")
    assert_node(result, [nodes.document, nodes.paragraph, nodes.reference, "foo@bar.baz"])
    assert_node(result[0][0], refuri="mailto:foo@bar.baz")


def test_example_608():
    text = "hello@mail+xyz.example isn't valid, but hello+xyz@mail.example is."
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, ("hello@mail+xyz.example isn't valid, but ",
                                                           [nodes.reference, "hello+xyz@mail.example"],
                                                           " is.")])
    assert_node(result[0][1], refuri="mailto:hello+xyz@mail.example")


def test_example_609():
    text = ("a.b-c_d@a.b\n"
            "\n"
            "a.b-c_d@a.b.\n"
            "\n"
            "a.b-c_d@a.b-\n"
            "\n"
            "a.b-c_d@a.b_\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, nodes.reference, "a.b-c_d@a.b"],
                                          [nodes.paragraph, ([nodes.reference, "a.b-c_d@a.b"],
                                                             ".")],
                                          [nodes.paragraph, "a.b-c_d@a.b-"],
                                          [nodes.paragraph, "a.b-c_d@a.b_"])])
    assert_node(result[0][0], refuri="mailto:a.b-c_d@a.b")
    assert_node(result[1][0], refuri="mailto:a.b-c_d@a.b")


def test_example_618():
    text = ("< a><\n"
            "foo><bar/ >\n"
            "<foo bar=baz\n"
            "bim!bop />\n")
    result = publish(text)
    assert_node(result, [nodes.document, nodes.paragraph, text.rstrip()])


def test_example_631():
    text = ("<strong> <title> <style> <em>\n"
            "\n"
            "<blockquote>\n"
            "  <xmp> is disallowed.  <XMP> is also disallowed.\n"
            "</blockquote>\n")
    result = publish(text)
    assert_node(result, [nodes.document, ([nodes.paragraph, ([nodes.raw, "<strong>"],
                                                             " <title> <style> ",
                                                             [nodes.raw, "<em>"])],
                                          [nodes.raw, ("<blockquote>\n"
                                                       "  &lt;xmp> is disallowed.  &lt;XMP> is also disallowed.\n"
                                                       "</blockquote>\n")])])
