"""
    pycmark_gfm.blockparser.container_processors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Table processor classes for BlockParser.

    :copyright: Copyright 2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

import re

from pycmark.blockparser import container_processors as commonmark


class BulletListProcessor(commonmark.BulletListProcessor):
    # an list item indented with 0-3 spaces is considered as consective item
    next_item_pattern = re.compile(r'^( {0,3}[-+*])([ \t]+.*|$)')


class NonEmptyBulletListProcessor(commonmark.NonEmptyBulletListProcessor):
    # an list item indented with 0-3 spaces is considered as consective item
    next_item_pattern = re.compile(r'^( {0,3}[-+*])([ \t]+.*|$)')


class OrderedListProcessor(commonmark.OrderedListProcessor):
    # an list item indented with 0-3 spaces is considered as consective item
    next_item_pattern = re.compile(r'^( {0,3}\d{1,9}[.)])([ \t]+.*|$)')


class OneBasedOrderedListProcessor(commonmark.OneBasedOrderedListProcessor):
    # an list item indented with 0-3 spaces is considered as consective item
    next_item_pattern = re.compile(r'^( {0,3}\d{1,9}[.)])([ \t]+.*|$)')
