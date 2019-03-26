"""
    pycmark_gfm.inlineparser.std_processors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A parser for inline elements.

    :copyright: Copyright 2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

import re

from docutils import nodes
from docutils.nodes import Element, Text
from pycmark.inlineparser import PatternInlineProcessor
from pycmark.readers import TextReader
from pycmark.utils import ATTRIBUTE, entitytrans

from pycmark_gfm import addnodes


# 5.3 Task list items
class TaskListItemProcessor(PatternInlineProcessor):
    priority = 400
    pattern = re.compile(r'\[([xX ])\](?=\s+)')

    def run(self, reader: TextReader, document: Element) -> bool:
        if isinstance(document.parent, nodes.list_item) and reader.position == 0:
            checkmark = reader.consume(self.pattern).group(1)
            checked = checkmark.lower() == 'x'
            document += addnodes.checkbox(checked=checked)
            return True
        else:
            return False


# 6.2 Entity and numeric character references
class EntityReferenceProcessor(PatternInlineProcessor):
    # Shorten length a length of HTML entities than CommonMark
    pattern = re.compile(r'&(?:\w{1,32}|#\d{1,7}|#[xX][0-9A-Fa-f]{1,6});')

    def run(self, reader: TextReader, document: Element) -> bool:
        text = reader.consume(self.pattern).group(0)
        document += Text(entitytrans._unescape(text))
        return True


# 6.5 Strikethrough
class StrikethroughProcessor(PatternInlineProcessor):
    pattern = re.compile(r'(~~)')

    def run(self, reader: TextReader, document: Element) -> bool:
        reader.consume(self.pattern)
        document += addnodes.strikethrough()
        return True


# 6.9 Autolinks
class WWWAutolinkProcessor(PatternInlineProcessor):
    pattern = re.compile(r'www(\.[a-zA-Z0-9_\-]+){1,}[^ <]*')

    def run(self, reader: TextReader, document: Element) -> bool:
        uri = reader.consume(self.pattern).group(0)
        while True:
            length = self.get_trailing_punctuation_length(uri)
            if length == 0:
                break
            else:
                uri = uri[:-length]
                reader.step(-length)

        document += self.create_reference_node(uri)
        return True

    def create_reference_node(self, uri: str) -> nodes.reference:
        return nodes.reference(uri, uri, refuri='http://' + uri)

    def get_trailing_punctuation_length(self, uri: str) -> int:
        if re.search(r'[?!.,:*_~]$', uri):
            return 1
        elif uri.endswith(')') and uri.count('(') < uri.count(')'):
            return 1
        else:
            matched = re.search(r'&[a-zA-Z0-9]+;$', uri)
            if matched:
                return len(matched.group(0))

        return 0


# 6.9 Autolinks
class URLAutolinkProcessor(WWWAutolinkProcessor):
    pattern = re.compile(r'(?:http|https|ftp)://[a-zA-Z0-9_\-]+(\.[a-zA-Z0-9_\-]+){1,}[^ <]*')

    def create_reference_node(self, uri: str) -> nodes.reference:
        return nodes.reference(uri, uri, refuri=uri)


# 6.9 Autolinks
class EmailAutolinkProcessor(PatternInlineProcessor):
    pattern = re.compile(r'[a-zA-Z0-9.\-_+]+@[a-zA-Z0-9.\-_]+(\.[a-zA-Z0-9.\-_]+){1,}')

    def run(self, reader: TextReader, document: Element) -> bool:
        uri = reader.consume(self.pattern).group(0)
        while uri.endswith('.'):
            uri = uri[:-1]
            reader.step(-1)

        if uri.endswith(('-', '_')):
            reader.step(-len(uri))
            return False

        document += nodes.reference(uri, uri, refuri='mailto:' + uri)
        return True


# 6.11 Disallowed Raw HTML
class DisallowedRawHTMLProcessor(PatternInlineProcessor):
    priority = 200
    DISALLOWED_TAGS = r'<(?:title|textarea|style|xmp|iframe|noembed|noframes|script|plaintext)' + ATTRIBUTE + r'*\s*/?>'
    pattern = re.compile(DISALLOWED_TAGS, re.I)

    def run(self, reader: TextReader, document: Element) -> bool:
        tag = reader.consume(self.pattern).group(0)
        document += Text(tag, tag)
        return True
