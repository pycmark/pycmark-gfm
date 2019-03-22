"""
    pycmark_gfm.addnodes
    ~~~~~~~~~~~~~~~~~~~~

    Additiona docutils nodes for pycmark-gfm.

    :copyright: Copyright 2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from docutils.nodes import Element


class checkbox(Element):
    """A node reprents a checkbox for task list item."""
    pass


class strikethrough(Element):
    """A node reprents a marker for strikethrough."""

    def __str__(self) -> str:
        return "~~"

    def astext(self) -> str:
        return str(self)
