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


# 6.11 Disallowed Raw HTML
class DisallowedRawHTMLProcessor(PatternInlineProcessor):
    DISALLOWED_TAGS = r'<(?:title|textarea|style|xmp|iframe|noembed|noframes|script|plaintext)' + ATTRIBUTE + r'*\s*/?>'
    pattern = re.compile(DISALLOWED_TAGS, re.I)

    def run(self, reader: TextReader, document: Element) -> bool:
        tag = reader.consume(self.pattern).group(0)
        document += Text(tag, tag)
        return True
