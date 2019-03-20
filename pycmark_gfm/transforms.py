"""
    pycmark_gfm.transforms
    ~~~~~~~~~~~~~~~~~~~~~~

    Transform classes for BlockParser.

    :copyright: Copyright 2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from docutils import nodes
from docutils.nodes import Element, Text, TextElement
from docutils.transforms import Transform
from pycmark.utils import transplant_nodes

from pycmark_gfm import addnodes


class StrikethroughConverter(Transform):
    default_priority = 900

    def apply(self, **kwargs) -> None:
        for node in self.document.traverse(TextElement):
            markers = list(n for n in node.children if isinstance(n, addnodes.strikethrough))
            while len(markers) >= 2:
                opener = markers.pop(0)
                closer = markers.pop(0)

                strikethrough = nodes.inline(classes=["strikethrough"])
                transplant_nodes(node, strikethrough, start=opener, end=closer)
                opener.replace_self(strikethrough)
                closer.parent.remove(closer)

            self.deactivate_markers(node)

    def deactivate_markers(self, node: Element) -> None:
        markers = list(n for n in node.children if isinstance(n, addnodes.strikethrough))
        for node in markers:
            marker = str(node)
            node.replace_self(Text(marker, marker))
