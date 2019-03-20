"""
    pycmark_gfm.inlineparser.std_processors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A parser for inline elements.

    :copyright: Copyright 2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

import re

from docutils.nodes import Element, Text
from pycmark.inlineparser import PatternInlineProcessor
from pycmark.readers import TextReader
from pycmark.utils import entitytrans


# 6.2 Entity and numeric character references
class EntityReferenceProcessor(PatternInlineProcessor):
    # Shorten length a length of HTML entities than CommonMark
    pattern = re.compile(r'&(?:\w{1,32}|#\d{1,7}|#[xX][0-9A-Fa-f]{1,6});')

    def run(self, reader: TextReader, document: Element) -> bool:
        text = reader.consume(self.pattern).group(0)
        document += Text(entitytrans._unescape(text))
        return True
