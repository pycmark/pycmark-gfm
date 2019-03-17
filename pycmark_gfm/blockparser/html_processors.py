"""
    pycmark_gfm.blockparser.html_processors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    HTML processor classes for BlockParser.

    :copyright: Copyright 2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

import re

from pycmark.blockparser.html_processors import BaseHTMLBlockProcessor, STANDARD_HTML_TAGS


# meta tag is not a part of standard meta tags.
GFM_STANDARD_HTML_TAGS = tuple(e for e in STANDARD_HTML_TAGS if e != 'meta')


# 4.6 HTML blocks; Standard tags
class StandardTagsHTMLBlockProcessor(BaseHTMLBlockProcessor):
    pattern = re.compile(r'^ {0,3}</?(%s)( |>|/>|$)' % '|'.join(STANDARD_HTML_TAGS), re.I)
    closing_pattern = re.compile(r'^\s*$')
