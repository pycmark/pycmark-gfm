"""
    test_gfmspec
    ~~~~~~~~~~~~

    :copyright: Copyright 2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from gfm2html import convert


def test_gfmspec(gfmspec):
    example_id, source, expected = gfmspec
    assert convert(source) == expected
