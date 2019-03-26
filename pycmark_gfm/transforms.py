"""
    pycmark_gfm.transforms
    ~~~~~~~~~~~~~~~~~~~~~~

    Transform classes for BlockParser.

    :copyright: Copyright 2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

import re
from typing import cast

from docutils import nodes
from docutils.nodes import Element, Text, TextElement, fully_normalize_name
from docutils.transforms import Transform
from pycmark.inlineparser import backtrack_onerror
from pycmark.inlineparser.link_processors import LinkTitleParser
from pycmark.readers import TextReader
from pycmark.utils import ATTRIBUTE, ESCAPED_CHARS, normalize_link_label, transplant_nodes

from pycmark_gfm import addnodes
from pycmark_gfm.inlineparser.link_processors import LinkDestinationParser


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


class TaskListItemConverter(Transform):
    default_priority = 500

    def apply(self, **kwargs) -> None:
        for node in self.document.traverse(addnodes.checkbox):
            if node['checked']:
                html = '<input checked="checked" disabled="disabled" type="checkbox" />'
            else:
                html = '<input disabled="disabled" type="checkbox" />'

            node.replace_self(nodes.raw('', html, format='html'))


class LinkReferenceDefinitionDetector(Transform):
    default_priority = 100
    pattern = re.compile(r'\s*\[((?:[^\[\]\\]|' + ESCAPED_CHARS + r'|\\)+)\]:')

    def apply(self, **kwargs) -> None:
        for node in self.document.traverse(nodes.paragraph):
            reader = TextReader(cast(Text, node[0]))
            self.parse_linkref_definition(reader, node)

    @backtrack_onerror
    def parse_linkref_definition(self, reader: TextReader, node: nodes.paragraph) -> None:
        targets = []
        while True:
            matched = reader.consume(self.pattern)
            if not matched:
                break
            else:
                name = fully_normalize_name(matched.group(1))
                label = normalize_link_label(matched.group(1))
                if label.strip() == '':
                    break
                destination = LinkDestinationParser().parse(reader, node)
                if destination == '':
                    break
                position = reader.position
                title = LinkTitleParser().parse(reader, node)
                eol = reader.consume(re.compile('\\s*(\n|$)'))
                if eol is None:
                    # unknown text remains; no title?
                    reader.position = position
                    if reader.consume(re.compile('\\s*(\n|$)')):
                        target = nodes.target('', names=[label], refuri=destination)
                else:
                    target = nodes.target('', names=[name], refuri=destination, title=title)

                if label not in self.document.nameids:
                    self.document.note_explicit_target(target)
                else:
                    self.document.reporter.warning('Duplicate explicit target name: "%s"' % label,
                                                   source=node.source, line=node.line)
                targets.append(target)

        if targets:
            # insert found targets before the paragraph
            pos = node.parent.index(node)
            for target in reversed(targets):
                node.parent.insert(pos, target)

            if reader.remain:
                node.pop(0)
                node.insert(0, Text(reader.remain))
            else:
                node.parent.remove(node)


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
