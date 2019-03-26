"""
    pycmark_gfm.inlineparser.link_processors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Link processor classes for InlineParser.

    :copyright: Copyright 2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

import re
from typing import Tuple

from docutils.nodes import Element
from pycmark.inlineparser import backtrack_onerror
from pycmark.inlineparser import link_processors as commonmark
from pycmark.inlineparser.link_processors import LinkTitleParser
from pycmark.readers import TextReader
from pycmark.utils import ESCAPED_CHARS


class LinkCloserProcessor(commonmark.LinkCloserProcessor):
    @backtrack_onerror
    def parse_link_destination(self, reader: TextReader, document: Element) -> Tuple[str, str]:
        reader.step()
        destination = LinkDestinationParser().parse(reader, document)
        title = LinkTitleParser().parse(reader, document)
        assert reader.consume(re.compile(r'\s*\)'))

        return destination, title


class LinkDestinationParser(commonmark.LinkDestinationParser):
    # spaces are allowed inside angle brackets
    pattern = re.compile(r'\s*<((?:[^<>\n\\]|' + ESCAPED_CHARS + r'|\\)*)>', re.S)
