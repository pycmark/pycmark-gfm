"""
    pycmark_gfm.transforms
    ~~~~~~~~~~~~~~~~~~~~~~

    Transform classes for BlockParser.

    :copyright: Copyright 2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

import re

from docutils import nodes
from docutils.nodes import Element, Text, TextElement
from docutils.transforms import Transform
from pycmark.transforms import TextNodeConnector
from pycmark.utils import ATTRIBUTE, transplant_nodes

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

        # invoke TextNodeConnector after the processing
        self.document.transformer.add_transform(TextNodeConnector)

    def deactivate_markers(self, node: Element) -> None:
        markers = list(n for n in node.children if isinstance(n, addnodes.strikethrough))
        for node in markers:
            marker = str(node)
            node.replace_self(Text(marker, marker))


class TaskListItemConverter(Transform):
    default_priority = 500

    def apply(self, **kwargs) -> None:
        for node in self.document.traverse(addnodes.checkbox):
            if node['checked']:
                html = '<input checked="checked" disabled="disabled" type="checkbox" />'
            else:
                html = '<input disabled="disabled" type="checkbox" />'

            node.replace_self(nodes.raw('', html, format='html'))


class DisallowedRawHTMLTransform(Transform):
    default_priority = 500
    DISALLOWED_TAGS = (r'<((?:title|textarea|style|xmp|iframe|noembed|noframes|script|plaintext)' +
                       ATTRIBUTE + r'*\s*/?>)')
    pattern = re.compile(DISALLOWED_TAGS, re.I)

    def apply(self, **kwargs) -> None:
        for node in self.document.traverse(nodes.raw):
            if node['format'] == 'html':
                text = self.pattern.sub(r'&lt;\1', node.astext())
                node[0] = nodes.Text(text)
